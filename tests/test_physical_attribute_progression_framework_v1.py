from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from observer_sandbox.db import connect
from observer_sandbox.event_log import record_event
from observer_sandbox.physical_attribute_progression import (
    physical_attribute_keys,
    physical_attribute_policy,
    physical_attribute_stimulus_events,
    settle_physical_attribute_progression,
)
from observer_sandbox.profile_seed import import_seed
from observer_sandbox.runtime import initialize
from observer_sandbox.training_methods import training_profile_for_target


DAR = "char_darian"
FIXTURE = "char_fixture"


def healthy() -> dict[str, float]:
    return {"energy": 90.0, "sleepiness": 10.0, "fatigue": 10.0}


def training_payload(method_id: str, minutes: float = 30.0) -> dict:
    return {
        "action": "train",
        "training_method": {
            "method_id": method_id,
            "source": "training-method-semantics-v1",
            "effective_load": {"effective_minutes": minutes},
        },
    }


def value(conn, actor_id: str, field_key: str) -> float:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, field_key),
    ).fetchone()
    assert row is not None
    return float(json.loads(row["value_json"]))


def add_fixture_character(conn) -> None:
    import_seed(
        conn,
        {
            "entity_id": FIXTURE,
            "name": "Fixture Character",
            "canonical_revision": "fixture-pa-v1",
            "profile_schema_version": 1,
            "values": {
                "raps_pa.speed": {"value": 50, "mode": "static", "authority": "attribute_engine"},
                "raps_pa.reflexes": {"value": 50, "mode": "static", "authority": "attribute_engine"},
                "raps_pa.endurance": {"value": 50, "mode": "static", "authority": "attribute_engine"},
                "raps_pa.flexibility": {"value": 50, "mode": "static", "authority": "attribute_engine"},
            },
        },
    )


def test_policy_batch_is_the_four_remaining_physical_attributes():
    assert physical_attribute_keys() == ("speed", "reflexes", "endurance", "flexibility")
    assert physical_attribute_policy("speed").field_key == "raps_pa.speed"
    assert physical_attribute_policy("reflexes").field_key == "raps_pa.reflexes"
    assert physical_attribute_policy("endurance").field_key == "raps_pa.endurance"
    assert physical_attribute_policy("flexibility").field_key == "raps_pa.flexibility"


def test_actor_generic_speed_progression_works_for_non_darian_character(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, tzinfo=timezone.utc)
    with connect(db) as conn:
        add_fixture_character(conn)
        darian_before = value(conn, DAR, "raps_pa.speed")
        fixture_before = value(conn, FIXTURE, "raps_pa.speed")

        bootstrap = settle_physical_attribute_progression(
            conn, FIXTURE, "speed", as_of_sim_time=t0.isoformat(), state=healthy()
        )
        assert bootstrap["status"] == "bootstrapped"
        assert bootstrap["net_delta"] == 0.0
        assert value(conn, FIXTURE, "raps_pa.speed") == fixture_before

        event_time = t0 + timedelta(minutes=1)
        event_id = record_event(
            conn,
            sim_time=event_time.isoformat(),
            actor_id=FIXTURE,
            event_type="action_completed",
            payload=training_payload("speed_agility_drills", 30.0),
        )
        conn.commit()
        policy = physical_attribute_policy("speed")
        result = settle_physical_attribute_progression(
            conn,
            FIXTURE,
            "speed",
            as_of_sim_time=(event_time + timedelta(hours=policy.full_recovery_hours)).isoformat(),
            state=healthy(),
        )
        assert event_id in result["consumed_stimulus_event_ids"]
        assert result["positive_delta"] > 0.0
        assert value(conn, FIXTURE, "raps_pa.speed") > fixture_before
        assert value(conn, DAR, "raps_pa.speed") == darian_before

        replay = settle_physical_attribute_progression(
            conn,
            FIXTURE,
            "speed",
            as_of_sim_time=(event_time + timedelta(hours=policy.full_recovery_hours)).isoformat(),
            state=healthy(),
        )
        assert replay["status"] == "no_change"


def test_evidence_domains_remain_distinct(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, tzinfo=timezone.utc)
    with connect(db) as conn:
        ids = {}
        for method_id in (
            "steady_state_cardio",
            "speed_agility_drills",
            "ai_combat_simulation",
            "obstacle_conditioning",
            "mobility_stretching",
        ):
            ids[method_id] = record_event(
                conn,
                sim_time=t0.isoformat(),
                actor_id=DAR,
                event_type="action_completed",
                payload=training_payload(method_id),
            )
        conn.commit()

        speed = physical_attribute_stimulus_events(conn, DAR, "speed", as_of_sim_time=t0.isoformat())
        reflexes = physical_attribute_stimulus_events(conn, DAR, "reflexes", as_of_sim_time=t0.isoformat())
        endurance = physical_attribute_stimulus_events(conn, DAR, "endurance", as_of_sim_time=t0.isoformat())
        flexibility = physical_attribute_stimulus_events(conn, DAR, "flexibility", as_of_sim_time=t0.isoformat())

        assert [event.event_id for event in speed] == [ids["speed_agility_drills"]]
        assert [event.event_id for event in reflexes] == [ids["ai_combat_simulation"]]
        assert [event.event_id for event in endurance] == [ids["obstacle_conditioning"]]
        assert [event.event_id for event in flexibility] == [ids["mobility_stretching"]]
        assert ids["steady_state_cardio"] not in {event.event_id for event in endurance}


def test_flexibility_has_a_real_trainable_world_resource(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        row = conn.execute(
            "SELECT name,capabilities_json FROM entities WHERE id=?",
            ("obj_thorne_estate_gym_mobility_stretching",),
        ).fetchone()
        assert row is not None
        assert row["name"] == "Mobility & Stretching Area"
        assert "train" in json.loads(row["capabilities_json"])

    method = training_profile_for_target("obj_thorne_estate_gym_mobility_stretching")
    assert method is not None
    assert method["method_id"] == "mobility_stretching"
    assert method["workload_channels"] == ["movement"]


def test_first_bootstrap_consumes_history_without_retroactive_gain(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 2, tzinfo=timezone.utc)
    evidence_by_attribute = {
        "speed": "speed_agility_drills",
        "reflexes": "ai_combat_simulation",
        "endurance": "combat_pit_drills",
        "flexibility": "mobility_stretching",
    }
    with connect(db) as conn:
        before = {
            key: value(conn, DAR, physical_attribute_policy(key).field_key)
            for key in physical_attribute_keys()
        }
        for attribute_key, method_id in evidence_by_attribute.items():
            record_event(
                conn,
                sim_time=(t0 - timedelta(days=1)).isoformat(),
                actor_id=DAR,
                event_type="action_completed",
                payload=training_payload(method_id),
            )
        conn.commit()

        for attribute_key in physical_attribute_keys():
            result = settle_physical_attribute_progression(
                conn,
                DAR,
                attribute_key,
                as_of_sim_time=t0.isoformat(),
                state=healthy(),
            )
            assert result["status"] == "bootstrapped"
            assert result["net_delta"] == 0.0
            assert value(conn, DAR, physical_attribute_policy(attribute_key).field_key) == before[attribute_key]
