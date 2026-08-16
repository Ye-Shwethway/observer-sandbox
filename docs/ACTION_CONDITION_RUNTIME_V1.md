# Action Condition Runtime Foundation v1

Status: IMPLEMENTATION CANDIDATE

## Why this slice exists

The canonical composable runtime contract includes `Conditions/Modifiers`. Modifiers now have both domain-specific contracts and the generic Active Modifier Runtime Foundation v1. Action-definition conditions, however, remained a persistence socket: `action_definitions.conditions_json` was returned by `action_definition()` but generic legal-option shaping and deterministic validation did not evaluate it.

The existing systemic-fatigue training guard exposed the gap cleanly because it was meaningful runtime behavior implemented as a hard-coded `train` branch rather than as an authored action-definition prerequisite.

This slice activates the existing condition socket without building an arbitrary expression language.

## V1 condition contract

An action definition may carry either an empty condition object or exactly:

```json
{
  "all": [
    {"field_key": "physiology.fatigue", "operator": "lt", "value": 70.0}
  ]
}
```

Every clause in `all` must pass.

Supported primitive comparators:
- `lt`
- `lte`
- `gt`
- `gte`
- `eq`
- `ne`

Malformed shapes, unknown fields and unsupported operators fail closed.

V1 deliberately does not implement `any`, nested boolean trees, scripts, formulas, cross-entity queries or arbitrary database predicates.

## Authoritative runtime values

The action-condition evaluator itself is pure and receives explicit values from the runtime consumer.

The first consumer exposes only established actor runtime context:
- `runtime.location`;
- `needs.energy`;
- `needs.hunger`;
- `needs.thirst`;
- `needs.sleepiness`;
- `physiology.cleanliness`;
- `physiology.fatigue`.

Living-state values come from the same effective `snapshot()` already used by cognition and validation. Therefore an active temporary modifier can legitimately change whether an action-definition condition is satisfied without changing the raw authoritative base field.

## First canonical exemplar — training fatigue prerequisite

The existing training rule remains exactly the same boundary:

`physiology.fatigue < 70`

The authority moves from a hard-coded `if action.name == "train"` branch into the canonical `train` action definition.

Both:
- `action_options()` availability; and
- `validate_action()` deterministic legality

consume the same generic condition evaluator.

This removes duplicate special-case authorization logic while preserving existing behavior.

`TRAINING_FATIGUE_LIMIT` is shared from the canonical action-definition module so the definition and legacy baseline policy cannot silently drift to different copies of the runtime legality boundary.

## Seed / compatibility behavior

`seed_action_definitions()` now synchronizes canonical `conditions_json` on existing databases as well as fresh databases. Schema remains v5.

No action-instance condition evidence is reinterpreted: `Action.conditions` / `action_instances.conditions_json` remain per-instance represented metadata. This slice concerns **definition prerequisites**, not proposal-authored conditions.

## Conditions + Modifiers composition

The focused bridge exemplar is:
- raw fatigue = 20;
- active temporary modifier = +55;
- effective snapshot fatigue = 75;
- canonical train prerequisite `fatigue < 70` fails;
- training disappears from legal options and direct validation rejects it;
- after modifier expiry, effective fatigue returns to the raw base and the action becomes legal again.

Neither subsystem overwrites the other's authority.

## Safety boundaries

- LLM cognition cannot author or bypass action-definition prerequisites.
- Proposal `Action.conditions` does not grant permission.
- Conditions do not create actions, targets, resources or effects.
- Ordinary target/capability/co-location/domain validation still applies after definition prerequisites pass.
- Existing specialized validators remain legal where a generic primitive condition cannot express the domain invariant.
- No schema change.

## Focused acceptance

Regression coverage proves:
- empty definitions remain legal;
- all clauses are conjunctive;
- malformed/unknown/unsupported contracts fail closed;
- fresh DB train definition owns the canonical fatigue prerequisite;
- below-boundary training remains available and valid;
- boundary fatigue hides training and direct validation rejects it;
- active modifiers compose through effective snapshot state;
- expiry restores ordinary legality;
- re-initialize restores canonical definition conditions on an existing schema-v5 DB.

## Non-goals

V1 does not add a universal policy language, condition authoring UI, environmental/weather engine, cross-actor relationship predicates, inventory expressions, scripted conditions, new action vocabulary, or new character-specific branches.

The slice is complete when focused regression, the normal one-time final PR CI, task-relevant automatic gates, deploy and production readback prove the generic condition seam without disturbing current runtime state.
