from __future__ import annotations

import json

import pytest

from observer_sandbox.controlled_h2h_runtime import (
    CONSENT_CAPABILITY,
    GRAPPLE_APPLICATION_ID,
    GRAPPLE_TASK_ID,
    SKILL_ID,
    SPAR_ACTION,
    controlled_h2h_outcome,
)
from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot
from observer_sandbox.skill_progression import maybe_settle_skill_progression


ROOM = "loc_thorne_estate_training_hall"
SESSION = "obj_test_controlled_h2h_grappling_session"
PARTNER = "char_test_controlled_h2h_grappling_partner"


def _prepare(conn) -> None:
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id) VALUES(?,?,?,?,?)",
        (
            SESSION,
            "object",
            "Controlled Grappling Session",
            json.dumps(["spar", "controlled_grappling_session"]),
            "represented_task:h2h_controlled_grappling_session_v1",
        ),
    )
    conn.execute(
        "INSERT INTO relations(source_id,relation_type,target_id) VALUES(?,?,?)",
        (ROOM, "contains", SESSION),
    )
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json,definition_id) VALUES(?,?,?,?,?,?)",
        (
            PARTNER,
            "character",
            "Controlled Grappling Partner",
            "{}",
            json.dumps([CONSENT_CAPABILITY]),
            "test:controlled_grappling_partner_v1",
        ),
    )
    set_dynamic_location(conn, PARTNER, ROOM)
    set_dynamic_location(conn, "char_darian", ROOM)
    conn.commit()


def test_exact_grappling_session_selects_grapple_application_and_modifier_contract(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        outcome = controlled_h2h_outcome(conn, "char_darian", SESSION, (PARTNER,))

        assert outcome["task"]["task_id"] == GRAPPLE_TASK_ID
        assert outcome["capability"]["skill_id"] == SKILL_ID
        assert outcome["capability"]["application_id"] == GRAPPLE_APPLICATION_ID
        assert outcome["capability"]["skill_score"] == pytest.approx(90.0)
        assert outcome["capability"]["proficiency_grade"] == "S"
        assert outcome["performance"]["contract_id"] == "h2h_controlled_grapple_performance_v1"
        assert outcome["authorization"]["participant_id"] == PARTNER
        assert outcome["consequence"] == {
            "mode": "scored_positional_control_only",
            "injury_state_mutated": False,
            "target_state_mutated": False,
        }
        factors = {
            factor["field_key"]
            for dimension in outcome["performance"]["dimensions"]
            for factor in dimension["factor_contributions"]
        }
        assert factors == {"raps_pa.reflexes", "raps_pa.agility", "raps_ma.focus"}
        assert "raps_ia.iq" not in factors
        assert "raps_pa.combat_skill" not in factors
        assert outcome["learning_evidence"] is False


def test_generic_spar_action_exposes_exact_grappling_session_without_new_action_engine(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        option = next(
            item
            for item in action_options(conn, "char_darian")
            if item["action"] == SPAR_ACTION and item["target"] == SESSION
        )
        assert option["target_name"] == "Controlled Grappling Session"
        definitions = conn.execute(
            "SELECT action_type FROM action_definitions WHERE action_type IN ('spar','grapple') ORDER BY action_type"
        ).fetchall()
        assert [row["action_type"] for row in definitions] == [SPAR_ACTION]


def test_completed_grappling_spar_records_application_only_without_restraint_injury_or_xp(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        before_skill = tuple(
            conn.execute(
                "SELECT score,experience FROM character_skills WHERE entity_id='char_darian' AND skill_key=?",
                (SKILL_ID,),
            ).fetchone()
        )
        before_partner_state = conn.execute(
            "SELECT state_json FROM entities WHERE id=?",
            (PARTNER,),
        ).fetchone()[0]

        action_id = "controlled-h2h-grapple-v1-action"
        apply_action(
            conn,
            Action(
                SPAR_ACTION,
                10,
                SESSION,
                "controlled positional grappling exchange",
                participants=(PARTNER,),
            ),
            "char_darian",
            action_id=action_id,
        )

        instance = conn.execute(
            "SELECT status,outcome_json,participants_json FROM action_instances WHERE id=?",
            (action_id,),
        ).fetchone()
        assert instance["status"] == "completed"
        assert json.loads(instance["participants_json"]) == [PARTNER]
        outcome = json.loads(instance["outcome_json"])
        represented = outcome["represented_skill_task"]
        evidence = outcome["skill_application"]
        assert represented["task"]["task_id"] == GRAPPLE_TASK_ID
        assert represented["consequence"]["mode"] == "scored_positional_control_only"
        assert represented["consequence"]["injury_state_mutated"] is False
        assert represented["consequence"]["target_state_mutated"] is False
        assert evidence["application_id"] == GRAPPLE_APPLICATION_ID
        assert evidence["learning_evidence"] is False
        assert evidence["participant_id"] == PARTNER

        events = conn.execute(
            "SELECT id,event_type,payload_json,caused_by_event_id FROM events WHERE action_id=? ORDER BY id",
            (action_id,),
        ).fetchall()
        assert [row["event_type"] for row in events] == ["action_completed", "skill_application_evidence"]
        assert json.loads(events[1]["payload_json"])["application_id"] == GRAPPLE_APPLICATION_ID
        assert events[1]["caused_by_event_id"] == events[0]["id"]

        maybe_settle_skill_progression(
            conn,
            "char_darian",
            as_of_sim_time=snapshot(conn, "char_darian")["sim_time"],
        )
        after_skill = tuple(
            conn.execute(
                "SELECT score,experience FROM character_skills WHERE entity_id='char_darian' AND skill_key=?",
                (SKILL_ID,),
            ).fetchone()
        )
        assert after_skill == before_skill
        assert conn.execute(
            "SELECT state_json FROM entities WHERE id=?",
            (PARTNER,),
        ).fetchone()[0] == before_partner_state
