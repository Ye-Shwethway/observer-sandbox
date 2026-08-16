from observer_sandbox.telegram_bot import _fmt_location, _location_icon


def _location(access: str):
    return {
        "location": {
            "id": "loc_fixture",
            "name": "Fixture Place",
            "type": "location",
            "kind": "outdoor_zone",
            "access": access,
        },
        "child_locations": [],
        "occupants": [],
        "objects": [],
        "exits": [],
        "recent_activity": [],
    }


def test_resident_access_is_presented_as_policy_not_unavailability():
    text = _fmt_location(_location("resident"))

    assert "🏠 Access · Resident" in text
    assert "Access unavailable" not in text
    assert _location_icon(_location("resident")["location"]) != "🔒"


def test_private_access_is_presented_without_actor_denial_claim():
    text = _fmt_location(_location("private"))

    assert "🔐 Access · Private" in text
    assert "Access unavailable" not in text


def test_locked_and_closed_policies_keep_their_exact_blocked_semantics():
    locked = _fmt_location(_location("locked"))
    closed = _fmt_location(_location("closed"))

    assert "🔒 Access · Locked" in locked
    assert "⛔ Access · Closed" in closed
    assert _location_icon(_location("locked")["location"]) == "🔒"
    assert _location_icon(_location("closed")["location"]) == "⛔"


def test_unknown_access_policy_is_rendered_neutrally_instead_of_inventing_denial():
    text = _fmt_location(_location("staff_only"))

    assert "ℹ️ Access · Staff Only" in text
    assert "Access unavailable" not in text
