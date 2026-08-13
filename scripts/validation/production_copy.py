from __future__ import annotations

import os
import sqlite3
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


def open_live_read_only(path: str | Path) -> sqlite3.Connection:
    """Open production SQLite with no write capability."""
    resolved = Path(path).expanduser().resolve()
    conn = sqlite3.connect(f"{resolved.as_uri()}?mode=ro", uri=True)
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


def copy_production_db(live_db: str | Path, destination: str | Path) -> Path:
    """Create one consistent writable snapshot using SQLite's backup API."""
    live_path = Path(live_db).expanduser().resolve()
    copy_path = Path(destination).expanduser().resolve()
    if live_path == copy_path:
        raise ValueError("disposable copy path must differ from live production")
    if not live_path.is_file():
        raise FileNotFoundError(live_path)

    copy_path.parent.mkdir(parents=True, exist_ok=True)
    _remove_sqlite_files(copy_path)

    with open_live_read_only(live_path) as source:
        destination_conn = sqlite3.connect(copy_path)
        try:
            source.backup(destination_conn)
            integrity = destination_conn.execute("PRAGMA integrity_check").fetchone()
            if not integrity or integrity[0] != "ok":
                raise RuntimeError(f"disposable copy integrity check failed: {integrity!r}")
            destination_conn.commit()
        finally:
            destination_conn.close()

    return copy_path


@contextmanager
def disposable_production_copy(live_db: str | Path) -> Iterator[Path]:
    """Yield a temporary writable snapshot and always clean it up.

    Production may continue advancing autonomously while validation runs. Safety
    is therefore guaranteed by structural read-only access to live SQLite, not
    by requiring before/after live state to remain identical.
    """
    fd, tmp_name = tempfile.mkstemp(prefix="observer-production-copy-", suffix=".sqlite3")
    os.close(fd)
    copy_path = Path(tmp_name)
    try:
        yield copy_production_db(live_db, copy_path)
    finally:
        _remove_sqlite_files(copy_path)
