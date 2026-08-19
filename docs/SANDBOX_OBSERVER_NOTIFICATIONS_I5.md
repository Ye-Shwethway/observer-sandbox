# Sandbox Observer / Notifications I5

Status: implementation acceptance

## Purpose

Provide Creator-only observability for Creation Sandbox state changes without inventing autonomous activity and without mixing notification state with the canonical Real World.

## Invariants

- Creation Sandbox events are the source of truth for this observer flow.
- Notifications never create simulation facts.
- Real World `events`, `runtime_state`, Telegram notification baselines and canonical Character state are not used as sandbox notification ownership.
- Notification preference and delivery cursor are scoped by `(sandbox_id, Telegram user_id)`.
- Delivery is cursor based: one observed sandbox event is not repeatedly emitted after successful dispatch.
- Disabling proactive updates does not delete sandbox history.
- `runtime_ready` remains distinct from `running`.
- No autonomous-action notification type is emitted until a sandbox-safe autonomous execution path actually exists.

## Observed event set

I5 initially observes explicit Creation Sandbox lifecycle/configuration/runtime-control events such as:

- sandbox object approval/activation;
- archive/delete/reset where represented;
- Character-to-Location relation binding;
- sandbox Character AI assignment;
- represented runtime-option refresh;
- sandbox clock configuration;
- sandbox speed changes;
- sandbox pause/resume.

The whitelist is intentional. Unknown future events do not become proactive notifications automatically.

## Telegram surface

`Sandbox World -> 📡 Observer`

The view provides:

- proactive Sandbox Updates ON/OFF;
- recent sandbox event presentation;
- Mark Current Seen;
- explicit Creation Sandbox / Real World isolation language.

## Dispatch contract

`creation_sandbox_events -> filter whitelisted events newer than user cursor -> aggregate -> transport send -> advance cursor only after successful send`

The dispatcher is deterministic and transport-agnostic. A transport failure must leave the cursor unchanged so the event remains pending.

## Scope boundary

This foundation defines event selection, preference, cursoring, formatting and deterministic dispatch. Long-poll Telegram transport wiring may be attached only through the existing Telegram adapter after this contract is green; transport must not own simulation semantics.

No full sandbox autonomy execution, canonical transmigration or second Real World Character activation is part of I5.
