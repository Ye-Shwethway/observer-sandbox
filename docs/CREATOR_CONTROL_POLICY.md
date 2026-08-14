# Creator Control Policy

Status: ACTIVE
Scope: privileged administrative controls that directly alter Observer Sandbox runtime/world state under explicit Creator authority.

## Purpose

Creator controls are deliberate administrative interventions. They are not character actions, cognition proposals or ordinary observer commands. Add them one bounded typed use case at a time; never turn Creator Control into arbitrary database editing.

Implemented controls:
1. Restore Basic Stats — actor-scoped living-state reset.
2. Replenish Inventory Stack — positive bounded stock addition to an existing stack.

## Authority boundary

The Creator may authorize a bounded mutation through a trusted reusable control service. That authorization does not give LLM cognition direct mutation authority and does not erase normal domain ownership afterward.

Telegram/CLI/Actions are adapters. They call backend control services; they never own the mutation semantics or write SQLite directly.

## Restore Basic Stats

Current baseline:
- Energy 75;
- Hunger 20;
- Thirst 15;
- Sleepiness 15;
- Cleanliness 80;
- systemic Fatigue 0.

The actor-scoped restore preserves simulation time, location, canonical profile, autonomy enabled/mode, world topology and unrelated state. It resets current action to idle, cancels a now-stale pending action, clears actor lease/retry and emits `creator_basic_stats_restored` with before/after evidence.

Field authority remains with the normal needs/physiology/living engines after the intervention.

## Replenish Inventory Stack

Backend: `replenish_inventory_stack(stack_id, quantity, ...)`.

This control is universal; it is not specific to Darian, one Estate or food. Any existing compatible stack anywhere in the universe may be targeted by stable stack id.

Allowed mutation:
- existing stack only;
- positive bounded quantity only;
- quantity is **added** to current stock.

It must preserve:
- item definition identity;
- owner;
- storage/container relation;
- world topology;
- simulation time;
- character profile/physiology;
- actor autonomy/runtime state.

It may not:
- create arbitrary definitions/stacks;
- set negative stock;
- change ownership/container;
- perform arbitrary SQL/field editing;
- impersonate a character action;
- trigger an LLM call.

Every successful replenishment emits `creator_inventory_replenished` containing Creator authority, requester/source, stack and definition ids, item name, added quantity/unit, before/after quantity, owner, container and resolved physical location.

## One-time canonical stock migrations

A Creator-approved canonical baseline migration is distinct from an ordinary Creator control call.

For example, `thorne-estate-wealthy-food-reserve-v1` uses `ensure_minimum` once to establish a realistic reserve while external purchasing/economy is absent. A durable marker prevents reapplication. Once applied, ordinary re-init/deploy must not refill depleted stock.

Such migrations emit explicit administrative audit evidence and must be production-copy validated before live deployment.

## Access control

### Telegram

- `OBSERVER_TELEGRAM_OWNER_ID` is the root Creator authority.
- Allowed users may use exposed read-only observer surfaces, including inventory browsing, but may not apply Creator mutations.
- Authorization is rechecked server-side for every mutation callback/command; hidden buttons are not authorization.
- Button-driven mutation uses a confirmation screen before application.

Current owner mutation surfaces include:
- `🩺 Restore Basic Stats` + confirmation;
- `/restorestats [character_id]`;
- inventory stack `➕ Replenish Stock` + confirmation;
- `/replenish <stack_id> <positive_quantity>`.

### CLI / Actions

Operator surfaces may expose the same reusable backend control services with equivalent authorization/audit policy. The existing basic-stats operator workflow remains separately guarded.

## Safety rules for future Creator controls

A new control must:
1. call a reusable backend control service;
2. define exactly what it may mutate and what it preserves;
3. retain normal domain authority afterward unless explicitly changing authority is the feature;
4. cancel/invalidate stale work only when the mutation makes that work obsolete;
5. append queryable audit evidence;
6. enforce owner/operator authorization server-side;
7. provide human-readable confirmation/result for risky UI actions;
8. have focused regression and state-sensitive production-copy/readback evidence where appropriate;
9. remain independent of LLM cognition;
10. stay minimum-runnable and entity/id generic.

Do not add arbitrary-field editors, SQL consoles, unrestricted entity mutation or bulk world rewriting under Creator Control.
