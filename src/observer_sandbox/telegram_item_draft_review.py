from __future__ import annotations

import json
import os
import re
import urllib.request
from typing import Any


def _fmt(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:g}"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, list):
        return ", ".join(_fmt(item) for item in value) if value else "—"
    if isinstance(value, dict):
        return ", ".join(f"{key}={_fmt(item)}" for key, item in value.items()) if value else "—"
    return str(value)


def _slug(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", str(value or "").lower()).strip("-")
    return text or "item"


def _entries(draft: dict[str, Any]) -> list[dict[str, Any]]:
    properties = draft.get("proposal", {}).get("properties", {})
    batch = properties.get("item_batch")
    if isinstance(batch, dict) and isinstance(batch.get("items"), list):
        return [dict(entry) for entry in batch["items"] if isinstance(entry, dict)]
    payload = properties.get("item_payload")
    if isinstance(payload, dict):
        return [{"ref": str(payload.get("definition", {}).get("key") or "item"), "payload": payload}]
    return []


def _ref_names(entries: list[dict[str, Any]]) -> dict[str, str]:
    names: dict[str, str] = {}
    for entry in entries:
        ref = str(entry.get("ref") or "").strip().lower()
        payload = entry.get("payload") if isinstance(entry.get("payload"), dict) else {}
        definition = payload.get("definition") if isinstance(payload.get("definition"), dict) else {}
        if ref:
            names[ref] = str(definition.get("name") or ref)
    return names


def _relation_display(value: Any, ref_names: dict[str, str]) -> str:
    if not isinstance(value, str):
        return _fmt(value)
    token = value.strip()
    if token.startswith("$"):
        return ref_names.get(token[1:].lower(), token[1:])
    return token


def _quantity(value: Any) -> str:
    if not isinstance(value, dict):
        return _fmt(value)
    if "value" in value and "unit" in value:
        return f"{_fmt(value.get('value'))} {value.get('unit')}"
    return _fmt(value)


def _module_lines(modules: dict[str, Any]) -> list[str]:
    labels = {
        "physical": "Physical details",
        "container": "Storage capacity",
        "nutrition": "Nutrition",
        "stack": "Quantity grouping",
        "resistance_training": "Training resistance",
    }
    field_labels = {
        "capacity_volume": "Capacity",
        "canonical_unit": "Unit",
        "initial_quantity": "Initial quantity",
        "resistance_load": "Resistance load",
        "basis_quantity": "Nutrition basis",
        "energy_kcal": "Energy",
        "protein_g": "Protein",
        "carbohydrate_g": "Carbohydrate",
        "fat_g": "Fat",
    }
    lines: list[str] = []
    for module_name in sorted(modules):
        module = modules[module_name]
        lines.append(f"• {labels.get(module_name, module_name.replace('_', ' ').title())}")
        if isinstance(module, dict):
            for key, value in module.items():
                if isinstance(value, dict) and "value" in value and "unit" in value:
                    rendered = _quantity(value)
                else:
                    rendered = _fmt(value)
                label = field_labels.get(key, key.replace("_", " ").title())
                if key.endswith("_g") and rendered != "—":
                    rendered = f"{rendered} g"
                elif key == "energy_kcal" and rendered != "—":
                    rendered = f"{rendered} kcal"
                lines.append(f"  - {label}: {rendered}")
        else:
            lines.append(f"  - {_fmt(module)}")
    return lines or ["• None represented"]


def _economics_lines(economic: dict[str, Any]) -> list[str]:
    classification = str(economic.get("classification") or "")
    treatment = str(economic.get("net_worth_treatment") or "")
    if classification == "economically_immaterial" and treatment == "excluded":
        return ["• Value tracking: Not included — no monetary value was supplied"]
    lines = [f"• Classification: {classification.replace('_', ' ').title() or '—'}"]
    if treatment:
        lines.append(f"• Net-worth treatment: {treatment.replace('_', ' ').title()}")
    currency = economic.get("currency_code")
    if currency:
        lines.append(f"• Currency: {currency}")
    for label, key in (("Market value", "market_value_minor"), ("Replacement value", "replacement_value_minor"), ("Unit value", "unit_value_minor")):
        if economic.get(key) is not None:
            lines.append(f"• {label} (minor units): {_fmt(economic.get(key))}")
    return lines


def item_detail_view(draft: dict[str, Any], index: int) -> tuple[str, list[list[dict[str, str]]]]:
    entries = _entries(draft)
    if not entries:
        return "📦 ITEM DRAFT DETAIL\n━━━━━━━━━━━━━━━━━━\nNo Item payload is available.", [[{"text": "← Draft Preview", "callback_data": "sw:cs:preview"}]]
    index = max(0, min(int(index), len(entries) - 1))
    entry = entries[index]
    payload = entry.get("payload") if isinstance(entry.get("payload"), dict) else {}
    definition = payload.get("definition") if isinstance(payload.get("definition"), dict) else {}
    instance = payload.get("instance") if isinstance(payload.get("instance"), dict) else {}
    economic = payload.get("economic_policy") if isinstance(payload.get("economic_policy"), dict) else {}
    requirements = payload.get("requirements") if isinstance(payload.get("requirements"), dict) else {}
    relationships = payload.get("relationships") if isinstance(payload.get("relationships"), dict) else {}
    modules = definition.get("modules") if isinstance(definition.get("modules"), dict) else {}
    capabilities = definition.get("capabilities") if isinstance(definition.get("capabilities"), list) else []
    tags = definition.get("tags") if isinstance(definition.get("tags"), list) else []
    ref_names = _ref_names(entries)

    mode = str(instance.get("mode") or "")
    instance_label = "Individual item" if mode == "unique" else "Grouped quantity" if mode == "stack" else mode.replace("_", " ").title() or "—"
    mobility = str(definition.get("mobility") or "").replace("_", " ").title() or "—"

    lines = [
        "📦 ITEM DRAFT PROFILE",
        "━━━━━━━━━━━━━━━━━━",
        f"Item {index + 1} of {len(entries)}",
        "",
        "IDENTITY",
        f"• Name: {definition.get('name', 'Unnamed')}",
        f"• Type: {str(definition.get('kind', '—')).replace('_', ' ').title()}",
        f"• Mobility: {mobility}",
        f"• Description: {definition.get('description', '—')}",
        "",
        "QUANTITY",
        f"• Form: {instance_label}",
    ]
    if mode == "stack":
        quantity = _fmt(instance.get("quantity"))
        unit = _fmt(instance.get("unit"))
        lines.append(f"• Quantity: {quantity} {unit}".rstrip())
    lines.extend([
        "",
        "CAPABILITIES & TAGS",
        f"• Capabilities: {_fmt([str(x).replace('_', ' ').title() for x in capabilities])}",
        f"• Tags: {_fmt(tags)}",
        "",
        "PHYSICAL & FUNCTIONAL DETAILS",
        *_module_lines(modules),
        "",
        "VALUE",
        *_economics_lines(economic),
    ])
    if requirements.get("use") is not None:
        lines.extend(["", "USE REQUIREMENTS", f"• {_fmt(requirements.get('use'))}"])

    active_relations = [(key, value) for key, value in relationships.items() if value is not None]
    if active_relations:
        relation_labels = {
            "stored_in": "Stored in",
            "located_at": "Located at",
            "owned_by": "Owned by",
            "carried_by": "Carried by",
            "equipped_by": "Equipped by",
        }
        lines.extend(["", "PLACEMENT & RELATIONSHIPS"])
        lines.extend(
            f"• {relation_labels.get(key, key.replace('_', ' ').title())}: {_relation_display(value, ref_names)}"
            for key, value in active_relations
        )

    lines.extend([
        "",
        "✅ Item contract and current realism checks passed.",
        "Review this draft before approving it into the Creation Sandbox.",
    ])

    keyboard: list[list[dict[str, str]]] = []
    nav: list[dict[str, str]] = []
    if index > 0:
        nav.append({"text": "← Previous Item", "callback_data": f"sw:cs:item-detail:{index - 1}"})
    if index + 1 < len(entries):
        nav.append({"text": "Next Item →", "callback_data": f"sw:cs:item-detail:{index + 1}"})
    if nav:
        keyboard.append(nav)
    keyboard.append([{"text": "← Batch Review", "callback_data": "sw:cs:preview"}])
    return "\n".join(lines), keyboard


def _export_filename(draft: dict[str, Any], entries: list[dict[str, Any]]) -> str:
    revision = draft.get("revision", "—")
    if not entries:
        return f"creator-studio-item-draft-r{revision}.txt"
    first_payload = entries[0].get("payload") if isinstance(entries[0].get("payload"), dict) else {}
    first_definition = first_payload.get("definition") if isinstance(first_payload.get("definition"), dict) else {}
    first_name = _slug(str(first_definition.get("name") or entries[0].get("ref") or "item"))
    if len(entries) == 1:
        return f"creator-studio-item-{first_name}-r{revision}.txt"
    return f"creator-studio-item-batch-{first_name}-plus-{len(entries) - 1}-r{revision}.txt"


def render_item_draft_text(draft: dict[str, Any]) -> tuple[str, str]:
    entries = _entries(draft)
    revision = draft.get("revision", "—")
    mode = "AI Draft" if draft.get("draft_mode") == "ai_generated" else "Manual"
    filename = _export_filename(draft, entries)
    lines = [
        "CREATION SANDBOX ITEM DRAFT",
        "=" * 72,
        f"Mode: {mode}",
        f"Revision: {revision}",
        f"Items: {len(entries)}",
        "Scope: Creation Sandbox only",
    ]
    for index, entry in enumerate(entries, start=1):
        payload = entry.get("payload") if isinstance(entry.get("payload"), dict) else {}
        definition = payload.get("definition") if isinstance(payload.get("definition"), dict) else {}
        lines.extend([
            "",
            f"ITEM {index}: {definition.get('name', 'Unnamed')}",
            "-" * 72,
            f"Internal batch ref: {entry.get('ref', '—')}",
            json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2),
        ])
    lines.extend([
        "",
        "BOUNDARY",
        "-" * 72,
        "This is a Creation Sandbox draft only.",
        "It is not canonical and has not been transmigrated or started.",
    ])
    return filename, "\n".join(lines) + "\n"


def send_item_draft_document(draft: dict[str, Any], user_id: int) -> str:
    token = os.environ.get("OBSERVER_TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Telegram bot token is not configured")
    filename, text = render_item_draft_text(draft)
    boundary = "----ObserverSandboxItemDraftBoundary"
    body = bytearray()

    def field(name: str, value: str) -> None:
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.extend(value.encode("utf-8"))
        body.extend(b"\r\n")

    field("chat_id", str(int(user_id)))
    field("caption", "📄 Full Item draft export")
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(f'Content-Disposition: form-data; name="document"; filename="{filename}"\r\n'.encode())
    body.extend(b"Content-Type: text/plain; charset=utf-8\r\n\r\n")
    body.extend(text.encode("utf-8"))
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode())
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendDocument",
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))
    if not result.get("ok"):
        raise RuntimeError(str(result.get("description") or "Telegram document upload failed"))
    return filename


__all__ = ["item_detail_view", "render_item_draft_text", "send_item_draft_document"]
