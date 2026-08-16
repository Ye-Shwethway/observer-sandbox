# Weather Region Registry v1

Status: **COMPLETE / DEPLOYED**

## Purpose

Remove the South Lake Tahoe single-region assumption from weather synchronization and Creator observability without expanding travel geography or turning arbitrary Earth weather lookups into universe state.

## Canonical distinction

Preserve:

`global provider capability != represented region != registered regional weather != character exposure/knowledge`

Open-Meteo can answer coordinate/date queries globally. Observer Sandbox only creates authoritative W1 weather for regions explicitly represented in the universe geography registry and linked to an enabled provider.

## Registry join

Creator geography remains in `config/worlds/geography.observer.v1.json`. Each represented region may declare `weather_provider_id`.

Weather providers remain in `config/environment/weather.providers.v1.json`. Each provider declares a stable id, enabled state, `region_id`, provider/mode/endpoint, represented W1 `scope_location_id`, geographic sampling anchor, hourly variables, cache policy and fallback policy.

The geography region id and provider `region_id` must agree before the pair is registered.

## Runtime synchronization

The world service reads one shared universe simulation time and synchronizes every enabled configured weather provider independently:

`universe sim time -> provider coordinate/date -> provider daily cache -> normalized W1 state -> W0 ambient publication`

A provider failure is isolated to that provider. It must not stop another region or actor autonomy. Provider-local caches and state ids remain namespaced by provider id.

## Creator Weather view

`/start -> Universe -> Weather` is registry-driven and DB-only. It never performs a live provider fetch on button press.

For every represented region with a valid enabled provider link it shows the region, sampling anchor, condition/temperature, precipitation, wind/visibility, cloud/daylight, historical-versus-synthetic provenance, and validity window.

At the current world boundary only South Lake Tahoe is registered, so only one regional block is shown today. Adding a future represented region/provider pair does not require a region-name code branch in the service loop or Creator Weather view.

## Future region addition

A future represented region joins weather runtime by adding:
1. a geography region record with `weather_provider_id`;
2. a matching enabled provider record with `region_id`, coordinate anchor and W1 scope location.

A non-Tahoe region should disable the current Tahoe-calibrated deterministic fallback unless/until it has an explicitly suitable fallback profile. Exact historical replay remains generic by coordinates.

## Arbitrary Earth lookup boundary

A future Creator utility may geocode/search an arbitrary Earth place and request historical weather for the current universe date/time. That result must be clearly **reference-only** and must not create a represented region, W1 state, W0 stimulus, character knowledge or travel topology unless geography is separately admitted into the simulation.

Do not preload Earth-wide weather locally. Use coordinate/date queries and bounded on-demand cache.

## Geography/travel safety

This registry does not create `loc_south_lake_tahoe`, public roads, backcountry travel or lake travel. Region presentation remains separate from authored movement authority.

## Production evidence

Weather Region Registry implementation:
- PR #225 — `Make Universe weather region-registry driven`
- final tested head `107f280eb209c0f63250cb53fcd1b655f3ec01fb`
- CI #994 / run `31957231935`: SUCCESS
- Strength Live Cycle Validation v1 #109: SUCCESS
- merge `6635e5809b80dd853035821976aebc311ccd92f2`
- Deploy #260 / run `31957363286`: FAILED only in final production verification because the live default actor had invalid missing-location state; service restart/status and registry code had already succeeded.

Production location-invariant repair:
- PR #226 — `Recover invalid missing actor locations at startup`
- final tested head `97c7820a0d28a390e94db72801679d0ca24d4158`
- CI #995 / run `31957745143`: SUCCESS
- Technology Diagnostic #44, Skill Progression #75, Skill Evidence #53, Inventory Foundation #73: SUCCESS
- merge `e1fdf4932bafe63e93408aec0dcb850898461bbf`
- Deploy #261 / run `31957822826`: **SUCCESS**
- production sync/install/configure/restart/status/final character verification: **SUCCESS**

The recovery preserves valid locations, otherwise prefers the actor's latest represented action place, and only uses the canonical world start as the selected default actor's last-resort seed fallback when no represented location evidence exists.
