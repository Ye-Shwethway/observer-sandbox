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

**Weather Region Registry v1 is COMPLETE / DEPLOYED.**

Evidence:
- PR #225 — region-registry weather implementation
- final tested head `107f280eb209c0f63250cb53fcd1b655f3ec01fb`
- CI #994 / run `31957231935`: SUCCESS
- Strength Live Cycle #109: SUCCESS
- merge `6635e5809b80dd853035821976aebc311ccd92f2`
- Deploy #260 surfaced invalid live missing-location state during final verification after service/status succeeded
- PR #226 — generic missing actor location recovery
- final tested head `97c7820a0d28a390e94db72801679d0ca24d4158`
- CI #995 / run `31957745143`: SUCCESS
- merge `e1fdf4932bafe63e93408aec0dcb850898461bbf`
- **Deploy #261 / run `31957822826`: SUCCESS**
- schema v11; environment schema v2; world-input schema v1; mind schema v1

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
- **Weather Region Registry v1**

South Lake Tahoe traversal remains intentionally paused.

## Canonical cognition / world-input chain

Required docs:
- `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
- `docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`
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

A future arbitrary Earth search is permitted only as a Creator reference utility. Search results must not automatically create represented geography, W1 state, W0 stimulus, knowledge or travel topology.

The existing Tahoe-calibrated synthetic fallback must not be silently reused for a different climate; a future region needs a suitable fallback profile or fallback disabled.

## Creator Universe observability — DEPLOYED

Telegram `/start -> Universe` exposes Weather, Regions and Locations. Weather is registry-driven and DB-only. Regions currently show South Lake Tahoe -> Thorne Estate while travel topology stays Estate-only. Character Update notifications show current local represented weather from DB without provider fetch or cognition mutation.

## Runtime location invariant

Characters participating in runtime simulation require a current physical location. Startup recovery preserves valid state; otherwise it prefers latest represented action place and uses canonical world start only as the selected default actor's final seed fallback. This closes the live invalid-state failure surfaced by Deploy #260 and verified green in Deploy #261.

## World element expansion policy

Phones, televisions, radios, computers, internet/network access, accounts, calendars, communication endpoints and similar elements become represented world entities/resources when a concrete feature needs possession/location/access/capability semantics. Devices/internet are never omniscient cognition channels.

## Active phase — remaining minimum World Input producers

### W2 — Commitments / Obligations Foundation — NEXT

Goal: represent factual future obligations before planning so later Mind can distinguish desired actions from expected/promised/scheduled duties.

Minimum target:
- obligation/commitment records
- appointment, promise, deadline and scheduled-responsibility types
- start/due simulation times
- optional represented person/entity/location target
- status/lifecycle
- flexibility/reschedulability metadata
- provenance/source
- W0 reminder/notice production where represented
- no automatic Mind concern, intention or plan creation

Potential expansion only when required:
- calendar/reminder representation
- communication endpoint/source for externally delivered commitments
- device representation for a concrete delivery path.

Keep commitment truth separate from reminder exposure and separate again from mental prioritization.

### W3 — Money / Economy Minimum Foundation

Balances/resources, transactions, income/expenses/obligations, deterministic affordability and financial notices through W0; no direct anxiety/behavior modifier.

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

**Weather Region Registry v1 is production-green through Deploy #261. Implement W2 Commitments / Obligations Foundation next on `test`, aligned with W0 and the Mind Engine contract. Expand calendars/devices/communication endpoints only when a concrete W2 consumer requires them. Do not activate Mental Episode/Planning yet.**
