from __future__ import annotations

import json
import sqlite3
from collections import Counter
from typing import Any

from .simulation import action_definition, local_objects, reachable_rooms
from .spatial_familiarity import location_is_globally_hidden
from .training_methods import training_profile_for_target


MEANINGFUL_RESOURCE_CAPABILITIES = {
    "train", "use", "read", "eat", "drink", "shower", "sleep", "rest", "research", "monitor",
}


def _action_definitions(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    return [
        action_definition(conn, row["action_type"])
        for row in conn.execute("SELECT action_type FROM action_definitions ORDER BY action_type")
    ]


def reachable_location_awareness(conn: sqlite3.Connection, room_id: str) -> list[dict[str, Any]]:
    """Describe non-concealed one-hop destinations as planning-only previews.

    The preview deliberately omits location/object IDs. Those IDs are actionable
    authority and belong only to the current ``action_options`` surface. Globally
    concealed destinations are also omitted here because this generic preview has
    no actor-specific knowledge authority; an explicitly knowledgeable actor may
    still receive an exact move option through their character cognition surface.
    """
    definitions = _action_definitions(conn)
    result: list[dict[str, Any]] = []
    for room in reachable_rooms(conn, room_id):
        if location_is_globally_hidden(conn, str(room["id"])):
            continue
        resources: list[dict[str, Any]] = []
        action_names: set[str] = set()
        training_families: set[str] = set()
        training_methods: list[dict[str, str]] = []
        for obj in local_objects(conn, room["id"]):
            supported: list[str] = []
            for definition in definitions:
                capability = definition["required_capability"]
                if capability and capability in obj["capabilities"]:
                    supported.append(str(definition["action_type"]))
                    action_names.add(str(definition["action_type"]))
            if not supported:
                continue
            item: dict[str, Any] = {
                "name": obj["name"],
                "actions": sorted(supported),
                "planning_only": True,
            }
            training = training_profile_for_target(obj["id"])
            if training is not None and "train" in supported:
                item["training_method"] = {
                    "method_id": training["method_id"],
                    "method_name": training["method_name"],
                    "family": training["family"],
                    "workload_channels": list(training.get("workload_channels", [])),
                }
                training_families.add(str(training["family"]))
                training_methods.append({
                    "method_id": str(training["method_id"]),
                    "method_name": str(training["method_name"]),
                })
            resources.append(item)
        result.append({
            "location_name": room["name"],
            "available_actions_after_move": sorted(action_names),
            "training_families": sorted(training_families),
            "training_methods": training_methods,
            "resources": resources,
            "planning_only": True,
            "instruction": (
                "Planning preview only. Do not copy a target from this preview into a decision. "
                "A move or resource action is legal only when its exact target ID appears in current action_options."
            ),
        })
    return result


def recent_action_usage(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    limit: int = 24,
) -> dict[tuple[str, str | None], dict[str, Any]]:
    rows = conn.execute(
        "SELECT sim_time,payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id DESC LIMIT ?",
        (actor_id, int(limit)),
    ).fetchall()
    counts: Counter[tuple[str, str | None]] = Counter()
    latest: dict[tuple[str, str | None], str] = {}
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        action = payload.get("action")
        if not isinstance(action, str):
            continue
        target = payload.get("target")
        key = (action, target if isinstance(target, str) else None)
        counts[key] += 1
        latest.setdefault(key, row["sim_time"])
    return {
        key: {
            "recent_uses": int(count),
            "last_used_sim_time": latest[key],
            "recently_repeated": count >= 2,
        }
        for key, count in counts.items()
    }


def enrich_options_with_usage(
    options: list[dict[str, Any]],
    usage: dict[tuple[str, str | None], dict[str, Any]],
) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for option in options:
        row = dict(option)
        key = (str(row.get("action")), row.get("target") if isinstance(row.get("target"), str) else None)
        recent = usage.get(key)
        if recent is None:
            row["recent_usage"] = {"recent_uses": 0, "last_used_sim_time": None, "recently_repeated": False}
        else:
            row["recent_usage"] = dict(recent)
        enriched.append(row)
    return enriched


def familiar_object_targets(
    conn: sqlite3.Connection,
    actor_id: str,
    room_id: str,
) -> tuple[set[str], dict[str, str]]:
    """Derive a minimal familiarity proxy without introducing a memory schema.

    Functional authored resources are treated as established resources rather than
    objects that need routine re-inspection. Any object the actor has already
    completed an action against is also familiar, including inspect-only objects
    after their first meaningful look.
    """
    familiar: set[str] = set()
    basis: dict[str, str] = {}

    for obj in local_objects(conn, room_id):
        capabilities = {str(value) for value in obj.get("capabilities", [])}
        if capabilities & MEANINGFUL_RESOURCE_CAPABILITIES:
            target = str(obj["id"])
            familiar.add(target)
            basis[target] = "established_functional_resource"

    rows = conn.execute(
        "SELECT payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id DESC",
        (actor_id,),
    ).fetchall()
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        target = payload.get("target")
        if isinstance(target, str):
            familiar.add(target)
            basis[target] = "prior_interaction"
    return familiar, basis


def shape_inspect_options_for_familiarity(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    room_id: str,
    action_options: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Remove routine inspect choices for resources that are already familiar.

    This is choice shaping, not a persistent memory engine. Inspect-only unknown
    objects remain available once; after any completed interaction they become
    familiar through event history.
    """
    familiar, basis = familiar_object_targets(conn, actor_id, room_id)
    suppressed: list[dict[str, str]] = []
    filtered: list[dict[str, Any]] = []
    for option in action_options:
        target = option.get("target")
        if option.get("action") == "inspect" and isinstance(target, str) and target in familiar:
            suppressed.append({"target": target, "basis": basis.get(target, "familiar")})
            continue
        filtered.append(option)
    return filtered, {
        "source": "object-familiarity-inspect-utility-v1",
        "suppressed_inspect_count": len(suppressed),
        "suppressed": suppressed,
        "guidance": (
            "Familiar stable resources are not offered for routine inspection. Inspect remains useful for genuinely unknown inspect-only objects or future explicit change/investigation signals."
        ),
    }
