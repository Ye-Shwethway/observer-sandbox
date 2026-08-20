# Location Schema v2 — Representative Examples

Status: **L11.0 CONTRACT EXAMPLES**  
Date: 2026-08-21

These examples prove that `location-v2` can represent materially different spatial scales without inventing a second ontology.

They are contract examples, not canonical Real World content and not materialization instructions.

---

# Example A — Property / Building-style Location

```json
{
  "schema_version": "location-v2",
  "identity": {
    "key": "example_private_estate",
    "name": "Example Private Estate",
    "kind": "property",
    "description": "A private residential property containing a main residence, outdoor grounds and support facilities.",
    "functional_classes": ["residential", "recreation", "storage"],
    "tags": ["private", "estate"]
  },
  "structure": {
    "parent_ref": null,
    "exposure": "mixed"
  },
  "geography": {
    "address_text": null,
    "locality": "South Lake Tahoe",
    "region": "California",
    "country_code": "US",
    "position": null,
    "bounds": null
  },
  "spatial": {
    "area": {"value": 522720.0, "unit": "ft2"},
    "length": null,
    "width": null,
    "height": null,
    "elevation": null,
    "terrain": "Mixed landscaped grounds and wooded terrain.",
    "surface": "mixed",
    "orientation_notes": null
  },
  "boundary": {
    "type": "mixed",
    "enclosure": "partially_enclosed",
    "notes": "The represented property has a physical perimeter in some areas and conceptual/open boundary segments elsewhere."
  },
  "access": {
    "policy": {"mode": "owner_or_resident"}
  },
  "operations": {
    "initial_state": "open"
  },
  "topology": {
    "interfaces": [
      {
        "key": "main_gate",
        "name": "Main Gate",
        "kind": "gate",
        "destination_ref": null,
        "directionality": "two_way",
        "enabled": true,
        "traversal_modes": ["walk"],
        "base_duration_minutes": 1.0,
        "distance": null
      }
    ]
  },
  "facilities": {
    "capabilities": ["inspect", "enter", "leave", "rest", "recreate", "store"],
    "facility_types": ["living_space", "storage", "recreation"],
    "resource_types": ["potable_water", "electric_power", "data_network", "storage_capacity"],
    "utilities": ["electricity", "potable_water", "wastewater", "internet"]
  },
  "environment": {
    "lighting_profile": "variable",
    "weather_exposure": "variable"
  },
  "control": {
    "ownership_class": "private",
    "owner_ref": null,
    "operator_ref": null
  },
  "economic_policy": {
    "classification": "standalone_asset",
    "currency_code": "USD",
    "market_value_minor": null,
    "replacement_value_minor": null,
    "net_worth_treatment": "independent",
    "included_in_parent_ref": null,
    "valuation_method": "unknown"
  },
  "provenance": {
    "source_status": "creator_authored",
    "source_note": "Example only; not canonical content."
  }
}
```

### What this example proves

- a property can be a root/placeholder before a larger region is authored;
- real-world locality may be known while exact address/coordinates remain null;
- boundary, access and topology remain separate;
- facilities/resources are machine-readable evidence rather than name-derived affordances;
- economic classification can exist without inventing a market value;
- scale grading may use represented area only when a compatible property reference profile exists;
- physical quantities use the current shared unit vocabulary rather than inventing a Location-only unit.

---

# Example B — Room-style Location

