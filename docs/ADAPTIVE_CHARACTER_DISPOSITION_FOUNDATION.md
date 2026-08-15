# Adaptive Character Disposition Foundation

Status: **COMPLETE v1 — MINIMUM FOUNDATION**

## Creator direction

Character disposition must not be interpreted as permanently fixed just because a field is canonical or already reaches cognition. The vertical-completeness checkpoint means the profile surface is runnable; it does **not** mean all developmental lifecycles are complete.

Observer Sandbox models four different plasticity classes instead of one generic mutable-profile mechanism:

1. **Personality — slow plasticity.** Stable authored dispositions may drift slightly only from accumulated long-horizon evidence. Ordinary single events never directly rewrite personality.
2. **Preferences — medium plasticity.** Repeated exposure, outcomes, voluntary choice, aversion and satisfaction may strengthen, weaken or reverse preferences over time.
3. **Hobbies / interests — developmental lifecycle.** Situational interest may become recurring interest, then an established hobby; established hobbies may become dormant or lapsed.
4. **Habits — cue-dependent learned behavior.** Repeated behavior in a stable represented context builds automaticity; prolonged non-reinforcement weakens expression while preserving history.

## Authority contract

The LLM remains proposal-only.

`represented actions/events -> deterministic evidence extraction -> disposition adaptation -> persisted state -> cognition context`

The model may use current disposition state when proposing an action, but it may not directly create, delete, score, or rewrite personality traits, preferences, hobbies, or habits. Canonical profile data supplies authored baselines; ordinary initialization/deploy must not reset learned runtime state or manufacture evidence.

## Scientific design constraints

The implementation follows conservative behavioral-science principles rather than pretending to reproduce a complete psychological model:

- personality is relatively stable but not immutable;
- habit strength emerges gradually from repetition in a stable context;
- context consistency matters for habit formation;
- one missed repetition must not erase a habit;
- non-reinforcement/long inactivity weakens expression gradually rather than deleting history;
- interests and preferences may develop through repeated engagement and represented outcomes;
- preference reversal requires accumulated opposing evidence rather than one surprising event;
- personality adaptation is materially slower than preference adaptation;
- all adaptation remains bounded and slower than moment-to-moment cognition.

These are design constraints, not clinical or population-frequency claims.

## Implementation sequence / status

Use exemplar-first, then batch-by-pattern:

1. **Habit Formation / Extinction Exemplar v1 — COMPLETE.**
2. **Hobby / Interest Lifecycle v1 — COMPLETE.**
3. **Preference Adaptation v1 — COMPLETE.**
4. **Slow Personality Plasticity v1 — COMPLETE.**

The Adaptive Character Disposition Foundation is therefore **closed at minimum-foundation v1**. Do not deepen local psychology next; return to the broader Overall Workflow/Foundation Review first.

## Habit Formation / Extinction Exemplar v1 — COMPLETE

PR #167 proved that completed represented behavior can create persistent learned disposition state without LLM mutation authority.

A habit candidate is keyed by represented behavior plus a stable context cue. Formation is gradual, short-interval repetition is diminished, and long inactivity can weaken an established habit into dormant/lapsed states without deleting its history. Dynamic state persists in `character_habits`, coexists with canonical baseline rows, survives ordinary initialization/deploy, and reaches cognition as compact context.

## Hobby / Interest Lifecycle v1 — COMPLETE

See `docs/HOBBY_INTEREST_LIFECYCLE_V1.md`.

PR #172 proved a second evidence-to-disposition pattern:

`completed voluntary target engagement -> learned interest authority -> established hobby projection -> cognition`

V1 uses completed target-based `read` / `use` engagement, gradual cross-day establishment, diminished short-interval repetition, dormant/lapsed lifecycle preservation, learned-interest authority in `character_preferences(type='interest')`, and established projection into `character_hobbies`. Authored hobbies remain independent baselines and the LLM has no lifecycle mutation authority.

## Preference Adaptation v1 — COMPLETE

See `docs/PREFERENCE_ADAPTATION_V1.md`.

PR #174 proved medium-plastic preference adaptation:

`represented voluntary engagement / explicit represented outcome -> signed preference evidence -> persisted ledger -> established active preference projection -> cognition`

