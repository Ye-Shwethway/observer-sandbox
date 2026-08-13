from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path

LIVE_PATH = Path("/var/lib/observer-sandbox/observer.sqlite3")


def main() -> int:
    db_value = os.environ.get("OBSERVER_SANDBOX_DB")
    if not db_value:
        raise SystemExit("OBSERVER_SANDBOX_DB is required")
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise SystemExit("disposable validation marker is missing")

    db_path = Path(db_value).resolve()
    if db_path == LIVE_PATH:
        raise SystemExit("validator was given the live production database")

    conn = sqlite3.connect(db_path)
    try:
        schema = conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()
        if not schema:
            raise AssertionError("copied production schema metadata is missing")
        entity_count = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
        event_count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        conn.execute("CREATE TABLE _validation_protocol_probe (id INTEGER PRIMARY KEY, marker TEXT NOT NULL)")
        conn.execute("INSERT INTO _validation_protocol_probe(marker) VALUES (?)", ("disposable-copy-only",))
        conn.commit()
        marker = conn.execute("SELECT marker FROM _validation_protocol_probe").fetchone()[0]
        if marker != "disposable-copy-only":
            raise AssertionError("copy mutation probe did not persist on the disposable database")
    finally:
        conn.close()

    print(json.dumps({
        "ok": True,
        "validator": "production-copy-protocol-v1",
        "schema_version": schema[0],
        "copied_entity_count": entity_count,
        "copied_event_count": event_count,
        "copy_mutation_probe": True,
        "production_path_received": False,
        "model_calls": 0,
        "telegram_calls": 0,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
