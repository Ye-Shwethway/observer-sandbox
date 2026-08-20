# Universal Location Schema v2

Status: **L11.0 SCHEMA CONTRACT — AUTHORITATIVE FOR NEW LOCATION CREATION IMPLEMENTATION**  
Date: 2026-08-21

## Purpose

`location-v2` is the versioned successor to `location-v1` for modern Creator Studio Location Creation.

It preserves the stable semantics already established by the world/location contracts while adding the minimum high-value dimensions needed for long-term universe building: geography, explicit boundary semantics, typed interfaces, registry-backed functional/facility/resource vocabulary, definition-versus-runtime state ownership, minimal control/ownership semantics, and explicit grading evidence boundaries.

This is a schema contract only. Runtime materialization, Telegram UI, AI structured fill and canonical transmigration remain later slices.

Core invariant:

> **A Location is a stable spatial identity plus authored spatial structure, policy/configuration and declared capability evidence. Live changing world state is downstream runtime authority.**

`location-v2` does not create a second Location ontology. It is the explicit incompatible evolution of `location-v1`.

---

# 1. Exact top-level payload

A `location-v2` payload contains exactly:

- `schema_version`
- `identity`
- `structure`
- `geography`
- `spatial`
- `boundary`
- `access`
- `operations`
- `topology`
- `facilities`
- `environment`
- `control`
- `economic_policy`
- `provenance`

Unknown top-level or nested fields fail closed.

`derived` is never an authored input field. Derived completeness/grading output is produced only by validators/read-time grading adapters.

---

# 2. Identity

Exact fields:

- `key` — stable lowercase technical token; required.
- `name` — human display name; required.
- `kind` — registry-backed spatial role; required.
- `description` — concise authored description; required.
- `functional_classes` — zero or more registry-backed functional classifications.
- `tags` — zero or more stable descriptive tokens.

Initial `kind` registry:

- `region`
- `property`
- `building`
- `floor`
- `room`
- `outdoor_zone`
- `boundary`
- `road`
- `path`
- `venue`
- `wilderness`
- `service_area`

Initial `functional_classes` registry:

- `residential`
- `commercial`
- `medical`
- `training`
- `recreation`
- `security`
- `storage`
- `food_service`
- `food_preparation`
- `administration`
- `research`
- `communications`
- `transport`
- `utility`
- `education`
- `wilderness`
- `mixed_use`

The registry is expandable. A class is descriptive/queryable evidence; it does not grant access, topology or executable actions by itself.

---

# 3. Structure

Exact fields:

- `parent_ref` — nullable reference to the intended structural parent Location.
- `exposure` — one of `indoor`, `covered_outdoor`, `outdoor`, `mixed`, `unknown`.

Rules:

- one canonical structural parent in v2;
- structural Location hierarchy uses `contains` when materialized;
- parentage does not create `connected_to` topology;
- the materialized Location parent graph must be acyclic;
- root/placeholder Locations may use null `parent_ref` where valid.

---

# 4. Geography

Exact fields:

- `address_text` — nullable free-text postal/street address when represented.
- `locality` — nullable city/town/locality name.
- `region` — nullable administrative region/state/province.
- `country_code` — nullable ISO-3166-style uppercase alpha-2 code.
- `position` — nullable geographic point.
- `bounds` — nullable coarse geographic bounds.

`position` exact fields:

- `latitude` — finite decimal degrees in `[-90, 90]`.
- `longitude` — finite decimal degrees in `[-180, 180]`.

`bounds` exact fields:

- `south`
- `west`
- `north`
- `east`

Bounds use finite decimal degrees and must satisfy `south <= north`; longitude values remain in `[-180,180]`. Antimeridian-spanning bounds are deferred rather than silently inferred.

Rules:

- geography is optional evidence;
- unknown addresses/coordinates remain null;
- AI must not fabricate coordinates/address precision merely to improve completeness;
- geographic position does not replace structural parentage or topology.

---

# 5. Spatial

Exact fields:

- `area`
- `length`
- `width`
- `height`
- `elevation`
- `terrain`
- `surface`
- `orientation_notes`

The five measurements use the shared physical quantity contract and may be null.

`terrain` is nullable descriptive text for bounded terrain facts not yet represented by a registry.

Initial `surface` registry:

- `interior_floor`
- `paved`
- `gravel`
- `soil`
- `grass`
- `sand`
- `rock`
- `snow_ice`
- `water`
- `mixed`
- `unknown`

`orientation_notes` is nullable descriptive layout/orientation evidence.

Unknown geometry remains null. The validator does not invent dimensions, coordinates, area, elevation or geometry.

---

# 6. Boundary

Exact fields:

- `type`
- `enclosure`
- `notes`

`type` registry:

- `physical`
- `virtual`
- `mixed`
- `open`
- `unknown`

`enclosure` registry:

- `enclosed`
- `partially_enclosed`
- `unenclosed`
- `unknown`

