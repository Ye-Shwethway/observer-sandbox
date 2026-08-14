from datetime import datetime, timedelta

from observer_sandbox.db import connect
from observer_sandbox.profile_seed import import_seed
from observer_sandbox.runtime import initialize
from observer_sandbox.sexual_anatomy_physiology_lifecycle import (
    maybe_settle_sexual_anatomy_physiology_lifecycle,
)
from observer_sandbox.simulation import snapshot


def _seed(actor_id: str, *, dob: str, length: float, girth: float, length_target: float, girth_target: float, baseline: float | None = None, cap: float | None = None) -> dict:
    values = {
        "identity.date_of_birth": {"value": dob, "mode": "canonical", "authority": "profile_core"},
        "identity.sex": {"value": "male", "mode": "canonical", "authority": "profile_core"},
        "sexual_anatomy.penis_length_in": {"value": length, "mode": "canonical", "authority": "profile_core"},
        "sexual_anatomy.penis_girth_in": {"value": girth, "mode": "canonical", "authority": "profile_core"},
        "genetics.penis_length_in": {"value": length_target, "mode": "canonical", "authority": "profile_core"},
        "genetics.penis_girth_in": {"value": girth_target, "mode": "canonical", "authority": "profile_core"},
    }
    if baseline is not None:
        values["sexual_anatomy.baseline_erectile_function"] = {"value": baseline, "mode": "static", "authority": "sexual_physiology_engine"}
    if cap is not None:
        values["sexual_anatomy.erection_firmness_cap"] = {"value": cap, "mode": "canonical", "authority": "profile_core"}
    return {
        "entity_id": actor_id,
        "name": actor_id,
        "canonical_revision": f"{actor_id}-sexual-lifecycle-test",
        "profile_schema_version": 1,
        "values": values,
    }


def _value_row(conn, actor: str, key: str):
    return conn.execute(
        "SELECT value_json,mode,authority,source FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor, key),
    ).fetchone()


def test_darian_adult_activation_preserves_structural_measurements(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, "char_darian")
        result = maybe_settle_sexual_anatomy_physiology_lifecycle(
            conn,
            "char_darian",
            as_of_sim_time=str(state["sim_time"]),
            state=state,
        )
        length = _value_row(conn, "char_darian", "sexual_anatomy.penis_length_in")
        girth = _value_row(conn, "char_darian", "sexual_anatomy.penis_girth_in")

    assert result["status"] == "bootstrapped"
    assert result["structural_phase"] == "adult_stable"
    assert result["structural_values"]["sexual_anatomy.penis_length_in"] == 10.0
    assert result["structural_values"]["sexual_anatomy.penis_girth_in"] == 5.0
    assert result["stat_mutated"] is False
    assert float(length["value_json"]) == 10.0
    assert float(girth["value_json"]) == 5.0
    assert length["mode"] == girth["mode"] == "simulated"
    assert length["authority"] == girth["authority"] == "sexual_anatomy_lifecycle_engine"
    assert length["source"] == girth["source"] == "sexual-anatomy-physiology-lifecycle-v1"


def test_adult_structural_values_remain_stable_without_arbitrary_aging_shrink(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, "char_darian")
        start = datetime.fromisoformat(str(state["sim_time"]))
        maybe_settle_sexual_anatomy_physiology_lifecycle(conn, "char_darian", as_of_sim_time=start.isoformat())
        result = maybe_settle_sexual_anatomy_physiology_lifecycle(
            conn,
            "char_darian",
            as_of_sim_time=(start + timedelta(days=3650)).isoformat(),
        )

    assert result["status"] == "stable"
    assert result["structural_values"]["sexual_anatomy.penis_length_in"] == 10.0
    assert result["structural_values"]["sexual_anatomy.penis_girth_in"] == 5.0


def test_synthetic_youth_develops_toward_but_not_beyond_adult_targets(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        actor = "char_synthetic_pubertal"
        import_seed(conn, _seed(actor, dob="2011-05-05", length=5.5, girth=3.4, length_target=7.0, girth_target=4.5))
        start = datetime.fromisoformat("2025-05-05T08:00:00+00:00")
        boot = maybe_settle_sexual_anatomy_physiology_lifecycle(conn, actor, as_of_sim_time=start.isoformat())
        result = maybe_settle_sexual_anatomy_physiology_lifecycle(
            conn,
            actor,
            as_of_sim_time=(start + timedelta(days=365)).isoformat(),
        )

    assert boot["structural_phase"] == "developmental_growth"
    assert result["status"] == "applied"
    assert 5.5 < result["structural_values"]["sexual_anatomy.penis_length_in"] <= 7.0
    assert 3.4 < result["structural_values"]["sexual_anatomy.penis_girth_in"] <= 4.5


def test_optional_long_term_erectile_capacity_declines_slowly_with_age_when_authored(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        actor = "char_synthetic_older_male"
        import_seed(conn, _seed(actor, dob="1955-05-05", length=6.5, girth=4.6, length_target=6.5, girth_target=4.6, baseline=90.0, cap=95.0))
        start = datetime.fromisoformat("2025-05-05T08:00:00+00:00")
        maybe_settle_sexual_anatomy_physiology_lifecycle(conn, actor, as_of_sim_time=start.isoformat())
        result = maybe_settle_sexual_anatomy_physiology_lifecycle(
            conn,
            actor,
            as_of_sim_time=(start + timedelta(days=365)).isoformat(),
        )
        row = _value_row(conn, actor, "sexual_anatomy.baseline_erectile_function")

    assert result["status"] == "applied"
    assert result["structural_values"]["sexual_anatomy.penis_length_in"] == 6.5
    assert result["functional_value"] is not None
    assert 88.0 < result["functional_value"] < 90.0
    assert row["mode"] == "simulated"
    assert row["authority"] == "sexual_physiology_engine"


def test_functional_capacity_is_optional_and_missing_values_are_not_invented(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, "char_darian")
        start = datetime.fromisoformat(str(state["sim_time"]))
        maybe_settle_sexual_anatomy_physiology_lifecycle(conn, "char_darian", as_of_sim_time=start.isoformat())
        result = maybe_settle_sexual_anatomy_physiology_lifecycle(
            conn,
            "char_darian",
            as_of_sim_time=(start + timedelta(days=365)).isoformat(),
        )
        baseline = _value_row(conn, "char_darian", "sexual_anatomy.baseline_erectile_function")
        cap = _value_row(conn, "char_darian", "sexual_anatomy.erection_firmness_cap")

    assert result["status"] == "stable"
    assert result["functional_value"] is None
    assert baseline is None
    assert cap is None
