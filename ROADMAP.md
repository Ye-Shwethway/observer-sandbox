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

Minimum-unlocked means a section has authoritative state plus a meaningful runtime/cognition influence and appropriate persistence/rendering. It does **not** mean every field is immutable or that its long-term developmental lifecycle is complete.

In particular:
- personality is comparatively stable but must remain slowly plastic over long evidence horizons;
- preferences are medium-plastic and may strengthen, weaken, form, or reverse from lived evidence;
- hobbies/interests may form, strengthen, become established, go dormant, or lapse;
- habits are learned cue/context -> behavior tendencies with gradual formation and extinction/decay.

## Adaptive Character Disposition Foundation — ACTIVE

See `docs/ADAPTIVE_CHARACTER_DISPOSITION_FOUNDATION.md`.

Canonical implementation order:

`Habit Formation/Extinction -> Hobby/Interest Lifecycle -> Preference Adaptation -> slow Personality Plasticity`

### Habit Formation/Extinction exemplar v1 — COMPLETE

PR #167 established deterministic habit adaptation from completed represented behavior plus stable context. Same-day repetition receives diminishing evidence, state develops gradually, inactivity may move learned habits through established/dormant/lapsed states without deleting history, and cognition receives compact dynamic context. Runtime adaptive rows survive ordinary initialization/deploy.

### Hobby / Interest Lifecycle v1 — COMPLETE

PR #172 established the second adaptive-disposition exemplar. See `docs/HOBBY_INTEREST_LIFECYCLE_V1.md`.

Current contract:
- completed represented voluntary target engagement is the only learning evidence;
- v1 eligibility is deliberately narrow: `read` and `use`;
- one engagement creates an `emerging` interest, not a hobby;
- repeated multi-day engagement can progress `emerging -> recurring -> established`;
- short-interval repetition receives diminished weight;
- learned interest authority lives in existing `character_preferences(type='interest')`;
- only established learned interests project into the active `character_hobbies` surface;
- long inactivity may move learned interests to dormant/lapsed while preserving lifecycle history;
- canonical authored hobbies remain independent and untouched;
- cognition reads existing preference/hobby surfaces but cannot mutate lifecycle state.

### Preference Adaptation v1 — COMPLETE

PR #174 established deterministic preference strengthening, weakening, and reversal at minimum-foundation depth. See `docs/PREFERENCE_ADAPTATION_V1.md`.

Current contract:
- repeated completed voluntary target-based `read` / `use` engagement supplies conservative positive evidence;
- one engagement is evidence only and does not create an instant visible preference;
- short-interval repetition receives diminished weight;
- non-selection, inactivity, and unrelated actions are never negative preference evidence;
- negative evidence requires an explicit represented aversive/outcome producer through the signed evidence API;
- per-target signed evidence persists in `runtime_state` under `preference_adaptation_v1:`;
- sufficiently repeated positive evidence projects an active dynamic `like`; sufficiently repeated negative evidence projects `dislike`;
- opposing evidence must pass through a neutral band before reversal, preventing instant `like <-> dislike` flips;
- authored canonical preferences remain untouched;
- established dynamic preferences reach cognition through the existing preference context;
- LLM cognition has no direct mutation authority.

No schema migration was required; schema remains v5.

## Autonomy continuity — Livelock Watchdog v1 COMPLETE

A production freeze exposed a reusable autonomy-continuity gap. PRs #168/#169 narrowed the model correction/planning context; PR #170 added the bounded deterministic continuity breaker documented in `docs/AUTONOMY_LIVELOCK_WATCHDOG_V1.md`.

The watchdog remains intentionally narrow: third consecutive same-sim-boundary authoritative pair-validation failure only, normal mode only, current legal action surface only, ordinary validation preserved, and no recovery for provider/API/quota/rate-limit, schedule, completion, or unrelated failures.

## Current verified deployment

Latest runtime deployment: **Deploy #234 / run `31900505874` SUCCESS**, Preference Adaptation v1, PR #174 merge `c72807dab416f64d459f4e4863efc15ce02c09e7`.

Final tested PR head: `6396ab34d190cfa894b69dcb9bdd52c743b4b02a`.

Validation:
- **CI #938 / run `31900387940` SUCCESS**;
- **566 passed in 114.85s**;
- fresh DB init/status succeeded; schema remains v5;
- Skill Progression Foundation, Physical Presentation, Strength, Stamina, Height, and other automatic gates were green;
- Body Composition, Sexual Anatomy/Physiology, and Body Measurement production-copy gates each initially hit an infrastructure-only SSH/rsync `Connection reset by peer` during staging before validators ran;
- only those three failed jobs were retried, and all three disposable production-copy validators then succeeded;
- no code change was made for those transient infrastructure failures and no duplicate full Python suite was deliberately run.

Verified production readback after Deploy #234:
- service active and healthy; schema v5;
- autonomy enabled, normal mode, retry null, pending action present;
- speed **5x**;
- sim time `2025-05-07T18:09:00+00:00`;
- Darian was naturally **reading in the Living Room** at readback;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy.

The natural in-progress `read` action is not claimed as an established learned preference. Preference evidence settles only on completed represented action boundaries. No production action or negative-outcome evidence was fabricated to manufacture proof.

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

## Near-term sequence

1. Keep Habit, Hobby/Interest, and Preference adaptation contracts at minimum-foundation depth.
2. Implement **Slow Personality Plasticity v1** next: only long-horizon accumulated evidence may produce a small bounded personality overlay/drift; ordinary single events must never rewrite personality.
3. Keep authored personality as the stable baseline and the LLM proposal-only; do not build a giant trait taxonomy or generic reward engine.
4. Return to the broader Overall Workflow/Foundation Review once slow Personality Plasticity minimally completes the Adaptive Character Disposition Foundation.
5. Deeper psychology, richer hobby taxonomy/proficiency, identity transformation, relationships, and other local depth remain later work.

## Deferred boundaries

No relationship-system expansion, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, bleeding/wound taxonomy, definitive-treatment engine, random-accident scheduler, deep weapon taxonomy, economy/jobs/quests, real-world weapon instructions, arbitrary LLM profile mutation, or synthetic production actors/actions solely for proof.

## Exact resume point

**Habit Formation/Extinction v1, Hobby/Interest Lifecycle v1, and Preference Adaptation v1 are complete as the first three Adaptive Character Disposition slices. Preference Adaptation v1 is deployed through PR #174 final head `6396ab34d190cfa894b69dcb9bdd52c743b4b02a`, CI #938 with 566 passed, merge `c72807dab416f64d459f4e4863efc15ce02c09e7`, and Deploy #234 SUCCESS. Production is healthy at schema v5 with autonomy normal, retry null, pending action present, speed 5x, and sim time `2025-05-07T18:09:00+00:00`; Darian was naturally reading in the Living Room. No synthetic preference evidence was created. Resume with Slow Personality Plasticity v1 at minimum-foundation depth.**
