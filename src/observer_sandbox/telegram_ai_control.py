from __future__ import annotations

from typing import Any

from .ai_control import (
    activate_cognition_model,
    cognition_overview,
    models_for_provider,
    probe_model,
    refresh_provider_catalog,
)
from .simulation import runtime_value, set_runtime_value

AI_PAGE_SIZE = 8
AI_CANDIDATE_PREFIX = "telegram_ai_candidate:"


def _candidate_key(user_id: int) -> str:
    return f"{AI_CANDIDATE_PREFIX}{user_id}"


def _candidate(conn, user_id: int) -> dict[str, Any] | None:
    value = runtime_value(conn, _candidate_key(user_id), None)
    return dict(value) if isinstance(value, dict) else None


def _save_candidate(conn, user_id: int, value: dict[str, Any] | None) -> None:
    set_runtime_value(conn, _candidate_key(user_id), value)
    conn.commit()


def _provider_map(conn) -> dict[str, dict[str, Any]]:
    return {row["id"]: row for row in cognition_overview(conn)["providers"]}


def _home_keyboard() -> list[list[dict[str, str]]]:
    return [
        [{"text": "🧠 AI Cognition", "callback_data": "ai:providers"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ]


def home_view(conn) -> tuple[str, list[list[dict[str, str]]]]:
    overview = cognition_overview(conn)
    binding = overview.get("binding") or {}
    provider = binding.get("provider_id") or "Not configured"
    model = binding.get("model_id") or "Not configured"
    text = (
        "⚙️ CREATOR SETTINGS\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🧠 AI Cognition\n\n"
        f"Current provider: {provider}\n"
        f"Current model: {model}\n\n"
        "Choose AI Cognition to browse providers, fetch live model catalogs, test a candidate, and activate it explicitly."
    )
    return text, _home_keyboard()


def _providers_view(conn) -> tuple[str, list[list[dict[str, str]]]]:
    overview = cognition_overview(conn)
    current = overview.get("binding") or {}
    current_provider = current.get("provider_id")
    lines = [
        "🧠 AI COGNITION · PROVIDERS",
        "━━━━━━━━━━━━━━━━━━",
        f"Current: {current.get('provider_id', 'None')} / {current.get('model_id', 'None')}",
        "",
        "Select a provider:",
    ]
    keyboard: list[list[dict[str, str]]] = []
    for provider in overview["providers"]:
        provider_id = str(provider["id"])
        credential = "🔑" if provider.get("credential_present") else "⚪"
        current_icon = "✅" if provider_id == current_provider else ""
        lines.append(
            f"• {provider['display_name']} · {'credential ready' if provider.get('credential_present') else 'credential missing'}"
        )
        keyboard.append(
            [{"text": f"{current_icon}{credential} {provider['display_name']}", "callback_data": f"ai:p:{provider_id}"}]
        )
    keyboard.extend([
        [{"text": "← Creator Settings", "callback_data": "ai:home"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ])
    return "\n".join(lines), keyboard


def _provider_view(conn, provider_id: str, *, notice: str | None = None) -> tuple[str, list[list[dict[str, str]]]]:
    providers = _provider_map(conn)
    provider = providers.get(provider_id)
    if provider is None:
        return "Unknown AI provider.", [[{"text": "← Providers", "callback_data": "ai:providers"}]]
    models = models_for_provider(conn, provider_id)
    lines = [
        f"🧠 {provider['display_name']}",
        "━━━━━━━━━━━━━━━━━━",
        f"🔐 Credential: {'Available' if provider.get('credential_present') else 'Missing'}",
        f"📚 Cached models: {len(models)}",
        f"🔄 Catalog: {provider.get('catalog_status') or 'never refreshed'}",
    ]
    if provider.get("last_refresh_at"):
        lines.append(f"🕒 Last refresh: {provider['last_refresh_at']}")
    if notice:
        lines.extend(["", notice])
    lines.extend(["", "Fetching a catalog does not change the active cognition binding."])
    keyboard = [
        [{"text": "🔄 Fetch Models", "callback_data": f"ai:r:{provider_id}"}],
        [{"text": "📚 Browse Models", "callback_data": f"ai:page:{provider_id}:0"}],
        [{"text": "← Providers", "callback_data": "ai:providers"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ]
    return "\n".join(lines), keyboard


def _models_page(conn, provider_id: str, page: int) -> tuple[str, list[list[dict[str, str]]]]:
    providers = _provider_map(conn)
    provider = providers.get(provider_id)
    if provider is None:
        return "Unknown AI provider.", [[{"text": "← Providers", "callback_data": "ai:providers"}]]
    models = models_for_provider(conn, provider_id)
    if not models:
        return _provider_view(conn, provider_id, notice="No cached models yet. Tap Fetch Models first.")
    pages = max(1, (len(models) + AI_PAGE_SIZE - 1) // AI_PAGE_SIZE)
    page = max(0, min(int(page), pages - 1))
    start = page * AI_PAGE_SIZE
    visible = models[start : start + AI_PAGE_SIZE]
    lines = [
        f"📚 {provider['display_name']} MODELS",
        "━━━━━━━━━━━━━━━━━━",
        f"Page {page + 1}/{pages} · {len(models)} models",
        "",
        "Select a candidate model. Selection alone changes nothing.",
    ]
    keyboard: list[list[dict[str, str]]] = []
    for offset, model in enumerate(visible):
        index = start + offset
        label = str(model.get("display_name") or model["model_id"])
        if len(label) > 48:
            label = label[:45] + "…"
        keyboard.append([{"text": f"🧠 {label}", "callback_data": f"ai:m:{provider_id}:{index}"}])
    nav: list[dict[str, str]] = []
    if page > 0:
        nav.append({"text": "◀️", "callback_data": f"ai:page:{provider_id}:{page - 1}"})
    if page + 1 < pages:
        nav.append({"text": "▶️", "callback_data": f"ai:page:{provider_id}:{page + 1}"})
    if nav:
        keyboard.append(nav)
    keyboard.extend([
        [{"text": "🔄 Refresh Catalog", "callback_data": f"ai:r:{provider_id}"}],
        [{"text": f"← {provider['display_name']}", "callback_data": f"ai:p:{provider_id}"}],
    ])
    return "\n".join(lines), keyboard


def _candidate_view(conn, user_id: int, *, notice: str | None = None) -> tuple[str, list[list[dict[str, str]]]]:
    candidate = _candidate(conn, user_id)
    if not candidate:
        return "No AI model candidate is selected.", [[{"text": "← Providers", "callback_data": "ai:providers"}]]
    provider_id = str(candidate["provider_id"])
    model_id = str(candidate["model_id"])
    providers = _provider_map(conn)
    provider_name = providers.get(provider_id, {}).get("display_name", provider_id)
    tested = bool(candidate.get("probe_ok"))
    lines = [
        "🧪 AI MODEL CANDIDATE",
        "━━━━━━━━━━━━━━━━━━",
        f"Provider: {provider_name}",
        f"Model: {model_id}",
        f"Test: {'✅ Passed' if tested else '⚪ Not passed'}",
    ]
    if candidate.get("latency_ms") is not None:
        lines.append(f"Latency: {candidate['latency_ms']} ms")
    if notice:
        lines.extend(["", notice])
    lines.extend(["", "The current cognition binding is unchanged until Save & Activate."])
    keyboard: list[list[dict[str, str]]] = [
        [{"text": "🧪 Test Model", "callback_data": "ai:test"}],
    ]
    if tested:
        keyboard.append([{"text": "✅ Save & Activate", "callback_data": "ai:save"}])
    keyboard.extend([
        [{"text": "🗑 Cancel Candidate", "callback_data": "ai:cancel"}],
        [{"text": f"← {provider_name} Models", "callback_data": f"ai:page:{provider_id}:0"}],
    ])
    return "\n".join(lines), keyboard


def _friendly_probe_error(exc: Exception) -> str:
    detail = str(exc)
    lower = detail.lower()
    if "http 429" in lower or "rate" in lower or "quota" in lower:
        heading = "🚦 Rate / quota limit reached"
    elif "http 401" in lower or "http 403" in lower or "credential" in lower or "api key" in lower:
        heading = "🔐 Authentication / permission failed"
    elif "http 404" in lower:
        heading = "🔎 Model or endpoint unavailable"
    elif "http 413" in lower:
        heading = "📦 Provider request limit reached"
    elif "timed out" in lower or "timeout" in lower:
        heading = "⌛ Provider request timed out"
    else:
        heading = "❌ Inference test failed"
    return f"{heading}\n{detail[:900]}"


def callback_view(conn, user_id: int, callback_data: str) -> tuple[str, list[list[dict[str, str]]] | None]:
    if callback_data == "ai:home":
        return home_view(conn)
    if callback_data == "ai:providers":
        return _providers_view(conn)
    if callback_data.startswith("ai:p:"):
        return _provider_view(conn, callback_data.split(":", 2)[2])
    if callback_data.startswith("ai:r:"):
        provider_id = callback_data.split(":", 2)[2]
        try:
            count = refresh_provider_catalog(conn, provider_id)
            return _provider_view(conn, provider_id, notice=f"✅ Catalog refreshed: {count} models available.")
        except Exception as exc:
            return _provider_view(conn, provider_id, notice=f"❌ Catalog refresh failed safely.\n{str(exc)[:900]}")
    if callback_data.startswith("ai:page:"):
        _, _, provider_id, page = callback_data.split(":", 3)
        try:
            return _models_page(conn, provider_id, int(page))
        except ValueError:
            return "Invalid model page.", [[{"text": "← Providers", "callback_data": "ai:providers"}]]
    if callback_data.startswith("ai:m:"):
        _, _, provider_id, index_text = callback_data.split(":", 3)
        try:
            index = int(index_text)
        except ValueError:
            return "Invalid model selection.", [[{"text": "← Providers", "callback_data": "ai:providers"}]]
        models = models_for_provider(conn, provider_id)
        if index < 0 or index >= len(models):
            return "That model selection is stale. Refresh the model list.", [[{"text": "← Providers", "callback_data": "ai:providers"}]]
        selected = models[index]
        _save_candidate(
            conn,
            user_id,
            {
                "provider_id": provider_id,
                "model_id": selected["model_id"],
                "probe_ok": False,
            },
        )
        return _candidate_view(conn, user_id)
    if callback_data == "ai:test":
        candidate = _candidate(conn, user_id)
        if not candidate:
            return "No AI model candidate is selected.", [[{"text": "← Providers", "callback_data": "ai:providers"}]]
        try:
            result = probe_model(conn, str(candidate["provider_id"]), str(candidate["model_id"]))
            candidate.update(
                {
                    "probe_ok": True,
                    "latency_ms": result["latency_ms"],
                    "tested_at": result["tested_at"],
                }
            )
            _save_candidate(conn, user_id, candidate)
            return _candidate_view(conn, user_id, notice="✅ Real inference succeeded. This candidate may now be activated.")
        except Exception as exc:
            candidate.update({"probe_ok": False})
            candidate.pop("latency_ms", None)
            candidate.pop("tested_at", None)
            _save_candidate(conn, user_id, candidate)
            return _candidate_view(conn, user_id, notice=_friendly_probe_error(exc))
    if callback_data == "ai:save":
        candidate = _candidate(conn, user_id)
        if not candidate or not candidate.get("probe_ok"):
            return "🔒 Test the selected model successfully before activation.", [[{"text": "← AI Providers", "callback_data": "ai:providers"}]]
        try:
            binding = activate_cognition_model(conn, str(candidate["provider_id"]), str(candidate["model_id"]))
        except Exception as exc:
            return _candidate_view(conn, user_id, notice=f"❌ Activation failed safely.\n{str(exc)[:900]}")
        _save_candidate(conn, user_id, None)
        return (
            "✅ AI COGNITION ACTIVATED\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"Provider: {binding['provider_id']}\n"
            f"Model: {binding['model_id']}\n\n"
            "Future cognition wakes will use this binding. Existing world/profile state was not changed.",
            _home_keyboard(),
        )
    if callback_data == "ai:cancel":
        _save_candidate(conn, user_id, None)
        return _providers_view(conn)
    return "Unknown AI Creator setting.", _home_keyboard()
