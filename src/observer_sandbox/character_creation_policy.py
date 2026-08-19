from __future__ import annotations

import sqlite3
from datetime import date
from typing import Any

CREATION_DOMAINS = frozenset({
    "identity",
    "appearance",
    "body",
    "genetics",
    "raps_pa",
    "raps_ma",
    "raps_ia",
    "raps_sa",
    "raps_vc",
    "personality",
    "background",
    "social",
    "sexual_anatomy",
    "training",
})

DENY_PREFIXES = (
    "emotion.",
    "needs.",
    "nutrition.",
    "physiology.",
    "sleep.",
    "goal.",
    "narrative.",
    "sexual_state.",
    "memory.",
)

DENY_EXACT = frozenset({
    "identity.age_years",
    "identity.current_status",
    "identity.zodiac_sign",
    "body.bmi",
    "body.fat_mass_lb",
    "body.lean_mass_lb",
    "body.abdominal_definition",
    "sexual_anatomy.erectile_state",
    "sexual_anatomy.erection_firmness",
    "sexual_anatomy.sensitivity",
    "raps_sa.self_satisfaction_weekly",
    "raps_sa.partnered_satisfaction_weekly",
    "training.accumulated_stimulus",
    "training.adaptation_state",
})

ALLOW_TRAINING_EXACT = frozenset({"training.training_age_years"})

# Source-union compatibility fields can remain registered for old canonical data
# while new Creator Studio output converges on one universal key.
CREATION_FIELD_ALIASES = {
    "raps_pa.practical_skill": "raps_pa.practical_skills",
}

_BODY_GENETIC_MAX = {
    "body.height_in": "genetics.height_max_in",
    "body.neck_in": "genetics.neck_max_in",
    "body.shoulders_in": "genetics.shoulders_max_in",
    "body.chest_in": "genetics.chest_max_in",
    "body.hips_in": "genetics.hips_max_in",
    "body.biceps_relaxed_in": "genetics.biceps_relaxed_max_in",
    "body.biceps_flexed_in": "genetics.biceps_flexed_max_in",
    "body.triceps_in": "genetics.triceps_max_in",
    "body.forearms_in": "genetics.forearms_max_in",
    "body.thighs_in": "genetics.thighs_max_in",
    "body.calves_in": "genetics.calves_max_in",
}


def is_creation_owned_field(field_key: str, domain: str | None = None) -> bool:
    key = str(field_key)
    if key in DENY_EXACT or key.startswith(DENY_PREFIXES):
        return False
    resolved_domain = str(domain or key.split(".", 1)[0])
    if resolved_domain not in CREATION_DOMAINS:
        return False
    if resolved_domain == "training" and key not in ALLOW_TRAINING_EXACT:
        return False
    return True


def creation_field_rows(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    rows = conn.execute(
        "SELECT field_key,domain,data_type,default_mode,default_authority FROM profile_field_definitions ORDER BY field_key"
    ).fetchall()
    return [row for row in rows if is_creation_owned_field(str(row["field_key"]), str(row["domain"]))]


def creation_field_keys(conn: sqlite3.Connection) -> set[str]:
    return {str(row["field_key"]) for row in creation_field_rows(conn)}


def _number(values: dict[str, Any], key: str) -> float | None:
    value = values.get(key)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Character profile field {key} must be numeric")
    return float(value)


def _validate_registered_types(conn: sqlite3.Connection, values: dict[str, Any]) -> None:
    if not values:
        return
    placeholders = ",".join("?" for _ in values)
    rows = conn.execute(
        f"SELECT field_key,data_type FROM profile_field_definitions WHERE field_key IN ({placeholders})",
        tuple(values),
    ).fetchall()
    types = {str(row["field_key"]): str(row["data_type"]) for row in rows}
    for key, value in values.items():
        data_type = types.get(key)
        if data_type is None:
            continue
        if data_type in {"number", "integer"}:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"Character profile field {key} must be numeric")
            if data_type == "integer" and float(value) != int(value):
                raise ValueError(f"Character profile field {key} must be an integer")
        elif data_type in {"text", "date", "datetime"} and not isinstance(value, str):
            raise ValueError(f"Character profile field {key} must be text")
        elif data_type == "boolean" and not isinstance(value, bool):
            raise ValueError(f"Character profile field {key} must be boolean")
        if data_type == "date" and isinstance(value, str):
            try:
                date.fromisoformat(value)
            except ValueError as exc:
                raise ValueError(f"Character profile field {key} must be ISO date YYYY-MM-DD") from exc


