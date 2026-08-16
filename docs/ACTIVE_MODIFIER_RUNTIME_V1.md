# Active Modifier Runtime Foundation v1

Status: COMPLETE v1 / DEPLOYED

## Why this slice exists

The composable runtime has long carried a first-class `active_modifiers` schema socket with source, time bounds, field key, operation, stack key/policy and conditions. Domain-specific modifiers are already real runtime behavior: Training Readiness shapes training cost/effectiveness, and Cognitive Performance contracts shape declared represented-task outcome dimensions.

The remaining cross-system gap was different: persisted temporary modifiers in `active_modifiers` could be stored but had no generic resolver and therefore no effective runtime influence.

This slice closes that minimum lifecycle without replacing the existing domain contracts or creating a universal hidden bonus engine.

## Contract

### Generic resolution

`resolve_active_modifier_value(...)` resolves one numeric base value for one subject + field at one simulation timestamp.

Supported operations reuse the existing schema vocabulary:
- `add`;
- `multiply`;
- `set`;
- `clamp_min`;
- `clamp_max`.

Time bounds are half-open:

`starts_sim_time <= as_of_sim_time < ends_sim_time`

A missing end time means the row remains active until another authority explicitly removes or supersedes it. Expired rows remain historical persisted rows; ordinary reads do not delete them.

### Stack semantics

Rows without a `stack_key` are independent.

Rows sharing one `stack_key` must share one policy:
- `stack`: apply all rows in deterministic start-time/id order;
- `replace`: use the newest active row;
- `max`: use the active row with the greatest numeric modifier value;
- `min`: use the active row with the smallest numeric modifier value.

Mixed policies inside one stack key fail closed.

After stack selection, the selected rows are applied in deterministic `starts_sim_time, id` order.

### Conditions

V1 condition semantics are intentionally small. `conditions_json` is an exact key/value match against explicit caller context. Empty conditions are unconditional. A conditional modifier does not activate when the caller supplies no matching context.

The runtime snapshot exemplar uses no contextual condition map, so only unconditional temporary physiology/need modifiers affect that surface in v1. Later domain consumers may supply their own authoritative context rather than growing an implicit global condition language.

## First runtime consumer

The existing actor runtime snapshot now resolves active modifiers for exactly the six established living-state fields:
- `needs.energy`;
- `needs.hunger`;
- `needs.thirst`;
- `needs.sleepiness`;
- `physiology.cleanliness`;
- `physiology.fatigue`.

These effective values feed the same cognition, need-priority, training-readiness and deterministic action-validation paths that already consume `snapshot()`.

The stored base field is **not overwritten** by a temporary modifier. `_advance_needs()` continues to mutate raw authoritative physiology from represented elapsed actions. This prevents a temporary effect from being baked permanently into the base state. Once a modifier expires, the effective read naturally falls back to the still-authoritative base value plus any remaining active modifiers.

The six living-state outputs remain clamped to the existing 0..100 runtime range.

## Authority and safety boundaries

- LLM cognition does not create, edit or delete `active_modifiers`.
- This slice does not invent modifier producers. It only makes the existing persisted socket executable.
- Active modifiers do not rewrite profile canon, Skill scores, inventory, world topology or action definitions.
- Existing Training Readiness and Cognitive Performance contracts remain independent domain-specific systems.
- No modifier may bypass ordinary action target/capability/resource validation.
- Schema remains v5.
- Deploy/init does not fabricate active modifier rows through this slice.

## Acceptance evidence

Regression coverage proves:
- half-open activation/expiry without row deletion;
- deterministic `stack`, `replace`, `max`, and `min` policy behavior;
- exact contextual conditions;
- mixed-policy stacks fail closed;
- snapshot effective value differs from stored base while active and returns to base after expiry;
- a temporary fatigue modifier can make training deterministically unavailable through the existing action legality path, then restore ordinary availability after expiry;
- the underlying fatigue base remains unchanged by the temporary modifier itself.

Canonical checkpoint:
- PR #180 final head `49000d37542ec80cf489f8bd5c78876aaba16201`;
- CI #941 / run `31921368331`: SUCCESS;
- full suite: **590 passed in 58.12s**;
- Minimum Training Stimulus Acceptance #27: SUCCESS;
- Strength Live Cycle Validation v1 #83: SUCCESS;
- Solo Regulation Naturalism v2 Acceptance #30: SUCCESS;
- merge `74a0d9db25b3249192c24954feed11a45a7c961d`;
- Deploy #237 / run `31921444434`: SUCCESS.

Production readback after Deploy #237:
- service active/healthy; schema v5;
- autonomy enabled/normal, retry null, pending action preserved, speed 1x;
- Darian remained naturally asleep in Darian's Master Suite;
- living-state readback: cleanliness 98.491, energy 88.791, fatigue 6.305, hunger 7.578, sleepiness 58.55, thirst 23.15;
- deploy output exposed sim time only as `2025-05-07T***:27:00+00:00`; the masked hour is not inferred;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy.

The deploy workflow does not query `active_modifiers` row count. This checkpoint therefore does **not** claim a verified live row count or claim that a modifier was naturally active in production. No modifier producer was introduced by this slice.

## Non-goals

V1 does not add modifier authoring UI, automatic item/status-effect producers, weather, medication/drug systems, generalized profile-field modification, hidden Skill/IQ bonuses, arbitrary expression conditions, modifier cleanup jobs, or universal application across every domain.

Do not deepen this system merely for completeness. Return to the Overall Workflow/Foundation Review and select the next genuine cross-system gap from current canonical/live evidence.
