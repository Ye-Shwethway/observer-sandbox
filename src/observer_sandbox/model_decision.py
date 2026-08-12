from __future__ import annotations

import json
import sqlite3
from typing import Any

from .ai_runtime import generate_character_decision
from .simulation import Action


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
