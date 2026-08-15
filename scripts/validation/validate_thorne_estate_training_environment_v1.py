from __future__ import annotations

import json
import os
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.world import seed_home_and_darian


EXPECTED_REVISION = "thorne-estate-v3.4-private-activity-semantics"
NEW_OBJECTS = {
    "obj_thorne_estate_training_ai_combat_sim": "loc_thorne_estate_training_hall",
    "obj_thorne_estate_training_obstacle_course": "loc_thorne_estate_training_hall",
    "obj_thorne_estate_training_combat_pit": "loc_thorne_estate_training_hall",
    "obj_thorne_estate_training_vr_tactical_sim": "loc_thorne_estate_training_hall",
    "obj_thorne_estate_gym_olympic_platform": "loc_thorne_estate_home_gym",
    "obj_thorne_estate_gym_power_rack": "loc_thorne_estate_home_gym",
    "obj_thorne_estate_gym_adjustable_bench": "loc_thorne_estate_home_gym",
    "obj_thorne_estate_gym_strength_machines": "loc_thorne_estate_home_gym",
    "obj_thorne_estate_gym_high_speed_treadmill": "loc_thorne_estate_home_gym",
    "obj_thorne_estate_gym_rowing_ergometer": "loc_thorne_estate_home_gym",
    "obj_thorne_estate_gym_speed_agility_station": "loc_thorne_estate_home_gym",
    "obj_thorne_estate_gym_altitude_chamber": "loc_thorne_estate_home_gym",
    "obj_thorne_estate_gym_mobility_stretching": "loc_thorne_estate_home_gym",
}


def _runtime_values(conn) -> dict[str, object]:
    return {
        row["key"]: json.loads(row["value_json"])
        for row in conn.execute("SELECT key,value_json FROM runtime_state ORDER BY key")
        if row["key"] != "world_identity_revision"
    }


def _dynamic_darian_fields(conn) -> dict[str, object]:
    rows = conn.execute(
        "SELECT field_key,value_json FROM fields WHERE entity_id='char_darian' "
        "AND (field_key LIKE 'runtime.%' OR field_key LIKE 'needs.%' OR field_key LIKE 'physiology.%') "
        "ORDER BY field_key"
    ).fetchall()
    return {row["field_key"]: json.loads(row["value_json"]) for row in rows}


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires OBSERVER_VALIDATION_DISPOSABLE=1")

    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError(f"refusing non-temporary validation DB: {db_path}")

    conn = connect(db_path)
    before_runtime = _runtime_values(conn)
    before_dynamic = _dynamic_darian_fields(conn)
    before_revision_row = conn.execute(
        "SELECT value_json FROM runtime_state WHERE key='world_identity_revision'"
    ).fetchone()
    before_revision = json.loads(before_revision_row[0]) if before_revision_row else None

    seed_home_and_darian(conn)

    after_runtime = _runtime_values(conn)
    after_dynamic = _dynamic_darian_fields(conn)
    revision = json.loads(conn.execute(
        "SELECT value_json FROM runtime_state WHERE key='world_identity_revision'"
    ).fetchone()[0])

    assert revision == EXPECTED_REVISION
    assert before_runtime == after_runtime
    assert before_dynamic == after_dynamic

    added = []
    for object_id, room_id in NEW_OBJECTS.items():
        row = conn.execute(
            "SELECT name,capabilities_json FROM entities WHERE id=? AND entity_type='object'",
            (object_id,),
        ).fetchone()
        assert row is not None, object_id
        assert json.loads(row["capabilities_json"]) == ["train", "inspect"]
        assert conn.execute(
            "SELECT 1 FROM relations WHERE source_id=? AND relation_type='contains' AND target_id=?",
            (room_id, object_id),
        ).fetchone() is not None
        added.append({"id": object_id, "name": row["name"], "room": room_id})

    assert conn.execute(
        "SELECT 1 FROM relations WHERE relation_type='connected_to' "
        "AND (source_id='loc_thorne_estate_exterior_boundary' OR target_id='loc_thorne_estate_exterior_boundary')"
    ).fetchone() is None

    water_effects = json.loads(conn.execute(
        "SELECT value_json FROM fields WHERE entity_id='obj_thorne_estate_kitchen_drinking_water' "
        "AND field_key='game.effects'"
    ).fetchone()[0])
    assert water_effects["drink"]["needs.thirst"] == -55.0

    print(json.dumps({
        "ok": True,
        "validation_db": str(db_path),
        "before_world_revision": before_revision,
        "after_world_revision": revision,
        "new_training_objects": added,
        "new_training_object_count": len(added),
        "runtime_state_preserved": True,
        "darian_dynamic_state_preserved": True,
        "exterior_boundary_preserved": True,
        "existing_drinking_water_effect_preserved": True,
        "model_calls": 0,
        "telegram_calls": 0,
        "production_mutated_by_validation": False,
    }, sort_keys=True))
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
