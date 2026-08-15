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
- adaptation rates must be bounded and slower than moment-to-moment cognition.

These are design constraints, not clinical or population-frequency claims.

## Implementation sequence / status

Use exemplar-first, then batch-by-pattern:

1. **Habit Formation / Extinction Exemplar v1 — COMPLETE.**
2. **Hobby / Interest Lifecycle v1 — COMPLETE.**
3. **Preference Adaptation v1 — NEXT.**
4. Slow Personality Plasticity v1.

Do not build the remaining layers all at once.

## Habit Formation / Extinction Exemplar v1 — COMPLETE

PR #167 proved that completed represented behavior can create persistent learned disposition state without LLM mutation authority.

A habit candidate is keyed by represented behavior plus a stable context cue. Formation is gradual, short-interval repetition is diminished, and long inactivity can weaken an established habit into dormant/lapsed states without deleting its history. Dynamic habit state persists in `character_habits`, coexists with canonical baseline rows, survives ordinary initialization/deploy, and reaches cognition as compact dynamic context.

The exemplar intentionally does not infer missed opportunities from arbitrary unrelated actions and excludes movement, idle, sleep, and private sexual actions from generic habit-learning evidence.

## Hobby / Interest Lifecycle v1 — COMPLETE

See `docs/HOBBY_INTEREST_LIFECYCLE_V1.md`.

PR #172 proves a second evidence-to-disposition pattern without adding a new schema.

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

## Preference Adaptation v1 — NEXT

The next minimum slice should reuse the proven evidence-to-disposition architecture without conflating interests, hobbies, habits and preferences.

Minimum goals:
- preserve authored preferences as starting baselines rather than immutable forever-values;
- require legitimate repeated voluntary choice/outcome evidence before meaningful strengthening/weakening;
- prevent one ordinary event from instantly reversing an authored preference;
- keep adaptation bounded and auditable;
- preserve history/state across initialization/deploy;
- expose the adapted preference surface to cognition through the existing profile context;
- keep the LLM proposal-only.

Exact evidence categories and reversal thresholds must be derived from current represented actions/outcomes rather than invented as a giant generic reward engine.

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
- personality mutation before the Preference Adaptation exemplar is proven.

## Later foundation review

The broader Overall Workflow/Foundation Review remains active. Adaptive disposition is a cross-cutting continuity foundation within that review, not permission to reopen every profile section for deep local work.
