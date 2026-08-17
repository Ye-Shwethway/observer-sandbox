from __future__ import annotations

from observer_sandbox.db import connect
from observer_sandbox.memory_aware_decision import MemoryAwareDecisionProvider
from observer_sandbox.perception import PERCEPTION_MODE, recent_perception_context
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot
from observer_sandbox.world_stimulus import (
    create_world_stimulus,
    invalidate_exposure,
    record_character_exposure,
)


DARIAN = "char_darian"
SUITE = "loc_thorne_estate_master_suite"


def _expose(
    conn,
    *,
    stimulus_id: str,
    exposure_id: str,
    sim_time: str,
    subject: str = "Perception fixture",
    payload: dict | None = None,
):
    create_world_stimulus(
        conn,
        stimulus_id=stimulus_id,
        stimulus_type="information",
        channel="device",
        subject=subject,
        start_sim_time=sim_time,
        payload=payload or {"fact": "fixture"},
        source_type="fixture_source",
        source_id=f"source_{stimulus_id}",
        salience=0.7,
        metadata={"authority": "test_fixture"},
    )
    return record_character_exposure(
        conn,
        exposure_id=exposure_id,
        stimulus_id=stimulus_id,
        character_id=DARIAN,
        sim_time=sim_time,
        channel="device",
        source_location_id=SUITE,
        attention_hint=0.4,
        metadata={"delivery": "fixture"},
    )


def test_perception_projects_only_actor_exposure_with_world_provenance(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _expose(
            conn,
            stimulus_id="stim_perception_fixture",
            exposure_id="exposure_perception_fixture",
            sim_time="2025-05-03T11:02:00+00:00",
            subject="Device notice",
            payload={"headline": "Fixture headline"},
        )

        context = recent_perception_context(
            conn,
            DARIAN,
            sim_time="2025-05-03T11:03:00+00:00",
        )

        assert context["mode"] == PERCEPTION_MODE == "exposure_projection_v1"
        assert len(context["inputs"]) == 1
        item = context["inputs"][0]
        assert item["exposure_id"] == "exposure_perception_fixture"
        assert item["stimulus_id"] == "stim_perception_fixture"
        assert item["stimulus_type"] == "information"
        assert item["channel"] == "device"
        assert item["subject"] == "Device notice"
        assert item["world_payload"] == {"headline": "Fixture headline"}
        assert item["external_salience"] == 0.7
        assert item["attention_hint"] == 0.4
        assert {"type": "fixture_source", "id": "source_stim_perception_fixture"} in item["source_links"]
        assert {"type": "location", "id": SUITE} in item["source_links"]
        assert item["provenance"]["stimulus"]["authority"] == "test_fixture"
        assert item["provenance"]["exposure"]["delivery"] == "fixture"


def test_perception_omits_future_and_invalidated_exposure(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _expose(
            conn,
            stimulus_id="stim_past_invalid",
            exposure_id="exposure_past_invalid",
            sim_time="2025-05-03T10:00:00+00:00",
        )
        invalidate_exposure(conn, "exposure_past_invalid")
        _expose(
            conn,
            stimulus_id="stim_future",
            exposure_id="exposure_future",
            sim_time="2025-05-03T12:00:00+00:00",
        )

        context = recent_perception_context(
            conn,
            DARIAN,
            sim_time="2025-05-03T11:00:00+00:00",
        )
        assert context["inputs"] == []


def test_perception_projection_does_not_create_memory_mind_or_world_mutation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _expose(
            conn,
            stimulus_id="stim_boundary_fixture",
            exposure_id="exposure_boundary_fixture",
            sim_time="2025-05-03T11:02:00+00:00",
        )
        before = {
            "events": conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
            "memories": conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0],
            "cycles": conn.execute("SELECT COUNT(*) FROM mental_cycles").fetchone()[0],
            "episodes": conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0],
            "artifacts": conn.execute("SELECT COUNT(*) FROM mental_artifacts").fetchone()[0],
        }

        recent_perception_context(
            conn,
            DARIAN,
            sim_time="2025-05-03T11:03:00+00:00",
        )

        after = {
            "events": conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
            "memories": conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0],
            "cycles": conn.execute("SELECT COUNT(*) FROM mental_cycles").fetchone()[0],
            "episodes": conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0],
            "artifacts": conn.execute("SELECT COUNT(*) FROM mental_artifacts").fetchone()[0],
        }
        assert after == before


def test_normal_memory_aware_cognition_context_receives_perception_socket(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, DARIAN)
        _expose(
            conn,
            stimulus_id="stim_cognition_fixture",
            exposure_id="exposure_cognition_fixture",
            sim_time=str(state["sim_time"]),
            subject="Cognition-visible fixture",
        )

        provider = MemoryAwareDecisionProvider(
            conn,
            character_id=DARIAN,
            capture_context=False,
        )
        enriched = provider._enrich_state(state)

        assert enriched["perception"]["mode"] == PERCEPTION_MODE
        assert [item["subject"] for item in enriched["perception"]["inputs"]] == [
            "Cognition-visible fixture"
        ]
        assert "relevant_memories" in enriched
        assert "action_options" in enriched
