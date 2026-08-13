#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
import sqlite3


def main() -> int:
    assert os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") == "1"
    db = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    assert "/tmp/observer-validation-" in str(db)
    assert "/var/lib/observer-sandbox/" not in str(db)

    conn = sqlite3.connect(str(db))
    try:
        schema = conn.execute("PRAGMA user_version").fetchone()[0]
        row = conn.execute("SELECT value_json FROM runtime_state WHERE key='sim_time'").fetchone()
        assert row is not None
        conn.execute("CREATE TEMP TABLE validation_protocol_probe (note TEXT NOT NULL)")
        conn.execute("INSERT INTO validation_protocol_probe(note) VALUES (?)", ("disposable-copy-write",))
        probe = conn.execute("SELECT COUNT(*) FROM validation_protocol_probe").fetchone()[0]
        assert probe == 1
    finally:
        conn.close()

    forbidden = [
        name for name in os.environ
        if name.startswith("OBSERVER_") and any(marker in name for marker in ("API_KEY", "TOKEN", "SECRET", "PASSWORD"))
    ]
    assert not forbidden, forbidden

    print(json.dumps({
        "ok": True,
        "protocol_selftest": True,
        "disposable_copy_accessible": True,
        "live_path_exposed_to_validator": False,
        "sensitive_observer_env_exposed": False,
        "schema_user_version": schema,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
