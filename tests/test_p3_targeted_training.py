from __future__ import annotations

import json

from observer_sandbox.actor_runtime import actor_runtime, pending_action, set_actor_runtime
from observer_sandbox.autonomy import autonomy_tick
from observer_sandbox.db import connect
from observer_sandbox.observer_query import observer_status, recent_history
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options
from observer_sandbox.telegram_bot import _fmt_history, _fmt_status
from observer_sandbox.telegram_notifications import format_action_completion
from observer_sandbox.world import set_field


HOME_GYM = "loc_thorne_estate_home_gym"
FREE_WEIGHTS = "obj_thorne_estate_gym_free_weights"
HEAVY_BAG = "obj_thorne_estate_gym_heavy_bag"
MASTER_SUITE = "loc_thorne_estate_master_suite"

GYM_TRAINING_TARGETS = {
    (FREE_WEIGHTS, "Free Weights"),
    (HEAVY_BAG, "Heavy Bag"),
    ("obj_thorne_estate_gym_olympic_platform", "Olympic Weightlifting Platform"),
    ("obj_thorne_estate_gym_power_rack", "Power Rack"),
    ("obj_thorne_estate_gym_adjustable_bench", "Adjustable Bench"),
    ("obj_thorne_estate_gym_strength_machines", "Strength Machine Circuit"),
    ("obj_thorne_estate_gym_high_speed_treadmill", "High-Speed Treadmill"),
    ("obj_thorne_estate_gym_rowing_ergometer", "Rowing Ergometer"),
    ("obj_thorne_estate_gym_speed_agility_station", "Speed & Agility Station"),
    ("obj_thorne_estate_gym_altitude_chamber", "Altitude Training Chamber"),
    ("obj_thorne_estate_gym_mobility_stretching", "Mobility & Stretching Area"),
}


class FixedTargetedTrainingProvider:
    def __init__(self, target: str) -> None:
        self.target = target

    def choose(self, snapshot, available_actions):
        assert "train" in available_actions
        return Action("train", 60, self.target, "A focused targeted training session fits the current routine.")


def _prepare_gym(conn) -> None:
    runtime = actor_runtime(conn, "char_darian")
    if runtime["pending_action_id"]:
        conn.execute(
            "UPDATE action_instances SET status='cancelled',updated_at=CURRENT_TIMESTAMP WHERE id=? AND status IN ('planned','in_progress')",
            (runtime["pending_action_id"],),
        )
    set_actor_runtime(
        conn,
        "char_darian",
        pending_action_id=None,
        autonomy_enabled=True,
        autonomy_mode="normal",
        wake_reason="p3_2_test",
    )
    conn.execute(
        "UPDATE actor_runtime SET lease_owner=NULL,lease_expires_at=NULL,retry_failures=0,retry_after=NULL,retry_last_error=NULL WHERE actor_id='char_darian'"
    )
    set_field(conn, "char_darian", "runtime.location", HOME_GYM)
    set_field(conn, "char_darian", "runtime.current_action", "idle")
    set_field(conn, "char_darian", "needs.energy", 80.0)
    set_field(conn, "char_darian", "physiology.fatigue", 0.0, authority="physiology_engine", source="p3.2-test")
    conn.commit()


def test_gym_exposes_real_training_targets_only_when_colocated(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", HOME_GYM)
        conn.commit()
        training = [option for option in action_options(conn) if option["action"] == "train"]
        assert {(row["target"], row["target_name"]) for row in training} == GYM_TRAINING_TARGETS

        set_field(conn, "char_darian", "runtime.location", MASTER_SUITE)
        conn.commit()
        assert not any(option["action"] == "train" for option in action_options(conn))


def test_autonomous_targeted_training_persists_target_and_completes(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare_gym(conn)
        provider = FixedTargetedTrainingProvider(HEAVY_BAG)

        planned = autonomy_tick(conn, provider=provider, now_wall=1000.0)
        assert planned["state"] == "planned"
        pending = pending_action(conn, "char_darian")
        assert pending is not None
        assert pending["action"] == "train"
        assert pending["target"] == HEAVY_BAG

        instance = conn.execute(
            "SELECT action_type,place_id,target_id,status FROM action_instances WHERE id=?",
            (pending["action_id"],),
        ).fetchone()
        assert dict(instance) == {
            "action_type": "train",
            "place_id": HOME_GYM,
            "target_id": HEAVY_BAG,
            "status": "in_progress",
        }

        completed = autonomy_tick(conn, provider=provider, now_wall=float(pending["due_wall_time"]) + 0.001)
        assert completed["state"] == "completed"
        assert completed["after"]["fatigue"] == 18.5

        event = conn.execute(
            "SELECT action_id,location_id,payload_json FROM events WHERE event_type='action_completed' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        payload = json.loads(event["payload_json"])
        assert event["action_id"] == pending["action_id"]
        assert event["location_id"] == HOME_GYM
        assert payload["action"] == "train"
        assert payload["target"] == HEAVY_BAG


def test_targeted_training_is_friendly_across_observer_surfaces(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare_gym(conn)
        provider = FixedTargetedTrainingProvider(FREE_WEIGHTS)
        planned = autonomy_tick(conn, provider=provider, now_wall=2000.0)
        pending = pending_action(conn, "char_darian")
        assert planned["state"] == "planned"
        assert pending is not None

        status = observer_status(conn)
        assert status["pending_target_name"] == "Free Weights"
        assert "Train → Free Weights" in _fmt_status(status)

        before = dict(status["character"])
        completed = autonomy_tick(conn, provider=provider, now_wall=float(pending["due_wall_time"]) + 0.001)
        after = completed["after"]
        history = recent_history(conn, limit=5)
        completed_row = next(row for row in history if row.get("action") == "train")
        assert completed_row["target_name"] == "Free Weights"
        assert "Train → Free Weights" in _fmt_history(history)

        message = format_action_completion(
            {
                "action": "train",
                "target": FREE_WEIGHTS,
                "target_name": "Free Weights",
                "reason": "A focused targeted training session fits the current routine.",
            },
            before,
            after,
            actor_name="Darian Thorne",
        )
        assert "Train → Free Weights" in message
        assert FREE_WEIGHTS not in message
