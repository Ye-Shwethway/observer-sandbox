from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from .ai_runtime import generate_character_decision
from .need_resolution import shape_action_options_for_needs
from .secrets import load_runtime_secrets
from .simulation import ACTION_NAMES, Action, action_options, snapshot, validate_action


REPO_ROOT = Path(__file__).resolve().parents[2]
DARIAN_AUTONOMY_POLICY_PATH = REPO_ROOT / "config" / "characters" / "darian.autonomy-policy.json"


def load_autonomy_policy(path: str | Path = DARIAN_AUTONOMY_POLICY_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


class ModelDecisionProvider:
    """Model-backed P1 decision provider. Runtime validation remains authoritative."""

    def __init__(
        self,
        conn: sqlite3.Connection,
        *,
        character_id: str = "char_darian",
        role: str = "cognition",
        policy: dict[str, Any] | None = None,
    ) -> None:
        self.conn = conn
        self.character_id = character_id
        self.role = role
        self.policy = policy if policy is not None else load_autonomy_policy()

    def _profile_value(self, field_key: str, default: Any = None) -> Any:
        row = self.conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
            (self.character_id, field_key),
        ).fetchone()
        return default if row is None else json.loads(row[0])

    def _recent_events(self, limit: int | None = None) -> list[dict[str, Any]]:
        if limit is None:
            limit = int(self.policy.get("repetition_policy", {}).get("recent_event_window", 8))
        rows = self.conn.execute(
            "SELECT sim_time, event_type, payload_json FROM events WHERE actor_id=? ORDER BY id DESC LIMIT ?",
            (self.character_id, limit),
        ).fetchall()
        result: list[dict[str, Any]] = []
        for row in reversed(rows):
            payload = json.loads(row["payload_json"])
            result.append(
                {
                    "sim_time": row["sim_time"],
                    "event_type": row["event_type"],
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
            "name": self._profile_value("identity.full_name", "Darian Thorne"),
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
        options = action_options(self.conn, self.character_id)
        enriched["action_options"] = shape_action_options_for_needs(
            self.conn,
            state=state,
            action_options=options,
            decision_signals=decision_signals,
        )
        enriched["character"] = self._character_context()
        enriched["autonomy_policy"] = self.policy
        enriched["decision_signals"] = decision_signals
        enriched["recent_events"] = self._recent_events()
        return enriched

    def choose(self, state: dict[str, Any], available_actions: list[str]) -> Action:
        enriched = self._enrich_state(state)
        option_actions = {str(option["action"]) for option in enriched["action_options"]}
        known_actions = sorted(set(available_actions) | option_actions)
        decision = generate_character_decision(
            self.conn,
            character_id=self.character_id,
            role=self.role,
            state=enriched,
            available_actions=known_actions,
        )
        return Action(
            decision["action"],
            decision["duration_minutes"],
            decision["target"] or None,
            decision["reason"],
        )


def dry_run_model_decision(
    conn: sqlite3.Connection,
    *,
    character_id: str = "char_darian",
    role: str = "cognition",
) -> dict[str, Any]:
    """Ask the bound model for one action and validate it without mutating world state."""
    load_runtime_secrets()
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
        },
        "state_before": before,
        "state_after": after,
        "event_count_before": event_count_before,
        "event_count_after": event_count_after,
    }
