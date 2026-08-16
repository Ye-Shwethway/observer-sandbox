from __future__ import annotations

from typing import Any

from .ai_control import (
    activate_cognition_fallback,
    activate_cognition_model,
    cognition_overview,
    models_for_provider,
    probe_model,
    refresh_provider_catalog,
    remove_cognition_fallback,
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


def _prefix(mode: str) -> str:
    return "af" if mode == "fallback" else "ai"


def _mode_title(mode: str) -> str:
    return "Fallback" if mode == "fallback" else "Primary"


def _home_keyboard() -> list[list[dict[str, str]]]:
    return [
        [{"text": "🧠 Primary Cognition", "callback_data": "ai:providers"}],
        [{"text": "🛟 Fallback Model", "callback_data": "af:providers"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ]


def home_view(conn) -> tuple[str, list[list[dict[str, str]]]]:
    overview = cognition_overview(conn)
    binding = overview.get("binding") or {}
    fallback = overview.get("fallback") or {}
    last = overview.get("last_fallback") or {}
    lines = [
        "⚙️ CREATOR SETTINGS",
        "━━━━━━━━━━━━━━━━━━",
        "🧠 AI Cognition",
        "",
        f"Primary: {binding.get('provider_id', 'Not configured')} / {binding.get('model_id', 'Not configured')}",
        f"Fallback: {fallback.get('provider_id', 'Not configured')} / {fallback.get('model_id', 'Not configured')}",
    ]
    if last:
        lines.extend([
            "",
            f"🛟 Last fallback: {last.get('fallback_provider_id')} / {last.get('fallback_model_id')}",
            f"🕒 {last.get('used_at', 'Unknown')}",
        ])
    lines.extend([
        "",
        "Primary is tried first. A configured fallback is used only when the provider/model call itself fails; deterministic action validation never triggers fallback.",
    ])
    return "\n".join(lines), _home_keyboard()


def _providers_view(conn, mode: str = "primary") -> tuple[str, list[list[dict[str, str]]]]:
    overview = cognition_overview(conn)
    selected_binding = (overview.get("fallback") if mode == "fallback" else overview.get("binding")) or {}
    selected_provider = selected_binding.get("provider_id")
    prefix = _prefix(mode)
    lines = [
        f"🧠 AI COGNITION · {_mode_title(mode).upper()} PROVIDERS",
        "━━━━━━━━━━━━━━━━━━",
        f"Current {_mode_title(mode).lower()}: {selected_binding.get('provider_id', 'None')} / {selected_binding.get('model_id', 'None')}",
        "",
        "Select a provider:",
    ]
    keyboard: list[list[dict[str, str]]] = []
    for provider in overview["providers"]:
        provider_id = str(provider["id"])
        credential = "🔑" if provider.get("credential_present") else "⚪"
        current_icon = "✅" if provider_id == selected_provider else ""
        lines.append(
            f"• {provider['display_name']} · {'credential ready' if provider.get('credential_present') else 'credential missing'}"
        )
        keyboard.append(
            [{"text": f"{current_icon}{credential} {provider['display_name']}", "callback_data": f"{prefix}:p:{provider_id}"}]
        )
    if mode == "fallback" and overview.get("fallback"):
        keyboard.append([{"text": "🗑 Remove Fallback", "callback_data": "af:clear"}])
    keyboard.extend([
        [{"text": "← Creator Settings", "callback_data": "ai:home"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ])
    return "\n".join(lines), keyboard


def _nanogpt_fetch_buttons(prefix: str) -> list[list[dict[str, str]]]:
    return [
        [{"text": "🟢 Fetch Subscription Only", "callback_data": f"{prefix}:r:nanogpt:subscription"}],
        [{"text": "💳 Fetch All · Subscription + Paid", "callback_data": f"{prefix}:r:nanogpt:all"}],
    ]


def _provider_view(
    conn,
    provider_id: str,
    *,
    mode: str = "primary",
    notice: str | None = None,
) -> tuple[str, list[list[dict[str, str]]]]:
    providers = _provider_map(conn)
    provider = providers.get(provider_id)
    prefix = _prefix(mode)
    if provider is None:
        return "Unknown AI provider.", [[{"text": "← Providers", "callback_data": f"{prefix}:providers"}]]
    models = models_for_provider(conn, provider_id)
    lines = [
        f"🧠 {_mode_title(mode)} · {provider['display_name']}",
        "━━━━━━━━━━━━━━━━━━",
        f"🔐 Credential: {'Available' if provider.get('credential_present') else 'Missing'}",
        f"📚 Cached models: {len(models)}",
        f"🔄 Catalog: {provider.get('catalog_status') or 'never refreshed'}",
    ]
    if provider.get("last_refresh_at"):
        lines.append(f"🕒 Last refresh: {provider['last_refresh_at']}")
    if provider_id == "nanogpt":
        lines.extend([
            "",
            "🟢 Subscription Only: models included in the NanoGPT subscription.",
            "💳 All: subscription models plus paid/premium models. Paid-model tests and runtime calls may use account balance.",
        ])
    if notice:
        lines.extend(["", notice])
    lines.extend(["", "Fetching a catalog does not change primary or fallback cognition settings."])
    keyboard: list[list[dict[str, str]]] = []
    if provider_id == "nanogpt":
        keyboard.extend(_nanogpt_fetch_buttons(prefix))
    else:
        keyboard.append([{"text": "🔄 Fetch Models", "callback_data": f"{prefix}:r:{provider_id}"}])
    keyboard.extend([
        [{"text": "📚 Browse Models", "callback_data": f"{prefix}:page:{provider_id}:0"}],
        [{"text": "← Providers", "callback_data": f"{prefix}:providers"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ])
    return "\n".join(lines), keyboard


def _models_page(conn, provider_id: str, page: int, *, mode: str = "primary") -> tuple[str, list[list[dict[str, str]]]]:
    providers = _provider_map(conn)
    provider = providers.get(provider_id)
    prefix = _prefix(mode)
    if provider is None:
        return "Unknown AI provider.", [[{"text": "← Providers", "callback_data": f"{prefix}:providers"}]]
    models = models_for_provider(conn, provider_id)
    if not models:
        return _provider_view(conn, provider_id, mode=mode, notice="No cached models yet. Fetch a model catalog first.")
    pages = max(1, (len(models) + AI_PAGE_SIZE - 1) // AI_PAGE_SIZE)
    page = max(0, min(int(page), pages - 1))
    start = page * AI_PAGE_SIZE
    visible = models[start : start + AI_PAGE_SIZE]
    lines = [
        f"📚 {_mode_title(mode).upper()} · {provider['display_name']} MODELS",
        "━━━━━━━━━━━━━━━━━━",
        f"Page {page + 1}/{pages} · {len(models)} models",
        "",
        "Select a candidate model. Selection alone changes nothing.",
    ]
    if provider_id == "nanogpt":
        lines.append("🟢 = subscription included · 💳 = paid/balance model")
    keyboard: list[list[dict[str, str]]] = []
    for offset, model in enumerate(visible):
        index = start + offset
        label = str(model.get("display_name") or model["model_id"])
        if len(label) > 48:
            label = label[:45] + "…"
        icon = "🧠"
        if provider_id == "nanogpt":
            scope = str((model.get("metadata") or {}).get("observer_nanogpt_billing_scope") or "subscription")
            icon = "💳" if scope == "paid" else "🟢"
        keyboard.append([{"text": f"{icon} {label}", "callback_data": f"{prefix}:m:{provider_id}:{index}"}])
    nav: list[dict[str, str]] = []
    if page > 0:
        nav.append({"text": "◀️", "callback_data": f"{prefix}:page:{provider_id}:{page - 1}"})
    if page + 1 < pages:
        nav.append({"text": "▶️", "callback_data": f"{prefix}:page:{provider_id}:{page + 1}"})
    if nav:
        keyboard.append(nav)
    if provider_id == "nanogpt":
        keyboard.extend(_nanogpt_fetch_buttons(prefix))
    else:
        keyboard.append([{"text": "🔄 Refresh Catalog", "callback_data": f"{prefix}:r:{provider_id}"}])
    keyboard.append([{"text": f"← {provider['display_name']}", "callback_data": f"{prefix}:p:{provider_id}"}])
    return "\n".join(lines), keyboard


def _candidate_view(conn, user_id: int, *, notice: str | None = None) -> tuple[str, list[list[dict[str, str]]]]:
    candidate = _candidate(conn, user_id)
    if not candidate:
        return "No AI model candidate is selected.", [[{"text": "← Creator Settings", "callback_data": "ai:home"}]]
    provider_id = str(candidate["provider_id"])
    model_id = str(candidate["model_id"])
    mode = str(candidate.get("mode") or "primary")
    prefix = _prefix(mode)
    providers = _provider_map(conn)
    provider_name = providers.get(provider_id, {}).get("display_name", provider_id)
    tested = bool(candidate.get("probe_ok"))
    lines = [
        f"🧪 {_mode_title(mode).upper()} MODEL CANDIDATE",
        "━━━━━━━━━━━━━━━━━━",
        f"Provider: {provider_name}",
        f"Model: {model_id}",
        f"Test: {'✅ Passed' if tested else '⚪ Not passed'}",
    ]
    if provider_id == "nanogpt":
        scope = str(candidate.get("billing_scope") or "subscription")
        lines.append(f"Billing: {'💳 Paid / balance' if scope == 'paid' else '🟢 Subscription included'}")
        if scope == "paid":
            lines.append("⚠️ Test Model and future runtime calls may consume NanoGPT balance.")
    if candidate.get("latency_ms") is not None:
        lines.append(f"Latency: {candidate['latency_ms']} ms")
    if notice:
        lines.extend(["", notice])
    if mode == "fallback":
        lines.extend(["", "The primary binding stays unchanged. Save will configure this tested model only as runtime fallback."])
    else:
        lines.extend(["", "The current primary binding is unchanged until Save & Activate."])
    keyboard: list[list[dict[str, str]]] = [
        [{"text": "🧪 Test Model", "callback_data": f"{prefix}:test"}],
    ]
    if tested:
        label = "✅ Save Fallback" if mode == "fallback" else "✅ Save & Activate"
        keyboard.append([{"text": label, "callback_data": f"{prefix}:save"}])
    keyboard.extend([
        [{"text": "🗑 Cancel Candidate", "callback_data": f"{prefix}:cancel"}],
        [{"text": f"← {provider_name} Models", "callback_data": f"{prefix}:page:{provider_id}:0"}],
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


def _select_model(conn, user_id: int, provider_id: str, index_text: str, *, mode: str):
    prefix = _prefix(mode)
    try:
        index = int(index_text)
    except ValueError:
        return "Invalid model selection.", [[{"text": "← Providers", "callback_data": f"{prefix}:providers"}]]
    models = models_for_provider(conn, provider_id)
    if index < 0 or index >= len(models):
        return "That model selection is stale. Refresh the model list.", [[{"text": "← Providers", "callback_data": f"{prefix}:providers"}]]
    selected = models[index]
    billing_scope = str((selected.get("metadata") or {}).get("observer_nanogpt_billing_scope") or "subscription")
    _save_candidate(
        conn,
        user_id,
        {
            "mode": mode,
            "provider_id": provider_id,
            "model_id": selected["model_id"],
            "billing_scope": billing_scope if provider_id == "nanogpt" else None,
            "probe_ok": False,
        },
    )
    return _candidate_view(conn, user_id)


def _test_candidate(conn, user_id: int, *, mode: str):
    candidate = _candidate(conn, user_id)
    if not candidate or str(candidate.get("mode") or "primary") != mode:
        return "No matching AI model candidate is selected.", [[{"text": "← Providers", "callback_data": f"{_prefix(mode)}:providers"}]]
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
        return _candidate_view(conn, user_id, notice="✅ Real inference succeeded. This candidate may now be saved.")
    except Exception as exc:
        candidate.update({"probe_ok": False})
        candidate.pop("latency_ms", None)
        candidate.pop("tested_at", None)
        _save_candidate(conn, user_id, candidate)
        return _candidate_view(conn, user_id, notice=_friendly_probe_error(exc))


def _save_selected_candidate(conn, user_id: int, *, mode: str):
    candidate = _candidate(conn, user_id)
    prefix = _prefix(mode)
    if not candidate or str(candidate.get("mode") or "primary") != mode or not candidate.get("probe_ok"):
        return "🔒 Test the selected model successfully before saving.", [[{"text": "← Providers", "callback_data": f"{prefix}:providers"}]]
    try:
        if mode == "fallback":
            binding = activate_cognition_fallback(
                conn,
                str(candidate["provider_id"]),
                str(candidate["model_id"]),
                tested_at=candidate.get("tested_at"),
            )
        else:
            binding = activate_cognition_model(conn, str(candidate["provider_id"]), str(candidate["model_id"]))
    except Exception as exc:
        return _candidate_view(conn, user_id, notice=f"❌ Save failed safely.\n{str(exc)[:900]}")
    _save_candidate(conn, user_id, None)
    if mode == "fallback":
        return (
            "✅ COGNITION FALLBACK SAVED\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"Provider: {binding['provider_id']}\n"
            f"Model: {binding['model_id']}\n\n"
            "Primary cognition is unchanged. This model is used only when the primary provider/model call fails.",
            _home_keyboard(),
        )
    return (
        "✅ AI COGNITION ACTIVATED\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"Provider: {binding['provider_id']}\n"
        f"Model: {binding['model_id']}\n\n"
        "Future cognition wakes will try this primary binding first. Existing world/profile state was not changed.",
        _home_keyboard(),
    )


def callback_view(conn, user_id: int, callback_data: str) -> tuple[str, list[list[dict[str, str]]] | None]:
    if callback_data == "ai:home":
        return home_view(conn)

    if callback_data in {"ai:providers", "af:providers"}:
        return _providers_view(conn, "fallback" if callback_data.startswith("af:") else "primary")

    mode = "fallback" if callback_data.startswith("af:") else "primary"
    prefix = _prefix(mode)
    if not callback_data.startswith(f"{prefix}:"):
        return "Unknown AI Creator setting.", _home_keyboard()

    if callback_data.startswith(f"{prefix}:p:"):
        return _provider_view(conn, callback_data.split(":", 2)[2], mode=mode)
    if callback_data.startswith(f"{prefix}:r:"):
        parts = callback_data.split(":")
        provider_id = parts[2] if len(parts) >= 3 else ""
        catalog_mode = parts[3] if len(parts) >= 4 else None
        try:
            count = refresh_provider_catalog(conn, provider_id, catalog_mode=catalog_mode)
            if provider_id == "nanogpt" and catalog_mode == "subscription":
                notice = f"✅ Subscription-only catalog refreshed: {count} included models available."
            elif provider_id == "nanogpt" and catalog_mode == "all":
                notice = f"✅ All-model catalog refreshed: {count} subscription + paid models available. 💳 Paid models may consume balance."
            else:
                notice = f"✅ Catalog refreshed: {count} models available."
            return _provider_view(conn, provider_id, mode=mode, notice=notice)
        except Exception as exc:
            return _provider_view(conn, provider_id, mode=mode, notice=f"❌ Catalog refresh failed safely.\n{str(exc)[:900]}")
    if callback_data.startswith(f"{prefix}:page:"):
        _, _, provider_id, page = callback_data.split(":", 3)
        try:
            return _models_page(conn, provider_id, int(page), mode=mode)
        except ValueError:
            return "Invalid model page.", [[{"text": "← Providers", "callback_data": f"{prefix}:providers"}]]
    if callback_data.startswith(f"{prefix}:m:"):
        _, _, provider_id, index_text = callback_data.split(":", 3)
        return _select_model(conn, user_id, provider_id, index_text, mode=mode)
    if callback_data == f"{prefix}:test":
        return _test_candidate(conn, user_id, mode=mode)
    if callback_data == f"{prefix}:save":
        return _save_selected_candidate(conn, user_id, mode=mode)
    if callback_data == f"{prefix}:cancel":
        _save_candidate(conn, user_id, None)
        return _providers_view(conn, mode)
    if callback_data == "af:clear":
        remove_cognition_fallback(conn)
        _save_candidate(conn, user_id, None)
        return _providers_view(conn, "fallback")
    return "Unknown AI Creator setting.", _home_keyboard()
