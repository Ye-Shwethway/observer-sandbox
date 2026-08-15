from __future__ import annotations

import pytest

import observer_sandbox.model_decision as model_decision
from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot


ACTOR = "char_darian"


def _legal_simple_decision(state):
    option = next(
        item
        for item in state["action_options"]
        if item.get("action") not in {"eat", "train"}
    )
    target = option.get("target") if isinstance(option.get("target"), str) else ""
    duration = 5
    preferred = option.get("preferred_duration")
    legal = option.get("duration")
    bounds = preferred if isinstance(preferred, (list, tuple)) and len(preferred) == 2 else legal
    if isinstance(bounds, (list, tuple)) and len(bounds) == 2:
        duration = int(bounds[0])
    return {
        "action": str(option["action"]),
        "duration_minutes": duration,
        "target": target,
        "reason": "legal corrective choice",
        "resources": [],
        "training_movements": [],
    }


def test_invalid_pair_gets_one_feedback_aware_corrective_retry(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    calls = []

    def fake_generate(conn, *, character_id, role, state, available_actions):
        calls.append(state)
        if len(calls) == 1:
            return {
                "action": "inspect",
                "duration_minutes": 5,
                "target": "obj_not_authoritative",
                "reason": "bad first proposal",
                "resources": [],
                "training_movements": [],
            }
        return _legal_simple_decision(state)

    monkeypatch.setattr(model_decision, "generate_character_decision", fake_generate)

    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        action = ModelDecisionProvider(conn, character_id=ACTOR).choose(state, [])

    assert len(calls) == 2
    correction = calls[1]["decision_correction"]
    assert correction["rejected_pair"] == {
        "action": "inspect",
        "target": "obj_not_authoritative",
    }
    allowed_pairs = {
        (item["action"], item["target"])
        for item in correction["allowed_pairs"]
    }
    assert (action.name, action.target) in allowed_pairs


def test_corrective_retry_is_bounded_and_still_fails_closed(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    calls = []

    def fake_generate(conn, *, character_id, role, state, available_actions):
        calls.append(state)
        return {
            "action": "inspect",
            "duration_minutes": 5,
            "target": f"obj_invalid_{len(calls)}",
            "reason": "still invalid",
            "resources": [],
            "training_movements": [],
        }

    monkeypatch.setattr(model_decision, "generate_character_decision", fake_generate)

    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        with pytest.raises(ValueError, match="after one corrective retry"):
            ModelDecisionProvider(conn, character_id=ACTOR).choose(state, [])

    assert len(calls) == 2
    assert "decision_correction" not in calls[0]
    assert calls[1]["decision_correction"]["rejected_pair"]["target"] == "obj_invalid_1"