`notes` is nullable descriptive boundary evidence.

Boundary describes the separation between inside/outside this spatial container. It is not access authorization, topology, or an executable barrier system.

---

# 7. Access

Exact fields:

- `policy`

`policy` reuses the shared universal requirement/access contract.

Access answers **who/what is authorized to enter or use the Location under represented policy**. It does not answer whether an interface exists or whether the Location is currently open.

---

# 8. Operations

Exact fields:

- `initial_state`

Initial state registry:

- `open`
- `closed`
- `locked`
- `blocked`

This is Creation-owned initial seed/configuration only.

After runtime activation, live changing operating state belongs to runtime authority and must not be silently reset from the Creation payload on ordinary initialization/reload.

Opening schedules, service hours and complex operating calendars are deferred until a concrete runtime consumer requires them.

---

# 9. Topology / interfaces

`topology` contains exactly:

- `interfaces`

Each interface contains exactly:

- `key`
- `name`
- `kind`
- `destination_ref`
- `directionality`
- `enabled`
- `traversal_modes`
- `base_duration_minutes`
- `distance`

Initial interface kind registry:

- `door`
- `opening`
- `gate`
- `stairs`
- `elevator`
- `path_connection`
- `road_connection`
- `tunnel`
- `dock`
- `portal`
- `other`

Directionality registry:

- `two_way`
- `outbound`
- `inbound`

Initial supported traversal modes:

- `walk`

`destination_ref` may be null while composing a draft, but must resolve before a materialized traversable connection is activated.

`enabled` is authored initial topology state. A later runtime topology system may own live enable/disable state after activation.

`base_duration_minutes` is nullable positive finite numeric evidence.

`distance` is a nullable shared physical quantity of kind `length`.

Rules:

- containment never creates an interface automatically;
- an interface is not access permission;
- duplicate interface keys fail;
- unsupported traversal modes fail closed;
- `portal` is merely a typed interface token; target-universe compatibility/policy decides whether such semantics are legitimate.

---

# 10. Facilities, resources and capabilities

`facilities` contains exactly:

- `capabilities`
- `facility_types`
- `resource_types`
- `utilities`

All are zero-or-more stable registry-backed tokens.

Initial Location capability registry:

- `inspect`
- `enter`
- `leave`
- `rest`
- `sleep`
- `train`
- `read`
- `research`
- `cook`
- `eat`
- `drink`
- `wash`
- `medical_care`
- `monitor`
- `communicate`
- `store`
- `work`
- `recreate`

Initial facility type registry:

- `living_space`
- `sleeping_space`
- `sanitation`
- `food_preparation`
- `food_service`
- `strength_training`
- `combat_training`
- `cardio_training`
- `medical`
- `research`
- `communications`
- `security_monitoring`
- `storage`
- `workshop`
- `parking`
- `water_access`
- `recreation`

Initial resource type registry:

- `potable_water`
- `food_supply`
- `medical_supply`
- `electric_power`
- `data_network`
- `communications_link`
- `fuel_supply`
- `waste_disposal`
- `storage_capacity`

Initial utility registry:

- `electricity`
- `potable_water`
- `wastewater`
- `heating`
- `cooling`
- `internet`
- `communications`

Rules:

- labels such as `Gym` or `Hospital` do not grant actions;
- executable affordances must later resolve from represented capability/facility/resource evidence plus deterministic runtime contracts;
- registry count alone is not a grade.

---

# 11. Environment

Exact fields:

- `lighting_profile`
- `weather_exposure`

`lighting_profile` registry:

- `natural`
- `artificial`
- `mixed`
- `dark`
- `variable`
- `unknown`

`weather_exposure` registry:

- `protected`
- `partial`
- `exposed`
- `variable`
- `unknown`

These are stable authored environment-profile facts, not live weather or live illumination state.

Live temperature, precipitation, visibility, hazards, sensor readings and other changing environmental conditions belong to downstream environment/runtime systems.

Utilities are represented under `facilities.utilities`, not duplicated here.

---

# 12. Control / ownership

Exact fields:

- `ownership_class`
- `owner_ref`
- `operator_ref`

Ownership class registry:

- `private`
- `public`
- `institutional`
- `communal`
- `unowned`
- `unknown`

`owner_ref` and `operator_ref` are nullable entity references.

Rules:

- ownership/control does not imply physical presence;
- residency and current occupancy are relationships/runtime state, not embedded identity facts;
- references must resolve according to the materialization/dependency contract before becoming authoritative relationships;
- access policy remains independent from ownership classification.

---

# 13. Economic policy

`economic_policy` remains nullable and reuses the existing economic-value semantics.

Supported initial classifications:

- `standalone_asset`
- `component`
- `resource_proxy`
- `economically_immaterial`

Supported net-worth treatments:

- `independent`
- `included_in_parent`
- `excluded`

