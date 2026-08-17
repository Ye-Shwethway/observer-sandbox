from __future__ import annotations

import sqlite3
import time
from datetime import datetime, timezone
from typing import Any

from .ai import AIConfigurationError, list_providers, resolve_binding, set_binding
from .structured_ai import generate_structured


NEWS_SCOPE_TYPE = "engine"
NEWS_SCOPE_ID = "information_media"
NEWS_ROLE = "news_generation"

NEWS_BULLETIN_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "stories": {
            "type": "array",
            "maxItems": 6,
            "items": {
                "type": "object",
                "properties": {
                    "source_item_id": {"type": "string"},
                    "headline": {"type": "string"},
                    "summary": {"type": "string"},
                },
                "required": ["source_item_id", "headline", "summary"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["title", "summary", "stories"],
    "additionalProperties": False,
}


def news_generation_binding(conn: sqlite3.Connection) -> dict[str, Any] | None:
    return resolve_binding(conn, role=NEWS_ROLE, engine_id=NEWS_SCOPE_ID)


def news_generation_overview(conn: sqlite3.Connection) -> dict[str, Any]:
    return {"binding": news_generation_binding(conn), "providers": list_providers(conn)}


def activate_news_generation_model(conn: sqlite3.Connection, provider_id: str, model_id: str) -> dict[str, Any]:
    conn.execute("UPDATE ai_providers SET enabled=1,updated_at=CURRENT_TIMESTAMP WHERE id=?", (provider_id,))
    set_binding(
        conn,
        scope_type=NEWS_SCOPE_TYPE,
        scope_id=NEWS_SCOPE_ID,
        role=NEWS_ROLE,
        provider_id=provider_id,
        model_id=model_id,
    )
    binding = news_generation_binding(conn)
    if binding is None:
        raise AIConfigurationError("News generation binding did not persist")
    return binding


def _validate_bulletin(value: dict[str, Any], allowed_source_ids: set[str]) -> dict[str, Any]:
    if set(value) != {"title", "summary", "stories"}:
        raise ValueError("news output keys do not match the required schema")
    if not isinstance(value["title"], str) or not isinstance(value["summary"], str):
        raise ValueError("news title/summary must be strings")
    stories = value["stories"]
    if not isinstance(stories, list) or len(stories) > 6:
        raise ValueError("news stories must be an array with at most six items")
    for story in stories:
        if not isinstance(story, dict) or set(story) != {"source_item_id", "headline", "summary"}:
            raise ValueError("news story keys do not match the required schema")
        if story["source_item_id"] not in allowed_source_ids:
            raise ValueError("news output referenced a source item that was not supplied")
        if not isinstance(story["headline"], str) or not isinstance(story["summary"], str):
            raise ValueError("news headline/summary must be strings")
    return value


def probe_news_generation_model(conn: sqlite3.Connection, provider_id: str, model_id: str) -> dict[str, Any]:
    source_id = "probe-source-1"
    prompt = (
        "News generation capability probe. You are an editor, not a source of world truth. "
        "Use only the supplied source record and preserve its source_item_id. Do not invent facts.\n\n"
        "Source record: {\"source_item_id\":\"probe-source-1\",\"title\":\"Test bulletin source\","
        "\"summary\":\"A bounded test record exists for schema validation.\"}\n\n"
        "Return one concise television bulletin using the required structured schema."
    )
    before = news_generation_binding(conn)
    started = time.perf_counter()
    value = generate_structured(
        conn,
        provider_id=provider_id,
        model_id=model_id,
        prompt=prompt,
        schema=NEWS_BULLETIN_SCHEMA,
        schema_name="observer_sandbox_news_bulletin",
    )
    _validate_bulletin(value, {source_id})
    after = news_generation_binding(conn)
    if before != after:
        raise RuntimeError("News model probe mutated the active binding")
    return {
        "ok": True,
        "provider_id": provider_id,
        "model_id": model_id,
        "latency_ms": int((time.perf_counter() - started) * 1000),
        "tested_at": datetime.now(timezone.utc).isoformat(),
    }


def generate_news_bulletin(
    conn: sqlite3.Connection,
    source_items: list[dict[str, Any]],
    *,
    bulletin_title: str,
) -> tuple[dict[str, Any], dict[str, str] | None]:
    bounded = source_items[:12]
    allowed_ids = {str(item["item_id"]) for item in bounded}
    if not bounded:
        return {"title": bulletin_title, "summary": "No eligible source reports.", "stories": []}, None

    binding = news_generation_binding(conn)
    if binding is not None:
        source_payload = [
            {
                "source_item_id": str(item["item_id"]),
                "title": str(item["title"]),
                "summary": str(item.get("summary") or ""),
                "source": str(item.get("source_name") or item.get("source_id") or "Unknown source"),
            }
            for item in bounded
        ]
        prompt = (
            "Create a concise television news bulletin from only the supplied authoritative publication evidence. "
            "You are an editor, not an authority for objective facts. Do not add claims that are unsupported by the supplied records. "
            "Every story must preserve one supplied source_item_id. Select at most six stories.\n\n"
            f"Bulletin title: {bulletin_title}\nSource records: {source_payload}"
        )
        try:
            value = generate_structured(
                conn,
                provider_id=str(binding["provider_id"]),
                model_id=str(binding["model_id"]),
                prompt=prompt,
                schema=NEWS_BULLETIN_SCHEMA,
                schema_name="observer_sandbox_news_bulletin",
                parameters=binding.get("parameters") or {},
            )
            return _validate_bulletin(value, allowed_ids), {
                "provider_id": str(binding["provider_id"]),
                "model_id": str(binding["model_id"]),
            }
        except Exception:
            pass

    stories = [
        {
            "source_item_id": str(item["item_id"]),
            "headline": str(item["title"]),
            "summary": str(item.get("summary") or ""),
        }
        for item in bounded[:6]
    ]
    return {
        "title": bulletin_title,
        "summary": "Deterministic bulletin compiled from represented source records.",
        "stories": stories,
    }, None
