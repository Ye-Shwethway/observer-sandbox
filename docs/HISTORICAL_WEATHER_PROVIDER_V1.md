# Historical Weather Provider v1

Status: IMPLEMENTATION SLICE

## Purpose

Historical Weather Provider v1 supplies authoritative external weather baseline data to the deployed W1 Environment / Weather Foundation without synchronizing universe time to the real-world clock.

The provider is an adapter, not a second weather engine.

Canonical flow:

`universe simulation time -> geographic sampling anchor -> historical provider/cache -> normalized W1 environment state -> W0 environment stimulus -> explicit character exposure -> future perception/appraisal/Mind`

Preserve the existing authority chain:

`external weather dataset != W1 normalized environment truth != W0 stimulus != character exposure != perception/appraisal != thought/memory != action authority`

## Time model

Observer Sandbox simulation time is authoritative. The provider must never use the host wall clock to decide which weather hour belongs in the universe.

Example:

- real deployment date may be 2026;
- universe simulation date may be 2025-05-03;
- provider lookup must request 2025-05-03 and select the hour corresponding to the universe simulation timestamp.

The current simulation clock is stored as offset-aware UTC. Provider requests therefore use GMT/UTC hourly timestamps for deterministic matching. Geographic daylight remains derived from the weather dataset's `is_day` field, not from the host clock.

## Primary external source

The initial provider is Open-Meteo Historical Weather API / archive endpoint.

Why this source:

- historical hourly weather is available for past simulation dates;
- the historical/reanalysis product is a better baseline for replaying past weather than binding the simulation to today's forecast;
- no API key is required for the ordinary public endpoint used by this project;
- requested variables map cleanly into the W1 schema.

Initial requested variables:

- temperature at 2 m;
- total precipitation;
- rain;
- snowfall;
- WMO weather code;
- cloud cover;
- visibility;
- wind speed at 10 m;
- day/night indicator.

Provider-specific payloads never become direct cognition input. They are normalized first.

## Geographic anchor

The Estate is canonically in South Lake Tahoe, California, but the repository does not currently define an exact real-world street coordinate for the fictional property.

Therefore v1 uses a documented **South Lake Tahoe city-area sampling anchor**, not an invented exact Estate coordinate.

The coordinate is infrastructure configuration only. It does not establish a new canonical Estate address or precise map position.

If exact canonical geography is introduced later, update the provider configuration without changing the W1/W0 contracts.

## Configuration

Canonical provider configuration:

`config/environment/weather.providers.v1.json`

Configuration owns:

- provider identity;
- endpoint;
- geographic sampling anchor;
- W1 scope location;
- timezone;
- requested variables;
- cache policy;
- fallback mode.

Do not hard-code Darian or any character identity in the provider.

## Daily local cache

The runtime caches provider responses by provider + simulation calendar date.

Reason:

- the service loop may evaluate autonomy many times during one simulation hour;
- weather should not require one network call per autonomy wake;
- one daily hourly response contains the full represented day;
- replay of an already cached simulation date should be deterministic and network-independent.

Cache states:

- `ok` — parsed provider response is stored;
- `error` — a provider failure is recorded with a bounded real-time retry cooldown.

A cache error is operational evidence only. It must not become a character-visible event, memory or mental state.

## Normalization into W1

Each selected provider hour becomes a normal `environment_states` record.

Normalization includes:

- WMO weather code -> generic W1 condition;
- temperature -> Celsius;
- precipitation/rain/snow -> precipitation kind + bounded intensity;
- wind speed -> metres/second;
- visibility -> kilometres;
- cloud cover -> 0..1;
- `is_day` -> daylight state;
- bounded light level derived from day/night + cloud cover.

The original provider and cache provenance remain metadata/source fields.

Provider normalization may not write:

- mood;
- motivation;
- anxiety;
- preferences;
- thoughts;
- memories;
- goals;
- intentions;
- plans;
- actions.

## Runtime update ownership

The Observer service loop owns **weather synchronization**, not a character and not the LLM.

Before an autonomous actor tick, the service asks the provider adapter to ensure that the W1 environment state covering the current universe simulation hour exists.

The adapter is lazy and idempotent:

1. if a suitable W1 state already covers the simulation time, do nothing;
2. otherwise read the date cache;
3. if cache is absent/stale, fetch the historical date once;
4. select and normalize the requested simulation hour;
5. publish the corresponding W0 ambient stimulus for represented outdoor descendants.

This makes weather follow simulation time even when simulation time advances faster, slower or independently from real time.

## Failure and future-date policy

Historical data may be unavailable because:

- network/API service is unavailable;
- provider returns an invalid/incomplete response;
- simulation time is ahead of the provider's available historical range.

V1 fallback is deliberately marked synthetic.

Fallback order:

1. keep/use an already valid exact W1 state if one exists;
2. use the cached exact provider day if available;
3. otherwise produce a deterministic seasonal-continuity fallback state when fallback is enabled.

Synthetic fallback state must carry source/metadata that clearly identifies it as procedural fallback. It must never be mislabeled historical truth.

When exact historical data later becomes available, an exact provider state may supersede the fallback for that hour.

## Deterministic procedural fallback

The fallback exists for continuity, not as the preferred weather source.

Properties:

- deterministic for the same provider/geographic anchor/simulation hour;
- season-aware at a coarse level;
- continuity-biased rather than independent random rolls;
- bounded to the existing W1 vocabulary;
- explicitly `synthetic=true` in metadata.

It is not presented as meteorological reconstruction.

No external API failure may stop core simulation autonomy.

## W0 exposure boundary

Creating/updating W1 weather is not character exposure.

W1 publishes an environmental W0 stimulus only to represented locations explicitly marked outdoor.

Actual character exposure remains a separate operation and requires the actor to be at a represented outdoor location during the active state.

Indoor actors do not receive direct ambient weather merely because the Estate geographically has weather.

Future mediated weather knowledge follows separate information channels:

`weather/forecast information -> represented phone/TV/computer/network -> information stimulus -> exposure -> perception`

A character indoors does not magically know the current weather just because the provider fetched it.

## Historical weather vs forecast information

Two different concepts must remain separate:

### Environment truth

Historical replay data represents the external environmental baseline used by W1.

### Forecast/media knowledge

A weather forecast visible on a phone, TV or website is information content. It belongs to the future Information / Media foundation and must reach a character through represented device/media exposure.

Do not use a forecast API response as automatic character knowledge.

## Determinism and replay

For a cached historical date:

- same simulation hour -> same normalized state;
- repeated service ticks do not generate new weather states;
- repeated reads do not create exposure;
- provider/network availability does not alter already cached historical replay.

The normalized state id is stable for provider + hour.

## Security and operational constraints

- no provider credential is required in v1;
- endpoint comes from repository configuration;
- provider HTTP timeout is bounded;
- failures are caught at the environment adapter boundary;
- weather failure must not crash the autonomy service loop;
- raw responses are data, never executable code;
- no provider response gains action/state mutation authority outside W1 normalization.

## Testing contract

Acceptance should prove:

1. simulation date/time, not wall clock, determines provider selection;
2. provider payload normalizes correctly into W1;
3. WMO conditions and units map deterministically;
4. daily cache prevents repeated network fetches;
5. repeated same-hour synchronization is idempotent;
6. outdoor W0 stimulus publication still follows W1 rules;
7. provider failure cannot directly mutate Mind, Memory or actions;
8. fallback is deterministic and explicitly synthetic;
9. a second character requires no provider-specific policy;
10. no exact Estate coordinate/address is invented by the provider.

## Non-goals v1

Not included:

- live current-real-world weather synchronization;
- exact fictional Estate geocoding;
- weather forecasts as character knowledge;
- full climate simulation;
- local microclimate/indoor HVAC modeling;
- lightning/fire/flood hazard engines;
- weather-driven mood modifiers;
- continuous API polling;
- character-specific weather preference rules.

## Future extension sockets

Later work can add without changing this foundation:

- exact Estate coordinate once canonically defined;
- alternate historical providers;
- high-resolution archived forecast replay;
- forecast/media information through devices;
- indoor climate/HVAC;
- deterministic weather affordance constraints;
- observer weather UI;
- richer procedural forward-weather model for simulation dates beyond real historical coverage.

All extensions must continue to reference both:

- `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`
- `docs/HISTORICAL_WEATHER_PROVIDER_V1.md`

and, when cognition-facing, the W0 and Mind Engine contracts.