def validate_creation_profile_values(conn: sqlite3.Connection, values: dict[str, Any]) -> None:
    """Validate provider-independent universal Character creation semantics."""
    _validate_registered_types(conn, values)

    for key in values:
        if key.startswith(("raps_pa.", "raps_ma.", "raps_ia.", "raps_sa.", "raps_vc.")) and key != "raps_ia.iq":
            value = _number(values, key)
            if value is not None and not 0 <= value <= 100:
                raise ValueError(f"Character profile field {key} must be within 0..100")
    for key in ("social.charisma", "social.emotional_intelligence"):
        value = _number(values, key)
        if value is not None and not 0 <= value <= 100:
            raise ValueError(f"Character profile field {key} must be within 0..100")

    body_fat = _number(values, "body.body_fat_pct")
    if body_fat is not None and not 2 <= body_fat <= 60:
        raise ValueError("body.body_fat_pct is outside a plausible human creation range")

    training_age = _number(values, "training.training_age_years")
    if training_age is not None and not 0 <= training_age <= 80:
        raise ValueError("training.training_age_years is outside a plausible human creation range")

    for key in values:
        if key.startswith(("body.", "genetics.")) and key not in {"body.abdominal_structure", "body.chest_hair"}:
            value = values.get(key)
            if isinstance(value, (int, float)) and not isinstance(value, bool) and float(value) <= 0:
                raise ValueError(f"Character profile field {key} must be positive")

    lean_min = _number(values, "genetics.weight_lean_min_lb")
    lean_max = _number(values, "genetics.weight_lean_max_lb")
    if lean_min is not None and lean_max is not None and lean_min > lean_max:
        raise ValueError("Genetic lean-weight minimum cannot exceed maximum")

    for body_key, genetic_key in _BODY_GENETIC_MAX.items():
        baseline = _number(values, body_key)
        maximum = _number(values, genetic_key)
        if baseline is not None and maximum is not None and baseline > maximum + 1e-9:
            raise ValueError(f"{body_key} cannot exceed {genetic_key}")

    for anatomy_key, genetic_key in (
        ("sexual_anatomy.penis_length_in", "genetics.penis_length_in"),
        ("sexual_anatomy.penis_girth_in", "genetics.penis_girth_in"),
    ):
        anatomy = _number(values, anatomy_key)
        genetic = _number(values, genetic_key)
        if anatomy is not None and genetic is not None and abs(anatomy - genetic) > 0.01:
            raise ValueError(f"{anatomy_key} must match fixed genetic value {genetic_key}")


def _normalize_creation_aliases(values: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(values)
    for alias, canonical in CREATION_FIELD_ALIASES.items():
        if alias not in normalized:
            continue
        alias_value = normalized.pop(alias)
        if canonical in normalized:
            canonical_value = normalized[canonical]
            if canonical_value != alias_value:
                raise ValueError(
                    f"Character profile alias conflict: {alias} and {canonical} must agree"
                )
        else:
            normalized[canonical] = alias_value
    return normalized


def sanitize_creation_profile_values(conn: sqlite3.Connection, values: dict[str, Any]) -> dict[str, Any]:
    allowed = creation_field_keys(conn)
    sanitized = {str(key): value for key, value in values.items() if str(key) in allowed}
    sanitized = _normalize_creation_aliases(sanitized)
    validate_creation_profile_values(conn, sanitized)
    return sanitized


__all__ = [
    "CREATION_DOMAINS",
    "CREATION_FIELD_ALIASES",
    "DENY_EXACT",
    "DENY_PREFIXES",
    "creation_field_keys",
    "creation_field_rows",
    "is_creation_owned_field",
    "sanitize_creation_profile_values",
    "validate_creation_profile_values",
]
