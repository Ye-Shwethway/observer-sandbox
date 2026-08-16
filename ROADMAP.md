# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-16

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve the composable runtime and the separation of world truth, exposure, perception, memory, Mind and action authority.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Character-specific behavioral hard-coding is forbidden.
- Persistent repository branches are only `main` and `test`; normal development occurs on `test` and is promoted to `main` after validation.

## Current production checkpoint

**Creator Universe Weather & Geography Observability v1 is COMPLETE / DEPLOYED on top of W1.1.**

Latest evidence:
- PR #222 — `Add Telegram Universe Weather and Geography Observability v1`
- final tested head `6b97919f3697e8fddc59210740219624aa3cd3bb`
- CI #991 / run `31955921285`: SUCCESS
- Strength Live Cycle Validation v1 #108: SUCCESS
- Inventory Operations v1 Acceptance #45: SUCCESS
- merge `d45b328767d045f5d1ed420a6b69257e96adb075`
- Deploy #258 / run `31956018743`: SUCCESS
- install/configure/restart/verify: SUCCESS
- schema v11
- environment schema v2
- world-input schema v1
- mind schema v1

Underlying W1.1 evidence:
- PR #220 — `Add Historical Weather Replay Provider v1`
- final tested head `3f7dedef03832876c263a97708103053c13e9b0d`
- CI #987 / run `31954748630`: SUCCESS
- merge `f719274598d0c5f21c492a2d20d2eb204e6cfe00`
- Deploy #257 / run `31954905811`: SUCCESS

## Completed foundation stack

The deployed minimum foundation includes:
- Character Profile / Skills and adaptive profile foundations;
- Estate spatial/reachability and outdoor affordance foundation;
- Universal Character Autonomy;
- Character Memory + Semantic Spatial Memory + Human Memory Dynamics;
- Intelligent Mind Engine Foundation v1;
- World Stimulus / Exposure Foundation v1;
- Environment / Weather Foundation v1;
- Historical Weather Provider v1;
- **Creator Universe Weather & Geography Observability v1**.

South Lake Tahoe traversal remains intentionally paused.

## Canonical cognition / world-input chain

Required docs:
- `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
- `docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`
- `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`
- `docs/HISTORICAL_WEATHER_PROVIDER_V1.md`
- `docs/TELEGRAM_UNIVERSE_OBSERVABILITY_V1.md`
- `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
- `docs/HUMAN_MEMORY_DYNAMICS_V1.md`

Preserve:

`world/event truth != stimulus availability != exposure != perception/interpretation != memory != mind state/thought != intention/plan != action proposal != action authority`.

## MIND-F0 — Intelligent Mind Engine Foundation — DEPLOYED

Generic persistence exists for bounded mental cycles, typed mental episodes, persistent/semi-persistent mental artifacts and typed links. It remains behavior-neutral; current autonomy does not automatically create thoughts or plans.

## W0 — World Stimulus / Exposure Foundation — DEPLOYED

Shared external-input boundary:
- `world_stimuli`
- `world_stimulus_scopes`
- `character_exposures`

Eligibility is not exposure; exposure is not perception/belief/memory/thought; exposure never grants action authority.

## W1 — Environment / Weather Foundation — DEPLOYED

Canonical contract: `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`.

Runtime provides authoritative `environment_states`, containment-aware applicability, environmental fields, W0 direct ambient publication, and explicit outdoor exposure boundaries. It has no direct weather-to-mood/action rule.

## W1.1 — Historical Weather Provider — DEPLOYED

Canonical architecture:
- `docs/HISTORICAL_WEATHER_PROVIDER_V1.md`
- `docs/HISTORICAL_WEATHER_PROVIDER_V1_IMPLEMENTATION.md`
- `docs/HISTORICAL_WEATHER_PROVIDER_V1_ACCEPTANCE.md`
- `config/environment/weather.providers.v1.json`

Runtime policy:

`universe sim time -> configured South Lake Tahoe sampling anchor -> Open-Meteo historical archive/cache -> W1 normalized environment state -> W0 direct outdoor stimulus/exposure`.

