from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .creator_authority import ordinary_seed_may_replace


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


BASELINE_SOURCE = "canonical_seed"


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
    metadata_active = isinstance(metadata, dict) and bool(metadata.get("progression_active"))
    return metadata_active or row["experience"] is not None


def _metadata_dict(raw: str | None) -> dict[str, Any]:
    parsed = json.loads(raw or "{}")
    return parsed if isinstance(parsed, dict) else {}


def _mark_canonical_baseline(metadata: dict[str, Any], revision: str | None) -> dict[str, Any]:
    merged = dict(metadata)
    merged["canonical_baseline"] = True
    merged["canonical_source"] = BASELINE_SOURCE
    if revision:
        merged["canonical_revision"] = revision
    return merged


def _seed_preferences(
    conn: sqlite3.Connection,
    *,
    entity_id: str,
    seed: dict[str, Any],
    revision: str | None,
) -> None:
    for kind, items in seed.get("preferences", {}).items():
        preference_type = "like" if kind == "likes" else "dislike" if kind == "dislikes" else kind
        for subject in items:
            row = conn.execute(
                """
                SELECT id,metadata_json FROM character_preferences
                WHERE entity_id=? AND preference_type=? AND subject=?
                """,
                (entity_id, preference_type, subject),
            ).fetchone()
            if row is None:
                metadata = _mark_canonical_baseline({}, revision)
                conn.execute(
                    """
                    INSERT INTO character_preferences(entity_id,preference_type,subject,metadata_json)
                    VALUES(?,?,?,?)
                    """,
                    (
                        entity_id,
                        preference_type,
                        subject,
                        json.dumps(metadata, ensure_ascii=False, sort_keys=True),
                    ),
                )
                continue
            metadata = _mark_canonical_baseline(_metadata_dict(row["metadata_json"]), revision)
            conn.execute(
                "UPDATE character_preferences SET metadata_json=? WHERE id=?",
                (json.dumps(metadata, ensure_ascii=False, sort_keys=True), row["id"]),
            )


def _seed_hobbies(
    conn: sqlite3.Connection,
    *,
    entity_id: str,
    seed: dict[str, Any],
    revision: str | None,
) -> None:
    for hobby in seed.get("hobbies", []):
        row = conn.execute(
            "SELECT id,metadata_json FROM character_hobbies WHERE entity_id=? AND name=?",
            (entity_id, hobby),
        ).fetchone()
        if row is None:
            metadata = _mark_canonical_baseline({}, revision)
            conn.execute(
                "INSERT INTO character_hobbies(entity_id,name,metadata_json) VALUES(?,?,?)",
                (entity_id, hobby, json.dumps(metadata, ensure_ascii=False, sort_keys=True)),
            )
            continue
        metadata = _mark_canonical_baseline(_metadata_dict(row["metadata_json"]), revision)
        conn.execute(
            "UPDATE character_hobbies SET metadata_json=? WHERE id=?",
            (json.dumps(metadata, ensure_ascii=False, sort_keys=True), row["id"]),
        )


def _seed_habits(
    conn: sqlite3.Connection,
    *,
    entity_id: str,
    seed: dict[str, Any],
    revision: str | None,
) -> None:
    for habit in seed.get("habits", []):
        row = conn.execute(
            "SELECT id,metadata_json FROM character_habits WHERE entity_id=? AND name=?",
            (entity_id, habit),
        ).fetchone()
        if row is None:
            metadata = _mark_canonical_baseline({}, revision)
            conn.execute(
                "INSERT INTO character_habits(entity_id,name,metadata_json) VALUES(?,?,?)",
                (entity_id, habit, json.dumps(metadata, ensure_ascii=False, sort_keys=True)),
            )
            continue
        metadata = _mark_canonical_baseline(_metadata_dict(row["metadata_json"]), revision)
        conn.execute(
            "UPDATE character_habits SET metadata_json=? WHERE id=?",
            (json.dumps(metadata, ensure_ascii=False, sort_keys=True), row["id"]),
        )


def import_seed(conn: sqlite3.Connection, seed: dict[str, Any]) -> None:
    """Import canonical/static character data without clobbering stronger live authority.

    Ordinary canonical seed refreshes may initialize missing state or refresh an
    unclaimed static baseline. Simulated live state and explicit Creator-owned
    state outrank seed/default state and survive ordinary re-initialization.

    Skills follow their existing progression-active preservation rule. Adaptive
    preference/hobby/habit rows are ensured as baselines without deleting learned
    additions or resetting their dynamic evidence metadata.
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

        if not ordinary_seed_may_replace(
            existing=old is not None,
            mode=None if old is None else old["mode"],
            authority=None if old is None else old["authority"],
            source=None if old is None else old["source"],
        ):
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

    _seed_preferences(conn, entity_id=entity_id, seed=seed, revision=revision)
    _seed_hobbies(conn, entity_id=entity_id, seed=seed, revision=revision)
    _seed_habits(conn, entity_id=entity_id, seed=seed, revision=revision)

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
