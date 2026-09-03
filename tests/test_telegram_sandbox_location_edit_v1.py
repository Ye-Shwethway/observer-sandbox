from __future__ import annotations

import json

from observer_sandbox.creator_studio_location import manual_location_template
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_location_v2 import get_sandbox_location_v2, materialize_sandbox_location_v2
from observer_sandbox.sandbox_runtime import sandbox_runtime_status
from observer_sandbox.telegram_sandbox_location_edit import (
    get_sandbox_location_edit_session,
    handle_sandbox_location_edit_text,
)
from observer_sandbox.telegram_world_layers import sandbox_object_view, world_layer_callback_view


def _callbacks(keyboard):
    return {
        button.get("callback_data")
        for row in keyboard or []
        for button in row
        if isinstance(button, dict) and button.get("callback_data")
    }


def _payload(*, key: str = "place.edit.house", name: str = "Family House", kind: str = "building"):
    payload = manual_location_template()
    payload["identity"].update({
        "key": key,
        "name": name,
        "kind": kind,
        "description": f"A represented Location named {name}.",
    })
    return payload


def test_location_detail_exposes_field_by_field_identity_edit_preview_apply_done(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "77")

    with connect(db) as conn:
        location = materialize_sandbox_location_v2(conn, _payload())
        object_id = location["object_id"]
        runtime_before = sandbox_runtime_status(conn, location["sandbox_id"])

        detail_text, detail_keyboard = sandbox_object_view(conn, object_id)
        assert "Family House" in detail_text
        assert f"sw:ledit:start:{object_id}" in _callbacks(detail_keyboard)

        home_text, home_keyboard = world_layer_callback_view(conn, f"sw:ledit:start:{object_id}")
        assert "SANDBOX LOCATION EDIT" in home_text
        assert "you do not need to write JSON" in home_text
        assert "sw:ledit:s:identity" in _callbacks(home_keyboard)
        assert sandbox_runtime_status(conn, location["sandbox_id"]) == runtime_before

        section_text, section_keyboard = world_layer_callback_view(conn, "sw:ledit:s:identity")
        assert "IDENTITY · EDIT" in section_text
        assert "Select one field" in section_text
        assert "sw:ledit:f:in_name" in _callbacks(section_keyboard)
        assert "sw:ledit:json:identity" in _callbacks(section_keyboard)
        assert "complete replacement JSON" not in section_text

        prompt_text, _ = world_layer_callback_view(conn, "sw:ledit:f:in_name")
        assert "EDIT NAME" in prompt_text
        assert "Send the new text" in prompt_text
        assert "{" not in prompt_text

        preview = handle_sandbox_location_edit_text(conn, user_id=77, text="Edited Family House")
        assert preview is not None
        preview_text, preview_keyboard = preview
        assert "LOCATION EDIT PREVIEW" in preview_text
        assert "Edited Family House" in preview_text
        assert "sw:ledit:apply" in _callbacks(preview_keyboard)
        assert get_sandbox_location_v2(conn, object_id)["source"]["identity"]["name"] == "Family House"

        applied_text, applied_keyboard = world_layer_callback_view(conn, "sw:ledit:apply")
        assert "LOCATION EDIT APPLIED" in applied_text
        assert "Edited Family House" in applied_text
        assert "sw:ledit:done" in _callbacks(applied_keyboard)
        assert get_sandbox_location_v2(conn, object_id)["source"]["identity"]["name"] == "Edited Family House"
        assert sandbox_runtime_status(conn, location["sandbox_id"]) == runtime_before

        done_text, done_keyboard = world_layer_callback_view(conn, "sw:ledit:done")
        assert "EDIT MODE CLOSED" in done_text
        assert "No runtime pause was needed" in done_text
        assert f"sw:o:{object_id}" in _callbacks(done_keyboard)
        assert get_sandbox_location_edit_session(user_id=77) is None


def test_location_facilities_use_toggle_picker_instead_of_json(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "78")

    with connect(db) as conn:
        payload = _payload(key="place.edit.kitchen", name="Kitchen", kind="room")
        payload["facilities"]["capabilities"] = ["cook", "eat"]
        payload["facilities"]["utilities"] = ["electricity"]
        location = materialize_sandbox_location_v2(conn, payload)
        object_id = location["object_id"]

        world_layer_callback_view(conn, f"sw:ledit:start:{object_id}")
        section_text, section_keyboard = world_layer_callback_view(conn, "sw:ledit:s:facilities")
        assert "FACILITIES · EDIT" in section_text
        assert "sw:ledit:f:fac_cap" in _callbacks(section_keyboard)
        assert "sw:ledit:f:fac_type" in _callbacks(section_keyboard)
        assert "sw:ledit:f:fac_res" in _callbacks(section_keyboard)
        assert "sw:ledit:f:fac_util" in _callbacks(section_keyboard)

        picker_text, picker_keyboard = world_layer_callback_view(conn, "sw:ledit:f:fac_cap")
        assert "CAPABILITIES" in picker_text
        assert "Tap values to select/unselect" in picker_text
        assert "sw:ledit:tok:fac_cap:cook" in _callbacks(picker_keyboard)
        assert "sw:ledit:tok:fac_cap:sleep" in _callbacks(picker_keyboard)
        assert "sw:ledit:tokdone:fac_cap" in _callbacks(picker_keyboard)
        assert "{" not in picker_text

        toggled_text, _ = world_layer_callback_view(conn, "sw:ledit:tok:fac_cap:sleep")
        assert "Selected: 3" in toggled_text
        preview_text, preview_keyboard = world_layer_callback_view(conn, "sw:ledit:tokdone:fac_cap")
        assert "LOCATION EDIT PREVIEW" in preview_text
        assert "sleep" in preview_text
        assert "sw:ledit:apply" in _callbacks(preview_keyboard)
        assert get_sandbox_location_v2(conn, object_id)["source"]["facilities"]["capabilities"] == ["cook", "eat"]

        world_layer_callback_view(conn, "sw:ledit:apply")
        capabilities = get_sandbox_location_v2(conn, object_id)["source"]["facilities"]["capabilities"]
        assert set(capabilities) == {"cook", "eat", "sleep"}


