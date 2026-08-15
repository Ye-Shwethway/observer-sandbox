from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.preference_adaptation import (
    SOURCE,
    preference_adaptation_state,
    settle_preference_adaptation,
    settle_preference_evidence,
)
from observer_sandbox.runtime import initialize


ACTOR = "char_darian"
BOOKSHELF = "obj_thorne_estate_library_bookshelf"


def _dynamic_projection(conn):
    rows = conn.execute(
        "SELECT id,preference_type,subject,intensity,metadata_json FROM character_preferences WHERE entity_id=? ORDER BY id",
        (ACTOR,),
    ).fetchall()
    for row in rows:
        metadata = json.loads(row["metadata_json"] or "{}")
        if isinstance(metadata, dict) and metadata.get("source") == SOURCE:
            return row, metadata
    return None, None


def test_one_voluntary_engagement_is_evidence_not_an_instant_preference(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    when = datetime(2025, 5, 2, 20, 0, tzinfo=timezone.utc).isoformat()

    with connect(db) as conn:
        result = settle_preference_adaptation(
            conn,
            ACTOR,
            action_name="read",
            target_id=BOOKSHELF,
            ended_sim_time=when,
        )
        conn.commit()

        assert result is not None
        assert result["score_after"] == 5.0
        assert result["preference_type"] is None
        assert _dynamic_projection(conn)[0] is None
        state = preference_adaptation_state(conn, ACTOR)[0]
        assert state["evidence_count"] == 1
        assert state["positive_evidence"] == 1
        assert state["negative_evidence"] == 0


def test_repeated_cross_day_engagement_establishes_like_and_reaches_cognition(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    start = datetime(2025, 5, 2, 20, 0, tzinfo=timezone.utc)

    with connect(db) as conn:
        for day in range(7):
            result = settle_preference_adaptation(
                conn,
                ACTOR,
                action_name="read",
                target_id=BOOKSHELF,
                ended_sim_time=(start + timedelta(days=day)).isoformat(),
            )
        conn.commit()

        row, metadata = _dynamic_projection(conn)
        assert result is not None
        assert result["status"] == "established"
        assert row is not None
        assert row["preference_type"] == "like"
        assert float(row["intensity"]) >= 35.0
        assert metadata["authority"] == "deterministic_preference_adaptation"

        context = ModelDecisionProvider(conn, character_id=ACTOR)._character_context()
        assert {"type": "like", "subject": row["subject"]} in context["preferences"]


def test_same_day_repetition_is_diminished(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    start = datetime(2025, 5, 2, 8, 0, tzinfo=timezone.utc)

    with connect(db) as conn:
        first = settle_preference_adaptation(
            conn,
            ACTOR,
            action_name="use",
            target_id=BOOKSHELF,
            ended_sim_time=start.isoformat(),
        )
        second = settle_preference_adaptation(
            conn,
            ACTOR,
            action_name="use",
            target_id=BOOKSHELF,
            ended_sim_time=(start + timedelta(hours=2)).isoformat(),
        )
        conn.commit()

        assert first is not None and second is not None
        assert second["temporal_weight"] == 0.25
        assert second["score_after"] == 6.25
        assert preference_adaptation_state(conn, ACTOR)[0]["distinct_evidence_days"] == 1
        assert _dynamic_projection(conn)[0] is None


def test_non_preference_actions_and_absence_of_choice_do_not_create_negative_evidence(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    when = datetime(2025, 5, 2, 20, 0, tzinfo=timezone.utc).isoformat()

    with connect(db) as conn:
        for action in ("train", "inspect", "eat", "drink", "rest", "idle", "move", "self_satisfaction"):
            assert settle_preference_adaptation(
                conn,
                ACTOR,
                action_name=action,
                target_id=BOOKSHELF,
                ended_sim_time=when,
            ) is None
        conn.commit()
        assert preference_adaptation_state(conn, ACTOR) == []
        assert _dynamic_projection(conn)[0] is None


def test_explicit_aversive_evidence_gradually_weakens_neutralizes_and_reverses_like(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    start = datetime(2025, 5, 2, 20, 0, tzinfo=timezone.utc)

    with connect(db) as conn:
        for day in range(7):
            settle_preference_adaptation(
                conn,
                ACTOR,
                action_name="read",
                target_id=BOOKSHELF,
                ended_sim_time=(start + timedelta(days=day)).isoformat(),
            )
        like, _ = _dynamic_projection(conn)
        assert like is not None and like["preference_type"] == "like"

        saw_neutral = False
        last = None
        for offset in range(7, 21):
            last = settle_preference_evidence(
                conn,
                ACTOR,
                target_id=BOOKSHELF,
                valence=-1,
                ended_sim_time=(start + timedelta(days=offset)).isoformat(),
                evidence_kind="represented_aversive_outcome",
            )
            if _dynamic_projection(conn)[0] is None:
                saw_neutral = True
        conn.commit()

        reversed_row, metadata = _dynamic_projection(conn)
        assert saw_neutral is True
        assert last is not None
        assert last["status"] == "established"
        assert last["preference_type"] == "dislike"
        assert reversed_row is not None
        assert reversed_row["preference_type"] == "dislike"
        assert float(reversed_row["intensity"]) >= 35.0
        assert metadata["source"] == SOURCE


def test_runtime_evidence_and_projection_survive_reinitialize_without_resetting_canonical_preferences(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    start = datetime(2025, 5, 2, 20, 0, tzinfo=timezone.utc)

    with connect(db) as conn:
        for day in range(7):
            settle_preference_adaptation(
                conn,
                ACTOR,
                action_name="read",
                target_id=BOOKSHELF,
                ended_sim_time=(start + timedelta(days=day)).isoformat(),
            )
        conn.commit()
        before = preference_adaptation_state(conn, ACTOR)
        assert _dynamic_projection(conn)[0] is not None

    initialize(db)

    with connect(db) as conn:
        after = preference_adaptation_state(conn, ACTOR)
        projection, _ = _dynamic_projection(conn)
        canonical = {
            (row["preference_type"], row["subject"])
            for row in conn.execute(
                "SELECT preference_type,subject FROM character_preferences WHERE entity_id=?",
                (ACTOR,),
            ).fetchall()
        }

        assert after == before
        assert projection is not None
        assert ("like", "intense training") in canonical
        assert ("dislike", "dishonesty") in canonical
