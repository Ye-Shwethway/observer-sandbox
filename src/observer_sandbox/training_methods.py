from __future__ import annotations

"""Authored training-method metadata and deterministic evidence derivation.

This layer describes what kind of work a training target represents. It does
not decide which character attribute progresses, how much stimulus is earned,
or how progression settles; those remain responsibilities of domain-specific
progression engines.
"""

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
TRAINING_METHODS_PATH = REPO_ROOT / "config" / "training_methods.v1.json"


@lru_cache(maxsize=1)
def load_training_method_catalog(path: str | Path = TRAINING_METHODS_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def training_profile_for_target(
    target: str | None,
    *,
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if not target:
        return None
    source = catalog if catalog is not None else load_training_method_catalog()
    raw = source.get("profiles", {}).get(target)
    if not isinstance(raw, dict):
        return None
    profile = dict(raw)
    profile["target"] = target
    profile["source"] = str(source.get("revision", "training-method-semantics-v1"))
    return profile


def enrich_training_action_options(
    options: list[dict[str, Any]],
    *,
    catalog: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    source = catalog if catalog is not None else load_training_method_catalog()
    enriched: list[dict[str, Any]] = []
    for option in options:
        row = dict(option)
        if row.get("action") == "train":
            profile = training_profile_for_target(row.get("target"), catalog=source)
            if profile is not None:
                row["training_method"] = profile
        enriched.append(row)
    return enriched


def training_method_evidence(
    *,
    action_name: str,
    target: str | None,
    training_load: dict[str, Any] | None,
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if action_name != "train" or not isinstance(training_load, dict):
        return None
    source = catalog if catalog is not None else load_training_method_catalog()
    profile = training_profile_for_target(target, catalog=source)
    if profile is None:
        return None
    return {
        "target": target,
        "method_id": profile["method_id"],
        "method_name": profile["method_name"],
        "family": profile["family"],
        "workload_channels": list(profile.get("workload_channels", [])),
        "tags": list(profile.get("tags", [])),
        "effective_load": {
            "planned_minutes": int(training_load.get("planned_minutes", 0)),
            "effectiveness": float(training_load.get("effectiveness", 0.0)),
            "effective_minutes": float(training_load.get("effective_minutes", 0.0)),
        },
        "source": profile["source"],
    }


def training_method_evidence_from_event(
    payload: dict[str, Any],
    *,
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if payload.get("action") != "train":
        return None
    return training_method_evidence(
        action_name="train",
        target=payload.get("target"),
        training_load=payload.get("training_load"),
        catalog=catalog,
    )
