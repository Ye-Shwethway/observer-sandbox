# Training Anatomy / Movement Semantics v1

Status: ACTIVE CANDIDATE

## Purpose

Training Method Semantics v2 answers **what kind of training method** a concrete target represents. Training Anatomy v1 adds the smaller layer underneath it: **what movement patterns were actually performed inside a resistance-training action**.

Universal chain:

`Actor + train action + concrete target -> reusable method -> selected reusable movement pattern(s) -> effective load -> movement anatomy evidence -> BC-3 regional exposure`

Movement definitions are actor-independent and world-independent. Darian and Thorne Estate equipment remain production exemplars only.

## Reusable movement catalog

Canonical movement definitions live in `config/training_movements.v1.json`.

Initial bounded catalog:
- squat;
- hinge;
- horizontal press;
- vertical press;
- row / horizontal pull;
- curl / elbow flexion;
- extension / elbow extension;
- calf raise / plantar flexion;
- Olympic pull.

Each movement owns only:
- stable movement id;
- human-readable name;
- semantic tags;
- normalized regional-loading weights for BC-3 measurement regions.

Movement definitions do **not** own hypertrophy formulas, progression magnitude, genetics, recovery, actor state, or circumference mutation.

## Method compatibility

Resistance method definitions list which movement ids they can support. For example:

`free_weight_strength -> squat | hinge | horizontal_press | vertical_press | row | curl | extension | calf_raise`

A future non-Thorne dumbbell area may bind to `free_weight_strength` and automatically expose the same movement vocabulary. No Darian/object-specific branch is required.

## Cognition contract

The structured cognition decision now includes `training_movements`.

- For a resistance train option with `movement_options`, cognition may select one to four exact movement ids from that option.
- For non-train actions, the array must be empty.
- For training methods without authored movement options, the array is empty.
- Server-side validation rejects movement ids that are not allowed by the selected target's reusable method.
- Selected ids persist in the existing `action_instances.conditions_json`; no database migration is required.

Legacy mocked decisions that predate this field normalize to an empty array for test compatibility.

## Event evidence

Completed training events retain the existing `training_method` evidence. When explicit movement ids are present, the method evidence additionally contains:

`movement_anatomy = { movement_ids, regional_load, source }`

`regional_load` is the equal-share aggregate of the selected movement definitions, clamped to `[0, 1]` per region.

Example distinction:
- `curl` gives direct biceps/forearm emphasis and zero thigh loading;
- `squat` gives direct thigh/hip/calf emphasis and zero biceps loading.

This removes the old ambiguity where both sessions could be represented only as broad `free_weight_strength`.

## BC-3 compatibility

BC-3 regional exposure follows a compatibility rule:

1. if a qualifying resistance event contains valid `movement_anatomy.regional_load`, use it;
2. otherwise use the existing `method_region_weights` fallback.

Therefore historical/pre-v1 events remain valid and no production history migration is required. New movement-aware sessions gain exercise-pattern specificity immediately.

BC-2 remains method/channel based and unchanged. Movement anatomy does not create a second body-composition authority.

## Safety / scope boundaries

This slice intentionally does not model:
- individual exercise names beyond movement-pattern semantics;
- sets, reps, RPE/RIR, tempo, ROM or unilateral loading;
- muscle-by-muscle anatomical simulation;
- injury biomechanics;
- exercise-specific calorie models;
- new database tables;
- extra model calls.

Those would be separate refinements only if later evidence shows they are worth the complexity.

## Acceptance

Training Anatomy v1 passes when:
- movement definitions contain no actor or concrete world-object identity;
- resistance methods expose only authored allowed movements;
- invalid target/movement combinations fail closed;
- selected movement ids persist through existing action conditions;
- completed events emit deterministic movement anatomy;
- curl-vs-squat regression proves region-specific distinction;
- BC-3 prefers movement anatomy for new events and preserves method-level fallback for historical events;
- existing Strength/Stamina/BC-2 behavior remains compatible;
- no schema migration or extra model call is introduced.
