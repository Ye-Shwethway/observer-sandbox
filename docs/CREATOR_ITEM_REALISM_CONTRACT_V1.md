# Creator Item Realism Contract v1

Status: LOCKED CREATION INVARIANT

## Purpose

Creator Studio Item generation must not treat schema validity as physical plausibility. For the default Creation Sandbox, generated physical facts must remain compatible with ordinary real-world physics unless a target universe explicitly declares different physical laws.

This rule applies equally to Single Item and Item Batch creation.

## Shared AI rule

The Single Item and Item Batch AI paths use one shared realism instruction. Unless overridden by an explicit target-universe physics contract, the AI must:

- obey ordinary real-world physics, geometry and scale;
- keep dimensions, mass, capacity, nutrition and other numeric facts mutually consistent;
- treat Item dimensions as external bounding dimensions;
- never claim internal container capacity larger than the external bounding volume;
- avoid false precision;
- use `null` for nullable unknown numeric facts rather than inventing unsupported measurements;
- preserve Creator-supplied facts unless they violate an explicit deterministic contract.

A reroll is not a substitute for this invariant.

## Deterministic plausibility gate

AI instruction alone is insufficient where an objective contradiction can be calculated. The default Creation Sandbox therefore performs deterministic cross-field plausibility checks after exact item-v1 validation and before draft acceptance/approval.

v1 objective check:

`container.capacity_volume <= physical.length * physical.width * physical.height`

when all three external dimensions and container capacity are known.

If one or more required dimensions are unknown, the gate does not infer them and does not fabricate a result.

The check is unit-normalized through the existing physical-quantity system.

## Scope and authority

This is a Creation Sandbox policy layer, not a rewrite of the universal Item schema and not a general realism oracle.

- exact item-v1 validation remains authoritative for schema/ontology correctness;
- the realism gate adds only objective cross-field impossibility checks;
- no missing facts are inferred or repaired;
- no canonical Real World mutation is authorized;
- batch atomicity and graph validation remain unchanged;
- future alternate universes may supply a different physics contract rather than weakening this default rule globally.

## Acceptance

A 40 L container with external dimensions 50 cm × 30 cm × 20 cm must be rejected because the outer bounding volume is only 30 L.

A 25 L container with the same external dimensions may pass this objective check.

Single Item and Item Batch AI must use the same shared realism instruction and the same deterministic plausibility policy.
