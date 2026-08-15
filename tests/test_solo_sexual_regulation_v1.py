from __future__ import annotations

import json
from datetime import datetime, timedelta

import pytest

from observer_sandbox.ai_runtime import _decision_prompt
from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.observer_query import location_summary, observer_status, recent_history
from observer_sandbox.profile_observer import profile_section
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import (
    Action,
    action_options,
    apply_action,
    ensure_action_instance,
    set_runtime_value,
    snapshot,
    validate_action,
)
from observer_sandbox.solo_sexual_regulation import solo_sexual_regulation_context
from observer_sandbox.world import get_field


ACTOR = "char_darian"
MASTER_SUITE = "loc_thorne_estate_master_suite"
LIVING_ROOM = "loc_thorne_estate_living_room"


def _profile_value(conn, field_key):
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (ACTOR, field_key),
    ).fetchone()
    assert row is not None
    return json.loads(row[0])


def _set_profile_value(conn, field_key, value):
    conn.execute(
        "UPDATE character_profile_values SET value_json=? WHERE entity_id=? AND field_key=?",
        (json.dumps(value), ACTOR, field_key),
    )
    conn.commit()


def _private_ready(conn):
    set_dynamic_location(conn, ACTOR, MASTER_SUITE)
    conn.commit()
    state = snapshot(conn, ACTOR)
    context = solo_sexual_regulation_context(conn, ACTOR, state=state)
    assert context["adult"] is True
    assert context["private_environment"]["safe_private"] is True
    assert context["available_now"] is True
    return state, context


def test_private_environment_and_cognition_context_are_authoritative(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, LIVING_ROOM)
        conn.commit()
        open_state = snapshot(conn, ACTOR)
        open_context = solo_sexual_regulation_context(conn, ACTOR, state=open_state)
        assert open_context["private_environment"]["safe_private"] is False
        assert all(option["action"] != "self_satisfaction" for option in action_options(conn, ACTOR))

        state, context = _private_ready(conn)
        options = action_options(conn, ACTOR)
        solo = next(option for option in options if option["action"] == "self_satisfaction")
        assert solo["target"] is None
        assert solo["solo_regulation"]["private_safe"] is True

        provider = ModelDecisionProvider(conn, character_id=ACTOR)
        enriched = provider._enrich_state(state)
        assert enriched["solo_sexual_regulation"]["private_environment"]["safe_private"] is True
        assert enriched["solo_sexual_regulation"]["available_now"] is True
        assert any(option["action"] == "self_satisfaction" for option in enriched["action_options"])

        prompt = _decision_prompt(enriched, sorted({option["action"] for option in enriched["action_options"]}))
        assert "solo_sexual_regulation" in prompt
        assert "safe/private" in prompt
        assert "never a weekly quota" in prompt
        assert context["recent_7d_count"] == 0


