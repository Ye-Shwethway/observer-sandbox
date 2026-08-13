from __future__ import annotations

import json
import sqlite3
from collections import Counter
from typing import Any

from .simulation import action_definition, local_objects, reachable_rooms
from .training_methods import training_profile_for_target


def _action_definitions(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    return [
        action_definition(conn, row["action_type"])
        for row in conn.execute("SELECT action_type FROM action_definitions ORDER BY action_type")
    ]


def reachable_location_awareness(conn: sqlite3.Connection, room_id: str) -> list[dict[str, Any]]:
    """Describe one-hop destinations without making distant objects directly actionable."""
    definitions = _action_definitions(conn)
    result: list[dict[str, Any]] = []
    for room in reachable_rooms(conn, room_id):
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
                "id": obj["id"],
                "name": obj["name"],
                "actions": sorted(supported),
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
            "location": room["id"],
            "location_name": room["name"],
            "available_actions_after_move": sorted(action_names),
            "training_families": sorted(training_families),
            "training_methods": training_methods,
            "resources": resources,
            "instruction": "Move here first before selecting any listed resource.",
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
