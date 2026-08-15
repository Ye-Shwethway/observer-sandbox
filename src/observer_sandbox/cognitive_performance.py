from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from .profile_schema import FIELDS
from .skill_application_requirements import get_executable_skill_application


REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "config" / "cognitive_performance_modifiers.v1.json"
ALLOWED_STATUSES = {"active", "experimental", "deprecated"}
ALLOWED_DIMENSIONS = {"reasoning_quality", "precision", "adaptation"}
FORBIDDEN_OUTCOME_EFFECTS = {"feasibility", "available_action_variants"}


class CognitivePerformanceValidationError(ValueError):
    pass


@dataclass(frozen=True)
class CognitivePerformanceDimension:
    dimension: str
    multiplier: float
    raw_effect: float
    max_abs_effect: float
    outcome_effects: tuple[str, ...]
    factor_contributions: tuple[dict[str, Any], ...]
    missing_inputs: tuple[str, ...]


@dataclass(frozen=True)
class CognitivePerformanceAssessment:
    contract_id: str
    skill_id: str
    application_id: str
    dimensions: tuple[CognitivePerformanceDimension, ...]
    principles: tuple[str, ...]

    def multiplier(self, dimension: str) -> float:
        for item in self.dimensions:
            if item.dimension == dimension:
                return item.multiplier
        raise KeyError(dimension)


def _load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CognitivePerformanceValidationError(f"{path}: expected object root")
    return value


@lru_cache(maxsize=1)
def load_cognitive_performance_config(path: str | Path = CONFIG_PATH) -> dict[str, Any]:
    return _load_json(path)


def _required_string(value: dict[str, Any], key: str, path: str) -> str:
    result = value.get(key)
    if not isinstance(result, str) or not result.strip():
        raise CognitivePerformanceValidationError(f"{path}.{key}: required non-empty string")
    return result.strip()


