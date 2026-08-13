from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .ai import seed_builtin_providers
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


def initialize(db_path: str | Path) -> None:
    with connect(db_path) as conn:
        migrate(conn)
        seed_builtin_providers(conn)
        seed_profile_field_definitions(conn)
        seed_source_union_extensions(conn)
        seed_sexual_state_fields(conn)
        seed_home_and_darian(conn)
        defaults = {
            "paused": False,
            "speed": 1.0,
            "world_id": "observer_universe",
            "autonomy_enabled": False,
        }
        for key, value in defaults.items():
            conn.execute(
                "INSERT OR IGNORE INTO runtime_state(key, value_json) VALUES(?, ?)",
                (key, json.dumps(value)),
            )

        # One-time semantic migration from the original P1 world root. `home`
        # remains a stable entity id, but now represents the Thorne Estate
        # location node beneath the generic Observer Universe root.
        row = conn.execute("SELECT value_json FROM runtime_state WHERE key='world_id'").fetchone()
        if row is not None and json.loads(row[0]) == "home":
            conn.execute(
                "UPDATE runtime_state SET value_json=?, updated_at=CURRENT_TIMESTAMP WHERE key='world_id'",
                (json.dumps("observer_universe"),),
            )
        conn.commit()


def status(db_path: str | Path) -> RuntimeStatus:
    with connect(db_path) as conn:
        migrate(conn)
        seed_builtin_providers(conn)
        seed_profile_field_definitions(conn)
        seed_source_union_extensions(conn)
        seed_sexual_state_fields(conn)
        seed_home_and_darian(conn)
        version = int(conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()[0])
        return RuntimeStatus(
            healthy=True,
            schema_version=version,
            runtime_state=get_runtime_state(conn),
            checked_at=datetime.now(timezone.utc).isoformat(),
        )
