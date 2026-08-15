from __future__ import annotations

import json
import sqlite3
from typing import Any

from .grading import evaluate_skill_score
from .skill_application_requirements import get_executable_skill_application
from .skill_definitions import load_skill_definition_config
from .skill_hierarchy import (
    hierarchy_cognition_awareness,
    hierarchy_profile_metadata,
    hierarchy_skill_descriptor,
)


COGNITIVE_FACTOR_FIELDS: tuple[tuple[str, str], ...] = (
    ("raps_ia.iq", "general_reasoning_capacity"),
    ("raps_ia.problem_solving", "problem_solving"),
    ("raps_ma.focus", "focus"),
    ("raps_ma.adaptability", "adaptability"),
    ("raps_ia.creativity", "creativity"),
    ("raps_ma.emotional_stability", "emotional_stability"),
    ("raps_ma.stress_management", "stress_management"),
    ("raps_ia.tactical_thinking", "tactical_thinking"),
)


class CognitionCapabilityAwarenessError(ValueError):
    pass


def _numeric_profile_value(
    conn: sqlite3.Connection,
    actor_id: str,
    field_key: str,
) -> float | int | None:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, field_key),
    ).fetchone()
    if row is None:
        return None
    try:
        value = json.loads(row["value_json"])
    except (TypeError, json.JSONDecodeError) as exc:
        raise CognitionCapabilityAwarenessError(
            f"Actor {actor_id!r} profile field {field_key!r} has invalid JSON"
        ) from exc
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CognitionCapabilityAwarenessError(
            f"Actor {actor_id!r} profile field {field_key!r} must be numeric"
        )
    return value


