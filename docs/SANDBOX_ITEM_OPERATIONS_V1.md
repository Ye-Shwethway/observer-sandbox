# Sandbox Item / Container Operations v1

Status: ACTIVE IMPLEMENTATION CONTRACT  
Slice: I5.9

## Purpose

Provide deterministic post-creation management for I5.7/I5.8 Sandbox Items without weakening I5.6 validation or silently destroying dependent Item state.

Supported operations:

- browse/inspect;
- validated full Item edit;
- physical placement/storage/carry/equip changes;
- ownership changes;
- stack quantity changes;
- dependency inspection;
- archive/delete with explicit dependent-detach policy.

All state remains Creation Sandbox-owned.

## Browse and inspect

`list_sandbox_items()` returns active Items by default and may explicitly include archived Items. `get_sandbox_item()` remains the detailed inspect/read model.

## Relation mutation

The relation vocabulary remains exact:

- `located_at`;
- `stored_in`;
- `owned_by`;
- `carried_by`;
- `equipped_by`.

`located_at`, `stored_in`, `carried_by`, and `equipped_by` are mutually exclusive physical-placement modes. Setting one replaces any existing physical-placement mode.

`owned_by` is orthogonal and is not removed by physical movement.

Targets must remain active, type-correct and in the same Sandbox. `stored_in` accepts Locations or container-capable Items. Storage cycles fail closed. Fixed Items cannot be carried/equipped.

After mutation, both normalized relation rows and the generic object relationship snapshot are synchronized.

## Stack quantity

Only `instance_mode=stack` Items have mutable quantity. Quantity may reach zero but may not become negative or non-finite. Definition canonical unit remains unchanged.

## Full edit

A full edit must pass the same I5.6 exact Item validator used at creation.

Stable identity constraints:

- `definition.key` is immutable after creation;
- instance mode (`unique` vs `stack`) is immutable after creation.

Definition facts may be revised through an Item only when that Item is the sole instance using the definition. If multiple concrete Items share the definition, one-instance edits may not silently rewrite shared semantics.

Per-instance economic policy, quantity and relations may be updated through validated state.

## Dependency handling

`item_dependencies()` reports incoming Sandbox relations to an Item. This is especially important for container Items whose contents use `stored_in`.

Archive/delete default behavior is fail-closed when incoming dependencies exist.

An explicit `detach_dependents=True` opts into removing those incoming relations before the container is archived/deleted. The dependent Items themselves are preserved. They are not recursively archived or deleted.

This prevents "delete refrigerator -> silently delete food" behavior.

## Archive

Item archive:

- preserves the Item definition/instance/economic record for history/readback;
- marks the generic Item object archived;
- removes the Item's outgoing active relations;
- requires explicit dependent detach when incoming dependencies exist;
- writes an audit event.

Archived Items cannot be mutated through active Item operations.

## Delete

Item delete permanently removes the concrete Sandbox object and its cascading instance/economic state.

The shared definition is deleted only when no other Sandbox Item instance references it. If another instance still uses the definition, the definition remains.

Incoming dependents require explicit detach exactly as archive does.

## Sandbox reset

Creation Sandbox reset clears concrete Item objects and all Item-specific instance/economic state. Shared Item definitions are also explicitly cleared because they are Sandbox-revision state rather than canonical catalog state.

This closes the orphan-definition case where object cascades alone would remove instances but leave definition rows behind.

## Isolation

All operations preserve canonical Real World state. No operation writes canonical entity/inventory/economic/relation/runtime tables.

## Acceptance

I5.9 is complete when tests prove:

- browse/inspect works for created Items;
- stack quantity updates including zero are valid while unique quantity changes fail;
- physical placement replacement and independent ownership are correct;
- storage cycles fail closed;
- full edit uses I5.6 and protects shared definitions;
- sole-instance definition/economic edit works;
- archive/delete refuse incoming dependencies by default;
- explicit detach preserves dependent Items while removing dependency relations;
- deleting one of several shared-definition instances keeps the definition;
- deleting the last instance removes the definition;
- Sandbox reset clears Item definitions as well as object-owned Item state;
- canonical fingerprint remains unchanged by Item operations.

## Deferred

Not part of I5.9:

- Telegram Item management UX;
- capacity/encumbrance enforcement;
- runtime consumption/training/equipment action execution;
- Location embedded-content authoring;
- canonical transmigration.
