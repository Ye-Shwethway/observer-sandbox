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
from .telegram_bot import run_polling

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
                autonomy_tick(conn)
        except Exception:
            # The scheduler records expected decision/completion failures itself.
            # An unexpected outer-loop failure must not kill the long-running service.
            pass
        time.sleep(2)


if __name__ == "__main__":
    main()
