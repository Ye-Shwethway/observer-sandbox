from __future__ import annotations

import argparse
import glob
import subprocess
from pathlib import Path
from typing import Iterable


FULL_SUITE_EXACT = {
    "pyproject.toml",
    ".github/workflows/ci.yml",
    ".github/workflows/full-regression.yml",
    "src/observer_sandbox/db.py",
    "src/observer_sandbox/runtime.py",
    "src/observer_sandbox/simulation.py",
    "src/observer_sandbox/cli.py",
}
FULL_SUITE_PREFIXES = (
    "src/observer_sandbox/migration",
    "src/observer_sandbox/schema",
)

_LOCATION_EDIT_TESTS = (
    "tests/test_sandbox_location_operations_v2.py",
    "tests/test_telegram_sandbox_location_edit_v1.py",
    "tests/test_telegram_sandbox_location_detail_v1.py",
)

LEAF_SOURCE_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "src/observer_sandbox/telegram_creator_studio_location_composition_extension.py",
        (
            "tests/test_creator_studio_location_composition*.py",
            "tests/test_telegram_creator_studio_location_v2.py",
        ),
    ),
    (
        "src/observer_sandbox/telegram_creator_studio_location_feedback_extension.py",
        (
            "tests/test_creator_studio_location_ai_feedback.py",
            "tests/test_location_ai_contract_v2.py",
            "tests/test_creator_studio_location_v2.py",
        ),
    ),
    (
        "src/observer_sandbox/location_ai_contract.py",
        (
            "tests/test_location_ai_contract_v2.py",
            "tests/test_location_ai_unit_normalization_v2.py",
            "tests/test_creator_studio_location_v2.py",
        ),
    ),
    (
        "src/observer_sandbox/telegram_world_layers_location_extension.py",
        ("tests/test_telegram_sandbox_location_detail_v1.py",),
    ),
    (
        "src/observer_sandbox/telegram_world_layers.py",
        (
            "tests/test_telegram_sandbox_location_detail_v1.py",
            "tests/test_creator_studio_location_composition_navigation.py",
            "tests/test_telegram_sandbox_location_edit_v1.py",
        ),
    ),
    # L11.6 Location Edit is a bounded vertical. Keep changes in its backend,
    # Telegram editor, text adapter and world-layer adapter on the exact edit
    # contract family instead of expanding generic telegram_/sandbox_/location
    # domains across hundreds of unrelated tests.
    ("src/observer_sandbox/sandbox_location_operations.py", _LOCATION_EDIT_TESTS),
    ("src/observer_sandbox/telegram_sandbox_location_edit.py", _LOCATION_EDIT_TESTS),
    ("src/observer_sandbox/telegram_sandbox_location_edit_adapter.py", _LOCATION_EDIT_TESTS),
    ("src/observer_sandbox/telegram_world_layers_location_edit_extension.py", _LOCATION_EDIT_TESTS),
    (
        "src/observer_sandbox/telegram_creator_studio.py",
        (
            "tests/test_telegram_sandbox_location_edit_v1.py",
            "tests/test_creator_studio_location_composition_navigation.py",
            "tests/test_creator_studio_navigation_canonicalization.py",
        ),
    ),
)

DOMAIN_RULES: tuple[tuple[tuple[str, ...], tuple[str, ...]], ...] = (
    (
        ("grading",),
        (
            "tests/test_*grading*.py",
            "tests/test_*grade_target*.py",
            "tests/test_*skill*.py",
            "tests/test_body_*.py",
            "tests/test_telegram_*profile*.py",
            "tests/test_universal_profile_grading_v1.py",
        ),
    ),
    (
        ("body", "physique", "profile_edit", "profile_observer"),
        (
            "tests/test_body_*.py",
            "tests/test_*profile*grading*.py",
            "tests/test_universal_profile_grading_v1.py",
            "tests/test_telegram_*profile*.py",
            "tests/test_*grade_target*.py",
        ),
    ),
    (("telegram_",), ("tests/test_telegram_*.py",)),
    (
        ("creation_sandbox", "sandbox_"),
        (
            "tests/test_creation_sandbox*.py",
            "tests/test_sandbox_*.py",
            "tests/test_telegram_sandbox*.py",
        ),
    ),
    (("inventory",), ("tests/test_*inventory*.py",)),
    (("skill",), ("tests/test_*skill*.py",)),
    (("training", "strength", "adaptation", "progression"), ("tests/test_*training*.py", "tests/test_*strength*.py", "tests/test_*adaptation*.py", "tests/test_*progression*.py")),
    (("physiology", "recovery", "fatigue", "nutrition", "hunger", "thirst", "sleep"), ("tests/test_*physiology*.py", "tests/test_*recovery*.py", "tests/test_*fatigue*.py", "tests/test_*nutrition*.py", "tests/test_*hunger*.py", "tests/test_*thirst*.py", "tests/test_*sleep*.py")),
    (("action", "effect", "modifier"), ("tests/test_*action*.py", "tests/test_*effect*.py", "tests/test_*modifier*.py")),
    (("research", "technology"), ("tests/test_*research*.py", "tests/test_*technology*.py")),
    (("cognition", "mind", "memory", "goal", "planning"), ("tests/test_*cognition*.py", "tests/test_*mind*.py", "tests/test_*memory*.py", "tests/test_*goal*.py", "tests/test_*planning*.py")),
    (("world", "location", "travel", "spatial"), ("tests/test_*world*.py", "tests/test_*location*.py", "tests/test_*travel*.py", "tests/test_*spatial*.py")),
    (("ai",), ("tests/test_ai*.py", "tests/test_*ai_*.py")),
)


