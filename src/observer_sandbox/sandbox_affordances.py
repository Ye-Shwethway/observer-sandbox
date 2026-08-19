from __future__ import annotations

import sqlite3
from typing import Any

from .sandbox_representation import derive_sandbox_action_options
from .sandbox_runtime import replace_sandbox_runtime_options, sandbox_runtime_options


def refresh_sandbox_runtime_options(
    conn: sqlite3.Connection,
    character_object_id: str,
) -> list[dict[str, Any]]:
    """Materialize only currently represented Character/Location affordances.

    This is deliberately deterministic and conservative. Future Item/Element/System
    sockets extend the derivation sources; they do not bypass this boundary.
    """
    derived = derive_sandbox_action_options(conn, character_object_id)
    replace_sandbox_runtime_options(conn, character_object_id, derived)
    return sandbox_runtime_options(conn, character_object_id)


__all__ = ["refresh_sandbox_runtime_options"]