Exact economic fields remain:

- `classification`
- `currency_code`
- `market_value_minor`
- `replacement_value_minor`
- `net_worth_treatment`
- `included_in_parent_ref`
- `valuation_method`

`included_in_parent` requires an explicit parent asset reference.

Economic value is separate from Location access, completeness, infrastructure capability and spatial scale.

---

# 14. Provenance

Exact fields:

- `source_status`
- `source_note`

Source status registry:

- `canonical`
- `creator_authored`
- `provisional`
- `imported`

This is content/source provenance. It remains separate from the generic Creation proposal provenance describing Manual/AI/import generation mode.

---

# 15. Definition / initial / runtime ownership boundary

Creation-owned stable facts include:

- identity/classification;
- structural parent proposal;
- geography;
- physical extent evidence;
- boundary profile;
- access policy;
- interface definitions;
- facility/resource/capability/utility declarations;
- stable environment profile;
- control/economic/provenance facts.

Creation-owned initial-state seed includes:

- `operations.initial_state`;
- interface `enabled` initial state.

Runtime-owned changing state includes, after activation:

- current open/closed/locked/blocked state;
- temporary interface availability;
- current occupants/presence;
- live weather/temperature/visibility/lighting;
- temporary hazards;
- dynamic resources/consumption;
- current service/facility outages;
- current actor/entity `located_at` state.

Ordinary runtime initialization must not reapply Creation initial-state seed over explicit live/runtime-owned state.

---

# 16. Grading boundary

Location grades are not authored fields.

Derived grading contract:

`authoritative Location facts + registered Location grading dimensions/evaluators + optional reference profiles + universe grading policy -> GradeProfile`

Initial grading dimensions:

1. `completeness` — mandatory derived interpretation of L0-L4 representation completeness.
2. `spatial_scale` — evidence/reference gated; magnitude only, not quality.
3. `infrastructure_capability` — evidence/reference gated from registered facilities/resources/capabilities/utilities; never raw string count.
4. `connectivity` — graph-context gated from resolved interfaces/topology; not access permission or design quality.
5. `asset_value` — economic/reference/universe gated; no timeless global currency threshold.
6. `security` — reserved; not active until an authoritative raw security evidence contract exists.

`GradeProfile.overall` is null in the first v2 implementation. Any overall/composite Location grade requires a separately approved explicit context-specific composite evaluator.

The authoritative field-to-grade evidence classification is defined in `docs/LOCATION_GRADING_EVIDENCE_MATRIX_V1.md`.

---

# 17. Completeness derivation

Retain the conceptual L0-L4 model with v2 evidence:

- **L0 — identity placeholder:** valid identity only.
- **L1 — structural container:** parent/root role plus structural/exposure/boundary semantics.
- **L2 — traversable place:** L1 plus explicit interface/topology and access semantics sufficient for represented traversal.
- **L3 — usable place:** L2 plus at least one machine-readable capability/facility/resource/utility affordance evidence.
- **L4 — living-configured place:** L3 plus represented operational/environment/economic/control configuration that enables downstream changing world state.

The completeness evaluator describes representation depth only. It never grants runtime readiness, access or prestige.

---

# 18. Composition boundary

`location-v2` itself contains no arbitrary `contents` bag.

Creation composition is an orchestration layer:

- child Locations use exact `location-v2` member payloads;
- embedded Items use the exact current Item member schema;
- local references are resolved before writes;
- structural child Location materializes through `contains`;
- movable Item normally uses `located_at`;
- Item stored in a typed container uses `stored_in`;
- ownership remains independent;
- whole graph validates before one atomic Sandbox apply.

---

# 19. Validation policy

Blocking v2 validation includes:

- exact object fields / schema version;
- stable key/token/enums;
- finite/ranged coordinates and quantities;
- valid shared access/economic contracts;
- unique interface keys;
- supported interface/traversal vocabulary;
- positive duration/distance when represented;
- valid reference syntax;
- materialization-time same-Sandbox reference resolution, acyclicity and dependency closure;
- isolation/authority violations.

Non-blocking by default:

- missing optional geometry/geography;
- subjective realism/aesthetic quality;
- perfect facility taxonomy coverage;
- fine-grained building-code realism;
- optimal pricing;
- missing optional grade dimensions.

Unknown evidence remains null/ungraded rather than fabricated.

---

# 20. Compatibility and implementation transition

`location-v1` remains supported only by the existing pre-L11.1 validator/runtime code until the implementation is migrated.

Transition order:

1. L11.0 locks this contract.
2. L11.1 implements `location-v2` registries/canonicalizer/validator/grading adapters and compatibility tests.
3. New Creator Location UI/AI/materialization uses `location-v2` only.
4. `location-v1` is not silently accepted as `location-v2`; any future migration adapter must be explicit and deterministic.

No Real World legacy Location migration is required because the approved Genesis plan retires prototype-era canonical content.
