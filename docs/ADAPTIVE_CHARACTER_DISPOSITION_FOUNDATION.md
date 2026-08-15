# Adaptive Character Disposition Foundation

Status: ACTIVE FOUNDATION

## Creator direction

Character disposition must not be interpreted as permanently fixed just because a field is canonical or already reaches cognition. The vertical-completeness checkpoint means the profile surface is runnable; it does **not** mean all developmental lifecycles are complete.

Observer Sandbox models four different plasticity classes instead of one generic mutable-profile mechanism:

1. **Personality — slow plasticity.** Stable dispositions may drift gradually from accumulated long-horizon evidence. Ordinary single events must not directly rewrite personality.
2. **Preferences — medium plasticity.** Repeated exposure, outcomes, voluntary choice, aversion and satisfaction may strengthen, weaken or reverse preferences over time.
3. **Hobbies / interests — developmental lifecycle.** Situational interest may become recurring interest, then an established hobby; established hobbies may become dormant or lapsed when engagement/value disappears.
4. **Habits — cue-dependent learned behavior.** Repeated behavior in a stable represented context builds automaticity; prolonged non-reinforcement weakens expression. Habit state must persist across deployment/reinitialization.

## Authority contract

The LLM remains proposal-only.

`represented actions/events -> deterministic evidence extraction -> disposition adaptation -> persisted state -> cognition context`

The model may use current disposition state when proposing an action, but it may not directly create, delete or rewrite personality traits, preferences, hobbies or habits.

Canonical profile data supplies the starting disposition/baseline. Canonical seed import must never be treated as a perpetual reset of learned runtime state.

## Scientific design constraints

The implementation follows conservative behavioral-science principles rather than pretending to reproduce a complete psychological model:

- personality is relatively stable but not immutable;
- habit strength emerges gradually from repetition in a stable context, not from a single action;
- context consistency matters for habit formation;
- one missed repetition must not erase a habit;
- non-reinforcement/long inactivity should weaken expression gradually rather than hard-delete history;
- interests and preferences can develop through repeated engagement and outcomes;
- preference reversal should require accumulated opposing evidence rather than one surprising event;
- personality adaptation must be materially slower than preference adaptation;
- adaptation rates must be bounded and slower than moment-to-moment cognition.

These are design constraints, not clinical or population-frequency claims.

## Implementation sequence / status

Use exemplar-first, then batch-by-pattern:

1. **Habit Formation / Extinction Exemplar v1 — COMPLETE.**
2. **Hobby / Interest Lifecycle v1 — COMPLETE.**
3. **Preference Adaptation v1 — COMPLETE.**
4. **Slow Personality Plasticity v1 — NEXT.**

Do not build the remaining personality layer as a giant generic psychology engine.

## Habit Formation / Extinction Exemplar v1 — COMPLETE

PR #167 proved that completed represented behavior can create persistent learned disposition state without LLM mutation authority.

A habit candidate is keyed by represented behavior plus a stable context cue. Formation is gradual, short-interval repetition is diminished, and long inactivity can weaken an established habit into dormant/lapsed states without deleting its history. Dynamic habit state persists in `character_habits`, coexists with canonical baseline rows, survives ordinary initialization/deploy, and reaches cognition as compact dynamic context.

The exemplar intentionally does not infer missed opportunities from arbitrary unrelated actions and excludes movement, idle, sleep, and private sexual actions from generic habit-learning evidence.

## Hobby / Interest Lifecycle v1 — COMPLETE

See `docs/HOBBY_INTEREST_LIFECYCLE_V1.md`.

PR #172 proved a second evidence-to-disposition pattern without adding a new schema.

Authority:

`completed voluntary target engagement -> learned interest authority -> established hobby projection -> cognition`

Key boundaries:
- v1 evidence is intentionally limited to target-based `read` and `use` completions;
- one engagement creates only an emerging interest;
- cross-day repeated engagement plus bounded strength/effective-engagement thresholds can progress emerging -> recurring -> established;
- short-interval repetition receives reduced evidence weight;
- learned-interest lifecycle authority uses existing `character_preferences(type='interest')` rows;
- established learned interests materialize to `character_hobbies` as active projections;
- dormant/lapsed state can remove the active learned-hobby projection while preserving the authoritative interest row/history;
- canonical authored hobbies remain independent baseline rows;
- cognition consumes the ordinary preference/hobby surfaces and has no lifecycle mutation authority.

