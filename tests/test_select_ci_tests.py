from pathlib import Path

from scripts.select_ci_tests import select_tests


def _touch(root: Path, *paths: str) -> None:
    for path in paths:
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# fixture\n", encoding="utf-8")


def test_body_change_selects_body_and_profile_grading_tests(tmp_path):
    _touch(
        tmp_path,
        "tests/test_body_aesthetic_grade_targeting_v2.py",
        "tests/test_universal_profile_grading_v1.py",
        "tests/test_telegram_profile_schema_grading_v1.py",
        "tests/test_inventory_foundation_v1.py",
    )

    mode, tests, _ = select_tests(["src/observer_sandbox/body_aesthetic.py"], root=tmp_path)

    assert mode == "targeted"
    assert "tests/test_body_aesthetic_grade_targeting_v2.py" in tests
    assert "tests/test_universal_profile_grading_v1.py" in tests
    assert "tests/test_telegram_profile_schema_grading_v1.py" in tests
    assert "tests/test_inventory_foundation_v1.py" not in tests


def test_telegram_change_selects_telegram_family_only(tmp_path):
    _touch(
        tmp_path,
        "tests/test_telegram_profile_schema_grading_v1.py",
        "tests/test_telegram_sandbox_profile_edit_v1.py",
        "tests/test_inventory_foundation_v1.py",
    )

    mode, tests, _ = select_tests(["src/observer_sandbox/telegram_fast_polling.py"], root=tmp_path)

    assert mode == "targeted"
    assert set(tests) == {
        "tests/test_telegram_profile_schema_grading_v1.py",
        "tests/test_telegram_sandbox_profile_edit_v1.py",
    }


def test_directly_changed_test_is_selected(tmp_path):
    _touch(tmp_path, "tests/test_inventory_foundation_v1.py")

    mode, tests, _ = select_tests(["tests/test_inventory_foundation_v1.py"], root=tmp_path)

    assert mode == "targeted"
    assert tests == ["tests/test_inventory_foundation_v1.py"]


def test_core_runtime_change_forces_full_suite(tmp_path):
    mode, tests, reason = select_tests(["src/observer_sandbox/db.py"], root=tmp_path)

    assert mode == "full"
    assert tests == []
    assert "core-risk" in reason


def test_unmapped_runtime_change_forces_full_suite(tmp_path):
    _touch(tmp_path, "tests/test_inventory_foundation_v1.py")

    mode, tests, reason = select_tests(["src/observer_sandbox/quantum_penguin.py"], root=tmp_path)

    assert mode == "full"
    assert tests == []
    assert "unmapped runtime" in reason


def test_unmapped_config_change_forces_full_suite(tmp_path):
    _touch(tmp_path, "tests/test_inventory_foundation_v1.py")

    mode, tests, reason = select_tests(["config/new_global_contract.json"], root=tmp_path)

    assert mode == "full"
    assert tests == []
    assert "unmapped runtime" in reason
