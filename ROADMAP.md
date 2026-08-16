# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-16

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve the separation of world truth, exposure, perception, memory, Mind and action authority.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Character-specific behavioral hard-coding is forbidden.
- Persistent branches are only `main` and `test`; normal development occurs on `test` and is promoted to `main` after validation.

## Current production checkpoint

**W2 Commitments / Obligations Foundation v1 is COMPLETE / DEPLOYED.**

Latest evidence:
- Telegram physiology presentation repair:
  - PR #228
  - CI #996 / run `31958374868`: SUCCESS
  - merge `088728fcabd6fa624a97ec81c2f128df6afa1e34`
  - Deploy #262 / run `31958476747`: SUCCESS
- W2 implementation:
  - PR #229 — `Add W2 Commitments and Obligations Foundation v1`
  - final tested head `a985c5b63ce8371544306ffc321f2cb34030dd03`
  - final CI #999 / run `31958910987`: SUCCESS
  - merge `0a24e7e700abf2c1e0fffcb8047a05f3f04c1891`
  - **Deploy #263 / run `31959001632`: SUCCESS**
- schema v12; commitment schema v1; environment schema v2; world-input schema v1; mind schema v1.

The first W2 CI run (#997) had 696 passing tests and one stale historical-weather expectation pinned to main schema v11. The compatibility assertion was corrected to follow `SCHEMA_VERSION`; W2 behavior was not the failure.

## Completed foundation stack

Deployed:
- Character Profile / Skills and adaptive profile foundations
- Estate spatial/reachability and outdoor affordance foundation
- Universal Character Autonomy
- Character Memory + Semantic Spatial Memory + Human Memory Dynamics
- Intelligent Mind Engine Foundation v1
- W0 World Stimulus / Exposure Foundation
- W1 Environment / Weather Foundation
- W1.1 Historical Weather Provider
- Creator Universe Weather & Geography Observability
- Weather Region Registry v1
- **W2 Commitments / Obligations Foundation v1**

South Lake Tahoe traversal remains intentionally paused.

## Canonical cognition / world-input chain

Required docs:
- `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
- `docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`
- `docs/COMMITMENTS_OBLIGATIONS_FOUNDATION_V1.md`
- `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`
- `docs/HISTORICAL_WEATHER_PROVIDER_V1.md`
- `docs/WEATHER_REGION_REGISTRY_V1.md`
- `docs/TELEGRAM_UNIVERSE_OBSERVABILITY_V1.md`
- `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
- `docs/HUMAN_MEMORY_DYNAMICS_V1.md`

Preserve:
`world/event truth != stimulus availability != exposure != perception/interpretation != memory != mind state/thought != intention/plan != action proposal != action authority`.

## MIND-F0 — Intelligent Mind Engine Foundation — DEPLOYED

Generic persistence exists for bounded mental cycles, typed mental episodes, persistent/semi-persistent mental artifacts and typed links. It remains behavior-neutral; current autonomy does not automatically create thoughts or plans.

## W0 — World Stimulus / Exposure — DEPLOYED

Shared external-input boundary: `world_stimuli`, `world_stimulus_scopes`, `character_exposures`. Eligibility is not exposure; exposure is not perception/belief/memory/thought and grants no action authority.

## W1 / W1.1 Weather — DEPLOYED

W1 stores authoritative environment state and publishes direct ambient W0 stimuli only through represented outdoor exposure boundaries. No direct weather-to-mood/action rule exists.

W1.1 uses universe simulation time with Open-Meteo historical replay, bounded daily cache, and explicit deterministic synthetic fallback when historical data is unavailable.

## Weather Region Registry — DEPLOYED

Canonical contract: `docs/WEATHER_REGION_REGISTRY_V1.md`.

Runtime policy:
`represented region -> enabled registered provider -> universe sim-time coordinate/date query -> provider cache -> W1 state -> W0 ambient boundary`.

Current registered region:
- South Lake Tahoe -> Open-Meteo historical provider -> Thorne Estate W1 scope.

The provider capability is global, but Earth-wide weather is not preloaded. Adding a future represented region requires a geography record and matching provider record; service synchronization and Creator Weather rendering are not region-name hard-coded.

## Creator Universe observability — DEPLOYED

Telegram `/start -> Universe` exposes Weather, Regions and Locations. Weather is registry-driven and DB-only. Regions currently show South Lake Tahoe -> Thorne Estate while travel topology stays Estate-only. Character Update notifications show current local represented weather from DB without provider fetch or cognition mutation.

Core Character Update physiology rows are now stable Creator-facing presentation: Energy, Fatigue, Hunger, Thirst, Sleepiness and Cleanliness remain visible even when a value has zero or sub-display-threshold change.

## W2 — Commitments / Obligations Foundation — DEPLOYED

Canonical contract: `docs/COMMITMENTS_OBLIGATIONS_FOUNDATION_V1.md`.

W2 represents factual future expectations before planning. Initial generic types:
- appointment;
- promise;
- deadline;
- scheduled responsibility.

Commitment truth supports start/due simulation times, optional represented entity/location targets, lifecycle status, flexibility/reschedulability, provenance and metadata.

Canonical W2 separation:
`commitment truth != reminder/notice stimulus != exposure != perception/interpretation != concern/intention/plan != action proposal != action authority`.

An explicit W2 notice can publish a character-scoped W0 `obligation` stimulus. Foundation notices remain availability-only and do not automatically create exposure, Character Memory, Mind artifacts, intentions, plans or action authority. Terminal commitments retire linked active notices.

No calendar, phone, alarm or communication endpoint is prebuilt. Add those only when a concrete delivery path needs represented possession/location/access/capability semantics.

## World element expansion policy

Phones, televisions, radios, computers, internet/network access, accounts, calendars, communication endpoints and similar elements become represented world entities/resources when a concrete feature needs possession/location/access/capability semantics. Devices/internet are never omniscient cognition channels.

## Active phase — remaining minimum World Input producers

### W3 — Money / Economy Minimum Foundation — NEXT

Goal: represent minimum authoritative financial truth and deterministic affordability without allowing economy state to directly script emotion, cognition or behavior.

Minimum direction:
- represented balance/resource/account facts where needed;
- transactions with source/provenance;
- income/expense/payable facts where required;
- deterministic affordability/resource checks owned by the relevant domain/runtime;
- explicit financial notices through W0 when represented;
- no direct mood/anxiety/action-selection modifier;
- no automatic Memory/Mind concern/intention/plan creation.

Potential expansion only when required:
- represented accounts or payment instruments;
- economic counterparties;
- devices/interfaces needed for a concrete financial-information exposure path.

### W4 — Information / Media Foundation

Information/media items, sources/publishers, publication/availability, credibility metadata, represented device/media exposure through W0, and `world knows != character knows`.

### W5 — Communication Exposure Foundation

Sender/recipient/channel/content/delivery boundary, message/utterance stimulus creation, actual read/heard exposure, and later interpretation/response through Social Cognition.

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

**W2 Commitments / Obligations Foundation v1 is production-green through Deploy #263. Implement W3 Money / Economy Minimum Foundation next on `test`, aligned with W0 and the Mind Engine contract. Expand accounts/devices/economic actors only when a concrete W3 consumer requires them. Do not activate Mental Episode/Planning yet.**
