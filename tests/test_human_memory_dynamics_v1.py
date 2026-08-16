from __future__ import annotations

import json

from observer_sandbox.character_memory import retrieve_relevant_memories
from observer_sandbox.db import SCHEMA_VERSION, connect
from observer_sandbox.memory_dynamics import settle_memory_dynamics
from observer_sandbox.profile_observer import profile_menu, profile_section
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_memory import memory_view
from observer_sandbox.telegram_profile_browser import character_keyboard


ACTOR = "char_darian"
SUITE = "loc_thorne_estate_master_suite"


def _completed_event(
    conn,
    *,
    sim_time: str,
    action: str,
    location_id: str = SUITE,
    emotional_arousal: float = 0.1,
    personal_relevance: float = 0.5,
) -> int:
    payload = {
        "action": action,
        "duration_minutes": 30,
        "reason": "memory dynamics fixture",
        "memory_signals": {
            "emotional_arousal": emotional_arousal,
            "personal_relevance": personal_relevance,
        },
    }
    cur = conn.execute(
        """INSERT INTO events(sim_time,actor_id,event_type,payload_json,location_id,state_changes_json)
           VALUES(?,?,?,?,?,?)""",
        (sim_time, ACTOR, "action_completed", json.dumps(payload), location_id, "{}"),
    )
    return int(cur.lastrowid)


def test_memory_profile_is_independent_first_class_profile_domain(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        version = int(conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0])
        assert version == SCHEMA_VERSION
        values = {
            row["field_key"]: json.loads(row["value_json"])
            for row in conn.execute(
                "SELECT field_key,value_json FROM character_profile_values WHERE entity_id=? AND field_key LIKE 'memory.%'",
                (ACTOR,),
            ).fetchall()
        }
        assert values == {
            "memory.working_memory": 86.0,
            "memory.encoding": 89.0,
            "memory.retention": 84.0,
            "memory.recall": 91.0,
        }
        iq = json.loads(conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key='raps_ia.iq'",
            (ACTOR,),
        ).fetchone()[0])
        assert values["memory.recall"] != iq
        menu = profile_menu(conn, ACTOR, role="owner")
        assert "memory_ability" in {section["id"] for section in menu["sections"]}
        section = profile_section(conn, ACTOR, "memory_ability", role="owner")
        assert {item["field_key"] for item in section["content"]} == set(values)


def test_significant_memory_retains_more_gist_and_detail_than_mundane_memory(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        mundane_event = _completed_event(
            conn, sim_time="2025-05-02T08:00:00+00:00", action="idle",
            emotional_arousal=0.02, personal_relevance=0.15,
        )
        important_event = _completed_event(
            conn, sim_time="2025-05-02T08:01:00+00:00", action="observe",
            emotional_arousal=0.95, personal_relevance=0.95,
        )
        conn.commit()
        # Raise only the important event's authored salience; the dynamics engine remains event-agnostic.
        conn.execute("UPDATE character_memories SET salience=0.95 WHERE source_event_id=?", (important_event,))
        conn.execute("UPDATE character_memories SET salience=0.25 WHERE source_event_id=?", (mundane_event,))
        settle_memory_dynamics(conn, ACTOR, "2025-05-05T08:00:00+00:00")
        rows = conn.execute(
            "SELECT source_event_id,memory_strength,detail_strength FROM character_memories WHERE source_event_id IN (?,?)",
            (mundane_event, important_event),
        ).fetchall()
        by_event = {row["source_event_id"]: row for row in rows}
        assert by_event[important_event]["memory_strength"] > by_event[mundane_event]["memory_strength"]
        assert by_event[important_event]["detail_strength"] > by_event[mundane_event]["detail_strength"]


def test_represented_sleep_consolidates_only_memories_before_sleep(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before = _completed_event(conn, sim_time="2025-05-03T20:00:00+00:00", action="read")
        _completed_event(conn, sim_time="2025-05-03T23:00:00+00:00", action="sleep")
        after = _completed_event(conn, sim_time="2025-05-04T07:30:00+00:00", action="drink")
        conn.commit()
        settle_memory_dynamics(conn, ACTOR, "2025-05-04T08:00:00+00:00")
        rows = conn.execute(
            "SELECT source_event_id,lifecycle_stage,consolidated_sim_time FROM character_memories WHERE source_event_id IN (?,?)",
            (before, after),
        ).fetchall()
        by_event = {row["source_event_id"]: row for row in rows}
        assert by_event[before]["lifecycle_stage"] == "consolidated"
        assert by_event[before]["consolidated_sim_time"] == "2025-05-03T23:00:00+00:00"
        assert by_event[after]["lifecycle_stage"] == "recent"
        assert by_event[after]["consolidated_sim_time"] is None


def test_faded_memory_is_retained_and_context_cue_can_restore_access(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        event_id = _completed_event(conn, sim_time="2025-05-01T08:00:00+00:00", action="observe")
        conn.commit()
        memory_id = conn.execute(
            "SELECT memory_id FROM character_memories WHERE source_event_id=?", (event_id,)
        ).fetchone()[0]
        conn.execute(
            """UPDATE character_memories SET lifecycle_stage='faded',memory_strength=0.02,detail_strength=0.01,
                   salience=0.05,personal_relevance=0.05,last_dynamics_sim_time='2025-06-01T08:00:00+00:00'
               WHERE memory_id=?""",
            (memory_id,),
        )
        conn.commit()
        without_cue = retrieve_relevant_memories(
            conn, ACTOR, current_sim_time="2025-06-01T08:00:00+00:00",
            current_location_id="loc_thorne_estate_kitchen", available_actions=["eat"], limit=20,
            record_recall=False,
        )
        assert memory_id not in {item["memory_id"] for item in without_cue}
        with_cue = retrieve_relevant_memories(
            conn, ACTOR, current_sim_time="2025-06-01T08:00:00+00:00",
            current_location_id=SUITE, available_actions=["observe"], limit=20,
            record_recall=True,
        )
        assert memory_id in {item["memory_id"] for item in with_cue}
        row = conn.execute(
            "SELECT status,recall_count,memory_strength FROM character_memories WHERE memory_id=?", (memory_id,)
        ).fetchone()
        assert row["status"] == "active"
        assert row["recall_count"] == 1
        assert row["memory_strength"] > 0.02


def test_telegram_memory_is_dynamic_and_character_buttons_use_distinct_icons(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _completed_event(conn, sim_time="2025-05-02T08:00:00+00:00", action="observe")
        conn.execute(
            "INSERT OR REPLACE INTO runtime_state(key,value_json) VALUES('sim_time',?)",
            (json.dumps("2025-05-02T09:00:00+00:00"),),
        )
        conn.commit()
        text, _ = memory_view(conn, ACTOR)
        assert "Recent" in text and "Long-term" in text and "Faded" in text
        assert "Strength" in text and "Detail" in text
        keyboard = character_keyboard(ACTOR)
        memory_button = next(button for row in keyboard for button in row if "Memory" in button["text"])
        assert memory_button["text"].startswith("🗃️")
