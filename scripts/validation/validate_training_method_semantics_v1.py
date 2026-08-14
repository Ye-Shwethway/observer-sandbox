from __future__ import annotations

import json
import os
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.simulation import Action, apply_action
from observer_sandbox.training_methods import load_training_method_catalog, training_profile_for_target
from observer_sandbox.world import set_field


HOME_GYM = "loc_thorne_estate_home_gym"
TREADMILL = "obj_thorne_estate_gym_high_speed_treadmill"
FREE_WEIGHTS = "obj_thorne_estate_gym_free_weights"


def _prepare_gym(conn) -> None:
    set_field(conn, "char_darian", "runtime.location", HOME_GYM)
    set_field(conn, "char_darian", "runtime.current_action", "idle")
    set_field(conn, "char_darian", "needs.energy", 90.0)
    set_field(conn, "char_darian", "physiology.fatigue", 0.0, authority="physiology_engine", source="training-method-acceptance")
    conn.commit()


def _latest_payload(conn) -> dict[str, object]:
    row = conn.execute(
        "SELECT payload_json FROM events WHERE event_type='action_completed' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    assert row is not None
    return json.loads(row["payload_json"])


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires OBSERVER_VALIDATION_DISPOSABLE=1")

    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError(f"refusing non-temporary validation DB: {db_path}")

    conn = connect(db_path)
    catalog = load_training_method_catalog()
    methods = catalog["methods"]
    bindings = catalog["bindings"]
    assert catalog["revision"] == "training-method-semantics-v2"
    assert len(methods) == 17
    assert len(bindings) == 17
    assert set(bindings.values()) <= set(methods)
    assert all("primary_domains" not in method for method in methods.values())

    missing_targets = [
        target
        for target in bindings
        if conn.execute("SELECT 1 FROM entities WHERE id=? AND entity_type='object'", (target,)).fetchone() is None
    ]
    assert not missing_targets, missing_targets

    synthetic_catalog = {
        "revision": "synthetic-training-method-semantics-v2",
        "methods": {"barbell_strength_work": methods["barbell_strength_work"]},
        "bindings": {"obj_other_world_public_gym_rack": "barbell_strength_work"},
    }
    synthetic = training_profile_for_target("obj_other_world_public_gym_rack", catalog=synthetic_catalog)
    assert synthetic is not None
    assert synthetic["method_id"] == "barbell_strength_work"

    _prepare_gym(conn)
    apply_action(conn, Action("train", 30, TREADMILL, "steady aerobic work"))
    treadmill_payload = _latest_payload(conn)
    treadmill_method = treadmill_payload["training_method"]
    assert treadmill_method["method_id"] == "steady_state_cardio"
    assert treadmill_method["workload_channels"] == ["conditioning"]
    assert treadmill_method["effective_load"]["planned_minutes"] == 30
    assert "training_stimulus" not in treadmill_payload

    set_field(conn, "char_darian", "physiology.fatigue", 0.0, authority="physiology_engine", source="training-method-acceptance")
    set_field(conn, "char_darian", "needs.energy", 90.0)
    conn.commit()
    apply_action(conn, Action("train", 60, FREE_WEIGHTS, "strength work"))
    strength_payload = _latest_payload(conn)
    strength_method = strength_payload["training_method"]
    assert strength_method["method_id"] == "free_weight_strength"
    assert strength_payload["training_stimulus"]["domain"] == "strength"
    assert strength_payload["training_stimulus"]["target"] == FREE_WEIGHTS

    print(json.dumps({
        "ok": True,
        "validation_db": str(db_path),
        "catalog_revision": catalog["revision"],
        "reusable_method_count": len(methods),
        "target_binding_count": len(bindings),
        "all_targets_present_on_production_copy": True,
        "synthetic_non_thorne_binding": synthetic,
        "treadmill_method": treadmill_method,
        "treadmill_strength_stimulus": False,
        "free_weights_method": strength_method,
        "free_weights_strength_mapping_preserved": True,
        "model_calls": 0,
        "telegram_calls": 0,
        "production_mutated_by_validation": False,
    }, sort_keys=True))
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
