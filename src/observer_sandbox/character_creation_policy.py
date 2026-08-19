from __future__ import annotations

import sqlite3
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


def sanitize_creation_profile_values(conn: sqlite3.Connection, values: dict[str, Any]) -> dict[str, Any]:
    allowed = creation_field_keys(conn)
    return {str(key): value for key, value in values.items() if str(key) in allowed}


__all__ = [
    "CREATION_DOMAINS",
    "DENY_EXACT",
    "DENY_PREFIXES",
    "creation_field_keys",
    "creation_field_rows",
    "is_creation_owned_field",
    "sanitize_creation_profile_values",
]
