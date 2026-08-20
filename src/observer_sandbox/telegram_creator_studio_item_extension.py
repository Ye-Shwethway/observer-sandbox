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


def install_item_creator_studio_extension(base) -> None:
    original_manual_draft = base.manual_draft
    original_ai_draft = base.ai_draft
    original_prompt_view = base._prompt_view
    original_draft_preview = base.draft_preview_view
    original_callback = base.studio_callback_view

    def manual_draft(conn, user_id, creation_type, raw, **kwargs):
        if creation_type == "item":
            return manual_item_draft(conn, user_id, raw, **kwargs)
        return original_manual_draft(conn, user_id, creation_type, raw, **kwargs)

    def ai_draft(conn, user_id, creation_type, prompt_text, **kwargs):
        if creation_type == "item":
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
            "📦 CREATE ITEM\n━━━━━━━━━━━━━━━━━━\nChoose a creation method.\n\n"
            "AI is the easiest path. Manual uses the exact item-v1 JSON contract for precise control.",
            [
                [{"text": "✨ Generate with AI", "callback_data": "sw:cs:input:item:ai"}],
                [{"text": "🧾 Exact Item JSON", "callback_data": "sw:cs:input:item:manual"}],
                [{"text": "← Creation Type", "callback_data": "sw:cs:create"}],
            ],
        )

    def prompt_view(creation_type: str, input_mode: str):
        if creation_type != "item":
            return original_prompt_view(creation_type, input_mode)
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

    def draft_preview_view(conn: sqlite3.Connection, user_id: int, *, notice: str | None = None):
        draft = active_draft(conn, user_id)
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
        expected = "item-json" if input_mode == "manual" else "description"
        conn.execute(
            """
            INSERT INTO creation_sandbox_studio_sessions(
                sandbox_id,user_id,creation_type,input_mode,expected_input,prompt_chat_id,prompt_message_id
            ) VALUES('creator-default',?,'item',?,?,NULL,NULL)
            ON CONFLICT(sandbox_id,user_id) DO UPDATE SET
                creation_type='item',input_mode=excluded.input_mode,expected_input=excluded.expected_input,
                prompt_chat_id=NULL,prompt_message_id=NULL,updated_at=CURRENT_TIMESTAMP
            """,
            (int(user_id), input_mode, expected),
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
        if callback_data in {"sw:cs:input:item:manual", "sw:cs:input:item:ai"}:
            mode = "manual" if callback_data.endswith(":manual") else "ai_generated"
            begin_item_session(conn, user_id, mode)
            base._install_input_router()
            return prompt_view("item", mode)
        draft = active_draft(conn, user_id)
        if draft and draft.get("creation_type") == "item":
            if callback_data == "sw:cs:preview":
                return draft_preview_view(conn, user_id)
            if callback_data == "sw:cs:reroll":
                try:
                    reroll_item_draft(conn, user_id)
                except CreatorStudioError as exc:
                    return draft_preview_view(conn, user_id, notice=f"Reroll rejected: {exc}")
                return draft_preview_view(conn, user_id, notice="♻️ AI Item draft rerolled. Review before approval.")
            if callback_data.startswith("sw:cs:approve:confirm:"):
                try:
                    expected_revision = int(callback_data.rsplit(":", 1)[-1])
                    obj = approve_item_draft(conn, user_id, expected_revision)
                except (CreatorStudioError, ValueError, TypeError) as exc:
                    return draft_preview_view(conn, user_id, notice=f"Approval rejected: {exc}")
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