def changed_files(base: str, head: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", base, head],
        check=True,
        text=True,
        capture_output=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _expand(patterns: Iterable[str], *, root: Path) -> set[str]:
    selected: set[str] = set()
    for pattern in patterns:
        for path in glob.glob(str(root / pattern)):
            candidate = Path(path)
            if candidate.is_file():
                selected.add(candidate.relative_to(root).as_posix())
    return selected


def _source_tokens(path: str) -> set[str]:
    stem = Path(path).stem.lower()
    ignored = {"v1", "v2", "runtime", "engine", "service", "adapter", "foundation"}
    return {token for token in stem.split("_") if len(token) >= 3 and token not in ignored}


def _leaf_patterns(path: str) -> tuple[str, ...] | None:
    for source_path, patterns in LEAF_SOURCE_RULES:
        if path == source_path:
            return patterns
    return None


def select_tests(paths: Iterable[str], *, root: Path = Path(".")) -> tuple[str, list[str], str]:
    changed = sorted(set(paths))
    if not changed:
        return "full", [], "no changed-file evidence"

    for path in changed:
        if path in FULL_SUITE_EXACT or path.startswith(FULL_SUITE_PREFIXES):
            return "full", [], f"core-risk path changed: {path}"

    selected: set[str] = set()
    unmapped_runtime: list[str] = []

    for path in changed:
        if path.startswith("tests/") and path.endswith(".py") and (root / path).exists():
            selected.add(path)
            continue

        if path == "scripts/select_ci_tests.py":
            selector_test = "tests/test_select_ci_tests.py"
            if (root / selector_test).exists():
                selected.add(selector_test)
            else:
                unmapped_runtime.append(path)
            continue

        if path.startswith("src/observer_sandbox/") and path.endswith(".py"):
            leaf_patterns = _leaf_patterns(path)
            if leaf_patterns is not None:
                leaf_tests = _expand(leaf_patterns, root=root)
                if leaf_tests:
                    selected |= leaf_tests
                else:
                    unmapped_runtime.append(path)
                continue

            stem = Path(path).stem.lower()
            matched = False
            selected |= _expand((f"tests/test_{stem}.py", f"tests/test_{stem}_*.py"), root=root)
            for source_needles, test_patterns in DOMAIN_RULES:
                if any(needle in stem for needle in source_needles):
                    matched = True
                    selected |= _expand(test_patterns, root=root)
            tokens = _source_tokens(path)
            token_hits = set()
            for test_path in (root / "tests").glob("test_*.py"):
                name = test_path.stem.lower()
                if any(token in name for token in tokens):
                    token_hits.add(test_path.relative_to(root).as_posix())
            if token_hits:
                matched = True
                selected |= token_hits
            if not matched:
                unmapped_runtime.append(path)
            continue

        if path.startswith("config/"):
            stem_tokens = {token for token in Path(path).stem.lower().replace(".", "_").split("_") if len(token) >= 4}
            hits = set()
            for test_path in (root / "tests").glob("test_*.py"):
                name = test_path.stem.lower()
                if any(token in name for token in stem_tokens):
                    hits.add(test_path.relative_to(root).as_posix())
            if hits:
                selected |= hits
            else:
                unmapped_runtime.append(path)
            continue

        if path.startswith("scripts/") or path.startswith(".github/workflows/"):
            continue

    if unmapped_runtime:
        return "full", [], "unmapped runtime/config path(s): " + ", ".join(unmapped_runtime)
    if not selected:
        return "full", [], "selector found no safe targeted tests"

    return "targeted", sorted(selected), f"selected {len(selected)} test file(s)"


def main() -> int:
    parser = argparse.ArgumentParser(description="Select a conservative pytest scope for a PR")
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--mode-output", required=True)
    args = parser.parse_args()
    paths = changed_files(args.base, args.head)
    mode, tests, reason = select_tests(paths)
    Path(args.output).write_text("\n".join(tests) + ("\n" if tests else ""), encoding="utf-8")
    Path(args.mode_output).write_text(mode + "\n", encoding="utf-8")
    print(f"CI test mode: {mode}")
    print(f"Reason: {reason}")
    print("Changed files:")
    for path in paths:
        print(f"  - {path}")
    if tests:
        print("Selected tests:")
        for path in tests:
            print(f"  - {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
