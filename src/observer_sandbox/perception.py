from __future__ import annotations

import json
import sqlite3
from typing import Any


PERCEPTION_MODE = "exposure_projection_v1"


def recent_perception_context(
    conn: sqlite3.Connection,
    character_id: str,
    *,
    sim_time: str,
    limit: int = 8,
) -> dict[str, Any]:
    """Project recent valid exposure into bounded actor-relative perception input.

    This is deliberately a deterministic provenance-preserving projection. It says
    only that the represented signal reached this actor through an implemented
    exposure channel. It does not assert understanding, belief, appraisal, memory,
    relationship meaning, intention, or action authority.
    """
    if conn.execute(
        "SELECT 1 FROM entities WHERE id=? AND entity_type='character'",
        (character_id,),
    ).fetchone() is None:
        raise ValueError(f"unknown character: {character_id}")

    bounded_limit = max(1, min(int(limit), 50))
    rows = conn.execute(
        """
        SELECT
            e.exposure_id,
            e.stimulus_id,
            e.sim_time AS exposed_at,
            e.channel AS exposure_channel,
            e.source_location_id,
            e.source_entity_id,
            e.attention_hint,
            e.metadata_json AS exposure_metadata_json,
            s.stimulus_type,
            s.channel AS stimulus_channel,
            s.subject,
            s.payload_json,
            s.source_type,
            s.source_id,
            s.source_event_id,
            s.source_entity_id AS stimulus_source_entity_id,
            s.salience,
            s.metadata_json AS stimulus_metadata_json
        FROM character_exposures e
        JOIN world_stimuli s ON s.stimulus_id=e.stimulus_id
        WHERE e.character_id=?
          AND e.status='exposed'
          AND e.sim_time<=?
        ORDER BY e.sim_time DESC,e.created_at DESC,e.exposure_id DESC
        LIMIT ?
        """,
        (character_id, sim_time, bounded_limit),
    ).fetchall()

    perceived_inputs: list[dict[str, Any]] = []
    for row in reversed(rows):
        source_links = []
        if row["source_type"] or row["source_id"]:
            source_links.append(
                {
                    "type": row["source_type"],
                    "id": row["source_id"],
                }
            )
        if row["source_event_id"] is not None:
            source_links.append({"type": "event", "id": int(row["source_event_id"])})
        source_entity_id = row["stimulus_source_entity_id"] or row["source_entity_id"]
        if source_entity_id:
            source_links.append({"type": "entity", "id": source_entity_id})
        if row["source_location_id"]:
            source_links.append({"type": "location", "id": row["source_location_id"]})

        perceived_inputs.append(
            {
                "exposure_id": row["exposure_id"],
                "stimulus_id": row["stimulus_id"],
                "stimulus_type": row["stimulus_type"],
                "channel": row["exposure_channel"] or row["stimulus_channel"],
                "subject": row["subject"],
                "world_payload": json.loads(row["payload_json"] or "{}"),
                "source_links": source_links,
                "exposed_at": row["exposed_at"],
                "external_salience": float(row["salience"]),
                "attention_hint": row["attention_hint"],
                "provenance": {
                    "stimulus": json.loads(row["stimulus_metadata_json"] or "{}"),
                    "exposure": json.loads(row["exposure_metadata_json"] or "{}"),
                },
            }
        )

    return {
        "mode": PERCEPTION_MODE,
        "inputs": perceived_inputs,
        "semantics": (
            "Actor-relative records of represented signals that reached this character. "
            "They are perception inputs, not claims of understanding, belief, appraisal, "
            "memory, relationship meaning, intention, or action authority."
        ),
    }
