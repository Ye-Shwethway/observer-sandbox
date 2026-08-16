from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_bot import _callback_view


def _contains_callback(keyboard, callback_data: str) -> bool:
    return any(button.get("callback_data") == callback_data for row in (keyboard or []) for button in row)


def test_owner_character_finances_are_reachable_and_canonical(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "100")

    with connect(db) as conn:
        _, keyboard = _callback_view(conn, 100, "char:char_darian")
        assert _contains_callback(keyboard, "eco:char:char_darian")

        text, _ = _callback_view(conn, 100, "eco:char:char_darian")
        assert "Darian Thorne · FINANCES" in text
        assert "Net worth   $25,000,000.00" in text
        assert "Primary Liquid: $1,800,000.00" in text
        assert "Thorne Estate: $16,500,000.00" in text
        assert "Liabilities" in text
        assert "$500,000.00" in text
        assert "Net worth and spendable balance are separate" in text


def test_financial_detail_remains_owner_only(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "100")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "200")

    with connect(db) as conn:
        _, keyboard = _callback_view(conn, 200, "char:char_darian")
        assert not _contains_callback(keyboard, "eco:char:char_darian")
        denied, _ = _callback_view(conn, 200, "eco:char:char_darian")
        assert "Creator authority required for financial details" in denied


def test_represented_estate_location_shows_property_value(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "100")

    with connect(db) as conn:
        text, _ = _callback_view(conn, 100, "loc:loc_thorne_estate")
        assert "Thorne Estate" in text
        assert "Economic asset" in text
        assert "Value: $16,500,000.00" in text
        assert "Owner: Darian Thorne" in text
        assert "Type: Real Estate" in text


def test_object_detail_shows_replacement_value_without_double_counting(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "100")

    with connect(db) as conn:
        text, _ = _callback_view(conn, 100, "obj:obj_thorne_estate_training_ai_combat_sim")
        assert "AI Combat Simulation System" in text
        assert "Economic value" in text
        assert "Replacement value: $450,000.00" in text
        assert "Net worth: Included in Thorne Estate" in text


def test_inventory_stack_detail_shows_live_and_unit_value(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "100")

    with connect(db) as conn:
        text, _ = _callback_view(conn, 100, "inv:stack:stack_estate_apples")
        assert "Apple" in text
        assert "ECONOMIC VALUE" in text
        assert "Current stock  $150.00" in text
        assert "Unit value     $1.25 / 1 piece" in text


def test_identity_owner_shows_gender_and_orientation_not_duplicate_sex(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "100")

    with connect(db) as conn:
        text, _ = _callback_view(conn, 100, "psec:char_darian:identity")
        assert "• Gender: male" in text
        assert "• Sexual orientation: heterosexual" in text
        assert "• Sex:" not in text


def test_identity_allowed_user_keeps_private_orientation_hidden(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "100")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "200")

    with connect(db) as conn:
        text, _ = _callback_view(conn, 200, "psec:char_darian:identity")
        assert "• Gender: male" in text
        assert "• Sex:" not in text
        assert "Sexual orientation" not in text
