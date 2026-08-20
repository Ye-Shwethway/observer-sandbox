import json

from observer_sandbox.body_grade_target_v2 import preview_body_grade_target
from observer_sandbox.creation_sandbox import ensure_sandbox
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_body_grade_target_v2 import preview_sandbox_body_grade_target
from observer_sandbox.sandbox_representation import set_sandbox_profile_values


def _change(proposal, field_key):
    return next(change for change in proposal["changes"] if change["field_key"] == field_key)


def test_real_body_grade_d_changes_composition_and_definition_coherently(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        proposal = preview_body_grade_target(conn, "char_darian", "D", mode="preserve_shape")
        body_fat = _change(proposal, "body.body_fat_pct")
        weight = _change(proposal, "body.weight_lb")
        assert body_fat["new_value"] > body_fat["old_value"]
        assert weight["new_value"] > weight["old_value"]
        assert proposal["new_aggregate"]["grade"] == "D"
        coherence = proposal["physique_coherence"]
        assert coherence["new_abdominal_definition"] == "limited definition"
        assert coherence["genetic_abdominal_anatomy"] == "preserved"
        assert any(metric["field_key"] == "body.abdominal_definition" and metric["value"] == "limited definition" for metric in proposal["new_metrics"])


def test_sandbox_body_grade_uses_same_coherence_without_real_writes(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        ensure_sandbox(conn, "coherence-v2", label="Coherence v2")
        conn.execute(
            """
            INSERT INTO creation_sandbox_objects(
                object_id,sandbox_id,creation_type,schema_version,lifecycle_status,
                identity_json,properties_json,relationships_json,capabilities_json,provenance_json
            ) VALUES('sbx_coherence','coherence-v2','character',1,'active',?,?,?,?,?)
            """,
            (json.dumps({"name": "Coherence Test"}), "{}", "[]", "[]", json.dumps({"source": "test"})),
        )
        conn.commit()
        keys = (
            "identity.sex",
            "body.height_in",
            "body.weight_lb",
            "body.body_fat_pct",
            "body.neck_in",
            "body.shoulders_in",
            "body.chest_in",
            "body.waist_in",
            "body.hips_in",
            "body.biceps_flexed_in",
            "body.forearms_in",
            "body.thighs_in",
            "body.calves_in",
            "genetics.body_fat_floor_pct",
        )
        values = {}
        for key in keys:
            row = conn.execute(
                "SELECT value_json FROM character_profile_values WHERE entity_id='char_darian' AND field_key=?",
                (key,),
            ).fetchone()
            assert row is not None, key
            values[key] = json.loads(row["value_json"])
        values["body.abdominal_definition"] = "visible four-pack"
        set_sandbox_profile_values(conn, "sbx_coherence", values, authority="creator", source="test")

        real_before = tuple(
            tuple(row)
            for row in conn.execute(
                "SELECT field_key,value_json,mode,authority,source FROM character_profile_values WHERE entity_id='char_darian' ORDER BY field_key"
            ).fetchall()
        )
        proposal = preview_sandbox_body_grade_target(conn, "sbx_coherence", "D", mode="preserve_shape")
        assert proposal["new_aggregate"]["grade"] == "D"
        assert _change(proposal, "body.body_fat_pct")["new_value"] > _change(proposal, "body.body_fat_pct")["old_value"]
        definition = _change(proposal, "body.abdominal_definition")
        assert definition["old_value"] == "visible four-pack"
        assert definition["new_value"] == "limited definition"
        assert proposal["physique_coherence"]["genetic_abdominal_anatomy"] == "preserved"
        real_after = tuple(
            tuple(row)
            for row in conn.execute(
                "SELECT field_key,value_json,mode,authority,source FROM character_profile_values WHERE entity_id='char_darian' ORDER BY field_key"
            ).fetchall()
        )
        assert real_after == real_before
