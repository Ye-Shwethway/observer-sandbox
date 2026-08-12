from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.profile_seed import import_seed, load_seed
from observer_sandbox.runtime import initialize


def test_darian_canonical_seed_imports_cleanly(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    seed = load_seed(Path("config/characters/darian.canonical.json"))

    with connect(db) as conn:
        import_seed(conn, seed)
        values = {
            row[0]: row[1]
            for row in conn.execute(
                "SELECT field_key, value_json FROM character_profile_values WHERE entity_id='char_darian'"
            )
        }
        revision = conn.execute(
            "SELECT canonical_revision FROM character_profiles WHERE entity_id='char_darian'"
        ).fetchone()[0]
        hobby_count = conn.execute(
            "SELECT COUNT(*) FROM character_hobbies WHERE entity_id='char_darian'"
        ).fetchone()[0]

    assert revision == "darian-canonical-v1"
    assert values["body.height_in"] == "76.0"
    assert values["body.weight_lb"] == "215.0"
    assert values["body.body_fat_pct"] == "9.0"
    assert values["raps_ia.iq"] == "140"
    assert values["sexual_anatomy.penis_length_in"] == "10.0"
    assert values["sexual_anatomy.penis_girth_in"] == "5.0"
    assert values["genetics.penis_length_in"] == "10.0"
    assert values["raps_sa.self_satisfaction_weekly"] == "0"
    assert hobby_count == 4


def test_darian_seed_is_idempotent(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    seed = load_seed(Path("config/characters/darian.canonical.json"))

    with connect(db) as conn:
        import_seed(conn, seed)
        import_seed(conn, seed)
        history_count = conn.execute(
            "SELECT COUNT(*) FROM character_profile_history WHERE entity_id='char_darian'"
        ).fetchone()[0]

    assert history_count == 0
