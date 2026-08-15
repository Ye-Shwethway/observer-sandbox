# Cognitive / Performance Modifier Contract v1

Status: implementation candidate

## Purpose

Skill proficiency answers what learned capability the actor has. Cognitive and supporting Attributes can influence how well a supported task is performed, but they must not silently become a second Skill score or a universal bonus.

This contract defines the first bounded, deterministic performance-modifier layer for represented Skill applications.

## Authority order

For a represented Skill task:

1. the Skill Definition and represented task contract define scope, challenge, context, resources, and allowed outcomes;
2. authoritative `character_skills.score` plus the Skill-specific proficiency anchor determine learned capability feasibility;
3. only after feasibility is established may a Cognitive / Performance Modifier contract shape explicitly allowed outcome dimensions;
4. the represented-task outcome resolver remains final deterministic outcome authority.

The modifier contract never upgrades `unsupported` capability to `supported` and never creates a new action variant.

## First exemplar

Contract:

`technology.diagnose_known_system_fault`

Dimensions:

- `reasoning_quality`
- `precision`
- `adaptation`

The first low-risk diagnostic simulation intentionally does not use stress modifiers. Pressure-sensitive factors should be introduced only when a represented task actually authors meaningful pressure.

## Input normalization

### 0..100 Attributes

`raps_100_centered_v1` uses a simulation-specific centered linear transform:

`normalized = clamp((value - 50) / 50, -1, 1)`

### IQ reasoning context

`iq_reasoning_context_v1` uses:

`normalized = clamp((IQ - 100) / 30, -1, 1)`

This is an Observer Sandbox gameplay normalization, not a claim that real-world performance is linearly determined by IQ.

IQ is general reasoning context. It is not Knowledge and is not learned Skill proficiency.

## Dimension resolution

Each dimension declares:

- a neutral base multiplier of `1.0`;
- an explicit maximum absolute effect, never greater than 15% in v1;
- allowed outcome effects that must already be declared by the Skill application;
- explicit factor field keys, normalization profiles, and positive weights;
- total factor weight no greater than `1.0`.

For each factor:

`weighted contribution = normalized factor × declared weight`

Then:

`effect = clamp(sum(weighted contributions) × max_abs_effect, -max_abs_effect, +max_abs_effect)`

`multiplier = 1 + effect`

Missing factor values contribute neutral zero. Weights are never renormalized around missing data.

## IQ boundary

High IQ may improve a dimension only where an explicit contract names `raps_ia.iq`. It must never:

- change the actor's Skill score or grade;
- create missing technical/medical/etc. Knowledge;
- authorize unsupported challenge classes;
- satisfy missing target/context/resource requirements;
- create access to actions;
- become a global modifier to unrelated tasks.

## Skill boundary

Learned Skill remains primary authority. A cognitively exceptional actor without the relevant Skill cannot pass capability resolution merely because a performance modifier would be favorable.

Conversely, a highly trained actor with weaker supporting factors may still possess the Skill while producing a lower bounded quality/precision/adaptation outcome inside a supported task.

## Knowledge boundary

No actor Knowledge subsystem exists yet. The modifier layer therefore does not read, infer, score, or fabricate Knowledge.

## Read-only boundary

Both the pure modifier resolver and actor-backed adapter are read-only. They emit no events/evidence, mutate no profile values, and change no Skill score/experience.

## Next consumer

The intended first consumer is **Technology Represented Diagnostic Task Runtime v1**. That runtime should:

1. validate the concrete represented task instance;
2. establish actor Skill capability feasibility;
3. resolve cognitive/performance modifiers;
4. deterministically produce bounded task outcome dimensions;
5. emit immutable application evidence only after an actual completed action;
6. keep learning evidence separate unless an explicit learning contract later authorizes it.
