# Skill Progression Foundation v1

Status: **COMPLETE / DEPLOYED / LIVE-ACTIVATED**

Canonical implementation checkpoint: PR #104, merge `a8c86705700f689024c75fe91e00be9361ae557a`, Deploy #196.

## Purpose

Establish one deterministic, auditable learned-skill progression invariant using **Hand-to-Hand Combat** as the bounded exemplar.

Core invariant:

`completed skill-relevant training evidence + effective duration + method relevance + current proficiency + recent-practice saturation -> effective learning units -> bounded score/experience settlement + immutable audit event`

This is a skill system, not a renamed physical-attribute progression engine.

## Authority

For learned skills:

- `character_skills.score` = authoritative current demonstrated proficiency;
- `character_skills.experience` = accumulated legitimate post-activation learning/practice evidence;
- persisted `tier` = legacy/compatibility data only;
- read-time grade = derived from `skill-proficiency-100-v1`;
- model prose, action reason text and Telegram are never progression authority.

Historical RAPS skill-like fields such as `raps_pa.combat_skill`, `raps_pa.weapons_proficiency` and `raps_pa.survival_skill` are not independent live progression authorities. In this exemplar they remain legacy compatibility snapshots. Exact alias derivation/cleanup is a follow-on concern; Hand-to-Hand progression mutates only `character_skills.hand_to_hand_combat`.

## Seed / deployment safety

Canonical skill seeds are initialization baselines, not periodic resets.

`import_seed()` no longer deletes and recreates all character skill rows. A progression-active skill preserves its current score, experience and progression metadata across ordinary initialize/deploy/status paths. A non-null legacy `experience` value is also treated as learned-state evidence and preserved even if it predates the explicit activation marker. Extra learned skills absent from the canonical seed are preserved.

Skill Progression bootstraps at the normal initialization/deploy boundary. The zero-gain bootstrap consumes already-existing eligible historical action evidence and marks the represented skill progression-active without inventing historical XP or retroactively changing the represented score. Because activation occurs before future autonomous actions, the first genuinely post-deploy eligible combat practice remains eligible.

Bootstrap and later settlement receipts remain immutable audit events. User-facing Recent Activity shows completed character actions rather than internal engine receipts.

## Exemplar: Hand-to-Hand Combat

Configured eligible training methods are reusable method IDs rather than actor-specific target switches:

- `heavy_bag_rounds` — relevance weight `0.75`;
- `combat_mat_drills` — `0.90`;
- `technical_dummy_drills` — `0.85`;
- `ai_combat_simulation` — `1.00`;
- `combat_pit_drills` — `1.00`.

The engine reconstructs method evidence from immutable `action_completed` events through the existing Training Method Semantics layer. Free weights, running, mobility and other non-combat methods do not improve Hand-to-Hand merely because their action type is `train`.

## Learning calculation

Raw learning units:

`effective training minutes / 60 * configured method relevance`

The existing effective-load evidence already incorporates training readiness/effectiveness, so Skill Progression does not independently recalculate fatigue/readiness or call physical progression engines.

Recent-practice saturation uses a 24-sim-hour window:

`1 / (1 + recent_raw_learning_units / 2)`

bounded to `0.10..1.00`.

Current-proficiency diminishing returns:

`clamp((100 - score) / 40, 0.05, 1.00)`

Score gain:

`effective_learning_units * 0.12 * proficiency_factor`

with a hard v1 score cap of `100`.

These constants are bounded simulation/gameplay semantics, not physiological or educational-science claims. They are configuration data so later evidence can justify tuning without rewriting the engine.

Experience accumulates effective learning units independently of score gain. A highly proficient actor may keep accumulating legitimate practice evidence while score growth becomes very small near the cap.

## Idempotency and audit

`skill_progression_settled` events record:

- skill key and bootstrap state;
- consumed action event IDs;
- old/new score and experience;
- method IDs and relevance weights;
- effective minutes;
- recent-practice units;
- saturation factor;
- proficiency factor;
- per-evidence score delta.

Consumed action event IDs cannot be credited twice.

## Observability

The deployed Character Change Observability foundation snapshots the Skills query surface around post-action settlements. A legitimate `character_skills.score` change therefore automatically inherits:

- Profile `▲/▼` deltas;
- cumulative `0.10` skill significance threshold;
- immediate grade-transition significance;
- per-character stat notification control;
- ordinary 5-real-minute anti-spam debounce;
- aggregated Character Progression pushes.

No Skill-specific Telegram subsystem exists.

## Acceptance and deployment evidence

PR #104 final tested head: `bc0dd277013c9cbed727fa48880dc2ff1258cc20`.

Validated before merge:
- CI #789 / run `31869352929`: SUCCESS;
- Skill Progression Foundation v1 Acceptance #2 / run `31869352985`: SUCCESS on disposable production copy after an infra-only SSH retry;
- Public Readiness Security Audit #58: SUCCESS;
- Strength Live Cycle, Strength/Stamina progression, BC-2, BC-3, Height, Physical Presentation, Sexual Anatomy and Inventory acceptance surfaces: SUCCESS;
- Solo Regulation acceptance: SUCCESS after its validator was made deterministic on the disposable copy instead of depending on current live cooldown/recovery timing.

Focused production-copy acceptance proved:
- initialization bootstrap leaves represented score/experience unchanged;
- historical eligible evidence is cursor-consumed without retroactive gain;
- a synthetic future Heavy-Bag session on the disposable copy produces legitimate score and experience gain from Training Method evidence;
- the same action event cannot be credited twice;
- re-initialization preserves earned skill state;
- production itself is not moved, trained, accelerated or otherwise mutated for evidence.

Merge: `a8c86705700f689024c75fe91e00be9361ae557a`.

Deploy #196 / run `31869399038`: SUCCESS.

Post-merge:
- CI #790 / run `31869399041`: SUCCESS;
- Skill Progression Foundation v1 Acceptance #3 / run `31869399147`: SUCCESS on main.

Deploy readback verified service healthy, schema v5, autonomy normal at 1.0x, Gemini primary cognition preserved, Groq tested fallback preserved, Telegram connected, and the live Hand-to-Hand query value remained at its pre-progression represented baseline after bootstrap. No live combat session was forced merely to manufacture a progression occurrence.

## Next pattern

The structural invariant is proven. Follow-ons should be **batched by evidence pattern**, not implemented as one PR/deploy per skill.

Before adding a skill to the batch, define legitimate evidence sources and method/action bindings rather than inferring learning from generic action names or model prose.

Likely groups:
- combat-practice skills where Training Method evidence is authoritative;
- study/research/technical skills where Research/action evidence is authoritative;
- fieldcraft/practical skills only where concrete actions already produce meaningful evidence.

## Deferred

Not part of v1:
- skill decay/retention/reacquisition;
- real opponent-performance learning evidence;
- RAPS legacy skill-alias derivation/cleanup;
- careers/jobs/quests;
- broad Mind/Behavior architecture.
