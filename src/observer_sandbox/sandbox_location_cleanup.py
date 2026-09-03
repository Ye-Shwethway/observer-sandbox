from __future__ import annotations

import json
import sqlite3
from typing import Any

from .creation_sandbox import canonical_state_fingerprint, get_sandbox_object
from .sandbox_location_operations import location_source_fingerprint
from .sandbox_location_v2 import get_sandbox_location_v2


class SandboxLocationCleanupError(ValueError):
    pass


def _loads(value: Any, fallback: Any) -> Any:
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return fallback


def _name_from_identity_json(raw: Any, fallback: str) -> str:
    value = _loads(raw, {})
    return str(value.get("name") or fallback) if isinstance(value, dict) else fallback


def location_delete_dependencies(conn: sqlite3.Connection, object_id: str) -> list[dict[str, str]]:
    """Return active Sandbox objects whose authoritative state depends on a Location.

    Location deletion is intentionally fail-closed. We never cascade through active
    Characters, Items or other Locations because doing so would silently rewrite a
    Creator-authored graph.
    """

    try:
        target = get_sandbox_location_v2(conn, object_id)
    except Exception as exc:
        raise SandboxLocationCleanupError(str(exc)) from exc
    if target["lifecycle_status"] != "active":
        raise SandboxLocationCleanupError("Location cleanup target must be active")
    sandbox_id = str(target["sandbox_id"])

    dependencies: dict[tuple[str, str], dict[str, str]] = {}

    # Non-Location objects express placement/ownership/etc. through resolved
    # relations. Any active incoming relation makes deletion unsafe.
    rows = conn.execute(
        """
        SELECT o.object_id,o.creation_type,o.identity_json,r.relation_type
        FROM creation_sandbox_relations r
        JOIN creation_sandbox_objects o
          ON o.object_id=r.source_object_id AND o.sandbox_id=r.sandbox_id
        WHERE r.sandbox_id=? AND r.target_object_id=?
          AND o.object_id<>? AND o.lifecycle_status='active'
          AND o.creation_type<>'location'
        ORDER BY o.created_at,o.object_id,r.id
        """,
        (sandbox_id, object_id, object_id),
    ).fetchall()
    for row in rows:
        source_id = str(row["object_id"])
        relation = str(row["relation_type"])
        key = (source_id, relation)
        dependencies[key] = {
            "object_id": source_id,
            "creation_type": str(row["creation_type"]),
            "name": _name_from_identity_json(row["identity_json"], source_id),
            "reason": relation.replace("_", " "),
        }

    # Runtime actor placement is checked independently so a damaged/missing
    # relation projection can never make a Location appear deletable.
    runtime_rows = conn.execute(
        """
        SELECT o.object_id,o.creation_type,o.identity_json
        FROM creation_sandbox_actor_runtime a
        JOIN creation_sandbox_objects o ON o.object_id=a.object_id
        WHERE a.sandbox_id=? AND a.current_location_object_id=?
          AND o.lifecycle_status='active'
        ORDER BY o.created_at,o.object_id
        """,
        (sandbox_id, object_id),
    ).fetchall()
    for row in runtime_rows:
        source_id = str(row["object_id"])
        key = (source_id, "runtime_location")
        dependencies[key] = {
            "object_id": source_id,
            "creation_type": str(row["creation_type"]),
            "name": _name_from_identity_json(row["identity_json"], source_id),
            "reason": "runtime current location",
        }

    # Location-to-Location authority lives in exact source_json. Scan that source
    # rather than relying only on relation projections, because directionality and
    # economic/control references are not all represented by the same row shape.
    location_rows = conn.execute(
        """
        SELECT p.object_id,p.source_json,o.identity_json
        FROM creation_sandbox_location_profiles p
        JOIN creation_sandbox_objects o ON o.object_id=p.object_id
        WHERE p.sandbox_id=? AND p.object_id<>? AND o.lifecycle_status='active'
        ORDER BY o.created_at,o.object_id
        """,
        (sandbox_id, object_id),
    ).fetchall()
    for row in location_rows:
        source_id = str(row["object_id"])
        source = _loads(row["source_json"], {})
        if not isinstance(source, dict):
            continue
        name = _name_from_identity_json(row["identity_json"], source_id)
        reasons: list[str] = []
        structure = source.get("structure") if isinstance(source.get("structure"), dict) else {}
        if str(structure.get("parent_ref") or "") == object_id:
            reasons.append("structural parent")
        topology = source.get("topology") if isinstance(source.get("topology"), dict) else {}
        interfaces = topology.get("interfaces") if isinstance(topology.get("interfaces"), list) else []
        if any(isinstance(item, dict) and str(item.get("destination_ref") or "") == object_id for item in interfaces):
            reasons.append("topology destination")
        control = source.get("control") if isinstance(source.get("control"), dict) else {}
        if str(control.get("owner_ref") or "") == object_id:
            reasons.append("owner reference")
        if str(control.get("operator_ref") or "") == object_id:
            reasons.append("operator reference")
        economic = source.get("economic_policy") if isinstance(source.get("economic_policy"), dict) else {}
        if str(economic.get("included_in_parent_ref") or "") == object_id:
            reasons.append("economic parent")
        for reason in reasons:
            dependencies[(source_id, reason)] = {
                "object_id": source_id,
                "creation_type": "location",
                "name": name,
                "reason": reason,
            }

    return list(dependencies.values())


