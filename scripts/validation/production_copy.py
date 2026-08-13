from __future__ import annotations

import os
import sqlite3
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


def open_live_read_only(path: str | Path) -> sqlite3.Connection:
    """Open production SQLite through a structurally read-only connection."""
    resolved = Path(path).expanduser().resolve()
    uri = f"{resolved.as_uri()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON")
    return conn


def _remove_sqlite_files(path: Path) -> None:
    for suffix in ("", "-wal", "-shm"):
        candidate = Path(f"{path}{suffix}")
        try:
            candidate.unlink()
        except FileNotFoundError:
            pass


@contextmanager
def disposable_production_copy(live_db: str | Path) -> Iterator[Path]:
    """Yield a writable temporary SQLite snapshot copied from live production.

    The live database is opened only with SQLite mode=ro + query_only. SQLite's
    backup API creates a transactionally consistent snapshot even while the
    autonomous production service continues to advance normally.
    """
    live_path = Path(live_db).expanduser().resolve()
    fd, tmp_name = tempfile.mkstemp(prefix="observer-production-copy-", suffix=".sqlite3")
    os.close(fd)
    copy_path = Path(tmp_name)

    try:
        with open_live_read_only(live_path) as source:
            destination = sqlite3.connect(copy_path)
            try:
                source.backup(destination)
                integrity = destination.execute("PRAGMA integrity_check").fetchone()
                if not integrity or integrity[0] != "ok":
                    raise RuntimeError(f"disposable copy integrity check failed: {integrity!r}")
                destination.commit()
            finally:
                destination.close()

        if copy_path == live_path:
            raise RuntimeError("disposable copy resolved to the live production path")

        yield copy_path
    finally:
        _remove_sqlite_files(copy_path)
