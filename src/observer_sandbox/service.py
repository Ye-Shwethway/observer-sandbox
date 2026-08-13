from __future__ import annotations

import os
import signal
import threading
import time
from pathlib import Path

from .autonomy import autonomy_tick
from .db import connect
from .runtime import initialize
from .secrets import load_runtime_secrets
from .simulation import runtime_value, snapshot
from .telegram_bot import run_polling
from .telegram_notifications import dispatch_action_completion

DB_PATH = Path(os.environ.get("OBSERVER_SANDBOX_DB", "/var/lib/observer-sandbox/observer.sqlite3"))
RUNNING = True


def _stop(_signum, _frame) -> None:
    global RUNNING
    RUNNING = False


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
                pending_before = runtime_value(conn, "autonomy_pending_action", None)
                before = snapshot(conn) if pending_before else None
                result = autonomy_tick(conn)
                if result.get("state") == "completed" and pending_before and before:
                    dispatch_action_completion(
                        conn,
                        action_id=str(result["action_id"]),
                        action=pending_before,
                        before=before,
                        after=result["after"],
                    )
        except Exception:
            # The scheduler records expected decision/completion failures itself.
            # Notification delivery is best-effort and must never kill or roll back
            # the long-running universe runtime.
            pass
        time.sleep(2)


if __name__ == "__main__":
    main()
