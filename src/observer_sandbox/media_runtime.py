from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from typing import Any
from zoneinfo import ZoneInfo

from .location_runtime import current_location
from .spatial_familiarity import location_is_globally_hidden
from .world_stimulus import character_exposure, record_character_exposure


MEDIA_CONSUMPTION_ACTION = "consume_media"
MEDIA_CONSUMPTION_CAPABILITY = "consume_media"
NEWS_BROADCAST_TIMEZONE = ZoneInfo("America/Los_Angeles")
NEWS_BROADCAST_SLOTS: tuple[tuple[str, int], ...] = (("morning", 7), ("evening", 18))


def _aware_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _device_location(conn: sqlite3.Connection, entity_id: str) -> str | None:
    row = conn.execute(
        "SELECT source_id FROM relations WHERE relation_type='contains' AND target_id=? ORDER BY id LIMIT 1",
        (entity_id,),
    ).fetchone()
    return None if row is None else str(row["source_id"])


def active_media_publication(
    conn: sqlite3.Connection,
    *,
    device_entity_id: str,
    sim_time: str,
) -> dict[str, Any] | None:
    """Return the currently available represented publication for one media device.

    This is availability only. It never records exposure, perception, memory, belief,
    preference, or action authority.
    """
    row = conn.execute(
        """
        SELECT
            p.publication_id,p.medium,p.title,p.available_from,p.available_until,
            s.stimulus_id,d.device_type
        FROM media_devices d
        JOIN world_stimuli s
          ON s.source_entity_id=d.entity_id
         AND s.source_type='media_publication'
         AND s.channel='media'
        JOIN media_publications p ON p.publication_id=s.source_id
        WHERE d.entity_id=?
          AND d.status='active'
          AND s.status='active'
          AND p.status='active'
          AND s.start_sim_time<=?
          AND (s.end_sim_time IS NULL OR s.end_sim_time>?)
          AND p.available_from<=?
          AND (p.available_until IS NULL OR p.available_until>?)
        ORDER BY p.available_from DESC,p.publication_id DESC
        LIMIT 1
        """,
        (device_entity_id, sim_time, sim_time, sim_time, sim_time),
    ).fetchone()
    return None if row is None else dict(row)


def media_consumption_option_context(
    conn: sqlite3.Connection,
    *,
    device_entity_id: str,
    sim_time: str,
) -> dict[str, Any] | None:
    publication = active_media_publication(
        conn,
        device_entity_id=device_entity_id,
        sim_time=sim_time,
    )
    if publication is None:
        return None
    return {
        "publication_id": str(publication["publication_id"]),
        "medium": str(publication["medium"]),
        "program": str(publication["title"]),
        "available_from": str(publication["available_from"]),
        "available_until": publication["available_until"],
        "availability_only": True,
    }


def validate_media_consumption(
    conn: sqlite3.Connection,
    *,
    actor_id: str,
    device_entity_id: str,
    sim_time: str,
) -> dict[str, Any]:
    device = conn.execute(
        "SELECT device_type,status FROM media_devices WHERE entity_id=?",
        (device_entity_id,),
    ).fetchone()
    if device is None or str(device["status"]) != "active":
        raise ValueError(f"Target {device_entity_id} is not an active represented media device")
    location = _device_location(conn, device_entity_id)
    if location is None:
        raise ValueError(f"Media device {device_entity_id} has no represented location")
    if current_location(conn, actor_id) != location:
        raise ValueError(f"Character {actor_id} is not co-located with media device {device_entity_id}")
    publication = active_media_publication(
        conn,
        device_entity_id=device_entity_id,
        sim_time=sim_time,
    )
    if publication is None:
        raise ValueError(f"Media device {device_entity_id} has no active publication at {sim_time}")
    return publication


def record_media_consumption_exposure(
    conn: sqlite3.Connection,
    *,
    actor_id: str,
    device_entity_id: str,
    publication_id: str,
    sim_time: str,
    action_id: str,
) -> dict[str, Any]:
    publication = conn.execute(
        "SELECT status FROM media_publications WHERE publication_id=?",
        (publication_id,),
    ).fetchone()
    if publication is None or str(publication["status"]) != "active":
        raise ValueError(f"Unknown active media publication: {publication_id}")
    location = _device_location(conn, device_entity_id)
    if location is None:
        raise ValueError(f"Media device {device_entity_id} has no represented location")
    if current_location(conn, actor_id) != location:
        raise ValueError(f"Character {actor_id} is not co-located with media device {device_entity_id}")
    stimulus = conn.execute(
        """
        SELECT stimulus_id FROM world_stimuli
        WHERE source_type='media_publication' AND source_id=? AND source_entity_id=?
        ORDER BY stimulus_id LIMIT 1
        """,
        (publication_id, device_entity_id),
    ).fetchone()
    if stimulus is None:
        raise ValueError(
            f"Publication {publication_id} is not represented on media device {device_entity_id}"
        )
    exposure_id = "exposure_media_" + hashlib.sha256(
        f"{actor_id}:{action_id}:{stimulus['stimulus_id']}".encode("utf-8")
    ).hexdigest()[:20]
    existing = conn.execute(
        "SELECT 1 FROM character_exposures WHERE exposure_id=?",
        (exposure_id,),
    ).fetchone()
    if existing is not None:
        return character_exposure(conn, exposure_id)
    return record_character_exposure(
        conn,
        exposure_id=exposure_id,
        stimulus_id=str(stimulus["stimulus_id"]),
        character_id=actor_id,
        sim_time=sim_time,
        channel="media",
        source_location_id=location,
        source_entity_id=device_entity_id,
        metadata={
            "publication_id": publication_id,
            "proof": "completed_media_consumption_action",
            "action_id": action_id,
        },
    )


def media_cognition_context(
    conn: sqlite3.Connection,
    *,
    actor_id: str,
    sim_time: str,
) -> dict[str, Any]:
    """Expose neutral represented media availability without exposing content.

    The context deliberately contains schedule/device/program availability metadata
    only. Story titles, summaries, claims and source records remain behind exposure.
    """
    devices: list[dict[str, Any]] = []
    rows = conn.execute(
        """
        SELECT d.entity_id,d.device_type,e.name
        FROM media_devices d JOIN entities e ON e.id=d.entity_id
        WHERE d.status='active'
        ORDER BY d.entity_id
        """
    ).fetchall()
    actor_location = current_location(conn, actor_id)
    for row in rows:
        entity_id = str(row["entity_id"])
        location = _device_location(conn, entity_id)
        if location is None or location_is_globally_hidden(conn, location):
            continue
        location_row = conn.execute("SELECT name FROM entities WHERE id=?", (location,)).fetchone()
        publication = active_media_publication(
            conn,
            device_entity_id=entity_id,
            sim_time=sim_time,
        )
        devices.append({
            "device_name": str(row["name"]),
            "device_type": str(row["device_type"]),
            "location_name": str(location_row["name"]) if location_row is not None else location,
            "co_located": actor_location == location,
            "active_program": None if publication is None else str(publication["title"]),
            "active_program_available_until": None if publication is None else publication["available_until"],
        })
    return {
        "news_schedule": {
            "timezone": "America/Los_Angeles",
            "slots": [
                {"name": "Morning News", "local_time": "07:00"},
                {"name": "Evening News", "local_time": "18:00"},
            ],
        },
        "devices": devices,
        "semantics": (
            "Represented availability only. This does not mean the character has watched, heard, understood, believed, remembered, or prefers the content, and it creates no obligation to consume media. Exact executable authority remains action_options."
        ),
    }
