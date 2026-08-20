from observer_sandbox.item_ai_contract import item_ai_fill_schema


def test_item_ai_schema_transport_is_closed():
    schema = item_ai_fill_schema()
    assert schema["additionalProperties"] is False
    assert schema["properties"]["definition"]["additionalProperties"] is False
