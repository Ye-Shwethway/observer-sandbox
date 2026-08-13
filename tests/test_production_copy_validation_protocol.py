from __future__ import annotations

import json
from pathlib import Path
import sqlite3
import subprocess
import sys


def test_disposable_copy_helper_preserves_source_and_detaches_copy(tmp_path: Path) -> None:
    source = tmp_path / "source.sqlite3"
    destination = tmp_path / "copy.sqlite3"

    conn = sqlite3.connect(source)
    conn.execute("PRAGMA user_version=4")
    conn.execute("CREATE TABLE sample (id INTEGER PRIMARY KEY, value TEXT NOT NULL)")
    conn.execute("INSERT INTO sample(value) VALUES ('source')")
    conn.commit()
    conn.close()

    script = Path(__file__).parents[1] / "scripts" / "validation" / "create_disposable_db_copy.py"
    completed = subprocess.run(
        [
            sys.executable,
            str(script),
            "--source",
            str(source),
            "--destination",
            str(destination),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    evidence = json.loads(completed.stdout.strip())
    assert evidence["ok"] is True
    assert evidence["source_access"] == "sqlite-mode-ro-query-only"
    assert evidence["copy_backend"] == "sqlite-backup-api"
    assert evidence["production_mutated_by_validation"] is False

    copy_conn = sqlite3.connect(destination)
    copy_conn.execute("UPDATE sample SET value='copy' WHERE id=1")
    copy_conn.commit()
    assert copy_conn.execute("SELECT value FROM sample WHERE id=1").fetchone()[0] == "copy"
    copy_conn.close()

    source_conn = sqlite3.connect(source)
    assert source_conn.execute("PRAGMA user_version").fetchone()[0] == 4
    assert source_conn.execute("SELECT value FROM sample WHERE id=1").fetchone()[0] == "source"
    source_conn.close()
