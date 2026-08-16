from __future__ import annotations

from observer_sandbox.db import connect
from observer_sandbox.event_log import record_event
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize


PARTICIPANT = "char_test_recent_event_participant"
UNRELATED = "char_test_recent_event_unrelated"
ROOM = "loc_thorne_estate_training_hall"


def _insert_character(conn, character_id: str, name: str) -> None:
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json,definition_id) VALUES(?,?,?,?,?,?)",
        (character_id, "character", name, "{}", "[]", f"test:{character_id}"),
    )


def _provider(conn, character_id: str) -> ModelDecisionProvider:
    return ModelDecisionProvider(
        conn,
        character_id=character_id,
        policy={"repetition_policy": {"recent_event_window": 8}},
    )


def test_actor_owned_event_remains_visible_once_with_actor_role(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        record_event(
            conn,
            sim_time="2025-05-01T08:00:00+00:00",
            event_type="action_completed",
            actor_id="char_darian",
            location_id=ROOM,
            payload={"action": "idle", "reason": "quiet reset"},
        )
        conn.commit()

        recent = _provider(conn, "char_darian")._recent_events()
        matches = [event for event in recent if event["reason"] == "quiet reset"]

        assert len(matches) == 1
        assert matches[0]["actor_id"] == "char_darian"
        assert matches[0]["participation_role"] == "actor"


def test_non_actor_participant_receives_authoritative_shared_event_context(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        _insert_character(conn, PARTICIPANT, "Recent Event Participant")
        record_event(
            conn,
            sim_time="2025-05-01T08:10:00+00:00",
            event_type="action_completed",
            actor_id="char_darian",
            location_id=ROOM,
            participants=[{"entity_id": PARTICIPANT, "role": "partner"}],
            payload={
                "action": "spar",
                "target": "obj_shared_session",
                "reason": "controlled practice",
            },
        )
        conn.commit()

        recent = _provider(conn, PARTICIPANT)._recent_events()

        assert recent == [
            {
                "sim_time": "2025-05-01T08:10:00+00:00",
                "event_type": "action_completed",
                "location_id": ROOM,
                "actor_id": "char_darian",
                "participation_role": "partner",
                "action": "spar",
                "target": "obj_shared_session",
                "reason": "controlled practice",
            }
        ]


def test_unrelated_character_does_not_receive_other_characters_event(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        _insert_character(conn, PARTICIPANT, "Recent Event Participant")
        _insert_character(conn, UNRELATED, "Unrelated Character")
        record_event(
            conn,
            sim_time="2025-05-01T08:20:00+00:00",
            event_type="action_completed",
            actor_id="char_darian",
            location_id=ROOM,
            participants=[{"entity_id": PARTICIPANT, "role": "partner"}],
            payload={"action": "spar", "reason": "shared only"},
        )
        conn.commit()

        assert _provider(conn, UNRELATED)._recent_events() == []


def test_recent_event_limit_and_chronological_order_span_actor_and_participant_roles(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        _insert_character(conn, PARTICIPANT, "Recent Event Participant")
        _insert_character(conn, UNRELATED, "Unrelated Character")

        record_event(
            conn,
            sim_time="2025-05-01T08:00:00+00:00",
            event_type="action_completed",
            actor_id=PARTICIPANT,
            location_id=ROOM,
            payload={"action": "idle", "reason": "old self event"},
        )
        record_event(
            conn,
            sim_time="2025-05-01T08:05:00+00:00",
            event_type="action_completed",
            actor_id=UNRELATED,
            location_id=ROOM,
            payload={"action": "idle", "reason": "unrelated interleave"},
        )
        record_event(
            conn,
            sim_time="2025-05-01T08:10:00+00:00",
            event_type="action_completed",
            actor_id="char_darian",
            location_id=ROOM,
            participants=[{"entity_id": PARTICIPANT, "role": "partner"}],
            payload={"action": "spar", "reason": "shared event"},
        )
        record_event(
            conn,
            sim_time="2025-05-01T08:15:00+00:00",
            event_type="action_completed",
            actor_id=PARTICIPANT,
            location_id=ROOM,
            payload={"action": "rest", "reason": "new self event"},
        )
        conn.commit()

        recent = _provider(conn, PARTICIPANT)._recent_events(limit=2)

        assert [event["reason"] for event in recent] == ["shared event", "new self event"]
        assert [event["participation_role"] for event in recent] == ["partner", "actor"]
