from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from .grading import SKILL_PROFICIENCY_100_SCHEME_ID, SCHEME_REGISTRY
from .profile_schema import FIELDS


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DEFINITIONS_CONFIG_PATH = REPO_ROOT / "config" / "skill_definitions.v1.json"
SKILL_PRACTICE_CONFIG_PATH = REPO_ROOT / "config" / "skill_practice_methods.v1.json"
SKILL_PROGRESSION_CONFIG_PATH = REPO_ROOT / "config" / "skill_progression.v1.json"

SKILL_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
EXPECTED_ANCHORS = ("E", "D", "C", "B", "A", "S")
CHALLENGE_CLASSES = ("routine", "standard", "challenging", "advanced", "extreme")
CHALLENGE_INDEX = {value: index for index, value in enumerate(CHALLENGE_CLASSES)}
ALLOWED_STATUSES = {"active", "experimental", "deprecated"}
ALLOWED_REUSABILITY = {"transversal", "cross_domain", "domain_specific", "specialized"}
ALLOWED_SKILL_TYPES = {"motor", "technical", "cognitive", "medical", "fieldcraft", "social", "mixed"}
ALLOWED_DEPENDENCY_RELATIONSHIPS = {"prerequisite", "performance_modifier", "learning_modifier"}
ALLOWED_SKILL_RELATIONS = {"complementary", "prerequisite", "overlaps", "transfer_source", "transfer_target"}
ALLOWED_GAMEPLAY_EFFECTS = {
    "feasibility",
    "quality_precision",
    "time_speed",
    "resource_efficiency",
    "error_probability_severity",
    "information_gained",
    "stealth_detection_exposure",
    "partial_failure_recovery",
    "available_action_variants",
}
ALLOWED_RISK_CLASSES = {"low", "moderate", "high", "critical"}
FORBIDDEN_ACTOR_STATE_KEYS = {"score", "experience", "tier", "grade", "actor_id", "entity_id"}
GENERIC_IMPLICIT_ACTIONS = {"use", "inspect", "research", "monitor"}


class SkillDefinitionValidationError(ValueError):
    pass


def _load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SkillDefinitionValidationError(f"{path}: expected object root")
    return value


@lru_cache(maxsize=1)
def load_skill_definition_config(path: str | Path = SKILL_DEFINITIONS_CONFIG_PATH) -> dict[str, Any]:
    return _load_json(path)


def _required_string(value: dict[str, Any], key: str, path: str) -> str:
    result = value.get(key)
    if not isinstance(result, str) or not result.strip():
        raise SkillDefinitionValidationError(f"{path}.{key}: required non-empty string")
    return result.strip()


def _string_list(value: object, path: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list):
        raise SkillDefinitionValidationError(f"{path}: expected list")
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise SkillDefinitionValidationError(f"{path}[{index}]: expected non-empty string")
        result.append(item.strip())
    if nonempty and not result:
        raise SkillDefinitionValidationError(f"{path}: must not be empty")
    if len(result) != len(set(result)):
        raise SkillDefinitionValidationError(f"{path}: duplicate values are not allowed")
    return result


