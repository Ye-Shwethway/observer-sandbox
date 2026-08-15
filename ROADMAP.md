# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-16

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve: `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Prefer **vertical completeness before local depth**.
- Never manipulate production merely to manufacture evidence.
- Verification is focused-first. Code/runtime PRs get one final full CI checkpoint by default; docs-only changes do not need the Python suite; do not deliberately repeat the full suite after merge.

## Character Profile checkpoint

All Character Profile sections are minimum-unlocked v1. Skills remains CLOSED v1.

Minimum-unlocked means a section has authoritative state plus a meaningful runtime/cognition influence and appropriate persistence/rendering. It does **not** mean exhaustive local mechanics.

## Adaptive Character Disposition Foundation — COMPLETE v1

See `docs/ADAPTIVE_CHARACTER_DISPOSITION_FOUNDATION.md`.

Canonical sequence is complete:

`Habit Formation/Extinction -> Hobby/Interest Lifecycle -> Preference Adaptation -> Slow Personality Plasticity`

### Habit Formation/Extinction v1 — COMPLETE

PR #167 established deterministic habit adaptation from completed represented behavior plus stable context. Formation is gradual, same-day repetition is diminished, long inactivity may move learned habits through established/dormant/lapsed states without deleting history, and compact dynamic state reaches cognition.

### Hobby / Interest Lifecycle v1 — COMPLETE

PR #172 established gradual interest formation and established-hobby projection from bounded voluntary `read` / `use` evidence while preserving canonical hobbies and deterministic mutation authority.

### Preference Adaptation v1 — COMPLETE

PR #174 established medium-plastic signed preference evidence, gradual dynamic `like` / `dislike` projection, neutral-band reversal, no negative inference from non-selection, canonical baseline preservation, and cognition visibility.

### Slow Personality Plasticity v1 — COMPLETE

PR #176 establishes the slowest disposition layer. See `docs/SLOW_PERSONALITY_PLASTICITY_V1.md`.

Current contract:
- canonical `personality.primary_traits` remains the authored baseline and is never rewritten;
- v1 proves one reusable registered channel for the authored `disciplined` trait;
- completed represented `train` actions may contribute `completed_deliberate_training` evidence;
- arbitrary traits/evidence kinds are rejected and a mapped trait must exist in the actor's authored baseline;
- same-day repetition has personality evidence weight 0;
- cognition-visible drift requires score/effective evidence >=14, at least 14 distinct evidence days, and at least 21 simulated days of horizon;
- first eligible overlay is only 0.02 and all overlay is capped at 0.15;
- negative/softening evidence requires an explicit registered represented outcome and is never inferred from omission/inactivity;
- opposing evidence must cross neutral and accumulate under the same long-horizon contract before softening;
- compact established overlay reaches cognition under `character.personality.slow_adaptation`;
- evidence ledger persists under `runtime_state` namespace `personality_plasticity_v1:`;
- LLM cognition has no mutation authority;
- schema remains v5.

Do not deepen psychology next. This foundation is closed at minimum depth.

## Autonomy continuity — Livelock Watchdog v1 COMPLETE

PRs #168/#169 narrowed model correction/planning context; PR #170 added a bounded continuity breaker for repeated authoritative action/target pair-validation livelock. It remains intentionally narrow and does not recover provider/API/quota/rate-limit or unrelated failures.

## Current verified deployment

Latest runtime deployment: **Deploy #235 / run `31901325402` SUCCESS**, Slow Personality Plasticity v1, PR #176 merge `c5a4f7cfa84965fe656070e54663c27f3ab8796f`.

Final tested PR head: `0874bb301b432201895b82465b0fd275b0bb0945`.

Validation:
- **CI #939 / run `31901212644` SUCCESS**;
- **574 passed in 80.08s**;
- fresh DB init/status succeeded; schema remains v5;
- all final automatic gates were green;
- Height Lifecycle, Eating Behavior, and Sexual Anatomy/Physiology production-copy gates initially hit infrastructure-only SSH/staging connection resets before validator execution;
- only those three failed jobs were retried, and all three actual disposable production-copy validators then succeeded;
- no code change was made for the transient infrastructure failures and no duplicate full Python suite was deliberately run.

Verified production readback after Deploy #235:
- service active and healthy; schema v5;
- autonomy enabled, normal mode, retry null, pending action present;
- speed **1x**;
- sim time `2025-05-07T19:44:00+00:00`;
- Darian was naturally in `self_satisfaction` in Darian's Master Suite;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy.

Production also contained ordinary one-day Preference Adaptation evidence rows from completed `read` / `use` behavior. These are evidence only, not established preferences.

No `personality_plasticity_v1:` row appeared in the deploy readback. Deploy/init therefore did not fabricate personality evidence. A live personality overlay remains intentionally unproven until ordinary runtime naturally accumulates the required long-horizon evidence.

## Skills — CLOSED v1

Frozen learned Skill surface:
- Hand-to-Hand Combat
- Bladed Weapons
- Firearms
- Survival
- Tactical Planning
- Technology
- Field Medicine

`Weapon Mastery` remains a derived/non-executable parent over Bladed Weapons + Firearms. Hidden legacy `weapons` remains compatibility only.

## Next phase — Overall Workflow/Foundation Review

Perform a **read-only canonical + production audit first** before selecting another runtime slice. Do not reopen local profile/psychology depth just because the adaptive foundation now exists.

Audit candidates:
- generic action/task lifecycle;
- resources/inventory/state consequences;
- environment/world context;
- knowledge/familiarity;
- inter-character participation;
- event/lifecycle handling;
- longer-horizon progression/decay;
- autonomy planning / goal continuity;
- remaining profile-to-cognition/runtime integration gaps, if any.

These are candidates, not assumed deficiencies. Let current source/contracts/live evidence determine the actual gaps and batch structurally equivalent work where possible.

## Deferred boundaries

No giant psychology engine, relationship-system expansion by default, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, bleeding/wound taxonomy, definitive-treatment engine, random-accident scheduler, deep weapon taxonomy, economy/jobs/quests, real-world weapon instructions, arbitrary LLM profile mutation, or synthetic production actors/actions solely for proof.

## Exact resume point

**Adaptive Character Disposition Foundation is COMPLETE v1 at minimum-foundation depth: Habit Formation/Extinction v1, Hobby/Interest Lifecycle v1, Preference Adaptation v1, and Slow Personality Plasticity v1 are all implemented. Slow Personality Plasticity is deployed through PR #176 final head `0874bb301b432201895b82465b0fd275b0bb0945`, CI #939 with 574 passed, merge `c5a4f7cfa84965fe656070e54663c27f3ab8796f`, and Deploy #235 SUCCESS. Production is healthy at schema v5 with autonomy normal, retry null, pending action present, speed 1x, sim time `2025-05-07T19:44:00+00:00`; Darian was naturally in `self_satisfaction` in the Master Suite. No synthetic personality evidence was created and no live personality overlay is claimed. Resume with a read-only Overall Workflow/Foundation Review and prioritize actual cross-system gaps before local depth.**
