from observer_sandbox.db import connect
from observer_sandbox.nutrition_facts import nutrition_facts_for_definition
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_bot import _callback_view


def test_default_nutrition_facts_scale_from_universal_definition():
    chicken = nutrition_facts_for_definition("item.food.chicken_breast_cooked")
    assert chicken is not None
    assert chicken["quantity"] == 200.0
    assert chicken["unit"] == "g"
    assert chicken["basis_quantity"] == 100.0
    assert chicken["energy_kcal"] == 330.0
    assert chicken["protein_g"] == 62.0
    assert chicken["carbohydrate_g"] == 0.0
    assert chicken["fat_g"] == 7.2
    assert chicken["source_revision"] == "universal-items-v1"


def test_nutrition_projection_is_definition_scoped_not_stock_scoped():
    one_hundred_fifty_grams = nutrition_facts_for_definition(
        "item.food.chicken_breast_cooked",
        150.0,
    )
    assert one_hundred_fifty_grams is not None
    assert one_hundred_fifty_grams["energy_kcal"] == 247.5
    assert one_hundred_fifty_grams["protein_g"] == 46.5
    assert one_hundred_fifty_grams["fat_g"] == 5.4


def test_telegram_item_detail_shows_default_portion_nutrient_facts(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "100")

    with connect(db) as conn:
        text, _ = _callback_view(conn, 100, "inv:stack:stack_estate_chicken_breast")

    assert "Cooked Chicken Breast" in text
    assert "NUTRIENT FACTS · DEFAULT PORTION" in text
    assert "Serving     200 g" in text
    assert "Energy      330 kcal" in text
    assert "Protein     62 g" in text
    assert "Carbs       0 g" in text
    assert "Fat         7.2 g" in text
    assert "Basis       100 g" in text


def test_telegram_piece_based_food_shows_piece_serving(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "100")

    with connect(db) as conn:
        text, _ = _callback_view(conn, 100, "inv:stack:stack_estate_apples")

    assert "Serving     1 piece" in text
    assert "Energy      95 kcal" in text
    assert "Protein     0.5 g" in text
    assert "Carbs       25 g" in text
    assert "Fat         0.3 g" in text
