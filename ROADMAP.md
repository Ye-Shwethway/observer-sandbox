# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

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

PR #172 establishes the second adaptive-disposition exemplar. See `docs/HOBBY_INTEREST_LIFECYCLE_V1.md`.

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

No schema migration was required; schema remains v5.

## Autonomy continuity — Livelock Watchdog v1 COMPLETE

A production freeze exposed a reusable autonomy-continuity gap. PRs #168/#169 narrowed the model correction/planning context; PR #170 added the bounded deterministic continuity breaker documented in `docs/AUTONOMY_LIVELOCK_WATCHDOG_V1.md`.

The watchdog remains intentionally narrow: third consecutive same-sim-boundary authoritative pair-validation failure only, normal mode only, current legal action surface only, ordinary validation preserved, and no recovery for provider/API/quota/rate-limit, schedule, completion, or unrelated failures.

## Current verified deployment

Latest runtime deployment: **Deploy #233 / run `31899884337` SUCCESS**, Hobby / Interest Lifecycle v1, PR #172 merge `3822332c0fb5bca7295e83e0cc0bcebf06973be8`.

Final tested PR head: `05388eba4c6e9e4870b3eb0e927c0247c0e68f06`.

Validation:
- **CI #937 / run `31899806440` SUCCESS**;
- **560 passed in 37.15s**;
- fresh DB init/status succeeded; schema remains v5;
- body, attribute/progression, physical presentation, height, sexual lifecycle, and other task-relevant automatic gates were green;
- Skill Progression Foundation production-copy acceptance initially hit an infrastructure-only SSH `Connection reset by peer` before its validator ran; only that failed job was retried, and the disposable production-copy validator then succeeded;
- no code change was made for that transient infrastructure failure and no duplicate full Python suite was deliberately run.

Verified production readback after Deploy #233:
- service active and healthy; schema v5;
- autonomy enabled, normal mode, retry null, pending action present;
- speed **5x**;
- sim time `2025-05-07T17:19:00+00:00`;
- Darian was naturally idle in the Top-Class Home Gym at readback;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy.

No production `read`/`use` action was fabricated to manufacture Hobby/Interest evidence. Therefore deployment proves the lifecycle is installed and healthy; it does **not** by itself prove that a new learned hobby has naturally formed in production yet.

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

1. Keep Habit and Hobby/Interest lifecycle contracts at minimum-foundation depth.
2. Implement **Preference Adaptation v1** next: bounded strengthening/weakening from legitimate repeated voluntary choice/outcome evidence, without arbitrary LLM writes or instant preference reversal.
3. Then implement slow Personality Plasticity v1 only after preference adaptation proves the reusable evidence-to-disposition pattern.
4. Return to the broader Overall Workflow/Foundation Review after this adaptive-disposition foundation is minimally complete.
5. Deeper psychology, richer hobby taxonomy/proficiency, identity transformation, relationships, and other local depth remain later work.

## Deferred boundaries

No relationship-system expansion, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, bleeding/wound taxonomy, definitive-treatment engine, random-accident scheduler, deep weapon taxonomy, economy/jobs/quests, real-world weapon instructions, arbitrary LLM profile mutation, or synthetic production actors/actions solely for proof.

## Exact resume point

**Habit Formation/Extinction v1 and Hobby/Interest Lifecycle v1 are complete as the first two Adaptive Character Disposition exemplars. Hobby/Interest Lifecycle v1 is deployed through PR #172 final head `05388eba4c6e9e4870b3eb0e927c0247c0e68f06`, CI #937 with 560 passed, merge `3822332c0fb5bca7295e83e0cc0bcebf06973be8`, and Deploy #233 SUCCESS. Production is healthy at schema v5 with autonomy normal, retry null, pending action present, speed 5x, and sim time `2025-05-07T17:19:00+00:00`. No synthetic hobby evidence was created. Resume with Preference Adaptation v1 at minimum-foundation depth.**
