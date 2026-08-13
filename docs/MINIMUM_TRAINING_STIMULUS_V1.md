# Minimum Training Stimulus v1

Status: candidate

## Scope

This slice adds session-only training stimulus evidence for one target/domain pair:

- action: `train`
- target: `obj_thorne_estate_gym_free_weights`
- domain: `strength`

It consumes the existing P3.5 effective training load and derives:

`stimulus_units = effective_minutes / 60`

A 60-effective-minute Free Weights session therefore records `1.0` session strength stimulus unit.

## Invariants

- stimulus is evidence, not progression state;
- raw `raps_pa.strength` is not mutated;
- derived grade is not mutated;
- no accumulated stimulus store;
- no adaptation/recovery conversion;
- no hypertrophy/body measurement change;
- no stimulus for Heavy Bag, Combat Mat, Practice Dummy, or other targets in v1;
- no schema v5.

The evidence is persisted in both `action_instances.outcome_json.training_stimulus` and the matching `action_completed` event payload.
