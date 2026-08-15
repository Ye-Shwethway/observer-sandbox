from __future__ import annotations

import json

import pytest

from observer_sandbox.cognition_capability_awareness import cognition_capability_awareness
from observer_sandbox.db import connect
from observer_sandbox.profile_observer import profile_section
from observer_sandbox.runtime import initialize
from observer_sandbox.skill_hierarchy import (
    load_skill_hierarchy_config,
    reconcile_skill_hierarchies,
    validate_skill_hierarchy_config,
)


ACTOR = "char_darian"
LEGACY = "weapons"
PARENT = "weapon_mastery"
BLADED = "bladed_weapons"
FIREARMS = "firearms"


def _skill(conn, key: str):
    row = conn.execute(
        """SELECT skill_key,category,score,tier,experience,metadata_json
        FROM character_skills WHERE entity_id=? AND skill_key=?""",
        (ACTOR, key),
    ).fetchone()
    assert row is not None
    return row


def _metadata(row) -> dict:
    return json.loads(row["metadata_json"] or "{}")


def test_hierarchy_contract_declares_derived_parent_and_two_components() -> None:
    source = load_skill_hierarchy_config()
    validate_skill_hierarchy_config(source)
    assert source["revision"] == "skill-hierarchy-v1"
    hierarchy = source["hierarchies"][PARENT]
    assert hierarchy["name"] == "Weapon Mastery"
    assert hierarchy["role"] == "derived_parent"
    assert hierarchy["direct_progression"] is False
    assert hierarchy["direct_application"] is False
    assert hierarchy["component_skills"] == [BLADED, FIREARMS]
    assert hierarchy["aggregation"]["method"] == "mean"
    assert hierarchy["legacy_skill_keys"] == [LEGACY]
    assert hierarchy["migration_policy"]["legacy_baseline_is_distinct_history_evidence"] is False


