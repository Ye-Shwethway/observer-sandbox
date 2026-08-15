from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from observer_sandbox.db import connect
from observer_sandbox.habit_adaptation import settle_habit_adaptation
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize


ACTOR = "char_darian"
LIBRARY = "loc_thorne_estate_library"
BOOKSHELF = "obj_thorne_estate_library_bookshelf"


def _dynamic_row(conn):
    rows = conn.execute(
        "SELECT name,strength,metadata_json FROM character_habits WHERE entity_id=? ORDER BY id",
        (ACTOR,),
    ).fetchall()
    for row in rows:
        metadata = json.loads(row["metadata_json"] or "{}")
        if metadata.get("source") == "habit_adaptation_v1":
            return row, metadata
    raise AssertionError("dynamic habit row not found")


def test_one_repetition_creates_only_an_emerging_candidate(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    when = datetime(2025, 5, 2, 20, 0, tzinfo=timezone.utc).isoformat()

    with connect(db) as conn:
        result = settle_habit_adaptation(
            conn,
            ACTOR,
            action_name="read",
            location_id=LIBRARY,
            target_id=BOOKSHELF,
            ended_sim_time=when,
        )
        conn.commit()
        row, metadata = _dynamic_row(conn)

        assert result is not None
        assert metadata["status"] == "emerging"
        assert metadata["repetition_count"] == 1
        assert metadata["effective_repetitions"] == 1.0
        assert float(row["strength"]) < 10.0


def test_consistent_daily_repetition_can_establish_a_habit(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    start = datetime(2025, 5, 2, 20, 0, tzinfo=timezone.utc)

    with connect(db) as conn:
        for day in range(18):
            settle_habit_adaptation(
                conn,
                ACTOR,
                action_name="read",
                location_id=LIBRARY,
                target_id=BOOKSHELF,
                ended_sim_time=(start + timedelta(days=day)).isoformat(),
            )
        conn.commit()
        row, metadata = _dynamic_row(conn)

        assert metadata["status"] == "established"
        assert metadata["effective_repetitions"] >= 18.0
        assert float(row["strength"]) >= 50.0


def test_same_day_repetition_has_diminishing_formation_weight(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    start = datetime(2025, 5, 2, 8, 0, tzinfo=timezone.utc)

    with connect(db) as conn:
        first = settle_habit_adaptation(
            conn,
            ACTOR,
            action_name="read",
            location_id=LIBRARY,
            target_id=BOOKSHELF,
            ended_sim_time=start.isoformat(),
        )
        second = settle_habit_adaptation(
            conn,
            ACTOR,
            action_name="read",
            location_id=LIBRARY,
            target_id=BOOKSHELF,
            ended_sim_time=(start + timedelta(hours=2)).isoformat(),
        )
        conn.commit()
        _, metadata = _dynamic_row(conn)

        assert first is not None and second is not None
        assert second["reinforcement"]["temporal_weight"] == 0.25
        assert metadata["repetition_count"] == 2
        assert metadata["effective_repetitions"] == 1.25
        assert metadata["status"] == "emerging"


def test_long_inactivity_weakens_established_habit_to_dormant_without_deletion(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    start = datetime(2025, 5, 2, 20, 0, tzinfo=timezone.utc)

    with connect(db) as conn:
        for day in range(18):
            settle_habit_adaptation(
                conn,
                ACTOR,
                action_name="read",
                location_id=LIBRARY,
                target_id=BOOKSHELF,
                ended_sim_time=(start + timedelta(days=day)).isoformat(),
            )
        row_before, metadata_before = _dynamic_row(conn)
        assert metadata_before["status"] == "established"
        strength_before = float(row_before["strength"])

        settle_habit_adaptation(
            conn,
            ACTOR,
            action_name="idle",
            location_id=LIBRARY,
            target_id=None,
            ended_sim_time=(start + timedelta(days=47)).isoformat(),
        )
        conn.commit()
        row_after, metadata_after = _dynamic_row(conn)

        assert float(row_after["strength"]) < strength_before
        assert metadata_after["status"] == "dormant"
        assert conn.execute(
            "SELECT COUNT(*) FROM character_habits WHERE entity_id=? AND name=?",
            (ACTOR, row_after["name"]),
        ).fetchone()[0] == 1


def test_reinitialization_preserves_learned_adaptive_rows_and_runtime_metadata(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        conn.execute(
            """
            INSERT INTO character_preferences(entity_id,preference_type,subject,intensity,metadata_json)
            VALUES(?,?,?,?,?)
            """,
            (ACTOR, "like", "night swimming", 77.0, json.dumps({"source": "test_runtime"})),
        )
        conn.execute(
            """
            INSERT INTO character_hobbies(entity_id,name,proficiency,frequency,enjoyment,metadata_json)
            VALUES(?,?,?,?,?,?)
            """,
            (ACTOR, "astronomy", 22.0, "occasional", 81.0, json.dumps({"source": "test_runtime"})),
        )
        conn.execute(
            """
            INSERT INTO character_habits(entity_id,name,strength,metadata_json)
            VALUES(?,?,?,?)
            """,
            (
                ACTOR,
                "Read — Test Space",
                63.0,
                json.dumps(
                    {
                        "source": "habit_adaptation_v1",
                        "habit_key": "read|test_space|",
                        "status": "established",
                        "effective_repetitions": 24.0,
                    }
                ),
            ),
        )
        conn.commit()

    initialize(db)

    with connect(db) as conn:
        pref = conn.execute(
            "SELECT intensity,metadata_json FROM character_preferences WHERE entity_id=? AND subject='night swimming'",
            (ACTOR,),
        ).fetchone()
        hobby = conn.execute(
            "SELECT proficiency,frequency,enjoyment,metadata_json FROM character_hobbies WHERE entity_id=? AND name='astronomy'",
            (ACTOR,),
        ).fetchone()
        habit = conn.execute(
            "SELECT strength,metadata_json FROM character_habits WHERE entity_id=? AND name='Read — Test Space'",
            (ACTOR,),
        ).fetchone()

        assert pref is not None and float(pref["intensity"]) == 77.0
        assert json.loads(pref["metadata_json"])["source"] == "test_runtime"
        assert hobby is not None and float(hobby["enjoyment"]) == 81.0
        assert hobby["frequency"] == "occasional"
        assert json.loads(hobby["metadata_json"])["source"] == "test_runtime"
        assert habit is not None and float(habit["strength"]) == 63.0
        assert json.loads(habit["metadata_json"])["status"] == "established"

        canonical_habit = conn.execute(
            "SELECT metadata_json FROM character_habits WHERE entity_id=? AND name='high-discipline routines'",
            (ACTOR,),
        ).fetchone()
        assert canonical_habit is not None
        assert json.loads(canonical_habit["metadata_json"])["canonical_baseline"] is True


def test_cognition_sees_compact_dynamics_but_only_established_dynamic_habits_as_habits(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    start = datetime(2025, 5, 2, 20, 0, tzinfo=timezone.utc)

    with connect(db) as conn:
        settle_habit_adaptation(
            conn,
            ACTOR,
            action_name="read",
            location_id=LIBRARY,
            target_id=BOOKSHELF,
            ended_sim_time=start.isoformat(),
        )
        emerging = ModelDecisionProvider(conn, character_id=ACTOR)._character_context()
        dynamic_name = emerging["habit_dynamics"][0]["name"]
        assert dynamic_name not in emerging["habits"]
        assert emerging["habit_dynamics"][0]["status"] == "emerging"
        assert set(emerging["habit_dynamics"][0]) == {
            "name",
            "strength",
            "status",
            "behavior",
            "cue_location_id",
        }

        for day in range(1, 18):
            settle_habit_adaptation(
                conn,
                ACTOR,
                action_name="read",
                location_id=LIBRARY,
                target_id=BOOKSHELF,
                ended_sim_time=(start + timedelta(days=day)).isoformat(),
            )
        conn.commit()
        established = ModelDecisionProvider(conn, character_id=ACTOR)._character_context()

        assert dynamic_name in established["habits"]
        assert established["habit_dynamics"][0]["status"] == "established"
