from __future__ import annotations

from typing import Any, Callable

from .information_media import latest_media_publications, refresh_historical_tv_news
from .news_ai import news_generation_binding
from .simulation import runtime_value


def _short(value: Any, limit: int = 360) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: max(1, limit - 1)].rstrip() + "…"


def _news_keyboard() -> list[list[dict[str, str]]]:
    return [
        [{"text": "⚡ Generate News Now", "callback_data": "uni:news:generate"}],
        [{"text": "↻ Refresh View", "callback_data": "uni:news"}],
        [{"text": "← Universe", "callback_data": "nav:universe"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ]


def _binding_label(binding: dict[str, Any] | None) -> str:
    if binding is None:
        return "No AI binding · deterministic editorial fallback available"
    return f"{binding['provider_id']} · {binding['model_id']}"


def news_view(
    conn,
    *,
    notice: str | None = None,
) -> tuple[str, list[list[dict[str, str]]]]:
    """Render represented news state without fetching, generating, or creating exposure."""
    sim_time = runtime_value(conn, "sim_time", None)
    binding = news_generation_binding(conn)
    publications = latest_media_publications(conn, limit=3)
    lines = [
        "📰 UNIVERSE NEWS",
        "━━━━━━━━━━━━━━━━━━",
        f"🕒 Universe time · {sim_time or 'Unknown'}",
        f"🤖 News model · {_binding_label(binding)}",
    ]
    if notice:
        lines.extend(["", notice])

    if not publications:
        lines.extend([
            "",
            "⚪ No represented news bulletin has been generated yet.",
            "",
            "Use Generate News Now to run the historical news provider → configured editorial model → canonical media publication workflow for the current universe time.",
        ])
        return "\n".join(lines), _news_keyboard()

    latest = publications[0]
    editorial_provider = latest.get("editorial_provider_id")
    editorial_model = latest.get("editorial_model_id")
    if editorial_provider and editorial_model:
        editorial = f"AI · {editorial_provider} · {editorial_model}"
    else:
        editorial = "Deterministic fallback"

    lines.extend([
        "",
        f"📺 {_short(latest.get('title'), 180)}",
        f"📝 {_short(latest.get('summary'), 420) or 'No bulletin summary.'}",
        f"✍️ Editorial · {editorial}",
        f"⏱ Available · {latest.get('available_from') or 'Unknown'} → {latest.get('available_until') or 'Open-ended'}",
        "",
        "Stories",
    ])
    items = latest.get("items") or []
    if not items:
        lines.append("• No source stories are attached.")
    for index, item in enumerate(items[:6], start=1):
        source = item.get("source_name") or item.get("source_id") or "Unknown source"
        lines.extend([
            f"{index}. {_short(item.get('title'), 220)}",
            f"   🛰 {source} · {item.get('published_at') or 'Unknown publication time'}",
        ])
        summary = _short(item.get("summary"), 260)
        if summary:
            lines.append(f"   {_short(summary, 260)}")

    if len(publications) > 1:
        lines.extend(["", "Recent bulletins"])
        for previous in publications[1:3]:
            lines.append(f"• {_short(previous.get('title'), 180)} · {previous.get('available_from') or 'Unknown time'}")

    lines.extend([
        "",
        "ℹ️ This view is Creator observability only. Reading it does not expose any character to the bulletin and does not create belief, Memory, mind state, or action authority.",
    ])
    return "\n".join(lines), _news_keyboard()


def generate_news_view(
    conn,
    *,
    refresh_news: Callable[..., dict[str, Any] | None] = refresh_historical_tv_news,
) -> tuple[str, list[list[dict[str, str]]]]:
    """Run one explicit Creator-requested historical news refresh, then render its persisted result."""
    sim_time = runtime_value(conn, "sim_time", None)
    if not sim_time:
        return news_view(conn, notice="❌ News generation rejected: universe simulation time is unavailable.")

    binding = news_generation_binding(conn)
    try:
        publication = refresh_news(conn, str(sim_time))
    except Exception as exc:
        return news_view(conn, notice=f"❌ News generation failed: {_short(exc, 500)}")

    if publication is None:
        return news_view(
            conn,
            notice="⚪ News workflow completed, but the historical provider returned no eligible source reports for this universe-time window.",
        )

    editorial_provider = publication.get("editorial_provider_id")
    editorial_model = publication.get("editorial_model_id")
    if editorial_provider and editorial_model:
        notice = f"✅ News workflow completed with AI editorial: {editorial_provider} · {editorial_model}."
    elif binding is not None:
        notice = (
            "⚠️ News workflow completed, but the configured AI editorial was not used successfully; "
            "the canonical deterministic fallback compiled the bulletin instead."
        )
    else:
        notice = "✅ News workflow completed with the canonical deterministic editorial fallback."
    return news_view(conn, notice=notice)
