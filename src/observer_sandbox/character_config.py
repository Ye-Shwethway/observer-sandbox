from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
CHARACTER_CONFIG_DIR = REPO_ROOT / "config" / "characters"
CHARACTER_REGISTRY_PATH = CHARACTER_CONFIG_DIR / "registry.json"


@lru_cache(maxsize=1)
def load_character_registry(path: str | Path = CHARACTER_REGISTRY_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def configured_character_ids(*, registry: dict[str, Any] | None = None) -> list[str]:
    source = registry if registry is not None else load_character_registry()
    characters = source.get("characters", {})
    if not isinstance(characters, dict):
        return []
    return sorted(str(key) for key in characters)


def character_config(character_id: str, *, registry: dict[str, Any] | None = None) -> dict[str, Any]:
    source = registry if registry is not None else load_character_registry()
    characters = source.get("characters", {})
    raw = characters.get(character_id) if isinstance(characters, dict) else None
    if not isinstance(raw, dict):
        raise KeyError(f"No character config registered for {character_id}")
    return dict(raw)


def character_config_path(character_id: str, key: str) -> Path:
    config = character_config(character_id)
    relative = config.get(key)
    if not isinstance(relative, str) or not relative.strip():
        raise KeyError(f"Character config {character_id} has no {key!r} file")
    return CHARACTER_CONFIG_DIR / relative


def load_character_autonomy_policy(character_id: str) -> dict[str, Any]:
    path = character_config_path(character_id, "autonomy_policy")
    policy = json.loads(path.read_text(encoding="utf-8"))
    configured_entity = policy.get("entity_id")
    if configured_entity not in (None, character_id):
        raise ValueError(
            f"Autonomy policy entity mismatch: expected {character_id}, got {configured_entity}"
        )
    return policy
