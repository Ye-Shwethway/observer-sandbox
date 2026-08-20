from __future__ import annotations

import json
import os
import urllib.request
from typing import Any


def _fmt(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:g}"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, list):
        return ", ".join(_fmt(item) for item in value) if value else "—"
    if isinstance(value, dict):
        return ", ".join(f"{key}={_fmt(item)}" for key, item in value.items()) if value else "—"
    return str(value)


def _entries(draft: dict[str, Any]) -> list[dict[str, Any]]:
    properties = draft.get("proposal", {}).get("properties", {})
    batch = properties.get("item_batch")
    if isinstance(batch, dict) and isinstance(batch.get("items"), list):
        return [dict(entry) for entry in batch["items"] if isinstance(entry, dict)]
    payload = properties.get("item_payload")
    if isinstance(payload, dict):
        return [{"ref": str(payload.get("definition", {}).get("key") or "item"), "payload": payload}]
    return []


def _quantity(value: Any) -> str:
    if not isinstance(value, dict):
        return _fmt(value)
    if "value" in value and "unit" in value:
        return f"{_fmt(value.get('value'))} {value.get('unit')}"
    return _fmt(value)


def _module_lines(modules: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for module_name in sorted(modules):
        module = modules[module_name]
        lines.append(f"• {module_name.replace('_', ' ').title()}")
        if isinstance(module, dict):
            for key, value in module.items():
                if isinstance(value, dict) and "value" in value and "unit" in value:
                    rendered = _quantity(value)
                else:
                    rendered = _fmt(value)
                lines.append(f"  - {key.replace('_', ' ')}: {rendered}")
        else:
            lines.append(f"  - {_fmt(module)}")
    return lines or ["• None"]


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

    lines = [
        "📦 ITEM DRAFT PROFILE",
        "━━━━━━━━━━━━━━━━━━",
        f"Item {index + 1}/{len(entries)} · ref: {entry.get('ref', '—')}",
        "",
        "IDENTITY",
        f"• Name: {definition.get('name', 'Unnamed')}",
        f"• Definition key: {definition.get('key', '—')}",
        f"• Kind: {str(definition.get('kind', '—')).replace('_', ' ').title()}",
        f"• Mobility: {str(definition.get('mobility', '—')).title()}",
        f"• Stackable: {_fmt(definition.get('stackable'))}",
        f"• Description: {definition.get('description', '—')}",
        "",
        "INSTANCE",
        f"• Mode: {instance.get('mode', '—')}",
        f"• Quantity: {_fmt(instance.get('quantity'))}",
        f"• Unit: {_fmt(instance.get('unit'))}",
        "",
        "CAPABILITIES & TAGS",
        f"• Capabilities: {_fmt(capabilities)}",
        f"• Tags: {_fmt(tags)}",
        "",
        "MODULES",
        *_module_lines(modules),
        "",
        "ECONOMICS",
        f"• Classification: {_fmt(economic.get('classification'))}",
        f"• Net-worth treatment: {_fmt(economic.get('net_worth_treatment'))}",
        f"• Currency: {_fmt(economic.get('currency_code'))}",
        f"• Market value minor: {_fmt(economic.get('market_value_minor'))}",
        f"• Replacement value minor: {_fmt(economic.get('replacement_value_minor'))}",
        f"• Unit value minor: {_fmt(economic.get('unit_value_minor'))}",
        f"• Unit quantity: {_fmt(economic.get('unit_quantity'))}",
        f"• Unit label: {_fmt(economic.get('unit_label'))}",
        f"• Valuation method: {_fmt(economic.get('valuation_method'))}",
        "",
        "REQUIREMENTS",
        f"• Use: {_fmt(requirements.get('use'))}",
        "",
        "RELATIONSHIPS",
    ]
    active_relations = [(key, value) for key, value in relationships.items() if value is not None]
    if active_relations:
        lines.extend(f"• {key.replace('_', ' ')} → {_fmt(value)}" for key, value in active_relations)
    else:
        lines.append("• None")
    lines.extend([
        "",
        "✅ Exact item-v1 validation passed in the current draft.",
        "This is still Creation Sandbox draft state; approval has not occurred.",
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


def render_item_draft_text(draft: dict[str, Any]) -> tuple[str, str]:
    entries = _entries(draft)
    revision = draft.get("revision", "—")
    mode = "AI Draft" if draft.get("draft_mode") == "ai_generated" else "Manual"
    filename = f"creator-studio-item-draft-r{revision}.txt"
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
            f"Batch ref: {entry.get('ref', '—')}",
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
