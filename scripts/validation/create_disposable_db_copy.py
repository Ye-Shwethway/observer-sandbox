#!/usr/bin/env python3
"""Create a disposable SQLite backup from a read-only source database."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sqlite3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    args = parser.parse_args()

    source_path = args.source.resolve()
    destination_path = args.destination.resolve()
    if not source_path.is_file():
        raise SystemExit(f"source database not found: {source_path}")
    if source_path == destination_path:
        raise SystemExit("source and destination must differ")

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    if destination_path.exists():
        destination_path.unlink()

    source = sqlite3.connect(f"file:{source_path}?mode=ro", uri=True)
    target = sqlite3.connect(str(destination_path))
    try:
        source.backup(target)
        target.commit()
    finally:
        target.close()
        source.close()

    check = sqlite3.connect(str(destination_path))
    try:
        check.execute("PRAGMA quick_check").fetchone()
        user_version = check.execute("PRAGMA user_version").fetchone()[0]
    finally:
        check.close()

    print(json.dumps({
        "ok": True,
        "source_open_mode": "ro",
        "destination": str(destination_path),
        "schema_user_version": user_version,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
