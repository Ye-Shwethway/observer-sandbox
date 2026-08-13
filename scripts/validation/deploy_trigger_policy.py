from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

RUNTIME_PATH_PREFIXES = (
    "src/",
    "config/",
)
RUNTIME_PATHS = {
    "pyproject.toml",
    "deploy/observer-sandbox.service",
}
RELEASE_MARKER = "deploy/RELEASE"


def _changed_paths(event: dict[str, Any]) -> set[str]:
    changed: set[str] = set()
    for commit in event.get("commits") or []:
        for key in ("added", "modified", "removed"):
            values = commit.get(key) or []
            changed.update(str(value) for value in values)
    return changed


def is_runtime_path(path: str) -> bool:
    return path in RUNTIME_PATHS or any(path.startswith(prefix) for prefix in RUNTIME_PATH_PREFIXES)


def authorize(event_name: str, event: dict[str, Any]) -> dict[str, Any]:
    if event_name == "workflow_dispatch":
        return {"authorized": True, "reason": "manual_dispatch", "changed_paths": []}

    if event_name != "push":
        return {"authorized": False, "reason": "unsupported_event", "changed_paths": []}

    changed = sorted(_changed_paths(event))
    changed_set = set(changed)
    if changed_set and changed_set <= {RELEASE_MARKER}:
        return {"authorized": True, "reason": "release_marker", "changed_paths": changed}

    runtime_changed = any(is_runtime_path(path) for path in changed)
    if not runtime_changed:
        return {"authorized": False, "reason": "no_runtime_change", "changed_paths": changed}

    message = str((event.get("head_commit") or {}).get("message") or "")
    if not message.startswith("Merge pull request #"):
        return {"authorized": False, "reason": "runtime_push_not_merged_pr", "changed_paths": changed}

    return {"authorized": True, "reason": "merged_runtime_pr", "changed_paths": changed}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", required=True)
    parser.add_argument("--event-name", required=True)
    args = parser.parse_args()

    event = json.loads(Path(args.event).read_text(encoding="utf-8"))
    result = authorize(args.event_name, event)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["authorized"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
