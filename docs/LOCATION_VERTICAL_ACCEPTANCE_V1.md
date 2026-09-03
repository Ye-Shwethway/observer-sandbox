# Location Vertical Acceptance v1

Status: **L11.7 acceptance candidate**  
Date: **2026-09-03**

This document is the executable-evidence map for the final `location-v2` vertical acceptance gate. It does not create a second Location contract. Authority remains the exact Location schema/registry/materializer/Creator Studio services plus the Creation Section Implementation Standard.

## Acceptance principle

L11.7 is a vertical proof pass, not a new feature family. Existing regression evidence is reused where it already proves the required behavior. New tests are added only for representative cross-slice scenarios that were not previously exercised as one graph.

A passing L11.7 means the modern Sandbox Location vertical is accepted for the current scope. It does **not** authorize runtime activation, automatic transmigration, or destructive Real World reset by itself.

## Acceptance matrix

| # | Required proof | Executable evidence |
|---|---|---|
| 1 | Property/building hierarchy | `tests/test_location_vertical_acceptance_v1.py::test_l11_7_representative_property_building_room_outdoor_vertical`; `tests/test_sandbox_location_v2.py::test_child_location_requires_active_same_sandbox_v2_parent_and_materializes_contains` |
| 2 | Room/outdoor-zone hierarchy | `tests/test_location_vertical_acceptance_v1.py::test_l11_7_representative_property_building_room_outdoor_vertical` |
| 3 | Explicit interfaces/topology | `tests/test_location_vertical_acceptance_v1.py::test_l11_7_representative_property_building_room_outdoor_vertical`; `tests/test_sandbox_location_v2.py::test_multiple_interfaces_preserve_full_source_and_coarse_connected_projection`; `tests/test_sandbox_location_composition_v1.py::test_local_topology_is_resolved_to_created_location_ids` |
| 4 | Access policy distinct from operating state | `tests/test_location_schema_v2.py::test_v2_access_policy_is_separate_from_initial_operating_state` |
| 5 | Partial/unknown geography without fabrication | `tests/test_location_schema_v2.py::test_v2_unknown_precision_remains_null_and_grades_completeness_only`; representative L11.7 property keeps position/bounds unknown while retaining supplied locality/region/country |
| 6 | Boundary semantics | `tests/test_location_vertical_acceptance_v1.py::test_l11_7_representative_property_building_room_outdoor_vertical` proves enclosed physical room vs open/unenclosed outdoor zone in the same graph |
| 7 | Facility/resource/capability evidence | `tests/test_location_schema_v2.py::test_v2_registry_backed_facility_evidence_rejects_unknown_tokens`; representative L11.7 graph proves capabilities, facility types, resources and utilities persist through materialization |
| 8 | Derived completeness + applicable grading dimensions | `tests/test_location_schema_v2.py::test_v2_unknown_precision_remains_null_and_grades_completeness_only`; `test_v2_completeness_requires_resolved_traversal_evidence_for_l2_plus`; representative L11.7 room GradeProfile. Current policy intentionally activates completeness only and produces no automatic overall grade. Other dimensions remain evidence/reference gated. |
| 9 | Nested child Locations | `tests/test_sandbox_location_composition_v1.py::test_materialize_property_room_item_graph_resolves_local_refs_atomically`; representative L11.7 property -> building -> room plus property -> outdoor zone |
| 10 | Embedded multi-class Items | `tests/test_location_vertical_acceptance_v1.py::test_l11_7_embedded_item_kinds_and_storage_relationships_are_preserved` proves embedded `container` + `object` Item kinds with local `located_at` and `stored_in`; `tests/test_sandbox_location_composition_v1.py::test_item_can_be_stored_in_local_container_item` |
| 11 | Manual and AI parity | `tests/test_creator_studio_location_v2.py` Manual Guided/Exact JSON and AI tests both use exact `location-v2` validation and the shared revision-bound approval/materializer path; `tests/test_location_ai_contract_v2.py` covers the provider contract |
| 12 | Preview/export write-free | `tests/test_creator_studio_location_v2.py::test_manual_location_draft_preview_and_export_are_write_free`; `tests/test_creator_studio_location_composition_v1.py::test_location_composition_starter_is_exact_previewable_and_write_free`; `test_location_composition_telegram_method_preview_and_export` |
| 13 | Atomic approval | `tests/test_creator_studio_location_v2.py::test_location_telegram_revision_confirmation_materializes_via_v2_only`; `tests/test_creator_studio_location_composition_v1.py::test_location_composition_telegram_revision_bound_approval_materializes_whole_graph`; `tests/test_sandbox_location_composition_v1.py::test_mid_transaction_failure_rolls_back_all_members` |
| 14 | Invalid parent/cycle/cross-Sandbox/local-ref => zero writes | `tests/test_sandbox_location_v2.py::test_cross_sandbox_parent_fails_without_location_write`; `test_corrupt_existing_parent_cycle_is_rejected_before_new_writes`; `tests/test_sandbox_location_composition_v1.py::test_unknown_local_ref_and_parent_cycle_fail_before_writes`; Creator Studio failed-approval tests |
| 15 | Creator-friendly Edit Preview/Apply/Done parity | `tests/test_telegram_sandbox_location_edit_v1.py`; `tests/test_telegram_sandbox_location_edit_preview_human_v1.py`; normal path remains Section -> Field -> friendly input/choice -> changed-field Preview -> Apply -> Continue/Done, with raw JSON only as explicit advanced fallback |
| 16 | Dependency-safe cleanup | `tests/test_sandbox_location_cleanup_v2.py`; `tests/test_telegram_sandbox_location_cleanup_v1.py` prove fail-closed dependencies, stale review, Cancel invalidation and explicit safe deletion |
| 17 | Canonical Real World fingerprint unchanged | `tests/test_sandbox_location_v2.py`, `tests/test_creator_studio_location_v2.py`, composition tests, representative L11.7 tests, and `tests/test_sandbox_location_canonical_transaction_v2.py`. Update/delete canonical samples are taken inside the same writer transaction and mismatch rolls back before commit. |
| 18 | Approved Locations remain not runtime-active | `tests/test_sandbox_location_v2.py::test_root_location_materializes_without_runtime_activation_and_preserves_canonical_state`; Creator Studio approval, composition approval and representative L11.7 graph assert no actor runtime row is created for approved Locations/Items |