def validate_cognitive_performance_config(config: dict[str, Any] | None = None) -> dict[str, Any]:
    source = config if config is not None else load_cognitive_performance_config()
    revision = source.get("revision")
    if not isinstance(revision, str) or not revision.strip():
        raise CognitivePerformanceValidationError("revision: required non-empty string")

    profiles = source.get("normalization_profiles")
    if not isinstance(profiles, dict) or not profiles:
        raise CognitivePerformanceValidationError("normalization_profiles: expected non-empty object")
    for profile_id, profile in profiles.items():
        path = f"normalization_profiles.{profile_id}"
        if not isinstance(profile, dict):
            raise CognitivePerformanceValidationError(f"{path}: expected object")
        if profile.get("kind") != "centered_linear":
            raise CognitivePerformanceValidationError(f"{path}.kind: v1 requires centered_linear")
        for key in ("center", "span", "clamp_min", "clamp_max"):
            value = profile.get(key)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise CognitivePerformanceValidationError(f"{path}.{key}: expected number")
        if float(profile["span"]) <= 0.0:
            raise CognitivePerformanceValidationError(f"{path}.span: must be positive")
        if float(profile["clamp_min"]) >= float(profile["clamp_max"]):
            raise CognitivePerformanceValidationError(f"{path}: invalid clamp range")
        _required_string(profile, "note", path)

    allowed_fields = {field.key for field in FIELDS}
    contracts = source.get("contracts")
    if not isinstance(contracts, dict) or not contracts:
        raise CognitivePerformanceValidationError("contracts: expected non-empty object")

    for registry_key, contract in contracts.items():
        path = f"contracts.{registry_key}"
        if not isinstance(contract, dict):
            raise CognitivePerformanceValidationError(f"{path}: expected object")
        skill_id = _required_string(contract, "skill_id", path)
        application_id = _required_string(contract, "application_id", path)
        if registry_key != f"{skill_id}.{application_id}":
            raise CognitivePerformanceValidationError(
                f"{path}: registry key must equal skill_id.application_id"
            )
        _required_string(contract, "contract_id", path)
        if _required_string(contract, "status", path) not in ALLOWED_STATUSES:
            raise CognitivePerformanceValidationError(f"{path}.status: unsupported")
        if contract.get("feasibility_policy") != "never_modify":
            raise CognitivePerformanceValidationError(
                f"{path}.feasibility_policy: v1 must never modify feasibility"
            )
        if contract.get("missing_input_policy") != "neutral_zero_no_renormalization":
            raise CognitivePerformanceValidationError(
                f"{path}.missing_input_policy: unsupported v1 policy"
            )
        if contract.get("knowledge_policy") != "do_not_infer_or_create_knowledge":
            raise CognitivePerformanceValidationError(
                f"{path}.knowledge_policy: v1 must not infer Knowledge"
            )

        try:
            _definition, application = get_executable_skill_application(skill_id, application_id)
        except (KeyError, ValueError) as exc:
            raise CognitivePerformanceValidationError(
                f"{path}: unknown executable Skill application"
            ) from exc
        allowed_outcomes = set(application.get("gameplay_effects") or [])

        dimensions = contract.get("dimensions")
        if not isinstance(dimensions, dict) or not dimensions:
            raise CognitivePerformanceValidationError(f"{path}.dimensions: expected non-empty object")
        unknown_dimensions = sorted(set(dimensions) - ALLOWED_DIMENSIONS)
        if unknown_dimensions:
            raise CognitivePerformanceValidationError(
                f"{path}.dimensions: unsupported {unknown_dimensions!r}"
            )
        for dimension_id, dimension in dimensions.items():
            dpath = f"{path}.dimensions.{dimension_id}"
            if not isinstance(dimension, dict):
                raise CognitivePerformanceValidationError(f"{dpath}: expected object")
            if float(dimension.get("base_multiplier", 0.0)) != 1.0:
                raise CognitivePerformanceValidationError(
                    f"{dpath}.base_multiplier: v1 baseline must be exactly 1.0"
                )
            max_effect = dimension.get("max_abs_effect")
            if (
                isinstance(max_effect, bool)
                or not isinstance(max_effect, (int, float))
                or not 0.0 < float(max_effect) <= 0.15
            ):
                raise CognitivePerformanceValidationError(
                    f"{dpath}.max_abs_effect: expected value in (0,0.15]"
                )
            effects = dimension.get("outcome_effects")
            if not isinstance(effects, list) or not effects:
                raise CognitivePerformanceValidationError(
                    f"{dpath}.outcome_effects: expected non-empty list"
                )
            if any(not isinstance(item, str) or not item for item in effects):
                raise CognitivePerformanceValidationError(
                    f"{dpath}.outcome_effects: expected strings"
                )
            effect_set = set(effects)
            if effect_set & FORBIDDEN_OUTCOME_EFFECTS:
                raise CognitivePerformanceValidationError(
                    f"{dpath}.outcome_effects: cannot modify feasibility/action availability"
                )
            if not effect_set.issubset(allowed_outcomes):
                raise CognitivePerformanceValidationError(
                    f"{dpath}.outcome_effects: outside Skill application contract"
                )

            factors = dimension.get("factors")
            if not isinstance(factors, list) or not factors:
                raise CognitivePerformanceValidationError(f"{dpath}.factors: expected non-empty list")
            seen: set[str] = set()
            total_weight = 0.0
            for index, factor in enumerate(factors):
                fpath = f"{dpath}.factors[{index}]"
                if not isinstance(factor, dict):
                    raise CognitivePerformanceValidationError(f"{fpath}: expected object")
                field_key = _required_string(factor, "field_key", fpath)
                if field_key not in allowed_fields:
                    raise CognitivePerformanceValidationError(
                        f"{fpath}.field_key: unknown profile field {field_key!r}"
                    )
                if field_key in seen:
                    raise CognitivePerformanceValidationError(
                        f"{fpath}.field_key: duplicate {field_key!r}"
                    )
                seen.add(field_key)
                normalization = _required_string(factor, "normalization", fpath)
                if normalization not in profiles:
                    raise CognitivePerformanceValidationError(
                        f"{fpath}.normalization: unknown profile {normalization!r}"
                    )
                weight = factor.get("weight")
                if (
                    isinstance(weight, bool)
                    or not isinstance(weight, (int, float))
                    or not 0.0 < float(weight) <= 1.0
                ):
                    raise CognitivePerformanceValidationError(
                        f"{fpath}.weight: expected value in (0,1]"
                    )
                total_weight += float(weight)
            if total_weight > 1.0000001:
                raise CognitivePerformanceValidationError(
                    f"{dpath}.factors: total weight must not exceed 1.0"
                )
    return source


def _normalize(value: float, profile: dict[str, Any]) -> float:
    center = float(profile["center"])
    span = float(profile["span"])
    normalized = (float(value) - center) / span
    return max(float(profile["clamp_min"]), min(float(profile["clamp_max"]), normalized))


