# Hobby / Interest Lifecycle v1

Status: runtime slice

## Purpose

Give Observer Sandbox a minimum deterministic lifecycle for interests that may grow into hobbies without treating every repeated action as a hobby or allowing the LLM to rewrite disposition state directly.

This slice follows `docs/ADAPTIVE_CHARACTER_DISPOSITION_FOUNDATION.md` and reuses the completed-action boundary proven by Habit Formation/Extinction v1.

## Authority

`completed represented voluntary engagement -> deterministic interest evidence -> persisted interest state -> established hobby projection -> cognition context`

The LLM may see the resulting preference/hobby context. It does not directly create, promote, decay, or delete an interest/hobby.

## Persistence model

The existing profile tables are sufficient; schema v5 is unchanged.

- `character_preferences(preference_type='interest')` is the lifecycle authority for learned interests.
- `character_hobbies` is the active projection for a learned interest only after it reaches `established`.
- canonical authored hobbies remain independent baseline rows and are never rewritten by this lifecycle.
- when a learned hobby becomes dormant/lapsed, the active hobby projection is removed while the authoritative interest row and its accumulated lifecycle metadata remain.

This makes `character_hobbies` an active established-hobby surface rather than a dumping ground for one-off curiosity.

## Eligible evidence v1

Only completed target-based voluntary engagements currently count:

- `read`
- `use`

The following do not create interests in v1:

- movement;
- physiological need resolution such as eat/drink/sleep/rest/shower;
- idle;
- inspect-only curiosity;
- training/Skill practice;
- self-satisfaction.

This is deliberately conservative. Future represented leisure/creative activities may opt into the same contract rather than broadening eligibility by inference.

## Lifecycle

A new eligible engagement creates an `emerging` interest candidate, not a hobby.

Repeated engagement can advance through:

`emerging -> recurring -> established`

Promotion uses bounded interest strength plus effective engagements and distinct engagement days. Multiple repetitions in a short interval receive reduced temporal weight, so same-day repetition cannot cheaply manufacture an established hobby.

The current constants are tuning policy, not claims about universal human psychology.

## Decay

Learned dynamic interests receive a grace period before gradual decay.

An established interest whose strength falls sufficiently after non-engagement becomes `dormant`, removing its active hobby projection while preserving the lifecycle authority/history. Very weak long-inactive interests may become `lapsed`.

Re-engagement may strengthen the same persisted interest again; it does not create a duplicate history.

## Cognition influence

Before establishment, the learned candidate reaches cognition through the existing `preferences` context as `type: interest`.

After establishment, the same subject additionally appears in the existing `hobbies` context through its active hobby projection.

Dormancy/lapse removes that learned active hobby projection. The interest authority remains persisted for future re-engagement and later richer cognition treatment.

## Explicit non-goals

v1 does not add:

- a universal leisure engine;
- automatic hobbies from Skills/training;
- proficiency progression for hobbies;
- identity transformation from hobbies;
- social/group hobby mechanics;
- arbitrary model-authored interests;
- reward-maximizing hobby loops;
- a new schema/table solely for this slice.

## Verification target

Focused regression should prove:

1. one eligible engagement creates only an emerging interest;
2. repeated cross-day engagement reaches recurring then established;
3. same-day engagement has diminished weight;
4. excluded actions cannot create interests;
5. long inactivity can make an established learned hobby dormant without deleting interest history;
6. learned authority/projection survive reinitialization while canonical hobbies remain intact.
