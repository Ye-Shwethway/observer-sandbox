from __future__ import annotations

import copy
from types import SimpleNamespace

import pytest

import observer_sandbox.creator_studio_location as location_studio
import observer_sandbox.telegram_creator_studio_location_feedback_extension as feedback
from observer_sandbox.creation_sandbox import canonical_state_fingerprint
from observer_sandbox.creator_studio import CreatorStudioError, active_draft
from observer_sandbox.creator_studio_location import ai_location_draft, manual_location_template
from observer_sandbox.db import connect
from observer_sandbox.location_ai_contract import location_ai_fill_schema, repair_location_ai_candidate
from observer_sandbox.location_schema_registry_v2 import LOCATION_KINDS
from observer_sandbox.runtime import initialize


def _location_count(conn) -> int:
    return int(conn.execute("SELECT COUNT(*) FROM creation_sandbox_location_profiles").fetchone()[0])


def _candidate(name: str = "AI Room"):
    value = manual_location_template()
    value["identity"]["key"] = "place.ai.room"
    value["identity"]["name"] = name
    value["provenance"] = {"source_status": "provisional", "source_note": "AI proposal"}
    return value


def test_location_ai_fill_schema_is_complete_strict_and_registry_backed() -> None:
    schema = location_ai_fill_schema()
    expected = {
        "schema_version", "identity", "structure", "geography", "spatial", "boundary",
        "access", "operations", "topology", "facilities", "environment", "control",
        "economic_policy", "provenance",
    }
    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert set(schema["properties"]) == expected
    assert set(schema["required"]) == expected
    identity = schema["properties"]["identity"]
    assert identity["additionalProperties"] is False
    assert set(identity["properties"]["kind"]["enum"]) == set(LOCATION_KINDS)
    assert "derived" not in schema["properties"]
    assert "grade" not in schema["properties"]


def test_location_ai_uses_exact_provider_schema_and_shared_draft_contract(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    calls = []
    monkeypatch.setattr(
        location_studio,
        "creator_creation_binding",
        lambda conn: {"provider_id": "fake", "model_id": "fake-model", "parameters": {}},
    )

    def fake_generate(*args, **kwargs):
        calls.append(kwargs)
        return _candidate()

    monkeypatch.setattr(location_studio, "generate_structured", fake_generate)

    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)
        draft = ai_location_draft(conn, 101, "Create a quiet room")
        after = canonical_state_fingerprint(conn)
        assert draft["draft_mode"] == "ai_generated"
        assert draft["revision"] == 1
        assert _location_count(conn) == 0
        assert before == after
        assert len(calls) == 1
        supplied = calls[0]["schema"]
        assert supplied["additionalProperties"] is False
        assert set(supplied["required"]) == set(location_ai_fill_schema()["required"])
        source = draft["proposal"]["properties"]["location_payload"]
        assert source["schema_version"] == "location-v2"
        assert "derived" not in source


def test_one_deterministic_repair_normalizes_representation_without_inventing_facts(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    candidate = _candidate("Repairable Room")
    candidate["derived"] = {"completeness_level": "L4"}
    candidate["identity"]["grade"] = "S"
    candidate["geography"]["country_code"] = "us"
    candidate["structure"]["parent_ref"] = "   "
    candidate["provenance"] = {"source_status": "canonical", "source_note": "   "}

    monkeypatch.setattr(
        location_studio,
        "creator_creation_binding",
        lambda conn: {"provider_id": "fake", "model_id": "fake-model", "parameters": {}},
    )
    monkeypatch.setattr(location_studio, "generate_structured", lambda *args, **kwargs: copy.deepcopy(candidate))

    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)
        draft = ai_location_draft(conn, 103, "Create a represented US room")
        source = draft["proposal"]["properties"]["location_payload"]
        assert draft["revision"] == 1
        assert "derived" not in source
        assert "grade" not in source["identity"]
        assert source["geography"]["country_code"] == "US"
        assert source["structure"]["parent_ref"] is None
        assert source["provenance"] == {"source_status": "provisional", "source_note": None}
        assert _location_count(conn) == 0
        assert canonical_state_fingerprint(conn) == before


def test_repair_does_not_invent_missing_required_location_facts(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    candidate = _candidate()
    del candidate["identity"]["name"]

    monkeypatch.setattr(
        location_studio,
        "creator_creation_binding",
        lambda conn: {"provider_id": "fake", "model_id": "fake-model", "parameters": {}},
    )
    monkeypatch.setattr(location_studio, "generate_structured", lambda *args, **kwargs: copy.deepcopy(candidate))

    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)
        with pytest.raises(CreatorStudioError, match="after one deterministic repair"):
            ai_location_draft(conn, 107, "Create a room")
        assert active_draft(conn, 107) is None
        assert _location_count(conn) == 0
        assert canonical_state_fingerprint(conn) == before


def test_repair_does_not_hide_semantic_validation_failure(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    candidate = _candidate()
    candidate["operations"]["initial_state"] = "teleporting"

    monkeypatch.setattr(
        location_studio,
        "creator_creation_binding",
        lambda conn: {"provider_id": "fake", "model_id": "fake-model", "parameters": {}},
    )
    monkeypatch.setattr(location_studio, "generate_structured", lambda *args, **kwargs: copy.deepcopy(candidate))

    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)
        with pytest.raises(CreatorStudioError, match="after one deterministic repair"):
            ai_location_draft(conn, 109, "Create a room")
        assert active_draft(conn, 109) is None
        assert _location_count(conn) == 0
        assert canonical_state_fingerprint(conn) == before


def test_repair_helper_leaves_missing_sections_missing() -> None:
    candidate = _candidate()
    del candidate["geography"]
    repaired = repair_location_ai_candidate(candidate)
    assert "geography" not in repaired
    assert repaired["provenance"]["source_status"] == "provisional"


def test_location_ai_feedback_wraps_generation_and_reroll_and_is_non_authoritative(monkeypatch) -> None:
    typing_calls = []
    generation_calls = []
    callback_calls = []
    draft = {"creation_type": "location", "draft_mode": "ai_generated"}

    base = SimpleNamespace()
    base._session = lambda conn, user_id: {"expected_input": "description"}

    def original_ai(conn, user_id, creation_type, prompt_text, **kwargs):
        generation_calls.append((user_id, creation_type, prompt_text))
        return {"ok": True}

    def original_callback(conn, user_id, callback_data):
        callback_calls.append((user_id, callback_data))
        return "ok", []

    base.ai_draft = original_ai
    base.studio_callback_view = original_callback
    monkeypatch.setattr(feedback, "_best_effort_typing", lambda user_id: typing_calls.append(user_id))
    monkeypatch.setattr(feedback, "active_draft", lambda conn, user_id: draft)

    feedback.install_location_ai_feedback_extension(base)

    assert base.ai_draft(None, 123, "location", "Create a room") == {"ok": True}
    assert typing_calls == [123]
    assert generation_calls == [(123, "location", "Create a room")]

    assert base.studio_callback_view(None, 123, "sw:cs:reroll") == ("ok", [])
    assert typing_calls == [123, 123]
    assert callback_calls == [(123, "sw:cs:reroll")]


def test_typing_transport_failure_is_best_effort(monkeypatch) -> None:
    monkeypatch.setenv("OBSERVER_TELEGRAM_BOT_TOKEN", "token")

    class BrokenBot:
        @staticmethod
        def _api(*args, **kwargs):
            raise RuntimeError("transport down")

    import observer_sandbox.telegram_bot as telegram_bot
    monkeypatch.setattr(telegram_bot, "_api", BrokenBot._api)
    feedback._best_effort_typing(123)  # must not raise
