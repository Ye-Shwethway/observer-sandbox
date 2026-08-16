# Weather Region Registry v1

Status: IMPLEMENTED — PENDING FINAL CI / DEPLOY

## Purpose

Remove the South Lake Tahoe single-region assumption from weather synchronization and Creator observability without expanding travel geography or turning arbitrary Earth weather lookups into universe state.

## Canonical distinction

Preserve:

`global provider capability != represented region != registered regional weather != character exposure/knowledge`

Open-Meteo can answer coordinate/date queries globally. Observer Sandbox only creates authoritative W1 weather for regions explicitly represented in the universe geography registry and linked to an enabled provider.

## Registry join

Creator geography remains in:

`config/worlds/geography.observer.v1.json`

Each represented region may declare:

`weather_provider_id`

Weather providers remain in:

`config/environment/weather.providers.v1.json`

Each provider declares:
- stable provider id;
- `enabled` state;
- `region_id`;
- provider/mode/endpoint;
- represented W1 `scope_location_id`;
- geographic sampling anchor;
- hourly variables/cache/fallback policy.

The region id and provider region id must agree before the Creator Weather screen treats the pair as registered.

## Runtime synchronization

The world service reads one shared universe simulation time and synchronizes every enabled configured weather provider independently.

For each provider:

`universe sim time -> provider coordinate/date -> provider daily cache -> normalized W1 state -> W0 ambient publication`

A provider failure is isolated to that provider. It must not stop another region or actor autonomy.

The existing historical provider implementation remains provider-local, so daily caches and state ids are already namespaced by provider id.

## Creator Weather view

`/start -> Universe -> Weather` is registry-driven.

It reads already represented DB weather only. It never performs a live provider fetch on button press.

For every represented region with a valid enabled provider link it shows:
- region name;
- sampling anchor;
- condition and temperature;
- precipitation;
- wind and visibility;
- cloud/daylight state;
- historical versus synthetic provenance;
- represented validity window.

At the current world boundary only South Lake Tahoe is registered, so only one regional block is shown today.

## Future region addition

A future represented region can join the weather runtime by adding:
1. a geography region record with `weather_provider_id`;
2. a matching enabled provider record with `region_id`, coordinate anchor and W1 scope location.

The service synchronization loop and Creator Weather view do not require a region-name code branch.

A non-Tahoe region should disable the current Tahoe-calibrated deterministic fallback unless/until it has an explicitly suitable fallback profile. Exact historical provider replay remains generic by coordinates.

## Arbitrary Earth lookup boundary

A future Creator utility may geocode/search an arbitrary Earth place and request historical weather for the current universe date/time. That result must be clearly labeled **reference-only** and must not create a represented region, W1 state, W0 stimulus, character knowledge or travel topology unless the geography is separately admitted into the simulation.

Do not preload Earth-wide weather into the local database. Use coordinate/date queries and bounded cache on demand.

## Geography/travel safety

This registry does not create `loc_south_lake_tahoe`, public roads, backcountry travel or lake travel. Region presentation remains separate from authored movement authority.
