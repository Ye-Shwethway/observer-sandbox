from observer_sandbox import telegram_creator_bot, telegram_news
from observer_sandbox.db import connect
from observer_sandbox.information_media import create_tv_publication, import_external_articles
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_universe import universe_view


def _seed_bulletin(conn, *, editorial_provider_id="groq", editorial_model_id="news/model"):
    item_ids = import_external_articles(conn, [
        {
            "provider_id": "test_provider",
            "provider_ref": "story-telegram-news-1",
            "title": "Tahoe source report",
            "summary": "A represented historical source report for Telegram observability.",
            "source_name": "Tahoe Test News",
            "source_url": "https://example.invalid/tahoe-news-1",
            "published_at": "2025-05-01T06:45:00+00:00",
        },
        {
            "provider_id": "test_provider",
            "provider_ref": "story-telegram-news-2",
            "title": "Second Tahoe source report",
            "summary": "A second represented source report.",
            "source_name": "Tahoe Test News",
            "source_url": "https://example.invalid/tahoe-news-2",
            "published_at": "2025-05-01T06:50:00+00:00",
        },
    ])
    return create_tv_publication(
        conn,
        publication_id="publication_telegram_news_test",
        title="Morning News — 2025-05-01",
        summary="A compiled represented bulletin.",
        item_ids=item_ids,
        available_from="2025-05-01T07:00:00+00:00",
        available_until="2025-05-01T09:00:00+00:00",
        editorial_provider_id=editorial_provider_id,
        editorial_model_id=editorial_model_id,
    )


def test_universe_menu_exposes_news_alongside_weather(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _, keyboard = universe_view(conn)
        callbacks = [button["callback_data"] for row in keyboard for button in row]
        assert "uni:weather" in callbacks
        assert "uni:news" in callbacks


def test_news_view_is_read_only_and_shows_human_friendly_persisted_evidence(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_bulletin(conn)
        before = {
            "items": conn.execute("SELECT COUNT(*) FROM information_items").fetchone()[0],
            "publications": conn.execute("SELECT COUNT(*) FROM media_publications").fetchone()[0],
            "exposures": conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0],
            "memories": conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0],
            "mind": conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0],
        }

        text, keyboard = telegram_news.news_view(conn)

        after = {
            "items": conn.execute("SELECT COUNT(*) FROM information_items").fetchone()[0],
            "publications": conn.execute("SELECT COUNT(*) FROM media_publications").fetchone()[0],
            "exposures": conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0],
            "memories": conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0],
            "mind": conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0],
        }
        assert after == before
        assert "UNIVERSE NEWS" in text
        assert "Morning News — 2025-05-01" in text
        assert "Tahoe source report" in text
        assert "Second Tahoe source report" in text
        assert "AI · groq · news/model" in text
        assert "01-05-2025 (Thursday) 07:00 AM" in text
        assert "2025-05-01T07:00:00+00:00" not in text
        assert "A represented historical source report for Telegram observability.\n\n2. Second Tahoe source report" in text
        assert "does not expose any character" in text
        callbacks = [button["callback_data"] for row in keyboard for button in row]
        labels = [button["text"] for row in keyboard for button in row]
        assert "uni:news:generate" in callbacks
        assert "🧪 Test News Generation" in labels


def test_generate_news_view_runs_explicit_diagnostic_once_then_renders_persisted_result(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    calls = []
    with connect(db) as conn:
        monkeypatch.setattr(telegram_news, "news_generation_binding", lambda conn: {
            "provider_id": "groq",
            "model_id": "news/model",
        })
        cognition_before = {
            "exposures": conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0],
            "memories": conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0],
            "mind": conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0],
        }

        def fake_refresh(conn, sim_time):
            calls.append(sim_time)
            return _seed_bulletin(conn)

        text, _ = telegram_news.generate_news_view(conn, refresh_news=fake_refresh)
        cognition_after = {
            "exposures": conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0],
            "memories": conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0],
            "mind": conn.execute("SELECT COUNT(*) FROM mental_episodes").fetchone()[0],
        }
        assert calls == ["2025-05-01T07:00:00+00:00"]
        assert "News workflow completed with AI editorial: groq · news/model" in text
        assert "Morning News — 2025-05-01" in text
        assert cognition_after == cognition_before


def test_generate_news_view_warns_when_configured_ai_falls_back(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        monkeypatch.setattr(telegram_news, "news_generation_binding", lambda conn: {
            "provider_id": "groq",
            "model_id": "news/model",
        })

        def fallback_refresh(conn, sim_time):
            return _seed_bulletin(conn, editorial_provider_id=None, editorial_model_id=None)

        text, _ = telegram_news.generate_news_view(conn, refresh_news=fallback_refresh)
        assert "configured AI editorial was not used successfully" in text
        assert "Deterministic fallback" in text


def test_news_generation_callback_requires_creator_authority(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "222")
    with connect(db) as conn:
        text, keyboard = telegram_creator_bot._callback_view(conn, 222, "uni:news:generate")
        assert "Creator authority required" in text
        assert keyboard[0][0]["callback_data"] == "uni:news"

        calls = []
        monkeypatch.setattr(
            telegram_creator_bot,
            "generate_news_view",
            lambda conn: (calls.append(True) or ("generated", [[{"text": "← News", "callback_data": "uni:news"}]])),
        )
        text, _ = telegram_creator_bot._callback_view(conn, 111, "uni:news:generate")
        assert text == "generated"
        assert calls == [True]
