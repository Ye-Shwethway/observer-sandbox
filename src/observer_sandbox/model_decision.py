from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from typing import Any

from .actor_selection import resolve_actor_id
from .ai_runtime import generate_character_decision
from .character_config import configured_character_ids, load_character_autonomy_policy
from .eating_behavior import enrich_eating_action_options, validate_proposed_resources
from .meal_choice_intelligence import meal_choice_context
from .need_resolution import shape_action_options_for_needs
from .resource_awareness import (
    enrich_options_with_usage,
    reachable_location_awareness,
    recent_action_usage,
    shape_inspect_options_for_familiarity,
)
from .secrets import load_runtime_secrets
from .simulation import ACTION_NAMES, Action, action_options, snapshot, validate_action
from .training_load_guard import projected_training_allowed, shape_training_options_for_load
from .training_methods import enrich_training_action_options
from .training_modifiers import training_readiness_modifier


def load_autonomy_policy(character_id: str | None = None) -> dict[str, Any]:
    """Load the selected character's authored policy from the character registry.

    The no-argument form remains convenient while exactly one character config is
    registered. Once multiple configured characters exist, callers must select one.
    """
    if character_id is None:
        configured = configured_character_ids()
        if len(configured) != 1:
            raise ValueError("character_id is required when multiple character configs are registered")
        character_id = configured[0]
    return load_character_autonomy_policy(character_id)


def _shape_discretionary_repetition(
    action_options: list[dict[str, Any]],
    recent_events: list[dict[str, Any]],
    *,
    current_location: str,
) -> list[dict[str, Any]]:
    """Suppress low-value inspect/use loops without hiding all fallback behavior."""
    action_events = [event for event in recent_events if event.get("action")]
    if not action_events:
        return action_options

    discretionary = {"inspect", "use"}
    blocked_pairs: set[tuple[str, str | None]] = set()
    last = action_events[-1]
    if last.get("action") in discretionary:
        blocked_pairs.add((str(last["action"]), last.get("target")))

    tail = action_events[-2:]
    suppress_room_discretionary = len(tail) == 2 and all(
        event.get("action") in discretionary and event.get("location_id") == current_location
        for event in tail
    )

    filtered: list[dict[str, Any]] = []
    for option in action_options:
        action = str(option.get("action"))
        target = option.get("target")
        if suppress_room_discretionary and action in discretionary:
            continue
        if (action, target) in blocked_pairs:
            continue
        filtered.append(option)
    return filtered or action_options


