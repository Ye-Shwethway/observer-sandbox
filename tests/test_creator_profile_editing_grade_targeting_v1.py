import json

import pytest

from observer_sandbox.character_memory import create_semantic_memory
from observer_sandbox.creator_profile_edit import (
    CreatorProfileEditError,
    apply_profile_proposal,
    preview_profile_edit,
    preview_section_grade_target,
)
from observer_sandbox.db import connect
from observer_sandbox.profile_observer import profile_section
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import runtime_value, set_runtime_value


def _value(conn, key):
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id='char_darian' AND field_key=?",
        (key,),
    ).fetchone()
    return json.loads(row["value_json"])


def test_creator_edit_changes_raw_value_and_read_time_grade_without_persisted_grade(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        proposal = preview_profile_edit(conn, "char_darian", "raps_pa.strength", 68)
        assert proposal["changes"][0]["old_grade"]["grade"] == "S"
        assert proposal["changes"][0]["new_grade"]["grade"] == "B"
        result = apply_profile_proposal(conn, proposal, requested_by="test:creator")
        assert result["ok"] is True
        assert _value(conn, "raps_pa.strength") == 68.0
        attributes = profile_section(conn, "char_darian", "attributes", role="owner")
        strength = next(item for item in attributes["content"] if item.get("field_key") == "raps_pa.strength")
        assert strength["grade"]["grade"] == "B"
        assert all(row[1] != "grade" for row in conn.execute("PRAGMA table_info(character_profile_values)"))
        history = conn.execute(
            "SELECT reason,old_value_json,new_value_json FROM character_profile_history WHERE entity_id='char_darian' AND field_key='raps_pa.strength' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        assert history is not None
        assert "creator profile" in history["reason"]


def test_physical_attributes_can_be_retargeted_to_b_preserving_shape(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        proposal = preview_section_grade_target(conn, "char_darian", "physical", "B", mode="preserve_shape")
        assert proposal["new_aggregate"]["grade"] == "B"
        assert proposal["new_aggregate"]["value"] == pytest.approx(67.5, abs=0.01)
        old_spread = max(c["old_value"] for c in proposal["changes"]) - min(c["old_value"] for c in proposal["changes"])
        new_spread = max(c["new_value"] for c in proposal["changes"]) - min(c["new_value"] for c in proposal["changes"])
        assert new_spread == pytest.approx(old_spread, abs=0.01)
        apply_profile_proposal(conn, proposal, requested_by="test:creator")
        attributes = profile_section(conn, "char_darian", "attributes", role="owner")
        assert attributes["section"]["group_grades"]["raps_pa"]["grade"] == "B"


def test_normalize_mode_targets_monotonic_group_and_skill_edit_regrades(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        proposal = preview_section_grade_target(conn, "char_darian", "physical", "C", mode="normalize")
        assert proposal["new_aggregate"]["grade"] == "C"
        assert len({round(c["new_value"], 6) for c in proposal["changes"]}) == 1
        apply_profile_proposal(conn, proposal, requested_by="test:creator")

        skill_row = conn.execute(
            "SELECT score FROM character_skills WHERE entity_id='char_darian' AND skill_key='hand_to_hand_combat'"
        ).fetchone()
        old = float(skill_row["score"])
        skill_proposal = {
            "proposal_version": 1,
            "kind": "field_edit",
            "character_id": "char_darian",
            "mutation_class": "creator_override",
            "changes": [{
                "store": "skill",
                "field_key": "skill:hand_to_hand_combat",
                "label": "Hand To Hand Combat",
                "old_value": old,
                "new_value": 68.0,
            }],
        }
        apply_profile_proposal(conn, skill_proposal, requested_by="test:creator")
        skills = profile_section(conn, "char_darian", "skills", role="owner")
        hand = next(item for item in skills["content"] if item["key"] == "hand_to_hand_combat")
        assert hand["score"] == 68.0
        assert hand["grade"]["grade"] == "B"
        metadata = conn.execute(
            "SELECT metadata_json FROM character_skills WHERE entity_id='char_darian' AND skill_key='hand_to_hand_combat'"
        ).fetchone()
        assert json.loads(metadata["metadata_json"])["creator_reanchored"] is True


def test_invalid_value_and_stale_preview_fail_without_partial_mutation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before = _value(conn, "raps_pa.strength")
        with pytest.raises(ValueError):
            preview_profile_edit(conn, "char_darian", "raps_pa.strength", 101)
        assert _value(conn, "raps_pa.strength") == before

        proposal = preview_profile_edit(conn, "char_darian", "raps_pa.strength", 70)
        conn.execute(
            "UPDATE character_profile_values SET value_json='69' WHERE entity_id='char_darian' AND field_key='raps_pa.strength'"
        )
        conn.commit()
        with pytest.raises(CreatorProfileEditError, match="stale"):
            apply_profile_proposal(conn, proposal, requested_by="test:creator")
        assert _value(conn, "raps_pa.strength") == 69


def test_profile_correction_retires_only_explicit_profile_derived_self_knowledge_and_reanchors_ledgers(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        sim_time = runtime_value(conn, "sim_time", None)
        stale = create_semantic_memory(
            conn,
            character_id="char_darian",
            summary="My represented strength is 90",
            content={"profile_field_key": "raps_pa.strength", "value": 90},
            sim_time=sim_time,
            source_type="profile_self_knowledge",
        )
        unrelated = create_semantic_memory(
            conn,
            character_id="char_darian",
            summary="A separate fact",
            content={"knowledge_kind": "unrelated"},
            sim_time=sim_time,
        )
        baseline_key = "telegram_stat_notification_baseline:123:char_darian"
        set_runtime_value(conn, baseline_key, {"raps_pa.strength": {"value": 90.0}})
        conn.commit()

        proposal = preview_profile_edit(conn, "char_darian", "raps_pa.strength", 72)
        result = apply_profile_proposal(conn, proposal, requested_by="test:creator")
        assert stale in result["retired_profile_self_knowledge"]
        statuses = {
            row["memory_id"]: row["status"]
            for row in conn.execute(
                "SELECT memory_id,status FROM character_memories WHERE memory_id IN (?,?)",
                (stale, unrelated),
            )
        }
        assert statuses[stale] == "retired"
        assert statuses[unrelated] == "active"
        baseline = runtime_value(conn, baseline_key, {})
        assert baseline["raps_pa.strength"]["value"] == 72.0
        display = runtime_value(conn, "profile_change_display_ledger:char_darian", {})
        assert display.get("display") == {}


def test_body_composite_is_not_inverse_targeted_in_v1(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        with pytest.raises(CreatorProfileEditError, match="Unsupported inverse-grade group"):
            preview_section_grade_target(conn, "char_darian", "body", "B")
