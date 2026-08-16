from __future__ import annotations

import json

from observer_sandbox.ai_runtime import _compact_prompt_state, _decision_prompt


def _state() -> dict:
    return {
        "location": "room_gym",
        "action_options": [
            {
                "action": "train",
                "target": "obj_rack",
                "target_name": "Power Rack",
                "duration": [20, 80],
                "training_load_guard": {"allowed": True, "verbose": "derived duplicate"},
                "training_method": {
                    "method_id": "barbell_strength_work",
                    "method_name": "Barbell Strength Work",
                    "family": "resistance",
                    "workload_channels": ["resistance"],
                    "tags": ["heavy", "barbell", "compound"],
                    "movement_pattern_ids": ["squat", "hinge"],
                    "movement_options": [
                        {"movement_id": "squat", "name": "Squat Pattern", "tags": ["lower_body"]},
                        {"movement_id": "hinge", "name": "Hip Hinge", "tags": ["posterior_chain"]},
                    ],
                    "planning": {"preferred_duration": [45, 90], "purpose": "barbell strength session"},
                    "target": "obj_rack",
                    "source": "training-method-semantics-v1",
                    "catalog_revision": "training-method-semantics-v2",
                },
            }
        ],
        "capability_awareness": {
            "revision": "cognition-capability-awareness-v1",
            "actor_id": "char_test",
            "unresolved_skills": [],
            "reasoning_profile": {
                "factors": {"focus": {"field_key": "raps_ma.focus", "value": 92}},
                "principles": ["Skill calibrates plausibility while engine authority remains deterministic."],
            },
            "skills": [
                {
                    "skill_id": "hand_to_hand_combat",
                    "name": "Hand-to-Hand Combat",
                    "category": "combat",
                    "proficiency": {
                        "score": 91.0,
                        "grade": "A",
                        "label": "expert",
                        "behavioral_anchor": {
                            "summary": "Handles advanced represented challenges independently.",
                            "independence": "high",
                            "supported_challenges": ["routine", "standard", "challenging", "advanced"],
                            "limits": "Extreme challenges remain uncertain.",
                        },
                    },
                    "definition": "Long descriptive definition that is useful canonically but duplicated in every cognition prompt.",
                    "scope_includes": ["striking", "grappling"],
                    "scope_excludes": ["weapons", "tactical command"],
                    "applications": [
                        {
                            "application_id": "engage_unarmed_striking",
                            "name": "Engage in Unarmed Striking",
                            "description": "Verbose application prose duplicated from the canonical definition.",
                            "outcome_intent": "Produce bounded striking and defensive performance.",
                            "challenge_classes": ["routine", "standard", "challenging", "advanced"],
                            "required_context": ["represented unarmed-combat context"],
                            "helpful_resources": [],
                            "required_context_tags": ["unarmed_combat_context"],
                            "required_resource_mode": "none",
                            "required_resource_capabilities_any": [],
                            "supporting_resource_capabilities": [],
                            "supporting_knowledge_keys": ["unarmed_striking_fundamentals"],
                            "risk_class": "moderate",
                            "failure_modes": ["poor distance or timing", "loss of balance"],
                        }
                    ],
                    "supporting_attributes": [
                        {
                            "field_key": "raps_pa.reflexes",
                            "value": 88,
                            "relationship": "performance_modifier",
                            "relevance": 1.0,
                        }
                    ],
                    "knowledge_context": {
                        "mode": "declarative_only_not_actor_knowledge_state",
                        "keys": ["unarmed_striking_fundamentals"],
                    },
                }
            ],
        },
    }


def test_compaction_preserves_executable_training_and_capability_semantics() -> None:
    compact = _compact_prompt_state(_state())

    option = compact["action_options"][0]
    assert option["action"] == "train"
    assert option["target"] == "obj_rack"
    assert option["duration"] == [20, 80]
    assert option["preferred_duration"] == (45, 80)
    assert option["duration_purpose"] == "barbell strength session"
    assert "training_load_guard" not in option

    method = option["training_method"]
    assert method["method_id"] == "barbell_strength_work"
    assert method["family"] == "resistance"
    assert method["movement_options"] == [
        {"movement_id": "squat", "name": "Squat Pattern"},
        {"movement_id": "hinge", "name": "Hip Hinge"},
    ]
    for duplicated_key in ("movement_pattern_ids", "planning", "target", "source", "catalog_revision"):
        assert duplicated_key not in method

    skill = compact["capability_awareness"]["skills"][0]
    assert skill["proficiency"]["score"] == 91.0
    assert skill["proficiency"]["behavioral_anchor"]["supported_challenges"][-1] == "advanced"
    assert skill["supporting_attributes"][0]["field_key"] == "raps_pa.reflexes"
    application = skill["applications"][0]
    assert application["application_id"] == "engage_unarmed_striking"
    assert application["required_context_tags"] == ["unarmed_combat_context"]
    assert application["supporting_knowledge_keys"] == ["unarmed_striking_fundamentals"]
    assert application["risk_class"] == "moderate"
    for verbose_key in ("definition", "scope_includes", "scope_excludes"):
        assert verbose_key not in skill
    for verbose_key in ("description", "required_context", "helpful_resources", "failure_modes"):
        assert verbose_key not in application


def test_compaction_is_idempotent_and_reduces_serialized_context() -> None:
    state = _state()
    once = _compact_prompt_state(state)
    twice = _compact_prompt_state(once)

    assert twice == once
    raw_size = len(json.dumps(state, sort_keys=True))
    compact_size = len(json.dumps(once, sort_keys=True))
    assert compact_size < raw_size


def test_decision_prompt_keeps_exact_movement_ids_without_verbose_duplicates() -> None:
    prompt = _decision_prompt(_state(), ["train"])

    assert '"movement_id": "squat"' in prompt
    assert '"movement_id": "hinge"' in prompt
    assert '"required_context_tags": ["unarmed_combat_context"]' in prompt
    assert "Verbose application prose duplicated" not in prompt
    assert "Long descriptive definition" not in prompt
    assert "training-method-semantics-v1" not in prompt