class ModelDecisionProvider:
    """Model-backed decision provider for any registered character.

    Character-specific facts and routine guidance come from config/profile data;
    runtime cognition and validation remain identity-agnostic.
    """

    def __init__(
        self,
        conn: sqlite3.Connection,
        *,
        character_id: str | None = None,
        role: str = "cognition",
        policy: dict[str, Any] | None = None,
    ) -> None:
        self.conn = conn
        self.character_id = resolve_actor_id(conn, character_id)
        self.role = role
        self.policy = policy if policy is not None else load_autonomy_policy(self.character_id)

    def _profile_value(self, field_key: str, default: Any = None) -> Any:
        row = self.conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
            (self.character_id, field_key),
        ).fetchone()
        return default if row is None else json.loads(row[0])

    def _entity_name(self) -> str:
        row = self.conn.execute(
            "SELECT name FROM entities WHERE id=? AND entity_type='character'",
            (self.character_id,),
        ).fetchone()
        return str(row[0]) if row is not None and row[0] else self.character_id

    def _recent_events(self, limit: int | None = None) -> list[dict[str, Any]]:
        if limit is None:
            limit = int(self.policy.get("repetition_policy", {}).get("recent_event_window", 8))
        rows = self.conn.execute(
            "SELECT sim_time, event_type, location_id, payload_json FROM events WHERE actor_id=? ORDER BY id DESC LIMIT ?",
            (self.character_id, limit),
        ).fetchall()
        result: list[dict[str, Any]] = []
        for row in reversed(rows):
            payload = json.loads(row["payload_json"])
            result.append(
                {
                    "sim_time": row["sim_time"],
                    "event_type": row["event_type"],
                    "location_id": row["location_id"],
                    "action": payload.get("action"),
                    "target": payload.get("target"),
                    "reason": payload.get("reason"),
                }
            )
        return result

    def _character_context(self) -> dict[str, Any]:
        preferences = self.conn.execute(
            "SELECT preference_type, subject FROM character_preferences WHERE entity_id=? ORDER BY preference_type, id",
            (self.character_id,),
        ).fetchall()
        hobbies = self.conn.execute(
            "SELECT name FROM character_hobbies WHERE entity_id=? ORDER BY id",
            (self.character_id,),
        ).fetchall()
        habits = self.conn.execute(
            "SELECT name FROM character_habits WHERE entity_id=? ORDER BY id",
            (self.character_id,),
        ).fetchall()
        skills = self.conn.execute(
            "SELECT skill_key, category, score FROM character_skills WHERE entity_id=? ORDER BY skill_key",
            (self.character_id,),
        ).fetchall()
        return {
            "name": self._profile_value("identity.full_name", self._entity_name()),
            "traits": self._profile_value("personality.primary_traits", []),
            "primary_motivation": self._profile_value("personality.primary_motivation", ""),
            "complexity_notes": self._profile_value("personality.complexity_notes", ""),
            "preferences": [
                {"type": row["preference_type"], "subject": row["subject"]}
                for row in preferences
            ],
            "hobbies": [row["name"] for row in hobbies],
            "habits": [row["name"] for row in habits],
            "skills": [
                {"key": row["skill_key"], "category": row["category"], "score": row["score"]}
                for row in skills
            ],
        }

    def _decision_signals(self, state: dict[str, Any]) -> dict[str, Any]:
        priorities = self.policy.get("need_priorities", {})
        strong = priorities.get("strong", {})
        critical = priorities.get("critical", {})

        checks = {
            "sleepiness": ("gte", float(state["sleepiness"])),
            "energy": ("lte", float(state["energy"])),
            "fatigue": ("gte", float(state["fatigue"])),
            "thirst": ("gte", float(state["thirst"])),
            "hunger": ("gte", float(state["hunger"])),
            "cleanliness": ("lte", float(state["cleanliness"])),
        }

        needs_attention: list[dict[str, Any]] = []
        for need, (direction, value) in checks.items():
            key = f"{need}_{direction}"
            level = None
            threshold = None
            if key in critical:
                candidate = float(critical[key])
                if (direction == "gte" and value >= candidate) or (direction == "lte" and value <= candidate):
                    level = "critical"
                    threshold = candidate
            if level is None and key in strong:
                candidate = float(strong[key])
                if (direction == "gte" and value >= candidate) or (direction == "lte" and value <= candidate):
                    level = "strong"
                    threshold = candidate
            if level:
                needs_attention.append(
                    {"need": need, "level": level, "value": value, "threshold": threshold}
                )

        needs_attention.sort(key=lambda item: 0 if item["level"] == "critical" else 1)

        hour = datetime.fromisoformat(state["sim_time"]).hour
        active_routine = None
        for window in self.policy.get("routine_windows", []):
            start = int(window["start_hour"])
            end = int(window["end_hour"])
            active = start <= hour < end if start < end else hour >= start or hour < end
            if active:
                active_routine = {
                    "name": window["name"],
                    "guidance": window["guidance"],
                }
                break

        recommended_duration = None
        highest = needs_attention[0] if needs_attention else None
        if (
            highest
            and highest["need"] == "sleepiness"
            and highest["level"] == "critical"
            and active_routine
            and active_routine["name"] == "night_sleep"
        ):
            guidance = self.policy.get("duration_guidance", {}).get("critical_night_sleep")
            if guidance:
                recommended_duration = {
                    "action": guidance["action"],
                    "min_minutes": guidance["min_minutes"],
                    "max_minutes": guidance["max_minutes"],
                    "guidance": guidance["guidance"],
                }

        return {
            "needs_attention": needs_attention,
            "highest_priority": highest,
            "active_routine": active_routine,
            "recommended_duration": recommended_duration,
            "instruction": (
                "Address highest_priority before discretionary routine behavior, make the reason explicitly reflect it, and follow recommended_duration when present."
                if needs_attention
                else "No strong physiological need is active; routine and character preferences may guide the next action."
            ),
        }

    def _enrich_state(self, state: dict[str, Any]) -> dict[str, Any]:
        enriched = dict(state)
        decision_signals = self._decision_signals(state)
        recent_events = self._recent_events()
        options = enrich_training_action_options(action_options(self.conn, self.character_id))
        options = enrich_eating_action_options(self.conn, str(state["location"]), options)
        options, training_load_guard = shape_training_options_for_load(
            self.conn,
            self.character_id,
            state=state,
            action_options=options,
        )
        options = shape_action_options_for_needs(
            self.conn,
            state=state,
            action_options=options,
            decision_signals=decision_signals,
        )
        options, familiarity = shape_inspect_options_for_familiarity(
            self.conn,
            self.character_id,
            room_id=str(state["location"]),
            action_options=options,
        )
        options = _shape_discretionary_repetition(
            options,
            recent_events,
            current_location=str(state["location"]),
        )
        options = enrich_options_with_usage(
            options,
            recent_action_usage(self.conn, self.character_id),
        )
        enriched["action_options"] = options
        enriched["training_load_guard"] = {
            **training_load_guard,
            "guidance": (
                "Recent training dose is already substantial; choose recovery or ordinary non-training activity before another workout."
                if not training_load_guard["allowed"]
                else "Training remains available only within the remaining effective-load budget shown on train options."
            ),
        }
        enriched["object_familiarity"] = familiarity
        enriched["resource_awareness"] = {
            "current_location": {
                "id": state["location"],
                "name": state["location_name"],
                "instruction": "Current-room action_options are directly actionable and authoritative.",
            },
            "reachable_locations": reachable_location_awareness(self.conn, str(state["location"])),
            "guidance": (
                "Use reachable-location previews to plan purposeful movement. Distant resources are visible for planning only; move to the destination before using them. "
                "When several suitable options exist, recent_usage is context for reasonable variety, not a hard prohibition on repetition."
            ),
        }
        enriched["character"] = self._character_context()
        enriched["autonomy_policy"] = self.policy
        enriched["decision_signals"] = decision_signals
        enriched["meal_choice_context"] = meal_choice_context(
            self.conn,
            self.character_id,
            state=state,
            autonomy_policy=self.policy,
        )
        enriched["recent_events"] = recent_events
        return enriched

    def choose(self, state: dict[str, Any], available_actions: list[str]) -> Action:
        enriched = self._enrich_state(state)
        option_actions = {str(option["action"]) for option in enriched["action_options"]}
        known_actions = sorted(option_actions) if option_actions else sorted(set(available_actions))
        decision = generate_character_decision(
            self.conn,
            character_id=self.character_id,
            role=self.role,
            state=enriched,
            available_actions=known_actions,
        )
        selected_target = decision["target"] or None
        allowed_pairs = {
            (str(option.get("action")), option.get("target") if isinstance(option.get("target"), str) else None)
            for option in enriched["action_options"]
        }
        if (decision["action"], selected_target) not in allowed_pairs:
            raise ValueError("Model selected an action/target pair outside authoritative action_options")
        resources = validate_proposed_resources(
            self.conn,
            action_name=str(decision["action"]),
            location_id=str(state["location"]),
            resources=decision.get("resources"),
        )
        if decision["action"] == "train":
            readiness = training_readiness_modifier(state)
            if not projected_training_allowed(
                enriched["training_load_guard"],
                duration_minutes=decision["duration_minutes"],
                effectiveness=float(readiness["effectiveness"]),
            ):
                raise ValueError("Training duration exceeds the remaining recent-load budget")
        return Action(
            decision["action"],
            decision["duration_minutes"],
            selected_target,
            decision["reason"],
            resources=resources,
        )


