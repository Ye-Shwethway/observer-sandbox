from __future__ import annotations

import json
import sqlite3
from typing import Any

from .event_log import record_event
from .physical_attribute_progression import (
    physical_attribute_keys,
    physical_attribute_policy,
    physical_attribute_stimulus_events,
)
from .skill_progression import (
    SETTLEMENT_EVENT_TYPE as SKILL_SETTLEMENT_EVENT_TYPE,
    _eligible_training_events,
    load_skill_progression_config,
)

SOURCE = "creator-profile-control-v1"


def _physical_policy_by_field() -> dict[str, tuple[str, Any]]:
    result: dict[str, tuple[str, Any]] = {}
    for attribute_key in physical_attribute_keys():
        policy = physical_attribute_policy(attribute_key)
        result[policy.field_key] = (attribute_key, policy)
    return result


def reanchor_creator_progression(
    conn: sqlite3.Connection,
    character_id: str,
    changes: list[dict[str, Any]],
    *,
    sim_time: str,
) -> dict[str, Any]:
    """Consume pre-edit progression evidence without fabricating organic change.

    Existing immutable action/training evidence is retained. Zero-delta settlement
    markers establish the Creator edit as the new field/skill progression cursor,
    so only evidence after this simulation boundary can move the corrected value.
    """
    physical_by_field = _physical_policy_by_field()
    skill_config = load_skill_progression_config()
    configured_skills = skill_config.get("skills") or {}
    physical_reanchors: list[dict[str, Any]] = []
    skill_reanchors: list[dict[str, Any]] = []

    for change in changes:
        store = str(change.get("store") or "")
        key = str(change.get("field_key") or "")
        new_value = change.get("new_value")

        if store == "profile" and key in physical_by_field:
            attribute_key, policy = physical_by_field[key]
            events = physical_attribute_stimulus_events(
                conn,
                character_id,
                attribute_key,
                as_of_sim_time=sim_time,
            )
            consumed = [event.event_id for event in events]
            event_id = record_event(
                conn,
                sim_time=sim_time,
                actor_id=character_id,
                event_type=policy.settlement_event_type,
                payload={
                    "source": SOURCE,
                    "creator_reanchor": True,
                    "attribute_key": attribute_key,
                    "field_key": key,
                    "bootstrap": False,
                    "settled_through_sim_time": sim_time,
                    "consumed_stimulus_event_ids": consumed,
                    "old_value": round(float(new_value), 6),
                    "new_value": round(float(new_value), 6),
                    "positive_delta": 0.0,
                    "negative_delta": 0.0,
                    "net_delta": 0.0,
                    "stat_mutated": False,
                },
            )
            physical_reanchors.append(
                {
                    "field_key": key,
                    "attribute_key": attribute_key,
                    "event_id": event_id,
                    "consumed_stimulus_event_ids": consumed,
                }
            )
            continue

        if store == "skill" and key.startswith("skill:"):
            skill_key = key.split(":", 1)[1]
            if skill_key not in configured_skills:
                continue
            events = _eligible_training_events(
                conn,
                character_id,
                skill_key,
                as_of_sim_time=sim_time,
                config=skill_config,
            )
            consumed = [int(event["event_id"]) for event in events]
            row = conn.execute(
                "SELECT experience FROM character_skills WHERE entity_id=? AND skill_key=?",
                (character_id, skill_key),
            ).fetchone()
            experience = 0.0 if row is None or row["experience"] is None else float(row["experience"])
            event_id = record_event(
                conn,
                sim_time=sim_time,
                actor_id=character_id,
                event_type=SKILL_SETTLEMENT_EVENT_TYPE,
                payload={
                    "source": SOURCE,
                    "skill_key": skill_key,
                    "creator_reanchor": True,
                    "bootstrap": False,
                    "consumed_action_event_ids": consumed,
                    "old_score": round(float(new_value), 6),
                    "new_score": round(float(new_value), 6),
                    "score_delta": 0.0,
                    "old_experience": round(experience, 6),
                    "new_experience": round(experience, 6),
                    "experience_gain": 0.0,
                    "evidence": [],
                },
            )
            skill_reanchors.append(
                {
                    "skill_key": skill_key,
                    "event_id": event_id,
                    "consumed_action_event_ids": consumed,
                }
            )

    return {
        "source": SOURCE,
        "sim_time": sim_time,
        "physical": physical_reanchors,
        "skills": skill_reanchors,
    }
