from __future__ import annotations

import pytest

from observer_sandbox.ai_runtime import _compact_prompt_state
from observer_sandbox.cognition_context_snapshots import (
    cognition_context_snapshots,
    record_cognition_context_snapshot,
)
from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot
from observer_sandbox.telegram_bot import _callback_view
from observer_sandbox.telegram_cognition_context import cognition_context_view


ACTOR = "char_darian"


def _record(conn, marker: int, *, injection_type: str = "primary", extra=None):
    context = {
        "sim_time": f"2025-05-07T0{marker}:00:00+00:00",
        "decision_signals": {"marker": marker},
        "future_system_context": extra if extra is not None else {"enabled": True},
    }
    record_cognition_context_snapshot(
        conn,
        character_id=ACTOR,
        role="cognition",
        injection_type=injection_type,
        provider_id="gemini",
        model_id="test-model",
        available_actions=["idle"],
        context=context,
    )
    return context


def test_actor_snapshot_ring_keeps_exact_last_three_newest_first(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        for marker in range(4):
            expected = _record(conn, marker)
        conn.commit()
        rows = cognition_context_snapshots(conn, ACTOR)

    assert len(rows) == 3
    assert [row["context"]["decision_signals"]["marker"] for row in rows] == [3, 2, 1]
    assert rows[0]["context"] == expected


def test_model_provider_captures_the_exact_compact_context_before_primary_injection(tmp_path, monkeypatch):
    class ExpectedModelBoundaryStop(RuntimeError):
        pass

    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setattr(
        "observer_sandbox.model_decision.resolve_binding",
        lambda conn, *, role, character_id: {"provider_id": "gemini", "model_id": "test-model"},
    )

    def stop_at_model_boundary(*args, **kwargs):
        raise ExpectedModelBoundaryStop

    monkeypatch.setattr(
        "observer_sandbox.model_decision.generate_character_decision",
        stop_at_model_boundary,
    )

    with connect(db) as conn:
        provider = ModelDecisionProvider(conn, character_id=ACTOR)
        state = snapshot(conn, ACTOR)
        enriched = provider._enrich_state(state)
        expected_context = _compact_prompt_state(enriched)
        expected_actions = sorted({str(option["action"]) for option in enriched["action_options"]})

        with pytest.raises(ExpectedModelBoundaryStop):
            provider.choose(state, ["idle"])

        rows = cognition_context_snapshots(conn, ACTOR)
        assert rows[0]["context"] == expected_context
        assert rows[0]["injection_type"] == "primary"
        assert rows[0]["available_actions"] == expected_actions


def test_unknown_future_context_is_rendered_automatically_and_paged(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    long_items = [
        {"new_signal_name": f"signal-{index}", "explanation": "x" * 180}
        for index in range(40)
    ]
    with connect(db) as conn:
        _record(conn, 1, extra={"brand_new_subsystem": long_items})
        conn.commit()
        first, keyboard = cognition_context_view(conn, ACTOR, slot=1, page=0)

        assert "Available Action Vocabulary" in first
        assert "Idle" in first.title()
        assert "Future System Context" in first
        assert "Brand New Subsystem" in first
        assert len(first) < 4096
        assert any(button["text"].startswith("Next") for row in keyboard for button in row)

        next_callback = next(
            button["callback_data"]
            for row in keyboard
            for button in row
            if button["text"].startswith("Next")
        )
        _, _, raw_slot, raw_page = next_callback.split(":")
        second, second_keyboard = cognition_context_view(
            conn,
            ACTOR,
            slot=int(raw_slot),
            page=int(raw_page),
        )
        assert len(second) < 4096
        assert "Page      2/" in second
        assert any(button["text"].startswith("◀") for row in second_keyboard for button in row)


def test_character_menu_places_owner_context_button_directly_under_profile_and_keeps_allowed_users_out(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "222")

    with connect(db) as conn:
        _, owner_keyboard = _callback_view(conn, 111, f"char:{ACTOR}")
        assert owner_keyboard[0][0]["callback_data"] == f"prof:{ACTOR}"
        assert owner_keyboard[1][0]["callback_data"] == f"cog:{ACTOR}:1:0"
        assert any(
            button["callback_data"] == f"ctl:restore_prompt:{ACTOR}"
            for row in owner_keyboard[2:]
            for button in row
        )

        _, allowed_keyboard = _callback_view(conn, 222, f"char:{ACTOR}")
        assert all(
            not button["callback_data"].startswith("cog:")
            for row in allowed_keyboard
            for button in row
        )
        locked, _ = _callback_view(conn, 222, f"cog:{ACTOR}:1:0")
        assert "Creator authority required" in locked


def test_snapshot_selectors_are_three_slots_and_corrective_retry_is_labeled(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _record(conn, 1, injection_type="primary")
        _record(conn, 2, injection_type="corrective_retry")
        conn.commit()
        text, keyboard = cognition_context_view(conn, ACTOR, slot=1, page=0)

    assert "Corrective Retry" in text
    assert [button["callback_data"] for button in keyboard[0]] == [
        f"cog:{ACTOR}:1:0",
        f"cog:{ACTOR}:2:0",
        f"cog:{ACTOR}:3:0",
    ]
