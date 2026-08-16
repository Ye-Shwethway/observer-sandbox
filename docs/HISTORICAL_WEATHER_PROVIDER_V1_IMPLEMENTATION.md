# Historical Weather Provider v1 — Implementation Notes

## Runtime owner

`src/observer_sandbox/service.py` performs one best-effort shared-world weather synchronization before actor autonomy ticks. Weather is therefore world infrastructure, not character behavior.

## Provider adapter

`src/observer_sandbox/historical_weather_provider.py`

Responsibilities:
- load provider configuration;
- derive provider date/hour from timezone-aware universe simulation time;
- fetch/cache a historical provider day;
- select one UTC simulation hour;
- normalize provider fields into W1;
- publish the W1 state through the existing W0 ambient-stimulus bridge;
- provide deterministic explicitly-synthetic continuity fallback when historical data is temporarily unavailable.

The adapter does not perform cognition, appraisal, memory encoding or action selection.

## Cache

Environment schema v2 adds `weather_provider_cache`, keyed by `(provider_id, cache_date)`.

A successful cache row stores the provider day response. An error row stores bounded operational error text and fetch time so repeated service wakes respect a retry cooldown rather than hammering the provider.

## Replay identity

Exact state ids are stable by provider + UTC simulation hour. Fallback ids are separately namespaced. This lets recovered exact historical data supersede the synthetic state through W1's existing overlap/supersession semantics.

## Deployment behavior

After service restart, the first active-autonomy loop asks for weather covering the current universe hour. If the historical request succeeds, W1 contains an `open_meteo_historical_weather` state. If it fails, the service continues and W1 may contain a `deterministic_weather_fallback` state marked `synthetic=true`.

The network provider is not a service-health dependency: external weather failure must not stop the sandbox.

## Data boundary

Historical provider response -> cache -> normalized W1 state -> W0 stimulus.

Neither cache rows nor raw provider JSON are character knowledge.