def test_location_parent_reference_is_selected_by_name_not_raw_object_id(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "79")

    with connect(db) as conn:
        parent = materialize_sandbox_location_v2(conn, _payload(key="place.parent", name="Parent House", kind="building"))
        child = materialize_sandbox_location_v2(conn, _payload(key="place.child", name="Child Room", kind="room"))

        world_layer_callback_view(conn, f"sw:ledit:start:{child['object_id']}")
        world_layer_callback_view(conn, "sw:ledit:s:structure")
        picker_text, picker_keyboard = world_layer_callback_view(conn, "sw:ledit:f:st_parent")
        assert "PARENT LOCATION" in picker_text
        assert "Raw object IDs are not required" in picker_text
        buttons = [button for row in picker_keyboard for button in row]
        parent_buttons = [button for button in buttons if "Parent House" in button.get("text", "")]
        assert len(parent_buttons) == 1
        assert parent["object_id"] not in parent_buttons[0]["text"]

        preview_text, _ = world_layer_callback_view(conn, parent_buttons[0]["callback_data"])
        assert "LOCATION EDIT PREVIEW" in preview_text
        world_layer_callback_view(conn, "sw:ledit:apply")
        assert get_sandbox_location_v2(conn, child["object_id"])["source"]["structure"]["parent_ref"] == parent["object_id"]


def test_location_topology_has_structured_add_and_interface_editor(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "80")

    with connect(db) as conn:
        location = materialize_sandbox_location_v2(conn, _payload(key="place.topology", name="Topology Room", kind="room"))
        object_id = location["object_id"]

        world_layer_callback_view(conn, f"sw:ledit:start:{object_id}")
        topology_text, topology_keyboard = world_layer_callback_view(conn, "sw:ledit:s:topology")
        assert "Manage interfaces one at a time" in topology_text
        assert "sw:ledit:ifadd" in _callbacks(topology_keyboard)
        assert "sw:ledit:json:topology" in _callbacks(topology_keyboard)

        preview_text, preview_keyboard = world_layer_callback_view(conn, "sw:ledit:ifadd")
        assert "LOCATION EDIT PREVIEW" in preview_text
        assert "New Interface 1" in preview_text
        assert "sw:ledit:apply" in _callbacks(preview_keyboard)
        world_layer_callback_view(conn, "sw:ledit:apply")

        topology_text, topology_keyboard = world_layer_callback_view(conn, "sw:ledit:s:topology")
        assert "sw:ledit:if:0" in _callbacks(topology_keyboard)
        interface_text, interface_keyboard = world_layer_callback_view(conn, "sw:ledit:if:0")
        assert "NEW INTERFACE 1" in interface_text
        assert "sw:ledit:iff:name" in _callbacks(interface_keyboard)
        assert "sw:ledit:iff:kind" in _callbacks(interface_keyboard)
        assert "sw:ledit:iff:dest" in _callbacks(interface_keyboard)
        assert "sw:ledit:ifdel" in _callbacks(interface_keyboard)


def test_location_enum_field_rejects_impossible_free_text_path_and_preserves_source(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "81")

    with connect(db) as conn:
        location = materialize_sandbox_location_v2(conn, _payload(key="place.operations", name="Operations Room", kind="room"))
        object_id = location["object_id"]
        before = get_sandbox_location_v2(conn, object_id)["source"]

        world_layer_callback_view(conn, f"sw:ledit:start:{object_id}")
        world_layer_callback_view(conn, "sw:ledit:s:operations")
        choice_text, choice_keyboard = world_layer_callback_view(conn, "sw:ledit:f:op_state")
        assert "Choose the new value" in choice_text
        assert "sw:ledit:choose:op_state:open" in _callbacks(choice_keyboard)
        assert "sw:ledit:choose:op_state:locked" in _callbacks(choice_keyboard)
        assert handle_sandbox_location_edit_text(conn, user_id=81, text="teleporting") is None
        assert get_sandbox_location_v2(conn, object_id)["source"] == before
