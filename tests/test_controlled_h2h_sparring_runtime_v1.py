from __future__ import annotations

import json

import pytest

from observer_sandbox.controlled_h2h_runtime import (
    APPLICATION_ID,
    CONSENT_CAPABILITY,
    SKILL_ID,
    SPAR_ACTION,
    TASK_ID,
    ControlledH2HRuntimeError,
    controlled_h2h_outcome,
)
from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot
from observer_sandbox.skill_progression import maybe_settle_skill_progression


ROOM = "loc_thorne_estate_training_hall"
SESSION = "obj_test_controlled_h2h_sparring_session"
PARTNER = "char_test_controlled_h2h_partner"


def _seed_session(conn, *, definition_id: str | None = None) -> None:
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id) VALUES(?,?,?,?,?)",
        (
            SESSION,
            "object",
            "Controlled Striking Sparring Session",
            json.dumps(["spar", "controlled_sparring_session"]),
            definition_id
            or "represented_task:h2h_controlled_striking_sparring_session_v1",
        ),
    )
    conn.execute(
        "INSERT INTO relations(source_id,relation_type,target_id) VALUES(?,?,?)",
        (ROOM, "contains", SESSION),
    )


def _seed_partner(conn, *, consent: bool = True, room: str = ROOM) -> None:
    capabilities = [CONSENT_CAPABILITY] if consent else []
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json,definition_id) VALUES(?,?,?,?,?,?)",
        (
            PARTNER,
            "character",
            "Controlled Sparring Partner",
            "{}",
            json.dumps(capabilities),
            "test:controlled_sparring_partner_v1",
        ),
    )
    set_dynamic_location(conn, PARTNER, room)


def _prepare(conn, *, consent: bool = True, partner_room: str = ROOM) -> None:
    _seed_session(conn)
    _seed_partner(conn, consent=consent, room=partner_room)
    set_dynamic_location(conn, "char_darian", ROOM)
    conn.commit()


