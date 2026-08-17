import json

import pytest

from observer_sandbox.information_media import (
    NEWS_BROADCAST_SLOTS as PUBLISHER_NEWS_SLOTS,
    TV_DEVICE_ID,
    create_tv_publication,
    import_external_articles,
)
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.media_runtime import NEWS_BROADCAST_SLOTS, media_cognition_context
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, set_runtime_value, snapshot, validate_action


LIVING_ROOM = "loc_thorne_estate_living_room"
ACTOR_ID = "char_darian"
SIM_TIME = "2025-05-14T22:09:00+00:00"
AVAILABLE_UNTIL = "2025-05-15T01:00:00+00:00"


def _publish_test_bulletin(conn):
    item_ids = import_external_articles(
        conn,
        [
            {
                "provider_id": "test_provider",
                "provider_ref": "media-action-story",
                "title": "Source-only headline must not leak into pre-exposure cognition",
                "summary": "Source-only summary must remain behind exposure.",
                "source_name": "Test News",
                "source_url": "https://example.invalid/media-action-story",
                "published_at": "2025-05-14T22:02:00+00:00",
            }
        ],
    )
    return create_tv_publication(
        conn,
        publication_id="publication_media_action_test",
        title="Evening News — 2025-05-14",
        summary="Editorial bulletin summary must also remain behind exposure.",
        item_ids=item_ids,
        available_from="2025-05-14T22:00:00+00:00",
        available_until=AVAILABLE_UNTIL,
    )


def _prepare_living_room(conn):
    set_dynamic_location(conn, ACTOR_ID, LIVING_ROOM)
    set_runtime_value(conn, "sim_time", SIM_TIME)
    conn.commit()


def test_media_console_and_action_are_authored_generically(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        capabilities = json.loads(
            conn.execute("SELECT capabilities_json FROM entities WHERE id=?", (TV_DEVICE_ID,)).fetchone()[0]
        )
        assert "consume_media" in capabilities
        definition = conn.execute(
            """SELECT target_mode,required_capability,requires_colocation,min_duration_minutes,max_duration_minutes
               FROM action_definitions WHERE action_type='consume_media'"""
        ).fetchone()
        assert tuple(definition) == ("object", "consume_media", 1, 5, 120)
        assert NEWS_BROADCAST_SLOTS == PUBLISHER_NEWS_SLOTS


def test_media_action_requires_current_publication_and_colocation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare_living_room(conn)
        assert not [option for option in action_options(conn, ACTOR_ID) if option["action"] == "consume_media"]

        publication = _publish_test_bulletin(conn)
        options = [option for option in action_options(conn, ACTOR_ID) if option["action"] == "consume_media"]
        assert len(options) == 1
        option = options[0]
        assert option["target"] == TV_DEVICE_ID
        assert option["media"]["publication_id"] == publication["publication_id"]
        assert option["media"]["program"] == "Evening News — 2025-05-14"
        assert "Source-only headline" not in json.dumps(option)
        assert "Source-only summary" not in json.dumps(option)

        set_dynamic_location(conn, ACTOR_ID, "loc_thorne_estate_master_suite")
        conn.commit()
        assert not [option for option in action_options(conn, ACTOR_ID) if option["action"] == "consume_media"]
        with pytest.raises(ValueError, match="not a local object"):
            validate_action(conn, ACTOR_ID, Action("consume_media", 20, TV_DEVICE_ID, "watch the available bulletin"))


def test_cognition_gets_schedule_and_availability_without_content_or_obligation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare_living_room(conn)
        _publish_test_bulletin(conn)
        before_exposures = conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0]
        context = media_cognition_context(conn, actor_id=ACTOR_ID, sim_time=SIM_TIME)
        encoded = json.dumps(context)
        assert context["news_schedule"]["timezone"] == "America/Los_Angeles"
        assert context["news_schedule"]["slots"] == [
            {"name": "Morning News", "local_time": "07:00"},
            {"name": "Evening News", "local_time": "18:00"},
        ]
        assert any(
            device["device_name"] == "Media Console"
            and device["location_name"] == "Living Room"
            and device["active_program"] == "Evening News — 2025-05-14"
            for device in context["devices"]
        )
        assert "Source-only headline" not in encoded
        assert "Source-only summary" not in encoded
        assert "Editorial bulletin summary" not in encoded
        assert "creates no obligation" in context["semantics"]
        assert conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0] == before_exposures

        enriched = ModelDecisionProvider(conn, character_id=ACTOR_ID, capture_context=False)._enrich_state(
            snapshot(conn, ACTOR_ID)
        )
        assert enriched["media_awareness"] == context


def test_completed_media_action_records_exposure_once_without_memory_or_mind_mutation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare_living_room(conn)
        publication = _publish_test_bulletin(conn)
        before_memory = conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0]
        before_mind = conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0]
        before_exposures = conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0]

        action = Action("consume_media", 20, TV_DEVICE_ID, "watch the available evening bulletin")
        apply_action(conn, action, ACTOR_ID, action_id="action_media_consumption_test")
        assert conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0] == before_exposures + 1
        exposure = conn.execute(
            "SELECT stimulus_id,channel,source_entity_id,metadata_json FROM character_exposures ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
        metadata = json.loads(exposure["metadata_json"])
        assert exposure["channel"] == "media"
        assert exposure["source_entity_id"] == TV_DEVICE_ID
        assert metadata["publication_id"] == publication["publication_id"]
        assert metadata["action_id"] == "action_media_consumption_test"
        assert metadata["proof"] == "completed_media_consumption_action"
        assert conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0] == before_memory
        assert conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0] == before_mind

        instance = conn.execute(
            "SELECT status,outcome_json FROM action_instances WHERE id='action_media_consumption_test'"
        ).fetchone()
        outcome = json.loads(instance["outcome_json"])
        assert instance["status"] == "completed"
        assert outcome["media_exposure"]["publication_id"] == publication["publication_id"]
        assert outcome["media_exposure"]["semantics"] == "exposure_only"

        apply_action(conn, action, ACTOR_ID, action_id="action_media_consumption_test")
        assert conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0] == before_exposures + 1
        assert conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0] == before_memory
        assert conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0] == before_mind
