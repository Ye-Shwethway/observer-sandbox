from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .runtime import initialize, status

DEFAULT_DB = Path(os.environ.get("OBSERVER_SANDBOX_DB", "runtime-data/observer.sqlite3"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sandboxctl")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("status")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "init":
        initialize(args.db)
        print(json.dumps({"ok": True, "db": str(args.db)}))
    elif args.command == "status":
        print(json.dumps(status(args.db).to_dict(), indent=2, sort_keys=True))
