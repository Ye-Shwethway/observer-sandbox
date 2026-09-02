from __future__ import annotations

import sqlite3

from .creator_studio import CreatorStudioError, active_draft
from .creator_studio_location_composition import (
    approve_location_composition_draft,
    composition_from_draft,
    manual_location_composition_draft,
    preview_location_composition_draft,
    start_location_composition_draft,
)


def install_location_composition_creator_studio_extension(base) -> None:
    original_manual_draft = base.manual_draft
    original_method_view = base._method_view
    original_draft_preview = base.draft_preview_view
    original_callback = base.studio_callback_view

    def _session_expected(conn: sqlite3.Connection, user_id: int) -> str:
        session = base._session(conn, user_id)
        return str(session.get("expected_input") or "") if session else ""

    def _begin_composition_session(conn: sqlite3.Connection, user_id: int) -> None:
        conn.execute(
            """
            INSERT INTO creation_sandbox_studio_sessions(
                sandbox_id,user_id,creation_type,input_mode,expected_input,prompt_chat_id,prompt_message_id
            ) VALUES('creator-default',?,'location','manual','location-composition-json',NULL,NULL)
            ON CONFLICT(sandbox_id,user_id) DO UPDATE SET
                creation_type='location',input_mode='manual',expected_input='location-composition-json',
                prompt_chat_id=NULL,prompt_message_id=NULL,updated_at=CURRENT_TIMESTAMP
            """,
            (int(user_id),),
        )
        conn.commit()

    def manual_draft(conn, user_id, creation_type, raw, **kwargs):
        if creation_type == "location" and _session_expected(conn, user_id) == "location-composition-json":
            return manual_location_composition_draft(conn, user_id, raw, **kwargs)
        return original_manual_draft(conn, user_id, creation_type, raw, **kwargs)

    def method_view(creation_type: str):
        if creation_type != "location":
            return original_method_view(creation_type)
        text, keyboard = original_method_view(creation_type)
        rows = list(keyboard)
        insert_at = max(0, len(rows) - 1)
        rows[insert_at:insert_at] = [
            [{"text": "🧩 Nested Composition · Starter", "callback_data": "sw:cs:location:composition:starter"}],
            [{"text": "🧾 Nested Composition · Exact JSON", "callback_data": "sw:cs:location:composition:json"}],
        ]
        return (
            text
            + "\n\nNested Composition creates a reviewed Location graph with exact location-v2 children and exact item-v1 members in one atomic approval.",
            rows,
        )

    def composition_prompt_view():
        return (
            "🧩 LOCATION · NESTED COMPOSITION\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Send one complete location-composition-v1 JSON object as your next message.\n\n"
            "Envelope:\n"
            "• schema_version = location-composition-v1\n"
            "• locations = [{ref, payload: exact location-v2}]\n"
            "• items = [{ref, payload: exact item-v1}]\n\n"
            "Use $ref for same-composition parent, topology, located_at or stored_in targets. "
            "The complete dependency graph is validated before the draft is saved. No member is materialized until explicit approval.",
            [
                [{"text": "🧩 Use Starter Instead", "callback_data": "sw:cs:location:composition:starter"}],
                [{"text": "← Change Method", "callback_data": "sw:cs:type:location"}],
                [{"text": "✕ Cancel", "callback_data": "sw:cs:input:cancel"}],
            ],
        )

    def draft_preview_view(conn: sqlite3.Connection, user_id: int, *, notice: str | None = None):
        draft = active_draft(conn, user_id)
        envelope = composition_from_draft(draft)
        if envelope is None:
            return original_draft_preview(conn, user_id, notice=notice)
        try:
            preview = preview_location_composition_draft(conn, user_id)
        except CreatorStudioError as exc:
            return original_draft_preview(conn, user_id, notice=notice or f"Composition validation failed: {exc}")

        lines = [
            "🧩 LOCATION COMPOSITION DRAFT",
            "━━━━━━━━━━━━━━━━━━",
            f"Revision: {draft.get('revision', '—') if draft else '—'}",
            f"Locations: {len(preview['locations'])}",
            f"Items: {len(preview['items'])}",
            f"Total members: {preview['count']}",
            "",
            "Locations",
        ]
        for entry in preview["locations"]:
            source = entry["source"]
            identity = source["identity"]
            parent = source["structure"]["parent_ref"] or "root / none"
            lines.append(
                f"• ${entry['ref']} · {identity['name']} · {identity['kind']} · parent={parent}"
            )
        lines.extend(["", "Items"])
        if preview["items"]:
            for entry in preview["items"]:
                definition = entry["normalized"]["definition"]
                relations = entry.get("resolved_relationships") or []
                placement = ", ".join(
                    f"{relation['relation_type']}→"
                    + (f"${relation['target']}" if relation["target_kind"] in {"location", "item"} else str(relation["target"]))
                    for relation in relations
                ) or "no placement relation"
                lines.append(f"• ${entry['ref']} · {definition['name']} · {placement}")
        else:
            lines.append("• none")
        lines.extend(
            [
                "",
                "✅ Exact member and dependency validation passed.",
                "Preview/export are write-free for composition members.",
                "One revision-bound approval materializes the complete graph atomically in Creation Sandbox only.",
                "Created members are not runtime-started and canonical Real World state is unchanged.",
            ]
        )
        if notice:
            lines.extend(["", notice])
        return "\n".join(lines), [
            [{"text": "📄 Export Full Draft (.txt)", "callback_data": "sw:cs:export"}],
            [{"text": "✅ Approve Whole Composition", "callback_data": "sw:cs:approve"}],
            [{"text": "🧾 Replace with Exact JSON", "callback_data": "sw:cs:location:composition:json"}],
            [{"text": "✕ Cancel Draft", "callback_data": "sw:cs:cancel"}],
            [{"text": "← Creator Studio", "callback_data": "sw:studio"}],
        ]

    def approval_confirmation_view(conn: sqlite3.Connection, user_id: int):
        draft = active_draft(conn, user_id)
        envelope = composition_from_draft(draft)
        if draft is None or envelope is None:
            return draft_preview_view(conn, user_id)
        try:
            preview = preview_location_composition_draft(conn, user_id)
        except CreatorStudioError as exc:
            return draft_preview_view(conn, user_id, notice=f"Approval preflight rejected: {exc}")
        revision = int(draft["revision"])
        return (
            "⚠️ CONFIRM COMPOSITION APPROVAL\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"Draft revision: {revision}\n"
            f"Locations: {len(preview['locations'])}\n"
            f"Items: {len(preview['items'])}\n"
            f"Total members: {preview['count']}\n\n"
            "This exact reviewed revision will be applied as one Sandbox-only transaction. "
            "Any member/ref/dependency failure aborts the whole graph. No runtime activation or Real World mutation is authorized.",
            [
                [{"text": "✅ Confirm Whole Composition", "callback_data": f"sw:cs:approve:confirm:{revision}"}],
                [{"text": "← Review Draft", "callback_data": "sw:cs:preview"}],
            ],
        )

    def studio_callback_view(conn: sqlite3.Connection, user_id: int, callback_data: str):
        if callback_data == "sw:cs:location:composition:starter":
            base._clear_session(conn, user_id)
            base._restore_input_router()
            try:
                start_location_composition_draft(conn, user_id)
            except CreatorStudioError as exc:
                return method_view("location")[0] + f"\n\nStarter rejected: {exc}", method_view("location")[1]
            return draft_preview_view(
                conn,
                user_id,
                notice="✅ Starter graph loaded: Property → child Room → movable Item.",
            )
        if callback_data == "sw:cs:location:composition:json":
            _begin_composition_session(conn, user_id)
            base._install_input_router()
            return composition_prompt_view()

        draft = active_draft(conn, user_id)
        if composition_from_draft(draft) is not None:
            if callback_data == "sw:cs:preview":
                return draft_preview_view(conn, user_id)
            if callback_data == "sw:cs:approve":
                return approval_confirmation_view(conn, user_id)
            if callback_data.startswith("sw:cs:approve:confirm:"):
                try:
                    expected_revision = int(callback_data.rsplit(":", 1)[-1])
                    created = approve_location_composition_draft(conn, user_id, expected_revision)
                except (CreatorStudioError, ValueError, TypeError) as exc:
                    return draft_preview_view(conn, user_id, notice=f"Approval rejected: {exc}")
                refs = created.get("refs") or {}
                return (
                    "✅ SANDBOX COMPOSITION APPROVED\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"Locations: {len(created.get('locations') or [])}\n"
                    f"Items: {len(created.get('items') or [])}\n"
                    f"Members: {len(refs)}\n\n"
                    "The complete graph was materialized atomically in Creation Sandbox only. "
                    "No member was runtime-started and canonical Real World state remains unchanged.",
                    [
                        [{"text": "🌌 Sandbox World", "callback_data": "sw:world"}],
                        [{"text": "🛠 Creator Studio", "callback_data": "sw:studio"}],
                    ],
                )
        return original_callback(conn, user_id, callback_data)

    base.manual_draft = manual_draft
    base._method_view = method_view
    base.draft_preview_view = draft_preview_view
    base.studio_callback_view = studio_callback_view
