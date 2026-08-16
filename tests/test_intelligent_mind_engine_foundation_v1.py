from __future__ import annotations

import sqlite3

import pytest

from observer_sandbox.db import SCHEMA_VERSION, connect, migrate
from observer_sandbox.mind_contract import (
    active_mental_context,
    complete_mental_cycle,
    create_mental_artifact,
    create_mental_cycle,
    link_mental_reference,
    record_mental_episode,
    set_mental_artifact_status,
)
from observer_sandbox.runtime import initialize


def test_schema_v8_installs_idempotent_character_generic_mind_foundation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert SCHEMA_VERSION == 8
        assert conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0] == "8"
        assert conn.execute("SELECT value FROM schema_meta WHERE key='mind_schema_version'").fetchone()[0] == "1"
        for table in ("mental_cycles", "mental_episodes", "mental_artifacts", "mental_links"):
            assert conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
            ).fetchone() is not None

        conn.execute(
            "INSERT INTO entities(id,entity_type,name) VALUES('char_fixture_mind','character','Fixture Mind')"
        )
        migrate(conn)
        cycle = create_mental_cycle(
            conn,
            character_id="char_fixture_mind",
            sim_time="2025-05-10T12:00:00+00:00",
            trigger_type="decision_wake",
        )
        assert conn.execute(
            "SELECT character_id FROM mental_cycles WHERE cycle_id=?", (cycle,)
        ).fetchone()[0] == "char_fixture_mind"


def test_foundation_records_structured_cycle_episode_artifact_and_links_without_world_mutation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        event_count_before = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        cycle = create_mental_cycle(
            conn,
            character_id="char_darian",
            sim_time="2025-05-10T12:00:00+00:00",
            trigger_type="decision_wake",
            input_summary={"socket_names": ["present_state", "recall"]},
        )
        episode = record_mental_episode(
            conn,
            cycle_id=cycle,
            mode="reflective",
            summary="Considers recent training experience",
            start_sim_time="2025-05-10T12:00:00+00:00",
            importance=0.7,
            persistence=0.3,
        )
        artifact = create_mental_artifact(
            conn,
            character_id="char_darian",
            artifact_type="concern",
            title="Recovery balance",
            sim_time="2025-05-10T12:00:00+00:00",
            source_cycle_id=cycle,
            priority=0.8,
        )
        link_mental_reference(
            conn,
            source_kind="episode",
            source_id=episode,
            target_kind="artifact",
            target_id=artifact,
            relation_type="raised_concern",
        )
        complete_mental_cycle(conn, cycle, output_summary={"episodes": 1, "artifacts": 1})
        conn.commit()

        context = active_mental_context(conn, "char_darian")
        assert context["episodes"][0]["mode"] == "reflective"
        assert context["active_artifacts"][0]["artifact_type"] == "concern"
        assert conn.execute("SELECT COUNT(*) FROM mental_links").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == event_count_before


def test_artifact_lifecycle_and_episode_vocabulary_are_bounded(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        cycle = create_mental_cycle(
            conn,
            character_id="char_darian",
            sim_time="2025-05-10T12:00:00+00:00",
            trigger_type="internal",
        )
        with pytest.raises(ValueError):
            record_mental_episode(
                conn,
                cycle_id=cycle,
                mode="magic_thought",
                summary="Invalid vocabulary",
                start_sim_time="2025-05-10T12:00:00+00:00",
            )

        artifact = create_mental_artifact(
            conn,
            character_id="char_darian",
            artifact_type="working_item",
            title="Temporary active item",
            sim_time="2025-05-10T12:00:00+00:00",
        )
        set_mental_artifact_status(
            conn, artifact, status="resolved", sim_time="2025-05-10T12:05:00+00:00"
        )
        row = conn.execute(
            "SELECT status,resolved_sim_time FROM mental_artifacts WHERE artifact_id=?", (artifact,)
        ).fetchone()
        assert row["status"] == "resolved"
        assert row["resolved_sim_time"] == "2025-05-10T12:05:00+00:00"


def test_cross_character_artifact_source_cycle_is_rejected(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        conn.execute(
            "INSERT INTO entities(id,entity_type,name) VALUES('char_other_mind','character','Other Mind')"
        )
        cycle = create_mental_cycle(
            conn,
            character_id="char_darian",
            sim_time="2025-05-10T12:00:00+00:00",
            trigger_type="decision_wake",
        )
        with pytest.raises(ValueError):
            create_mental_artifact(
                conn,
                character_id="char_other_mind",
                artifact_type="concern",
                title="Should fail",
                sim_time="2025-05-10T12:00:00+00:00",
                source_cycle_id=cycle,
            )
