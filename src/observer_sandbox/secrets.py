from __future__ import annotations

import os
from pathlib import Path

DEFAULT_SECRET_FILE = Path(os.environ.get("OBSERVER_SECRET_FILE", "/var/lib/observer-sandbox/secrets.env"))


def load_runtime_secrets(path: str | Path | None = None) -> None:
    secret_path = Path(path) if path is not None else DEFAULT_SECRET_FILE
    if not secret_path.exists():
        return
    for raw_line in secret_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key and value and key not in os.environ:
            os.environ[key] = value