def assess_cognitive_performance(
    skill_id: str,
    application_id: str,
    *,
    factor_values: dict[str, float | int | None],
    config: dict[str, Any] | None = None,
) -> CognitivePerformanceAssessment:
    source = validate_cognitive_performance_config(config)
    contract = (source.get("contracts") or {}).get(f"{skill_id}.{application_id}")
    if not isinstance(contract, dict):
        raise KeyError(f"No cognitive performance contract for {skill_id}.{application_id}")
    if contract.get("status") == "deprecated":
        raise CognitivePerformanceValidationError("Deprecated cognitive performance contract is not executable")

    profiles = source["normalization_profiles"]
    resolved: list[CognitivePerformanceDimension] = []
    for dimension_id, dimension in contract["dimensions"].items():
        weighted_sum = 0.0
        contributions: list[dict[str, Any]] = []
        missing: list[str] = []
        for factor in dimension["factors"]:
            field_key = str(factor["field_key"])
            raw = factor_values.get(field_key)
            if raw is None:
                missing.append(field_key)
                contributions.append(
                    {
                        "field_key": field_key,
                        "raw_value": None,
                        "normalized": 0.0,
                        "weight": float(factor["weight"]),
                        "weighted_contribution": 0.0,
                    }
                )
                continue
            if isinstance(raw, bool) or not isinstance(raw, (int, float)):
                raise CognitivePerformanceValidationError(
                    f"Factor {field_key!r} must be numeric or None"
                )
            normalized = _normalize(float(raw), profiles[factor["normalization"]])
            weighted = normalized * float(factor["weight"])
            weighted_sum += weighted
            contributions.append(
                {
                    "field_key": field_key,
                    "raw_value": float(raw),
                    "normalized": round(normalized, 6),
                    "weight": float(factor["weight"]),
                    "weighted_contribution": round(weighted, 6),
                }
            )
        max_effect = float(dimension["max_abs_effect"])
        effect = max(-max_effect, min(max_effect, weighted_sum * max_effect))
        resolved.append(
            CognitivePerformanceDimension(
                dimension=str(dimension_id),
                multiplier=round(1.0 + effect, 6),
                raw_effect=round(effect, 6),
                max_abs_effect=max_effect,
                outcome_effects=tuple(str(item) for item in dimension["outcome_effects"]),
                factor_contributions=tuple(contributions),
                missing_inputs=tuple(missing),
            )
        )

    return CognitivePerformanceAssessment(
        contract_id=str(contract["contract_id"]),
        skill_id=skill_id,
        application_id=application_id,
        dimensions=tuple(resolved),
        principles=(
            "These multipliers never modify Skill/task feasibility.",
            "IQ and supporting Attributes do not create learned Skill proficiency or Knowledge.",
            "Missing factor values contribute neutral zero and weights are never renormalized.",
            "Final task outcomes remain owned by a deterministic represented-task outcome resolver.",
        ),
    )


def assess_actor_cognitive_performance(
    conn: sqlite3.Connection,
    actor_id: str,
    skill_id: str,
    application_id: str,
    *,
    config: dict[str, Any] | None = None,
) -> CognitivePerformanceAssessment:
    source = validate_cognitive_performance_config(config)
    contract = (source.get("contracts") or {}).get(f"{skill_id}.{application_id}")
    if not isinstance(contract, dict):
        raise KeyError(f"No cognitive performance contract for {skill_id}.{application_id}")

    field_keys = sorted(
        {
            str(factor["field_key"])
            for dimension in contract["dimensions"].values()
            for factor in dimension["factors"]
        }
    )
    placeholders = ",".join("?" for _ in field_keys)
    rows = conn.execute(
        f"""
        SELECT field_key,value_json
        FROM character_profile_values
        WHERE entity_id=? AND field_key IN ({placeholders})
        """,
        (actor_id, *field_keys),
    ).fetchall()
    values: dict[str, float | None] = {field_key: None for field_key in field_keys}
    for row in rows:
        field_key = str(row["field_key"])
        try:
            raw = json.loads(row["value_json"])
        except (TypeError, json.JSONDecodeError) as exc:
            raise CognitivePerformanceValidationError(
                f"Actor {actor_id!r} profile field {field_key!r} has invalid JSON"
            ) from exc
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            raise CognitivePerformanceValidationError(
                f"Actor {actor_id!r} profile field {field_key!r} must be numeric"
            )
        values[field_key] = float(raw)

    return assess_cognitive_performance(
        skill_id,
        application_id,
        factor_values=values,
        config=source,
    )
