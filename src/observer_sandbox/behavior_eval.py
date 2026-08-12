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


def _move_to(*rooms: str) -> Callable[[Action], bool]:
    allowed = set(rooms)
    return lambda action: action.name == "move" and action.target in allowed


def _action_target(action_name: str, *targets: str) -> Callable[[Action], bool]:
    allowed = set(targets)
    return lambda action: action.name == action_name and action.target in allowed


def _either(*predicates: Callable[[Action], bool]) -> Callable[[Action], bool]:
    return lambda action: any(predicate(action) for predicate in predicates)


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
        accepts=_action_target("sleep", "obj_bed"),
        intent="sleep in the Bed when already in the Bedroom",
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
    passed = bool(scenario.accepts(action))
    return {
        "scenario": scenario.name,
        "intent": scenario.intent,
        "passed": passed,
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
