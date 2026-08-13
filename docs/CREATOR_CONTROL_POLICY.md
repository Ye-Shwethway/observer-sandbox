# Creator Control Policy

Status: ACTIVE
Scope: privileged administrative controls that directly alter Observer Sandbox runtime/world state under explicit Creator authority.

## Purpose

Creator controls are a deliberate escape hatch for administrative intervention in the running universe. They are not character actions, not cognition proposals, and not ordinary observer commands.

The first implemented control is **Restore Basic Stats** for a character. Future Creator controls must be added one minimum-runnable slice at a time rather than as a broad admin framework.

## Authority boundary

The Creator may authorize a bounded direct state mutation through a trusted control service. That authorization does **not** transfer domain ownership of the affected fields.

Examples:
- `needs.energy`, `needs.hunger`, `needs.thirst`, `needs.sleepiness` remain owned by `needs_engine`;
- `physiology.cleanliness` and `physiology.fatigue` remain owned by `physiology_engine`;
- `runtime.current_action` remains owned by `living_runtime`.

Creator authority is recorded in the control event/audit payload. Normal simulation engines continue owning the resulting fields afterward.

LLMs never receive Creator-control authority.

## First control — Restore Basic Stats

Current baseline:
- Energy: `75`
- Hunger: `20`
- Thirst: `15`
- Sleepiness: `15`
- Cleanliness: `80`
- Systemic fatigue: `0`

The restore is actor-scoped and currently defaults to `char_darian` in operator surfaces.

It preserves:
- simulation time;
- current location;
- canonical profile data;
- autonomy enabled/disabled state;
- autonomy mode;
- world topology and all unrelated state.

It resets `runtime.current_action` to `idle` and cancels an outstanding pending autonomous action because the action's original physiological reason may no longer be valid after the restore. Actor lease/retry state is cleared and the actor wake reason becomes `creator_basic_stats_restored`, allowing cognition to re-evaluate from the restored state.

## Audit/event contract

Every successful privileged restore must append a `creator_basic_stats_restored` event containing at least:
- actor id;
- location id;
- simulation time;
- requested-by identity/source;
- Creator authority marker;
- cancelled pending action id when present;
- before/after snapshots;
- explicit state changes;
- applied baseline.

The control event is administrative history. It is not fabricated as a character action and does not need to appear in the default narrative history feed.

## Access control

### Telegram

- Only the configured `OBSERVER_TELEGRAM_OWNER_ID` may apply Creator-authority mutations.
- Allowed users may continue using the ordinary authorized observer surface but cannot invoke root Creator controls.
- Server-side authorization is mandatory even if a control button is hidden from non-owners.
- Mutating inline controls should use a confirmation step when a mistaken tap could alter live state.

Current Telegram surfaces:
- owner-only `🩺 Restore Basic Stats` button on a character view;
- confirmation screen before callback mutation;
- owner-only `/restorestats [character_id]` typed command for deliberate direct use.

### CLI / Actions

Operator CLI:

`sandboxctl creator restore-basic-stats --character <character_id>`

GitHub Actions exposes the same backend through `.github/workflows/creator-control.yml`. The workflow's initial push is guarded by a persistent marker so the bootstrap production restore is applied only once automatically. A later deliberate `workflow_dispatch` may apply the restore again.

## Safety rules for future Creator controls

A new control must:
1. call a reusable backend control service rather than write SQLite directly from Telegram;
2. define exactly which state it may mutate and which state it must preserve;
3. retain normal domain field authority after the intervention unless the feature explicitly changes ownership;
4. invalidate/cancel stale pending work when the mutation makes that work semantically obsolete;
5. append a queryable audit event with before/after evidence;
6. enforce owner/operator authorization server-side;
7. expose a human-readable confirmation/result in Creator-facing UI;
8. have focused tests and production readback before being considered live;
9. remain independent of LLM cognition;
10. stay within the minimum-runnable expansion policy.

Do not build generic arbitrary-field editing, SQL consoles, unrestricted entity mutation, or bulk world rewriting under the label of Creator Control. Add narrow typed controls only when a concrete operational use case exists.
