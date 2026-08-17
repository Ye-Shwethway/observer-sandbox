from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Any

from .historical_news_provider import gdelt_historical_articles
from .news_ai import generate_news_bulletin
from .world import get_field
from .world_stimulus import add_stimulus_scope, create_world_stimulus, record_character_exposure


TV_DEVICE_ID = "obj_thorne_estate_living_media_console"
TV_DEVICE_TYPE = "television"


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _stable_id(prefix: str, value: str) -> str:
    return f"{prefix}_{hashlib.sha256(value.encode('utf-8')).hexdigest()[:20]}"


def ensure_information_media_seed(conn: sqlite3.Connection) -> None:
    if conn.execute("SELECT 1 FROM entities WHERE id=?", (TV_DEVICE_ID,)).fetchone() is not None:
        conn.execute(
            """
            INSERT INTO media_devices(entity_id,device_type,channels_json,status,metadata_json)
            VALUES(?, ?, ?, 'active', ?)
            ON CONFLICT(entity_id) DO UPDATE SET
                device_type=excluded.device_type,
                channels_json=excluded.channels_json,
                status='active',
                metadata_json=excluded.metadata_json,
                updated_at=CURRENT_TIMESTAMP
            """,
            (TV_DEVICE_ID, TV_DEVICE_TYPE, _json(["media", "visual", "auditory"]), _json({"role": "W4 TV exemplar"})),
        )
    conn.commit()


def upsert_information_source(
    conn: sqlite3.Connection,
    *,
    source_id: str,
    name: str,
    source_type: str = "publisher",
    credibility: str = "unknown",
    provenance: dict[str, Any] | None = None,
) -> None:
    conn.execute(
        """
        INSERT INTO information_sources(source_id,name,source_type,credibility,provenance_json)
        VALUES(?,?,?,?,?)
        ON CONFLICT(source_id) DO UPDATE SET
            name=excluded.name,
            source_type=excluded.source_type,
            credibility=excluded.credibility,
            provenance_json=excluded.provenance_json,
            updated_at=CURRENT_TIMESTAMP
        """,
        (source_id, name, source_type, credibility, _json(provenance or {})),
    )


def import_external_articles(conn: sqlite3.Connection, records: list[dict[str, Any]]) -> list[str]:
    """Persist reported publication evidence without declaring its claims objectively true."""
    item_ids: list[str] = []
    for record in records:
        provider_id = str(record.get("provider_id") or "external")
        provider_ref = str(record.get("provider_ref") or record.get("source_url") or record.get("title"))
        source_name = str(record.get("source_name") or record.get("source_domain") or "Unknown source")
        source_id = _stable_id("source", source_name.lower())
        upsert_information_source(
            conn,
            source_id=source_id,
            name=source_name,
            source_type="publisher",
            credibility="unknown",
            provenance={"provider_id": provider_id, "domain": record.get("source_domain")},
        )
        item_id = _stable_id("info", f"{provider_id}:{provider_ref}")
        conn.execute(
            """
            INSERT INTO information_items(
                item_id,item_type,title,summary,source_id,published_at,provider_id,provider_ref,
                source_url,language,verification_status,metadata_json
            ) VALUES(?,?,?,?,?,?,?,?,?,?, 'reported', ?)
            ON CONFLICT(item_id) DO UPDATE SET
                title=excluded.title,
                summary=excluded.summary,
                source_id=excluded.source_id,
                published_at=excluded.published_at,
                source_url=excluded.source_url,
                language=excluded.language,
                metadata_json=excluded.metadata_json,
                updated_at=CURRENT_TIMESTAMP
            """,
            (
                item_id,
                "news_report",
                str(record.get("title") or "Untitled report"),
                str(record.get("summary") or ""),
                source_id,
                record.get("published_at"),
                provider_id,
                provider_ref,
                record.get("source_url"),
                record.get("language"),
                _json({"provenance": record.get("provenance") or {}}),
            ),
        )
        item_ids.append(item_id)
    conn.commit()
    return item_ids


