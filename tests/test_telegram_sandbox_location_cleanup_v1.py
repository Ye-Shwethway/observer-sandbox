from __future__ import annotations

from observer_sandbox.creator_studio_location import manual_location_template
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_location_v2 import materialize_sandbox_location_v2
from observer_sandbox.telegram_world_layers import sandbox_object_view, world_layer_callback_view


def _callbacks(keyboard):
    return {
        button.get("callback_data")
        for row in keyboard or []
        for button in row
        if isinstance(button, dict) and button.get("callback_data")
    }


def _payload(*, key: str, name: str, kind: str = "room"):
    payload = manual_location_template()
    payload["identity"].update({
        "key": key,
        "name": name,
        "kind": kind,
        "description": f"Telegram cleanup fixture for {name}",
    })
    return payload


def test_location_detail_exposes_dependency_safe_delete_review_and_confirm(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "701")

    with connect(db) as conn:
        location = materialize_sandbox_location_v2(
            conn,
            _payload(key="place.telegram.cleanup", name="Disposable Room"),
        )
        object_id = location["object_id"]

        detail_text, detail_keyboard = sandbox_object_view(conn, object_id)
        assert "Disposable Room" in detail_text
        assert f"sw:ldel:start:{object_id}" in _callbacks(detail_keyboard)

        review_text, review_keyboard = world_layer_callback_view(conn, f"sw:ldel:start:{object_id}")
        assert "SANDBOX LOCATION CLEANUP" in review_text
        assert "No active Sandbox dependencies were found" in review_text
        assert "sw:ldel:apply" in _callbacks(review_keyboard)
        assert conn.execute(
            "SELECT count(*) FROM creation_sandbox_objects WHERE object_id=?",
            (object_id,),
        ).fetchone()[0] == 1

        done_text, done_keyboard = world_layer_callback_view(conn, "sw:ldel:apply")
        assert "SANDBOX LOCATION DELETED" in done_text
        assert "Canonical state fingerprint unchanged" in done_text
        assert "sw:list:location" in _callbacks(done_keyboard)
        assert conn.execute(
            "SELECT count(*) FROM creation_sandbox_objects WHERE object_id=?",
            (object_id,),
        ).fetchone()[0] == 0


def test_location_cleanup_review_blocks_parent_with_active_child_and_does_not_write(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "702")

    with connect(db) as conn:
        parent = materialize_sandbox_location_v2(
            conn,
            _payload(key="place.telegram.parent", name="Parent House", kind="building"),
        )
        child_payload = _payload(key="place.telegram.child", name="Dependent Room")
        child_payload["structure"]["parent_ref"] = parent["object_id"]
        materialize_sandbox_location_v2(conn, child_payload)

        review_text, review_keyboard = world_layer_callback_view(
            conn,
            f"sw:ldel:start:{parent['object_id']}",
        )

        assert "cannot be deleted yet" in review_text
        assert "Dependent Room" in review_text
        assert "Structural Parent" in review_text
        assert "sw:ldel:apply" not in _callbacks(review_keyboard)
        assert f"sw:o:{parent['object_id']}" in _callbacks(review_keyboard)
        assert conn.execute(
            "SELECT count(*) FROM creation_sandbox_objects WHERE object_id=?",
            (parent["object_id"],),
        ).fetchone()[0] == 1
