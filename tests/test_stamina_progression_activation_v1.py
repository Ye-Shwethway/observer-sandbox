from datetime import datetime, timedelta, timezone

from observer_sandbox.db import connect
from observer_sandbox.event_log import record_event
from observer_sandbox.runtime import initialize
from observer_sandbox.stamina_progression_activation import maybe_settle_stamina_progression, stamina_progression_due


def healthy():
    return {"energy": 75, "sleepiness": 25, "fatigue": 20}


def cardio():
    return {"action": "train", "training_method": {"method_id": "steady_state_cardio", "source": "training-method-semantics-v1", "effective_load": {"effective_minutes": 45.0}}}


def test_activation_bootstrap_and_30h_eligibility(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, tzinfo=timezone.utc)
    with connect(db) as conn:
        old_id = record_event(conn, sim_time=(t0 - timedelta(days=2)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=cardio())
        conn.commit()
        boot = maybe_settle_stamina_progression(conn, "char_darian", as_of_sim_time=t0.isoformat(), state=healthy())
        assert boot["settlement"]["status"] == "bootstrapped"
        assert old_id in boot["settlement"]["consumed_stimulus_event_ids"]
        assert boot["settlement"]["net_delta"] == 0.0

        new_id = record_event(conn, sim_time=(t0 + timedelta(minutes=1)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=cardio())
        conn.commit()
        early = stamina_progression_due(conn, "char_darian", as_of_sim_time=(t0 + timedelta(hours=29)).isoformat(), state=healthy())
        assert new_id not in early.eligible_stimulus_event_ids
        due = stamina_progression_due(conn, "char_darian", as_of_sim_time=(t0 + timedelta(hours=30, minutes=1)).isoformat(), state=healthy())
        assert due.reason == "eligible_stimulus"
        assert due.eligible_stimulus_event_ids == (new_id,)


def test_fatigue_block_preserves_pending_stimulus(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, tzinfo=timezone.utc)
    with connect(db) as conn:
        maybe_settle_stamina_progression(conn, "char_darian", as_of_sim_time=t0.isoformat(), state=healthy())
        event_id = record_event(conn, sim_time=(t0 + timedelta(minutes=1)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=cardio())
        conn.commit()
        blocked = stamina_progression_due(conn, "char_darian", as_of_sim_time=(t0 + timedelta(hours=31)).isoformat(), state={"energy": 80, "sleepiness": 15, "fatigue": 70})
        assert event_id not in blocked.eligible_stimulus_event_ids
        recovered = stamina_progression_due(conn, "char_darian", as_of_sim_time=(t0 + timedelta(hours=31)).isoformat(), state=healthy())
        assert recovered.reason == "eligible_stimulus"
        assert event_id in recovered.eligible_stimulus_event_ids
