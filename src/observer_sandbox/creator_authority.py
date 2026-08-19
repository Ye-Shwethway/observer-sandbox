from __future__ import annotations

from typing import Any


CREATOR_AUTHORITY = "creator"
CREATOR_PROFILE_CONTROL_SOURCE = "creator-profile-control-v1"
CREATOR_CREATION_SOURCE = "creator-creation-v1"
CREATOR_CONTROL_SOURCES = frozenset(
    {
        CREATOR_PROFILE_CONTROL_SOURCE,
        CREATOR_CREATION_SOURCE,
    }
)


def is_creator_authoritative(*, authority: Any = None, source: Any = None) -> bool:
    """Return whether persisted state is explicitly owned by Creator authority.

    This is the project-wide seed/import precedence boundary. Ordinary canonical
    baseline refreshes may initialize missing state, but they must never silently
    replace state explicitly approved or corrected by Creator.
    """

    return str(authority or "").strip().lower() == CREATOR_AUTHORITY or str(source or "").strip() in CREATOR_CONTROL_SOURCES


def ordinary_seed_may_replace(
    *,
    existing: bool,
    mode: Any = None,
    authority: Any = None,
    source: Any = None,
) -> bool:
    """Whether an ordinary canonical seed refresh may replace an existing value.

    Missing values may always be initialized. Simulated live state and explicit
    Creator state outrank seed/default state and therefore cannot be replaced by
    an ordinary initialization pass.
    """

    if not existing:
        return True
    if str(mode or "").strip().lower() == "simulated":
        return False
    if is_creator_authoritative(authority=authority, source=source):
        return False
    return True


__all__ = [
    "CREATOR_AUTHORITY",
    "CREATOR_CONTROL_SOURCES",
    "CREATOR_CREATION_SOURCE",
    "CREATOR_PROFILE_CONTROL_SOURCE",
    "is_creator_authoritative",
    "ordinary_seed_may_replace",
]
