# Sandbox Item Creation v1

Status: ACTIVE IMPLEMENTATION CONTRACT  
Slice: I5.7

## Purpose

Materialize one I5.6-valid Item into Creation Sandbox state without mutating canonical Real World inventory, entity-definition, economic-value or relation tables.

The flow is:

`Manual/AI intent -> I5.6 exact Item validation -> target validation -> one atomic Sandbox transaction -> Item available for later Sandbox composition/runtime`

This slice is the single-Item path. Batch creation must reuse this semantic boundary rather than invent a second Item model.

## Storage mapping

I5.7 mirrors the existing canonical semantic split while keeping all mutable state Sandbox-owned:

- `creation_sandbox_item_definitions` — stable Item definition facts;
- `creation_sandbox_item_instances` — concrete unique instance or stack quantity/unit;
- `creation_sandbox_item_economic_profiles` — staged economic policy for that concrete Item;
- `creation_sandbox_relations` — current placement/storage/ownership/carriage/equipment relations;
- `creation_sandbox_objects` — generic Creator Creation object identity/lifecycle/provenance;
- `creation_sandbox_events` — materialization audit evidence.

No row is written to canonical `entity_definitions`, `entities`, `inventory_stacks`, `economic_value_profiles`, `economic_assets`, or canonical `relations`.

## Item socket

The generic creation envelope now registers `item` as a supported type with schema version 1. The generic socket remains deliberately shallow; I5.6 `validate_item_payload()` is authoritative for Item-specific semantics.

Generic socket validation must never replace the exact Item validator.

## Definition reuse

A Sandbox may contain multiple concrete instances sharing one `definition_key`.

Reuse is legal only when the complete definition-owned semantics match:

- schema version;
- name/kind/description;
- stackability and mobility;
- capabilities/tags;
- conditional modules;
- use requirements;
- derived Item-grade evidence.

If a Creator tries to reuse a stable definition key with different semantics, creation fails before a new Item object is written.

## Instance semantics

- non-stackable definitions create `instance_mode=unique`;
- stackable definitions create `instance_mode=stack` with validated positive quantity and canonical unit;
- definition facts are not copied into quantity state;
- quantity is instance state, not definition identity.

## Economic semantics

The exact I5.6 economic policy is staged per concrete Sandbox Item. It reuses the existing classification/treatment vocabulary but does not write canonical net-worth state.

Economic staging therefore means "this Item is internally coherent and ready for future adaptation/transmigration validation", not "this value is canonical wealth".

## Relation semantics

I5.7 materializes only explicit I5.6 relations:

- `located_at` -> active Sandbox Location;
- `stored_in` -> active Sandbox Location or Item carrying the `container` module;
- `owned_by` -> active Sandbox Character;
- `carried_by` -> active Sandbox Character;
- `equipped_by` -> active Sandbox Character.

Targets must be active and in the same Sandbox namespace. Cross-Sandbox relations fail closed.

I5.6 already ensures only one current physical placement mode among `located_at`, `stored_in`, `carried_by`, and `equipped_by`.

Ownership remains orthogonal to physical placement.

## Atomicity

One Item materialization transaction includes:

1. Item definition insertion/reuse;
2. generic Sandbox object insertion;
3. instance/stack insertion;
4. staged economic policy insertion;
5. explicit relation insertion;
6. materialization event.

A failure rolls back the Item graph. The Sandbox namespace itself may already exist independently and is not part of an Item transaction.

## Provenance

Each Item carries the generic creation provenance mode:

- `manual`;
- `ai_generated`;
- `imported`.

`requested_by` is retained when supplied. AI still cannot write Item state directly: AI output must pass I5.6 validation and the same I5.7 materialization service.

## Runtime boundary

Created Item != runtime affordance.

I5.7 does not expose training/eating/storage actions merely because a capability/module is present. Later runtime-affordance slices must adapt validated Item capabilities, requirements, colocation and state into deterministic options.

## Acceptance

I5.7 is complete when tests prove:

- Item socket registration preserves Character/Location socket behavior;
- unique Item materializes definition + instance + economic policy + audit event;
- stack Item preserves definition versus quantity/unit state;
- definition key reuse accepts exact semantic matches and rejects conflicts;
- explicit relations resolve only to legal active same-Sandbox targets;
- invalid target failure leaves zero new Item materialization;
- canonical state fingerprint is unchanged by Item creation;
- canonical entity/economic tables receive no Item rows;
- additive Sandbox Item tables migrate idempotently without changing global schema version 21.

## Deferred

Not in I5.7:

- Telegram Item creation UI;
- AI Item prompt generation UX;
- heterogeneous Item batch approval/rollback;
- edit/move/quantity-change/archive management UX;
- Location embedded-content orchestration;
- runtime affordance projection;
- canonical transmigration.
