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

**W2 Commitments / Obligations Foundation v1 is COMPLETE / DEPLOYED.**

Latest production evidence:
- Telegram physiology presentation repair:
  - PR #228 — `Keep core physiology rows visible in Telegram updates`
  - final tested head `9d16cc05c647ad5cb2a6f10f6777daf2ad4cbcfd`
  - CI #996 / run `31958374868`: SUCCESS
  - merge `088728fcabd6fa624a97ec81c2f128df6afa1e34`
  - Deploy #262 / run `31958476747`: SUCCESS
  - Creator `CHARACTER UPDATE` now keeps Energy, Fatigue, Hunger, Thirst, Sleepiness and Cleanliness visible even for zero/sub-display-threshold deltas.
- W2 implementation:
  - PR #229 — `Add W2 Commitments and Obligations Foundation v1`
  - final tested head `a985c5b63ce8371544306ffc321f2cb34030dd03`
  - initial CI #997 exposed one stale historical-weather assertion hard-coded to main schema v11; W2 runtime behavior was not the failure
  - corrected final CI #999 / run `31958910987`: SUCCESS
  - merge `0a24e7e700abf2c1e0fffcb8047a05f3f04c1891`
  - **Deploy #263 / run `31959001632`: SUCCESS**
  - production sync/install/configure/restart/final verification: SUCCESS
- main schema is now **v12**
- commitment schema is **v1**
- environment schema remains **v2**
- world-input schema remains **v1**
- mind schema remains **v1**

Underlying Weather Region Registry v1 remains production-green through Deploy #261.

## Required cognition / world-input read order

1. `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
2. `docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`
3. `docs/COMMITMENTS_OBLIGATIONS_FOUNDATION_V1.md`
4. `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`
5. `docs/HISTORICAL_WEATHER_PROVIDER_V1.md`
6. `docs/WEATHER_REGION_REGISTRY_V1.md`
7. `docs/TELEGRAM_UNIVERSE_OBSERVABILITY_V1.md`
8. `docs/HUMAN_MEMORY_DYNAMICS_V1.md`
9. `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
10. task-relevant world/profile/runtime docs only.

## Canonical layer separation

Preserve:

`world/event truth != stimulus availability != character exposure != perception != memory != mind/thought != intention/plan != action proposal != action authority`.

MIND-F0 remains behavior-neutral. Current autonomy does not automatically create thoughts or plans.

For commitments specifically preserve:

`commitment truth != reminder/notice stimulus != exposure != perception/interpretation != concern/intention/plan != action proposal != action authority`.

## W0 / W1 / W1.1 / W2 status

- W0 World Stimulus / Exposure Foundation: DEPLOYED.
- W1 Environment / Weather Foundation: DEPLOYED.
- W1.1 Historical Weather Provider: DEPLOYED.
- Weather Region Registry v1: DEPLOYED.
- **W2 Commitments / Obligations Foundation v1: DEPLOYED.**

W2 now provides generic factual commitment persistence for:
- appointment;
- promise;
- deadline;
- scheduled responsibility.

Records support start/due simulation times, optional represented entity/location targets, lifecycle status, flexibility/reschedulability, provenance and metadata.

A commitment may explicitly publish a character-scoped W0 `obligation` notice. Foundation notices remain availability-only and use the neutral W0 `other` channel until a concrete calendar/device/delivery path is represented. Publishing a notice does not create exposure, Memory, Mind state, intention, plan or action authority. Terminal commitment states retire linked active notices.

No phone, calendar, alarm or communication endpoint was invented for W2. Expand those only when a concrete producer/consumer needs possession/location/access/capability semantics.

## Weather / geography state

Weather runtime remains:

`represented region -> registered enabled provider -> universe sim-time coordinate/date query -> daily cache -> W1 environment state -> W0 ambient boundary`.

Open-Meteo capability is global, but only explicitly represented/registered regions become universe weather state. At the current world boundary only **South Lake Tahoe** is registered.

Creator Telegram `/start -> Universe` exposes Weather, Regions and Locations. Weather remains registry-driven and DB-only. Observer geography shows `South Lake Tahoe -> Thorne Estate` as regional context only; no public-road/backcountry/water traversal is open.

## Runtime location invariant

A represented actor with no current location is invalid runtime state. Startup recovery leaves valid locations unchanged, otherwise prefers the actor's latest represented action `place_id`, and only for the selected default actor with no runtime evidence uses canonical world start as last-resort seed recovery.

## Next world-input sequence

Completed:
1. W0 World Stimulus / Exposure Foundation
2. W1 Environment / Weather Foundation
3. W1.1 Historical Weather Provider
4. Creator Universe Weather & Geography Observability
5. Weather Region Registry v1
6. **W2 Commitments / Obligations Foundation v1**

Next:
7. **W3 Money / Economy Minimum Foundation**
8. W4 Information / Media Foundation
9. W5 Communication Exposure Foundation
10. MIND-F2 Mental Episode Runtime after minimum external-input foundations are sufficient.

## W3 direction

Represent minimum authoritative financial truth without turning money state into scripted emotion or behavior.

Expected minimum direction:
- character/account/resource balances where actually represented;
- transactions and provenance;
- income/expense or payable facts where needed;
- deterministic affordability/resource checks through domain/runtime authority;
- financial notices through W0 when explicitly represented;
- no direct `low cash -> anxiety` or action-selection modifier;
- no automatic Memory/Mind concern/intention/plan creation.

Expand accounts, payment instruments, devices or economic actors only when a concrete W3 consumer requires them.

## Estate boundary

Estate-first scope remains active. South Lake Tahoe/public-road/backcountry/water traversal remains paused.

## Exact resume point

**W2 Commitments / Obligations Foundation v1 is production-green through Deploy #263. Build W3 Money / Economy Minimum Foundation next on `test`, aligned with W0 + Mind. Do not activate Mental Episode/Planning runtime yet.**
