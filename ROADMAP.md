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
- hobbies/interests may form, strengthen, become identity-linked, go dormant, or lapse;
- habits are learned cue/context -> behavior tendencies with gradual formation and extinction/decay.

Do not convert these domains into static forever-fields merely because the profile minimum-unlock pass is closed.

## Adaptive Character Disposition Foundation — ACTIVE

See `docs/ADAPTIVE_CHARACTER_DISPOSITION_FOUNDATION.md`.

Canonical implementation order:

`Habit Formation/Extinction exemplar -> Hobby/Interest Lifecycle -> Preference Adaptation -> slow Personality Plasticity`

### Habit Formation/Extinction exemplar v1 — COMPLETE

PR #167 established the first deterministic adaptive-disposition exemplar.

Current contract:
- represented completed behavior + stable context supplies habit evidence;
- same-day repetition receives diminishing evidence rather than linear spam credit;
- habit strength develops gradually and can move through emerging/established/dormant/lapsed states;
- inactivity weakens habits gradually rather than deleting history;
- cognition receives compact habit-dynamics context;
- the LLM does not directly mutate habit strength/status.

A critical persistence flaw was also fixed: profile initialization/deploy no longer deletes and reseeds runtime preferences/hobbies/habits. Canonical profile data is the **starting baseline**, not a perpetual reset authority over learned disposition state.

Hobby/Interest Lifecycle v1 is the next planned adaptive-disposition exemplar after continuity cleanup.

## Autonomy continuity — Livelock Watchdog v1 COMPLETE

A production freeze exposed a reusable autonomy-continuity gap.

Observed incident:
- service remained active;
- Darian remained in the Training Hall at sim time `2025-05-07T15:04:00+00:00`;
- no pending action existed;
- repeated decision-stage `ValueError` events rejected `move -> loc_thorne_estate_food_storage` because the pair was outside the currently authoritative need-shaped `action_options`;
- exponential retry backoff reached 256 seconds and effectively froze universe progress.

PR #168 added one bounded corrective model retry while preserving deterministic validation.
PR #169 made reachable-resource previews planning-only and removed actionable target IDs from advisory context.
The live model still repeated the invalid pair, proving a deterministic continuity breaker was required.

PR #170 added **Autonomy Livelock Watchdog v1**. See `docs/AUTONOMY_LIVELOCK_WATCHDOG_V1.md`.

Watchdog boundaries:
- eligible only for the third consecutive same-sim-boundary decision-pair validation failure;
- normal autonomy only; no canary recovery;
- no recovery for provider/API/rate-limit/quota, schedule, completion, or unrelated errors;
- recovery chooses only from the already-shaped authoritative `action_options`;
- strong/critical physiology therefore keeps normal need-resolution priority;
- discretionary recovery prefers targetless `idle`, then `rest`;
- ordinary deterministic action validation still applies;
- provenance is carried in action conditions and therefore ordinary action-start evidence.

## Current verified deployment

Latest runtime deployment: **Deploy #232 / run `31899099486` SUCCESS**, Autonomy Livelock Watchdog v1, PR #170 merge `b17fbb7fe77e3d4e79f71d0b9a526244ef81c9ff`.

Final tested PR head: `efe4814483cb997c941555e40de879532058938a`.

Validation:
- **CI #936 / run `31899038839` SUCCESS**;
- **554 passed in 38.40s**;
- fresh DB init/status succeeded; schema remains v5;
- Cognition Capability Awareness, Research Action Semantics, Training Movement Contract Normalization, Eating Behavior, and Solo Regulation Naturalism acceptance gates were green on the final head.

Verified production recovery after Deploy #232:
- service remained active;
- the prior eight-failure retry/backoff state cleared to `current_retry = null`;
- a legal pending action was scheduled (`71ab5f8e-...` at first readback);
- a later readback showed a different pending action (`9b02ef99-...`), proving the first recovered action completed and autonomy crossed another action boundary rather than remaining frozen;
- the old Food Storage validation errors remain historical event evidence and were not erased.

No production state was fabricated to prove recovery.

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

## Solo Sexual Regulation Naturalism v2 — COMPLETE

Current corrected baseline includes authored libido, bounded positive young-adult/recovery/solitude context, libido-shaped release recency, trailing-24h saturation, 2h anti-loop pacing, authored private-activity semantics, and graph-based safe-private-location awareness. There is no daily/weekly quota and cognition retains discretion.

## Near-term sequence

1. Keep the Autonomy Livelock Watchdog bounded; do not broaden it into a generic deterministic decision-maker.
2. Continue Adaptive Character Disposition Foundation with **Hobby/Interest Lifecycle v1** as the next exemplar.
3. Then implement Preference Adaptation and slow Personality Plasticity only at minimum-foundation depth.
4. Return to the broader Overall Workflow/Foundation Review after this human-continuity foundation is minimally complete.
5. Deeper psychology, richer hobby taxonomy, identity transformation, relationships, and other local depth remain later work.

## Deferred boundaries

No relationship-system expansion, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, bleeding/wound taxonomy, definitive-treatment engine, random-accident scheduler, deep weapon taxonomy, economy/jobs/quests, real-world weapon instructions, arbitrary LLM profile mutation, or synthetic production actors/actions solely for proof.

## Exact resume point

**Habit Formation/Extinction exemplar v1 is deployed and runtime-learned dispositions now survive initialization/deploy. The Training Hall autonomy freeze was diagnosed as repeated LLM action/target noncompliance rather than service crash or provider call-limit failure. PR #170 final head `efe4814483cb997c941555e40de879532058938a` passed CI #936 with 554 tests, merged as `b17fbb7fe77e3d4e79f71d0b9a526244ef81c9ff`, and Deploy #232 succeeded. Production readback cleared the eight-failure retry state and then showed two successive pending action IDs, proving autonomy resumed across an action completion boundary. Resume with Hobby/Interest Lifecycle v1, preserving adaptive-disposition semantics and the bounded watchdog contract.**
