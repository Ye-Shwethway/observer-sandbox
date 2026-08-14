# Training Method Semantics v2

Status: ACTIVE CANDIDATE

## Purpose

Training methods are reusable semantic definitions. A concrete world object or training target may bind to one reusable method, but the method definition itself must not encode a character identity, estate identity, or world-specific object id.

This preserves the universal runtime rule:

`Actor + train action + concrete target + target->method binding + effective load -> method evidence -> domain progression engines`

Darian and the Thorne Estate remain production exemplars only.

## Separation of concerns

The catalog has two layers:

1. `methods`
   - keyed by stable `method_id`;
   - owns method name, family, workload channels, tags, and planning metadata;
   - contains no target id and no character id;
   - does not own attribute progression formulas or stimulus settlement.

2. `bindings`
   - maps a concrete trainable target/entity id to one reusable `method_id`;
   - allows different world objects to reuse the same method definition without copying semantic metadata.

Example:

`obj_thorne_estate_gym_power_rack -> barbell_strength_work`

A future `obj_other_world_public_gym_rack` may bind to the same `barbell_strength_work` definition with no engine change and no duplicated method profile.

## Runtime behavior

`training_profile_for_target(target)` resolves:

`target -> binding -> method definition`

The returned evidence still contains the concrete target id for event causality plus the stable method id for downstream progression semantics.

Unknown or unbound targets fail closed by returning no training-method evidence rather than guessing a method from object names.

## Catalog revision versus evidence revision

The catalog architecture is `training-method-semantics-v2`, but the persisted event evidence shape remains compatible with the existing `training-method-semantics-v1` evidence contract.

New evidence therefore carries both:

- `source = training-method-semantics-v1` — stable evidence-contract identity used by existing progression readers and historical events;
- `catalog_revision = training-method-semantics-v2` — the resolver/catalog architecture that produced the evidence.

This separation avoids invalidating historical Stamina/other progression evidence merely because target binding storage was refactored. No event migration is required.

Existing downstream consumers such as Body Composition and Body Measurement progression continue to use stable `method_id` / workload-channel evidence. Their numerical policies are not duplicated into this layer.

## Universal-character boundary

The training-method resolver is actor-independent. Actor-specific physiology, genetics, recovery, current attributes, and progression limits remain inputs to domain engines, never constants in the method catalog.

A future character using the same target receives the same method semantics but may receive different deterministic progression because their actor state and envelopes differ.

## Acceptance

The slice passes when:

- reusable definitions are separated from concrete target bindings;
- all current production training targets resolve to the same stable method ids as v1;
- cognition still exposes method metadata for train actions;
- completed training events still persist backward-compatible method evidence plus v2 catalog provenance;
- existing historical v1 evidence remains consumable by progression readers;
- current Strength and Stamina mappings remain unchanged;
- a synthetic non-Thorne target can bind to an existing method definition without duplicating that definition;
- no schema migration, additional model call, or Telegram call is introduced.

## Deferred refinement

Training Method Semantics v2 does not yet model exercise-level anatomy. A later movement/anatomy slice may add reusable movement patterns such as squat, hinge, horizontal press, vertical press, row, curl, extension, and calf raise, with primary/secondary regional loading consumed by BC-3.
