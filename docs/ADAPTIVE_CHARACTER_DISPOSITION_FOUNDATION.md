# Adaptive Character Disposition Foundation

Status: ACTIVE FOUNDATION

## Creator direction

Character disposition must not be interpreted as permanently fixed just because a field is canonical or already reaches cognition. The vertical-completeness checkpoint means the profile surface is runnable; it does **not** mean all developmental lifecycles are complete.

Observer Sandbox should model four different plasticity classes instead of one generic mutable-profile mechanism:

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

## Implementation sequence

Use exemplar-first, then batch-by-pattern:

1. **Habit Formation / Extinction Exemplar v1 — implement now.**
2. Hobby / Interest Lifecycle v1.
3. Preference Adaptation v1.
4. Slow Personality Plasticity v1.

Do not build all four at once.

## Habit Formation / Extinction Exemplar v1

### Purpose

Prove the reusable contract that completed represented behavior can create persistent learned disposition state without LLM mutation authority.

### Evidence

A habit candidate is keyed by a represented behavior plus a stable context cue. The minimum v1 cue is the action's represented location; target may further distinguish the behavior when present.

Movement, idle and sleep are not habit-learning evidence in this exemplar. Private sexual actions are intentionally excluded from general habit cognition/disposition learning.

### Formation

Each eligible repeated behavior in the same cue context reinforces the same candidate. Strength rises asymptotically and is bounded to 0..100. A candidate stays `emerging` until both repetition and strength thresholds are met; only then may it become `established`.

There is no one-action habit creation and no fixed claim that every human habit requires the same number of days.

### Weakening / extinction

V1 implements conservative inactivity-based weakening:

- recent habits do not decay;
- after an authored grace period, simulated-time inactivity produces gradual bounded decay;
- sufficiently weakened established habits become `dormant` rather than being deleted;
- very weak, long-unreinforced dynamic habits may become `lapsed` but their history remains persisted.

A later refinement may add explicit cue-present / behavior-omitted extinction evidence if the runtime gains a clean represented opportunity contract. V1 must not infer missed opportunities from every unrelated action in the same room.

### Persistence

Dynamic habit rows live in `character_habits` using the existing `strength` and `metadata_json` surface. Canonical seed rows and runtime-learned rows coexist.

Profile initialization must:

- ensure canonical baseline habits/preferences/hobbies exist;
- preserve extra runtime-learned rows;
- preserve runtime strength/status/evidence metadata;
- never `DELETE` the whole adaptive table during ordinary initialization.

This preservation rule applies immediately to preferences and hobbies too, even before their own adaptation engines arrive, because otherwise future learned state would be structurally unsafe.

### Cognition

Existing concise habit names remain available for compatibility. Cognition additionally receives compact dynamic metadata (strength/status/cue) for runtime-learned habits. It must not receive internal evidence ledgers or mutation commands.

## Non-goals

This foundation does not add:

- a giant psychology engine;
- arbitrary LLM profile writes;
- personality mutation in the habit slice;
- hobby or preference formation in the habit slice;
- relationship mechanics;
- clinical psychiatric modeling;
- hard daily behavior quotas;
- instant deletion of old dispositions;
- Darian-specific habit switch logic.

## Completion standard for the exemplar

Habit v1 is complete when focused regression proves:

1. repeated eligible action+context evidence strengthens one persistent dynamic habit candidate;
2. a single repetition does not establish a strong habit;
3. repeated consistent evidence can transition `emerging -> established`;
4. long simulated inactivity weakens and may transition an established habit to `dormant` without deleting it;
5. canonical reinitialization preserves dynamic habit state and extra learned rows;
6. preferences/hobbies are no longer destructively reset during seed import;
7. cognition can see compact habit dynamics while deterministic runtime remains mutation authority.

## Later foundation review

The broader Overall Workflow/Foundation Review remains active. Adaptive disposition is a cross-cutting continuity foundation within that review, not permission to reopen every profile section for deep local work.