```json
{
  "schema_version": "location-v2",
  "identity": {
    "key": "example_training_room",
    "name": "Strength Training Room",
    "kind": "room",
    "description": "An indoor room configured for resistance training and recovery support.",
    "functional_classes": ["training"],
    "tags": ["indoor", "strength_training"]
  },
  "structure": {
    "parent_ref": "sbx_loc_example_building",
    "exposure": "indoor"
  },
  "geography": {
    "address_text": null,
    "locality": null,
    "region": null,
    "country_code": null,
    "position": null,
    "bounds": null
  },
  "spatial": {
    "area": {"value": 850.0, "unit": "ft2"},
    "length": {"value": 34.0, "unit": "ft"},
    "width": {"value": 25.0, "unit": "ft"},
    "height": {"value": 10.0, "unit": "ft"},
    "elevation": null,
    "terrain": null,
    "surface": "interior_floor",
    "orientation_notes": "Main access is on the east side of the room."
  },
  "boundary": {
    "type": "physical",
    "enclosure": "enclosed",
    "notes": null
  },
  "access": {
    "policy": {"mode": "public"}
  },
  "operations": {
    "initial_state": "open"
  },
  "topology": {
    "interfaces": [
      {
        "key": "east_door",
        "name": "East Door",
        "kind": "door",
        "destination_ref": "sbx_loc_example_hallway",
        "directionality": "two_way",
        "enabled": true,
        "traversal_modes": ["walk"],
        "base_duration_minutes": 0.2,
        "distance": null
      }
    ]
  },
  "facilities": {
    "capabilities": ["inspect", "enter", "leave", "train", "rest"],
    "facility_types": ["strength_training"],
    "resource_types": ["electric_power", "potable_water"],
    "utilities": ["electricity", "potable_water", "cooling"]
  },
  "environment": {
    "lighting_profile": "mixed",
    "weather_exposure": "protected"
  },
  "control": {
    "ownership_class": "private",
    "owner_ref": null,
    "operator_ref": null
  },
  "economic_policy": {
    "classification": "component",
    "currency_code": "USD",
    "market_value_minor": null,
    "replacement_value_minor": null,
    "net_worth_treatment": "included_in_parent",
    "included_in_parent_ref": "sbx_loc_example_building",
    "valuation_method": "included_in_parent"
  },
  "provenance": {
    "source_status": "creator_authored",
    "source_note": "Example only; embedded Items are intentionally outside the Location member payload."
  }
}
```

### What this example proves

- child parentage is explicit and separate from its doorway connection;
- dimensions can be known for a room without requiring GIS geography;
- a functional label does not replace facility/capability evidence;
- an included-in-parent economic treatment remains separate from physical containment;
- embedded training equipment would be composed through the Location Creation orchestration layer using exact Item schemas, not through a generic contents field.

---

# Example C — Outdoor Zone with intentionally sparse evidence

```json
{
  "schema_version": "location-v2",
  "identity": {
    "key": "example_forest_clearing",
    "name": "Forested Clearing",
    "kind": "outdoor_zone",
    "description": "A small clearing inside a larger wooded property zone.",
    "functional_classes": ["wilderness", "recreation"],
    "tags": ["forest", "clearing"]
  },
  "structure": {
    "parent_ref": "sbx_loc_example_estate_woods",
    "exposure": "outdoor"
  },
  "geography": {
    "address_text": null,
    "locality": null,
    "region": null,
    "country_code": null,
    "position": null,
    "bounds": null
  },
  "spatial": {
    "area": null,
    "length": null,
    "width": null,
    "height": null,
    "elevation": null,
    "terrain": "Forested clearing with natural ground.",
    "surface": "soil",
    "orientation_notes": null
  },
  "boundary": {
    "type": "virtual",
    "enclosure": "unenclosed",
    "notes": "The clearing boundary is conceptual rather than walled."
  },
  "access": {
    "policy": {"mode": "public"}
  },
  "operations": {
    "initial_state": "open"
  },
  "topology": {
    "interfaces": []
  },
  "facilities": {
    "capabilities": ["inspect", "rest", "recreate"],
    "facility_types": [],
    "resource_types": [],
    "utilities": []
  },
  "environment": {
    "lighting_profile": "natural",
    "weather_exposure": "exposed"
  },
  "control": {
    "ownership_class": "private",
    "owner_ref": null,
    "operator_ref": null
  },
  "economic_policy": null,
  "provenance": {
    "source_status": "provisional",
    "source_note": "Exact dimensions and topology are intentionally unknown."
  }
}
```

### What this example proves

- a valid Location may remain intentionally sparse;
- unknown geometry and topology are not fabricated to force higher completeness;
- an outdoor conceptual boundary does not need walls;
- absent scale/connectivity/economic evidence produces ungraded dimensions rather than guessed grades.

---

# Grading expectations

These examples intentionally do not contain authored `grade`, `derived`, `evaluator`, `threshold` or `reference_profile` fields.

Expected read-time behavior:

- completeness derives from represented v2 facts;
- spatial scale is available only where valid size evidence plus a compatible kind reference exists;
- infrastructure capability is available only through registered semantic evidence and an applicable evaluator/reference;
- connectivity requires resolved graph context and therefore may remain ungraded at isolated-draft review time;
- asset value remains ungraded when market/reference evidence is insufficient;
- overall Location grade remains absent.
