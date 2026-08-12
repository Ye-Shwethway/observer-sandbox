from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize, status


def test_initialize_and_status(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    result = status(db)
    assert result.healthy is True
    assert result.schema_version == 1
    assert result.runtime_state["paused"] is False
    assert result.runtime_state["speed"] == 1.0
    assert result.runtime_state["world_id"] == "home"

    with connect(db) as conn:
        tables = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
    assert {"entities", "relations", "fields", "events", "runtime_state"} <= tables