def information_item(conn: sqlite3.Connection, item_id: str) -> dict[str, Any]:
    row = conn.execute(
        """
        SELECT i.*,s.name AS source_name,s.credibility AS source_credibility
        FROM information_items i LEFT JOIN information_sources s ON s.source_id=i.source_id
        WHERE i.item_id=?
        """,
        (item_id,),
    ).fetchone()
    if row is None:
        raise ValueError(f"unknown information item: {item_id}")
    value = dict(row)
    value["metadata"] = json.loads(value.pop("metadata_json"))
    return value


def latest_information_items(conn: sqlite3.Connection, *, limit: int = 20) -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT item_id FROM information_items ORDER BY COALESCE(published_at,created_at) DESC,item_id LIMIT ?",
        (max(1, min(int(limit), 100)),),
    ).fetchall()
    return [information_item(conn, str(row["item_id"])) for row in rows]


def _device_location(conn: sqlite3.Connection, entity_id: str) -> str | None:
    row = conn.execute(
        "SELECT source_id FROM relations WHERE relation_type='contains' AND target_id=? ORDER BY id LIMIT 1",
        (entity_id,),
    ).fetchone()
    return None if row is None else str(row["source_id"])


def create_tv_publication(
    conn: sqlite3.Connection,
    *,
    publication_id: str,
    title: str,
    summary: str,
    item_ids: list[str],
    available_from: str,
    available_until: str | None = None,
    editorial_provider_id: str | None = None,
    editorial_model_id: str | None = None,
    device_entity_id: str = TV_DEVICE_ID,
) -> dict[str, Any]:
    device = conn.execute("SELECT * FROM media_devices WHERE entity_id=? AND status='active'", (device_entity_id,)).fetchone()
    if device is None:
        raise ValueError(f"unknown active media device: {device_entity_id}")
    if not item_ids:
        raise ValueError("a media publication requires at least one source information item")
    conn.execute(
        """
        INSERT INTO media_publications(
            publication_id,medium,title,summary,available_from,available_until,status,
            editorial_provider_id,editorial_model_id,metadata_json
        ) VALUES(?, 'television', ?, ?, ?, ?, 'active', ?, ?, ?)
        ON CONFLICT(publication_id) DO UPDATE SET
            title=excluded.title,summary=excluded.summary,available_from=excluded.available_from,
            available_until=excluded.available_until,status='active',
            editorial_provider_id=excluded.editorial_provider_id,
            editorial_model_id=excluded.editorial_model_id,
            metadata_json=excluded.metadata_json,updated_at=CURRENT_TIMESTAMP
        """,
        (
            publication_id,
            title,
            summary,
            available_from,
            available_until,
            editorial_provider_id,
            editorial_model_id,
            _json({"claim_authority": "publication_only"}),
        ),
    )
    conn.execute("DELETE FROM media_publication_items WHERE publication_id=?", (publication_id,))
    for ordinal, item_id in enumerate(item_ids):
        if conn.execute("SELECT 1 FROM information_items WHERE item_id=?", (item_id,)).fetchone() is None:
            raise ValueError(f"unknown information item: {item_id}")
        conn.execute(
            "INSERT INTO media_publication_items(publication_id,item_id,ordinal) VALUES(?,?,?)",
            (publication_id, item_id, ordinal),
        )
    conn.commit()

    stimulus_id = f"stimulus_media_{publication_id}"
    if conn.execute("SELECT 1 FROM world_stimuli WHERE stimulus_id=?", (stimulus_id,)).fetchone() is None:
        create_world_stimulus(
            conn,
            stimulus_id=stimulus_id,
            stimulus_type="information",
            channel="media",
            subject=title,
            start_sim_time=available_from,
            end_sim_time=available_until,
            source_type="media_publication",
            source_id=publication_id,
            source_entity_id=device_entity_id,
            payload={"publication_id": publication_id, "medium": "television", "summary": summary},
            salience=0.5,
            metadata={"device_entity_id": device_entity_id},
        )
        add_stimulus_scope(conn, stimulus_id=stimulus_id, scope_type="entity", scope_id=device_entity_id, relation_role="displayed_by")
    return media_publication(conn, publication_id)


