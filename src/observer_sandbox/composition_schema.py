from __future__ import annotations

import json
import sqlite3
from typing import Any


TRAINING_FATIGUE_LIMIT = 70.0

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

CREATE TABLE IF NOT EXISTS inventory_stacks (
    entity_id TEXT PRIMARY KEY REFERENCES entities(id) ON DELETE CASCADE,
    quantity REAL NOT NULL CHECK(quantity >= 0),
    unit TEXT NOT NULL,
    seed_revision TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_action_instances_actor_status ON action_instances(actor_id, status);
CREATE INDEX IF NOT EXISTS idx_action_instances_place_time ON action_instances(place_id, planned_sim_time);
CREATE INDEX IF NOT EXISTS idx_active_modifiers_subject_time ON active_modifiers(subject_id, starts_sim_time, ends_sim_time);
CREATE INDEX IF NOT EXISTS idx_event_participants_entity ON event_participants(entity_id, event_id);
CREATE INDEX IF NOT EXISTS idx_inventory_stacks_quantity ON inventory_stacks(quantity);
"""


def _definition(
    action_type: str,
    label: str,
    minimum: int,
    maximum: int,
    target_mode: str,
    capability: str | None,
    colocation: int,
    *,
    conditions: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "action_type": action_type,
        "label": label,
        "min": minimum,
        "max": maximum,
        "target_mode": target_mode,
        "capability": capability,
        "colocation": colocation,
        "conditions": conditions or {},
    }


ACTION_DEFINITIONS: tuple[dict[str, Any], ...] = (
    _definition("move", "Move", 1, 30, "location", None, 0),
    _definition("sleep", "Sleep", 30, 720, "object", "sleep", 1),
    _definition("eat", "Eat", 5, 90, "object", "eat", 1),
    _definition("drink", "Drink", 1, 30, "object", "drink", 1),
    _definition("shower", "Shower", 5, 60, "object", "shower", 1),
    _definition("rest", "Rest", 5, 240, "optional", "rest", 1),
    _definition("inspect", "Inspect", 1, 60, "object", "inspect", 1),
    _definition("use", "Use", 1, 120, "object", "use", 1),
    _definition(
        "train",
        "Train",
        10,
        240,
        "object",
        "train",
        1,
        conditions={
            "all": [
                {
                    "field_key": "physiology.fatigue",
                    "operator": "lt",
                    "value": TRAINING_FATIGUE_LIMIT,
                }
            ]
        },
    ),
    _definition("read", "Read", 5, 240, "object", "read", 1),
    _definition("research", "Research", 10, 180, "object", "research", 1),
    _definition("monitor", "Monitor", 5, 120, "object", "monitor", 1),
    _definition("self_satisfaction", "Private self-satisfaction", 5, 45, "none", None, 0),
    _definition("idle", "Idle", 1, 120, "none", None, 0),
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
                conditions_json=excluded.conditions_json,
                updated_at=CURRENT_TIMESTAMP""",
            (
                row["action_type"], row["label"], row["min"], row["max"], row["target_mode"],
                row["capability"], row["colocation"], json.dumps({}), json.dumps(row["conditions"]), json.dumps({}), json.dumps({}),
            ),
        )
    conn.commit()


def ensure_actor_runtime(conn: sqlite3.Connection, actor_id: str) -> None:
    conn.execute("INSERT OR IGNORE INTO actor_runtime(actor_id) VALUES(?)", (actor_id,))
    conn.commit()
