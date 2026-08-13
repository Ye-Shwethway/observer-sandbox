from __future__ import annotations

import json
import os
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.simulation import snapshot
from observer_sandbox.strength_progression_activation import maybe_settle_strength_progression


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("disposable validation required")
    path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(path):
        raise RuntimeError("temporary database required")

    conn = connect(path)
    state = snapshot(conn, "char_darian")
    boundary = str(state["sim_time"])
    first = maybe_settle_strength_progression(conn, "char_darian", as_of_sim_time=boundary, state=state)
    assert first["state"] in {"settled", "skipped"}
    second = maybe_settle_strength_progression(conn, "char_darian", as_of_sim_time=boundary, state=snapshot(conn, "char_darian"))
    assert second["state"] == "skipped"
    print(json.dumps({"ok": True, "first": first["state"], "replay": second["state"], "production_mutated_by_validation": False}, sort_keys=True))
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
