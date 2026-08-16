from __future__ import annotations

import json
import sqlite3
from collections import Counter
from typing import Any

from .simulation import action_definition, local_objects, reachable_rooms
from .spatial_familiarity import location_is_globally_hidden
from .training_methods import training_profile_for_target
from .world import get_field


MEANINGFUL_RESOURCE_CAPABILITIES = {
    "train", "use", "read", "eat", "drink", "shower", "sleep", "rest", "research", "monitor",
}

_EFFECT_STATE_KEYS = {
    "needs.energy": ("energy", 1),
    "needs.hunger": ("hunger", -1),
    "needs.thirst": ("thirst", -1),
    "needs.sleepiness": ("sleepiness", -1),
    "physiology.cleanliness": ("cleanliness", 1),
    "physiology.fatigue": ("fatigue", -1),
}
LOW_MARGINAL_BENEFIT = 5.0
RECENT_SATIATION_DISTANCE = 3


def _action_definitions(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    return [
        action_definition(conn, row["action_type"])
        for row in conn.execute("SELECT action_type FROM action_definitions ORDER BY action_type")
    ]


def _location_affordances(conn: sqlite3.Connection, location_id: str) -> list[str]:
    spatial = get_field(conn, location_id, "world.spatial_container", {}) or {}
    if not isinstance(spatial, dict):
        return []
    return sorted({str(value) for value in spatial.get("affordances", []) if isinstance(value, str)})


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
        location_affordances = _location_affordances(conn, str(room["id"]))
        for definition in definitions:
            capability = definition["required_capability"]
            if (
                definition.get("target_mode") == "none"
                and isinstance(capability, str)
                and capability in location_affordances
            ):
                action_names.add(str(definition["action_type"]))
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
            "location_affordances": location_affordances,
            "training_families": sorted(training_families),
            "training_methods": training_methods,
            "resources": resources,
            "planning_only": True,
            "instruction": (
                "Planning preview only. Location affordances describe ordinary activities supported by that place after arrival. "
                "Do not copy a target from this preview into a decision. A move or resource action is legal only when its exact target ID appears in current action_options."
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
    latest: dict[tuple[str, str | None], dict[str, Any]] = {}
    for event_distance, row in enumerate(rows):
        payload = json.loads(row["payload_json"] or "{}")
        action = payload.get("action")
        if not isinstance(action, str):
            continue
        target = payload.get("target")
        key = (action, target if isinstance(target, str) else None)
        counts[key] += 1
        latest.setdefault(
            key,
            {
                "last_used_sim_time": row["sim_time"],
                "event_distance": int(event_distance),
                "last_before": payload.get("before") if isinstance(payload.get("before"), dict) else {},
                "last_after": payload.get("after") if isinstance(payload.get("after"), dict) else {},
            },
        )
    return {
        key: {
            "recent_uses": int(count),
            "last_used_sim_time": latest[key]["last_used_sim_time"],
            "recently_repeated": count >= 2,
            "event_distance": latest[key]["event_distance"],
            "last_before": latest[key]["last_before"],
            "last_after": latest[key]["last_after"],
        }
        for key, count in counts.items()
    }


def _project_effect(current: float, spec: Any) -> float:
    value = float(current)
    if isinstance(spec, (int, float)):
        return value + float(spec)
    if not isinstance(spec, dict):
        return value
    if "add" in spec:
        value += float(spec["add"])
    if "multiply" in spec:
        value *= float(spec["multiply"])
    if "set" in spec:
        value = float(spec["set"])
    if "clamp_min" in spec:
        value = max(value, float(spec["clamp_min"]))
    if "clamp_max" in spec:
        value = min(value, float(spec["clamp_max"]))
    return max(0.0, min(100.0, value))


def _marginal_physiological_benefit(option: dict[str, Any], recent: dict[str, Any]) -> float | None:
    effects = option.get("effects")
    after = recent.get("last_after")
    if not isinstance(effects, dict) or not isinstance(after, dict):
        return None
    benefits: list[float] = []
    for field_key, spec in effects.items():
        mapped = _EFFECT_STATE_KEYS.get(str(field_key))
        if mapped is None:
            continue
        state_key, direction = mapped
        current = after.get(state_key)
        if not isinstance(current, (int, float)):
            continue
        projected = _project_effect(float(current), spec)
        benefits.append(max(0.0, (projected - float(current)) * direction))
    if not benefits:
        return None
    return round(sum(benefits), 3)


def enrich_options_with_usage(
    options: list[dict[str, Any]],
    usage: dict[tuple[str, str | None], dict[str, Any]],
) -> list[dict[str, Any]]:
    """Attach recent-use context and suppress only low-value non-mobility loops.

    Legal movement is navigation authority, not a consumable choice. Repetition may
    inform character choice through ``recent_usage`` metadata, but it must never
    remove an otherwise legal move destination from cognition. Other actions may
    still be suppressed when authored physiology proves negligible recent benefit.
    """
    enriched: list[dict[str, Any]] = []
    suppressed: list[dict[str, Any]] = []
    for option in options:
        row = dict(option)
        key = (str(row.get("action")), row.get("target") if isinstance(row.get("target"), str) else None)
        recent = usage.get(key)
        if recent is None:
            row["recent_usage"] = {
                "recent_uses": 0,
                "last_used_sim_time": None,
                "recently_repeated": False,
                "event_distance": None,
            }
            enriched.append(row)
            continue

        public_recent = {
            "recent_uses": int(recent.get("recent_uses", 0)),
            "last_used_sim_time": recent.get("last_used_sim_time"),
            "recently_repeated": bool(recent.get("recently_repeated", False)),
            "event_distance": recent.get("event_distance"),
        }
        row["recent_usage"] = public_recent

        action = str(row.get("action"))
        if action == "move":
            enriched.append(row)
            continue

        distance = recent.get("event_distance")
        marginal = _marginal_physiological_benefit(row, recent)
        if (
            isinstance(distance, int)
            and distance <= RECENT_SATIATION_DISTANCE
            and marginal is not None
            and marginal <= LOW_MARGINAL_BENEFIT
        ):
            suppressed.append({
                "action": action,
                "target": row.get("target"),
                "basis": "recently_satiated_low_marginal_benefit",
                "marginal_benefit": marginal,
            })
            continue

        enriched.append(row)

    # Never erase the complete legal surface. This is choice shaping only; hard
    # validity and need resolution remain authoritative elsewhere.
    return enriched or [
        {
            **dict(option),
            "recent_usage": {
                "recent_uses": int((usage.get((str(option.get("action")), option.get("target") if isinstance(option.get("target"), str) else None)) or {}).get("recent_uses", 0)),
                "last_used_sim_time": (usage.get((str(option.get("action")), option.get("target") if isinstance(option.get("target"), str) else None)) or {}).get("last_used_sim_time"),
                "recently_repeated": bool((usage.get((str(option.get("action")), option.get("target") if isinstance(option.get("target"), str) else None)) or {}).get("recently_repeated", False)),
                "event_distance": (usage.get((str(option.get("action")), option.get("target") if isinstance(option.get("target"), str) else None)) or {}).get("event_distance"),
            },
        }
        for option in options
    ]


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
