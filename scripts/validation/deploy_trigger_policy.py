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
            changed.update(str(value) for value in (commit.get(key) or []))
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

    if not any(is_runtime_path(path) for path in changed):
        return {"authorized": False, "reason": "no_runtime_change", "changed_paths": changed}

    message = str((event.get("head_commit") or {}).get("message") or "")
    if not message.startswith("Merge pull request #"):
        return {"authorized": False, "reason": "runtime_push_not_merged_pr", "changed_paths": changed}

    return {"authorized": True, "reason": "merged_runtime_pr", "changed_paths": changed}


def _push(message: str, changed: list[str]) -> dict[str, Any]:
    return {
        "head_commit": {"message": message},
        "commits": [{"added": [], "modified": changed, "removed": []}],
    }


def self_test() -> None:
    assert is_runtime_path("src/observer_sandbox/service.py")
    assert is_runtime_path("config/worlds/home.v1.json")
    assert is_runtime_path("pyproject.toml")
    assert is_runtime_path("deploy/observer-sandbox.service")
    assert not is_runtime_path("docs/ROADMAP.md")
    assert not is_runtime_path("tests/test_example.py")

    assert authorize("workflow_dispatch", {})["reason"] == "manual_dispatch"
    assert authorize("push", _push("release marker", [RELEASE_MARKER]))["reason"] == "release_marker"
    assert authorize("push", _push("Merge pull request #47 from branch", ["src/observer_sandbox/service.py"]))["reason"] == "merged_runtime_pr"
    assert authorize("push", _push("direct hotfix", ["src/observer_sandbox/service.py"]))["reason"] == "runtime_push_not_merged_pr"
    assert authorize("push", _push("Merge pull request #50 from docs", ["docs/ROADMAP.md"]))["reason"] == "no_runtime_change"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event")
    parser.add_argument("--event-name")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print(json.dumps({"ok": True, "self_test": "deploy_trigger_policy_v2"}, sort_keys=True))
        return 0

    if not args.event or not args.event_name:
        parser.error("--event and --event-name are required unless --self-test is used")
    event = json.loads(Path(args.event).read_text(encoding="utf-8"))
    result = authorize(args.event_name, event)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["authorized"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
