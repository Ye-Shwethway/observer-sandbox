from __future__ import annotations

import json
from datetime import datetime, timedelta

from observer_sandbox.actor_runtime import actor_runtime, pending_action
from observer_sandbox.autonomy import autonomy_tick, set_autonomy_enabled, set_autonomy_speed
from observer_sandbox.composition_schema import ensure_actor_runtime
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, ensure_sim_clock, set_runtime_value
from observer_sandbox.world import set_field


class FixedProvider:
    def __init__(self, action: Action): self.action = action
    def choose(self, state, available_actions): return self.action


def _add_quasi_stub(conn):
    conn.execute("INSERT OR IGNORE INTO entities(id,entity_type,name,capabilities_json) VALUES('char_quasi','character','Quasi Winterfield','[]')")
    set_field(conn, "char_quasi", "runtime.location", "loc_thorne_estate_master_suite")
    set_field(conn, "char_quasi", "runtime.current_action", "idle")
    ensure_actor_runtime(conn, "char_quasi")
    conn.commit()


def test_two_actors_can_hold_independent_pending_actions(tmp_path):
    db = tmp_path / "observer.sqlite3"; initialize(db)
    with connect(db) as conn:
        _add_quasi_stub(conn)
        set_autonomy_speed(conn, 60.0)
        set_autonomy_enabled(conn, True, actor_id="char_darian")
        set_autonomy_enabled(conn, True, actor_id="char_quasi")
        darian = autonomy_tick(conn, actor_id="char_darian", provider=FixedProvider(Action("rest", 60, None, "recover")), now_wall=1000)
        quasi = autonomy_tick(conn, actor_id="char_quasi", provider=FixedProvider(Action("rest", 60, None, "recover")), now_wall=1000)
        assert darian["state"] == quasi["state"] == "planned"
        assert darian["pending"]["action_id"] != quasi["pending"]["action_id"]
        assert pending_action(conn, "char_darian") is not None
        assert pending_action(conn, "char_quasi") is not None
        assert actor_runtime(conn, "char_darian")["lease"] is None
        assert actor_runtime(conn, "char_quasi")["lease"] is None


def test_concurrent_action_completion_does_not_double_advance_universe_clock(tmp_path):
    db = tmp_path / "observer.sqlite3"; initialize(db)
    with connect(db) as conn:
        _add_quasi_stub(conn)
        start = ensure_sim_clock(conn)
        set_autonomy_speed(conn, 60.0)
        set_autonomy_enabled(conn, True, actor_id="char_darian")
        set_autonomy_enabled(conn, True, actor_id="char_quasi")
        autonomy_tick(conn, actor_id="char_darian", provider=FixedProvider(Action("rest", 60, None)), now_wall=1000)
        autonomy_tick(conn, actor_id="char_quasi", provider=FixedProvider(Action("rest", 60, None)), now_wall=1000)
        assert autonomy_tick(conn, actor_id="char_darian", provider=FixedProvider(Action("rest", 60, None)), now_wall=1060)["state"] == "completed"
        assert autonomy_tick(conn, actor_id="char_quasi", provider=FixedProvider(Action("rest", 60, None)), now_wall=1060)["state"] == "completed"
        assert ensure_sim_clock(conn) == start + timedelta(hours=1)


def test_action_participants_and_event_links_are_queryable(tmp_path):
    db = tmp_path / "observer.sqlite3"; initialize(db)
    with connect(db) as conn:
        _add_quasi_stub(conn)
        action = Action("rest", 30, None, "shared quiet recovery", participants=("char_quasi",), conditions={"privacy": "quiet"}, modifiers={"mood": "calm"})
        apply_action(conn, action, "char_darian")
        action_row = conn.execute("SELECT id,place_id,participants_json,conditions_json,modifiers_json,status FROM action_instances ORDER BY created_at DESC,id DESC LIMIT 1").fetchone()
        assert action_row["status"] == "completed"
        assert "char_quasi" in json.loads(action_row["participants_json"])
        assert json.loads(action_row["conditions_json"])["privacy"] == "quiet"
        event = conn.execute("SELECT id,action_id,location_id,state_changes_json FROM events WHERE event_type='action_completed' ORDER BY id DESC LIMIT 1").fetchone()
        assert event["action_id"] == action_row["id"] and event["location_id"] == "loc_thorne_estate_master_suite"
        participant_ids = {r[0] for r in conn.execute("SELECT entity_id FROM event_participants WHERE event_id=?", (event["id"],)).fetchall()}
        assert {"char_darian", "char_quasi"} <= participant_ids


def test_definition_instance_and_modifier_sockets_exist(tmp_path):
    db = tmp_path / "observer.sqlite3"; initialize(db)
    with connect(db) as conn:
        conn.execute("INSERT INTO entity_definitions(id,entity_type,name,capabilities_json,effects_json) VALUES('item_def_energy_drink','item','Energy Drink','[\"drink\"]',?)", (json.dumps({"drink": {"needs.energy": {"add": 10}, "needs.sleepiness": {"add": -8}}}),))
        conn.execute("INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id) VALUES('item_test_energy_drink_01','object','Energy Drink','[\"drink\"]','item_def_energy_drink')")
        conn.execute("INSERT INTO active_modifiers(id,subject_id,source_entity_id,field_key,operation,value_json,starts_sim_time,ends_sim_time,stack_key,stack_policy) VALUES('mod_test_stimulant','char_darian','item_test_energy_drink_01','needs.sleepiness','multiply','0.8','2025-05-01T10:00:00+00:00','2025-05-01T12:00:00+00:00','stimulant','replace')")
        conn.commit()
        assert conn.execute("SELECT definition_id FROM entities WHERE id='item_test_energy_drink_01'").fetchone()[0] == "item_def_energy_drink"
        modifier = conn.execute("SELECT operation,stack_policy FROM active_modifiers WHERE id='mod_test_stimulant'").fetchone()
        assert modifier["operation"] == "multiply" and modifier["stack_policy"] == "replace"
        assert conn.execute("SELECT target_mode FROM action_definitions WHERE action_type='drink'").fetchone()[0] == "object"
