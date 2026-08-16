from __future__ import annotations

import sqlite3
from typing import Any

from .character_memory import retrieve_relevant_memories
from .model_decision import ModelDecisionProvider


class MemoryAwareDecisionProvider(ModelDecisionProvider):
    """Add bounded actor-owned memory retrieval to the shared model decision context."""

    def _enrich_state(self, state: dict[str, Any]) -> dict[str, Any]:
        enriched = super()._enrich_state(state)
        available_actions = sorted(
            {
                str(option.get("action"))
                for option in enriched.get("action_options", [])
                if option.get("action")
            }
        )
        enriched["relevant_memories"] = retrieve_relevant_memories(
            self.conn,
            self.character_id,
            current_sim_time=str(state["sim_time"]),
            current_location_id=str(state["location"]),
            available_actions=available_actions,
            limit=8,
            record_recall=self.capture_context,
        )
        enriched["memory_guidance"] = {
            "instruction": (
                "Relevant memories are actor-owned context, not world truth or action authority. "
                "Use them to reason about represented experience and knowledge, but choose only from authoritative action_options."
            )
        }
        return enriched