## Representative graph

The L11.7 cross-slice scenario intentionally exercises this graph in one atomic composition:

`Property -> Building -> Room`

`Property -> Outdoor Zone`

`Room <-> Outdoor Zone` through an explicit walkable door interface.

It also embeds two distinct Item kinds:

`Room <-located_at- Container <-stored_in- Object`

The property supplies only known locality/region/country while position and bounds remain `null`, proving partial geography is preserved rather than fabricated. The indoor room uses a physical/enclosed boundary while the outdoor zone uses open/unenclosed semantics. Registry-backed facilities/resources/utilities are persisted on represented Locations.

## Grading acceptance boundary

Current `location-v2` grading policy has one active universal dimension: **completeness**. The accepted behavior is therefore:

- completeness derives from validated Location evidence;
- no Creator/AI-authored grade authority;
- `GradeProfile.overall` remains `None`;
- spatial scale, infrastructure/facility capability, connectivity and asset value remain ungraded unless their approved evidence/reference sockets are actually available;
- security remains deferred until raw security evidence exists.

L11.7 must not manufacture grades merely to make the acceptance matrix look fuller.

## Closure rule

L11.7 may be marked closed only after the repository CI selected for this acceptance change passes, including the representative acceptance scenarios and all path-aware affected Location regressions. Any discovered implementation defect must be fixed narrowly and re-verified before closure.

After L11.7 closes, Location Creation is complete for the approved current scope and the next major authorized sequence is the Genesis transition beginning with **G1 — Prototype Content Reset Audit & Contract**. The later destructive reset remains a separate explicit operation, not an automatic consequence of this acceptance pass.