Key guarantees:
- universe simulation time, not real wall-clock time, chooses the weather hour;
- South Lake Tahoe coordinate is an external weather sampling anchor, not an invented exact Estate location;
- daily cache prevents per-tick API calls;
- provider failure does not stop autonomy;
- deterministic seasonal fallback is explicitly synthetic;
- recovered historical data can supersede fallback;
- raw provider/cache data never becomes character knowledge;
- future forecast/app/TV weather is separate Information/Media content requiring represented device/media exposure.

## Creator Universe observability — DEPLOYED

Canonical contract: `docs/TELEGRAM_UNIVERSE_OBSERVABILITY_V1.md`.

Telegram `/start -> Universe` now exposes:
- `Weather`
- `Regions`
- `Locations`

Weather reads the already represented W1 state for the current simulation time. It is read-only Creator observability and does not fetch the provider, create character exposure, Memory or Mind records.

Observer geography currently displays:

`South Lake Tahoe -> Thorne Estate`

Region and location semantics remain separate:
- Region = geographic context/grouping for Creator observability;
- Location = represented simulation place;
- Travel topology = separate authored movement authority.

The South Lake Tahoe observer hierarchy does **not** insert `loc_south_lake_tahoe` into runtime topology and does not open Estate outward routes. Locations contains Thorne Estate and continues through the existing recursive Estate browser.

Do not add a separate Geography hub until multiple regions/categories make the extra layer useful.

## World element expansion policy

Phones, televisions, radios, computers, internet/network access, accounts, calendars, communication endpoints and similar elements are represented world entities/resources when a concrete feature needs possession/location/access/capability semantics. Do not treat devices/internet as omniscient cognition channels.

## Active phase — remaining minimum World Input producers

### W2 — Commitments / Obligations Foundation — NEXT

Goal: represent factual future obligations before planning so later Mind can distinguish desired actions from expected/promised/scheduled duties.

Minimum target:
- obligation/commitment records;
- appointment, promise, deadline and scheduled-responsibility types;
- start/due simulation times;
- optional represented person/entity/location target;
- status/lifecycle;
- flexibility/reschedulability metadata;
- provenance/source;
- W0 reminder/notice production where represented;
- no automatic Mind concern, intention or plan creation.

Potential world expansion only when required:
- calendar/reminder representation;
- communication endpoint/source for externally delivered commitments;
- devices if a concrete reminder/delivery path requires them.

Keep commitment truth separate from reminder exposure and separate again from mental prioritization.

### W3 — Money / Economy Minimum Foundation

Minimum target: balances/resources, transactions, income/expenses/obligations, deterministic affordability, financial notices through W0, no direct anxiety/behavior modifier.

### W4 — Information / Media Foundation

Minimum target: information/media items, sources/publishers, publication/availability, credibility metadata, represented device/media exposure through W0, and `world knows != character knows`.

### W5 — Communication Exposure Foundation

Minimum target: sender/recipient/channel/content/delivery boundary, message/utterance stimulus creation, actual read/heard exposure, and later interpretation/response through Social Cognition rather than direct chatbot ping-pong.

## Mind sequence after minimum world inputs

- MIND-F2 Mental Episode Runtime
- MIND-F3 Attention / Appraisal / Active Concerns
- MIND-F4 Intention Foundation
- MIND-F5 Planning
- MIND-F6 Social Cognition / Communication
- MIND-F7 Relationship Adaptation

No continuous per-minute LLM thought polling. Plans remain interruptible and never bypass deterministic action validation.

## Universal autonomy semantic lock

Character-specific factual seeds are allowed. Character-specific behavioral scripts, world-input interpretations, mental scripts, destination steering or bespoke autonomy prompts are not.

## World / spatial lock

Current Estate boundary remains closed: no public-road edge from Main Security Gate, no Tahoe-backcountry edge from Concealed Forest Passage, and no water-travel edge from Hidden Dock.

## Current exact resume point

**Creator Universe observability is deployed over W1.1. Implement W2 Commitments / Obligations Foundation next on `test`, aligned with W0 and the Mind Engine contract. Expand calendars/devices/communication endpoints only when a concrete W2 consumer requires them. Do not activate Mental Episode/Planning yet.**
