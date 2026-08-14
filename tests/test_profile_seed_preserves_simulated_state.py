from __future__ import annotations

import copy
import json

from observer_sandbox.db import connect
from observer_sandbox.profile_seed import import_seed, load_seed
from observer_sandbox.runtime import initialize
from observer_sandbox.world import DARIAN_SEED_PATH


def _profile_row(conn, field_key: str):
    return conn.execute(
        "SELECT value_json,mode,authority,source FROM character_profile_values WHERE entity_id=? AND field_key=?",
        ("char_darian", field_key),
    ).fetchone()


def test_reinitialize_preserves_engine_owned_simulated_profile_value(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        conn.execute(
            """UPDATE character_profile_values
            SET value_json=?,mode='simulated',authority='test-progression-engine',source='test-settlement'
            WHERE entity_id='char_darian' AND field_key='raps_pa.strength'""",
            (json.dumps(91.234),),
        )
        conn.commit()

    initialize(db)

    with connect(db) as conn:
        row = _profile_row(conn, "raps_pa.strength")
        assert row is not None
        assert json.loads(row["value_json"]) == 91.234
        assert row["mode"] == "simulated"
        assert row["authority"] == "test-progression-engine"
        assert row["source"] == "test-settlement"


def test_seed_can_still_update_non_simulated_canonical_field(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    seed = copy.deepcopy(load_seed(DARIAN_SEED_PATH))
    seed["canonical_revision"] = "test-canonical-revision"
    seed["values"]["body.height_in"]["value"] = 77.0

    with connect(db) as conn:
        before = _profile_row(conn, "body.height_in")
        assert before is not None and before["mode"] == "canonical"
        import_seed(conn, seed)
        after = _profile_row(conn, "body.height_in")
        assert after is not None
        assert json.loads(after["value_json"]) == 77.0
        assert after["mode"] == "canonical"
        assert after["source"] == "test-canonical-revision"
        history = conn.execute(
            """SELECT reason FROM character_profile_history
            WHERE entity_id='char_darian' AND field_key='body.height_in'
            ORDER BY id DESC LIMIT 1"""
        ).fetchone()
        assert history is not None and history["reason"] == "canonical seed update"
