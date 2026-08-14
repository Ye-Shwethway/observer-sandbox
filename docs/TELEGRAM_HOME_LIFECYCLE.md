# Telegram Observer Home Message Lifecycle

Status: ACTIVE / AUTHORIZED

## Intent

Keep the private Creator chat tidy while preserving `/start` as the fast mobile entry point to Observer Sandbox.

## `/start` board lifecycle

The Observer Home message created by `/start` is ephemeral presentation state, not world/runtime state.

Current v1 behavior:

- the Home keyboard includes `✕ Close`;
- manual Close deletes the Home message through Telegram `deleteMessage` rather than replacing it with a closed placeholder;
- newly sent `/start` Home boards are scheduled for automatic deletion;
- default TTL is 300 seconds / 5 minutes;
- `OBSERVER_TELEGRAM_HOME_TTL_SECONDS` may override the TTL, bounded to 30..3600 seconds;
- deletion failure is non-fatal and must never affect simulation/autonomy.

The timer is an in-process Telegram presentation timer. A service restart may forget outstanding deletion timers; manual Close remains available and no persistent simulation schema is added for ephemeral chat cleanup.

## Architecture boundary

Message lifecycle stays inside the Telegram adapter extension. It must not become a simulation event, cognition input, Creator mutation, or world-state field.

The existing polling shell remains authoritative; the Creator extension hooks send/edit/API behavior rather than duplicating the polling engine.

## Security

Close callbacks pass through the same private-chat and authorization gate as other callbacks. No world data is exposed by the lifecycle mechanism.
