import json

from observer_sandbox.actor_runtime import actor_runtime, pending_action, set_actor_runtime, set_retry
from observer_sandbox.autonomy_recovery import DECISION_RECOVERY_THRESHOLD, recover_decision_livelock
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot


ACTOR = "char_darian"


def _seed_decision_errors(conn, sim_time: str, *, error_type: str, count: int) -> None:
    for _ in range(count):
        conn.execute(
            "INSERT INTO events(sim_time,actor_id,event_type,payload_json) VALUES(?,?,?,?)",
            (
                sim_time,
                ACTOR,
                "autonomy_error",
                json.dumps({
                    "stage": "decide",
                    "error_type": error_type,
                    "message": "synthetic repeated decision validation failure",
                    "retry_seconds": 8.0,
                }),
            ),
        )
    set_retry(
        conn,
        ACTOR,
        {
            "failures": count,
            "retry_after": 9999999999.0,
            "last_error": error_type,
        },
    )
    set_actor_runtime(
        conn,
        ACTOR,
        autonomy_enabled=True,
        autonomy_mode="normal",
        pending_action_id=None,
    )
    conn.commit()


def test_repeated_value_error_is_recovered_with_authoritative_pending_action(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        _seed_decision_errors(
            conn,
            state["sim_time"],
            error_type="ValueError",
            count=DECISION_RECOVERY_THRESHOLD,
        )

        result = recover_decision_livelock(conn, ACTOR, now_wall=1000.0)

        assert result is not None
        assert result["state"] == "planned"
        pending = pending_action(conn, ACTOR)
        assert pending is not None
        assert pending["conditions"]["autonomy_recovery"]["source"] == "autonomy-recovery-v1"
        assert pending["conditions"]["autonomy_recovery"]["basis"] == "repeated_decision_validation_failure"
        assert actor_runtime(conn, ACTOR)["retry"] is None
        event = conn.execute(
            "SELECT payload_json FROM events WHERE actor_id=? AND event_type='autonomy_recovery' ORDER BY id DESC LIMIT 1",
            (ACTOR,),
        ).fetchone()
        assert event is not None


def test_provider_error_is_not_masked_by_deterministic_recovery(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        _seed_decision_errors(
            conn,
            state["sim_time"],
            error_type="AIDecisionError",
            count=DECISION_RECOVERY_THRESHOLD,
        )

        result = recover_decision_livelock(conn, ACTOR, now_wall=1000.0)

        assert result is None
        assert pending_action(conn, ACTOR) is None
        assert actor_runtime(conn, ACTOR)["retry"] is not None