def test_action_requires_adult_authorized_private_alone_context(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        action = Action("self_satisfaction", 15, None, "private self-regulation")

        set_dynamic_location(conn, ACTOR, LIVING_ROOM)
        conn.commit()
        with pytest.raises(ValueError, match="private"):
            validate_action(conn, ACTOR, action)

        _private_ready(conn)
        validate_action(conn, ACTOR, action)

        _set_profile_value(conn, "identity.date_of_birth", "2010-09-03")
        state = snapshot(conn, ACTOR)
        context = solo_sexual_regulation_context(conn, ACTOR, state=state)
        assert context["adult"] is False
        assert context["available_now"] is False
        assert all(option["action"] != "self_satisfaction" for option in action_options(conn, ACTOR))
        with pytest.raises(ValueError, match="non-adult"):
            validate_action(conn, ACTOR, action)


def test_action_start_and_completion_drive_runtime_physiology_and_rolling_count(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _private_ready(conn)
        structural_before = {
            "length": _profile_value(conn, "sexual_anatomy.penis_length_in"),
            "girth": _profile_value(conn, "sexual_anatomy.penis_girth_in"),
            "baseline": _profile_value(conn, "sexual_anatomy.baseline_erectile_function"),
            "cap": _profile_value(conn, "sexual_anatomy.erection_firmness_cap"),
        }
        action = Action("self_satisfaction", 15, None, "private self-regulation")
        validate_action(conn, ACTOR, action)
        action_id = ensure_action_instance(conn, action, ACTOR)

        start_arousal = float(get_field(conn, ACTOR, "sexual_state.arousal_level", 0.0))
        start_firmness = float(get_field(conn, ACTOR, "sexual_anatomy.erection_firmness", 0.0))
        start_state = str(get_field(conn, ACTOR, "sexual_anatomy.erectile_state", ""))
        assert start_arousal >= 60.0
        assert start_firmness > 0.0
        assert start_state in {"developing", "erect"}

        apply_action(conn, action, ACTOR, action_id=action_id)
        assert _profile_value(conn, "raps_sa.self_satisfaction_weekly") == 1
        assert get_field(conn, ACTOR, "sexual_anatomy.erectile_state", None) == "subsiding"
        assert float(get_field(conn, ACTOR, "sexual_state.arousal_level", -1)) == 5.0
        assert float(get_field(conn, ACTOR, "sexual_anatomy.erection_firmness", -1)) == 10.0

        post_context = solo_sexual_regulation_context(conn, ACTOR, state=snapshot(conn, ACTOR))
        assert post_context["recent_7d_count"] == 1
        assert post_context["cooldown_remaining_hours"] > 0
        assert post_context["available_now"] is False
        with pytest.raises(ValueError, match="cooldown"):
            validate_action(conn, ACTOR, action)

        structural_after = {
            "length": _profile_value(conn, "sexual_anatomy.penis_length_in"),
            "girth": _profile_value(conn, "sexual_anatomy.penis_girth_in"),
            "baseline": _profile_value(conn, "sexual_anatomy.baseline_erectile_function"),
            "cap": _profile_value(conn, "sexual_anatomy.erection_firmness_cap"),
        }
        assert structural_after == structural_before


def test_post_release_state_subsides_and_rolling_window_expires(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _private_ready(conn)
        apply_action(conn, Action("self_satisfaction", 15, None, "private self-regulation"), ACTOR)
        release_time = datetime.fromisoformat(snapshot(conn, ACTOR)["sim_time"])

        set_runtime_value(conn, "sim_time", (release_time + timedelta(hours=1)).isoformat())
        conn.commit()
        apply_action(conn, Action("idle", 10, None, "quiet time"), ACTOR)
        assert get_field(conn, ACTOR, "sexual_anatomy.erectile_state", None) == "flaccid"
        assert float(get_field(conn, ACTOR, "sexual_state.arousal_level", -1)) == 0.0
        assert float(get_field(conn, ACTOR, "sexual_anatomy.erection_firmness", -1)) == 0.0
        assert _profile_value(conn, "raps_sa.self_satisfaction_weekly") == 1

        set_runtime_value(conn, "sim_time", (release_time + timedelta(days=8)).isoformat())
        conn.commit()
        apply_action(conn, Action("idle", 10, None, "ordinary day"), ACTOR)
        assert _profile_value(conn, "raps_sa.self_satisfaction_weekly") == 0


def test_intimate_action_is_owner_only_across_observer_surfaces(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _private_ready(conn)
        action = Action("self_satisfaction", 15, None, "private self-regulation")
        apply_action(conn, action, ACTOR)

        owner_history = recent_history(conn, character_id=ACTOR, limit=12, role="owner")
        allowed_history = recent_history(conn, character_id=ACTOR, limit=12, role="allowed")
        assert any(row.get("action") == "self_satisfaction" for row in owner_history)
        assert all(row.get("action") != "self_satisfaction" for row in allowed_history)

        owner_room = location_summary(conn, MASTER_SUITE, role="owner")
        allowed_room = location_summary(conn, MASTER_SUITE, role="allowed")
        assert any(row.get("action") == "self_satisfaction" for row in owner_room["recent_activity"])
        assert all(row.get("action") != "self_satisfaction" for row in allowed_room["recent_activity"])

        # A fresh in-progress sensitive action is redacted from non-owner runtime status.
        now = datetime.fromisoformat(snapshot(conn, ACTOR)["sim_time"])
        set_runtime_value(conn, "sim_time", (now + timedelta(hours=7)).isoformat())
        conn.commit()
        pending = Action("self_satisfaction", 15, None, "private self-regulation")
        validate_action(conn, ACTOR, pending)
        action_id = ensure_action_instance(conn, pending, ACTOR)
        conn.execute("UPDATE actor_runtime SET pending_action_id=? WHERE actor_id=?", (action_id, ACTOR))
        conn.commit()
        owner_status = observer_status(conn, ACTOR, role="owner")
        allowed_status = observer_status(conn, ACTOR, role="allowed")
        assert owner_status["pending_action"]["action"] == "self_satisfaction"
        assert allowed_status["pending_action"]["action"] == "private_activity"
        assert allowed_status["pending_action"].get("reason") is None


def test_owner_profile_shows_drive_and_weekly_metric_but_allowed_user_cannot_open_section(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _private_ready(conn)
        apply_action(conn, Action("idle", 10, None, "ordinary pause"), ACTOR)
        sexual = profile_section(conn, ACTOR, "sexual", role="owner")
        by_key = {item["field_key"]: item for item in sexual["content"]}
        assert "sexual_state.solo_regulation_drive" in by_key
        assert "raps_sa.self_satisfaction_weekly" in by_key
        with pytest.raises(PermissionError):
            profile_section(conn, ACTOR, "sexual", role="allowed")
