# Tactical Planning Skill Progression v1

Status: IMPLEMENTED CANDIDATE / VALIDATION PENDING

## Purpose

Apply the proven Skill Progression Foundation pattern to the next represented learned skill whose current runtime already has explicit structured practice evidence: **Tactical Planning**.

This is a follow-on-by-pattern slice. It does not add a new progression architecture.

## Authority

The Skill Progression Foundation authority contract remains unchanged:

- `character_skills.score` is current demonstrated proficiency;
- `character_skills.experience` is accumulated legitimate post-activation learning/practice evidence;
- persisted `tier` remains legacy/compatibility only;
- grade remains a read-time derivation through `skill-proficiency-100-v1`;
- model prose, action reason text and Telegram are never progression authority.

The historical RAPS skill-like snapshots remain non-authoritative compatibility data and are not independently mutated by this slice.

## Evidence mapping

Tactical Planning consumes only completed Training Method evidence whose canonical method semantics explicitly include tactical work.

Eligible methods:

- `vr_tactical_drills` — relevance `1.00`; canonical workload channel is `tactical`, with scenario/decision tags;
- `ai_combat_simulation` — relevance `0.80`; canonical workload channels are `combat` + `tactical`, so it supplies meaningful cross-training but is not treated as purely tactical practice.

Combat methods that do not declare tactical semantics, such as `combat_mat_drills`, do not improve Tactical Planning merely because they are combat activities.

The `0.80` cross-training weight is bounded gameplay semantics reflecting a mixed-purpose method, not a scientific learning coefficient.

## Progression calculation

Tactical Planning reuses the already-deployed generic Skill Progression calculation unchanged:

`effective training minutes / 60 * method relevance -> raw learning units`

then:

- 24-sim-hour recent-practice saturation;
- current-proficiency diminishing returns;
- bounded score gain;
- cumulative effective learning units as experience;
- hard score cap `100`;
- immutable `skill_progression_settled` evidence;
- consumed action-event idempotency.

No new formula or Tactical-specific engine exists.

## Activation safety

At initialization/deployment, Tactical Planning receives the same zero-gain activation bootstrap as the Hand-to-Hand exemplar:

- represented score is preserved;
- represented existing experience is preserved;
- already-existing eligible historical action evidence is cursor-consumed;
- no historical XP or score is invented;
- only genuinely future eligible practice can create adaptation after activation.

Ordinary re-initialization must preserve earned score/experience.

## Observability

A legitimate Tactical Planning score change automatically reuses Character Change Observability & Notification Foundation v1:

- Profile delta arrows;
- `0.10` cumulative Skill significance;
- immediate grade-transition significance;
- generic Skills grading;
- per-character stat-notification controls;
- aggregated/debounced Character Progression messages.

No Tactical-specific Telegram implementation is added.

## Why other represented skills are not included here

The current runtime does not yet provide sufficiently specific structured evidence for the other represented skills:

- **Weapons** — Armory currently exposes inspect/use affordances, not weapon-practice semantics;
- **Survival** — obstacle training currently carries conditioning/movement semantics, not fieldcraft/survival evidence;
- **Technology** — workstation/terminal use and generic Research Desk activity do not encode a technical topic/work product;
- **Field Medicine** — Diagnostic Station use does not yet encode medical practice/treatment evidence.

The existing generic `research` action also has no topic/domain semantics and explicitly did not create skill progression when introduced. These skills remain deferred until a real structured evidence family exists; action names or model reason prose must not be guessed into XP.

## Acceptance

Focused tests and a disposable production-copy validator must prove:

- zero-gain Tactical activation preserves current score/experience;
- non-tactical combat practice does not progress Tactical Planning;
- future VR Tactical practice progresses score and experience;
- the same action cannot be credited twice;
- re-initialization preserves earned state;
- production itself is not moved, trained, accelerated or otherwise mutated for validation.

## Deferred

- Weapons progression;
- Survival progression;
- Technology progression;
- Field Medicine progression;
- skill retention/decay/reacquisition;
- broad research-topic/knowledge systems;
- careers/jobs/quests;
- broad Mind/Behavior architecture.
