# Cognitive / Performance Modifier Contract v1

Status: **COMPLETE / DEPLOYED**
Date: 2026-08-15
Implementation: PR #125
Merge: `44774ec7829eb955551fedd8594697b72035e2cf`
Deployment: Deploy #207 / run `31875826283` SUCCESS

## Purpose

Skill proficiency answers what learned capability the actor has. Cognitive and supporting Attributes may influence how well a supported task is performed, but they must not silently become a second Skill score or universal bonus.

This contract defines a bounded deterministic performance-modifier layer for represented Skill applications.

## Authority order

1. Skill Definition + represented task define scope, challenge, context, resources and allowed outcomes.
2. Authoritative `character_skills.score` plus Skill-specific proficiency anchor determine learned capability feasibility.
3. Only after feasibility is established may a declared modifier contract shape explicitly allowed outcome dimensions.
4. The represented-task outcome resolver remains final deterministic outcome authority.

Modifiers never upgrade `unsupported` capability to `supported` and never create a new action variant.

## First exemplar

Contract:
`technology.diagnose_known_system_fault`

Dimensions:
- `reasoning_quality`
- `precision`
- `adaptation`.

The low-risk diagnostic exemplar intentionally omits stress modifiers.

## Input normalization

For 0..100 Attributes, `raps_100_centered_v1` uses:
`normalized = clamp((value - 50) / 50, -1, 1)`

For IQ reasoning context, `iq_reasoning_context_v1` uses:
`normalized = clamp((IQ - 100) / 30, -1, 1)`

These are Observer Sandbox gameplay normalizations, not claims that real-world performance is linearly determined by IQ or these Attributes.

## Dimension resolution

Each dimension declares:
- neutral multiplier `1.0`;
- explicit maximum absolute effect, never above 15% in v1;
- allowed outcome effects already declared by the Skill application;
- explicit factor keys, normalization profiles and positive weights;
- total factor weight no greater than `1.0`.

For each factor:
`weighted contribution = normalized factor × declared weight`

Then:
`effect = clamp(sum(weighted contributions) × max_abs_effect, -max_abs_effect, +max_abs_effect)`

`multiplier = 1 + effect`

Missing factors contribute neutral zero. Weights are not renormalized around missing data.

## IQ boundary

High IQ may improve a dimension only where an explicit contract names `raps_ia.iq`. It must never:
- change Skill score/grade;
- create missing Knowledge;
- authorize unsupported challenge classes;
- satisfy missing target/context/resource requirements;
- create action access;
- become a global modifier to unrelated tasks.

## Skill / Knowledge boundary

Learned Skill remains primary feasibility authority. A cognitively exceptional actor without the relevant learned Skill cannot pass merely because modifiers are favorable.

No first-class actor Knowledge subsystem exists yet, so this layer does not infer or fabricate Knowledge scores.

## Read-only boundary

Pure and actor-backed modifier resolution emit no events/evidence, mutate no profile state, and change no Skill score/experience.

## First consumer completed

Technology Represented Diagnostic Task Runtime v1 consumes this contract through PR #126 / Deploy #208. It proved that IQ/supporting factors can shape bounded deterministic task outcomes without replacing learned Skill authority.

## Next direction

Tactical Planning `assess_tactical_situation` is the next represented gameplay exemplar. It should declare its own relevant factor/dimension contract rather than reusing Technology weights by analogy or turning IQ into a generic planning bonus.
