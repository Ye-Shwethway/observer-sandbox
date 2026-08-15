# Skill Evidence Semantics v1

Status: COMPLETE / DEPLOYED / LIVE-ACTIVATED

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

## Evidence payload / dual gate

A completed registered practice action emits `action_completed.skill_practice` with source/revision, method identity, target identity, planned/effective minutes, bounded quality, positive `skill_relevance`, and semantic tags.

Skill Progression consumes practice evidence only when:
1. the evidence positively names the skill in `skill_relevance`; and
2. the method is explicitly whitelisted for that skill in `skill_progression.v1.json`.

This dual gate prevents arbitrary payloads or generic object actions from granting XP.

## Technology progression

Technology is enabled only from `systems_diagnostic_practice = 1.0`.

All existing Skill Progression behavior is reused unchanged:
- effective duration × configured method weight;
- 24-sim-hour saturation;
- proficiency diminishing returns;
- score cap 100;
- cumulative experience;
- consumed-action-event idempotency;
- reseed persistence;
- Profile/grade/change-notification inheritance.

No Technology-specific XP formula or Telegram subsystem exists.

## Activation safety

Deployment/initialize performs a zero-gain Technology bootstrap:
- represented Technology score/experience are preserved;
- pre-existing eligible evidence is cursor-consumed without retroactive gain;
- only genuinely future registered practice may progress the skill.

Because the `practice` action and purpose-built console were introduced with this slice, production had no historical legitimate practice actions to reinterpret.

## Acceptance / deployment evidence

PR #108 final tested head: `66354c2f5f783a231321dcf8f67b950a5554f231`.

PR validation:
- CI #797 / run `31870663425`: SUCCESS;
- Skill Evidence Semantics v1 Acceptance #1 / run `31870663517`: SUCCESS on disposable production copy;
- Hand-to-Hand Skill Progression Foundation Acceptance #6 / run `31870663472`: SUCCESS;
- Tactical Planning Acceptance #3 / run `31870663487`: SUCCESS;
- Public Readiness Security Audit #62 / run `31870663365`: SUCCESS;
- Inventory Foundation #36, Eating Behavior #26, Nutrition & Energy Evidence #16: SUCCESS;
- Strength Live Cycle #35 / run `31870663376`: SUCCESS on retry after an infra-only SSH staging reset before validator execution.

Merged as `3cd35cb1480533c0c2258ee72d2726cfe24b586b`.

Deployment:
- Deploy #198 / run `31870737488`: SUCCESS;
- post-merge CI #798 / run `31870737278`: SUCCESS;
- post-merge Skill Evidence Semantics Acceptance #2 / run `31870737515`: SUCCESS;
- post-merge Tactical Planning Acceptance #4 / run `31870737546`: SUCCESS.

Deploy readback verified service healthy, schema v5, autonomy normal at 1.0x, cognition bindings preserved, Telegram connected, and live **Technology remained `82.0 / A Advanced`** after activation. This proves deployment caused no retroactive Technology score jump. Production was not moved, practiced, accelerated or otherwise manipulated to manufacture an occurrence.

## Proven extension policy

The new structural evidence invariant is now proven. Structurally equivalent simulation-safe practice targets/methods should be added by batch-by-pattern rather than one new architecture or PR per skill.

Good candidates are skills that can use the exact same explicit `practice` action + purpose-built simulation/training target + typed skill relevance contract. Skills requiring qualitatively different real-world evidence should remain deferred until their evidence family exists.

## Deferred / next coverage

Not yet enabled:
- Weapons practice evidence;
- Survival/fieldcraft evidence;
- Field Medicine practice evidence;
- topic-aware general research/knowledge acquisition;
- variable practice quality/challenge scoring;
- Skill Retention/Decay/Reacquisition.

The next minimum-runnable follow-on should batch only structurally equivalent safe practice mappings. Weapons remains optional/deferred if a clean abstract simulation target would add unnecessary scope or operational semantics.
