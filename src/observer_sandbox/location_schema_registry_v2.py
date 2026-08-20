from __future__ import annotations

LOCATION_SCHEMA_VERSION = "location-v2"

LOCATION_KINDS = frozenset({
    "region", "property", "building", "floor", "room", "outdoor_zone",
    "boundary", "road", "path", "venue", "wilderness", "service_area",
})

FUNCTIONAL_CLASSES = frozenset({
    "residential", "commercial", "medical", "training", "recreation", "security",
    "storage", "food_service", "food_preparation", "administration", "research",
    "communications", "transport", "utility", "education", "wilderness", "mixed_use",
})

EXPOSURES = frozenset({"indoor", "covered_outdoor", "outdoor", "mixed", "unknown"})
SURFACES = frozenset({
    "interior_floor", "paved", "gravel", "soil", "grass", "sand", "rock",
    "snow_ice", "water", "mixed", "unknown",
})
BOUNDARY_TYPES = frozenset({"physical", "virtual", "mixed", "open", "unknown"})
ENCLOSURES = frozenset({"enclosed", "partially_enclosed", "unenclosed", "unknown"})
OPERATING_STATES = frozenset({"open", "closed", "locked", "blocked"})
INTERFACE_KINDS = frozenset({
    "door", "opening", "gate", "stairs", "elevator", "path_connection",
    "road_connection", "tunnel", "dock", "portal", "other",
})
DIRECTIONALITY = frozenset({"two_way", "outbound", "inbound"})
TRAVERSAL_MODES = frozenset({"walk"})

LOCATION_CAPABILITIES = frozenset({
    "inspect", "enter", "leave", "rest", "sleep", "train", "read", "research",
    "cook", "eat", "drink", "wash", "medical_care", "monitor", "communicate",
    "store", "work", "recreate",
})
FACILITY_TYPES = frozenset({
    "living_space", "sleeping_space", "sanitation", "food_preparation", "food_service",
    "strength_training", "combat_training", "cardio_training", "medical", "research",
    "communications", "security_monitoring", "storage", "workshop", "parking",
    "water_access", "recreation",
})
RESOURCE_TYPES = frozenset({
    "potable_water", "food_supply", "medical_supply", "electric_power", "data_network",
    "communications_link", "fuel_supply", "waste_disposal", "storage_capacity",
})
UTILITIES = frozenset({
    "electricity", "potable_water", "wastewater", "heating", "cooling", "internet",
    "communications",
})
LIGHTING_PROFILES = frozenset({"natural", "artificial", "mixed", "dark", "variable", "unknown"})
WEATHER_EXPOSURES = frozenset({"protected", "partial", "exposed", "variable", "unknown"})
OWNERSHIP_CLASSES = frozenset({"private", "public", "institutional", "communal", "unowned", "unknown"})
SOURCE_STATUSES = frozenset({"canonical", "creator_authored", "provisional", "imported"})
VALUE_CLASSIFICATIONS = frozenset({"standalone_asset", "component", "resource_proxy", "economically_immaterial"})
VALUE_TREATMENTS = frozenset({"independent", "included_in_parent", "excluded"})

__all__ = [name for name in globals() if name.isupper()]
