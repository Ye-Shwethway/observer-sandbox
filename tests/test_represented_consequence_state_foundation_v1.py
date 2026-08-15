from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.event_log import record_event
from observer_sandbox.represented_consequence_state import (
    EVENT_TYPE,
    ConsequenceAuthorization,
    RepresentedConsequenceStateError,
    StateMutation,
    apply_represented_consequence,
)
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import ensure_sim_clock
from observer_sandbox.world import get_field, set_field


ACTOR = "char_darian"
TASK = "test_represented_consequence_task_v1"


def _actor_location(conn) -> str:
    row = conn.execute(
        """SELECT target_id FROM relations
        WHERE source_id=? AND relation_type='located_at' LIMIT 1""",
        (ACTOR,),
    ).fetchone()
    if row is not None:
        return str(row[0])
    value = get_field(conn, ACTOR, "runtime.location")
    assert isinstance(value, str)
    return value


def _seed_completed_represented_action(
    conn,
    *,
    action_id: str = "test-consequence-action",
    task_id: str = TASK,
    status: str = "completed",
    target_id: str | None = None,
    participants: tuple[str, ...] = (),
) -> int | None:
    sim_time = ensure_sim_clock(conn).isoformat()
    outcome = {
        "represented_skill_task": {
            "task": {
                "task_id": task_id,
                "status": "authorized",
            }
        }
    }
    conn.execute(
        """INSERT INTO action_instances(
            id,action_type,actor_id,place_id,target_id,status,duration_minutes,intent,
            participants_json,resources_json,conditions_json,modifiers_json,
            planned_sim_time,started_sim_time,ended_sim_time,outcome_json
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            action_id,
            "idle",
            ACTOR,
            _actor_location(conn),
            target_id,
            status,
            5,
            "ephemeral represented consequence foundation fixture",
            json.dumps(list(participants)),
            "[]",
            "{}",
            "{}",
            sim_time,
            sim_time,
            sim_time if status == "completed" else None,
            json.dumps(outcome),
        ),
    )
    for participant in participants:
        conn.execute(
            "INSERT INTO action_participants(action_id,entity_id,role) VALUES(?,?,?)",
            (action_id, participant, "participant"),
        )
    if status != "completed":
        conn.commit()
        return None
    event_id = record_event(
        conn,
        sim_time=sim_time,
        event_type="action_completed",
        actor_id=ACTOR,
        action_id=action_id,
        location_id=_actor_location(conn),
        participants=[{"entity_id": value, "role": "participant"} for value in participants],
        payload={
            "action_id": action_id,
            "action": "idle",
            "duration_minutes": 5,
            "target": target_id,
        },
    )
    conn.commit()
    return event_id


def _authorization(
    *,
    consequence_id: str = "test_condition_delta",
    task_id: str = TASK,
    subject_id: str = ACTOR,
    subject_role: str = "actor",
    mutations: tuple[StateMutation, ...] = (StateMutation("simulation.test_condition", "add", 2.5),),
) -> ConsequenceAuthorization:
    return ConsequenceAuthorization(
        consequence_id=consequence_id,
        represented_task_id=task_id,
        subject_id=subject_id,
        subject_role=subject_role,
        mutations=mutations,
    )


def test_applies_authorized_simulated_state_and_emits_causal_event(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(
            conn,
            ACTOR,
            "simulation.test_condition",
            10.0,
            mode="simulated",
            authority="test_domain",
            source="test_fixture",
        )
        completion_event_id = _seed_completed_represented_action(conn)

        result = apply_represented_consequence(
            conn,
            action_id="test-consequence-action",
            authorization=_authorization(),
        )
        conn.commit()

        assert result["already_applied"] is False
        assert get_field(conn, ACTOR, "simulation.test_condition") == pytest.approx(12.5)
        field = conn.execute(
            "SELECT mode,authority,source FROM fields WHERE entity_id=? AND field_key=?",
            (ACTOR, "simulation.test_condition"),
        ).fetchone()
        assert tuple(field) == ("simulated", "test_domain", "test_fixture")

        event = conn.execute(
            """SELECT id,event_type,actor_id,action_id,location_id,caused_by_event_id,
            payload_json,state_changes_json FROM events WHERE id=?""",
            (result["event_id"],),
        ).fetchone()
        assert event["event_type"] == EVENT_TYPE
        assert event["actor_id"] == ACTOR
        assert event["action_id"] == "test-consequence-action"
        assert event["caused_by_event_id"] == completion_event_id
        payload = json.loads(event["payload_json"])
        assert payload["authorization"] == "deterministic_consequence_contract"
        assert payload["represented_task_id"] == TASK
        assert payload["learning_evidence"] is False
        changes = json.loads(event["state_changes_json"])
        assert changes["fields"]["simulation.test_condition"] == {
            "before": 10.0,
            "after": 12.5,
            "operation": "add",
            "operand": 2.5,
        }
        actor_participant = conn.execute(
            "SELECT role FROM event_participants WHERE event_id=? AND entity_id=?",
            (result["event_id"], ACTOR),
        ).fetchone()
        assert actor_participant["role"] == "actor"


def test_retry_is_idempotent_and_does_not_double_apply_additive_consequence(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, ACTOR, "simulation.test_condition", 10.0)
        _seed_completed_represented_action(conn)
        first = apply_represented_consequence(
            conn,
            action_id="test-consequence-action",
            authorization=_authorization(),
        )
        second = apply_represented_consequence(
            conn,
            action_id="test-consequence-action",
            authorization=_authorization(),
        )
        conn.commit()

        assert first["already_applied"] is False
        assert second["already_applied"] is True
        assert second["event_id"] == first["event_id"]
        assert get_field(conn, ACTOR, "simulation.test_condition") == pytest.approx(12.5)
        count = conn.execute(
            "SELECT COUNT(*) FROM events WHERE action_id=? AND event_type=?",
            ("test-consequence-action", EVENT_TYPE),
        ).fetchone()[0]
        assert count == 1


def test_participant_subject_requires_exact_action_participation(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        participant = "char_test_consequence_participant"
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json) VALUES(?,?,?,?,?)",
            (participant, "character", "Ephemeral Consequence Participant", "{}", "[]"),
        )
        set_field(conn, participant, "simulation.control_state", "free")
        _seed_completed_represented_action(conn, participants=(participant,))

        result = apply_represented_consequence(
            conn,
            action_id="test-consequence-action",
            authorization=_authorization(
                consequence_id="test_participant_control_state",
                subject_id=participant,
                subject_role="participant",
                mutations=(StateMutation("simulation.control_state", "set", "stabilized"),),
            ),
        )
        conn.commit()

        assert get_field(conn, participant, "simulation.control_state") == "stabilized"
        row = conn.execute(
            "SELECT role FROM event_participants WHERE event_id=? AND entity_id=?",
            (result["event_id"], participant),
        ).fetchone()
        assert row["role"] == "consequence_subject"


def test_wrong_task_authorization_fails_without_state_or_event(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, ACTOR, "simulation.test_condition", 10.0)
        _seed_completed_represented_action(conn)

        with pytest.raises(RepresentedConsequenceStateError, match="task does not match"):
            apply_represented_consequence(
                conn,
                action_id="test-consequence-action",
                authorization=_authorization(task_id="different_task_v1"),
            )

        assert get_field(conn, ACTOR, "simulation.test_condition") == 10.0
        assert conn.execute(
            "SELECT 1 FROM events WHERE action_id=? AND event_type=?",
            ("test-consequence-action", EVENT_TYPE),
        ).fetchone() is None


def test_non_simulated_field_is_never_mutated(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(
            conn,
            ACTOR,
            "canonical.test_truth",
            10.0,
            mode="canonical",
            authority="canonical_profile",
            source="canonical_fixture",
        )
        _seed_completed_represented_action(conn)

        with pytest.raises(RepresentedConsequenceStateError, match="must be simulated"):
            apply_represented_consequence(
                conn,
                action_id="test-consequence-action",
                authorization=_authorization(
                    mutations=(StateMutation("canonical.test_truth", "add", 5.0),),
                ),
            )

        assert get_field(conn, ACTOR, "canonical.test_truth") == 10.0
        row = conn.execute(
            "SELECT mode,authority,source FROM fields WHERE entity_id=? AND field_key=?",
            (ACTOR, "canonical.test_truth"),
        ).fetchone()
        assert tuple(row) == ("canonical", "canonical_profile", "canonical_fixture")


def test_noncompleted_source_action_is_rejected(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, ACTOR, "simulation.test_condition", 10.0)
        _seed_completed_represented_action(conn, status="in_progress")

        with pytest.raises(RepresentedConsequenceStateError, match="completed source action"):
            apply_represented_consequence(
                conn,
                action_id="test-consequence-action",
                authorization=_authorization(),
            )
        assert get_field(conn, ACTOR, "simulation.test_condition") == 10.0


def test_savepoint_rolls_back_earlier_field_write_when_later_operation_is_invalid(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, ACTOR, "simulation.test_condition", 10.0)
        set_field(conn, ACTOR, "simulation.test_label", "ready")
        _seed_completed_represented_action(conn)

        with pytest.raises(RepresentedConsequenceStateError, match="requires a numeric value"):
            apply_represented_consequence(
                conn,
                action_id="test-consequence-action",
                authorization=_authorization(
                    mutations=(
                        StateMutation("simulation.test_condition", "add", 5.0),
                        StateMutation("simulation.test_label", "multiply", 2.0),
                    ),
                ),
            )

        assert get_field(conn, ACTOR, "simulation.test_condition") == 10.0
        assert get_field(conn, ACTOR, "simulation.test_label") == "ready"
        assert conn.execute(
            "SELECT 1 FROM events WHERE action_id=? AND event_type=?",
            ("test-consequence-action", EVENT_TYPE),
        ).fetchone() is None


def test_subject_relation_mismatch_fails_closed(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        outsider = "char_test_consequence_outsider"
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json) VALUES(?,?,?,?,?)",
            (outsider, "character", "Ephemeral Consequence Outsider", "{}", "[]"),
        )
        set_field(conn, outsider, "simulation.test_condition", 10.0)
        _seed_completed_represented_action(conn)

        with pytest.raises(RepresentedConsequenceStateError, match="not the authorized participant"):
            apply_represented_consequence(
                conn,
                action_id="test-consequence-action",
                authorization=_authorization(
                    subject_id=outsider,
                    subject_role="participant",
                ),
            )
        assert get_field(conn, outsider, "simulation.test_condition") == 10.0
