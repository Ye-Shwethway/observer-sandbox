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

**W1.1 — Historical Weather Provider v1 is COMPLETE / DEPLOYED.**

Latest runtime evidence:
- PR #220 — `Add Historical Weather Replay Provider v1`
- final tested PR head: `3f7dedef03832876c263a97708103053c13e9b0d`
- CI #987 / run `31954748630`: SUCCESS
- merge: `f719274598d0c5f21c492a2d20d2eb204e6cfe00`
- Deploy #257 / run `31954905811`: SUCCESS
- deployment verification (`sync -> install/configure cognition -> restart -> verify`): SUCCESS
- schema: **v11**
- environment schema: **v2**
- world-input schema: **v1**
- mind schema: **v1**

Two production-copy acceptance jobs during PR validation failed only at their SSH configuration step before validators ran; final full CI and the normal production deploy were green.

## Required cognition / world-input read order

1. `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
2. `docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`
3. `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`
4. `docs/HISTORICAL_WEATHER_PROVIDER_V1.md`
5. `docs/HUMAN_MEMORY_DYNAMICS_V1.md`
6. `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
7. task-relevant world/profile/runtime docs only.

## Canonical layer separation

Preserve:

`world/event truth != stimulus availability != character exposure != perception != memory != mind/thought != intention/plan != action proposal != action authority`.

The Mind Engine remains the shared actor-owned cognition substrate. MIND-F0 is still behavior-neutral: current autonomy does not automatically generate mental cycles/thoughts and no planner is active.

## W0 — World Stimulus / Exposure Foundation

Deployed generic persistence:
- `world_stimuli`
- `world_stimulus_scopes`
- `character_exposures`

World existence is not character knowledge; eligibility is not exposure; exposure is not perception, belief, memory, thought or behavior.

## W1 — Environment / Weather Foundation v1

Canonical contract: `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`.

Deployed authoritative state:
- `environment_states`
- weather condition, temperature, precipitation, wind, visibility, cloud cover and daylight/light;
- containment-aware applicability;
- direct ambient W0 stimulus publication only to explicitly outdoor represented locations;
- indoor geographic weather truth remains separate from direct physical exposure;
- no direct mood, Mind, Memory, relationship or action mutation.

Canonical W1 flow:

`environment truth -> location applicability -> W0 environment stimulus -> actual direct outdoor exposure -> future perception/appraisal -> Mind`.

## W1.1 — Historical Weather Provider v1

Canonical architecture:
- `docs/HISTORICAL_WEATHER_PROVIDER_V1.md`
- `docs/HISTORICAL_WEATHER_PROVIDER_V1_IMPLEMENTATION.md`
- `docs/HISTORICAL_WEATHER_PROVIDER_V1_ACCEPTANCE.md`
- `config/environment/weather.providers.v1.json`

The service loop now owns world-weather synchronization. It uses **universe simulation time**, not the host/real-world clock.

Primary flow:

`universe UTC sim hour -> South Lake Tahoe city-area sampling anchor -> Open-Meteo Historical Weather archive -> daily cache -> normalized W1 state -> W0 outdoor stimulus/exposure boundary`.

Important rules:
- the configured coordinate is a South Lake Tahoe city-area weather sampling anchor, **not** a canonical exact Estate address/coordinate;
- provider data is normalized into W1 before use;
- successful provider days are cached locally, so the service does not call the API on every autonomy wake;
- same universe hour is idempotent;
- provider failure cannot stop autonomy;
- when historical data is unavailable, a deterministic seasonal fallback may keep weather continuity, but it is explicitly `synthetic=true` and never mislabeled historical truth;
- after retry cooldown/recovery, exact historical data can supersede a synthetic fallback;
- raw provider/cache data is not character knowledge;
- forecasts/weather apps/TV reports remain future Information/Media content and require represented device/network/media exposure.

## Device / internet weather rule

Direct ambient weather requires no device.

Forecasts, alerts, phone weather widgets, TV reports, websites or internet weather services are **information/media** producers, not ambient environment truth. Preserve:

`weather exists != forecast publication != device/service availability != character exposure != character belief`.

Add devices/network/services only when a concrete consumer needs them.

## Memory / Mind rules remain authoritative

Exposure is not memory. Thought is not automatically memory. Prospective thought is not automatically intention or plan.

External facts should eventually flow:

`authoritative fact -> stimulus -> exposure -> perception -> character-relative appraisal -> mental episode/artifact -> possible intention/action`.

## Next world-input sequence

Completed:
1. W0 World Stimulus / Exposure Foundation
2. W1 Environment / Weather Foundation
3. W1.1 Historical Weather Provider

Next:
4. **W2 Commitments / Obligations Foundation**
5. W3 Money / Economy Minimum Foundation
6. W4 Information / Media Foundation
7. W5 Communication Exposure Foundation
8. MIND-F2 Mental Episode Runtime after minimum external-input foundations are sufficient.

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

**W1.1 Historical Weather Provider v1 is deployed. Build W2 Commitments / Obligations Foundation next on `test`, aligned with W0 + Mind. Do not activate Mental Episode/Planning runtime yet.**
