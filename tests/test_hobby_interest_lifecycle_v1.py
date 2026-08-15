from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from observer_sandbox.db import connect
from observer_sandbox.hobby_interest_lifecycle import (
    SOURCE,
    interest_lifecycle_rows,
    settle_hobby_interest_lifecycle,
)
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize


ACTOR = "char_darian"
LIBRARY = "loc_thorne_estate_library"
BOOKSHELF = "obj_thorne_estate_library_bookshelf"


def _dynamic_interest(conn):
    rows = conn.execute(
        "SELECT id,subject,intensity,metadata_json FROM character_preferences WHERE entity_id=? AND preference_type='interest' ORDER BY id",
        (ACTOR,),
    ).fetchall()
    for row in rows:
        metadata = json.loads(row["metadata_json"] or "{}")
        if metadata.get("source") == SOURCE:
            return row, metadata
    raise AssertionError("dynamic interest row not found")


def _dynamic_hobby(conn):
    rows = conn.execute(
        "SELECT id,name,enjoyment,frequency,metadata_json FROM character_hobbies WHERE entity_id=? ORDER BY id",
        (ACTOR,),
    ).fetchall()
    for row in rows:
        metadata = json.loads(row["metadata_json"] or "{}")
        if metadata.get("source") == SOURCE:
            return row, metadata
    return None, None


def test_one_engagement_creates_emerging_interest_not_hobby(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    when = datetime(2025, 5, 2, 20, 0, tzinfo=timezone.utc).isoformat()

    with connect(db) as conn:
        result = settle_hobby_interest_lifecycle(
            conn,
            ACTOR,
            action_name="read",
            target_id=BOOKSHELF,
            ended_sim_time=when,
        )
        conn.commit()
        row, metadata = _dynamic_interest(conn)
        hobby, _ = _dynamic_hobby(conn)

        assert result is not None
        assert metadata["status"] == "emerging"
        assert metadata["engagement_count"] == 1
        assert metadata["effective_engagements"] == 1.0
        assert metadata["distinct_engagement_days"] == 1
        assert float(row["intensity"]) < 10.0
        assert hobby is None

        context = ModelDecisionProvider(conn, character_id=ACTOR)._character_context()
        assert {"type": "interest", "subject": row["subject"]} in context["preferences"]
        assert row["subject"] not in context["hobbies"]


def test_repeated_engagement_crosses_recurring_then_established_and_projects_hobby(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    start = datetime(2025, 5, 2, 20, 0, tzinfo=timezone.utc)

    with connect(db) as conn:
        statuses = []
        for day in range(10):
            result = settle_hobby_interest_lifecycle(
                conn,
                ACTOR,
                action_name="read",
                target_id=BOOKSHELF,
                ended_sim_time=(start + timedelta(days=day)).isoformat(),
            )
            statuses.append(result["engagement"]["status_after"])
        conn.commit()

        interest, metadata = _dynamic_interest(conn)
        hobby, hobby_metadata = _dynamic_hobby(conn)
        context = ModelDecisionProvider(conn, character_id=ACTOR)._character_context()

        assert "recurring" in statuses
        assert statuses[-1] == "established"
        assert metadata["status"] == "established"
        assert metadata["effective_engagements"] >= 10.0
        assert metadata["distinct_engagement_days"] == 10
        assert hobby is not None
        assert hobby["name"] == interest["subject"]
        assert hobby["frequency"] == "established"
        assert hobby_metadata["projection"] == "established_interest"
        assert interest["subject"] in context["hobbies"]


def test_same_day_engagement_is_diminished_and_cannot_instantly_establish(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    start = datetime(2025, 5, 2, 8, 0, tzinfo=timezone.utc)

    with connect(db) as conn:
        first = settle_hobby_interest_lifecycle(
            conn,
            ACTOR,
            action_name="read",
            target_id=BOOKSHELF,
            ended_sim_time=start.isoformat(),
        )
        second = settle_hobby_interest_lifecycle(
            conn,
            ACTOR,
            action_name="read",
            target_id=BOOKSHELF,
            ended_sim_time=(start + timedelta(hours=2)).isoformat(),
        )
        conn.commit()
        _, metadata = _dynamic_interest(conn)

        assert first is not None and second is not None
        assert second["engagement"]["temporal_weight"] == 0.25
        assert metadata["engagement_count"] == 2
        assert metadata["effective_engagements"] == 1.25
        assert metadata["distinct_engagement_days"] == 1
        assert metadata["status"] == "emerging"


def test_non_voluntary_or_skill_actions_do_not_create_interests(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    when = datetime(2025, 5, 2, 20, 0, tzinfo=timezone.utc).isoformat()

    with connect(db) as conn:
        for action in ("train", "inspect", "eat", "drink", "rest", "idle", "self_satisfaction"):
            settle_hobby_interest_lifecycle(
                conn,
                ACTOR,
                action_name=action,
                target_id=BOOKSHELF,
                ended_sim_time=when,
            )
        conn.commit()
        assert interest_lifecycle_rows(conn, ACTOR) == []


def test_long_inactivity_makes_established_interest_dormant_and_removes_active_projection(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    start = datetime(2025, 5, 2, 20, 0, tzinfo=timezone.utc)

    with connect(db) as conn:
        for day in range(10):
            settle_hobby_interest_lifecycle(
                conn,
                ACTOR,
                action_name="read",
                target_id=BOOKSHELF,
                ended_sim_time=(start + timedelta(days=day)).isoformat(),
            )
        interest, before_meta = _dynamic_interest(conn)
        assert before_meta["status"] == "established"
        assert _dynamic_hobby(conn)[0] is not None

        settle_hobby_interest_lifecycle(
            conn,
            ACTOR,
            action_name="idle",
            target_id=None,
            ended_sim_time=(start + timedelta(days=54)).isoformat(),
        )
        conn.commit()
        interest_after, after_meta = _dynamic_interest(conn)
        hobby_after, _ = _dynamic_hobby(conn)

        assert interest_after["id"] == interest["id"]
        assert after_meta["status"] == "dormant"
        assert hobby_after is None
        context = ModelDecisionProvider(conn, character_id=ACTOR)._character_context()
        assert interest_after["subject"] not in context["hobbies"]


def test_lifecycle_authority_and_established_projection_survive_reinitialize(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    start = datetime(2025, 5, 2, 20, 0, tzinfo=timezone.utc)

    with connect(db) as conn:
        for day in range(10):
            settle_hobby_interest_lifecycle(
                conn,
                ACTOR,
                action_name="read",
                target_id=BOOKSHELF,
                ended_sim_time=(start + timedelta(days=day)).isoformat(),
            )
        conn.commit()
        before = interest_lifecycle_rows(conn, ACTOR)[0]
        assert _dynamic_hobby(conn)[0] is not None

    initialize(db)

    with connect(db) as conn:
        after = interest_lifecycle_rows(conn, ACTOR)[0]
        hobby, metadata = _dynamic_hobby(conn)
        canonical_names = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM character_hobbies WHERE entity_id=?",
                (ACTOR,),
            ).fetchall()
        }

        assert after == before
        assert hobby is not None
        assert metadata["source"] == SOURCE
        assert {"physical fitness", "swimming", "tactical planning", "cooking"}.issubset(canonical_names)
