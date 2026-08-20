from __future__ import annotations

import json
import sqlite3

from .creator_studio import CreatorStudioError, active_draft
from .creator_studio_item import (
    ai_item_draft,
    approve_item_draft,
    manual_item_draft,
    manual_item_template,
    reroll_item_draft,
)
from .creator_studio_item_batch import (
    ai_item_batch_draft,
    approve_item_batch_draft,
    manual_item_batch_draft,
    reroll_item_batch_draft,
)


def _item_payload(draft: dict[str, object] | None) -> dict[str, object] | None:
    if not draft or draft.get("creation_type") != "item":
        return None
    proposal = draft.get("proposal")
    if not isinstance(proposal, dict):
        return None
    properties = proposal.get("properties")
    if not isinstance(properties, dict):
        return None
    payload = properties.get("item_payload")
    return payload if isinstance(payload, dict) else None


def _batch_entries(draft: dict[str, object] | None) -> list[dict[str, object]] | None:
    if not draft or draft.get("creation_type") != "item":
        return None
    proposal = draft.get("proposal")
    if not isinstance(proposal, dict):
        return None
    properties = proposal.get("properties")
    if not isinstance(properties, dict):
        return None
    batch = properties.get("item_batch")
    if not isinstance(batch, dict):
        return None
    items = batch.get("items")
    if not isinstance(items, list) or not all(isinstance(entry, dict) for entry in items):
        return None
    return items


