from __future__ import annotations

import os
import signal
import time
from pathlib import Path

from .autonomy import autonomy_tick
from .db import connect
from .runtime import initialize

DB_PATH = Path(os.environ.get("OBSERVER_SANDBOX_DB", "/var/lib/observer-sandbox/observer.sqlite3"))
RUNNING = True


def _stop(_signum, _frame) -> None:
    global RUNNING
    RUNNING = False


def main() -> None:
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    initialize(DB_PATH)
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
