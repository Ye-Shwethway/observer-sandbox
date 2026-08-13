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

Future uses may include important character/world events, runtime failures, watched-character/location activity, or later category-specific preferences layered under the global gate.

If the global preference is OFF, proactive notifications are suppressed for that user. Direct replies to commands/callbacks are interactive responses and are not suppressed by this preference.

## Action completion contract

When an autonomous character action completes successfully and its deterministic state transition has committed, every authorized user whose global notification preference is ON should receive one concise summary message.

The notification should include:

- character name;
- completed action and human-readable target name when one exists;
- canonical human-facing simulated timestamp;
- completed simulated duration and approximate real wait at the action's recorded speed;
- short cognition reason when available;
- location or location transition;
- changed basic physiological stats as before -> after values and deltas when present.

### Mandatory next-update block

When the normal next decision boundary resolves successfully and a new action has been planned, the **same Character Update notification must also include**:

- the newly planned next action and human-readable target;
- its planned simulated duration;
- approximate real wait at the recorded speed;
- its expected simulated completion / next-update timestamp.

A successfully planned next action must not be silently omitted from the proactive Character Update message. This ETA is intentionally visible in the notification itself so the Creator can know the expected next update without opening a detailed/status surface.

The service may resolve the next normal decision boundary immediately after completion so the same completion notification can expose what is now in progress and when its next update is expected. This does not authorize a second proactive planning notification.

If the next decision does not resolve successfully because of failure/backoff/control state, the message must not invent an ETA.

Do not push on scheduler polling ticks, action planning alone, `in_progress`, bookkeeping events, or recovered duplicate completion records. **One committed action still produces at most one proactive push per recipient.**

The displayed next-update time is an estimate for the currently planned action. Pause/control intervention, service interruption, runtime failure/backoff, or other later state changes can delay or invalidate it.

Time semantics remain runtime-owned: wall wait is approximately `duration_minutes × 60 / speed` seconds. At normal production `1x`, one simulated minute is therefore approximately one real minute between action boundaries.

Delivery is **best effort and downstream of simulation truth**. A Telegram network/API failure must never roll back or invalidate a successfully committed universe action. Successful deliveries persist the last delivered action id per recipient to prevent duplicate pushes from repeated service processing.

## Authorization

Only authorized Telegram users may receive proactive world/character data or read/change their own notification preference through the exposed bot surface. Owner and Allowed User recipients use the same global preference gate; Owner precedence still applies to role resolution.

Future owner-managed user controls must not silently rewrite another user's preference unless an explicit administrative design is approved.

## Presentation

Notification messages must follow `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md` presentation rules: human-readable names, mobile-scannable structure, restrained icons, and canonical display timestamps where simulated time is shown.

Normal action notifications must not expose internal ids when a human-readable entity name exists.

## Persistence boundary

Notification preferences and delivery-deduplication markers are Telegram UI/configuration state, not world state. They may be stored in runtime configuration storage but must never alter simulation truth, character state, or scheduler semantics.

See `docs/AUTONOMY_BREADTH_TIME_OBSERVABILITY.md` for the production rollout that introduced duration and next-action ETA presentation.