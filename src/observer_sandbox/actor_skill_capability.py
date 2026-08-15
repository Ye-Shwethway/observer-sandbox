from __future__ import annotations

import json
import sqlite3
from typing import Any, Iterable

from .skill_application_requirements import get_executable_skill_application
from .skill_capability import SkillCapabilityAssessment, assess_skill_application


class ActorSkillCapabilityError(ValueError):
    pass


def _actor_skill_score(conn: sqlite3.Connection, actor_id: str, skill_id: str) -> float:
    row = conn.execute(
        "SELECT score FROM character_skills WHERE entity_id=? AND skill_key=?",
        (actor_id, skill_id),
    ).fetchone()
    if row is None:
        raise ActorSkillCapabilityError(
            f"Actor {actor_id!r} has no authoritative Skill state for {skill_id!r}"
        )
    value = row["score"]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ActorSkillCapabilityError(
            f"Actor {actor_id!r} Skill {skill_id!r} has non-numeric score"
        )
    return float(value)


def _declared_attribute_values(
    conn: sqlite3.Connection,
    actor_id: str,
    definition: dict[str, Any],
) -> dict[str, float]:
    field_keys = [
        str(item.get("field_key"))
        for item in (definition.get("ability_dependencies") or [])
        if isinstance(item, dict) and isinstance(item.get("field_key"), str)
    ]
    if not field_keys:
        return {}

    placeholders = ",".join("?" for _ in field_keys)
    rows = conn.execute(
        f"""
        SELECT field_key,value_json
        FROM character_profile_values
        WHERE entity_id=? AND field_key IN ({placeholders})
        """,
        (actor_id, *field_keys),
    ).fetchall()
    values: dict[str, float] = {}
    for row in rows:
        field_key = str(row["field_key"])
        try:
            value = json.loads(row["value_json"])
        except (TypeError, json.JSONDecodeError) as exc:
            raise ActorSkillCapabilityError(
                f"Actor {actor_id!r} profile field {field_key!r} has invalid JSON"
            ) from exc
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ActorSkillCapabilityError(
                f"Actor {actor_id!r} profile field {field_key!r} must be numeric"
            )
        values[field_key] = float(value)
    return values


def assess_actor_skill_application(
    conn: sqlite3.Connection,
    actor_id: str,
    skill_id: str,
    application_id: str,
    *,
    challenge_class: str,
    context_tags: Iterable[str] | None = None,
    resource_capabilities: Iterable[str] | None = None,
    config: dict[str, Any] | None = None,
) -> SkillCapabilityAssessment:
    """Read authoritative actor inputs and delegate to the pure capability resolver.

    The adapter performs no writes and deliberately does not infer task context or
    resource capabilities from inventory, location, object names, model prose, or
    other ambient state. Those tokens belong to the caller/task contract.
    """

    definition, _application = get_executable_skill_application(
        skill_id,
        application_id,
        config=config,
    )
    score = _actor_skill_score(conn, actor_id, skill_id)
    attributes = _declared_attribute_values(conn, actor_id, definition)
    return assess_skill_application(
        skill_id,
        application_id,
        skill_score=score,
        challenge_class=challenge_class,
        context_tags=context_tags,
        resource_capabilities=resource_capabilities,
        attribute_values=attributes,
        config=config,
    )