def test_runtime_registers_spar_action_without_fabricating_live_session_or_partner(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        action = conn.execute(
            "SELECT target_mode,required_capability,requires_colocation FROM action_definitions WHERE action_type=?",
            (SPAR_ACTION,),
        ).fetchone()
        assert action is not None
        assert action["target_mode"] == "object"
        assert action["required_capability"] == SPAR_ACTION
        assert action["requires_colocation"] == 1
        assert conn.execute(
            "SELECT 1 FROM entities WHERE definition_id='represented_task:h2h_controlled_striking_sparring_session_v1'"
        ).fetchone() is None
        assert conn.execute(
            "SELECT 1 FROM entities WHERE capabilities_json LIKE '%controlled_sparring_consent%'"
        ).fetchone() is None


def test_controlled_h2h_outcome_uses_parent_skill_and_only_declared_supporting_attributes(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        outcome = controlled_h2h_outcome(conn, "char_darian", SESSION, (PARTNER,))
        assert outcome["task"]["task_id"] == TASK_ID
        assert outcome["capability"]["skill_id"] == SKILL_ID
        assert outcome["capability"]["application_id"] == APPLICATION_ID
        assert outcome["capability"]["skill_score"] == pytest.approx(90.0)
        assert outcome["capability"]["proficiency_grade"] == "S"
        assert outcome["authorization"]["participant_id"] == PARTNER
        assert outcome["authorization"]["authorization_capabilities"] == [CONSENT_CAPABILITY]
        assert outcome["consequence"] == {
            "mode": "scored_contact_only",
            "injury_state_mutated": False,
            "target_state_mutated": False,
        }
        assert outcome["learning_evidence"] is False
        factors = {
            factor["field_key"]
            for dimension in outcome["performance"]["dimensions"]
            for factor in dimension["factor_contributions"]
        }
        assert factors == {"raps_pa.reflexes", "raps_pa.agility", "raps_ma.focus"}
        assert "raps_ia.iq" not in factors
        assert "raps_pa.combat_skill" not in factors


def test_completed_spar_writes_application_evidence_without_xp_or_injury_state_mutation(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        option = next(
            item
            for item in action_options(conn, "char_darian")
            if item["action"] == SPAR_ACTION and item["target"] == SESSION
        )
        assert option["target_name"] == "Controlled Striking Sparring Session"

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

        action_id = "controlled-h2h-spar-v1-action"
        apply_action(
            conn,
            Action(
                SPAR_ACTION,
                10,
                SESSION,
                "controlled scored-contact sparring",
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
        assert outcome["represented_skill_task"]["consequence"]["mode"] == "scored_contact_only"
        assert outcome["represented_skill_task"]["consequence"]["injury_state_mutated"] is False
        assert outcome["skill_application"]["skill_id"] == SKILL_ID
        assert outcome["skill_application"]["learning_evidence"] is False
        assert outcome["skill_application"]["participant_id"] == PARTNER

        events = conn.execute(
            "SELECT id,event_type,payload_json,caused_by_event_id FROM events WHERE action_id=? ORDER BY id",
            (action_id,),
        ).fetchall()
        assert [row["event_type"] for row in events] == ["action_completed", "skill_application_evidence"]
        evidence = json.loads(events[1]["payload_json"])
        assert evidence["learning_evidence"] is False
        assert events[1]["caused_by_event_id"] == events[0]["id"]
        participants = {
            row["entity_id"]
            for row in conn.execute(
                "SELECT entity_id FROM event_participants WHERE event_id=?",
                (events[0]["id"],),
            ).fetchall()
        }
        assert {"char_darian", PARTNER}.issubset(participants)

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


def test_missing_participant_fails_closed_and_rolls_back_action(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        before = snapshot(conn, "char_darian")
        with pytest.raises(ControlledH2HRuntimeError, match="exactly 1 participant"):
            apply_action(
                conn,
                Action(SPAR_ACTION, 10, SESSION, "missing participant"),
                "char_darian",
                action_id="spar-missing-participant",
            )
        assert snapshot(conn, "char_darian") == before
        assert conn.execute(
            "SELECT 1 FROM action_instances WHERE id='spar-missing-participant'"
        ).fetchone() is None


def test_participant_without_explicit_consent_fails_closed(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn, consent=False)
        before = snapshot(conn, "char_darian")
        with pytest.raises(ControlledH2HRuntimeError, match="explicit authorization"):
            apply_action(
                conn,
                Action(SPAR_ACTION, 10, SESSION, "consent absent", participants=(PARTNER,)),
                "char_darian",
                action_id="spar-no-consent",
            )
        assert snapshot(conn, "char_darian") == before
        assert conn.execute("SELECT 1 FROM action_instances WHERE id='spar-no-consent'").fetchone() is None


def test_non_colocated_participant_fails_closed(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn, partner_room="loc_thorne_estate_living_room")
        before = snapshot(conn, "char_darian")
        with pytest.raises(ControlledH2HRuntimeError, match="colocated"):
            apply_action(
                conn,
                Action(SPAR_ACTION, 10, SESSION, "remote partner", participants=(PARTNER,)),
                "char_darian",
                action_id="spar-remote-partner",
            )
        assert snapshot(conn, "char_darian") == before
        assert conn.execute("SELECT 1 FROM action_instances WHERE id='spar-remote-partner'").fetchone() is None


def test_wrong_session_definition_fails_exact_binding_before_persisting_action(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_session(conn, definition_id="represented_task:not_authorized_for_controlled_sparring")
        _seed_partner(conn)
        set_dynamic_location(conn, "char_darian", ROOM)
        conn.commit()
        before = snapshot(conn, "char_darian")
        with pytest.raises(Exception, match="expected"):
            apply_action(
                conn,
                Action(SPAR_ACTION, 10, SESSION, "wrong session", participants=(PARTNER,)),
                "char_darian",
                action_id="spar-wrong-session",
            )
        assert snapshot(conn, "char_darian") == before
        assert conn.execute("SELECT 1 FROM action_instances WHERE id='spar-wrong-session'").fetchone() is None
