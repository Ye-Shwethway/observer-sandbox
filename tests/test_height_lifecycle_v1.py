from datetime import datetime, timedelta

from observer_sandbox.db import connect
from observer_sandbox.height_lifecycle import maybe_settle_height_lifecycle
from observer_sandbox.profile_seed import import_seed
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot


def _synthetic_seed(actor_id: str, *, dob: str, sex: str, height: float, maximum: float) -> dict:
    return {
        "entity_id": actor_id,
        "name": actor_id,
        "canonical_revision": f"{actor_id}-height-test",
        "profile_schema_version": 1,
        "values": {
            "identity.date_of_birth": {"value": dob, "mode": "canonical", "authority": "profile_core"},
            "identity.sex": {"value": sex, "mode": "canonical", "authority": "profile_core"},
            "body.height_in": {"value": height, "mode": "canonical", "authority": "profile_core"},
            "genetics.height_max_in": {"value": maximum, "mode": "canonical", "authority": "profile_core"},
        },
    }


def _height_row(conn, actor_id: str):
    return conn.execute(
        "SELECT value_json,mode,authority,source FROM character_profile_values WHERE entity_id=? AND field_key='body.height_in'",
        (actor_id,),
    ).fetchone()


def test_darian_activation_preserves_adult_structural_height(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, "char_darian")
        result = maybe_settle_height_lifecycle(
            conn,
            "char_darian",
            as_of_sim_time=str(state["sim_time"]),
            state=state,
        )
        row = _height_row(conn, "char_darian")

    assert result["status"] == "bootstrapped"
    assert result["phase"] == "adult_stable"
    assert result["height_in"] == 76.0
    assert result["stat_mutated"] is False
    assert row["mode"] == "simulated"
    assert row["authority"] == "height_lifecycle_engine"
    assert row["source"] == "height-lifecycle-v1"


def test_adult_plateau_records_stability_without_random_drift(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, "char_darian")
        start = datetime.fromisoformat(str(state["sim_time"]))
        maybe_settle_height_lifecycle(conn, "char_darian", as_of_sim_time=start.isoformat(), state=state)
        result = maybe_settle_height_lifecycle(
            conn,
            "char_darian",
            as_of_sim_time=(start + timedelta(days=365)).isoformat(),
        )
        row = _height_row(conn, "char_darian")

    assert result["status"] == "stable"
    assert result["phase"] == "adult_stable"
    assert result["height_in"] == 76.0
    assert result["stat_mutated"] is False
    assert float(row["value_json"]) == 76.0


def test_younger_actor_grows_toward_but_never_beyond_authored_genetic_max(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        actor = "char_synthetic_youth"
        import_seed(conn, _synthetic_seed(actor, dob="2010-05-05", sex="male", height=66.0, maximum=72.0))
        start = datetime.fromisoformat("2025-05-05T08:00:00+00:00")
        boot = maybe_settle_height_lifecycle(conn, actor, as_of_sim_time=start.isoformat())
        result = maybe_settle_height_lifecycle(
            conn,
            actor,
            as_of_sim_time=(start + timedelta(days=365)).isoformat(),
        )
        row = _height_row(conn, actor)

    assert boot["phase"] == "developmental_growth"
    assert result["status"] == "applied"
    assert result["phase"] == "developmental_growth"
    assert 66.0 < result["height_in"] <= 72.0
    assert float(row["value_json"]) == result["height_in"]


def test_older_actor_has_slow_bounded_age_related_decline(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        actor = "char_synthetic_older"
        import_seed(conn, _synthetic_seed(actor, dob="1950-05-05", sex="male", height=70.0, maximum=72.0))
        start = datetime.fromisoformat("2025-05-05T08:00:00+00:00")
        boot = maybe_settle_height_lifecycle(conn, actor, as_of_sim_time=start.isoformat())
        result = maybe_settle_height_lifecycle(
            conn,
            actor,
            as_of_sim_time=(start + timedelta(days=365)).isoformat(),
        )

    assert boot["phase"] == "age_related_decline"
    assert result["status"] == "applied"
    assert result["phase"] == "age_related_decline"
    assert 69.8 <= result["height_in"] < 70.0


def test_missing_lifecycle_inputs_fail_closed_without_claiming_height_authority(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        actor = "char_synthetic_missing_max"
        seed = _synthetic_seed(actor, dob="2010-05-05", sex="male", height=66.0, maximum=72.0)
        del seed["values"]["genetics.height_max_in"]
        import_seed(conn, seed)
        result = maybe_settle_height_lifecycle(
            conn,
            actor,
            as_of_sim_time="2025-05-05T08:00:00+00:00",
        )
        row = _height_row(conn, actor)

    assert result == {"status": "deferred_missing_inputs", "stat_mutated": False}
    assert row["mode"] == "canonical"
    assert row["authority"] == "profile_core"