Automatic positive evidence is intentionally limited to completed target-based `read` / `use` engagement. Non-selection and inactivity are never negative evidence. Negative evidence requires an explicit represented aversive/outcome producer. Opposing evidence must pass through a neutral band before reversal. Authored canonical preferences remain untouched.

Runtime checkpoint:
- final head `6396ab34d190cfa894b69dcb9bdd52c743b4b02a`;
- CI #938 / run `31900387940`: 566 passed;
- merge `c72807dab416f64d459f4e4863efc15ce02c09e7`;
- Deploy #234 / run `31900505874`: SUCCESS.

Natural production runtime subsequently accumulated single-day Preference Adaptation evidence for ordinary completed `read` / `use` actions. Those rows are evidence only and are not overinterpreted as established preferences.

## Slow Personality Plasticity v1 — COMPLETE

See `docs/SLOW_PERSONALITY_PLASTICITY_V1.md`.

PR #176 proves the fourth and slowest adaptation pattern without rewriting canonical personality fields.

Authority:

`represented completion / explicit represented outcome -> registered authored-trait evidence channel -> long-horizon ledger -> bounded overlay -> cognition`

V1 exemplar:
- authored baseline trait: `disciplined`;
- automatic positive evidence: completed represented `train` actions via `completed_deliberate_training`;
- explicit registered positive outcome channel: `represented_self_regulation_outcome`;
- explicit registered opposing channel: `represented_counter_discipline_outcome`.

Key boundaries:
- the trait must already exist in the actor's authored `personality.primary_traits` and have a registered evidence channel;
- arbitrary new traits and arbitrary evidence kinds are rejected;
- same-day repetition has personality evidence weight `0`;
- cognition-visible drift requires signed score magnitude >=14, effective evidence >=14, at least 14 distinct evidence days, and at least 21 simulated days of horizon;
- first eligible overlay is only `0.02` and all overlay is capped at `0.15`;
- negative/softening evidence is never inferred from omission, inactivity, or missed routine;
- opposing evidence must first neutralize prior evidence and then accumulate over the same long-horizon contract before softening appears;
- canonical trait text is never rewritten;
- cognition receives only compact `character.personality.slow_adaptation`, not the evidence ledger;
- evidence persists under `runtime_state` namespace `personality_plasticity_v1:`;
- no schema migration was required; schema remains v5.

Runtime checkpoint:
- PR #176 final head `0874bb301b432201895b82465b0fd275b0bb0945`;
- **CI #939 / run `31901212644`: SUCCESS — 574 passed in 80.08s**;
- fresh DB init/status healthy; schema v5;
- Height Lifecycle, Eating Behavior, and Sexual Anatomy/Physiology production-copy gates initially hit infrastructure-only SSH/staging connection resets before validator execution; only those failed jobs were retried and all three actual validators then succeeded;
- merge `c5a4f7cfa84965fe656070e54663c27f3ab8796f`;
- **Deploy #235 / run `31901325402`: SUCCESS**.

Verified production readback after Deploy #235:
- service active and healthy; schema v5;
- autonomy enabled, normal mode, retry null, pending action present;
- speed **1x**;
- sim time `2025-05-07T19:44:00+00:00`;
- Darian was naturally in `self_satisfaction` in Darian's Master Suite;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy.

No `personality_plasticity_v1:` row appeared in the deploy readback. That is expected and important: deploy/init did not fabricate personality evidence, and the current private action is not a personality evidence channel. A live personality overlay therefore remains intentionally unproven until ordinary runtime naturally accumulates the long-horizon represented evidence required by the contract.

## Non-goals

This foundation does not add:
- a giant psychology engine;
- arbitrary LLM profile writes;
- relationship mechanics;
- clinical psychiatric modeling;
- hard daily behavior quotas;
- instant deletion of old dispositions;
- universal reward scoring for every action;
- personality mutation from single ordinary events;
- broad automatic trait inference from unrelated behavior.

Additional adaptive depth should be added only when a represented runtime contract supplies semantically defensible evidence and only after higher-priority cross-system foundations are reviewed.

## Next phase

**Return to the Overall Workflow/Foundation Review.** Start read-only and audit the actual canonical/runtime coverage before implementing another slice. Candidate cross-system areas include generic action/task lifecycle, resources/inventory consequences, environment/world context, knowledge/familiarity, inter-character participation, event/lifecycle handling, longer-horizon progression/decay, and autonomy goal continuity. Treat those as audit candidates, not assumed gaps.