Production deployment deliberately did not force a `read`/`use` action merely to manufacture proof. Tests establish the deterministic lifecycle; natural production formation remains evidence-driven.

## Preference Adaptation v1 — COMPLETE

See `docs/PREFERENCE_ADAPTATION_V1.md`.

PR #174 proved a third evidence-to-disposition pattern: medium-plastic preference state can develop and reverse gradually without making authored preference rows disposable or granting the model mutation authority.

Authority:

`represented voluntary engagement / explicit represented outcome -> signed preference evidence -> persisted ledger -> established active preference projection -> cognition`

Key boundaries:
- automatic positive evidence in v1 is intentionally limited to completed target-based `read` / `use` engagement;
- a single engagement is evidence only and cannot create an instant visible preference;
- short-interval repetition is diminished;
- non-selection, inactivity, and arbitrary unrelated actions are never negative evidence;
- negative evidence requires an explicit represented aversive/outcome producer through the signed evidence API;
- per-target signed evidence persists in `runtime_state` under the `preference_adaptation_v1:` namespace;
- sufficiently repeated cross-day positive evidence can project a dynamic `like`; sufficiently repeated negative evidence can project `dislike`;
- opposing evidence weakens an active projection through a neutral band before the opposite preference can establish, preventing instant reversal;
- authored canonical preferences remain independent baseline rows and are not rewritten by dynamic projection handling;
- established dynamic preference rows reach cognition through the existing preference context;
- the LLM has no direct write path to scores, valence, evidence history, or projection status.

V1 deliberately does not include a universal aversion/satisfaction engine. The signed negative-evidence contract exists so a future represented outcome producer can supply legitimate evidence without changing preference authority semantics. No negative production event was fabricated for proof.

Runtime checkpoint:
- PR #174 final head `6396ab34d190cfa894b69dcb9bdd52c743b4b02a`;
- CI #938 / run `31900387940`: 566 passed; fresh DB healthy; schema v5;
- merge `c72807dab416f64d459f4e4863efc15ce02c09e7`;
- Deploy #234 / run `31900505874`: SUCCESS;
- three automatic production-copy gates initially hit SSH/rsync connection resets before validator execution; only those failed jobs were retried and all actual validators succeeded;
- production remained healthy with autonomy normal, retry null, a pending action, speed 5x, and sim time `2025-05-07T18:09:00+00:00`;
- Darian was naturally reading in the Living Room at readback, but the in-progress action was not claimed as an established learned preference.

## Slow Personality Plasticity v1 — NEXT

Personality is the slowest-plastic disposition layer and must not reuse preference timescales blindly.

Minimum goals:
- preserve authored personality traits as the stable baseline;
- ordinary single actions/events must never directly rewrite personality;
- require accumulated long-horizon, semantically relevant evidence before any drift is eligible;
- keep any drift small, bounded, auditable, and reversible only over similarly long horizons;
- prefer a persisted plastic overlay/evidence ledger over destructively rewriting canonical trait text;
- expose only the resulting compact adapted disposition context to cognition, not internal mutation instructions or evidence ledgers;
- keep deterministic runtime as sole mutation authority and the LLM proposal-only;
- avoid a giant trait taxonomy, universal reward model, clinical interpretation, or Darian-specific switches.

Exact evidence mappings and thresholds must be derived from the current represented runtime and existing personality cognition contract before implementation.

## Non-goals

This foundation does not add:

- a giant psychology engine;
- arbitrary LLM profile writes;
- relationship mechanics;
- clinical psychiatric modeling;
- hard daily behavior quotas;
- instant deletion of old dispositions;
- Darian-specific disposition switches;
- hobby proficiency/career systems;
- universal reward scoring for every action;
- personality mutation from single ordinary events.

## Later foundation review

The broader Overall Workflow/Foundation Review remains active. Adaptive disposition is a cross-cutting continuity foundation within that review, not permission to reopen every profile section for deep local work. Once Slow Personality Plasticity v1 is minimally complete, return to that broader foundation review before adding local psychology depth.
