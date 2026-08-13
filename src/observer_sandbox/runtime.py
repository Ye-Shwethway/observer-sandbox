from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .actor_runtime import actor_runtime, migrate_legacy_actor_runtime
from .ai import seed_builtin_providers
from .composition_schema import seed_action_definitions
from .db import connect, get_runtime_state, migrate
from .profile_schema import seed_profile_field_definitions
from .profile_schema_source_union import seed_source_union_extensions
from .sexual_state_schema import seed_sexual_state_fields
from .world import seed_home_and_darian


@dataclass(slots=True)
class RuntimeStatus:
    healthy: bool
    schema_version: int
    runtime_state: dict[str, object]
    checked_at: str

    def to_dict(self) -> dict[str, object]:
        return {
            "healthy": self.healthy,
            "schema_version": self.schema_version,
            "runtime_state": self.runtime_state,
            "checked_at": self.checked_at,
        }


def _initialize_conn(conn) -> None:
    migrate(conn)
    seed_builtin_providers(conn)
    seed_profile_field_definitions(conn)
    seed_source_union_extensions(conn)
    seed_sexual_state_fields(conn)
    seed_home_and_darian(conn)
    seed_action_definitions(conn)
    defaults = {
        "paused": False,
        "speed": 1.0,
        "world_id": "world_observer_universe",
    }
    for key, value in defaults.items():
        conn.execute(
            "INSERT OR IGNORE INTO runtime_state(key, value_json) VALUES(?, ?)",
            (key, json.dumps(value)),
        )
    conn.commit()
    migrate_legacy_actor_runtime(conn, "char_darian")


def initialize(db_path: str | Path) -> None:
    with connect(db_path) as conn:
        _initialize_conn(conn)


def status(db_path: str | Path) -> RuntimeStatus:
    with connect(db_path) as conn:
        _initialize_conn(conn)
        version = int(conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()[0])
        runtime = get_runtime_state(conn)
        darian = actor_runtime(conn, "char_darian")
        # Compatibility projection for operational/readback surfaces. Actor-owned
        # state is authoritative in actor_runtime; these fields are not persisted
        # back into global runtime_state.
        runtime.update({
            "autonomy_enabled": darian["autonomy_enabled"],
            "autonomy_mode": darian["autonomy_mode"],
            "autonomy_pending_action_id": darian["pending_action_id"],
            "autonomy_retry": darian["retry"],
            "cognition_wake_reason": darian["wake_reason"],
            "cognition_wake_stats": darian["cognition_stats"],
        })
        return RuntimeStatus(
            healthy=True,
            schema_version=version,
            runtime_state=runtime,
            checked_at=datetime.now(timezone.utc).isoformat(),
        )
