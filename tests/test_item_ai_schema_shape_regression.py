from observer_sandbox.item_ai_contract import item_ai_fill_schema
from observer_sandbox.item_creation_schema import ITEM_CAPABILITIES, ITEM_KINDS, ITEM_MOBILITY, ITEM_MODULES
from observer_sandbox.item_metrics import DEFAULT_ITEM_METRIC_REGISTRY


def test_item_ai_schema_shape_tracks_validator_surface_exactly():
    schema = item_ai_fill_schema()
    definition = schema["properties"]["definition"]["properties"]
    modules = definition["modules"]["properties"]

    assert set(definition["kind"]["enum"]) == set(ITEM_KINDS)
    assert set(definition["mobility"]["enum"]) == set(ITEM_MOBILITY)
    assert set(definition["capabilities"]["items"]["enum"]) == set(ITEM_CAPABILITIES)
    assert set(modules) == set(ITEM_MODULES)

    metrics_any_of = modules["metrics"]["anyOf"]
    metric_schema = next(branch for branch in metrics_any_of if branch.get("type") == "object")
    assert set(metric_schema["properties"]) == set(DEFAULT_ITEM_METRIC_REGISTRY.metric_ids())
