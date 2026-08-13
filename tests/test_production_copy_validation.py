from __future__ import annotations

import importlib.util
import sqlite3
from pathlib import Path


def _load_helper():
    helper_path = Path(__file__).parents[1] / "scripts" / "validation" / "production_copy.py"
    spec = importlib.util.spec_from_file_location("production_copy", helper_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_live_connection_is_structurally_read_only(tmp_path):
    helper = _load_helper()
    live = tmp_path / "live.sqlite3"
    conn = sqlite3.connect(live)
    conn.execute("CREATE TABLE sample (value TEXT NOT NULL)")
    conn.execute("INSERT INTO sample(value) VALUES ('live')")
    conn.commit()
    conn.close()

    ro = helper.open_live_read_only(live)
    try:
        assert ro.execute("SELECT value FROM sample").fetchone()[0] == "live"
        try:
            ro.execute("INSERT INTO sample(value) VALUES ('forbidden')")
        except sqlite3.OperationalError:
            pass
        else:
            raise AssertionError("read-only connection unexpectedly accepted a write")
    finally:
        ro.close()


def test_disposable_copy_is_writable_and_isolated(tmp_path):
    helper = _load_helper()
    live = tmp_path / "live.sqlite3"
    conn = sqlite3.connect(live)
    conn.execute("CREATE TABLE sample (value TEXT NOT NULL)")
    conn.execute("INSERT INTO sample(value) VALUES ('live')")
    conn.commit()
    conn.close()

    with helper.disposable_production_copy(live) as copy_path:
        copied = sqlite3.connect(copy_path)
        copied.execute("INSERT INTO sample(value) VALUES ('copy-only')")
        copied.commit()
        assert copied.execute("SELECT COUNT(*) FROM sample").fetchone()[0] == 2
        copied.close()

        original = sqlite3.connect(live)
        assert original.execute("SELECT COUNT(*) FROM sample").fetchone()[0] == 1
        original.close()

    assert not copy_path.exists()
