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

Current uses:

- startup notification: `Universe is alive!`;
- **character action completion summaries** after a committed autonomous action changes world/character state.

Future uses may include:

- important character/world events beyond ordinary action completion;
- runtime failures or fail-closed autonomy events;
- watched-character or watched-location activity;
- later category-specific notification preferences layered under the global gate.

If the global preference is OFF, proactive notifications are suppressed for that user. Direct replies to commands/callbacks are interactive responses and are not suppressed by this preference.

## Action completion contract

When an autonomous character action completes successfully and its deterministic state transition has committed, every authorized user whose global notification preference is ON should receive one concise summary message.

The notification should include, when relevant:

- character name;
- completed action and human-readable target name;
- canonical human-facing simulated timestamp;
- short cognition reason;
- location or location transition;
- changed basic physiological stats as before -> after values and deltas.

Do not push on scheduler polling ticks, action planning alone, `in_progress`, bookkeeping events, or recovered duplicate completion records. One committed action should produce at most one push per recipient.

Delivery is **best effort and downstream of simulation truth**. A Telegram network/API failure must never roll back or invalidate a successfully committed universe action. Successful deliveries persist the last delivered action id per recipient to prevent duplicate pushes from repeated service processing.

## Authorization

Only authorized Telegram users may receive proactive world/character data or read/change their own notification preference through the exposed bot surface. Owner and Allowed User recipients use the same global preference gate; Owner precedence still applies to role resolution.

Future owner-managed user controls must not silently rewrite another user's preference unless an explicit administrative design is approved.

## Presentation

Notification messages must follow `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md` presentation rules: human-readable names, mobile-scannable structure, restrained icons, and canonical display timestamps where simulated time is shown.

Normal action notifications must not expose internal ids such as `obj_meal_stock` or `room_gym` when a human-readable entity name exists.

## Persistence boundary

Notification preferences and delivery-deduplication markers are Telegram UI/configuration state, not world state. They may be stored in runtime configuration storage but must never alter simulation truth, character state, or scheduler semantics.