def dry_run_model_decision(
    conn: sqlite3.Connection,
    *,
    character_id: str | None = None,
    role: str = "cognition",
) -> dict[str, Any]:
    """Ask the bound model for one action and validate it without mutating world state."""
    load_runtime_secrets()
    character_id = resolve_actor_id(conn, character_id)
    before = snapshot(conn, character_id)
    event_count_before = int(conn.execute("SELECT COUNT(*) FROM events").fetchone()[0])
    action = ModelDecisionProvider(conn, character_id=character_id, role=role).choose(before, ACTION_NAMES)
    validate_action(conn, character_id, action)
    after = snapshot(conn, character_id)
    event_count_after = int(conn.execute("SELECT COUNT(*) FROM events").fetchone()[0])
    if before != after or event_count_before != event_count_after:
        raise RuntimeError("Dry-run invariant failed: model proposal mutated live state")
    return {
        "ok": True,
        "validated": True,
        "mutated": False,
        "actor_id": character_id,
        "proposal": {
            "action": action.name,
            "duration_minutes": action.duration_minutes,
            "target": action.target,
            "reason": action.reason,
            "resources": list(action.resources),
        },
        "state_before": before,
        "state_after": after,
        "event_count_before": event_count_before,
        "event_count_after": event_count_after,
    }
