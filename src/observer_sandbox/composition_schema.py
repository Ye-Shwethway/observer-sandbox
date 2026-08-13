from __future__ import annotations

import json
import sqlite3
from typing import Any


COMPOSITION_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS entity_definitions (
    id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL,
    name TEXT NOT NULL,
    capabilities_json TEXT NOT NULL DEFAULT '[]',
    properties_json TEXT NOT NULL DEFAULT '{}',
    effects_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS action_definitions (
    action_type TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    min_duration_minutes INTEGER NOT NULL,
    max_duration_minutes INTEGER NOT NULL,
    target_mode TEXT NOT NULL CHECK(target_mode IN ('none','optional','object','location')),
    required_capability TEXT,
    requires_colocation INTEGER NOT NULL DEFAULT 0 CHECK(requires_colocation IN (0,1)),
    base_effects_json TEXT NOT NULL DEFAULT '{}',
    conditions_json TEXT NOT NULL DEFAULT '{}',
    modifiers_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS action_instances (
    id TEXT PRIMARY KEY,
    action_type TEXT NOT NULL REFERENCES action_definitions(action_type),
    actor_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    place_id TEXT REFERENCES entities(id) ON DELETE SET NULL,
    target_id TEXT REFERENCES entities(id) ON DELETE SET NULL,
    status TEXT NOT NULL CHECK(status IN ('planned','in_progress','completed','failed','cancelled')),
    duration_minutes INTEGER NOT NULL,
    intent TEXT,
    participants_json TEXT NOT NULL DEFAULT '[]',
    resources_json TEXT NOT NULL DEFAULT '[]',
    conditions_json TEXT NOT NULL DEFAULT '{}',
    modifiers_json TEXT NOT NULL DEFAULT '{}',
    planned_sim_time TEXT NOT NULL,
    started_sim_time TEXT,
    ended_sim_time TEXT,
    planned_wall_time REAL,
    due_wall_time REAL,
    speed_at_plan REAL,
    outcome_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS action_participants (
    action_id TEXT NOT NULL REFERENCES action_instances(id) ON DELETE CASCADE,
    entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    role TEXT NOT NULL DEFAULT 'participant',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    PRIMARY KEY(action_id, entity_id, role)
);

CREATE TABLE IF NOT EXISTS actor_runtime (
    actor_id TEXT PRIMARY KEY REFERENCES entities(id) ON DELETE CASCADE,
    autonomy_enabled INTEGER NOT NULL DEFAULT 0 CHECK(autonomy_enabled IN (0,1)),
    autonomy_mode TEXT NOT NULL DEFAULT 'normal',
    pending_action_id TEXT REFERENCES action_instances(id) ON DELETE SET NULL,
    lease_owner TEXT,
    lease_expires_at REAL,
    retry_failures INTEGER NOT NULL DEFAULT 0,
    retry_after REAL,
    retry_last_error TEXT,
    cognition_stats_json TEXT NOT NULL DEFAULT '{}',
    wake_reason TEXT,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS active_modifiers (
    id TEXT PRIMARY KEY,
    subject_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    source_entity_id TEXT REFERENCES entities(id) ON DELETE SET NULL,
    source_action_id TEXT REFERENCES action_instances(id) ON DELETE SET NULL,
    field_key TEXT NOT NULL,
    operation TEXT NOT NULL CHECK(operation IN ('add','multiply','set','clamp_min','clamp_max')),
    value_json TEXT NOT NULL,
    starts_sim_time TEXT NOT NULL,
    ends_sim_time TEXT,
    stack_key TEXT,
    stack_policy TEXT NOT NULL DEFAULT 'replace' CHECK(stack_policy IN ('replace','stack','max','min')),
    conditions_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS event_participants (
    event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    role TEXT NOT NULL DEFAULT 'participant',
    PRIMARY KEY(event_id, entity_id, role)
);

CREATE INDEX IF NOT EXISTS idx_action_instances_actor_status ON action_instances(actor_id, status);
CREATE INDEX IF NOT EXISTS idx_action_instances_place_time ON action_instances(place_id, planned_sim_time);
CREATE INDEX IF NOT EXISTS idx_active_modifiers_subject_time ON active_modifiers(subject_id, starts_sim_time, ends_sim_time);
CREATE INDEX IF NOT EXISTS idx_event_participants_entity ON event_participants(entity_id, event_id);
"""


ACTION_DEFINITIONS: tuple[dict[str, Any], ...] = (
    {"action_type": "move", "label": "Move", "min": 1, "max": 30, "target_mode": "location", "capability": None, "colocation": 0},
    {"action_type": "sleep", "label": "Sleep", "min": 30, "max": 720, "target_mode": "object", "capability": "sleep", "colocation": 1},
    {"action_type": "eat", "label": "Eat", "min": 5, "max": 90, "target_mode": "object", "capability": "eat", "colocation": 1},
    {"action_type": "drink", "label": "Drink", "min": 1, "max": 30, "target_mode": "object", "capability": "drink", "colocation": 1},
    {"action_type": "shower", "label": "Shower", "min": 5, "max": 60, "target_mode": "object", "capability": "shower", "colocation": 1},
    {"action_type": "rest", "label": "Rest", "min": 5, "max": 240, "target_mode": "optional", "capability": "rest", "colocation": 1},
    {"action_type": "inspect", "label": "Inspect", "min": 1, "max": 60, "target_mode": "object", "capability": "inspect", "colocation": 1},
    {"action_type": "use", "label": "Use", "min": 1, "max": 120, "target_mode": "object", "capability": "use", "colocation": 1},
    {"action_type": "train", "label": "Train", "min": 10, "max": 240, "target_mode": "object", "capability": "train", "colocation": 1},
    {"action_type": "read", "label": "Read", "min": 5, "max": 240, "target_mode": "object", "capability": "read", "colocation": 1},
    {"action_type": "research", "label": "Research", "min": 10, "max": 180, "target_mode": "object", "capability": "research", "colocation": 1},
    {"action_type": "idle", "label": "Idle", "min": 1, "max": 120, "target_mode": "none", "capability": None, "colocation": 0},
)


def _columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}


def migrate_composition_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(COMPOSITION_SCHEMA_SQL)
    event_columns = _columns(conn, "events")
    for column, sql_type in (
        ("event_uuid", "TEXT"),
        ("action_id", "TEXT"),
        ("location_id", "TEXT"),
        ("caused_by_event_id", "INTEGER"),
        ("state_changes_json", "TEXT NOT NULL DEFAULT '{}'"),
    ):
        if column not in event_columns:
            conn.execute(f"ALTER TABLE events ADD COLUMN {column} {sql_type}")
    entity_columns = _columns(conn, "entities")
    if "definition_id" not in entity_columns:
        conn.execute("ALTER TABLE entities ADD COLUMN definition_id TEXT")
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_events_uuid ON events(event_uuid) WHERE event_uuid IS NOT NULL")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_events_action ON events(action_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_events_location_time ON events(location_id, sim_time)")
    conn.commit()


def seed_action_definitions(conn: sqlite3.Connection) -> None:
    for row in ACTION_DEFINITIONS:
        conn.execute(
            """INSERT INTO action_definitions(
                action_type,label,min_duration_minutes,max_duration_minutes,target_mode,
                required_capability,requires_colocation,base_effects_json,conditions_json,modifiers_json,metadata_json
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(action_type) DO UPDATE SET
                label=excluded.label,
                min_duration_minutes=excluded.min_duration_minutes,
                max_duration_minutes=excluded.max_duration_minutes,
                target_mode=excluded.target_mode,
                required_capability=excluded.required_capability,
                requires_colocation=excluded.requires_colocation,
                updated_at=CURRENT_TIMESTAMP""",
            (
                row["action_type"], row["label"], row["min"], row["max"], row["target_mode"],
                row["capability"], row["colocation"], json.dumps({}), json.dumps({}), json.dumps({}), json.dumps({}),
            ),
        )
    conn.commit()


def ensure_actor_runtime(conn: sqlite3.Connection, actor_id: str) -> None:
    conn.execute("INSERT OR IGNORE INTO actor_runtime(actor_id) VALUES(?)", (actor_id,))
    conn.commit()
