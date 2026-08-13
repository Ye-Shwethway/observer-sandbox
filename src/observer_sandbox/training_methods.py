from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
TRAINING_METHODS_PATH = REPO_ROOT / "config" / "training_methods.v1.json"


@lru_cache(maxsize=1)
def load_training_method_catalog(path: str | Path = TRAINING_METHODS_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def training_profile_for_target(target: str | None) -> dict[str, Any] | None:
    if not target:
        return None
    catalog = load_training_method_catalog()
    raw = catalog.get("profiles", {}).get(target)
    if not isinstance(raw, dict):
        return None
    profile = dict(raw)
    profile["target"] = target
    profile["source"] = str(catalog.get("revision", "training-method-semantics-v1"))
    return profile


def training_method_evidence(
    *,
    action_name: str,
    target: str | None,
    training_profile: dict[str, Any] | None,
    training_load: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if action_name != "train" or not target or not isinstance(training_profile, dict):
        return None
    if training_profile.get("target") != target:
        return None

    evidence: dict[str, Any] = {
        "method_id": training_profile.get("method_id"),
        "method_name": training_profile.get("method_name"),
        "family": training_profile.get("family"),
        "workload": list(training_profile.get("workload", [])),
        "primary_domains": list(training_profile.get("primary_domains", [])),
        "target": target,
        "source": training_profile.get("source", "training-method-semantics-v1"),
    }
    if isinstance(training_load, dict):
        evidence["planned_minutes"] = int(training_load.get("planned_minutes", 0))
        evidence["effective_minutes"] = float(training_load.get("effective_minutes", 0.0))
        evidence["effectiveness"] = float(training_load.get("effectiveness", 0.0))
    return evidence
