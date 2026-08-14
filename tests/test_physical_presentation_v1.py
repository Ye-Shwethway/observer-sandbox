from __future__ import annotations

import json

from observer_sandbox.db import connect
from observer_sandbox.physical_presentation import (
    abdominal_definition_from_composition,
    refresh_physical_presentation,
)
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot


def test_definition_is_relative_to_authored_body_fat_floor():
    assert abdominal_definition_from_composition(9.0, 8.0) == "peak definition"
    assert abdominal_definition_from_composition(11.0, 8.0) == "high definition"
    assert abdominal_definition_from_composition(14.0, 8.0) == "moderate definition"
    assert abdominal_definition_from_composition(18.0, 8.0) == "limited definition"


def test_refresh_replaces_stale_definition_without_touching_structure(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, "char_darian")
        structure_before = conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id='char_darian' AND field_key='body.abdominal_structure'"
        ).fetchone()["value_json"]
        result = refresh_physical_presentation(conn, "char_darian", as_of_sim_time=str(state["sim_time"]))
        definition = conn.execute(
            "SELECT value_json,mode,authority,source FROM character_profile_values WHERE entity_id='char_darian' AND field_key='body.abdominal_definition'"
        ).fetchone()
        structure_after = conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id='char_darian' AND field_key='body.abdominal_structure'"
        ).fetchone()["value_json"]

    assert result["abdominal_definition"] == "peak definition"
    assert json.loads(definition["value_json"]) == "peak definition"
    assert definition["mode"] == "derived"
    assert definition["authority"] == "appearance_engine"
    assert definition["source"] == "physical-presentation-v1"
    assert structure_before == structure_after == '"rare 8-pack configuration"'


def test_definition_changes_when_authoritative_body_fat_changes(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, "char_darian")
        refresh_physical_presentation(conn, "char_darian", as_of_sim_time=str(state["sim_time"]))
        conn.execute(
            "UPDATE character_profile_values SET value_json='14.0' WHERE entity_id='char_darian' AND field_key='body.body_fat_pct'"
        )
        conn.commit()
        result = refresh_physical_presentation(conn, "char_darian", as_of_sim_time=str(state["sim_time"]))

    assert result["abdominal_definition"] == "moderate definition"


def test_schema_semantics_are_truthful_after_closure(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        rows = {
            row["field_key"]: row
            for row in conn.execute(
                "SELECT field_key,label,default_mode,default_authority FROM profile_field_definitions WHERE field_key IN ('body.abdominal_structure','body.abdominal_definition','appearance.skin_quality','appearance.pars','sexual_anatomy.sensitivity')"
            ).fetchall()
        }

    assert rows["body.abdominal_structure"]["default_mode"] == "canonical"
    assert rows["body.abdominal_definition"]["default_mode"] == "derived"
    assert rows["body.abdominal_definition"]["default_authority"] == "appearance_engine"
    assert rows["appearance.skin_quality"]["default_mode"] == "canonical"
    assert rows["appearance.skin_quality"]["default_authority"] == "profile_core"
    assert rows["appearance.pars"]["default_mode"] == "canonical"
    assert rows["appearance.pars"]["default_authority"] == "profile_core"
    assert rows["sexual_anatomy.sensitivity"]["default_authority"] == "sexual_physiology_engine"
