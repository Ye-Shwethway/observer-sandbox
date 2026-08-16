from __future__ import annotations

import json

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.semantic_memory_seed import seed_initial_semantic_memories
from observer_sandbox.spatial_familiarity import location_known, spatial_familiarity_state


def test_second_character_uses_same_semantic_spatial_seed_contract(tmp_path):
    db = tmp_path / "observer.sqlite3"
    seed_path = tmp_path / "semantic.json"
    initialize(db)

    with connect(db) as conn:
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json) VALUES(?,?,?,?,?)",
            ("char_fixture", "character", "Fixture Character", "{}", "[]"),
        )
        conn.commit()
        sim_time = json.loads(
            conn.execute("SELECT value_json FROM runtime_state WHERE key='sim_time'").fetchone()[0]
        )

        seed_path.write_text(
            json.dumps(
                {
                    "revision": "fixture-semantic-memory-v1",
                    "characters": [
                        {
                            "character_id": "char_fixture",
                            "memories": [
                                {
                                    "knowledge_kind": "spatial_familiarity",
                                    "location_id": "loc_thorne_estate_mansion_exterior",
                                    "familiarity": "aware",
                                    "basis": "fixture_initial_knowledge",
                                }
                            ],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        seed_initial_semantic_memories(conn, sim_time=sim_time, path=seed_path)

        state = spatial_familiarity_state(conn, "char_fixture")
        assert state is not None
        assert state["locations"]["loc_thorne_estate_mansion_exterior"]["familiarity"] == "aware"
        assert location_known(conn, "char_fixture", "loc_thorne_estate_mansion_exterior") is True
        assert location_known(conn, "char_fixture", "loc_thorne_estate_core_grounds") is False
        row = conn.execute(
            """SELECT source_type,event_sim_time,encoded_sim_time FROM character_memories
               WHERE character_id='char_fixture' AND memory_type='semantic'"""
        ).fetchone()
        assert row["source_type"] == "seed"
        assert row["event_sim_time"] == "2025-05-01T07:00:00+00:00"
        assert row["encoded_sim_time"] == sim_time
