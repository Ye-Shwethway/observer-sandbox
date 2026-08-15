from __future__ import annotations

import json
from pathlib import Path

from observer_sandbox.skill_application_requirements import validate_application_requirements
from observer_sandbox.skill_capability import assess_skill_application
from observer_sandbox.skill_definitions import load_validated_skill_definitions
from observer_sandbox.skill_progression import load_skill_progression_config


REPO_ROOT = Path(__file__).resolve().parents[1]
CURRENT_SKILLS = {
    "hand_to_hand_combat",
    "weapons",
    "survival",
    "tactical_planning",
    "technology",
    "field_medicine",
}
LEGACY_SKILL_LIKE_FIELDS = {
    "raps_pa.combat_skill",
    "raps_pa.weapons_proficiency",
    "raps_pa.survival_skill",
    "raps_ia.tactical_thinking",
    "raps_ia.technological_aptitude",
    "raps_ia.medical_knowledge",
}
EXPECTED_PARENT_SCORES = {
    "hand_to_hand_combat": 90,
    "weapons": 87,
    "survival": 85,
    "tactical_planning": 92,
    "technology": 82,
    "field_medicine": 75,
}


def test_registry_covers_current_actor_skill_rows_without_score_migration() -> None:
    config = load_validated_skill_definitions()
    seed = json.loads((REPO_ROOT / "config/characters/darian.canonical.json").read_text(encoding="utf-8"))
    seed_scores = {item["key"]: item["score"] for item in seed["skills"]}

    assert set(config["skills"]) == CURRENT_SKILLS
    assert seed_scores == EXPECTED_PARENT_SCORES


def test_remaining_five_umbrella_skills_are_gameplay_grade_definitions() -> None:
    config = load_validated_skill_definitions()
    for skill_id in CURRENT_SKILLS - {"technology"}:
        definition = config["skills"][skill_id]
        validate_application_requirements(definition)
        assert len(definition["applications"]) == 2
        assert definition["relations"]["component_skills"] == []
        assert definition["provenance"]["compatibility"]["character_skill_key"] == skill_id


def test_legacy_skill_like_raps_fields_are_compatibility_only_not_dependencies() -> None:
    config = load_validated_skill_definitions()
    for definition in config["skills"].values():
        dependency_fields = {item["field_key"] for item in definition["ability_dependencies"]}
        assert dependency_fields.isdisjoint(LEGACY_SKILL_LIKE_FIELDS)
        assert set(definition["provenance"]["compatibility"]["legacy_profile_fields"]) <= LEGACY_SKILL_LIKE_FIELDS


def test_existing_progression_is_preserved_and_field_medicine_closure_is_explicit() -> None:
    definitions = load_validated_skill_definitions()["skills"]
    progression = load_skill_progression_config()["skills"]

    assert definitions["hand_to_hand_combat"]["learning_evidence"]["families"] == ["training_method"]
    assert definitions["tactical_planning"]["learning_evidence"]["families"] == ["training_method"]
    assert definitions["technology"]["learning_evidence"]["families"] == ["skill_practice"]
    assert set(progression) == {
        "bladed_weapons",
        "field_medicine",
        "firearms",
        "hand_to_hand_combat",
        "survival",
        "tactical_planning",
        "technology",
    }

    # Simulation-safe practice producers are explicit progression authority.
    # Historical umbrella/definition metadata is not reinterpreted as implicit
    # learning evidence and ordinary application still does not grant XP.
    assert definitions["survival"]["learning_evidence"]["families"] == ["supervised_application"]
    assert progression["bladed_weapons"]["eligible_methods"] == {
        "bladed_weapons_handling_practice": 1.0
    }
    assert progression["firearms"]["eligible_methods"] == {
        "firearms_handling_practice": 1.0
    }
    assert progression["field_medicine"]["eligible_methods"] == {
        "field_medicine_scenario_practice": 1.0
    }

    assert definitions["weapons"]["learning_evidence"]["families"] == ["supervised_application"]
    assert "weapons" not in progression


def test_no_resource_h2h_application_can_be_supported() -> None:
    assessment = assess_skill_application(
        "hand_to_hand_combat",
        "engage_unarmed_striking",
        skill_score=90,
        challenge_class="advanced",
        context_tags=["unarmed_combat_context", "opponent_or_training_target_represented"],
        resource_capabilities=[],
        attribute_values={"raps_pa.reflexes": 86, "raps_pa.agility": 83, "raps_ma.focus": 92},
    )
    assert assessment.status == "supported"
    assert assessment.matched_required_resource_capabilities == ()


def test_supporting_navigation_aid_changes_constrained_to_supported_without_gating() -> None:
    kwargs = dict(
        skill_id="survival",
        application_id="navigate_field_environment",
        skill_score=85,
        challenge_class="advanced",
        context_tags=["field_environment_represented", "navigation_objective_defined"],
        attribute_values={"raps_ma.adaptability": 85, "raps_ia.problem_solving": 88, "raps_pa.endurance": 87},
    )
    constrained = assess_skill_application(resource_capabilities=[], **kwargs)
    supported = assess_skill_application(resource_capabilities=["navigation_aid"], **kwargs)

    assert constrained.status == "constrained"
    assert constrained.missing_supporting_resource_capabilities == ("navigation_aid",)
    assert supported.status == "supported"


def test_required_bladed_training_resource_remains_a_real_gate() -> None:
    kwargs = dict(
        skill_id="bladed_weapons",
        application_id="employ_familiar_melee_weapon",
        skill_score=87,
        challenge_class="advanced",
        context_tags=[
            "weapon_employment_context",
            "represented_melee_weapon",
            "simulation_safe_training_context",
        ],
        attribute_values={"raps_pa.reflexes": 86, "raps_ma.focus": 92, "raps_pa.agility": 83},
    )
    unsupported = assess_skill_application(resource_capabilities=[], **kwargs)
    supported = assess_skill_application(
        resource_capabilities=["usable_bladed_training_weapon"],
        **kwargs,
    )

    assert unsupported.status == "unsupported"
    assert "required_resource_capability_missing" in unsupported.reasons
    assert supported.status == "supported"
