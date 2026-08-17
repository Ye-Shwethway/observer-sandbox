from __future__ import annotations

import sqlite3
import uuid
from typing import Any, Iterable

from .event_log import record_event
from .location_runtime import current_location
from .world_stimulus import add_stimulus_scope, create_world_stimulus, record_character_exposure


def _require_character(conn: sqlite3.Connection, entity_id: str, *, role: str) -> str:
    row = conn.execute(
        "SELECT entity_type FROM entities WHERE id=?",
        (entity_id,),
    ).fetchone()
    if row is None or row["entity_type"] != "character":
        raise ValueError(f"{role} is not a represented character: {entity_id}")
    return str(entity_id)


def record_direct_utterance(
    conn: sqlite3.Connection,
    *,
    sender_id: str,
    recipient_ids: Iterable[str],
    sim_time: str,
    content: str,
    salience: float = 0.5,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Persist direct-speech truth and W0 exposure without interpreting the content.

    Intended recipients are part of the authoritative utterance event. Only represented
    intended recipients co-located with the sender at this boundary receive a W0
    `character_exposure` row. This function creates no Memory/Mind/relationship state.
    """
    sender_id = _require_character(conn, str(sender_id), role="sender")
    recipients = [str(value) for value in recipient_ids]
    recipients = list(dict.fromkeys(recipients))
    if not recipients:
        raise ValueError("at least one recipient is required")
    if not str(content).strip():
        raise ValueError("content is required")
    for recipient_id in recipients:
        _require_character(conn, recipient_id, role="recipient")
        if recipient_id == sender_id:
            raise ValueError("sender cannot be an intended recipient of direct speech")

    sender_location = current_location(conn, sender_id)
    event_id = record_event(
        conn,
        sim_time=sim_time,
        event_type="communication_utterance",
        actor_id=sender_id,
        location_id=sender_location,
        participants=[
            {"entity_id": recipient_id, "role": "intended_recipient"}
            for recipient_id in recipients
        ],
        payload={
            "channel": "direct",
            "content": content,
            "recipient_ids": recipients,
            "metadata": dict(metadata or {}),
        },
    )

    stimulus_id = f"communication:{uuid.uuid4()}"
    create_world_stimulus(
        conn,
        stimulus_id=stimulus_id,
        stimulus_type="communication",
        channel="direct",
        subject="Direct utterance",
        start_sim_time=sim_time,
        end_sim_time=sim_time,
        payload={"content": content, "sender_id": sender_id},
        source_type="communication_utterance",
        source_id=str(event_id),
        source_event_id=event_id,
        source_entity_id=sender_id,
        salience=salience,
        metadata={"delivery_mode": "co_location", **dict(metadata or {})},
    )
    for recipient_id in recipients:
        add_stimulus_scope(
            conn,
            stimulus_id=stimulus_id,
            scope_type="character",
            scope_id=recipient_id,
            relation_role="intended_recipient",
        )

    exposures: list[dict[str, Any]] = []
    if sender_location is not None:
        for recipient_id in recipients:
            if current_location(conn, recipient_id) != sender_location:
                continue
            exposures.append(
                record_character_exposure(
                    conn,
                    exposure_id=f"communication-exposure:{uuid.uuid4()}",
                    stimulus_id=stimulus_id,
                    character_id=recipient_id,
                    sim_time=sim_time,
                    channel="direct",
                    source_location_id=sender_location,
                    source_entity_id=sender_id,
                    metadata={
                        "communication_event_id": event_id,
                        "delivery": "heard_directly",
                    },
                )
            )

    conn.commit()
    return {
        "event_id": event_id,
        "stimulus_id": stimulus_id,
        "sender_id": sender_id,
        "recipient_ids": recipients,
        "sender_location_id": sender_location,
        "exposures": exposures,
    }
