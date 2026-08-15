from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.personality_plasticity import (
    MAX_OVERLAY,
    personality_plasticity_context,
    personality_plasticity_state,
    record_personality_evidence,
    settle_personality_plasticity,
)
from observer_sandbox.runtime import initialize


ACTOR = "char_darian"
START = datetime(2025, 5, 2, 8, 0, tzinfo=timezone.utc)


def _canonical_traits(conn):
    return ModelDecisionProvider(conn, character_id=ACTOR)._profile_value("personality.primary_traits", [])


def _train_day(conn, day_offset: int):
    return settle_personality_plasticity(
        conn,
        ACTOR,
        action_name="train",
        ended_sim_time=(START + timedelta(days=day_offset)).isoformat(),
    )


def test_one_event_is_evidence_but_cannot_change_personality(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        before_traits = _canonical_traits(conn)
        result = _train_day(conn, 0)
        conn.commit()

        assert result is not None
        assert result["score_after"] == 1.0
        assert result["overlay"] == 0.0
        assert result["status"] == "baseline"
        assert personality_plasticity_context(conn, ACTOR) == []
        assert _canonical_traits(conn) == before_traits


def test_same_day_repetition_does_not_accelerate_long_horizon_gate(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        first = _train_day(conn, 0)
        second = settle_personality_plasticity(
            conn,
            ACTOR,
            action_name="train",
            ended_sim_time=(START + timedelta(hours=4)).isoformat(),
        )
        conn.commit()

        assert first is not None and second is not None
        assert first["daily_weight"] == 1.0
        assert second["daily_weight"] == 0.0
        assert second["score_after"] == 1.0
        state = personality_plasticity_state(conn, ACTOR)[0]
        assert state["evidence_count"] == 2
        assert state["effective_evidence"] == 1.0
        assert state["distinct_evidence_days"] == 1
        assert state["overlay"] == 0.0


def test_short_horizon_evidence_does_not_change_personality_even_with_many_days(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        result = None
        for day in range(14):
            result = _train_day(conn, day)
        conn.commit()

        assert result is not None
        assert result["distinct_evidence_days"] == 14
        assert result["effective_evidence"] == 14.0
        assert result["horizon_days"] == 13
        assert result["overlay"] == 0.0
        assert personality_plasticity_context(conn, ACTOR) == []


def test_long_horizon_evidence_creates_only_small_overlay_and_preserves_canonical_traits(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        before_traits = _canonical_traits(conn)
        result = None
        for offset in range(0, 28, 2):
            result = _train_day(conn, offset)
        conn.commit()

        assert result is not None
        assert result["distinct_evidence_days"] == 14
        assert result["horizon_days"] == 26
        assert result["overlay"] == 0.02
        assert abs(result["overlay"]) <= MAX_OVERLAY
        assert _canonical_traits(conn) == before_traits

        context = ModelDecisionProvider(conn, character_id=ACTOR)._character_context()
        assert context["personality"]["traits"] == before_traits
        assert context["personality"]["slow_adaptation"] == [
            {
                "trait": "disciplined",
                "direction": "strengthened",
                "magnitude": "slight",
                "overlay": 0.02,
            }
        ]
        assert "signed_score" not in str(context["personality"]["slow_adaptation"])
        assert "evidence_count" not in str(context["personality"]["slow_adaptation"])


def test_only_registered_trait_evidence_channels_are_accepted(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        with pytest.raises(ValueError, match="unregistered personality trait"):
            record_personality_evidence(
                conn,
                ACTOR,
                trait="reckless",
                valence=1,
                ended_sim_time=START.isoformat(),
                evidence_kind="invented_signal",
            )
        with pytest.raises(ValueError, match="unregistered evidence kind"):
            record_personality_evidence(
                conn,
                ACTOR,
                trait="disciplined",
                valence=1,
                ended_sim_time=START.isoformat(),
                evidence_kind="generic_reward",
            )
        assert personality_plasticity_state(conn, ACTOR) == []


def test_unregistered_ordinary_actions_do_not_become_personality_evidence(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        for action in ("read", "use", "eat", "drink", "shower", "rest", "inspect", "idle", "move", "sleep", "self_satisfaction"):
            assert settle_personality_plasticity(
                conn,
                ACTOR,
                action_name=action,
                ended_sim_time=START.isoformat(),
            ) is None
        conn.commit()
        assert personality_plasticity_state(conn, ACTOR) == []


def test_opposing_evidence_must_cross_neutral_over_a_similarly_long_horizon(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        for offset in range(0, 28, 2):
            _train_day(conn, offset)
        assert personality_plasticity_context(conn, ACTOR)[0]["direction"] == "strengthened"

        # Fourteen opposing observations erase the signed score but cannot flip it.
        for index in range(14):
            neutral = record_personality_evidence(
                conn,
                ACTOR,
                trait="disciplined",
                valence=-1,
                ended_sim_time=(START + timedelta(days=30 + index * 2)).isoformat(),
                evidence_kind="represented_counter_discipline_outcome",
            )
        assert neutral["score_after"] == 0.0
        assert neutral["overlay"] == 0.0
        assert personality_plasticity_context(conn, ACTOR) == []

        # Another long opposing run must accumulate before a slight softening appears.
        for index in range(14):
            softened = record_personality_evidence(
                conn,
                ACTOR,
                trait="disciplined",
                valence=-1,
                ended_sim_time=(START + timedelta(days=60 + index * 2)).isoformat(),
                evidence_kind="represented_counter_discipline_outcome",
            )
        conn.commit()

        assert softened["score_after"] == -14.0
        assert softened["overlay"] == -0.02
        assert personality_plasticity_context(conn, ACTOR)[0]["direction"] == "softened"


def test_overlay_is_bounded_and_survives_reinitialize_without_rewriting_profile(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        canonical = _canonical_traits(conn)
        for offset in range(0, 240, 2):
            _train_day(conn, offset)
        conn.commit()
        before = personality_plasticity_state(conn, ACTOR)
        assert before[0]["overlay"] == MAX_OVERLAY
        assert _canonical_traits(conn) == canonical

    initialize(db)

    with connect(db) as conn:
        after = personality_plasticity_state(conn, ACTOR)
        assert after == before
        assert _canonical_traits(conn) == canonical
        assert ModelDecisionProvider(conn, character_id=ACTOR)._character_context()["personality"]["slow_adaptation"]
