import copy

import pytest

from observer_sandbox.ai_runtime import AIDecisionError
from observer_sandbox.skill_vocabulary import (
    canonical_skill_keys,
    missing_background_skill_coverage,
    normalize_creator_skills,
)
from observer_sandbox.structured_ai import (
    _prepare_creator_character_contract,
    _validate_creator_character_skill_contract,
)


def _schema():
    return {
        "properties": {
            "properties": {
                "properties": {
                    "character_profile": {
                        "properties": {
                            "skills": {
                                "items": {
                                    "properties": {
                                        "skill_key": {"type": "string"},
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }


def _adrian_value(skills):
    return {
        "properties": {
            "character_profile": {
                "values": {
                    "background.origins": (
                        "Joined a professional wilderness search-and-rescue organization, gaining practical "
                        "experience in difficult terrain, navigation, climbing, and emergency response. "
                        "Has amateur boxing and wrestling training."
                    )
                },
                "skills": skills,
            }
        }
    }


def _skill(key, score=70):
    return {"skill_key": key, "category": None, "score": score, "tier": None, "experience": 2.0}


def test_creator_character_schema_is_tightened_to_shared_skill_vocabulary():
    original = _schema()
    prompt, tightened = _prepare_creator_character_contract(
        "Create a trained rescue character.", original, "observer_creator_studio_character"
    )
    enum = tightened["properties"]["properties"]["properties"]["character_profile"]["properties"]["skills"]["items"]["properties"]["skill_key"]["enum"]
    assert tuple(enum) == canonical_skill_keys()
    assert "navigation" in enum
    assert "climbing" in enum
    assert "emergency_response" in enum
    assert "Universal Character skill vocabulary" in prompt
    assert original == _schema()  # caller schema is not mutated


def test_adrian_style_background_rejects_partial_structured_skill_coverage():
    value = _adrian_value([
        _skill("survival"),
        _skill("hand_to_hand_combat"),
    ])
    with pytest.raises(AIDecisionError) as exc:
        _validate_creator_character_skill_contract(value, "observer_creator_studio_character")
    message = str(exc.value)
    assert "navigation" in message
    assert "climbing" in message
    assert "emergency_response" in message


def test_adrian_style_background_accepts_material_skill_coverage_and_normalizes_categories():
    skills = [
        _skill("survival"),
        _skill("navigation"),
        _skill("climbing"),
        _skill("emergency_response"),
        _skill("hand_to_hand_combat"),
    ]
    value = _adrian_value(skills)
    _validate_creator_character_skill_contract(value, "observer_creator_studio_character")
    normalized = value["properties"]["character_profile"]["skills"]
    assert {item["skill_key"] for item in normalized} == {
        "survival", "navigation", "climbing", "emergency_response", "hand_to_hand_combat"
    }
    categories = {item["skill_key"]: item["category"] for item in normalized}
    assert categories["navigation"] == "fieldcraft"
    assert categories["emergency_response"] == "rescue"


def test_skill_vocabulary_aliases_are_normalized_and_unknown_creator_skills_reject():
    normalized = normalize_creator_skills([_skill("first_aid")])
    assert normalized[0]["skill_key"] == "field_medicine"
    assert normalized[0]["category"] == "medical"
    with pytest.raises(ValueError, match="Unknown Creator Character skill_key"):
        normalize_creator_skills([_skill("made_up_skill")])


def test_background_coverage_helper_is_semantic_not_character_specific():
    values = {
        "background.origins": "A mountaineer trained in land navigation and first aid."
    }
    missing = missing_background_skill_coverage(values, [_skill("climbing")])
    assert missing == {"navigation", "field_medicine"}
