# Skill Progression Foundation v1

Status: IMPLEMENTED CANDIDATE / VALIDATION PENDING

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
- read-time grade = derived from the existing `skill-proficiency-100-v1` grading scheme;
- model prose, action reason text and Telegram are never progression authority.

The historical RAPS skill-like fields such as `raps_pa.combat_skill`, `raps_pa.weapons_proficiency` and `raps_pa.survival_skill` are not independent live progression authorities. In this exemplar they remain legacy compatibility snapshots. Exact alias derivation/cleanup is a follow-on concern; Hand-to-Hand progression mutates only `character_skills.hand_to_hand_combat`.

## Seed / deployment safety

Canonical skill seeds are initialization baselines, not periodic resets.

`import_seed()` no longer deletes and recreates all character skill rows. A progression-active skill preserves its current score, experience and progression metadata across ordinary initialize/deploy/status paths. Extra learned skills absent from the canonical seed are also preserved.

The first Skill Progression settlement is a non-progressing bootstrap. It consumes all already-existing eligible historical action evidence and marks the represented skill progression-active without inventing historical XP or retroactively changing the authored score.

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

The existing training-load evidence already incorporates training readiness/effectiveness, so Skill Progression does not independently recalculate fatigue/readiness or call the physical progression engines.

Recent-practice saturation uses a 24-sim-hour window:

`1 / (1 + recent_raw_learning_units / 2)`

bounded to `0.10..1.00`.

Current-proficiency diminishing returns:

`clamp((100 - score) / 40, 0.05, 1.00)`

Score gain:

`effective_learning_units * 0.12 * proficiency_factor`

with a hard v1 score cap of `100`.

These constants are bounded simulation/gameplay semantics, not physiological or educational-science claims. They are configuration data so future evidence can justify tuning without rewriting the engine.

Experience accumulates effective learning units independently of score gain. A highly proficient actor may therefore continue accumulating legitimate practice evidence while score growth becomes very small near the cap.

## Idempotency and audit

`skill_progression_settled` events record:

- skill key;
- bootstrap/non-bootstrap state;
- consumed action event IDs;
- old/new score;
- old/new experience;
- method IDs and weights;
- effective minutes;
- recent-practice units;
- saturation factor;
- proficiency factor;
- per-evidence score delta.

Consumed action event IDs cannot be credited twice.

## Observability

The deployed Character Change Observability foundation already snapshots the Skills query surface around post-action settlements.

Therefore a legitimate `character_skills.score` change automatically inherits:

- Profile `▲/▼` deltas;
- cumulative `0.10` skill significance threshold;
- immediate grade-transition significance;
- per-character stat notification control;
- ordinary 5-real-minute anti-spam debounce;
- aggregated Character Progression pushes.

No Skill-specific Telegram subsystem is added.

## Deferred

Not part of this exemplar:

- skill decay/retention/reacquisition;
- progression for Weapons, Survival, Tactical Planning, Technology or Field Medicine;
- real combat/opponent-performance learning evidence;
- RAPS legacy skill-alias derivation/cleanup;
- careers/jobs/quests;
- broad Mind/Behavior architecture.

Once this invariant is validated, structurally equivalent learned skills should be added by batch-by-pattern rather than one PR per skill.
