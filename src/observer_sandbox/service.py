from __future__ import annotations

import os
import signal
import threading
import time
from pathlib import Path

from .actor_runtime import pending_action
from .autonomy import autonomy_tick
from .db import connect
from .runtime import initialize
from .secrets import load_runtime_secrets
from .simulation import snapshot
from .strength_progression_activation import maybe_settle_strength_progression
from .telegram_bot import run_polling
from .telegram_notifications import dispatch_action_completion

DB_PATH = Path(os.environ.get("OBSERVER_SANDBOX_DB", "/var/lib/observer-sandbox/observer.sqlite3"))
RUNNING = True


def _stop(_signum, _frame) -> None:
    global RUNNING
    RUNNING = False


def _active_actor_ids(conn) -> list[str]:
    return [row[0] for row in conn.execute("SELECT actor_id FROM actor_runtime WHERE autonomy_enabled=1 ORDER BY actor_id").fetchall()]


def main() -> None:
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    initialize(DB_PATH)
    load_runtime_secrets()

    telegram_thread: threading.Thread | None = None
    if os.environ.get("OBSERVER_TELEGRAM_BOT_TOKEN", "").strip():
        telegram_thread = threading.Thread(target=run_polling, args=(DB_PATH,), name="telegram-observer", daemon=True)
        telegram_thread.start()

    while RUNNING:
        try:
            with connect(DB_PATH) as conn:
                for actor_id in _active_actor_ids(conn):
                    pending_before = pending_action(conn, actor_id)
                    before = snapshot(conn, actor_id) if pending_before else None
                    result = autonomy_tick(conn, actor_id=actor_id)
                    if result.get("state") == "completed" and pending_before and before:
                        # Progression activation is checked only at completed-action
                        # simulation boundaries, never on the tight 2-second service
                        # poll. The activation policy bootstraps once, immediately
                        # settles eligible recovered Strength stimulus, and otherwise
                        # bounds pure detraining checkpoints to at most once per sim day.
                        after = result["after"]
                        try:
                            maybe_settle_strength_progression(
                                conn,
                                actor_id,
                                as_of_sim_time=str(after["sim_time"]),
                                state=after,
                            )
                            # Refresh the state after a possible tiny raw Strength
                            # settlement before cognition resolves the next action.
                            after = snapshot(conn, actor_id)
                        except Exception:
                            # Progression remains downstream of a successfully
                            # completed action. A progression failure must not roll
                            # back the action or kill continuous autonomy.
                            after = result["after"]

                        # The next normal decision boundary would occur on the next
                        # service poll anyway. Resolve it immediately so the single
                        # completion notification can show the Creator what is now
                        # in progress and when its next update is expected.
                        next_result = autonomy_tick(conn, actor_id=actor_id)
                        next_pending = next_result.get("pending") if next_result.get("state") == "planned" else None
                        dispatch_action_completion(
                            conn,
                            action_id=str(result["action_id"]),
                            action=pending_before,
                            before=before,
                            after=after,
                            next_action=next_pending,
                        )
        except Exception:
            # Scheduler failures are recorded per actor; observer delivery remains
            # downstream/best-effort and must never kill or roll back the universe.
            pass
        time.sleep(2)


if __name__ == "__main__":
    main()
