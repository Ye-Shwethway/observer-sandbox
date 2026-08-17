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
from .news_ai import activate_news_generation_model, news_generation_binding, probe_news_generation_model
from .simulation import runtime_value, set_runtime_value
from .telegram_creator_diagnostics import callback_view as diagnostic_callback_view

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
    if mode == "fallback":
        return "af"
    if mode == "news":
        return "ai:n"
    return "ai"


def _mode_title(mode: str) -> str:
    return {"primary": "Primary", "fallback": "Fallback", "news": "News Generation"}[mode]


def _home_keyboard() -> list[list[dict[str, str]]]:
    return [
        [{"text": "🧠 Character AI", "callback_data": "ai:character"}],
        [{"text": "📰 News Generation AI", "callback_data": "ai:n:home"}],
        [{"text": "🧪 Diagnostics", "callback_data": "ai:diag:home"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ]


def home_view(conn) -> tuple[str, list[list[dict[str, str]]]]:
    overview = cognition_overview(conn)
    primary = overview.get("binding") or {}
    fallback = overview.get("fallback") or {}
    news = news_generation_binding(conn) or {}
    return (
        "\n".join([
            "⚙️ CREATOR SETTINGS",
            "━━━━━━━━━━━━━━━━━━",
            "🤖 AI SETTINGS",
            "",
            "🧠 Character AI",
            f"Primary: {primary.get('provider_id', 'Not configured')} / {primary.get('model_id', 'Not configured')}",
            f"Fallback: {fallback.get('provider_id', 'Not configured')} / {fallback.get('model_id', 'Not configured')}",
            "",
            "📰 News Generation AI",
            f"Model: {news.get('provider_id', 'Not configured')} / {news.get('model_id', 'Not configured')}",
            "",
            "Character cognition and news editorial generation use independent role bindings.",
        ]),
        _home_keyboard(),
    )


def _character_home_view(conn):
    overview = cognition_overview(conn)
    primary = overview.get("binding") or {}
    fallback = overview.get("fallback") or {}
    return (
        "\n".join([
            "🧠 CHARACTER AI",
            "━━━━━━━━━━━━━━━━━━",
            f"Primary: {primary.get('provider_id', 'Not configured')} / {primary.get('model_id', 'Not configured')}",
            f"Fallback: {fallback.get('provider_id', 'Not configured')} / {fallback.get('model_id', 'Not configured')}",
            "",
            "These bindings affect autonomous character cognition only.",
        ]),
        [
            [{"text": "🧠 Primary Cognition", "callback_data": "ai:providers"}],
            [{"text": "🛟 Fallback Model", "callback_data": "af:providers"}],
            [{"text": "← AI Settings", "callback_data": "ai:home"}],
        ],
    )


def _news_home_view(conn):
    binding = news_generation_binding(conn) or {}
    return (
        "\n".join([
            "📰 NEWS GENERATION AI",
            "━━━━━━━━━━━━━━━━━━",
            f"Current: {binding.get('provider_id', 'Not configured')} / {binding.get('model_id', 'Not configured')}",
            "",
            "This role edits represented source evidence into bounded TV bulletins. It does not establish objective world truth.",
        ]),
        [
            [{"text": "📰 Select News Model", "callback_data": "ai:n:providers"}],
            [{"text": "← AI Settings", "callback_data": "ai:home"}],
        ],
    )


def _selected_binding(conn, mode: str) -> dict[str, Any]:
    if mode == "news":
        return news_generation_binding(conn) or {}
    overview = cognition_overview(conn)
    return (overview.get("fallback") if mode == "fallback" else overview.get("binding")) or {}


def _providers_view(conn, mode: str = "primary"):
    overview = cognition_overview(conn)
    selected = _selected_binding(conn, mode)
    prefix = _prefix(mode)
    lines = [
        f"{'📰' if mode == 'news' else '🧠'} {_mode_title(mode).upper()} PROVIDERS",
        "━━━━━━━━━━━━━━━━━━",
        f"Current {_mode_title(mode).lower()}: {selected.get('provider_id', 'None')} / {selected.get('model_id', 'None')}",
        "",
        "Select a provider:",
    ]
    keyboard: list[list[dict[str, str]]] = []
    for provider in overview["providers"]:
        provider_id = str(provider["id"])
        credential = "🔑" if provider.get("credential_present") else "⚪"
        current = "✅" if provider_id == selected.get("provider_id") else ""
        lines.append(f"• {provider['display_name']} · {'credential ready' if provider.get('credential_present') else 'credential missing'}")
        keyboard.append([{"text": f"{current}{credential} {provider['display_name']}", "callback_data": f"{prefix}:p:{provider_id}"}])
    if mode == "fallback" and overview.get("fallback"):
        keyboard.append([{"text": "🗑 Remove Fallback", "callback_data": "af:clear"}])
    keyboard.append([{"text": "← Back", "callback_data": "ai:n:home" if mode == "news" else "ai:character"}])
    keyboard.append([{"text": "⌂ Observer Home", "callback_data": "nav:home"}])
    return "\n".join(lines), keyboard


def _nanogpt_fetch_buttons(prefix: str):
    return [
        [{"text": "🟢 Fetch Subscription Only", "callback_data": f"{prefix}:r:nanogpt:subscription"}],
        [{"text": "💳 Fetch All · Subscription + Paid", "callback_data": f"{prefix}:r:nanogpt:all"}],
    ]


def _provider_view(conn, provider_id: str, *, mode: str = "primary", notice: str | None = None):
    provider = _provider_map(conn).get(provider_id)
    prefix = _prefix(mode)
    if provider is None:
        return "Unknown AI provider.", [[{"text": "← Providers", "callback_data": f"{prefix}:providers"}]]
    models = models_for_provider(conn, provider_id)
    lines = [
        f"{'📰' if mode == 'news' else '🧠'} {_mode_title(mode)} · {provider['display_name']}",
        "━━━━━━━━━━━━━━━━━━",
        f"🔐 Credential: {'Available' if provider.get('credential_present') else 'Missing'}",
        f"📚 Cached models: {len(models)}",
        f"🔄 Catalog: {provider.get('catalog_status') or 'never refreshed'}",
    ]
    if provider_id == "nanogpt":
        lines.extend(["", "🟢 Subscription Only: models included in the NanoGPT subscription.", "💳 Paid: all-model catalog may consume balance."])
    if notice:
        lines.extend(["", notice])
    lines.extend(["", "Fetching a catalog does not change any active binding."])
    keyboard: list[list[dict[str, str]]] = []
    if provider_id == "nanogpt":
        keyboard.extend(_nanogpt_fetch_buttons(prefix))
    else:
        keyboard.append([{"text": "🔄 Fetch Models", "callback_data": f"{prefix}:r:{provider_id}"}])
    keyboard.extend([
        [{"text": "📚 Browse Models", "callback_data": f"{prefix}:page:{provider_id}:0"}],
        [{"text": "← Providers", "callback_data": f"{prefix}:providers"}],
    ])
    return "\n".join(lines), keyboard


def _models_page(conn, provider_id: str, page: int, *, mode: str = "primary"):
    provider = _provider_map(conn).get(provider_id)
    prefix = _prefix(mode)
    if provider is None:
        return "Unknown AI provider.", [[{"text": "← Providers", "callback_data": f"{prefix}:providers"}]]
    models = models_for_provider(conn, provider_id)
    if not models:
        return _provider_view(conn, provider_id, mode=mode, notice="No cached models yet. Fetch a model catalog first.")
    pages = max(1, (len(models) + AI_PAGE_SIZE - 1) // AI_PAGE_SIZE)
    page = max(0, min(int(page), pages - 1))
    start = page * AI_PAGE_SIZE
    visible = models[start:start + AI_PAGE_SIZE]
    lines = [f"📚 {_mode_title(mode).upper()} · {provider['display_name']} MODELS", "━━━━━━━━━━━━━━━━━━", f"Page {page + 1}/{pages} · {len(models)} models", "", "Select a candidate model. Selection alone changes nothing."]
    if provider_id == "nanogpt":
        lines.append("🟢 = subscription included · 💳 = paid/balance model")
    keyboard: list[list[dict[str, str]]] = []
    for offset, model in enumerate(visible):
        index = start + offset
        label = str(model.get("display_name") or model["model_id"])
        if len(label) > 48:
            label = label[:45] + "…"
        icon = "📰" if mode == "news" else "🧠"
        if provider_id == "nanogpt":
            scope = str((model.get("metadata") or {}).get("observer_nanogpt_billing_scope") or "subscription")
            icon = "💳" if scope == "paid" else "🟢"
        keyboard.append([{"text": f"{icon} {label}", "callback_data": f"{prefix}:m:{provider_id}:{index}"}])
    nav = []
    if page > 0:
        nav.append({"text": "◀️", "callback_data": f"{prefix}:page:{provider_id}:{page - 1}"})
    if page + 1 < pages:
        nav.append({"text": "▶️", "callback_data": f"{prefix}:page:{provider_id}:{page + 1}"})
    if nav:
        keyboard.append(nav)
    keyboard.append([{"text": f"← {provider['display_name']}", "callback_data": f"{prefix}:p:{provider_id}"}])
    return "\n".join(lines), keyboard


def _candidate_view(conn, user_id: int, *, notice: str | None = None):
    candidate = _candidate(conn, user_id)
    if not candidate:
        return "No AI model candidate is selected.", [[{"text": "← AI Settings", "callback_data": "ai:home"}]]
    provider_id = str(candidate["provider_id"])
    model_id = str(candidate["model_id"])
    mode = str(candidate.get("mode") or "primary")
    prefix = _prefix(mode)
    provider_name = _provider_map(conn).get(provider_id, {}).get("display_name", provider_id)
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
    if candidate.get("latency_ms") is not None:
        lines.append(f"Latency: {candidate['latency_ms']} ms")
    if notice:
        lines.extend(["", notice])
    if mode == "fallback":
        lines.extend(["", "The primary binding stays unchanged. Save configures this model only as runtime fallback."])
    elif mode == "news":
        lines.extend(["", "The current news-generation binding is unchanged until Save & Activate."])
    else:
        lines.extend(["", "The current primary binding is unchanged until Save & Activate."])
    keyboard = [[{"text": "🧪 Test Model", "callback_data": f"{prefix}:test"}]]
    if tested:
        keyboard.append([{"text": "✅ Save Fallback" if mode == "fallback" else "✅ Save & Activate", "callback_data": f"{prefix}:save"}])
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
    _save_candidate(conn, user_id, {
        "mode": mode,
        "provider_id": provider_id,
        "model_id": selected["model_id"],
        "billing_scope": billing_scope if provider_id == "nanogpt" else None,
        "probe_ok": False,
    })
    return _candidate_view(conn, user_id)


def _test_candidate(conn, user_id: int, *, mode: str):
    candidate = _candidate(conn, user_id)
    if not candidate or str(candidate.get("mode") or "primary") != mode:
        return "No matching AI model candidate is selected.", [[{"text": "← Providers", "callback_data": f"{_prefix(mode)}:providers"}]]
    try:
        probe = probe_news_generation_model if mode == "news" else probe_model
        result = probe(conn, str(candidate["provider_id"]), str(candidate["model_id"]))
        candidate.update({"probe_ok": True, "latency_ms": result["latency_ms"], "tested_at": result["tested_at"]})
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
            binding = activate_cognition_fallback(conn, str(candidate["provider_id"]), str(candidate["model_id"]), tested_at=candidate.get("tested_at"))
        elif mode == "news":
            binding = activate_news_generation_model(conn, str(candidate["provider_id"]), str(candidate["model_id"]))
        else:
            binding = activate_cognition_model(conn, str(candidate["provider_id"]), str(candidate["model_id"]))
    except Exception as exc:
        return _candidate_view(conn, user_id, notice=f"❌ Save failed safely.\n{str(exc)[:900]}")
    _save_candidate(conn, user_id, None)
    if mode == "fallback":
        return ("✅ COGNITION FALLBACK SAVED\n━━━━━━━━━━━━━━━━━━\n" f"Provider: {binding['provider_id']}\nModel: {binding['model_id']}\n\nPrimary cognition is unchanged.", _home_keyboard())
    if mode == "news":
        return ("✅ NEWS GENERATION AI ACTIVATED\n━━━━━━━━━━━━━━━━━━\n" f"Provider: {binding['provider_id']}\nModel: {binding['model_id']}\n\nCharacter cognition bindings were not changed.", _home_keyboard())
    return ("✅ AI COGNITION ACTIVATED\n━━━━━━━━━━━━━━━━━━\n" f"Provider: {binding['provider_id']}\nModel: {binding['model_id']}\n\nFuture cognition wakes will try this primary binding first.", _home_keyboard())


def _mode_and_rest(callback_data: str) -> tuple[str, str]:
    if callback_data.startswith("ai:n:"):
        return "news", callback_data[len("ai:n:"):]
    if callback_data.startswith("af:"):
        return "fallback", callback_data[len("af:"):]
    if callback_data.startswith("ai:"):
        return "primary", callback_data[len("ai:"):]
    return "primary", ""


def callback_view(conn, user_id: int, callback_data: str) -> tuple[str, list[list[dict[str, str]]] | None]:
    if callback_data == "ai:home":
        return home_view(conn)
    if callback_data == "ai:character":
        return _character_home_view(conn)
    if callback_data == "ai:n:home":
        return _news_home_view(conn)
    if callback_data.startswith("ai:diag:"):
        return diagnostic_callback_view(conn, user_id, "diag:" + callback_data[len("ai:diag:"):], requested_by=f"telegram:{user_id}")

    mode, rest = _mode_and_rest(callback_data)
    prefix = _prefix(mode)
    if rest == "providers":
        return _providers_view(conn, mode)
    if rest.startswith("p:"):
        return _provider_view(conn, rest.split(":", 1)[1], mode=mode)
    if rest.startswith("r:"):
        parts = rest.split(":")
        provider_id = parts[1] if len(parts) >= 2 else ""
        catalog_mode = parts[2] if len(parts) >= 3 else None
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
    if rest.startswith("page:"):
        _, provider_id, page = rest.split(":", 2)
        try:
            return _models_page(conn, provider_id, int(page), mode=mode)
        except ValueError:
            return "Invalid model page.", [[{"text": "← Providers", "callback_data": f"{prefix}:providers"}]]
    if rest.startswith("m:"):
        _, provider_id, index_text = rest.split(":", 2)
        return _select_model(conn, user_id, provider_id, index_text, mode=mode)
    if rest == "test":
        return _test_candidate(conn, user_id, mode=mode)
    if rest == "save":
        return _save_selected_candidate(conn, user_id, mode=mode)
    if rest == "cancel":
        _save_candidate(conn, user_id, None)
        return _providers_view(conn, mode)
    if mode == "fallback" and rest == "clear":
        remove_cognition_fallback(conn)
        _save_candidate(conn, user_id, None)
        return _providers_view(conn, "fallback")
    return "Unknown AI Creator setting.", _home_keyboard()
