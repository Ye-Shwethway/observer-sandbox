# Skill Evidence Semantics v1

Status: IMPLEMENTED CANDIDATE / VALIDATION PENDING

## Purpose

Create one reusable evidence contract for learned skills whose legitimate practice cannot be represented by existing Training Method semantics.

First bounded exemplar: **Technology — Systems Diagnostic Practice**.

This layer answers only: **what completed activity is legitimate learning evidence for which skill?** It does not own proficiency, XP, grading or notifications.

## Core invariant

`validated domain-specific practice target + explicit practice method + bounded duration/context -> immutable structured skill-practice evidence -> existing generic Skill Progression settlement`

## Authority separation

Skill Evidence Semantics owns:
- practice-method definitions;
- practice-target bindings;
- validation that a completed action is a registered practice activity;
- immutable `skill_practice` evidence attached to `action_completed`.

Skill Progression remains authoritative for:
- `character_skills.score`;
- `character_skills.experience`;
- zero-gain activation/bootstrap;
- recent-practice saturation;
- proficiency diminishing returns;
- score cap and idempotency;
- immutable progression settlements.

Grading remains read-time derived. Change observability/Telegram remain generic consumers.

## Explicit `practice` action

v1 adds a generic `practice` action definition:
- target mode: object;
- required capability: `practice`;
- colocation required;
- duration bounded by the registered practice-method family.

Only purpose-built objects explicitly seeded from the practice registry advertise `practice`. Ordinary objects with `use`, `inspect`, `research`, `monitor`, `train` or other capabilities are not reinterpreted as learning targets.

This is deliberate: ordinary computer use must not silently improve Technology, ordinary medical-station use must not silently improve Field Medicine, and generic research must not become universal XP.

## Technology exemplar

Method:
- `systems_diagnostic_practice`;
- minimum duration: 10 sim minutes;
- Technology relevance: `1.0`;
- tags: technical, diagnostic, simulation-safe.

Purpose-built target:
- `Systems Diagnostic Practice Console`;
- located in the authored Communications room;
- capabilities: `inspect`, `practice`;
- definition identity references the generic practice method, not an actor.

The console represents a safe diagnostic/troubleshooting simulation fixture, not a production terminal side effect. The ordinary Secure Communications Terminal remains an ordinary `use` target and does not emit Skill Evidence.

## Evidence payload

A completed registered practice action emits `action_completed.skill_practice` with:
- source/revision;
- method id/name;
- target id;
- planned/effective minutes;
- bounded quality placeholder (`1.0` in this minimal exemplar);
- explicit positive `skill_relevance` mapping;
- semantic tags.

Skill Progression consumes practice evidence only when both conditions hold:
1. the evidence positively names the skill in `skill_relevance`;
2. that method is explicitly whitelisted for the skill in `skill_progression.v1.json`.

This dual gate prevents arbitrary payloads from granting XP.

## Technology progression

Technology is added to the existing Skill Progression config with `systems_diagnostic_practice = 1.0`.

All existing progression behavior is reused unchanged:
- raw units from effective duration × configured method weight;
- 24-sim-hour saturation;
- proficiency diminishing returns;
- score cap 100;
- cumulative experience;
- consumed action-event idempotency;
- reseed persistence;
- Profile/grade/change-notification inheritance.

No Technology-specific XP formula or Telegram subsystem exists.

## Activation safety

Deployment/initialize performs a zero-gain Technology bootstrap:
- represented Technology score/experience are preserved;
- any pre-existing eligible evidence is cursor-consumed without retroactive gain;
- only genuinely future registered practice may progress the skill.

Because the `practice` action and purpose-built console are new in this slice, production cannot contain historical legitimate practice actions from before activation.

## Acceptance requirements

Focused tests and disposable production-copy validation must prove:
- practice action + purpose-built target are seeded generically;
- only the explicit practice console surfaces `practice` in its room;
- ordinary Secure Communications Terminal use emits no `skill_practice` evidence and no Technology progression;
- future valid diagnostic practice emits typed evidence and progresses Technology;
- sub-minimum practice is rejected;
- the same evidence cannot be double-counted;
- reinitialize preserves earned state;
- production itself is not moved, practiced, accelerated or otherwise manipulated for validation.

## Deferred

Not in this exemplar:
- Weapons practice evidence;
- Survival/fieldcraft evidence;
- Field Medicine treatment/practice evidence;
- topic-aware general research/knowledge acquisition;
- variable practice quality/challenge scoring;
- Skill Retention/Decay/Reacquisition;
- careers/jobs/quests;
- broad Mind/Behavior architecture.

After this invariant is proven, structurally equivalent safe practice targets/methods should be batched by pattern instead of creating one new architecture per skill.
