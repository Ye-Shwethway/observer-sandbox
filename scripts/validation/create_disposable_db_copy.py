#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from production_copy import copy_production_db


def main() -> int:
    parser = argparse.ArgumentParser(description="Create one disposable SQLite snapshot from live production")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    args = parser.parse_args()

    destination = copy_production_db(args.source, args.destination)
    print(json.dumps({
        "ok": True,
        "source_access": "sqlite-mode-ro-query-only",
        "copy_backend": "sqlite-backup-api",
        "destination": str(destination),
        "production_mutated_by_validation": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
