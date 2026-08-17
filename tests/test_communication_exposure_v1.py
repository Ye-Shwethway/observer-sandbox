from __future__ import annotations

from observer_sandbox.communication import record_direct_utterance
from observer_sandbox.db import connect, migrate
from observer_sandbox.location_runtime import set_dynamic_location


def _db(tmp_path):
    conn = connect(tmp_path / "observer.db")
    migrate(conn)
    for entity_id, entity_type, name in (
        ("room-a", "location", "Room A"),
        ("room-b", "location", "Room B"),
        ("speaker", "character", "Speaker"),
        ("listener", "character", "Listener"),
        ("away", "character", "Away"),
        ("unrelated", "character", "Unrelated"),
        ("fixture", "object", "Fixture"),
    ):
        conn.execute(
            "INSERT INTO entities(id,entity_type,name) VALUES(?,?,?)",
            (entity_id, entity_type, name),
        )
    set_dynamic_location(conn, "speaker", "room-a")
    set_dynamic_location(conn, "listener", "room-a")
    set_dynamic_location(conn, "away", "room-b")
    set_dynamic_location(conn, "unrelated", "room-a")
    conn.commit()
    return conn


def test_direct_utterance_records_truth_targeted_stimulus_and_only_colocated_exposure(tmp_path):
    conn = _db(tmp_path)
    result = record_direct_utterance(
        conn,
        sender_id="speaker",
        recipient_ids=["listener", "away"],
        sim_time="2025-05-16T12:00:00+00:00",
        content="Meet me outside after lunch.",
    )

    event = conn.execute("SELECT * FROM events WHERE id=?", (result["event_id"],)).fetchone()
    assert event["event_type"] == "communication_utterance"
    assert event["actor_id"] == "speaker"
    participants = conn.execute(
        "SELECT entity_id,role FROM event_participants WHERE event_id=? ORDER BY entity_id",
        (result["event_id"],),
    ).fetchall()
    assert {(row["entity_id"], row["role"]) for row in participants} == {
        ("speaker", "actor"),
        ("listener", "intended_recipient"),
        ("away", "intended_recipient"),
    }

    stimulus = conn.execute(
        "SELECT stimulus_type,channel,source_event_id,source_entity_id FROM world_stimuli WHERE stimulus_id=?",
        (result["stimulus_id"],),
    ).fetchone()
    assert tuple(stimulus) == ("communication", "direct", result["event_id"], "speaker")
    scopes = conn.execute(
        "SELECT scope_type,scope_id FROM world_stimulus_scopes WHERE stimulus_id=? ORDER BY scope_id",
        (result["stimulus_id"],),
    ).fetchall()
    assert [(row["scope_type"], row["scope_id"]) for row in scopes] == [
        ("character", "away"),
        ("character", "listener"),
    ]

    exposures = conn.execute(
        "SELECT character_id,channel,source_location_id,source_entity_id FROM character_exposures WHERE stimulus_id=?",
        (result["stimulus_id"],),
    ).fetchall()
    assert [tuple(row) for row in exposures] == [("listener", "direct", "room-a", "speaker")]


def test_direct_utterance_does_not_mutate_memory_mind_relationship_or_unrelated_actor(tmp_path):
    conn = _db(tmp_path)
    before = {
        "memory": conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0],
        "cycles": conn.execute("SELECT COUNT(*) FROM mental_cycles").fetchone()[0],
        "episodes": conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0],
        "artifacts": conn.execute("SELECT COUNT(*) FROM mental_artifacts").fetchone()[0],
        "relationships": conn.execute("SELECT COUNT(*) FROM character_relationship_state").fetchone()[0],
    }
    result = record_direct_utterance(
        conn,
        sender_id="speaker",
        recipient_ids=["listener"],
        sim_time="2025-05-16T12:00:00+00:00",
        content="Hello.",
    )
    after = {
        "memory": conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0],
        "cycles": conn.execute("SELECT COUNT(*) FROM mental_cycles").fetchone()[0],
        "episodes": conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0],
        "artifacts": conn.execute("SELECT COUNT(*) FROM mental_artifacts").fetchone()[0],
        "relationships": conn.execute("SELECT COUNT(*) FROM character_relationship_state").fetchone()[0],
    }
    assert after == before
    assert conn.execute(
        "SELECT COUNT(*) FROM character_exposures WHERE stimulus_id=? AND character_id='unrelated'",
        (result["stimulus_id"],),
    ).fetchone()[0] == 0


def test_direct_utterance_fails_closed_for_invalid_participants(tmp_path):
    conn = _db(tmp_path)
    for kwargs in (
        {"sender_id": "fixture", "recipient_ids": ["listener"]},
        {"sender_id": "speaker", "recipient_ids": ["fixture"]},
        {"sender_id": "speaker", "recipient_ids": ["speaker"]},
    ):
        try:
            record_direct_utterance(
                conn,
                sim_time="2025-05-16T12:00:00+00:00",
                content="Test",
                **kwargs,
            )
        except ValueError:
            pass
        else:
            raise AssertionError("invalid direct communication participant must fail closed")


def test_direct_utterance_is_character_generic(tmp_path):
    conn = _db(tmp_path)
    result = record_direct_utterance(
        conn,
        sender_id="away",
        recipient_ids=["speaker"],
        sim_time="2025-05-16T12:01:00+00:00",
        content="Different fixture identities use the same runtime.",
    )
    assert result["sender_id"] == "away"
    assert result["exposures"] == []
