import json
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize


def test_contextual_sexual_state_schema(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        rows = {
            row["field_key"]: dict(row)
            for row in conn.execute(
                """
                SELECT field_key, domain, data_type, unit, default_mode,
                       default_authority, sensitivity, metadata_json
                FROM profile_field_definitions
                WHERE field_key IN (
                    'sexual_anatomy.erectile_state',
                    'sexual_anatomy.erection_firmness',
                    'sexual_anatomy.erection_firmness_cap',
                    'sexual_anatomy.baseline_erectile_function',
                    'sexual_state.arousal_level'
                )
                """
            )
        }

    assert set(rows) == {
        "sexual_anatomy.erectile_state",
        "sexual_anatomy.erection_firmness",
        "sexual_anatomy.erection_firmness_cap",
        "sexual_anatomy.baseline_erectile_function",
        "sexual_state.arousal_level",
    }
    assert rows["sexual_anatomy.erection_firmness"]["default_mode"] == "simulated"
    assert rows["sexual_anatomy.erection_firmness"]["unit"] == "0-100"
    assert rows["sexual_anatomy.erection_firmness_cap"]["default_mode"] == "canonical"
    assert rows["sexual_state.arousal_level"]["default_mode"] == "simulated"

    firmness_meta = json.loads(rows["sexual_anatomy.erection_firmness"]["metadata_json"])
    assert firmness_meta["min"] == 0
    assert firmness_meta["max"] == 100
    assert firmness_meta["baseline_when_flaccid"] == 0


def test_darian_runtime_defaults_are_physiological_baseline():
    path = Path("config/characters/darian.runtime-defaults.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    values = data["values"]

    assert values["sexual_anatomy.erectile_state"]["value"] == "flaccid"
    assert values["sexual_anatomy.erection_firmness"]["value"] == 0
    assert values["sexual_anatomy.erection_firmness_cap"]["value"] == 100
    assert values["sexual_state.arousal_level"]["value"] == 0
    assert data["semantics"]["firmness_is_contextual"] is True
    assert data["semantics"]["arousal_is_separate"] is True