def delete_sandbox_location_v2(
    conn: sqlite3.Connection,
    object_id: str,
    *,
    expected_source_fingerprint: str,
) -> dict[str, Any]:
    location = get_sandbox_location_v2(conn, object_id)
    if location["lifecycle_status"] != "active":
        raise SandboxLocationCleanupError("Location cleanup target must be active")
    actual_fingerprint = location_source_fingerprint(location["source"])
    if str(expected_source_fingerprint or "") != actual_fingerprint:
        raise SandboxLocationCleanupError("Location changed since delete review; review the latest approved state")

    dependencies = location_delete_dependencies(conn, object_id)
    if dependencies:
        raise SandboxLocationCleanupError(
            f"Location still has {len(dependencies)} active dependency reference(s); detach or edit them before deleting"
        )

    obj = get_sandbox_object(conn, object_id)
    sandbox_id = str(obj["sandbox_id"])
    name = str(obj.get("identity", {}).get("name") or object_id)
    canonical_before = canonical_state_fingerprint(conn)

    savepoint = "sandbox_location_delete"
    conn.execute(f"SAVEPOINT {savepoint}")
    try:
        conn.execute(
            """
            INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json)
            VALUES(?,?, 'sandbox_location_v2_deleted', ?)
            """,
            (
                sandbox_id,
                object_id,
                json.dumps(
                    {
                        "name": name,
                        "source_fingerprint": actual_fingerprint,
                        "runtime_started": False,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ),
            ),
        )
        conn.execute(
            "DELETE FROM creation_sandbox_relations WHERE sandbox_id=? AND (source_object_id=? OR target_object_id=?)",
            (sandbox_id, object_id, object_id),
        )
        conn.execute(
            "DELETE FROM creation_sandbox_location_profiles WHERE sandbox_id=? AND object_id=?",
            (sandbox_id, object_id),
        )
        conn.execute(
            "DELETE FROM creation_sandbox_objects WHERE sandbox_id=? AND object_id=?",
            (sandbox_id, object_id),
        )
        if canonical_state_fingerprint(conn) != canonical_before:
            raise SandboxLocationCleanupError("Canonical Real World changed during Sandbox Location delete")
        conn.execute(f"RELEASE SAVEPOINT {savepoint}")
        conn.commit()
    except Exception:
        conn.execute(f"ROLLBACK TO SAVEPOINT {savepoint}")
        conn.execute(f"RELEASE SAVEPOINT {savepoint}")
        raise

    return {
        "object_id": object_id,
        "name": name,
        "sandbox_id": sandbox_id,
        "deleted": True,
        "canonical_unchanged": True,
    }


__all__ = [
    "SandboxLocationCleanupError",
    "delete_sandbox_location_v2",
    "location_delete_dependencies",
]
