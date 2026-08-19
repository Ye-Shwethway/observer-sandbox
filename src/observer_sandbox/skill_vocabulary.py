from __future__ import annotations

from typing import Any, Iterable, Mapping

# Minimum shared Character skill vocabulary for Creator Creation and future
# transmigration validation. Storage remains backward-compatible/free-form for
# existing live data; new Creator-generated Characters converge on these keys.
SKILL_DEFINITIONS: dict[str, dict[str, Any]] = {
    "hand_to_hand_combat": {
        "category": "combat",
        "cues": ("hand-to-hand", "hand to hand", "boxing", "wrestling", "martial arts", "combat sports"),
    },
    "weapons": {
        "category": "combat",
        "cues": ("weapons training", "weapon training", "weapon handling"),
    },
    "firearms": {
        "category": "combat",
        "cues": ("firearms", "firearm", "shooting", "marksmanship"),
    },
    "bladed_weapons": {
        "category": "combat",
        "cues": ("bladed weapons", "blade training", "knife training", "sword training"),
    },
    "survival": {
        "category": "fieldcraft",
        "cues": ("survival", "fieldcraft", "wilderness", "search-and-rescue", "search and rescue"),
    },
    "navigation": {
        "category": "fieldcraft",
        "cues": ("navigation", "orienteering", "map reading", "topographic map", "land navigation"),
    },
    "climbing": {
        "category": "fieldcraft",
        "cues": ("climbing", "mountaineering", "rope rescue", "rope work"),
    },
    "emergency_response": {
        "category": "rescue",
        "cues": ("emergency response", "search-and-rescue", "search and rescue", "rescue organization", "rescue work"),
    },
    "field_medicine": {
        "category": "medical",
        "cues": ("first aid", "field medicine", "emergency medicine", "medical response", "paramedic"),
    },
    "tactical_planning": {
        "category": "cognition",
        "cues": ("tactical planning", "operational planning", "mission planning"),
    },
    "technology": {
        "category": "technical",
        "cues": ("technology", "technical systems", "computer systems", "electronics"),
    },
}

SKILL_ALIASES = {
    "weapon_mastery": "weapons",
    "first_aid": "field_medicine",
    "search_and_rescue": "emergency_response",
}


def canonical_skill_keys() -> tuple[str, ...]:
    return tuple(SKILL_DEFINITIONS)


def normalize_skill_key(skill_key: str) -> str:
    key = str(skill_key or "").strip().lower().replace(" ", "_")
    return SKILL_ALIASES.get(key, key)


def normalize_creator_skills(skills: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in skills:
        key = normalize_skill_key(str(raw.get("skill_key") or ""))
        if not key:
            continue
        if key not in SKILL_DEFINITIONS:
            raise ValueError(f"Unknown Creator Character skill_key: {key}")
        if key in seen:
            continue
        item = dict(raw)
        item["skill_key"] = key
        item["category"] = SKILL_DEFINITIONS[key]["category"]
        score = item.get("score")
        if score is not None and (isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= float(score) <= 100):
            raise ValueError(f"Character skill score out of range: {key}")
        experience = item.get("experience")
        if experience is not None and (isinstance(experience, bool) or not isinstance(experience, (int, float)) or float(experience) < 0):
            raise ValueError(f"Character skill experience cannot be negative: {key}")
        seen.add(key)
        result.append(item)
    return result


def required_skills_from_background(values: Mapping[str, Any]) -> set[str]:
    background = " ".join(
        str(values.get(key) or "")
        for key in ("background.origins", "background.story_elements")
    ).lower()
    required: set[str] = set()
    for skill_key, definition in SKILL_DEFINITIONS.items():
        if any(str(cue).lower() in background for cue in definition.get("cues", ())):
            required.add(skill_key)
    return required


def missing_background_skill_coverage(values: Mapping[str, Any], skills: Iterable[Mapping[str, Any]]) -> set[str]:
    required = required_skills_from_background(values)
    present = {normalize_skill_key(str(item.get("skill_key") or "")) for item in skills}
    return required - present


__all__ = [
    "SKILL_ALIASES",
    "SKILL_DEFINITIONS",
    "canonical_skill_keys",
    "missing_background_skill_coverage",
    "normalize_creator_skills",
    "normalize_skill_key",
    "required_skills_from_background",
]