def install_item_creator_studio_extension(base) -> None:
    original_manual_draft = base.manual_draft
    original_ai_draft = base.ai_draft
    original_prompt_view = base._prompt_view
    original_draft_preview = base.draft_preview_view
    original_callback = base.studio_callback_view

    def _session_expected(conn: sqlite3.Connection, user_id: int) -> str:
        session = base._session(conn, user_id)
        return str(session.get("expected_input") or "") if session else ""

    def manual_draft(conn, user_id, creation_type, raw, **kwargs):
        if creation_type == "item":
            if _session_expected(conn, user_id) == "item-batch-json":
                return manual_item_batch_draft(conn, user_id, raw, **kwargs)
            return manual_item_draft(conn, user_id, raw, **kwargs)
        return original_manual_draft(conn, user_id, creation_type, raw, **kwargs)

    def ai_draft(conn, user_id, creation_type, prompt_text, **kwargs):
        if creation_type == "item":
            if _session_expected(conn, user_id) == "item-batch-description":
                return ai_item_batch_draft(conn, user_id, prompt_text, **kwargs)
            return ai_item_draft(conn, user_id, prompt_text, **kwargs)
        return original_ai_draft(conn, user_id, creation_type, prompt_text, **kwargs)

    def create_type_view():
        return (
            "➕ CREATE IN SANDBOX\n━━━━━━━━━━━━━━━━━━\nChoose what you want to create.",
            [
                [
                    {"text": "👤 Character", "callback_data": "sw:cs:type:character"},
                    {"text": "📍 Location", "callback_data": "sw:cs:type:location"},
                ],
                [{"text": "📦 Item", "callback_data": "sw:cs:type:item"}],
                [{"text": "← Creator Studio", "callback_data": "sw:studio"}],
            ],
        )

    def method_view(creation_type: str):
        if creation_type != "item":
            return base._original_item_method_view(creation_type)
        return (
            "📦 CREATE ITEM\n━━━━━━━━━━━━━━━━━━\nChoose single Item or atomic Item batch creation.\n\n"
            "AI is the easiest path. Exact JSON is available for advanced control.",
            [
                [{"text": "✨ Single Item · AI", "callback_data": "sw:cs:input:item:ai"}],
                [{"text": "📦 Item Batch · AI", "callback_data": "sw:cs:input:item:batch-ai"}],
                [{"text": "🧾 Single Item · Exact JSON", "callback_data": "sw:cs:input:item:manual"}],
                [{"text": "🗂 Batch · Exact JSON", "callback_data": "sw:cs:input:item:batch-manual"}],
                [{"text": "← Creation Type", "callback_data": "sw:cs:create"}],
            ],
        )

    def prompt_view(creation_type: str, input_mode: str):
        if creation_type != "item":
            return original_prompt_view(creation_type, input_mode)
        if input_mode == "batch-ai":
            return (
                "📦 ITEM BATCH · AI DRAFT\n━━━━━━━━━━━━━━━━━━\n"
                "Describe the whole Item set naturally as your next message.\n\n"
                "You may mix unique Items, stacks and containers, and say when one Item should be stored inside another. "
                "The entire batch is previewed and validated before one atomic approval.\n\n"
                "Example: a gym rack, Olympic barbell, four 45 lb plates, and a storage bin containing six resistance bands.",
                [
                    [{"text": "← Change Method", "callback_data": "sw:cs:type:item"}],
                    [{"text": "✕ Cancel", "callback_data": "sw:cs:input:cancel"}],
                ],
            )
        if input_mode == "batch-manual":
            return (
                "🗂 ITEM BATCH · EXACT JSON\n━━━━━━━━━━━━━━━━━━\n"
                "Send one JSON object with exactly this shape:\n"
                "{\"items\":[{\"ref\":\"item_a\",\"payload\":{...exact item-v1...}}, ...]}\n\n"
                "Each ref must be unique. Batch-local storage may use stored_in: \"$container_ref\". "
                "Every payload is validated by item-v1 and the whole graph must pass before any write.",
                [
                    [{"text": "← Change Method", "callback_data": "sw:cs:type:item"}],
                    [{"text": "✕ Cancel", "callback_data": "sw:cs:input:cancel"}],
                ],
            )
        if input_mode == "manual":
            template = json.dumps(manual_item_template(), ensure_ascii=False, indent=2)
            return (
                "📦 ITEM · EXACT JSON\n━━━━━━━━━━━━━━━━━━\n"
                "Send one complete item-v1 JSON object as your next message.\n"
                "The exact Item validator runs before anything enters the draft.\n\n"
                "Example template:\n"
                f"{template}\n\n"
                "Edit the values/modules you need; do not add unknown fields.",
                [
                    [{"text": "← Change Method", "callback_data": "sw:cs:type:item"}],
                    [{"text": "✕ Cancel", "callback_data": "sw:cs:input:cancel"}],
                ],
            )
        return (
            "📦 ITEM · AI DRAFT\n━━━━━━━━━━━━━━━━━━\n"
            "Describe the Item naturally as your next message.\n\n"
            "Useful details include what it is, approximate size/weight, whether it stacks, capabilities, "
            "container capacity, nutrition or training resistance when relevant. Omit anything you do not know.\n\n"
            "Creation AI drafts the exact item-v1 contract; deterministic validation remains authoritative.",
            [
                [{"text": "← Change Method", "callback_data": "sw:cs:type:item"}],
                [{"text": "✕ Cancel", "callback_data": "sw:cs:input:cancel"}],
            ],
        )

    def batch_preview_view(conn: sqlite3.Connection, user_id: int, draft: dict[str, object], entries: list[dict[str, object]], *, notice: str | None = None):
        lines = [
            "📋 ITEM BATCH SANDBOX DRAFT",
            "━━━━━━━━━━━━━━━━━━",
            f"Items: {len(entries)}",
            f"Mode: {'AI Draft' if draft.get('draft_mode') == 'ai_generated' else 'Manual'}",
            f"Revision: {draft.get('revision')}",
            "",
        ]
        for index, entry in enumerate(entries, start=1):
            payload = entry.get("payload") if isinstance(entry.get("payload"), dict) else {}
            definition = payload.get("definition") if isinstance(payload.get("definition"), dict) else {}
            instance = payload.get("instance") if isinstance(payload.get("instance"), dict) else {}
            relationships = payload.get("relationships") if isinstance(payload.get("relationships"), dict) else {}
            mode = str(instance.get("mode") or "—")
            quantity = ""
            if mode == "stack" and isinstance(instance.get("quantity"), (int, float)):
                quantity = f" · {instance['quantity']:g} {instance.get('unit', '')}".rstrip()
            relation = next((f" · stored in {value}" for key, value in relationships.items() if key == "stored_in" and value), "")
            lines.append(
                f"{index}. {definition.get('name', 'Unnamed')} · {str(definition.get('kind', '—')).replace('_', ' ')} · {mode}{quantity}{relation}"
            )
        lines.extend([
            "",
            "Whole-batch I5.8 validation passed.",
            "Approval materializes every Item and batch-local relation atomically in Creation Sandbox only.",
            "If any member fails, zero batch Items are created.",
        ])
        if notice:
            lines.extend(["", notice])
        keyboard = []
        if draft.get("draft_mode") == "ai_generated":
            keyboard.append([{"text": "♻️ Reroll Batch", "callback_data": "sw:cs:reroll"}])
        keyboard.extend([
            [{"text": "✅ Approve Entire Batch", "callback_data": "sw:cs:approve"}],
            [{"text": "✕ Cancel Draft", "callback_data": "sw:cs:cancel"}],
            [{"text": "← Creator Studio", "callback_data": "sw:studio"}],
        ])
        return "\n".join(lines), keyboard

    def draft_preview_view(conn: sqlite3.Connection, user_id: int, *, notice: str | None = None):
        draft = active_draft(conn, user_id)
        entries = _batch_entries(draft)
        if draft is not None and entries is not None:
            return batch_preview_view(conn, user_id, draft, entries, notice=notice)
        payload = _item_payload(draft)
        if payload is None:
            return original_draft_preview(conn, user_id, notice=notice)
        definition = payload.get("definition") if isinstance(payload.get("definition"), dict) else {}
        instance = payload.get("instance") if isinstance(payload.get("instance"), dict) else {}
        economic = payload.get("economic_policy") if isinstance(payload.get("economic_policy"), dict) else {}
        relationships = payload.get("relationships") if isinstance(payload.get("relationships"), dict) else {}
        modules = definition.get("modules") if isinstance(definition.get("modules"), dict) else {}
        capabilities = definition.get("capabilities") if isinstance(definition.get("capabilities"), list) else []
        lines = [
            "📋 ITEM SANDBOX DRAFT",
            "━━━━━━━━━━━━━━━━━━",
            f"Name: {definition.get('name', 'Unnamed')}",
            f"Kind: {str(definition.get('kind', '—')).replace('_', ' ').title()}",
            f"Mobility: {str(definition.get('mobility', '—')).title()}",
            f"Mode: {'AI Draft' if draft and draft.get('draft_mode') == 'ai_generated' else 'Manual'}",
            f"Revision: {draft.get('revision') if draft else '—'}",
            "",
            str(definition.get("description") or "No description."),
            "",
            f"Instance: {instance.get('mode', '—')}" + (
                f" · {instance.get('quantity'):g} {instance.get('unit')}" if instance.get("mode") == "stack" and isinstance(instance.get("quantity"), (int, float)) else ""
            ),
            f"Capabilities: {', '.join(str(v) for v in capabilities) if capabilities else '—'}",
            f"Modules: {', '.join(sorted(str(v) for v in modules)) if modules else '—'}",
            f"Economics: {str(economic.get('classification', '—')).replace('_', ' ')} / {str(economic.get('net_worth_treatment', '—')).replace('_', ' ')}",
        ]
        relation_lines = [f"{key.replace('_', ' ')} → {value}" for key, value in relationships.items() if value]
        if relation_lines:
            lines.extend(["", "Relations"] + [f"• {value}" for value in relation_lines])
        lines.extend([
            "",
            "Exact item-v1 validation passed for this draft.",
            "Approval materializes Item definition/instance/economic/relation state in Creation Sandbox only.",
            "It does not transmigrate or start runtime behavior.",
        ])
        if notice:
            lines.extend(["", notice])
        keyboard = []
        if draft and draft.get("draft_mode") == "ai_generated":
            keyboard.append([{"text": "♻️ Reroll", "callback_data": "sw:cs:reroll"}])
        keyboard.extend([
            [{"text": "✅ Approve into Sandbox", "callback_data": "sw:cs:approve"}],
            [{"text": "✕ Cancel Draft", "callback_data": "sw:cs:cancel"}],
            [{"text": "← Creator Studio", "callback_data": "sw:studio"}],
        ])
        return "\n".join(lines), keyboard

    def begin_item_session(conn: sqlite3.Connection, user_id: int, input_mode: str) -> None:
        if input_mode == "batch-manual":
            expected = "item-batch-json"
            stored_mode = "manual"
        elif input_mode == "batch-ai":
            expected = "item-batch-description"
            stored_mode = "ai_generated"
        elif input_mode == "manual":
            expected = "item-json"
            stored_mode = "manual"
        else:
            expected = "description"
            stored_mode = "ai_generated"
        conn.execute(
            """
            INSERT INTO creation_sandbox_studio_sessions(
                sandbox_id,user_id,creation_type,input_mode,expected_input,prompt_chat_id,prompt_message_id
            ) VALUES('creator-default',?,'item',?,?,NULL,NULL)
            ON CONFLICT(sandbox_id,user_id) DO UPDATE SET
                creation_type='item',input_mode=excluded.input_mode,expected_input=excluded.expected_input,
                prompt_chat_id=NULL,prompt_message_id=NULL,updated_at=CURRENT_TIMESTAMP
            """,
            (int(user_id), stored_mode, expected),
        )
        conn.commit()

    def studio_callback_view(conn: sqlite3.Connection, user_id: int, callback_data: str):
        if callback_data == "sw:cs:create":
            base._clear_session(conn, user_id)
            base._restore_input_router()
            return create_type_view()
        if callback_data == "sw:cs:type:item":
            base._clear_session(conn, user_id)
            base._restore_input_router()
            return method_view("item")
        if callback_data in {
            "sw:cs:input:item:manual",
            "sw:cs:input:item:ai",
            "sw:cs:input:item:batch-manual",
            "sw:cs:input:item:batch-ai",
        }:
            token = callback_data.rsplit(":", 1)[-1]
            mode = token if token in {"batch-manual", "batch-ai"} else ("manual" if token == "manual" else "ai")
            begin_item_session(conn, user_id, mode)
            base._install_input_router()
            return prompt_view("item", mode)
        draft = active_draft(conn, user_id)
        if draft and draft.get("creation_type") == "item":
            batch_entries = _batch_entries(draft)
            if callback_data == "sw:cs:preview":
                return draft_preview_view(conn, user_id)
            if callback_data == "sw:cs:reroll":
                try:
                    if batch_entries is not None:
                        reroll_item_batch_draft(conn, user_id)
                        message = "♻️ AI Item batch rerolled. Review the whole batch before approval."
                    else:
                        reroll_item_draft(conn, user_id)
                        message = "♻️ AI Item draft rerolled. Review before approval."
                except CreatorStudioError as exc:
                    return draft_preview_view(conn, user_id, notice=f"Reroll rejected: {exc}")
                return draft_preview_view(conn, user_id, notice=message)
            if callback_data.startswith("sw:cs:approve:confirm:"):
                try:
                    expected_revision = int(callback_data.rsplit(":", 1)[-1])
                    if batch_entries is not None:
                        created = approve_item_batch_draft(conn, user_id, expected_revision)
                    else:
                        obj = approve_item_draft(conn, user_id, expected_revision)
                except (CreatorStudioError, ValueError, TypeError) as exc:
                    return draft_preview_view(conn, user_id, notice=f"Approval rejected: {exc}")
                if batch_entries is not None:
                    sample = []
                    for obj in created[:5]:
                        item = obj.get("item", {})
                        definition = item.get("definition", {}) if isinstance(item, dict) else {}
                        sample.append(f"• {definition.get('name', 'Item')} · {obj.get('object_id', '—')}")
                    more = f"\n• …and {len(created) - 5} more" if len(created) > 5 else ""
                    return (
                        "✅ SANDBOX ITEM BATCH APPROVED\n━━━━━━━━━━━━━━━━━━\n"
                        f"Created atomically: {len(created)} Items\n\n"
                        + "\n".join(sample)
                        + more
                        + "\n\nCreation Sandbox only. Canonical Real World remains unchanged.",
                        [
                            [{"text": "📦 View All Items", "callback_data": "sw:list:item"}],
                            [{"text": "🛠 Creator Studio", "callback_data": "sw:studio"}],
                        ],
                    )
                name = obj.get("identity", {}).get("name", obj.get("object_id", "Item"))
                return (
                    "✅ SANDBOX ITEM APPROVED\n━━━━━━━━━━━━━━━━━━\n"
                    f"Item: {name}\nID: {obj['object_id']}\n\n"
                    "Materialized in Creation Sandbox only. Canonical Real World remains unchanged.",
                    [
                        [{"text": "📦 View Item", "callback_data": f"sw:o:{obj['object_id']}"}],
                        [{"text": "📦 Items", "callback_data": "sw:list:item"}],
                        [{"text": "🛠 Creator Studio", "callback_data": "sw:studio"}],
                    ],
                )
        return original_callback(conn, user_id, callback_data)

    base._original_item_method_view = base._method_view
    base.manual_draft = manual_draft
    base.ai_draft = ai_draft
    base._create_type_view = create_type_view
    base._method_view = method_view
    base._prompt_view = prompt_view
    base.draft_preview_view = draft_preview_view
    base.studio_callback_view = studio_callback_view
