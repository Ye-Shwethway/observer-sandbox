from __future__ import annotations

import json
import sqlite3
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

from .grading import evaluate_skill_score


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_HIERARCHY_CONFIG_PATH = REPO_ROOT / "config" / "skill_hierarchy.v1.json"
SOURCE = "weapon-mastery-skill-hierarchy-foundation-v1"


class SkillHierarchyError(ValueError):
    pass


@lru_cache(maxsize=1)
def load_skill_hierarchy_config(path: str | Path = SKILL_HIERARCHY_CONFIG_PATH) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SkillHierarchyError("Skill hierarchy config requires an object root")
    validate_skill_hierarchy_config(value)
    return value


def validate_skill_hierarchy_config(source: Mapping[str, Any]) -> None:
    revision = source.get("revision")
    if not isinstance(revision, str) or not revision.strip():
        raise SkillHierarchyError("Skill hierarchy config requires a revision")
    hierarchies = source.get("hierarchies")
    if not isinstance(hierarchies, Mapping) or not hierarchies:
        raise SkillHierarchyError("Skill hierarchy config requires hierarchies")

    seen_components: set[str] = set()
    for parent_id, raw in hierarchies.items():
        if not isinstance(parent_id, str) or not parent_id:
            raise SkillHierarchyError("Skill hierarchy parent ids must be non-empty strings")
        if not isinstance(raw, Mapping):
            raise SkillHierarchyError(f"Hierarchy {parent_id!r} must be an object")
        if raw.get("role") != "derived_parent":
            raise SkillHierarchyError(f"Hierarchy {parent_id!r} must declare role derived_parent")
        if raw.get("direct_progression") is not False or raw.get("direct_application") is not False:
            raise SkillHierarchyError(
                f"Hierarchy {parent_id!r} derived parent cannot own direct progression or application"
            )
        components = raw.get("component_skills")
        component_defs = raw.get("components")
        if not isinstance(components, list) or len(components) < 2:
            raise SkillHierarchyError(f"Hierarchy {parent_id!r} requires at least two component Skills")
        if not isinstance(component_defs, Mapping) or set(component_defs) != set(components):
            raise SkillHierarchyError(f"Hierarchy {parent_id!r} component definitions must match component_skills")
        if parent_id in components or len(set(components)) != len(components):
            raise SkillHierarchyError(f"Hierarchy {parent_id!r} has invalid component identity")
        overlap = seen_components.intersection(components)
        if overlap:
            raise SkillHierarchyError(f"Component Skills cannot belong to multiple v1 parents: {sorted(overlap)!r}")
        seen_components.update(str(value) for value in components)

        aggregation = raw.get("aggregation")
        if not isinstance(aggregation, Mapping) or aggregation.get("method") != "mean":
            raise SkillHierarchyError(f"Hierarchy {parent_id!r} v1 aggregation must be mean")
        weights = aggregation.get("weights")
        if not isinstance(weights, Mapping) or set(weights) != set(components):
            raise SkillHierarchyError(f"Hierarchy {parent_id!r} aggregation weights must match components")
        for component in components:
            weight = weights.get(component)
            if isinstance(weight, bool) or not isinstance(weight, (int, float)) or float(weight) <= 0.0:
                raise SkillHierarchyError(f"Hierarchy {parent_id!r} component weights must be positive numbers")

        legacy = raw.get("legacy_skill_keys")
        if not isinstance(legacy, list) or not legacy or not all(isinstance(item, str) and item for item in legacy):
            raise SkillHierarchyError(f"Hierarchy {parent_id!r} requires legacy_skill_keys")


def _metadata(row: sqlite3.Row | None) -> dict[str, Any]:
    if row is None:
        return {}
    try:
        value = json.loads(row["metadata_json"] or "{}")
    except (TypeError, json.JSONDecodeError) as exc:
        raise SkillHierarchyError("Skill metadata contains invalid JSON") from exc
    return value if isinstance(value, dict) else {}


def hierarchy_skill_descriptor(skill_id: str, *, config: dict[str, Any] | None = None) -> dict[str, Any] | None:
    source = config if config is not None else load_skill_hierarchy_config()
    for parent_id, hierarchy in (source.get("hierarchies") or {}).items():
        if skill_id == parent_id:
            return {
                "skill_id": parent_id,
                "name": hierarchy["name"],
                "category": hierarchy["category"],
                "hierarchy_role": "parent",
                "parent_skill": None,
                "component_skills": list(hierarchy["component_skills"]),
                "description": hierarchy["description"],
                "direct_progression": False,
                "direct_application": False,
            }
        component = (hierarchy.get("components") or {}).get(skill_id)
        if isinstance(component, Mapping):
            return {
                "skill_id": skill_id,
                "name": component["name"],
                "category": component["category"],
                "hierarchy_role": "component",
                "parent_skill": parent_id,
                "component_skills": [],
                "description": component["description"],
                "direct_progression": True,
                "direct_application": True,
                "legacy_application_family": list(component.get("legacy_application_family") or []),
            }
    return None


