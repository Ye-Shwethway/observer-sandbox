from __future__ import annotations

import json
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize

CATALOG = Path("config/physical_profile_coverage.v1.json")


def _catalog():
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def test_audit_classifies_core_physical_lifecycle_fields():
    fields = _catalog()["fields"]
    assert fields["body.height_in"] == {
        "classification": "lifecycle_driven",
        "authority": "height_lifecycle_engine",
        "status": "complete",
    }
    assert fields["body.weight_lb"]["classification"] == "simulated_dynamic"
    assert fields["body.bmi"]["classification"] == "derived"
    assert fields["body.hips_in"]["authority"] == "body_progression_engine"
    assert fields["body.abdominal_structure"]["classification"] == "canonical_structural"
    assert fields["body.abdominal_definition"]["classification"] == "derived"
    assert fields["sexual_anatomy.penis_length_in"]["authority"] == "sexual_anatomy_lifecycle_engine"
    assert fields["sexual_anatomy.baseline_erectile_function"]["authority"] == "sexual_physiology_engine"


def test_physical_completion_gate_has_no_unresolved_representation_blockers():
    catalog = _catalog()
    assert catalog["gate"]["required_follow_up_fields"] == []
    assert catalog["gate"]["physical_profile_completion"] is True
    assert catalog["fields"]["appearance.skin_quality"]["classification"] == "intentionally_static"
    assert catalog["fields"]["appearance.skin_quality"]["authority"] == "profile_core"
    assert catalog["fields"]["appearance.pars"]["classification"] == "canonical_structural"
    assert catalog["fields"]["appearance.pars"]["authority"] == "profile_core"
    assert catalog["fields"]["sexual_anatomy.sensitivity"]["status"] == "deferred_context_behavior"


def test_intimate_audit_entries_match_schema_sensitivity(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    fields = _catalog()["fields"]
    intimate = [
        "sexual_anatomy.penis_length_in",
        "sexual_anatomy.penis_girth_in",
        "sexual_anatomy.baseline_erectile_function",
        "sexual_anatomy.erection_firmness_cap",
        "sexual_anatomy.erectile_state",
        "sexual_anatomy.erection_firmness",
        "sexual_anatomy.sensitivity",
        "sexual_state.arousal_level",
    ]
    with connect(db) as conn:
        for key in intimate:
            row = conn.execute(
                "SELECT sensitivity FROM profile_field_definitions WHERE field_key=?",
                (key,),
            ).fetchone()
            assert row is not None, key
            assert row["sensitivity"] == "intimate", key
            assert fields[key]["sensitivity"] == "intimate", key


def test_audit_does_not_mutate_profile_values(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before = conn.execute("SELECT COUNT(*), COALESCE(MAX(updated_at),'') FROM character_profile_values").fetchone()
    _catalog()
    with connect(db) as conn:
        after = conn.execute("SELECT COUNT(*), COALESCE(MAX(updated_at),'') FROM character_profile_values").fetchone()
    assert tuple(before) == tuple(after)
