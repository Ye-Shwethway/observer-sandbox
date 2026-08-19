import pytest

from observer_sandbox.creation_socket import (
    CreationProposalError,
    build_creation_proposal,
    validate_creation_proposal,
)
from observer_sandbox.creator_authority import (
    CREATOR_CREATION_SOURCE,
    CREATOR_PROFILE_CONTROL_SOURCE,
    is_creator_authoritative,
    ordinary_seed_may_replace,
)
from observer_sandbox.creator_creation_ai import (
    activate_creator_creation_model,
    creator_creation_binding,
)
from observer_sandbox.db import connect
from observer_sandbox.news_ai import activate_news_generation_model, news_generation_binding
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_ai_control import callback_view, home_view


def _add_model(conn, provider: str, model: str) -> None:
    conn.execute("UPDATE ai_providers SET enabled=1 WHERE id=?", (provider,))
    conn.execute(
        "INSERT INTO ai_models(provider_id,model_id,display_name) VALUES(?,?,?)",
        (provider, model, model),
    )
    conn.commit()


def test_creator_authority_outranks_ordinary_seed_and_simulated_state():
    assert is_creator_authoritative(authority="creator") is True
    assert is_creator_authoritative(source=CREATOR_PROFILE_CONTROL_SOURCE) is True
    assert is_creator_authoritative(source=CREATOR_CREATION_SOURCE) is True

    assert ordinary_seed_may_replace(existing=False) is True
    assert ordinary_seed_may_replace(existing=True, mode="canonical", source="seed-v1") is True
    assert ordinary_seed_may_replace(existing=True, mode="simulated", source="seed-v1") is False
    assert ordinary_seed_may_replace(
        existing=True,
        mode="static",
        source=CREATOR_PROFILE_CONTROL_SOURCE,
    ) is False
    assert ordinary_seed_may_replace(
        existing=True,
        mode="static",
        authority="creator",
        source="creator-creation-v1",
    ) is False


def test_character_and_location_use_same_sandbox_proposal_envelope():
    character = build_creation_proposal(
        "character",
        identity={"name": "Sandbox Character"},
        properties={"summary": "Disposable staging character."},
        provenance_mode="manual",
        requested_by="test:creator",
    )
    location = build_creation_proposal(
        "location",
        identity={"name": "Sandbox Location"},
        properties={"summary": "Disposable staging location."},
        provenance_mode="ai_generated",
        requested_by="test:creator",
    )

    assert set(character) == set(location)
    assert character["target_scope"] == "sandbox"
    assert location["target_scope"] == "sandbox"
    assert character["creation_type"] == "character"
    assert location["creation_type"] == "location"


def test_creation_proposal_rejects_direct_canonical_target_and_unknown_socket():
    proposal = build_creation_proposal(
        "location",
        identity={"name": "Staging Only"},
        provenance_mode="manual",
    )
    proposal["target_scope"] = "canonical"
    with pytest.raises(CreationProposalError, match="sandbox-only"):
        validate_creation_proposal(proposal)

    with pytest.raises(CreationProposalError, match="Unsupported creation socket"):
        build_creation_proposal("supernatural_power", identity={"name": "Teleport"})


def test_creator_creation_ai_binding_is_independent_from_news_binding(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_model(conn, "gemini", "creation-model")
        _add_model(conn, "openai", "news-model")

        news = activate_news_generation_model(conn, "openai", "news-model")
        creation = activate_creator_creation_model(conn, "gemini", "creation-model")

        assert news_generation_binding(conn)["model_id"] == "news-model"
        assert creator_creation_binding(conn)["model_id"] == "creation-model"
        assert news["provider_id"] == "openai"
        assert creation["provider_id"] == "gemini"


def test_creator_settings_has_ai_upper_layer_and_creation_ai_page(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        text, keyboard = home_view(conn)
        assert "CREATOR SETTINGS" in text
        assert any(
            button.get("callback_data") == "ai:settings"
            for row in keyboard
            for button in row
        )
        assert not any(
            button.get("callback_data") == "ai:character"
            for row in keyboard
            for button in row
        )

        ai_text, ai_keyboard = callback_view(conn, 123, "ai:settings")
        assert "AI SETTINGS" in ai_text
        assert "Creator Creation AI" in ai_text
        callbacks = {
            button.get("callback_data")
            for row in ai_keyboard
            for button in row
        }
        assert {"ai:character", "ai:n:home", "ai:c:home"} <= callbacks

        creation_text, creation_keyboard = callback_view(conn, 123, "ai:c:home")
        assert "CREATOR CREATION AI" in creation_text
        assert "sandbox proposals only" in creation_text.lower()
        assert any(
            button.get("callback_data") == "ai:c:providers"
            for row in creation_keyboard
            for button in row
        )
