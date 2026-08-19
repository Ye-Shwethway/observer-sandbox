import pytest

from observer_sandbox.ai_runtime import AIDecisionError
from observer_sandbox.skill_vocabulary import canonical_skill_keys, normalize_creator_skills
from observer_sandbox.structured_ai import (
    _prepare_creator_character_contract,
    _validate_creator_character_contract,
)


def _schema():
    return {
        "properties": {
            "properties": {
                "properties": {
                    "character_profile": {
                        "properties": {
                            "values": {
                                "type": "object",
                                "properties": {
                                    "identity.full_name": {"type": "string"},
                                    "body.height_in": {"type": "number"},
                                    "raps_pa.strength": {"type": "number"},
                                    "raps_pa.practical_skills": {"type": "number"},
                                    "raps_pa.practical_skill": {"type": "number"},
                                },
                                "additionalProperties": False,
                                "minProperties": 4,
                            },
                            "skills": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "skill_key": {"type": "string"},
                                        "category": {"type": ["string", "null"]},
                                        "score": {"type": ["number", "null"]},
                                        "tier": {"type": ["string", "null"]},
                                        "experience": {"type": ["number", "null"]},
                                    },
                                    "required": ["skill_key", "category", "score", "tier", "experience"],
                                    "additionalProperties": False,
                                },
                            },
                        }
                    }
                }
            }
        }
    }


def _skill(key, score=70, experience=2):
    return {"skill_key": key, "category": None, "score": score, "tier": None, "experience": experience}


def _value(values=None, skills=None):
    return {
        "properties": {
            "character_profile": {
                "values": values or {
                    "identity.full_name": "Adrian Vale",
                    "body.height_in": 74.0,
                    "raps_pa.strength": 82.0,
                    "raps_pa.practical_skills": 78.0,
                },
                "skills": [] if skills is None else skills,
            }
        }
    }


def test_creator_character_contract_is_exact_profile_template_with_sparse_skills():
    original = _schema()
    prompt, tightened = _prepare_creator_character_contract(
        "Create Adrian Vale.", original, "observer_creator_studio_character"
    )
    profile = tightened["properties"]["properties"]["properties"]["character_profile"]
    values = profile["properties"]["values"]
    assert set(values["required"]) == {
        "identity.full_name", "body.height_in", "raps_pa.strength", "raps_pa.practical_skills"
    }
    assert "raps_pa.practical_skill" not in values["properties"]
    assert values["minProperties"] == values["maxProperties"] == 4

    skills = profile["properties"]["skills"]
    assert "minItems" not in skills
    assert "maxItems" not in skills
    assert tuple(skills["items"]["properties"]["skill_key"]["enum"]) == canonical_skill_keys()
    assert "include only skills the Character actually has" in prompt
    assert original == _schema()


def test_exact_seed_rejects_missing_or_extra_profile_keys():
    _, schema = _prepare_creator_character_contract(
        "Create Adrian Vale.", _schema(), "observer_creator_studio_character"
    )
    value = _value()
    del value["properties"]["character_profile"]["values"]["body.height_in"]
    with pytest.raises(AIDecisionError, match="canonical template"):
        _validate_creator_character_contract(value, schema, "observer_creator_studio_character")

    value = _value()
    value["properties"]["character_profile"]["values"]["made_up.field"] = 1
    with pytest.raises(AIDecisionError, match="canonical template"):
        _validate_creator_character_contract(value, schema, "observer_creator_studio_character")


def test_sparse_skills_accept_relevant_subset_and_normalize_categories():
    _, schema = _prepare_creator_character_contract(
        "Create Adrian Vale.", _schema(), "observer_creator_studio_character"
    )
    value = _value(skills=[
        _skill("survival", 80, 4),
        _skill("navigation", 76, 4),
        _skill("field_medicine", 72, 4),
        _skill("hand_to_hand_combat", 68, 1.5),
    ])
    _validate_creator_character_contract(value, schema, "observer_creator_studio_character")
    normalized = value["properties"]["character_profile"]["skills"]
    assert {item["skill_key"] for item in normalized} == {
        "survival", "navigation", "field_medicine", "hand_to_hand_combat"
    }
    categories = {item["skill_key"]: item["category"] for item in normalized}
    assert categories["navigation"] == "fieldcraft"
    assert categories["field_medicine"] == "medical"


def test_sparse_skills_allow_empty_and_reject_unknown_keys():
    _, schema = _prepare_creator_character_contract(
        "Create an untrained character.", _schema(), "observer_creator_studio_character"
    )
    value = _value(skills=[])
    _validate_creator_character_contract(value, schema, "observer_creator_studio_character")
    assert value["properties"]["character_profile"]["skills"] == []

    with pytest.raises(AIDecisionError, match="Unknown Creator Character skill_key"):
        _validate_creator_character_contract(
            _value(skills=[_skill("made_up_skill")]), schema, "observer_creator_studio_character"
        )


def test_skill_vocabulary_aliases_still_normalize():
    normalized = normalize_creator_skills([_skill("first_aid", score=50, experience=1)])
    assert normalized[0]["skill_key"] == "field_medicine"
    assert normalized[0]["category"] == "medical"
