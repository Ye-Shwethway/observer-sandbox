from __future__ import annotations

from observer_sandbox.autonomy import set_autonomy_enabled
from observer_sandbox.autonomy_intent import (
    CONDITION_KEY,
    MAX_INTENT_AGE_HOURS,
    MAX_MOVEMENT_STEPS,
    active_intent,
    autonomy_tick,
    commit_planned_transition,
    expire_stale_intent,
    intent_context,
    settle_completed_transition,
    transition_for_action,
)
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, snapshot


ACTOR = "char_darian"


class FixedProvider:
    def __init__(self, action: Action) -> None:
        self.action = action
        self.seen_states: list[dict] = []

    def choose(self, state, _available_actions):
        self.seen_states.append(state)
        return self.action


def _first_move(conn) -> dict:
    return next(option for option in action_options(conn, ACTOR) if option["action"] == "move")


def test_only_purposeful_move_starts_intent(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        move = _first_move(conn)
        none = transition_for_action(
            None,
            Action("idle", 5, reason="wait briefly"),
            actor_id=ACTOR,
            sim_time=state["sim_time"],
            origin_location_id=state["location"],
        )
        assert none["mode"] == "none"

        start = transition_for_action(
            None,
            Action("move", 5, move["target"], "go there to use the available facility"),
            actor_id=ACTOR,
            sim_time=state["sim_time"],
            origin_location_id=state["location"],
        )
        assert start["mode"] == "start"
        assert start["destination_location_id"] == move["target"]
        assert active_intent(conn, ACTOR) is None


def test_intent_persists_as_separate_runtime_overlay_and_survives_initialize(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        move = _first_move(conn)
        transition = transition_for_action(
            None,
            Action("move", 5, move["target"], "go there to inspect the selected resource"),
            actor_id=ACTOR,
            sim_time=state["sim_time"],
            origin_location_id=state["location"],
        )
        commit_planned_transition(conn, ACTOR, transition)
        current = active_intent(conn, ACTOR)
        assert current is not None
        assert current["summary"] == "go there to inspect the selected resource"

    initialize(db)
    with connect(db) as conn:
        current = active_intent(conn, ACTOR)
        assert current is not None
        assert current["intent_id"] == transition["intent_id"]


def test_context_is_guidance_not_action_authority(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        assert intent_context(conn, ACTOR, as_of_sim_time=state["sim_time"])["active"] is False
        move = _first_move(conn)
        transition = transition_for_action(
            None,
            Action("move", 5, move["target"], "go there for a specific follow-up task"),
            actor_id=ACTOR,
            sim_time=state["sim_time"],
            origin_location_id=state["location"],
        )
        commit_planned_transition(conn, ACTOR, transition)
        context = intent_context(conn, ACTOR, as_of_sim_time=state["sim_time"])
        assert context["active"] is True
        assert context["summary"] == "go there for a specific follow-up task"
        assert "not an order" in context["guidance"]
        assert "override" in context["guidance"]


def test_movement_continuation_is_bounded_and_self_clears(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        move = _first_move(conn)
        transition = transition_for_action(
            None,
            Action("move", 5, move["target"], "travel there for a bounded purpose"),
            actor_id=ACTOR,
            sim_time=state["sim_time"],
            origin_location_id=state["location"],
        )
        commit_planned_transition(conn, ACTOR, transition)
        current = active_intent(conn, ACTOR)
        assert current is not None

        for _ in range(MAX_MOVEMENT_STEPS - 1):
            continuation = transition_for_action(
                current,
                Action("move", 5, move["target"], "continue toward the purpose"),
                actor_id=ACTOR,
                sim_time=state["sim_time"],
                origin_location_id=state["location"],
            )
            assert continuation["mode"] == "continue"
            commit_planned_transition(conn, ACTOR, continuation)
            current = active_intent(conn, ACTOR)
            assert current is not None

        bounded = transition_for_action(
            current,
            Action("move", 5, move["target"], "keep moving"),
            actor_id=ACTOR,
            sim_time=state["sim_time"],
            origin_location_id=state["location"],
        )
        assert bounded["mode"] == "abandon"
        commit_planned_transition(conn, ACTOR, bounded)
        assert active_intent(conn, ACTOR) is None


def test_self_care_interrupts_do_not_force_goal_abandonment(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        move = _first_move(conn)
        start = transition_for_action(
            None,
            Action("move", 5, move["target"], "travel there for a follow-up task"),
            actor_id=ACTOR,
            sim_time=state["sim_time"],
            origin_location_id=state["location"],
        )
        commit_planned_transition(conn, ACTOR, start)
        current = active_intent(conn, ACTOR)
        interrupt = transition_for_action(
            current,
            Action("drink", 5, reason="address thirst first"),
            actor_id=ACTOR,
            sim_time=state["sim_time"],
            origin_location_id=state["location"],
        )
        assert interrupt["mode"] == "interrupt"
        commit_planned_transition(conn, ACTOR, interrupt)
        current = active_intent(conn, ACTOR)
        assert current is not None
        assert current["interruptions"] == 1


def test_local_follow_up_clears_only_after_completion(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        move = _first_move(conn)
        start = transition_for_action(
            None,
            Action("move", 5, move["target"], "travel there for a local follow-up"),
            actor_id=ACTOR,
            sim_time=state["sim_time"],
            origin_location_id=state["location"],
        )
        commit_planned_transition(conn, ACTOR, start)
        current = active_intent(conn, ACTOR)
        finish = transition_for_action(
            current,
            Action("idle", 1, reason="finish the local purpose"),
            actor_id=ACTOR,
            sim_time=state["sim_time"],
            origin_location_id=state["location"],
        )
        assert finish["mode"] == "finish_after_completion"
        assert active_intent(conn, ACTOR) is not None
        settle_completed_transition(conn, ACTOR, finish)
        assert active_intent(conn, ACTOR) is None


def test_stale_intent_expires_at_decision_boundary(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        move = _first_move(conn)
        start = transition_for_action(
            None,
            Action("move", 5, move["target"], "travel there for a time-bounded task"),
            actor_id=ACTOR,
            sim_time=state["sim_time"],
            origin_location_id=state["location"],
        )
        commit_planned_transition(conn, ACTOR, start)
        later = _parse_later(state["sim_time"], MAX_INTENT_AGE_HOURS + 0.1)
        assert active_intent(conn, ACTOR, as_of_sim_time=later) is None
        assert expire_stale_intent(conn, ACTOR, as_of_sim_time=later) is True
        assert active_intent(conn, ACTOR) is None


def _parse_later(sim_time: str, hours: float) -> str:
    from datetime import timedelta

    from datetime import datetime

    return (datetime.fromisoformat(sim_time) + timedelta(hours=hours)).isoformat()


def test_wrapper_carries_move_purpose_into_next_cognition_then_finishes(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_autonomy_enabled(conn, True, actor_id=ACTOR)
        state = snapshot(conn, ACTOR)
        move = _first_move(conn)
        move_provider = FixedProvider(
            Action("move", 5, move["target"], "go there to complete a specific local task")
        )

        planned = autonomy_tick(conn, actor_id=ACTOR, provider=move_provider, now_wall=1000.0)
        assert planned["state"] == "planned"
        pending = planned["pending"]
        assert pending["conditions"][CONDITION_KEY]["mode"] == "start"
        assert active_intent(conn, ACTOR) is not None

        completed = autonomy_tick(
            conn,
            actor_id=ACTOR,
            provider=move_provider,
            now_wall=float(pending["due_wall_time"]) + 0.01,
        )
        assert completed["state"] == "completed"
        assert active_intent(conn, ACTOR) is not None

        follow_provider = FixedProvider(Action("idle", 1, reason="complete the local task"))
        follow = autonomy_tick(
            conn,
            actor_id=ACTOR,
            provider=follow_provider,
            now_wall=float(pending["due_wall_time"]) + 0.02,
        )
        assert follow["state"] == "planned"
        assert follow_provider.seen_states[0]["autonomy_intent"]["active"] is True
        assert follow["pending"]["conditions"][CONDITION_KEY]["mode"] == "finish_after_completion"
        assert active_intent(conn, ACTOR) is not None

        finished = autonomy_tick(
            conn,
            actor_id=ACTOR,
            provider=follow_provider,
            now_wall=float(follow["pending"]["due_wall_time"]) + 0.01,
        )
        assert finished["state"] == "completed"
        assert active_intent(conn, ACTOR) is None


def test_non_move_action_does_not_create_sticky_intent(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_autonomy_enabled(conn, True, actor_id=ACTOR)
        provider = FixedProvider(Action("idle", 1, reason="briefly wait here"))
        planned = autonomy_tick(conn, actor_id=ACTOR, provider=provider, now_wall=2000.0)
        assert planned["state"] == "planned"
        assert planned["pending"]["conditions"][CONDITION_KEY]["mode"] == "none"
        assert active_intent(conn, ACTOR) is None
