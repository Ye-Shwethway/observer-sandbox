# Character Change Observability & Notification Foundation v1

Status: COMPLETE / DEPLOYED

## Purpose

Make existing and future progression visible without turning tiny simulation settlements into notification spam.

Core invariant:

`authoritative mutation/history -> domain-aware cumulative delta -> significance policy -> grade-transition check -> presentation ledger -> Profile delta UX + eligible aggregated notification`

The authoritative profile/skill/body value and its normal history remain truth. Change ledgers and notification baselines are presentation/preferences only.

## Separation of precision

Engine precision, display precision and notification significance are different concerns.

- progression engines may settle at high precision;
- Profile UX may show more useful precision for slowly changing measurements;
- proactive notifications require a larger domain-aware cumulative change unless a grade boundary is crossed.

No progression engine is allowed to quantize its authoritative state merely to make Telegram easier to render.

## Observation boundary

The service captures the tracked profile before the existing post-action progression settlement family and again after current progression/body/lifecycle/presentation settlements.

The generic observer therefore covers current:
- graded Attributes / physical progression;
- BC-2 Body Composition values;
- BC-3 Body Measurements;
- current Skills query values;
- derived Body grading/reference rows and section grades where represented.

Individual progression engines do not call Telegram and are not modified to own presentation state. Future Skill Progression can inherit the same observation boundary by changing authoritative `character_skills.score` before the after-snapshot.

Actors without a represented Character Profile no-op safely. Sexual anatomy/current sexual state, personality, preferences/habits and recovery-status surfaces are not part of this v1 progression-change observer merely because they may contain numeric values.

## Cumulative significance / anti-spam

Microscopic changes accumulate against a surfaced baseline. A settlement below threshold does not disappear; it contributes to the next cumulative comparison.

Initial v1 significance defaults:
- RAPS / Skill score: `0.10` points;
- body circumferences: `0.05 in` cumulative;
- structural Height: `0.10 in`;
- Weight: `0.25 lb`;
- Body Fat: `0.10` percentage point;
- derived ratios: `0.01`;
- section overall grades: grade-transition only.

These are visibility/notification defaults, not biological progression step sizes.

A grade transition is always meaningful even when raw numeric movement is below the normal threshold.

Example:
`Strength 89.98 (A) -> 90.01 (S)` is surfaced immediately despite only `+0.03` raw movement.

### Push debounce

Ordinary stat-change pushes are additionally limited to one message per recipient/character per **5 real minutes**. Meaningful changes that occur inside that cooldown remain pending and continue accumulating from the last successfully notified baseline.

Grade transitions are rare/high-signal events and bypass the ordinary debounce. A failed Telegram send does not consume the pending baseline.

## Profile UX

Meaningful recent deltas are attached by the query/presentation layer and shown independently of notification preferences.

Direction and quality are separate concepts:
- `▲` / `▼` = numeric direction;
- `🟢` = beneficial where the domain has an explicit monotonic/grade semantic;
- `🔴` = detrimental where such semantics exist;
- descriptive Body measurements are direction-only by default rather than assuming larger/smaller is universally better.

Slow-changing Body measurements render to two decimal places in the Body section so changes such as `+0.05 in` remain visible. This precision change is scoped to `body.*` measurement fields and does not alter other inch-valued profile domains such as sexual anatomy.

Notification OFF never suppresses Profile deltas.

## Aggregated proactive notification

A recipient receives at most one `CHARACTER PROGRESSION` message for one actor at one eligible progression boundary. Multiple significant field changes are batched into that message.

Notification baseline advances only after a successful send. Failed delivery does not consume the pending meaningful change.

The message is capped to a bounded number of visible rows and summarizes any additional simultaneous changes.

## Notification gates

A stat/progression push requires all three:

`global notifications ON AND per-character stat notifications ON AND significant change present`

The existing global `/notify on|off` remains the outer user-level gate.

Character-scoped preference:
- `/statnotify` lists current active character states;
- `/statnotify <character name or id> on|off` changes one caller's preference;
- Character detail includes a `Stat Updates: ON/OFF` inline toggle.

Default policy:
- current/default actor: stat notifications ON unless explicitly overridden;
- other/future characters: stat notifications OFF until explicitly enabled.

This prevents a future multi-character universe from becoming notification-heavy merely because characters exist.

## Backlog prevention

Changing a per-character preference resets that recipient/actor notification baseline to current state.

Explicit global notification toggles also reset all current character stat baselines for that recipient.

Therefore OFF -> ON begins fresh monitoring and never replays a historical backlog burst. Historical authoritative profile/history evidence remains queryable separately.

## Privacy and authority

This layer does not widen profile visibility. It observes only the explicitly tracked non-intimate progression/profile families for this v1 and uses existing Telegram authorization/global notification controls.

Telegram does not become progression authority. Runtime-state ledgers are derived UX/preference state and may be rebuilt/reset without changing canonical profile values or progression history.

## Verification / release evidence

Runtime PR #102 final tested head: `f3694480af22770286607adbb05751e06b29ee5a`.

Validated on the candidate through:
- CI #777 / run `31867315561` SUCCESS;
- Sexual Anatomy Physiology Lifecycle v1 Acceptance #23 SUCCESS;
- Stamina Progression Activation v1 Acceptance #42 SUCCESS;
- Height Lifecycle v1 Acceptance #14 SUCCESS;
- Physical Presentation Closure v1 Acceptance #10 SUCCESS;
- Body Composition Progression v1 Acceptance #31 SUCCESS;
- Body Measurement Progression v1 Acceptance #27 SUCCESS;
- Attribute Grading Batch 1 Acceptance #36 SUCCESS;
- Read-Only Grading Proof Acceptance #37 SUCCESS;
- Strength Progression Auto Activation v1 Acceptance #41 SUCCESS after an infra-only VPS staging retry;
- Inventory Operations v1 Acceptance #37 SUCCESS after an infra-only VPS staging retry.

PR #102 merged as `bfd57ebec3b897be66ec81774de314d16a63db59`.

Deploy #195 / run `31867444633` SUCCESS. Readback verified service healthy/active, schema version 5, autonomy enabled in normal mode at 1.0x, Telegram API connected, Gemini `gemini-3.1-flash-lite` primary cognition preserved and the tested Groq fallback preserved. Production progression/profile state was not forced or accelerated to manufacture notification evidence.

Post-merge CI #778 / run `31867444621` SUCCESS.

## Development sequencing

This foundation intentionally precedes Skill Progression Foundation v1 and is now complete/deployed.

The next planned family returns to Skill Progression using Hand-to-Hand Combat as the bounded exemplar. New legitimate skill-score changes should inherit Profile arrows, cumulative significance, grade-transition visibility, debounce and character-scoped notification controls without a skill-specific Telegram subsystem.
