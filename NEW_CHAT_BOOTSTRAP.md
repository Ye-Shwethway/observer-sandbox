# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-16

## Startup / authority

Read and reconcile in order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical docs/source
5. verified production before runtime implementation decisions.

Authority:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

Persistent branches are only `main` and `test`.

Default workflow:
`develop on test -> focused tests + final PR CI -> merge test into main -> automatic deploy when runtime-affecting -> production verification -> sync test to final main checkpoint`.

Do not create per-slice `agent/*` branches unless the Creator explicitly approves an exceptional isolation need.

## Current canonical checkpoint

**Weather Region Registry v1 is COMPLETE / DEPLOYED on top of W1.1 and Creator Universe observability.**

Latest production evidence:
- PR #225 — `Make Universe weather region-registry driven`
- final tested head `107f280eb209c0f63250cb53fcd1b655f3ec01fb`
- CI #994 / run `31957231935`: SUCCESS
- Strength Live Cycle #109: SUCCESS
- merge `6635e5809b80dd853035821976aebc311ccd92f2`
- Deploy #260 / run `31957363286`: final verification exposed pre-existing invalid missing actor location after service/status had succeeded
- PR #226 — `Recover invalid missing actor locations at startup`
- final tested head `97c7820a0d28a390e94db72801679d0ca24d4158`
- CI #995 / run `31957745143`: SUCCESS
- merge `e1fdf4932bafe63e93408aec0dcb850898461bbf`
- **Deploy #261 / run `31957822826`: SUCCESS**
- production sync/install/configure/restart/status/final character verification: SUCCESS
- schema remains **v11**
- environment schema remains **v2**
- world-input schema remains **v1**
- mind schema remains **v1**

## Required cognition / world-input read order

1. `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
2. `docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`
3. `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`
4. `docs/HISTORICAL_WEATHER_PROVIDER_V1.md`
5. `docs/WEATHER_REGION_REGISTRY_V1.md`
6. `docs/TELEGRAM_UNIVERSE_OBSERVABILITY_V1.md`
7. `docs/HUMAN_MEMORY_DYNAMICS_V1.md`
8. `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
9. task-relevant world/profile/runtime docs only.

## Canonical layer separation

Preserve:

`world/event truth != stimulus availability != character exposure != perception != memory != mind/thought != intention/plan != action proposal != action authority`.

MIND-F0 remains behavior-neutral. Current autonomy does not automatically create thoughts or plans.

## W0 / W1 / W1.1 status

- W0 World Stimulus / Exposure Foundation: DEPLOYED.
- W1 Environment / Weather Foundation: DEPLOYED.
- W1.1 Historical Weather Provider: DEPLOYED.
- Weather Region Registry v1: DEPLOYED.

Weather runtime now follows:

`represented region -> registered enabled provider -> universe sim-time coordinate/date query -> daily cache -> W1 environment state -> W0 ambient boundary`.

Open-Meteo capability is global, but only explicitly represented/registered regions become universe weather state. Earth-wide data is not preloaded.

At the current world boundary only **South Lake Tahoe** is registered. Future represented regions can add a geography/provider pair without adding a region-name branch to the service or Creator Weather UI.

A future arbitrary-Earth weather search may exist as a **Creator reference-only** utility. Search results must not create geography, W1 state, W0 stimulus, character knowledge or travel authority.

## Creator Universe observability

Telegram `/start -> Universe` exposes:
- `Weather`
- `Regions`
- `Locations`

Weather is DB-only and registry-driven; opening it never performs a live provider fetch.

Observer geography currently presents:
`South Lake Tahoe -> Thorne Estate`

This remains regional context only. `loc_south_lake_tahoe` is not inserted into runtime topology and no public-road/backcountry/water traversal is open.

Proactive `CHARACTER UPDATE` notifications also show the focused character's current represented-location weather from DB only.

## Runtime location invariant

A represented actor with no current location is invalid runtime state, not a movement phase. Startup recovery:
1. leaves valid locations unchanged;
2. if missing, prefers the actor's latest represented action `place_id`;
3. only for the selected default actor with no runtime evidence, uses canonical world start as last-resort seed recovery.

This repair exists because Deploy #260 surfaced a live null/missing location; Deploy #261 proved the repaired production state and final observer verification green.

## Device / internet weather rule

Direct ambient weather requires no device. Forecasts, alerts, phone widgets, TV reports, websites and internet weather services are Information/Media producers and later require represented access/exposure.

Preserve:
`weather exists != forecast publication != device/service availability != character exposure != character belief`.

## Next world-input sequence

Completed:
1. W0 World Stimulus / Exposure Foundation
2. W1 Environment / Weather Foundation
3. W1.1 Historical Weather Provider
4. Creator Universe Weather & Geography Observability
5. Weather Region Registry v1

Next:
6. **W2 Commitments / Obligations Foundation**
7. W3 Money / Economy Minimum Foundation
8. W4 Information / Media Foundation
9. W5 Communication Exposure Foundation
10. MIND-F2 Mental Episode Runtime after minimum external-input foundations are sufficient.

## W2 direction

Commitments/obligations represent factual future expectations without automatically becoming intentions/plans.

Minimum scope:
- appointment / promise / deadline / scheduled obligation facts;
- start/due simulation time;
- represented target/person/location where applicable;
- status/lifecycle and flexibility;
- source/provenance;
- reminder/notice production through W0 when represented;
- no automatic Mind concern/intention/plan creation.

Expand calendars/devices/communication endpoints only when a concrete W2 delivery path requires them.

## Estate boundary

Estate-first scope remains active. South Lake Tahoe/public-road/backcountry/water traversal remains paused.

## Exact resume point

**Weather Region Registry v1 is production-green through Deploy #261. Build W2 Commitments / Obligations Foundation next on `test`, aligned with W0 + Mind. Do not activate Mental Episode/Planning runtime yet.**