def _supporting_attributes(
    conn: sqlite3.Connection,
    actor_id: str,
    definition: dict[str, Any],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for dependency in definition.get("ability_dependencies") or []:
        if not isinstance(dependency, dict):
            continue
        field_key = dependency.get("field_key")
        if not isinstance(field_key, str):
            continue
        result.append(
            {
                "field_key": field_key,
                "value": _numeric_profile_value(conn, actor_id, field_key),
                "relationship": dependency.get("relationship"),
                "relevance": dependency.get("relevance"),
            }
        )
    return result


def _application_awareness(application: dict[str, Any]) -> dict[str, Any]:
    requirements = application.get("requirements") or {}
    knowledge = requirements.get("knowledge") or {}
    risk = application.get("risk") or {}
    return {
        "application_id": application.get("application_id"),
        "name": application.get("name"),
        "description": application.get("description"),
        "outcome_intent": application.get("outcome_intent"),
        "challenge_classes": list(application.get("challenge_classes") or []),
        "required_context": list(application.get("required_context") or []),
        "helpful_resources": list(application.get("helpful_resources") or []),
        "required_context_tags": list(requirements.get("context_tags_all") or []),
        "required_resource_mode": requirements.get("required_resource_mode"),
        "required_resource_capabilities_any": list(
            requirements.get("resource_capabilities_any") or []
        ),
        "supporting_resource_capabilities": list(
            requirements.get("supporting_resource_capabilities") or []
        ),
        "supporting_knowledge_keys": list(knowledge.get("supporting_keys") or []),
        "risk_class": risk.get("default_class"),
        "failure_modes": list(risk.get("failure_modes") or []),
    }


def _skill_awareness(
    conn: sqlite3.Connection,
    actor_id: str,
    row: sqlite3.Row,
    definition: dict[str, Any],
) -> dict[str, Any]:
    score = row["score"]
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise CognitionCapabilityAwarenessError(
            f"Actor {actor_id!r} Skill {row['skill_key']!r} has non-numeric score"
        )
    grade = evaluate_skill_score(score)
    anchor = (definition.get("proficiency_anchors") or {}).get(grade.grade)
    if not isinstance(anchor, dict):
        raise CognitionCapabilityAwarenessError(
            f"Skill {row['skill_key']!r} lacks proficiency anchor {grade.grade!r}"
        )
    return {
        "skill_id": row["skill_key"],
        "name": definition.get("name"),
        "category": row["category"],
        "proficiency": {
            "score": float(score),
            "grade": grade.grade,
            "label": grade.label,
            "behavioral_anchor": {
                "summary": anchor.get("summary"),
                "independence": anchor.get("independence"),
                "supported_challenges": list(anchor.get("supported_challenges") or []),
                "limits": anchor.get("limits"),
            },
        },
        "definition": definition.get("definition"),
        "scope_includes": list(definition.get("scope_includes") or []),
        "scope_excludes": list(definition.get("scope_excludes") or []),
        "applications": [
            _application_awareness(application)
            for application in (definition.get("applications") or [])
            if isinstance(application, dict)
        ],
        "supporting_attributes": _supporting_attributes(conn, actor_id, definition),
        "knowledge_context": {
            "mode": "declarative_only_not_actor_knowledge_state",
            "keys": [
                item.get("knowledge_key")
                for item in (definition.get("knowledge_requirements") or [])
                if isinstance(item, dict) and isinstance(item.get("knowledge_key"), str)
            ],
        },
    }


def _hierarchy_awareness_with_active_applications(
    conn: sqlite3.Connection,
    actor_id: str,
    row: sqlite3.Row,
) -> dict[str, Any] | None:
    awareness = hierarchy_cognition_awareness(row)
    if awareness is None:
        return None
    descriptor = hierarchy_skill_descriptor(str(row["skill_key"]))
    if descriptor is None or descriptor.get("hierarchy_role") != "component":
        return awareness

    applications: list[dict[str, Any]] = []
    definitions: list[dict[str, Any]] = []
    for application_id in descriptor.get("legacy_application_family") or []:
        try:
            definition, application = get_executable_skill_application(
                str(row["skill_key"]),
                str(application_id),
            )
        except (KeyError, ValueError):
            continue
        applications.append(_application_awareness(application))
        definitions.append(definition)

    if not applications:
        return awareness

    enriched = dict(awareness)
    enriched["applications"] = applications
    # All currently activated applications for one hierarchy component are derived
    # from one canonical semantic source. Keep support context read-only and avoid
    # inventing a separate Knowledge state for the component.
    definition = definitions[0]
    enriched["supporting_attributes"] = _supporting_attributes(conn, actor_id, definition)
    enriched["knowledge_context"] = {
        "mode": "declarative_only_not_actor_knowledge_state",
        "keys": [
            item.get("knowledge_key")
            for item in (definition.get("knowledge_requirements") or [])
            if isinstance(item, dict) and isinstance(item.get("knowledge_key"), str)
        ],
    }
    return enriched


def cognition_capability_awareness(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build read-only semantic capability context for model cognition.

    The returned values help cognition reason about what the actor can plausibly
    attempt. They do not authorize actions, mutate state, invent Knowledge state,
    or modify deterministic Skill/capability resolution.
    """

    source = config if config is not None else load_skill_definition_config()
    definitions = source.get("skills") or {}
    rows = conn.execute(
        """SELECT skill_key,category,score,metadata_json
        FROM character_skills WHERE entity_id=? ORDER BY skill_key""",
        (actor_id,),
    ).fetchall()

    skills: list[dict[str, Any]] = []
    unresolved_skills: list[str] = []
    for row in rows:
        try:
            raw_metadata = json.loads(row["metadata_json"] or "{}")
        except (TypeError, json.JSONDecodeError):
            raw_metadata = {}
        metadata = hierarchy_profile_metadata(raw_metadata if isinstance(raw_metadata, dict) else {})
        if metadata["compatibility_projection"]:
            continue

        skill_id = str(row["skill_key"])
        definition = definitions.get(skill_id) if isinstance(definitions, dict) else None
        if isinstance(definition, dict):
            skills.append(_skill_awareness(conn, actor_id, row, definition))
            continue
        hierarchy_awareness = _hierarchy_awareness_with_active_applications(
            conn,
            actor_id,
            row,
        )
        if hierarchy_awareness is not None:
            skills.append(hierarchy_awareness)
            continue
        unresolved_skills.append(skill_id)

    reasoning_factors = {
        semantic_key: {
            "field_key": field_key,
            "value": _numeric_profile_value(conn, actor_id, field_key),
        }
        for field_key, semantic_key in COGNITIVE_FACTOR_FIELDS
    }

    return {
        "revision": "cognition-capability-awareness-v1",
        "actor_id": actor_id,
        "skills": skills,
        "unresolved_skills": unresolved_skills,
        "reasoning_profile": {
            "factors": reasoning_factors,
            "principles": [
                "General reasoning capacity can affect planning and problem solving but does not create missing knowledge or learned Skill proficiency.",
                "Supporting attributes inform judgment only where the relevant Skill/task contract declares them; they do not replace the authoritative Skill score.",
                "Knowledge keys describe semantic support requirements only; no hidden actor Knowledge score is inferred when no Knowledge subsystem exists.",
                "Use numeric scores and grade labels only to calibrate internal decision quality; do not mention game-stat numbers or grade letters in in-world reasons.",
                "Action legality, target/resource validity, task outcomes, and state mutation remain deterministic engine authority.",
            ],
        },
    }
