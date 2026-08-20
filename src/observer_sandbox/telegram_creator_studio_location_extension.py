from __future__ import annotations

import json
import sqlite3

from .creator_studio import CreatorStudioError, active_draft
from .creator_studio_location import (
    approve_location_draft,
    manual_location_draft,
    manual_location_template,
)


def _location_payload(draft: dict[str, object] | None) -> dict[str, object] | None:
    if not draft or draft.get("creation_type") != "location":
        return None
    proposal = draft.get("proposal")
    if not isinstance(proposal, dict):
        return None
    properties = proposal.get("properties")
    if not isinstance(properties, dict):
        return None
    payload = properties.get("location_payload")
    return payload if isinstance(payload, dict) else None


def install_location_creator_studio_extension(base) -> None:
    original_manual_draft = base.manual_draft
    original_create_type_view = base._create_type_view
    original_method_view = base._method_view
    original_prompt_view = base._prompt_view
    original_draft_preview = base.draft_preview_view
    original_callback = base.studio_callback_view

    def _session_expected(conn: sqlite3.Connection, user_id: int) -> str:
        session = base._session(conn, user_id)
        return str(session.get("expected_input") or "") if session else ""

    def manual_draft(conn, user_id, creation_type, raw, **kwargs):
        if creation_type == "location" and _session_expected(conn, user_id) == "location-json":
            return manual_location_draft(conn, user_id, raw, **kwargs)
        return original_manual_draft(conn, user_id, creation_type, raw, **kwargs)

    def create_type_view():
        # Preserve the already-installed Item extension's Creation Type surface.
        return original_create_type_view()

    def method_view(creation_type: str):
        if creation_type != "location":
            return original_method_view(creation_type)
        return (
            "📍 CREATE LOCATION\n━━━━━━━━━━━━━━━━━━\n"
            "Manual full-schema Location creation is now available.\n\n"
            "Use Exact location-v2 JSON for this slice. AI authoring is added separately after the Manual vertical is accepted.",
            [
                [{"text": "🧾 Location · Exact JSON", "callback_data": "sw:cs:input:location:manual"}],
                [{"text": "← Creation Type", "callback_data": "sw:cs:create"}],
            ],
        )

    def prompt_view(creation_type: str, input_mode: str):
        if creation_type != "location" or input_mode != "manual":
            return original_prompt_view(creation_type, input_mode)
        template = json.dumps(manual_location_template(), ensure_ascii=False, indent=2)
        return (
            "📍 LOCATION · EXACT JSON\n━━━━━━━━━━━━━━━━━━\n"
            "Send one complete location-v2 JSON object as your next message.\n"
            "The exact Location validator runs before a draft is saved. Graph references are validated again on approval.\n\n"
            "Example sparse template:\n"
            f"{template}\n\n"
            "Unknown facts should stay null/empty rather than being invented. Do not add grade or derived fields.",
            [
                [{"text": "← Change Method", "callback_data": "sw:cs:type:location"}],
                [{"text": "✕ Cancel", "callback_data": "sw:cs:input:cancel"}],
            ],
        )

    def draft_preview_view(conn: sqlite3.Connection, user_id: int, *, notice: str | None = None):
        draft = active_draft(conn, user_id)
        payload = _location_payload(draft)
        if payload is None:
            return original_draft_preview(conn, user_id, notice=notice)
        identity = payload.get("identity") if isinstance(payload.get("identity"), dict) else {}
        structure = payload.get("structure") if isinstance(payload.get("structure"), dict) else {}
        geography = payload.get("geography") if isinstance(payload.get("geography"), dict) else {}
        spatial = payload.get("spatial") if isinstance(payload.get("spatial"), dict) else {}
        topology = payload.get("topology") if isinstance(payload.get("topology"), dict) else {}
        facilities = payload.get("facilities") if isinstance(payload.get("facilities"), dict) else {}
        operations = payload.get("operations") if isinstance(payload.get("operations"), dict) else {}
        control = payload.get("control") if isinstance(payload.get("control"), dict) else {}

        represented_geo = [
            value for value in (
                geography.get("address_text"), geography.get("locality"), geography.get("region"), geography.get("country_code")
            ) if value
        ]
        dimensions = [key for key in ("area", "length", "width", "height", "elevation") if spatial.get(key) is not None]
        interfaces = topology.get("interfaces") if isinstance(topology.get("interfaces"), list) else []
        capabilities = facilities.get("capabilities") if isinstance(facilities.get("capabilities"), list) else []

        lines = [
            "📋 LOCATION SANDBOX DRAFT",
            "━━━━━━━━━━━━━━━━━━",
            f"Name: {identity.get('name', 'Unnamed')}",
            f"Kind: {str(identity.get('kind', '—')).replace('_', ' ').title()}",
            f"Exposure: {str(structure.get('exposure', '—')).replace('_', ' ').title()}",
            f"Revision: {draft.get('revision') if draft else '—'}",
            "",
            str(identity.get("description") or "No description."),
            "",
            f"Parent: {structure.get('parent_ref') or 'Root / none'}",
            f"Geography: {', '.join(str(v) for v in represented_geo) if represented_geo else 'Not specified'}",
            f"Spatial facts: {', '.join(dimensions) if dimensions else 'None represented'}",
            f"Interfaces: {len(interfaces)}",
            f"Capabilities: {', '.join(str(v) for v in capabilities) if capabilities else '—'}",
            f"Initial operation: {operations.get('initial_state', '—')}",
            f"Ownership: {str(control.get('ownership_class', '—')).replace('_', ' ')}",
            "",
            "Exact location-v2 source validation passed for this draft.",
            "Approval revalidates same-Sandbox graph references and materializes the Location atomically.",
            "Created does not mean runtime-ready/running, and no canonical Real World state is changed.",
        ]
        if notice:
            lines.extend(["", notice])
        return "\n".join(lines), [
            [{"text": "📄 Export Full Draft (.txt)", "callback_data": "sw:cs:export"}],
            [{"text": "✅ Approve into Sandbox", "callback_data": "sw:cs:approve"}],
            [{"text": "✕ Cancel Draft", "callback_data": "sw:cs:cancel"}],
            [{"text": "← Creator Studio", "callback_data": "sw:studio"}],
        ]

    def begin_location_session(conn: sqlite3.Connection, user_id: int) -> None:
        conn.execute(
            """
            INSERT INTO creation_sandbox_studio_sessions(
                sandbox_id,user_id,creation_type,input_mode,expected_input,prompt_chat_id,prompt_message_id
            ) VALUES('creator-default',?,'location','manual','location-json',NULL,NULL)
            ON CONFLICT(sandbox_id,user_id) DO UPDATE SET
                creation_type='location',input_mode='manual',expected_input='location-json',
                prompt_chat_id=NULL,prompt_message_id=NULL,updated_at=CURRENT_TIMESTAMP
            """,
            (int(user_id),),
        )
        conn.commit()

    def studio_callback_view(conn: sqlite3.Connection, user_id: int, callback_data: str):
        if callback_data == "sw:cs:type:location":
            base._clear_session(conn, user_id)
            base._restore_input_router()
            return method_view("location")
        if callback_data == "sw:cs:input:location:manual":
            begin_location_session(conn, user_id)
            base._install_input_router()
            return prompt_view("location", "manual")

        draft = active_draft(conn, user_id)
        if draft and draft.get("creation_type") == "location" and _location_payload(draft) is not None:
            if callback_data == "sw:cs:preview":
                return draft_preview_view(conn, user_id)
            if callback_data.startswith("sw:cs:approve:confirm:"):
                try:
                    expected_revision = int(callback_data.rsplit(":", 1)[-1])
                    obj = approve_location_draft(conn, user_id, expected_revision)
                except (CreatorStudioError, ValueError, TypeError) as exc:
                    return draft_preview_view(conn, user_id, notice=f"Approval rejected: {exc}")
                source = obj.get("source") if isinstance(obj.get("source"), dict) else {}
                identity = source.get("identity") if isinstance(source.get("identity"), dict) else {}
                return (
                    "✅ SANDBOX LOCATION APPROVED\n━━━━━━━━━━━━━━━━━━\n"
                    f"Location: {identity.get('name', obj.get('object_id', 'Location'))}\n"
                    f"ID: {obj.get('object_id', '—')}\n\n"
                    "Materialized in Creation Sandbox only. Runtime is not started and canonical Real World remains unchanged.",
                    [
                        [{"text": "🛠 Creator Studio", "callback_data": "sw:studio"}],
                        [{"text": "🌌 Sandbox World", "callback_data": "sw:world"}],
                    ],
                )
        return original_callback(conn, user_id, callback_data)

    base.manual_draft = manual_draft
    base._create_type_view = create_type_view
    base._method_view = method_view
    base._prompt_view = prompt_view
    base.draft_preview_view = draft_preview_view
    base.studio_callback_view = studio_callback_view
