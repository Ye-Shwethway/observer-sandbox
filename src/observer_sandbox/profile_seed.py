from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class ProfileSeedError(RuntimeError):
    pass


MALE_REQUIRED_SEXUAL_PROFILE_FIELDS = (
    "sexual_anatomy.penis_length_in",
    "sexual_anatomy.penis_girth_in",
    "genetics.penis_length_in",
    "genetics.penis_girth_in",
    "sexual_anatomy.baseline_erectile_function",
    "sexual_anatomy.erection_firmness_cap",
)


def load_seed(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _seed_value(seed: dict[str, Any], field_key: str) -> Any:
    record = seed.get("values", {}).get(field_key)
    return None if not isinstance(record, dict) else record.get("value")


def _validate_male_sexual_profile(seed: dict[str, Any]) -> None:
    sex = str(_seed_value(seed, "identity.sex") or "").strip().lower()
    if sex != "male":
        return

    values = seed.get("values", {})
    missing = [field for field in MALE_REQUIRED_SEXUAL_PROFILE_FIELDS if field not in values]
    if missing:
        raise ProfileSeedError(
            "Male canonical profiles require structural and erectile physiology fields: "
            + ", ".join(missing)
        )

    baseline = _seed_value(seed, "sexual_anatomy.baseline_erectile_function")
    cap = _seed_value(seed, "sexual_anatomy.erection_firmness_cap")
    if not isinstance(baseline, (int, float)) or not isinstance(cap, (int, float)):
        raise ProfileSeedError("Male erectile physiology baseline and cap must be numeric")
    baseline_f = float(baseline)
    cap_f = float(cap)
    if not 0.0 <= baseline_f <= 100.0 or not 0.0 <= cap_f <= 100.0:
        raise ProfileSeedError("Male erectile physiology baseline and cap must be within 0..100")
    if baseline_f > cap_f:
        raise ProfileSeedError("Male baseline erectile function cannot exceed erection firmness cap")


def validate_seed(conn: sqlite3.Connection, seed: dict[str, Any]) -> None:
    defined = {
        row[0]
        for row in conn.execute("SELECT field_key FROM profile_field_definitions")
    }
    unknown = sorted(set(seed.get("values", {})) - defined)
    if unknown:
        raise ProfileSeedError(f"Unknown profile fields: {', '.join(unknown)}")
    _validate_male_sexual_profile(seed)


def _skill_progression_active(row: sqlite3.Row | None) -> bool:
    if row is None:
        return False
    metadata = json.loads(row["metadata_json"] or "{}")
    return isinstance(metadata, dict) and bool(metadata.get("progression_active"))


def import_seed(conn: sqlite3.Connection, seed: dict[str, Any]) -> None:
    """Import canonical/static character data without clobbering live simulation state.

    Canonical seeds initialize profile values and may update fields that have not
    been activated by a simulation engine. Once a field's persisted mode is
    ``simulated``, that live engine-owned value is authoritative across ordinary
    re-initialization/deployment and is not reset from the seed.

    Skills follow the same initialization rule. Seed rows may refresh an
    unactivated skill baseline, but a progression-active skill keeps its current
    score/experience/metadata. Extra learned skills that are not present in the
    canonical seed are preserved instead of being deleted on initialization.
    """
    validate_seed(conn, seed)
    entity_id = seed["entity_id"]
    name = seed["name"]
    revision = seed.get("canonical_revision")
    schema_version = int(seed.get("profile_schema_version", 1))

    conn.execute(
        """
        INSERT INTO entities(id, entity_type, name)
        VALUES (?, 'character', ?)
        ON CONFLICT(id) DO UPDATE SET name=excluded.name, updated_at=CURRENT_TIMESTAMP
        """,
        (entity_id, name),
    )
    conn.execute(
        """
        INSERT INTO character_profiles(entity_id, profile_schema_version, canonical_revision, status)
        VALUES (?, ?, ?, 'active')
        ON CONFLICT(entity_id) DO UPDATE SET
            profile_schema_version=excluded.profile_schema_version,
            canonical_revision=excluded.canonical_revision,
            updated_at=CURRENT_TIMESTAMP
        """,
        (entity_id, schema_version, revision),
    )

    for field_key, record in seed.get("values", {}).items():
        value_json = json.dumps(record["value"], ensure_ascii=False)
        old = conn.execute(
            """SELECT value_json,mode,authority,source
            FROM character_profile_values WHERE entity_id=? AND field_key=?""",
            (entity_id, field_key),
        ).fetchone()

        # Re-seeding is initialization, not an engine reset. A domain engine that
        # has activated a field owns the persisted simulated value until an
        # explicit migration/control operation says otherwise.
        if old is not None and old["mode"] == "simulated":
            continue

        if old is not None and old["value_json"] != value_json:
            conn.execute(
                """
                INSERT INTO character_profile_history(
                    entity_id, field_key, old_value_json, new_value_json, mode, authority, reason
                ) VALUES (?, ?, ?, ?, ?, ?, 'canonical seed update')
                """,
                (entity_id, field_key, old["value_json"], value_json, record["mode"], record["authority"]),
            )
        conn.execute(
            """
            INSERT INTO character_profile_values(
                entity_id, field_key, value_json, mode, authority, source, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, 1.0)
            ON CONFLICT(entity_id, field_key) DO UPDATE SET
                value_json=excluded.value_json,
                mode=excluded.mode,
                authority=excluded.authority,
                source=excluded.source,
                confidence=excluded.confidence,
                updated_at=CURRENT_TIMESTAMP
            """,
            (entity_id, field_key, value_json, record["mode"], record["authority"], revision),
        )

    conn.execute("DELETE FROM character_preferences WHERE entity_id=?", (entity_id,))
    for kind, items in seed.get("preferences", {}).items():
        preference_type = "like" if kind == "likes" else "dislike" if kind == "dislikes" else kind
        for subject in items:
            conn.execute(
                "INSERT INTO character_preferences(entity_id, preference_type, subject) VALUES (?, ?, ?)",
                (entity_id, preference_type, subject),
            )

    conn.execute("DELETE FROM character_hobbies WHERE entity_id=?", (entity_id,))
    for hobby in seed.get("hobbies", []):
        conn.execute(
            "INSERT INTO character_hobbies(entity_id, name) VALUES (?, ?)",
            (entity_id, hobby),
        )

    conn.execute("DELETE FROM character_habits WHERE entity_id=?", (entity_id,))
    for habit in seed.get("habits", []):
        conn.execute(
            "INSERT INTO character_habits(entity_id, name) VALUES (?, ?)",
            (entity_id, habit),
        )

    for skill in seed.get("skills", []):
        skill_key = str(skill["key"])
        old_skill = conn.execute(
            """
            SELECT score,tier,experience,metadata_json
            FROM character_skills WHERE entity_id=? AND skill_key=?
            """,
            (entity_id, skill_key),
        ).fetchone()
        if _skill_progression_active(old_skill):
            # Category remains authored classification; progression-owned score,
            # experience and metadata survive ordinary initialization/deployment.
            conn.execute(
                "UPDATE character_skills SET category=? WHERE entity_id=? AND skill_key=?",
                (skill.get("category"), entity_id, skill_key),
            )
            continue
        conn.execute(
            """
            INSERT INTO character_skills(entity_id, skill_key, category, score, tier, experience, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(entity_id, skill_key) DO UPDATE SET
                category=excluded.category,
                score=excluded.score,
                tier=excluded.tier,
                experience=excluded.experience,
                metadata_json=excluded.metadata_json
            """,
            (
                entity_id,
                skill_key,
                skill.get("category"),
                skill.get("score"),
                skill.get("tier"),
                skill.get("experience"),
                json.dumps(skill.get("metadata") or {}, ensure_ascii=False, sort_keys=True),
            ),
        )
    conn.commit()