def _numeric_score(value: object, *, skill_id: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SkillHierarchyError(f"Skill {skill_id!r} requires a numeric score")
    score = float(value)
    if not 0.0 <= score <= 100.0:
        raise SkillHierarchyError(f"Skill {skill_id!r} score must be within 0..100")
    return score


def _skill_row(conn: sqlite3.Connection, entity_id: str, skill_id: str) -> sqlite3.Row | None:
    return conn.execute(
        """SELECT skill_key,category,score,tier,experience,metadata_json
        FROM character_skills WHERE entity_id=? AND skill_key=?""",
        (entity_id, skill_id),
    ).fetchone()


def _upsert_component(
    conn: sqlite3.Connection,
    entity_id: str,
    *,
    parent_id: str,
    component_id: str,
    component: Mapping[str, Any],
    baseline: float,
    legacy_key: str,
    profile_order: int,
) -> None:
    if _skill_row(conn, entity_id, component_id) is not None:
        return
    metadata = {
        "source": SOURCE,
        "hierarchy_role": "component",
        "parent_skill": parent_id,
        "display_name": component["name"],
        "profile_order": profile_order,
        "baseline_provenance": {
            "kind": "legacy_umbrella_compatibility_baseline",
            "legacy_skill_key": legacy_key,
            "legacy_score": baseline,
            "distinct_historical_specialization_evidence": False,
        },
        "progression_active": False,
    }
    conn.execute(
        """INSERT INTO character_skills(
        entity_id,skill_key,category,score,tier,experience,metadata_json
        ) VALUES(?,?,?,?,?,?,?)""",
        (
            entity_id,
            component_id,
            component.get("category"),
            baseline,
            None,
            None,
            json.dumps(metadata, ensure_ascii=False, sort_keys=True),
        ),
    )


def _derived_score(conn: sqlite3.Connection, entity_id: str, hierarchy: Mapping[str, Any]) -> float:
    components = list(hierarchy["component_skills"])
    weights = hierarchy["aggregation"]["weights"]
    weighted = 0.0
    total_weight = 0.0
    for component_id in components:
        row = _skill_row(conn, entity_id, component_id)
        if row is None:
            raise SkillHierarchyError(f"Missing component Skill {component_id!r} for derived parent")
        score = _numeric_score(row["score"], skill_id=component_id)
        weight = float(weights[component_id])
        weighted += score * weight
        total_weight += weight
    if total_weight <= 0.0:
        raise SkillHierarchyError("Derived Skill hierarchy has no positive aggregation weight")
    return round(weighted / total_weight, 6)


def _upsert_parent(
    conn: sqlite3.Connection,
    entity_id: str,
    *,
    parent_id: str,
    hierarchy: Mapping[str, Any],
    score: float,
) -> None:
    metadata = {
        "source": SOURCE,
        "hierarchy_role": "parent",
        "display_name": hierarchy["name"],
        "component_skills": list(hierarchy["component_skills"]),
        "aggregation": dict(hierarchy["aggregation"]),
        "derived": True,
        "direct_progression": False,
        "direct_application": False,
        "aggregate_exclude": True,
        "profile_order": 10,
    }
    conn.execute(
        """INSERT INTO character_skills(
        entity_id,skill_key,category,score,tier,experience,metadata_json
        ) VALUES(?,?,?,?,?,?,?)
        ON CONFLICT(entity_id,skill_key) DO UPDATE SET
          category=excluded.category,
          score=excluded.score,
          tier=NULL,
          experience=NULL,
          metadata_json=excluded.metadata_json""",
        (
            entity_id,
            parent_id,
            hierarchy.get("category"),
            score,
            None,
            None,
            json.dumps(metadata, ensure_ascii=False, sort_keys=True),
        ),
    )


def _upsert_legacy_projection(
    conn: sqlite3.Connection,
    entity_id: str,
    *,
    legacy_key: str,
    parent_id: str,
    category: str,
    score: float,
) -> None:
    row = _skill_row(conn, entity_id, legacy_key)
    prior_metadata = _metadata(row)
    metadata = {
        **prior_metadata,
        "source": SOURCE,
        "compatibility_projection": True,
        "profile_hidden": True,
        "projection_of": parent_id,
        "derived": True,
        "direct_progression": False,
    }
    conn.execute(
        """INSERT INTO character_skills(
        entity_id,skill_key,category,score,tier,experience,metadata_json
        ) VALUES(?,?,?,?,?,?,?)
        ON CONFLICT(entity_id,skill_key) DO UPDATE SET
          category=excluded.category,
          score=excluded.score,
          tier=NULL,
          experience=NULL,
          metadata_json=excluded.metadata_json""",
        (
            entity_id,
            legacy_key,
            category,
            score,
            None,
            None,
            json.dumps(metadata, ensure_ascii=False, sort_keys=True),
        ),
    )


def reconcile_skill_hierarchies(
    conn: sqlite3.Connection,
    entity_id: str | None = None,
    *,
    config: dict[str, Any] | None = None,
) -> None:
    """Migrate umbrella Skill state into learned components plus derived parents.

    The first migration copies the legacy umbrella score only as a compatibility
    baseline because historical data cannot prove distinct specialization scores.
    Existing component rows are never overwritten. Every later reconciliation
    derives the parent and hidden legacy projection from current component state.
    """
    source = config if config is not None else load_skill_hierarchy_config()
    validate_skill_hierarchy_config(source)
    if entity_id is None:
        entity_ids = [
            str(row["entity_id"])
            for row in conn.execute(
                "SELECT entity_id FROM character_profiles WHERE status='active' ORDER BY entity_id"
            ).fetchall()
        ]
    else:
        entity_ids = [entity_id]

    for actor_id in entity_ids:
        for parent_id, hierarchy in source["hierarchies"].items():
            legacy_keys = list(hierarchy["legacy_skill_keys"])
            legacy_row = next(
                (_skill_row(conn, actor_id, key) for key in legacy_keys if _skill_row(conn, actor_id, key) is not None),
                None,
            )
            parent_row = _skill_row(conn, actor_id, parent_id)
            existing_components = [
                _skill_row(conn, actor_id, component_id)
                for component_id in hierarchy["component_skills"]
            ]
            if legacy_row is None and parent_row is None and not any(existing_components):
                continue

            if not any(existing_components):
                baseline_row = legacy_row if legacy_row is not None else parent_row
                if baseline_row is None:
                    continue
                baseline = _numeric_score(baseline_row["score"], skill_id=str(baseline_row["skill_key"]))
                legacy_key = str(legacy_row["skill_key"]) if legacy_row is not None else legacy_keys[0]
                for index, component_id in enumerate(hierarchy["component_skills"], start=1):
                    component = hierarchy["components"][component_id]
                    _upsert_component(
                        conn,
                        actor_id,
                        parent_id=parent_id,
                        component_id=component_id,
                        component=component,
                        baseline=baseline,
                        legacy_key=legacy_key,
                        profile_order=10 + index,
                    )

            score = _derived_score(conn, actor_id, hierarchy)
            _upsert_parent(
                conn,
                actor_id,
                parent_id=parent_id,
                hierarchy=hierarchy,
                score=score,
            )
            if hierarchy["migration_policy"].get("keep_legacy_key_as_hidden_compatibility_projection"):
                for legacy_key in legacy_keys:
                    _upsert_legacy_projection(
                        conn,
                        actor_id,
                        legacy_key=legacy_key,
                        parent_id=parent_id,
                        category=str(hierarchy["category"]),
                        score=score,
                    )
    conn.commit()


def hierarchy_profile_metadata(metadata: Mapping[str, Any] | None) -> dict[str, Any]:
    value = dict(metadata or {})
    return {
        "profile_hidden": bool(value.get("profile_hidden")),
        "hierarchy_role": value.get("hierarchy_role"),
        "parent_skill": value.get("parent_skill"),
        "component_skills": list(value.get("component_skills") or []),
        "derived": bool(value.get("derived")),
        "aggregate_exclude": bool(value.get("aggregate_exclude")),
        "display_name": value.get("display_name"),
        "profile_order": int(value.get("profile_order", 999)),
        "compatibility_projection": bool(value.get("compatibility_projection")),
    }


def hierarchy_cognition_awareness(row: sqlite3.Row) -> dict[str, Any] | None:
    descriptor = hierarchy_skill_descriptor(str(row["skill_key"]))
    if descriptor is None:
        return None
    score = _numeric_score(row["score"], skill_id=descriptor["skill_id"])
    grade = evaluate_skill_score(score)
    parent = descriptor["hierarchy_role"] == "parent"
    return {
        "skill_id": descriptor["skill_id"],
        "name": descriptor["name"],
        "category": row["category"],
        "hierarchy": {
            "role": descriptor["hierarchy_role"],
            "parent_skill": descriptor["parent_skill"],
            "component_skills": list(descriptor["component_skills"]),
            "derived_parent": parent,
        },
        "proficiency": {
            "score": score,
            "grade": grade.grade,
            "label": grade.label,
            "behavioral_anchor": {
                "summary": "Derived overview only." if parent else "Learned specialization proficiency.",
                "independence": "Not executable directly." if parent else "Executable only through separately represented and authorized task contracts.",
                "supported_challenges": [],
                "limits": "This hierarchy foundation does not itself authorize weapon use or create a represented weapon runtime.",
            },
        },
        "definition": descriptor["description"],
        "scope_includes": list(descriptor.get("legacy_application_family") or []),
        "scope_excludes": ["hostile authorization", "lethality", "automatic learning from generic use"],
        "applications": [],
        "supporting_attributes": [],
        "knowledge_context": {
            "mode": "hierarchy_foundation_only",
            "keys": [],
        },
    }
