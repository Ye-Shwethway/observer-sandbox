from __future__ import annotations

import json
import sqlite3

from .creator_studio import CreatorStudioError, active_draft
from .creator_studio_location import (
    MANUAL_LOCATION_SECTIONS,
    ai_location_draft,
    approve_location_draft,
    manual_location_draft,
    manual_location_template,
    reroll_location_draft,
    start_manual_location_draft,
    update_manual_location_section,
)


_SECTION_META = {
    "identity": ("🪪", "Identity"),
    "structure": ("🏗", "Structure"),
    "geography": ("🗺", "Geography"),
    "spatial": ("📐", "Spatial"),
    "boundary": ("🧱", "Boundary"),
    "access": ("🚪", "Access"),
    "operations": ("⚙️", "Operations"),
    "topology": ("🔗", "Topology"),
    "facilities": ("🏢", "Facilities"),
    "environment": ("🌤", "Environment"),
    "control": ("🔐", "Control"),
    "economic_policy": ("💰", "Economics"),
    "provenance": ("🧾", "Provenance"),
}


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


def _section_summary(payload: dict[str, object], section_key: str) -> str:
    value = payload.get(section_key)
    if section_key == "identity" and isinstance(value, dict):
        return str(value.get("name") or "Unnamed")
    if section_key == "structure" and isinstance(value, dict):
        return f"{value.get('exposure', '—')} · parent={value.get('parent_ref') or 'none'}"
    if section_key == "geography" and isinstance(value, dict):
        represented = [value.get(key) for key in ("locality", "region", "country_code") if value.get(key)]
        return ", ".join(str(item) for item in represented) if represented else "not specified"
    if section_key == "spatial" and isinstance(value, dict):
        represented = [key for key in ("area", "length", "width", "height", "elevation") if value.get(key) is not None]
        return ", ".join(represented) if represented else "sparse"
    if section_key == "boundary" and isinstance(value, dict):
        return f"{value.get('type', '—')} · {value.get('enclosure', '—')}"
    if section_key == "access" and isinstance(value, dict):
        policy = value.get("policy") if isinstance(value.get("policy"), dict) else {}
        return str(policy.get("mode") or "—")
    if section_key == "operations" and isinstance(value, dict):
        return str(value.get("initial_state") or "—")
    if section_key == "topology" and isinstance(value, dict):
        interfaces = value.get("interfaces") if isinstance(value.get("interfaces"), list) else []
        return f"{len(interfaces)} interface(s)"
    if section_key == "facilities" and isinstance(value, dict):
        caps = value.get("capabilities") if isinstance(value.get("capabilities"), list) else []
        return f"{len(caps)} capability token(s)"
    if section_key == "environment" and isinstance(value, dict):
        return f"{value.get('lighting_profile', '—')} · {value.get('weather_exposure', '—')}"
    if section_key == "control" and isinstance(value, dict):
        return str(value.get("ownership_class") or "—")
    if section_key == "economic_policy":
        return "not specified" if value is None else "represented"
    if section_key == "provenance" and isinstance(value, dict):
        return str(value.get("source_status") or "—")
    return "represented"


