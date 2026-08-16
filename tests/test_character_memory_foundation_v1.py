from __future__ import annotations

import json

from observer_sandbox.character_memory import retrieve_relevant_memories
from observer_sandbox.db import connect, migrate
from observer_sandbox.memory_aware_decision import MemoryAwareDecisionProvider
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot
from observer_sandbox.telegram_profile_browser import character_keyboard, profile_callback_view


def _insert_completed_event(conn, *, sim_time: str, location_id: str, action: str = "rest") -> int:
    cur = conn.execute(
        """INSERT INTO events(
            sim_time,actor_id,event_type,payload_json,location_id,state_changes_json
        ) VALUES(?,?,?,?,?,?)""",
        (
            sim_time,
            "char_darian",
            "action_completed",
            json.dumps(
                {
                    "action": action,
                    "duration_minutes": 30,
                    "reason": "represented completion fixture",
                }
            ),
            location_id,
            json.dumps({"needs.energy": {"before": 80.0, "after": 84.0}}),
        ),
    )
    return int(cur.lastrowid)


def test_schema_v6_encodes_completed_action_memory_once_and_is_idempotent(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        state = snapshot(conn, "char_darian")
        event_id = _insert_completed_event(
            conn,
            sim_time=str(state["sim_time"]),
            location_id=str(state["location"]),
        )
        conn.commit()

        row = conn.execute(
            """SELECT memory_id,character_id,memory_type,source_event_id,event_sim_time,recall_count
               FROM character_memories WHERE source_event_id=?""",
            (event_id,),
        ).fetchone()
        assert row is not None
        assert row["character_id"] == "char_darian"
        assert row["memory_type"] == "episodic"
        assert row["source_event_id"] == event_id
        assert row["recall_count"] == 0

        migrate(conn)
        assert conn.execute(
            "SELECT COUNT(*) FROM character_memories WHERE source_event_id=?",
            (event_id,),
        ).fetchone()[0] == 1
        assert conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()[0] == "6"


def test_retrieval_is_bounded_actor_scoped_and_updates_only_selected_recall_metadata(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        state = snapshot(conn, "char_darian")
        location_id = str(state["location"])
        first = _insert_completed_event(
            conn,
            sim_time="2025-05-10T08:00:00",
            location_id=location_id,
            action="rest",
        )
        second = _insert_completed_event(
            conn,
            sim_time="2025-05-10T09:00:00",
            location_id=location_id,
            action="read",
        )
        conn.commit()

        memories = retrieve_relevant_memories(
            conn,
            "char_darian",
            current_sim_time="2025-05-10T09:30:00",
            current_location_id=location_id,
            available_actions=["read", "rest"],
            limit=1,
            record_recall=True,
        )
        assert len(memories) == 1
        selected_id = memories[0]["memory_id"]
        rows = conn.execute(
            "SELECT memory_id,source_event_id,recall_count,last_recalled_sim_time FROM character_memories WHERE source_event_id IN (?,?)",
            (first, second),
        ).fetchall()
        by_id = {row["memory_id"]: row for row in rows}
        assert by_id[selected_id]["recall_count"] == 1
        assert by_id[selected_id]["last_recalled_sim_time"] == "2025-05-10T09:30:00"
        assert sum(int(row["recall_count"]) for row in rows) == 1


def test_memory_aware_provider_injects_memory_without_recalling_in_non_capture_mode(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        state = snapshot(conn, "char_darian")
        _insert_completed_event(
            conn,
            sim_time=str(state["sim_time"]),
            location_id=str(state["location"]),
            action="rest",
        )
        conn.commit()

        monkeypatch.setattr(
            ModelDecisionProvider,
            "_enrich_state",
            lambda self, raw_state: {"action_options": [{"action": "rest", "target": None}]},
        )
        provider = MemoryAwareDecisionProvider(
            conn,
            character_id="char_darian",
            capture_context=False,
        )
        enriched = provider._enrich_state(state)
        assert enriched["relevant_memories"]
        assert enriched["relevant_memories"][0]["type"] == "episodic"
        assert "action authority" in enriched["memory_guidance"]["instruction"]
        assert conn.execute("SELECT SUM(recall_count) FROM character_memories").fetchone()[0] == 0


def test_telegram_character_menu_exposes_live_memory_view(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        state = snapshot(conn, "char_darian")
        _insert_completed_event(
            conn,
            sim_time=str(state["sim_time"]),
            location_id=str(state["location"]),
            action="observe",
        )
        conn.commit()

        keyboard = character_keyboard("char_darian")
        assert any(button["text"] == "🧠 Memory" for row in keyboard for button in row)

        view = profile_callback_view(conn, "mem:char_darian:all:0", role="owner")
        assert view is not None
        text, memory_keyboard = view
        assert "Darian Thorne · MEMORY" in text
        assert "Episodic 1" in text
        assert "Observe" in text
        assert memory_keyboard is not None
        assert any("Episodes" in button["text"] for row in memory_keyboard for button in row)
