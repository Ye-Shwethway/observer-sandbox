from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

from .model_decision import ModelDecisionProvider
from .simulation import ACTION_NAMES, Action, set_runtime_value, snapshot, validate_action
from .world import set_field


@dataclass(frozen=True)
class BehaviorScenario:
    name: str
    hour: int
    energy: float
    hunger: float
    thirst: float
    sleepiness: float
    cleanliness: float
    location: str
    accepts: Callable[[Action], bool]
    intent: str
    reason_keywords: tuple[str, ...]


def _move_to(*rooms: str) -> Callable[[Action], bool]:
    allowed = set(rooms)
    return lambda action: action.name == "move" and action.target in allowed


def _action_target(action_name: str, *targets: str) -> Callable[[Action], bool]:
    allowed = set(targets)
    return lambda action: action.name == action_name and action.target in allowed


def _action_target_duration(
    action_name: str,
    targets: tuple[str, ...],
    min_minutes: int,
    max_minutes: int,
) -> Callable[[Action], bool]:
    allowed = set(targets)
    return lambda action: (
        action.name == action_name
        and action.target in allowed
        and min_minutes <= action.duration_minutes <= max_minutes
    )


def _either(*predicates: Callable[[Action], bool]) -> Callable[[Action], bool]:
    return lambda action: any(predicate(action) for predicate in predicates)


def _reason_matches(action: Action, keywords: tuple[str, ...]) -> bool:
    reason = (action.reason or "").lower()
    return any(keyword.lower() in reason for keyword in keywords)


SCENARIOS: tuple[BehaviorScenario, ...] = (
    BehaviorScenario(
        name="morning_ready",
        hour=8,
        energy=85,
        hunger=20,
        thirst=15,
        sleepiness=10,
        cleanliness=80,
        location="room_bedroom",
        accepts=_move_to("room_living"),
        intent="begin the morning training path toward the Home Gym",
        reason_keywords=("train", "gym", "physical"),
    ),
    BehaviorScenario(
        name="strong_thirst",
        hour=13,
        energy=70,
        hunger=30,
        thirst=70,
        sleepiness=20,
        cleanliness=75,
        location="room_bedroom",
        accepts=_either(
            _move_to("room_bathroom", "room_living"),
            _action_target("drink", "obj_sink", "obj_water", "obj_fridge"),
        ),
        intent="prioritize hydration or move toward an available drink source",
        reason_keywords=("thirst", "hydrat", "water", "drink"),
    ),
    BehaviorScenario(
        name="strong_hunger",
        hour=13,
        energy=65,
        hunger=72,
        thirst=25,
        sleepiness=20,
        cleanliness=75,
        location="room_bedroom",
        accepts=_move_to("room_bathroom", "room_living"),
        intent="move toward the Kitchen to address hunger",
        reason_keywords=("hunger", "food", "eat", "kitchen", "meal"),
    ),
    BehaviorScenario(
        name="high_sleep_pressure",
        hour=23,
        energy=24,
        hunger=35,
        thirst=30,
        sleepiness=88,
        cleanliness=65,
        location="room_bedroom",
        accepts=_action_target_duration("sleep", ("obj_bed",), 360, 540),
        intent="take a normal overnight sleep in the Bed when critically sleepy at night",
        reason_keywords=("sleep", "rest", "tired", "recover"),
    ),
    BehaviorScenario(
        name="poor_cleanliness",
        hour=18,
        energy=65,
        hunger=35,
        thirst=30,
        sleepiness=25,
        cleanliness=25,
        location="room_bedroom",
        accepts=_move_to("room_bathroom"),
        intent="move to the Bathroom to restore hygiene",
        reason_keywords=("clean", "hygiene", "shower", "bathroom"),
    ),
)


def prepare_scenario(conn, scenario: BehaviorScenario, actor_id: str = "char_darian") -> None:
    set_field(conn, actor_id, "runtime.location", scenario.location)
    set_field(conn, actor_id, "runtime.current_action", "idle")
    set_field(conn, actor_id, "needs.energy", scenario.energy)
    set_field(conn, actor_id, "needs.hunger", scenario.hunger)
    set_field(conn, actor_id, "needs.thirst", scenario.thirst)
    set_field(conn, actor_id, "needs.sleepiness", scenario.sleepiness)
    set_field(conn, actor_id, "physiology.cleanliness", scenario.cleanliness)
    set_runtime_value(
        conn,
        "sim_time",
        datetime(2025, 5, 1, scenario.hour, 0, tzinfo=timezone.utc).isoformat(),
    )
    conn.execute("DELETE FROM events WHERE actor_id=?", (actor_id,))
    conn.commit()


def evaluate_scenario(conn, scenario: BehaviorScenario, actor_id: str = "char_darian") -> dict[str, object]:
    prepare_scenario(conn, scenario, actor_id)
    state = snapshot(conn, actor_id)
    action = ModelDecisionProvider(conn, character_id=actor_id).choose(state, ACTION_NAMES)
    validate_action(conn, actor_id, action)
    action_passed = bool(scenario.accepts(action))
    reason_passed = _reason_matches(action, scenario.reason_keywords)
    return {
        "scenario": scenario.name,
        "intent": scenario.intent,
        "passed": action_passed and reason_passed,
        "action_passed": action_passed,
        "reason_passed": reason_passed,
        "proposal": {
            "action": action.name,
            "target": action.target,
            "duration_minutes": action.duration_minutes,
            "reason": action.reason,
        },
    }


def run_behavior_matrix(conn, actor_id: str = "char_darian") -> dict[str, object]:
    results = [evaluate_scenario(conn, scenario, actor_id) for scenario in SCENARIOS]
    passed = sum(1 for result in results if result["passed"])
    return {
        "ok": passed == len(results),
        "passed": passed,
        "total": len(results),
        "results": results,
    }
