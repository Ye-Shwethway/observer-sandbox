import gzip
import json
from datetime import datetime, timezone

from observer_sandbox import news_ai, telegram_ai_control
from observer_sandbox.ai import resolve_binding
from observer_sandbox.db import connect
from observer_sandbox.information_media import (
    TV_DEVICE_ID,
    ensure_historical_tv_news_for_sim_time,
    import_external_articles,
    media_publication,
    news_broadcast_slot,
    record_tv_exposure,
    refresh_historical_tv_news,
)
from observer_sandbox.runtime import initialize
from observer_sandbox.world import set_field


def _gal_blob(records):
    text = "\n".join(json.dumps(record) for record in records) + "\n"
    return gzip.compress(text.encode("utf-8"))


def test_information_truth_publication_and_exposure_stay_separate(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert conn.execute("SELECT device_type FROM media_devices WHERE entity_id=?", (TV_DEVICE_ID,)).fetchone()[0] == "television"
        before_memory = conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0]
        before_mind = conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0]
        item_ids = import_external_articles(conn, [{
            "provider_id": "test_provider",
            "provider_ref": "story-1",
            "title": "A reported event",
            "summary": "The outlet reports a bounded claim.",
            "source_name": "Test News",
            "source_url": "https://example.invalid/story-1",
            "published_at": "2025-05-23T18:00:00+00:00",
        }])
        assert conn.execute("SELECT verification_status FROM information_items WHERE item_id=?", (item_ids[0],)).fetchone()[0] == "reported"

        publication = refresh_historical_tv_news(
            conn,
            "2025-05-23T19:00:00+00:00",
            fetch=lambda url: _gal_blob([{
                "date": "2025-05-23T18:55:00Z",
                "url": "https://example.invalid/gdelt-story",
                "title": "Historical headline",
                "domain": "example.invalid",
                "outletName": "Example News",
                "description": "Historical source description.",
            }]) if "20250523190000" in url else None,
            lookback_minutes=15,
        )
        assert publication is not None
        stored = media_publication(conn, publication["publication_id"])
        assert stored["medium"] == "television"
        stimulus_id = f"stimulus_media_{stored['publication_id']}"
        stimulus = conn.execute("SELECT stimulus_type,channel FROM world_stimuli WHERE stimulus_id=?", (stimulus_id,)).fetchone()
        assert tuple(stimulus) == ("information", "media")
        assert conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0] == 0
        assert conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0] == before_mind
        assert conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0] == before_memory

        device_location = conn.execute(
            "SELECT source_id FROM relations WHERE relation_type='contains' AND target_id=? LIMIT 1",
            (TV_DEVICE_ID,),
        ).fetchone()[0]
        set_field(conn, "char_darian", "runtime.location", device_location)
        exposure = record_tv_exposure(
            conn,
            character_id="char_darian",
            publication_id=stored["publication_id"],
            sim_time="2025-05-23T19:05:00+00:00",
        )
        assert exposure["channel"] == "media"
        assert exposure["source_entity_id"] == TV_DEVICE_ID
        assert conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0] == before_mind
        assert conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0] == before_memory


def test_news_slot_uses_tahoe_local_time_and_materializes_once(tmp_path):
    slot = news_broadcast_slot("2025-05-23T19:00:00+00:00")
    assert slot == {
        "slot_id": "2025-05-23:morning",
        "slot_name": "morning",
        "label": "Morning News",
        "local_date": "2025-05-23",
        "available_from": "2025-05-23T14:00:00+00:00",
        "available_until": "2025-05-24T01:00:00+00:00",
    }

    db = tmp_path / "observer.sqlite3"
    initialize(db)
    calls = []

    def fetch(url):
        calls.append(url)
        if "20250523140000" not in url:
            return None
        return _gal_blob([{
            "date": "2025-05-23T13:55:00Z",
            "url": "https://example.invalid/scheduled-story",
            "title": "Scheduled historical headline",
            "domain": "example.invalid",
            "outletName": "Example News",
            "description": "Historical source description for the scheduled bulletin.",
        }])

    with connect(db) as conn:
        before_memory = conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0]
        before_mind = conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0]
        first = ensure_historical_tv_news_for_sim_time(
            conn,
            "2025-05-23T19:00:00+00:00",
            fetch=fetch,
            lookback_minutes=15,
            now=datetime(2026, 8, 17, 0, 0, tzinfo=timezone.utc),
        )
        assert first is not None
        assert first["title"] == "Morning News — 2025-05-23"
        assert first["available_from"] == "2025-05-23T14:00:00+00:00"
        assert first["available_until"] == "2025-05-24T01:00:00+00:00"
        call_count = len(calls)

        second = ensure_historical_tv_news_for_sim_time(
            conn,
            "2025-05-23T20:30:00+00:00",
            fetch=fetch,
            lookback_minutes=15,
            now=datetime(2026, 8, 17, 0, 1, tzinfo=timezone.utc),
        )
        assert second["publication_id"] == first["publication_id"]
        assert len(calls) == call_count
        assert conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0] == 0
        assert conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0] == before_mind
        assert conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0] == before_memory