def _walk_forbidden_actor_state(value: object, path: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_ACTOR_STATE_KEYS:
                raise SkillDefinitionValidationError(
                    f"{path}.{key}: universal Skill Definitions must not contain actor state"
                )
            _walk_forbidden_actor_state(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_forbidden_actor_state(child, f"{path}[{index}]")


def _validate_identity(skill_id: str, definition: dict[str, Any], path: str) -> None:
    if not SKILL_ID_RE.fullmatch(skill_id):
        raise SkillDefinitionValidationError(f"{path}: invalid skill id {skill_id!r}")
    if definition.get("skill_id") != skill_id:
        raise SkillDefinitionValidationError(f"{path}.skill_id: must equal registry key {skill_id!r}")
    _required_string(definition, "name", path)
    _required_string(definition, "revision", path)
    status = _required_string(definition, "status", path)
    if status not in ALLOWED_STATUSES:
        raise SkillDefinitionValidationError(f"{path}.status: unsupported value {status!r}")
    _required_string(definition, "category", path)
    skill_type = _required_string(definition, "skill_type", path)
    if skill_type not in ALLOWED_SKILL_TYPES:
        raise SkillDefinitionValidationError(f"{path}.skill_type: unsupported value {skill_type!r}")
    reusability = _required_string(definition, "reusability", path)
    if reusability not in ALLOWED_REUSABILITY:
        raise SkillDefinitionValidationError(f"{path}.reusability: unsupported value {reusability!r}")
    aliases = definition.get("aliases", [])
    _string_list(aliases, f"{path}.aliases")


def _validate_scope(definition: dict[str, Any], path: str) -> None:
    text = _required_string(definition, "definition", path)
    if len(text) < 30:
        raise SkillDefinitionValidationError(f"{path}.definition: definition is too weak/short")
    _string_list(definition.get("scope_includes"), f"{path}.scope_includes", nonempty=True)
    _string_list(definition.get("scope_excludes"), f"{path}.scope_excludes", nonempty=True)


def _validate_relations(skill_id: str, definition: dict[str, Any], skills: dict[str, Any], path: str) -> None:
    relations = definition.get("relations")
    if not isinstance(relations, dict):
        raise SkillDefinitionValidationError(f"{path}.relations: expected object")
    parent = relations.get("parent_skill")
    if parent is not None:
        if not isinstance(parent, str) or parent not in skills:
            raise SkillDefinitionValidationError(f"{path}.relations.parent_skill: unknown Skill {parent!r}")
        if parent == skill_id:
            raise SkillDefinitionValidationError(f"{path}.relations.parent_skill: Skill cannot parent itself")
    components = _string_list(relations.get("component_skills", []), f"{path}.relations.component_skills")
    for component in components:
        if component not in skills:
            raise SkillDefinitionValidationError(f"{path}.relations.component_skills: unknown Skill {component!r}")
        if component == skill_id:
            raise SkillDefinitionValidationError(f"{path}.relations.component_skills: Skill cannot contain itself")
    related = relations.get("related_skills", [])
    if not isinstance(related, list):
        raise SkillDefinitionValidationError(f"{path}.relations.related_skills: expected list")
    for index, item in enumerate(related):
        item_path = f"{path}.relations.related_skills[{index}]"
        if not isinstance(item, dict):
            raise SkillDefinitionValidationError(f"{item_path}: expected object")
        target = _required_string(item, "skill_id", item_path)
        relation = _required_string(item, "relationship", item_path)
        if target not in skills:
            raise SkillDefinitionValidationError(f"{item_path}.skill_id: unknown Skill {target!r}")
        if target == skill_id:
            raise SkillDefinitionValidationError(f"{item_path}.skill_id: self relation is not allowed")
        if relation not in ALLOWED_SKILL_RELATIONS:
            raise SkillDefinitionValidationError(f"{item_path}.relationship: unsupported value {relation!r}")


def _validate_hierarchy_cycles(skills: dict[str, Any]) -> None:
    edges: dict[str, set[str]] = {skill_id: set() for skill_id in skills}
    for skill_id, definition in skills.items():
        relations = definition.get("relations") or {}
        parent = relations.get("parent_skill")
        if isinstance(parent, str):
            edges[parent].add(skill_id)
        for child in relations.get("component_skills") or []:
            if isinstance(child, str):
                edges[skill_id].add(child)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(skill_id: str) -> None:
        if skill_id in visiting:
            raise SkillDefinitionValidationError(f"Skill hierarchy contains a cycle at {skill_id!r}")
        if skill_id in visited:
            return
        visiting.add(skill_id)
        for child in edges[skill_id]:
            visit(child)
        visiting.remove(skill_id)
        visited.add(skill_id)

    for skill_id in edges:
        visit(skill_id)


def _validate_dependencies(definition: dict[str, Any], path: str) -> None:
    knowledge = definition.get("knowledge_requirements")
    if not isinstance(knowledge, list):
        raise SkillDefinitionValidationError(f"{path}.knowledge_requirements: expected list")
    knowledge_keys: set[str] = set()
    for index, item in enumerate(knowledge):
        item_path = f"{path}.knowledge_requirements[{index}]"
        if not isinstance(item, dict):
            raise SkillDefinitionValidationError(f"{item_path}: expected object")
        key = _required_string(item, "knowledge_key", item_path)
        if key in knowledge_keys:
            raise SkillDefinitionValidationError(f"{item_path}.knowledge_key: duplicate {key!r}")
        knowledge_keys.add(key)
        _required_string(item, "description", item_path)
        relationship = _required_string(item, "relationship", item_path)
        if relationship not in ALLOWED_DEPENDENCY_RELATIONSHIPS:
            raise SkillDefinitionValidationError(f"{item_path}.relationship: unsupported {relationship!r}")
        importance = item.get("importance")
        if not isinstance(importance, (int, float)) or isinstance(importance, bool) or not 0.0 <= float(importance) <= 1.0:
            raise SkillDefinitionValidationError(f"{item_path}.importance: expected number in 0..1")
        if not isinstance(item.get("blocking_if_absent"), bool):
            raise SkillDefinitionValidationError(f"{item_path}.blocking_if_absent: expected boolean")

    allowed_fields = {field.key for field in FIELDS}
    abilities = definition.get("ability_dependencies")
    if not isinstance(abilities, list):
        raise SkillDefinitionValidationError(f"{path}.ability_dependencies: expected list")
    field_keys: set[str] = set()
    for index, item in enumerate(abilities):
        item_path = f"{path}.ability_dependencies[{index}]"
        if not isinstance(item, dict):
            raise SkillDefinitionValidationError(f"{item_path}: expected object")
        field_key = _required_string(item, "field_key", item_path)
        if field_key not in allowed_fields:
            raise SkillDefinitionValidationError(f"{item_path}.field_key: unknown profile/attribute field {field_key!r}")
        if field_key in field_keys:
            raise SkillDefinitionValidationError(f"{item_path}.field_key: duplicate {field_key!r}")
        field_keys.add(field_key)
        relationship = _required_string(item, "relationship", item_path)
        if relationship not in ALLOWED_DEPENDENCY_RELATIONSHIPS:
            raise SkillDefinitionValidationError(f"{item_path}.relationship: unsupported {relationship!r}")
        relevance = item.get("relevance")
        if not isinstance(relevance, (int, float)) or isinstance(relevance, bool) or not 0.0 < float(relevance) <= 1.0:
            raise SkillDefinitionValidationError(f"{item_path}.relevance: expected number in (0,1]")


def _validate_effects(effects: object, path: str, *, nonempty: bool = True) -> list[str]:
    values = _string_list(effects, path, nonempty=nonempty)
    unknown = sorted(set(values) - ALLOWED_GAMEPLAY_EFFECTS)
    if unknown:
        raise SkillDefinitionValidationError(f"{path}: unsupported gameplay effects {unknown!r}")
    return values


def _validate_applications(definition: dict[str, Any], path: str) -> None:
    applications = definition.get("applications")
    if not isinstance(applications, list) or not applications:
        raise SkillDefinitionValidationError(f"{path}.applications: at least one observable application is required")
    ids: set[str] = set()
    for index, app in enumerate(applications):
        app_path = f"{path}.applications[{index}]"
        if not isinstance(app, dict):
            raise SkillDefinitionValidationError(f"{app_path}: expected object")
        app_id = _required_string(app, "application_id", app_path)
        if not SKILL_ID_RE.fullmatch(app_id):
            raise SkillDefinitionValidationError(f"{app_path}.application_id: invalid id {app_id!r}")
        if app_id in ids:
            raise SkillDefinitionValidationError(f"{app_path}.application_id: duplicate {app_id!r}")
        ids.add(app_id)
        _required_string(app, "name", app_path)
        _required_string(app, "description", app_path)
        _required_string(app, "outcome_intent", app_path)
        if app.get("skill_role") not in {"primary", "supporting"}:
            raise SkillDefinitionValidationError(f"{app_path}.skill_role: expected primary or supporting")
        challenges = _string_list(app.get("challenge_classes"), f"{app_path}.challenge_classes", nonempty=True)
        if any(value not in CHALLENGE_INDEX for value in challenges):
            raise SkillDefinitionValidationError(f"{app_path}.challenge_classes: unknown challenge class")
        _string_list(app.get("required_context"), f"{app_path}.required_context", nonempty=True)
        _string_list(app.get("helpful_resources", []), f"{app_path}.helpful_resources")
        _validate_effects(app.get("gameplay_effects"), f"{app_path}.gameplay_effects")
        risk = app.get("risk")
        if not isinstance(risk, dict):
            raise SkillDefinitionValidationError(f"{app_path}.risk: expected object")
        risk_class = _required_string(risk, "default_class", f"{app_path}.risk")
        if risk_class not in ALLOWED_RISK_CLASSES:
            raise SkillDefinitionValidationError(f"{app_path}.risk.default_class: unsupported {risk_class!r}")
        _string_list(risk.get("failure_modes"), f"{app_path}.risk.failure_modes", nonempty=True)
        consequence = _required_string(risk, "consequence_bounds", f"{app_path}.risk")
        if risk_class in {"high", "critical"} and len(consequence) < 40:
            raise SkillDefinitionValidationError(f"{app_path}.risk.consequence_bounds: high-risk boundary is too weak")
        _required_string(risk, "practice_reliability_boundary", f"{app_path}.risk")


def _validate_proficiency_anchors(definition: dict[str, Any], path: str) -> None:
    scheme_id = _required_string(definition, "grading_scheme", path)
    if scheme_id != SKILL_PROFICIENCY_100_SCHEME_ID or scheme_id not in SCHEME_REGISTRY:
        raise SkillDefinitionValidationError(
            f"{path}.grading_scheme: v1 definitions require {SKILL_PROFICIENCY_100_SCHEME_ID!r}"
        )
    anchors = definition.get("proficiency_anchors")
    if not isinstance(anchors, dict):
        raise SkillDefinitionValidationError(f"{path}.proficiency_anchors: expected object")
    if tuple(anchors.keys()) != EXPECTED_ANCHORS:
        raise SkillDefinitionValidationError(
            f"{path}.proficiency_anchors: expected ordered anchors {EXPECTED_ANCHORS!r}; SS+ is unsupported on 0..100"
        )
    prior_max = -1
    for grade in EXPECTED_ANCHORS:
        anchor = anchors[grade]
        anchor_path = f"{path}.proficiency_anchors.{grade}"
        if not isinstance(anchor, dict):
            raise SkillDefinitionValidationError(f"{anchor_path}: expected object")
        _required_string(anchor, "summary", anchor_path)
        _required_string(anchor, "independence", anchor_path)
        challenges = _string_list(anchor.get("supported_challenges"), f"{anchor_path}.supported_challenges", nonempty=True)
        indices = [CHALLENGE_INDEX.get(value, -1) for value in challenges]
        if any(index < 0 for index in indices):
            raise SkillDefinitionValidationError(f"{anchor_path}.supported_challenges: unknown challenge class")
        if indices != sorted(set(indices)):
            raise SkillDefinitionValidationError(f"{anchor_path}.supported_challenges: must be unique and ordered")
        current_max = max(indices)
        if current_max < prior_max:
            raise SkillDefinitionValidationError(f"{anchor_path}: higher proficiency cannot reduce supported challenge range")
        prior_max = current_max
        _required_string(anchor, "limits", anchor_path)


def _validate_learning_evidence(
    skill_id: str,
    definition: dict[str, Any],
    path: str,
    practice_config: dict[str, Any],
    progression_config: dict[str, Any],
) -> None:
    evidence = definition.get("learning_evidence")
    if not isinstance(evidence, dict):
        raise SkillDefinitionValidationError(f"{path}.learning_evidence: expected object")
    families = _string_list(evidence.get("families"), f"{path}.learning_evidence.families", nonempty=True)
    if not set(families) <= {"training_method", "skill_practice", "supervised_application", "live_application", "topic_aware_study"}:
        raise SkillDefinitionValidationError(f"{path}.learning_evidence.families: unsupported evidence family")
    if evidence.get("implicit_action_evidence") is not False:
        raise SkillDefinitionValidationError(f"{path}.learning_evidence.implicit_action_evidence: must be false in v1")
    notes = _required_string(evidence, "notes", f"{path}.learning_evidence")
    lower_notes = notes.lower()
    if any(f"generic {action}" not in lower_notes and f"{action}," not in lower_notes for action in GENERIC_IMPLICIT_ACTIONS):
        # Keep the policy visible in the definition rather than relying only on validator behavior.
        raise SkillDefinitionValidationError(
            f"{path}.learning_evidence.notes: must explicitly state that generic use/inspect/research/monitor are not implicit evidence"
        )

    practice_method_ids = _string_list(
        evidence.get("practice_method_ids", []), f"{path}.learning_evidence.practice_method_ids"
    )
    if "skill_practice" in families and not practice_method_ids:
        raise SkillDefinitionValidationError(f"{path}.learning_evidence.practice_method_ids: required for skill_practice family")
    practice_methods = practice_config.get("methods") or {}
    progression_skills = progression_config.get("skills") or {}
    progression_skill = progression_skills.get(skill_id) if isinstance(progression_skills, dict) else None
    eligible_methods = progression_skill.get("eligible_methods") if isinstance(progression_skill, dict) else {}
    if not isinstance(eligible_methods, dict):
        eligible_methods = {}
    for method_id in practice_method_ids:
        method = practice_methods.get(method_id) if isinstance(practice_methods, dict) else None
        if not isinstance(method, dict):
            raise SkillDefinitionValidationError(
                f"{path}.learning_evidence.practice_method_ids: unknown practice method {method_id!r}"
            )
        relevance = method.get("skill_relevance") or {}
        weight = relevance.get(skill_id) if isinstance(relevance, dict) else None
        if not isinstance(weight, (int, float)) or isinstance(weight, bool) or float(weight) <= 0.0:
            raise SkillDefinitionValidationError(
                f"{path}.learning_evidence.practice_method_ids: method {method_id!r} has no positive {skill_id!r} relevance"
            )
        progression_weight = eligible_methods.get(method_id)
        if not isinstance(progression_weight, (int, float)) or isinstance(progression_weight, bool) or float(progression_weight) <= 0.0:
            raise SkillDefinitionValidationError(
                f"{path}.learning_evidence.practice_method_ids: method {method_id!r} is not whitelisted by Skill Progression for {skill_id!r}"
            )


def _validate_transfer_and_retention(definition: dict[str, Any], path: str) -> None:
    transfer = definition.get("transfer")
    if not isinstance(transfer, list):
        raise SkillDefinitionValidationError(f"{path}.transfer: expected list")
    for index, rule in enumerate(transfer):
        rule_path = f"{path}.transfer[{index}]"
        if not isinstance(rule, dict):
            raise SkillDefinitionValidationError(f"{rule_path}: expected object")
        if rule.get("auto_create_state") is not False:
            raise SkillDefinitionValidationError(f"{rule_path}.auto_create_state: transfer may not fabricate Skill state")
        target = _required_string(rule, "skill_id", rule_path)
        if target == definition.get("skill_id"):
            raise SkillDefinitionValidationError(f"{rule_path}.skill_id: self transfer is not allowed")
    retention = definition.get("retention")
    if not isinstance(retention, dict):
        raise SkillDefinitionValidationError(f"{path}.retention: expected object")
    _required_string(retention, "profile", f"{path}.retention")
    if retention.get("decay_policy") != "deferred" or retention.get("reacquisition_policy") != "deferred":
        raise SkillDefinitionValidationError(f"{path}.retention: v1 retention/reacquisition must remain deferred")


def _validate_presentation_and_provenance(definition: dict[str, Any], path: str) -> None:
    presentation = definition.get("presentation")
    if not isinstance(presentation, dict):
        raise SkillDefinitionValidationError(f"{path}.presentation: expected object")
    _required_string(presentation, "short_description", f"{path}.presentation")
    if not isinstance(presentation.get("order"), int) or isinstance(presentation.get("order"), bool):
        raise SkillDefinitionValidationError(f"{path}.presentation.order: expected integer")
    if presentation.get("sensitivity") not in {"normal", "private", "intimate"}:
        raise SkillDefinitionValidationError(f"{path}.presentation.sensitivity: unsupported value")
    provenance = definition.get("provenance")
    if not isinstance(provenance, dict):
        raise SkillDefinitionValidationError(f"{path}.provenance: expected object")
    _required_string(provenance, "canonical_design", f"{path}.provenance")
    _string_list(provenance.get("research_basis"), f"{path}.provenance.research_basis", nonempty=True)
    compatibility = provenance.get("compatibility")
    if not isinstance(compatibility, dict):
        raise SkillDefinitionValidationError(f"{path}.provenance.compatibility: expected object")
    if compatibility.get("character_skill_key") != definition.get("skill_id"):
        raise SkillDefinitionValidationError(
            f"{path}.provenance.compatibility.character_skill_key: must equal skill_id"
        )
    _string_list(
        compatibility.get("legacy_profile_fields", []),
        f"{path}.provenance.compatibility.legacy_profile_fields",
    )
    _required_string(provenance, "historical_evidence_policy", f"{path}.provenance")
    _required_string(provenance, "migration_notes", f"{path}.provenance")


def validate_skill_definition_config(
    config: dict[str, Any],
    *,
    practice_config: dict[str, Any] | None = None,
    progression_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _required_string(config, "revision", "registry")
    challenge_model = config.get("challenge_model")
    if not isinstance(challenge_model, dict):
        raise SkillDefinitionValidationError("registry.challenge_model: expected object")
    if challenge_model.get("id") != "generic-five-class-v1":
        raise SkillDefinitionValidationError("registry.challenge_model.id: expected generic-five-class-v1")
    classes = _string_list(challenge_model.get("classes"), "registry.challenge_model.classes", nonempty=True)
    if tuple(classes) != CHALLENGE_CLASSES:
        raise SkillDefinitionValidationError(f"registry.challenge_model.classes: expected {CHALLENGE_CLASSES!r}")
    skills = config.get("skills")
    if not isinstance(skills, dict) or not skills:
        raise SkillDefinitionValidationError("registry.skills: expected non-empty object")

    practice = practice_config if practice_config is not None else _load_json(SKILL_PRACTICE_CONFIG_PATH)
    progression = progression_config if progression_config is not None else _load_json(SKILL_PROGRESSION_CONFIG_PATH)

    for skill_id, definition in skills.items():
        path = f"registry.skills.{skill_id}"
        if not isinstance(skill_id, str) or not isinstance(definition, dict):
            raise SkillDefinitionValidationError(f"{path}: invalid Skill definition")
        _walk_forbidden_actor_state(definition, path)
        _validate_identity(skill_id, definition, path)
        _validate_scope(definition, path)
        _validate_relations(skill_id, definition, skills, path)
        _validate_dependencies(definition, path)
        _validate_applications(definition, path)
        _validate_proficiency_anchors(definition, path)
        if definition.get("challenge_model") != challenge_model.get("id"):
            raise SkillDefinitionValidationError(f"{path}.challenge_model: must reference registry challenge model")
        _validate_effects(definition.get("gameplay_effects"), f"{path}.gameplay_effects")
        _validate_learning_evidence(skill_id, definition, path, practice, progression)
        _validate_transfer_and_retention(definition, path)
        _validate_presentation_and_provenance(definition, path)

    _validate_hierarchy_cycles(skills)
    return config


@lru_cache(maxsize=1)
def load_validated_skill_definitions(
    path: str | Path = SKILL_DEFINITIONS_CONFIG_PATH,
) -> dict[str, Any]:
    return validate_skill_definition_config(_load_json(path))


def get_skill_definition(skill_id: str, *, config: dict[str, Any] | None = None) -> dict[str, Any]:
    source = validate_skill_definition_config(config) if config is not None else load_validated_skill_definitions()
    definition = (source.get("skills") or {}).get(skill_id)
    if not isinstance(definition, dict):
        raise KeyError(f"Unknown Skill definition: {skill_id}")
    return definition
