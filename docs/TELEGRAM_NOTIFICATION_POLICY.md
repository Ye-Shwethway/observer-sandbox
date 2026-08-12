# Telegram Notification Policy

Status: ACTIVE CONTRACT
Scope: proactive Creator-facing Telegram notifications.

## Default

Notifications are **ON by default for every authorized Telegram user**. Absence of a stored preference means enabled.

Preferences are persisted per Telegram user in the runtime database and survive bot/service restarts and deployments.

## Commands

Canonical commands:

- `/notify on`
- `/notify off`

Accepted compatibility aliases:

- `/notification on|off`
- `/notifications on|off`
- `/notion/on`
- `/notion/off`

The `/notion/...` aliases are retained because they were explicitly requested during initial rollout; future UI/help text should prefer the canonical `/notify on|off` form.

## Shared gate

There must be one reusable per-user notification preference gate. New proactive features must consult this shared preference instead of inventing separate global toggles.

Current use:

- Owner startup notification: `Universe is alive!`

Future uses may include:

- important character/world events;
- runtime failures or fail-closed autonomy events;
- watched-character or watched-location activity;
- later category-specific notification preferences layered under the global gate.

If the global preference is OFF, proactive notifications are suppressed for that user. Direct replies to commands/callbacks are interactive responses and are not suppressed by this preference.

## Authorization

Only authorized Telegram users may read or change their own notification preference through the exposed bot surface. Future owner-managed user controls must not silently rewrite another user's preference unless an explicit administrative design is approved.

## Presentation

Notification messages must follow `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md` presentation rules: human-readable names, mobile-scannable structure, restrained icons, and canonical display timestamps where simulated time is shown.

## Persistence boundary

Notification preferences are Telegram UI/configuration state, not world state. They may be stored in runtime configuration storage but must never alter simulation truth, character state, or scheduler semantics.
