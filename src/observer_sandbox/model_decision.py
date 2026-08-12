from __future__ import annotations

import json
import sqlite3
from typing import Any

from .ai_runtime import generate_character_decision
from .secrets import load_runtime_secrets
from .simulation import ACTION_NAMES, Action, snapshot, validate_action


class ModelDecisionProvider:
    """Model-backed P1 decision provider. Runtime validation remains authoritative."""

    def __init__(self, conn: sqlite3.Connection, *, character_id: str = "char_darian", role: str = "cognition") -> None:
        self.conn = conn
        self.character_id = character_id
        self.role = role

    def _enrich_state(self, state: dict[str, Any]) -> dict[str, Any]:
        enriched = dict(state)
        location = state["location"]
        reachable = self.conn.execute(
            """
            SELECT e.id, e.name
            FROM relations r JOIN entities e ON e.id=r.target_id
            WHERE r.source_id=? AND r.relation_type='connected_to'
            ORDER BY e.id
            """,
            (location,),
        ).fetchall()
        local_objects = self.conn.execute(
            """
            SELECT e.id, e.name, e.capabilities_json
            FROM relations r JOIN entities e ON e.id=r.target_id
            WHERE r.source_id=? AND r.relation_type='contains'
            ORDER BY e.id
            """,
            (location,),
        ).fetchall()
        enriched["reachable_rooms"] = [
            {"id": row["id"], "name": row["name"]} for row in reachable
        ]
        enriched["local_objects"] = [
            {
                "id": row["id"],
                "name": row["name"],
                "capabilities": json.loads(row["capabilities_json"]),
            }
            for row in local_objects
        ]
        return enriched

    def choose(self, snapshot: dict[str, Any], available_actions: list[str]) -> Action:
        decision = generate_character_decision(
            self.conn,
            character_id=self.character_id,
            role=self.role,
            state=self._enrich_state(snapshot),
            available_actions=available_actions,
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

    provider = ModelDecisionProvider(conn, character_id=character_id, role=role)
    action = provider.choose(before, ACTION_NAMES)
    validate_action(conn, character_id, action)

    after = snapshot(conn, character_id)
    event_count_after = int(conn.execute("SELECT COUNT(*) FROM events").fetchone()[0])
    unchanged = before == after and event_count_before == event_count_after
    if not unchanged:
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
