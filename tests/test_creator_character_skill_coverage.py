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


def _skill(key, score=0, experience=0):
    return {"skill_key": key, "category": None, "score": score, "tier": None, "experience": experience}


def _all_skills():
    return [_skill(key) for key in canonical_skill_keys()]


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
                "skills": _all_skills() if skills is None else skills,
            }
        }
    }


def test_creator_character_contract_is_exact_full_seed_template():
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
    assert skills["minItems"] == skills["maxItems"] == len(canonical_skill_keys())
    assert tuple(skills["items"]["properties"]["skill_key"]["enum"]) == canonical_skill_keys()
    assert skills["items"]["properties"]["score"] == {"type": "number", "minimum": 0, "maximum": 100}
    assert skills["items"]["properties"]["experience"] == {"type": "number", "minimum": 0}
    assert "Fill the supplied Character seed schema exactly" in prompt
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


def test_exact_seed_requires_every_canonical_skill_once():
    _, schema = _prepare_creator_character_contract(
        "Create Adrian Vale.", _schema(), "observer_creator_studio_character"
    )
    incomplete = _all_skills()[:-1]
    with pytest.raises(AIDecisionError, match="skill keys do not match"):
        _validate_creator_character_contract(
            _value(skills=incomplete), schema, "observer_creator_studio_character"
        )

    value = _value(skills=_all_skills())
    _validate_creator_character_contract(value, schema, "observer_creator_studio_character")
    normalized = value["properties"]["character_profile"]["skills"]
    assert {item["skill_key"] for item in normalized} == set(canonical_skill_keys())


def test_skill_vocabulary_aliases_still_normalize_and_unknown_keys_reject():
    normalized = normalize_creator_skills([_skill("first_aid", score=50, experience=1)])
    assert normalized[0]["skill_key"] == "field_medicine"
    assert normalized[0]["category"] == "medical"
    with pytest.raises(ValueError, match="Unknown Creator Character skill_key"):
        normalize_creator_skills([_skill("made_up_skill")])