def test_news_scheduler_throttles_same_slot_when_provider_has_no_records(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    calls = []

    def no_records(url):
        calls.append(url)
        return None

    with connect(db) as conn:
        first = ensure_historical_tv_news_for_sim_time(
            conn,
            "2025-05-23T19:00:00+00:00",
            fetch=no_records,
            lookback_minutes=15,
            now=datetime(2026, 8, 17, 0, 0, tzinfo=timezone.utc),
        )
        assert first is None
        call_count = len(calls)
        second = ensure_historical_tv_news_for_sim_time(
            conn,
            "2025-05-23T20:00:00+00:00",
            fetch=no_records,
            lookback_minutes=15,
            now=datetime(2026, 8, 17, 0, 5, tzinfo=timezone.utc),
        )
        assert second is None
        assert len(calls) == call_count


def test_news_binding_is_independent_and_probe_is_non_mutating(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        conn.execute("UPDATE ai_providers SET enabled=1 WHERE id='groq'")
        conn.execute("INSERT INTO ai_models(provider_id,model_id,display_name,active) VALUES('groq','news/model','news/model',1)")
        conn.commit()
        monkeypatch.setattr(news_ai, "generate_structured", lambda *args, **kwargs: {
            "title": "Probe bulletin",
            "summary": "Schema probe.",
            "stories": [{"source_item_id": "probe-source-1", "headline": "Probe", "summary": "Schema probe."}],
        })
        assert news_ai.news_generation_binding(conn) is None
        result = news_ai.probe_news_generation_model(conn, "groq", "news/model")
        assert result["ok"] is True
        assert news_ai.news_generation_binding(conn) is None
        binding = news_ai.activate_news_generation_model(conn, "groq", "news/model")
        assert binding["scope_type"] == "engine"
        assert binding["scope_id"] == "information_media"
        assert resolve_binding(conn, role="cognition", character_id="char_darian") is None


def test_telegram_news_ai_reuses_provider_model_test_save_flow(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        conn.execute("UPDATE ai_providers SET enabled=1 WHERE id='groq'")
        conn.execute("INSERT INTO ai_models(provider_id,model_id,display_name,active) VALUES('groq','news/model','News Model',1)")
        conn.commit()
        creator_home, creator_keyboard = telegram_ai_control.home_view(conn)
        creator_callbacks = [button["callback_data"] for row in creator_keyboard for button in row]
        assert "CREATOR SETTINGS" in creator_home
        assert "ai:settings" in creator_callbacks

        ai_home, keyboard = telegram_ai_control.callback_view(conn, 111, "ai:settings")
        callbacks = [button["callback_data"] for row in keyboard for button in row]
        assert "Character AI" in ai_home
        assert "News Generation AI" in ai_home
        assert "ai:n:home" in callbacks

        telegram_ai_control.callback_view(conn, 111, "ai:n:m:groq:0")
        monkeypatch.setattr(telegram_ai_control, "probe_news_generation_model", lambda conn, provider_id, model_id: {
            "ok": True, "provider_id": provider_id, "model_id": model_id, "latency_ms": 12, "tested_at": "2026-08-17T00:00:00+00:00"
        })
        tested, tested_keyboard = telegram_ai_control.callback_view(conn, 111, "ai:n:test")
        assert "Real inference succeeded" in tested
        assert any(button.get("callback_data") == "ai:n:save" for row in tested_keyboard for button in row)
        saved, _ = telegram_ai_control.callback_view(conn, 111, "ai:n:save")
        assert "NEWS GENERATION AI ACTIVATED" in saved
        assert news_ai.news_generation_binding(conn)["model_id"] == "news/model"