def install_location_creator_studio_extension(base) -> None:
    original_manual_draft = base.manual_draft
    original_ai_draft = base.ai_draft
    original_create_type_view = base._create_type_view
    original_method_view = base._method_view
    original_prompt_view = base._prompt_view
    original_draft_preview = base.draft_preview_view
    original_callback = base.studio_callback_view

    def _session_expected(conn: sqlite3.Connection, user_id: int) -> str:
        session = base._session(conn, user_id)
        return str(session.get("expected_input") or "") if session else ""

    def manual_draft(conn, user_id, creation_type, raw, **kwargs):
        expected = _session_expected(conn, user_id)
        if creation_type == "location" and expected == "location-json":
            return manual_location_draft(conn, user_id, raw, **kwargs)
        if creation_type == "location" and expected.startswith("location-section:"):
            section_key = expected.split(":", 1)[1]
            return update_manual_location_section(conn, user_id, section_key, raw, **kwargs)
        return original_manual_draft(conn, user_id, creation_type, raw, **kwargs)

    def ai_draft(conn, user_id, creation_type, prompt_text, **kwargs):
        if creation_type == "location" and _session_expected(conn, user_id) == "description":
            return ai_location_draft(conn, user_id, prompt_text, **kwargs)
        return original_ai_draft(conn, user_id, creation_type, prompt_text, **kwargs)

    def create_type_view():
        return original_create_type_view()

    def method_view(creation_type: str):
        if creation_type != "location":
            return original_method_view(creation_type)
        return (
            "📍 CREATE LOCATION\n━━━━━━━━━━━━━━━━━━\n"
            "Choose guided Manual authoring, exact location-v2 JSON, or natural-language AI. All paths converge on the same validator and Sandbox materializer.",
            [
                [{"text": "✍️ Location · Guided Build", "callback_data": "sw:cs:location:guided"}],
                [{"text": "🧾 Location · Exact JSON", "callback_data": "sw:cs:input:location:manual"}],
                [{"text": "✨ Location · AI", "callback_data": "sw:cs:input:location:ai"}],
                [{"text": "← Creation Type", "callback_data": "sw:cs:create"}],
            ],
        )

    def prompt_view(creation_type: str, input_mode: str):
        if creation_type != "location":
            return original_prompt_view(creation_type, input_mode)
        if input_mode == "manual":
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
        return (
            "📍 LOCATION · AI DRAFT\n━━━━━━━━━━━━━━━━━━\n"
            "Describe the Location naturally as your next message. Include known scale, geography, boundaries, access, facilities, resources, utilities or topology when useful.\n\n"
            "Unknown facts remain unknown. AI cannot author grades or invent Sandbox object references. The exact location-v2 validator remains authoritative.",
            [
                [{"text": "← Change Method", "callback_data": "sw:cs:type:location"}],
                [{"text": "✕ Cancel", "callback_data": "sw:cs:input:cancel"}],
            ],
        )

    def manual_location_builder_view(conn: sqlite3.Connection, user_id: int, *, notice: str | None = None):
        draft = active_draft(conn, user_id)
        payload = _location_payload(draft)
        if payload is None or not draft or draft.get("draft_mode") != "manual":
            return draft_preview_view(conn, user_id, notice=notice or "No active guided Manual Location draft.")
        identity = payload.get("identity") if isinstance(payload.get("identity"), dict) else {}
        lines = [
            "✍️ LOCATION · GUIDED MANUAL BUILD",
            "━━━━━━━━━━━━━━━━━━",
            f"Name: {identity.get('name', 'Unnamed')}",
            f"Revision: {draft.get('revision', '—')}",
            "",
            "Choose a section. Send only that section's JSON when prompted; the complete location-v2 payload is revalidated before the draft revision is saved.",
            "",
        ]
        keyboard = []
        for section_key in MANUAL_LOCATION_SECTIONS:
            icon, label = _SECTION_META[section_key]
            lines.append(f"{icon} {label}: {_section_summary(payload, section_key)}")
            keyboard.append([{"text": f"{icon} Edit {label}", "callback_data": f"sw:cs:location:section:{section_key}"}])
        if notice:
            lines.extend(["", notice])
        keyboard.extend([
            [{"text": "📋 Review Full Draft", "callback_data": "sw:cs:preview"}],
            [{"text": "✕ Cancel Draft", "callback_data": "sw:cs:cancel"}],
            [{"text": "← Creator Studio", "callback_data": "sw:studio"}],
        ])
        return "\n".join(lines), keyboard

    def location_section_prompt_view(conn: sqlite3.Connection, user_id: int, section_key: str):
        draft = active_draft(conn, user_id)
        payload = _location_payload(draft)
        if payload is None or section_key not in MANUAL_LOCATION_SECTIONS:
            return manual_location_builder_view(conn, user_id, notice="Section unavailable.")
        icon, label = _SECTION_META[section_key]
        current = json.dumps(payload.get(section_key), ensure_ascii=False, indent=2)
        return (
            f"{icon} LOCATION · {label.upper()}\n━━━━━━━━━━━━━━━━━━\n"
            "Send the replacement JSON for this section as your next message.\n"
            "Only this section changes; the entire Location is then validated and saved as a new draft revision.\n"
            "Use null/empty values for unknown facts. Do not author grade or derived fields.\n\n"
            f"Current {label}:\n{current}",
            [
                [{"text": "← Guided Builder", "callback_data": "sw:cs:location:sections"}],
                [{"text": "✕ Cancel Input", "callback_data": "sw:cs:input:cancel"}],
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

        represented_geo = [value for value in (
            geography.get("address_text"), geography.get("locality"), geography.get("region"), geography.get("country_code")
        ) if value]
        dimensions = [key for key in ("area", "length", "width", "height", "elevation") if spatial.get(key) is not None]
        interfaces = topology.get("interfaces") if isinstance(topology.get("interfaces"), list) else []
        capabilities = facilities.get("capabilities") if isinstance(facilities.get("capabilities"), list) else []

        lines = [
            "📋 LOCATION SANDBOX DRAFT",
            "━━━━━━━━━━━━━━━━━━",
            f"Name: {identity.get('name', 'Unnamed')}",
            f"Kind: {str(identity.get('kind', '—')).replace('_', ' ').title()}",
            f"Exposure: {str(structure.get('exposure', '—')).replace('_', ' ').title()}",
            f"Mode: {'AI Draft' if draft and draft.get('draft_mode') == 'ai_generated' else 'Manual'}",
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
        keyboard = []
        if draft and draft.get("draft_mode") == "manual":
            keyboard.append([{"text": "✍️ Edit Sections", "callback_data": "sw:cs:location:sections"}])
        if draft and draft.get("draft_mode") == "ai_generated":
            keyboard.append([{"text": "♻️ Reroll", "callback_data": "sw:cs:reroll"}])
        keyboard.extend([
            [{"text": "📄 Export Full Draft (.txt)", "callback_data": "sw:cs:export"}],
            [{"text": "✅ Approve into Sandbox", "callback_data": "sw:cs:approve"}],
            [{"text": "✕ Cancel Draft", "callback_data": "sw:cs:cancel"}],
            [{"text": "← Creator Studio", "callback_data": "sw:studio"}],
        ])
        return "\n".join(lines), keyboard

    def begin_location_session(conn: sqlite3.Connection, user_id: int, input_mode: str, *, expected: str | None = None) -> None:
        stored_mode = "manual" if input_mode == "manual" else "ai_generated"
        expected_input = expected or ("location-json" if input_mode == "manual" else "description")
        conn.execute(
            """
            INSERT INTO creation_sandbox_studio_sessions(
                sandbox_id,user_id,creation_type,input_mode,expected_input,prompt_chat_id,prompt_message_id
            ) VALUES('creator-default',?,'location',?,?,NULL,NULL)
            ON CONFLICT(sandbox_id,user_id) DO UPDATE SET
                creation_type='location',input_mode=excluded.input_mode,expected_input=excluded.expected_input,
                prompt_chat_id=NULL,prompt_message_id=NULL,updated_at=CURRENT_TIMESTAMP
            """,
            (int(user_id), stored_mode, expected_input),
        )
        conn.commit()

    def studio_callback_view(conn: sqlite3.Connection, user_id: int, callback_data: str):
        if callback_data == "sw:cs:type:location":
            base._clear_session(conn, user_id)
            base._restore_input_router()
            return method_view("location")
        if callback_data == "sw:cs:location:guided":
            base._clear_session(conn, user_id)
            base._restore_input_router()
            try:
                start_manual_location_draft(conn, user_id)
            except CreatorStudioError as exc:
                return method_view("location")[0] + f"\n\nGuided draft could not start: {exc}", method_view("location")[1]
            return manual_location_builder_view(conn, user_id, notice="✅ Sparse valid location-v2 draft started. Fill only what you know.")
        if callback_data == "sw:cs:location:sections":
            base._clear_session(conn, user_id)
            base._restore_input_router()
            return manual_location_builder_view(conn, user_id)
        if callback_data.startswith("sw:cs:location:section:"):
            section_key = callback_data.rsplit(":", 1)[-1]
            if section_key not in MANUAL_LOCATION_SECTIONS:
                return manual_location_builder_view(conn, user_id, notice="Unknown Location section.")
            begin_location_session(conn, user_id, "manual", expected=f"location-section:{section_key}")
            base._install_input_router()
            return location_section_prompt_view(conn, user_id, section_key)
        if callback_data in {"sw:cs:input:location:manual", "sw:cs:input:location:ai"}:
            mode = "manual" if callback_data.endswith(":manual") else "ai"
            begin_location_session(conn, user_id, mode)
            base._install_input_router()
            return prompt_view("location", mode)

        draft = active_draft(conn, user_id)
        if draft and draft.get("creation_type") == "location" and _location_payload(draft) is not None:
            if callback_data == "sw:cs:preview":
                return draft_preview_view(conn, user_id)
            if callback_data == "sw:cs:reroll":
                try:
                    reroll_location_draft(conn, user_id)
                except CreatorStudioError as exc:
                    return draft_preview_view(conn, user_id, notice=f"Reroll rejected: {exc}")
                return draft_preview_view(conn, user_id, notice="♻️ AI Location draft rerolled. Review before approval.")
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
    base.ai_draft = ai_draft
    base._create_type_view = create_type_view
    base._method_view = method_view
    base._prompt_view = prompt_view
    base.draft_preview_view = draft_preview_view
    base.studio_callback_view = studio_callback_view
