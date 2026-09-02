import importlib.util
from pathlib import Path


_SELECTOR_PATH = Path(__file__).resolve().parents[1] / "scripts" / "select_ci_tests.py"
_SPEC = importlib.util.spec_from_file_location("select_ci_tests", _SELECTOR_PATH)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
select_tests = _MODULE.select_tests


def _touch(root: Path, *paths: str) -> None:
    for path in paths:
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# fixture\n", encoding="utf-8")


def test_location_ai_contract_change_selects_location_ai_tests_only(tmp_path):
    _touch(
        tmp_path,
        "tests/test_location_ai_contract_v2.py",
        "tests/test_location_ai_unit_normalization_v2.py",
        "tests/test_creator_studio_location_v2.py",
        "tests/test_telegram_bot.py",
    )

    mode, tests, reason = select_tests(
        ["src/observer_sandbox/location_ai_contract.py"],
        root=tmp_path,
    )

    assert mode == "targeted"
    assert reason == "selected 3 test file(s)"
    assert tests == [
        "tests/test_creator_studio_location_v2.py",
        "tests/test_location_ai_contract_v2.py",
        "tests/test_location_ai_unit_normalization_v2.py",
    ]
