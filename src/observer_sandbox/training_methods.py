from __future__ import annotations

"""Authored training-method metadata and deterministic evidence derivation.

Training methods are reusable definitions. Concrete world targets bind to a
method id; neither the definition nor this resolver depends on character
identity. Domain progression engines remain authoritative for what progresses
and by how much.
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


def training_method_definition(
    method_id: str | None,
    *,
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if not method_id:
        return None
    source = catalog if catalog is not None else load_training_method_catalog()
    raw = source.get("methods", {}).get(method_id)
    if not isinstance(raw, dict):
        return None
    method = dict(raw)
    method["method_id"] = method_id
    method["source"] = str(source.get("revision", "training-method-semantics-v2"))
    return method


def training_method_id_for_target(
    target: str | None,
    *,
    catalog: dict[str, Any] | None = None,
) -> str | None:
    if not target:
        return None
    source = catalog if catalog is not None else load_training_method_catalog()
    raw = source.get("bindings", {}).get(target)
    return raw if isinstance(raw, str) and raw else None


def training_profile_for_target(
    target: str | None,
    *,
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if not target:
        return None
    source = catalog if catalog is not None else load_training_method_catalog()
    method_id = training_method_id_for_target(target, catalog=source)
    method = training_method_definition(method_id, catalog=source)
    if method is None:
        return None
    method["target"] = target
    return method


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
