from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DurationProfile:
    min_minutes: int
    max_minutes: int
    label: str


# These are preferred planning ranges for newly proposed actions. They do not
# replace the broader persisted legality bounds in action_definitions.
GENERIC_PROFILES: dict[str, DurationProfile] = {
    "move": DurationProfile(2, 8, "routine movement"),
    "eat": DurationProfile(10, 30, "ordinary meal"),
    "drink": DurationProfile(2, 5, "ordinary drink"),
    "shower": DurationProfile(8, 20, "ordinary shower"),
    "rest": DurationProfile(10, 60, "short recovery"),
    "inspect": DurationProfile(2, 6, "routine inspection"),
    "use": DurationProfile(2, 10, "simple object use"),
    "train": DurationProfile(30, 90, "ordinary training session"),
    "read": DurationProfile(20, 60, "focused reading"),
    "research": DurationProfile(20, 90, "focused research session"),
    "monitor": DurationProfile(15, 45, "focused monitoring session"),
    "idle": DurationProfile(5, 20, "brief idle period"),
}


TARGET_PROFILES: dict[tuple[str, str], DurationProfile] = {
    ("inspect", "obj_thorne_estate_kitchen_refrigerator"): DurationProfile(2, 5, "quick refrigerator check"),
    ("inspect", "obj_thorne_estate_kitchen_pantry"): DurationProfile(2, 5, "quick pantry check"),
    ("use", "obj_thorne_estate_kitchen_stove"): DurationProfile(10, 30, "meal preparation"),
    ("read", "obj_thorne_estate_library_research_desk"): DurationProfile(20, 90, "focused research reading"),
    ("research", "obj_thorne_estate_library_research_desk"): DurationProfile(30, 90, "focused desk research"),
    ("train", "obj_thorne_estate_gym_heavy_bag"): DurationProfile(20, 45, "heavy-bag session"),
    ("train", "obj_thorne_estate_gym_free_weights"): DurationProfile(45, 90, "strength session"),
    ("train", "obj_thorne_estate_training_combat_mat"): DurationProfile(20, 60, "combat-mat practice"),
    ("train", "obj_thorne_estate_training_practice_dummy"): DurationProfile(20, 60, "practice-dummy session"),
}


def duration_profile(action: str, target: str | None) -> DurationProfile | None:
    if target is not None:
        targeted = TARGET_PROFILES.get((action, target))
        if targeted is not None:
            return targeted
    return GENERIC_PROFILES.get(action)


def normalize_duration(action: str, target: str | None, requested_minutes: int) -> int:
    profile = duration_profile(action, target)
    if profile is None:
        return int(requested_minutes)
    requested = int(requested_minutes)
    return max(profile.min_minutes, min(profile.max_minutes, requested))


def enrich_action_options(options: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for option in options:
        item = dict(option)
        profile = duration_profile(str(item.get("action")), item.get("target"))
        if profile is not None:
            item["preferred_duration"] = (profile.min_minutes, profile.max_minutes)
            item["duration_purpose"] = profile.label
        enriched.append(item)
    return enriched
