# Represented Consequence State Foundation v1

Status: IMPLEMENTED FOUNDATION

## Purpose

Provide the smallest deterministic bridge from a validated represented-task action outcome to an explicitly authorized state consequence:

`validated represented task -> deterministic consequence authorization -> bounded simulated-state mutation -> causal event evidence`

This is infrastructure, not a Combat Engine, Injury Engine, Weapons system, or Field Medicine implementation.

## Authority boundary

A consequence is never authorized by Skill score, IQ, supporting Attributes, performance quality, model prose, or a generic capability.

The deterministic caller must supply a `ConsequenceAuthorization` bound to:
- one consequence id;
- the exact represented task id already persisted on the completed source action;
- one subject id;
- an explicit subject role: `actor`, `target`, or `participant`;
- an explicit finite list of field operations.

The source action must already be `completed` and have its `action_completed` event. The subject must actually occupy the declared relationship to that action.

## State boundary

V1 mutates only pre-existing rows in the generic `fields` table whose mode is exactly `simulated`.

It cannot create or rewrite canonical/static/derived profile truth. It does not create new state fields implicitly.

Supported operations reuse the established immediate-effect vocabulary:
- `add`
- `multiply`
- `set`
- `clamp_min`
- `clamp_max`

Numeric operations fail closed on non-numeric current values or operands. `set` may write an explicitly authorized JSON value.

Existing field mode, authority and source metadata are preserved; consequence provenance belongs to the linked event rather than silently taking ownership of the domain field.

## Evidence / causality

A successful consequence emits `represented_consequence_applied` with:
- the source `action_id`;
- the source action location;
- `caused_by_event_id` pointing to the `action_completed` event;
- actor and consequence-subject participants;
- structured before/after state-change data;
- consequence/task/subject authorization provenance;
- `learning_evidence: false`.

Application/consequence evidence is not learning evidence and awards no Skill XP.

## Transaction and retry behavior

Application uses a SQLite savepoint. Any validation, operation or event failure rolls back all field writes from that consequence attempt.

The operation is idempotent for the tuple:

`action_id + consequence_id + represented_task_id + subject_id`

A retry returns the existing consequence event instead of applying additive/multiplicative state changes twice.

## Deliberately deferred

V1 does not implement:
- automatic consequence selection from performance scores;
- injury, bleeding, pain, restraint, incapacity or recovery semantics;
- hostile/non-consensual combat authorization;
- Weapons lethality/resource consumption;
- Field Medicine treatment mutation;
- automatic active-modifier creation or a universal modifier evaluator;
- new schema tables or schema-version changes;
- a production consequence-producing action solely for proof.

Concrete future domain consumers must define their own explicit consequence authorization semantics and can reuse this foundation only after their own task/resource/participant/safety contracts are validated.
