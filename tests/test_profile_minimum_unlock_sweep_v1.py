from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot


ACTOR = "char_darian"


def test_canonical_profile_context_reaches_cognition_without_mutation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        before = dict(state)
        enriched = ModelDecisionProvider(conn, character_id=ACTOR)._enrich_state(state)

        character = enriched["character"]
        assert character["identity"]["name"] == "Darian Thorne"
        assert character["identity"]["date_of_birth"] == "2002-09-03"
        assert character["identity"]["sex"] == "male"

        assert character["appearance"]["eye_color"] == "deep blue"
        assert character["appearance"]["hair_color"] == "jet black"
        assert character["appearance"]["pars"] == 98.0
        assert "natural-bodybuilder aesthetic" in character["appearance"]["distinctive_features"]

        assert "disciplined" in character["personality"]["traits"]
        assert character["personality"]["primary_motivation"]
        assert character["background"]["origins"]

        assert character["preferences"]
        assert all(item["type"] and item["subject"] for item in character["preferences"])
        assert "physical fitness" in character["hobbies"]
        assert "high-discipline routines" in character["habits"]

        assert state == before
        assert snapshot(conn, ACTOR) == before


def test_profile_context_is_compact_and_excludes_intimate_identity_fields(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        character = ModelDecisionProvider(conn, character_id=ACTOR)._character_context()

        assert set(character["identity"]) == {
            "name",
            "date_of_birth",
            "sex",
            "gender",
            "current_status",
        }
        assert "sexual_orientation" not in character["identity"]
        assert set(character["appearance"]) == {
            "distinctive_features",
            "eye_color",
            "hair_color",
            "hair_style",
            "facial_hair",
            "pars",
        }
        assert set(character["background"]) == {"origins"}
