# Universal Profile Grading Framework v1

Status: PLANNED / NOT YET IMPLEMENTED

## Purpose

Complete grading as a reusable profile-wide interpretation layer before Skill Progression begins.

The authoritative state remains the underlying profile/skill/body value. Grades are derived at read time and are never independently persisted truth.

Core invariant:

`authoritative current value(s) + explicit named grading scheme + scheme-specific context -> derived grade metadata -> profile/query consumers -> Telegram / future unlock systems`

Future career, quest, job, salary and progression systems may consume grade results, but must not make Telegram presentation the authority.

## Shared vocabulary

Retain the canonical cross-domain vocabulary:

- E — Beginner
- D — Novice
- C — Capable
- B — Skilled
- A — Advanced
- S — Expert
- SS — Elite
- SSS — Master
- X — Mythic
- XX — Transcendent

A grading scheme may legitimately expose only a subset. The current 0..100 RAPS scheme remains E..S only; SS..XX must not be artificially squeezed into that scale.

## Scheme registry

The grading layer should support explicit named schemes rather than one universal numeric formula.

Initial scheme families:

- `monotonic`: higher or lower value has a meaningful ordered interpretation;
- `target_range`: a bounded desirable/reference interval is meaningful and excessive deviation in either direction can reduce grade;
- `target_proximity`: grade follows distance from an evidence-backed or explicitly authored target ratio/reference;
- `composite`: multiple compatible derived metrics combine into a higher-level grade;
- `reference_distribution`: future percentile/reference grading where a valid population/reference distribution exists.

A numeric field does **not** automatically become gradeable. Membership in a scheme is explicit.

## Attributes

Preserve the proven `raps-100-proof-v1` behavior for explicitly opted-in 0..100 attributes.

- individual values are graded at read time;
- compatible group/overall aggregates are read-time only;
- IQ remains excluded from the RAPS scheme because its scale semantics differ;
- progression engines and grading remain separate authorities.

## Skills

Skills are a natural monotonic proficiency domain once their score semantics are confirmed.

Planned presentation example:

`Hand-to-Hand Combat   90 (S) · Expert`

`character_skills.score` should become the grading input for learned-skill proficiency. Existing persisted `tier` data must not become an independently mutable grade authority; the Skill Progression family will reconcile score/experience/tier ownership before progression is implemented.

Skill grades are intended to be reusable later by career, quest, job and compensation requirements.

## Body and physique grading

Body measurements must **not** inherit a simple `larger = better` rule.

Absolute height, weight and circumferences are descriptive state. Many physique judgments depend on proportional relationships, composition and context rather than raw magnitude.

Planned body grading therefore emphasizes derived metrics such as:

- shoulder-to-waist relationship;
- chest-to-waist relationship;
- waist-to-height relationship where a health/reference interpretation is intended;
- waist-to-hip relationship where appropriate;
- upper/lower-body balance;
- limb proportionality and bilateral/symmetry-compatible relationships when represented;
- body-composition/conditioning context;
- composite physique proportionality.

Exact target bands must be evidence-backed and configurable. Do not hard-code a single popularized “golden ratio” as universal biological truth.

### Context-specific interpretation

The same raw body can support multiple later named interpretations, for example:

- general physique proportionality;
- health-oriented composition/central-adiposity interpretation;
- bodybuilding/classic-physique suitability;
- modelling/presentation suitability.

These are different schemes, not competing mutations of body state.

Future career systems should combine the appropriate contextual grades rather than treating a single circumference as a universal quality score.

## Grading eligibility audit

Before closure, current profile surfaces should be classified as one of:

- `graded`;
- `derived-grade candidate`;
- `contextual-only`;
- `not gradeable`.

Expected current direction:

- Attributes — graded under explicit compatible schemes;
- Skills — graded once proficiency-score semantics are locked;
- Body — partially/compositely graded through derived/contextual schemes;
- Appearance anchors such as PARS — separate future decision, not silently inherited;
- IQ — separate future scale/reference scheme;
- Recovery — status/condition, not a quality grade by default;
- Personality — not gradeable by default;
- Preferences/Habits — not gradeable by default;
- sexual anatomy/current sexual counts — not gradeable merely because they are numeric.

## Telegram and query architecture

The profile query layer should attach derived grade metadata. Telegram consumes that metadata generically.

Do not create field-specific Telegram grade logic when the grading registry can provide the result.

Raw value, grade, label and any derived metric context should remain distinguishable.

## Implementation order

1. grading registry + scheme contract;
2. preserve/route existing Attribute grading through the registry;
3. add Skill grading presentation without implementing Skill Progression yet;
4. research and implement Body/Physique derived grading with explicit contextual schemes;
5. run a profile-wide grading coverage audit and close relevant presentation gaps;
6. only then begin Skill Progression Foundation v1.

## Boundaries

This planning slice does not implement runtime/code/schema changes.

The later grading implementation must not:

- persist grades as competing authoritative state;
- assume every numeric field deserves a grade;
- treat raw body size as linear quality;
- conflate health, aesthetics, bodybuilding and modelling criteria;
- invent unsupported universal body-proportion constants;
- mutate Skill scores while only adding presentation;
- introduce careers, quests, jobs, salary or economy as side effects.