def test_fresh_initialize_migrates_legacy_weapons_into_components_and_derived_parent(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        parent = _skill(conn, PARENT)
        bladed = _skill(conn, BLADED)
        firearms = _skill(conn, FIREARMS)
        legacy = _skill(conn, LEGACY)

        assert float(parent["score"]) == pytest.approx(87.0)
        assert float(bladed["score"]) == pytest.approx(87.0)
        assert float(firearms["score"]) == pytest.approx(87.0)
        assert float(legacy["score"]) == pytest.approx(87.0)

        parent_meta = _metadata(parent)
        assert parent_meta["hierarchy_role"] == "parent"
        assert parent_meta["component_skills"] == [BLADED, FIREARMS]
        assert parent_meta["derived"] is True
        assert parent_meta["direct_progression"] is False
        assert parent_meta["direct_application"] is False
        assert parent_meta["aggregate_exclude"] is True

        bladed_meta = _metadata(bladed)
        firearms_meta = _metadata(firearms)
        for metadata in (bladed_meta, firearms_meta):
            assert metadata["hierarchy_role"] == "component"
            assert metadata["parent_skill"] == PARENT
            provenance = metadata["baseline_provenance"]
            assert provenance["legacy_skill_key"] == LEGACY
            assert provenance["legacy_score"] == pytest.approx(87.0)
            assert provenance["distinct_historical_specialization_evidence"] is False

        # Bladed progression is now explicitly activated while Firearms remains
        # a learned component with no progression producer yet.
        assert bladed_meta["progression_active"] is True
        assert firearms_meta["progression_active"] is False

        legacy_meta = _metadata(legacy)
        assert legacy_meta["compatibility_projection"] is True
        assert legacy_meta["profile_hidden"] is True
        assert legacy_meta["projection_of"] == PARENT


def test_existing_component_learning_is_preserved_and_parent_rederives(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        row = _skill(conn, BLADED)
        metadata = _metadata(row)
        metadata["progression_active"] = True
        metadata["test_learning_marker"] = "preserve"
        conn.execute(
            """UPDATE character_skills
            SET score=?, experience=?, metadata_json=?
            WHERE entity_id=? AND skill_key=?""",
            (91.0, 3.25, json.dumps(metadata, sort_keys=True), ACTOR, BLADED),
        )
        conn.commit()

    initialize(db)
    with connect(db) as conn:
        bladed = _skill(conn, BLADED)
        firearms = _skill(conn, FIREARMS)
        parent = _skill(conn, PARENT)
        legacy = _skill(conn, LEGACY)
        assert float(bladed["score"]) == pytest.approx(91.0)
        assert float(bladed["experience"]) == pytest.approx(3.25)
        assert _metadata(bladed)["test_learning_marker"] == "preserve"
        assert float(firearms["score"]) == pytest.approx(87.0)
        assert float(parent["score"]) == pytest.approx(89.0)
        assert float(legacy["score"]) == pytest.approx(89.0)

        # Reconciliation itself is idempotent and cannot convert the hidden
        # compatibility projection back into component learning evidence.
        reconcile_skill_hierarchies(conn, ACTOR)
        assert float(_skill(conn, BLADED)["score"]) == pytest.approx(91.0)
        assert float(_skill(conn, PARENT)["score"]) == pytest.approx(89.0)


def test_profile_shows_parent_and_components_but_hides_legacy_projection(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        section = profile_section(conn, ACTOR, "skills", role="owner")
        by_key = {item["key"]: item for item in section["content"] if item["kind"] == "skill"}
        assert LEGACY not in by_key
        assert PARENT in by_key
        assert BLADED in by_key
        assert FIREARMS in by_key

        parent = by_key[PARENT]
        assert parent["label"] == "Weapon Mastery"
        assert parent["mode"] == "derived"
        assert parent["hierarchy_role"] == "parent"
        assert parent["component_skills"] == [BLADED, FIREARMS]
        assert parent["aggregate_exclude"] is True

        assert by_key[BLADED]["parent_skill"] == PARENT
        assert by_key[FIREARMS]["parent_skill"] == PARENT
        assert by_key[BLADED]["mode"] == "learned"
        assert by_key[FIREARMS]["mode"] == "learned"

        # Overall grade uses independently learned leaf Skills and excludes the
        # derived parent so Weapon Mastery is not double-counted.
        included_scores = [
            float(item["score"])
            for item in by_key.values()
            if not item.get("aggregate_exclude") and isinstance(item.get("score"), (int, float))
        ]
        expected = round(sum(included_scores) / len(included_scores), 3)
        assert section["section"]["overall_grade"]["value"] == pytest.approx(expected)


def test_cognition_sees_hierarchy_semantics_not_hidden_legacy_projection(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        awareness = cognition_capability_awareness(conn, ACTOR)
        by_id = {item["skill_id"]: item for item in awareness["skills"]}
        assert LEGACY not in by_id
        assert PARENT in by_id
        assert BLADED in by_id
        assert FIREARMS in by_id
        assert PARENT not in awareness["unresolved_skills"]
        assert BLADED not in awareness["unresolved_skills"]
        assert FIREARMS not in awareness["unresolved_skills"]
        assert by_id[PARENT]["hierarchy"]["derived_parent"] is True
        assert by_id[PARENT]["applications"] == []
        assert by_id[BLADED]["hierarchy"]["parent_skill"] == PARENT
        assert by_id[FIREARMS]["hierarchy"]["parent_skill"] == PARENT


def test_weapon_hierarchy_keeps_parent_and_firearms_non_progressing(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        progression_keys = {
            row["skill_key"]
            for row in conn.execute(
                "SELECT skill_key FROM character_skills WHERE entity_id=? AND json_extract(metadata_json, '$.progression_active') = 1",
                (ACTOR,),
            ).fetchall()
        }
        assert PARENT not in progression_keys
        assert BLADED in progression_keys
        assert FIREARMS not in progression_keys
        assert _metadata(_skill(conn, PARENT))["direct_application"] is False
        assert _skill(conn, PARENT)["experience"] is None
