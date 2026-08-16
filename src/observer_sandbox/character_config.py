from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
CHARACTER_CONFIG_DIR = REPO_ROOT / "config" / "characters"
CHARACTER_REGISTRY_PATH = CHARACTER_CONFIG_DIR / "registry.json"
UNIVERSAL_AUTONOMY_POLICY_PATH = REPO_ROOT / "config" / "autonomy" / "universal.autonomy-policy.v1.json"


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


def load_universal_autonomy_policy(
    path: str | Path = UNIVERSAL_AUTONOMY_POLICY_PATH,
) -> dict[str, Any]:
    """Load the character-agnostic cognition policy used by every actor."""
    policy = json.loads(Path(path).read_text(encoding="utf-8"))
    if policy.get("entity_id") is not None:
        raise ValueError("Universal autonomy policy must not bind to a character entity")
    return policy


def load_character_autonomy_policy(character_id: str) -> dict[str, Any]:
    """Compatibility shim: autonomy policy is universal, never character-specific."""
    character_config(character_id)
    return load_universal_autonomy_policy()