def media_publication(conn: sqlite3.Connection, publication_id: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM media_publications WHERE publication_id=?", (publication_id,)).fetchone()
    if row is None:
        raise ValueError(f"unknown media publication: {publication_id}")
    value = dict(row)
    value["metadata"] = json.loads(value.pop("metadata_json"))
    items = conn.execute(
        "SELECT item_id FROM media_publication_items WHERE publication_id=? ORDER BY ordinal",
        (publication_id,),
    ).fetchall()
    value["items"] = [information_item(conn, str(item["item_id"])) for item in items]
    return value


def latest_media_publications(conn: sqlite3.Connection, *, limit: int = 12) -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT publication_id FROM media_publications ORDER BY available_from DESC,publication_id LIMIT ?",
        (max(1, min(int(limit), 50)),),
    ).fetchall()
    return [media_publication(conn, str(row["publication_id"])) for row in rows]


def refresh_historical_tv_news(
    conn: sqlite3.Connection,
    sim_time: str,
    *,
    fetch=None,
    lookback_minutes: int = 90,
) -> dict[str, Any] | None:
    kwargs: dict[str, Any] = {"lookback_minutes": lookback_minutes, "limit": 40}
    if fetch is not None:
        kwargs["fetch"] = fetch
    records = gdelt_historical_articles(sim_time, **kwargs)
    if not records:
        return None
    item_ids = import_external_articles(conn, records)
    source_items = [information_item(conn, item_id) for item_id in item_ids]
    label = str(sim_time)[:10]
    bulletin, editorial = generate_news_bulletin(conn, source_items, bulletin_title=f"Evening News — {label}")
    selected = [str(story["source_item_id"]) for story in bulletin["stories"]]
    if not selected:
        selected = item_ids[:6]
    publication_id = _stable_id("publication", f"gdelt-tv:{sim_time[:16]}")
    try:
        available_until = (datetime.fromisoformat(sim_time.replace("Z", "+00:00")) + timedelta(hours=2)).isoformat()
    except Exception:
        available_until = None
    return create_tv_publication(
        conn,
        publication_id=publication_id,
        title=str(bulletin["title"]),
        summary=str(bulletin["summary"]),
        item_ids=selected,
        available_from=sim_time,
        available_until=available_until,
        editorial_provider_id=None if editorial is None else editorial["provider_id"],
        editorial_model_id=None if editorial is None else editorial["model_id"],
    )


def record_tv_exposure(
    conn: sqlite3.Connection,
    *,
    character_id: str,
    publication_id: str,
    sim_time: str,
    device_entity_id: str = TV_DEVICE_ID,
) -> dict[str, Any]:
    publication = media_publication(conn, publication_id)
    if publication["status"] != "active":
        raise ValueError("media publication is not active")
    device_location = _device_location(conn, device_entity_id)
    if device_location is None:
        raise ValueError("media device has no represented location")
    actor_location = get_field(conn, character_id, "runtime.location", None)
    if actor_location != device_location:
        raise ValueError("character is not co-located with the represented media device")
    stimulus_id = f"stimulus_media_{publication_id}"
    exposure_id = _stable_id("exposure", f"{character_id}:{stimulus_id}:{sim_time}")
    return record_character_exposure(
        conn,
        exposure_id=exposure_id,
        stimulus_id=stimulus_id,
        character_id=character_id,
        sim_time=sim_time,
        channel="media",
        source_location_id=device_location,
        source_entity_id=device_entity_id,
        metadata={"publication_id": publication_id, "proof": "explicit_tv_consumption"},
    )
