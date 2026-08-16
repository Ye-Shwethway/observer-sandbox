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

**W3 Money / Economy Foundation v1 and W3.1 Universe Object Valuation & Creation Rules v1 are COMPLETE / DEPLOYED.**

Latest evidence:
- W3:
  - PR #232 — `Add W3 Money Economy Foundation v1`
  - final tested head `b47fe188ea064308a2c83e3b21c4014d3364245d`
  - CI #1001 / run `31961595256`: SUCCESS — 705 passed
  - merge `135fee320c5f137b6f748f312d4105aa00b010e7`
  - Deploy #265 / run `31961742114`: SUCCESS
- W3.1:
  - PR #233 — `Add W3.1 Universe Object Valuation Rules v1`
  - final tested head `68fdb631e828bc4707bce631a19decb3e970ab03`
  - CI #1004 / run `31962052231`: SUCCESS — 710 passed
  - merge `ac07817979a55ca3846e5efee570c56493bd23c3`
  - **Deploy #266 / run `31962148301`: SUCCESS**
- main schema **v14**; economy schema **v2**; commitment schema v1; environment schema v2; world-input schema v1; mind schema v1.

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
- W2 Commitments / Obligations Foundation v1
- **W3 Money / Economy Foundation v1**
- **W3.1 Universe Object Valuation & Creation Rules v1**

South Lake Tahoe traversal remains intentionally paused.

## Canonical cognition / world-input chain

Required docs:
- `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
- `docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`
- `docs/COMMITMENTS_OBLIGATIONS_FOUNDATION_V1.md`
- `docs/MONEY_ECONOMY_FOUNDATION_V1.md`
- `docs/UNIVERSE_OBJECT_VALUATION_RULES_V1.md`
- `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`
- `docs/HISTORICAL_WEATHER_PROVIDER_V1.md`
- `docs/WEATHER_REGION_REGISTRY_V1.md`
- `docs/TELEGRAM_UNIVERSE_OBSERVABILITY_V1.md`
- `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
- `docs/HUMAN_MEMORY_DYNAMICS_V1.md`

Preserve:
`world/event truth != stimulus availability != exposure != perception/interpretation != memory != mind state/thought != intention/plan != action proposal != action authority`.

For economy preserve:
`economic truth != financial notice availability != exposure != perception/interpretation != memory != concern/thought != intention/plan != action proposal != action authority`.

## W0 — World Stimulus / Exposure — DEPLOYED

Shared external-input boundary: `world_stimuli`, `world_stimulus_scopes`, `character_exposures`. Eligibility is not exposure; exposure is not perception/belief/memory/thought and grants no action authority.

## W1 / W1.1 Weather — DEPLOYED

W1 stores authoritative environment state and publishes direct ambient W0 stimuli only through represented outdoor exposure boundaries. W1.1 replays historical weather from universe simulation time with bounded caching and explicit deterministic fallback.

Weather remains registry-driven:
`represented region -> enabled registered provider -> universe sim-time query -> cache -> W1 -> W0`.

Only South Lake Tahoe is currently represented/registered. Telegram Universe Weather/Regions/Locations remains DB-only observer presentation.

## W2 — Commitments / Obligations — DEPLOYED

Commitment truth supports appointment, promise, deadline and scheduled responsibility, with start/due times, lifecycle, flexibility and provenance. Explicit W0 obligation notices remain availability-only and do not create exposure, Memory, Mind, plans or action authority.

## W3 — Money / Economy Foundation — DEPLOYED

Canonical contract: `docs/MONEY_ECONOMY_FOUNDATION_V1.md`.

W3 provides a socket-style financial spine suitable for later Jobs/Careers, companies, governments and broader economy systems without activating those systems yet:
- economic entities;
- financial accounts with integer minor-unit balances;
- immutable transaction headers + signed ledger entries;
- assets;
- liabilities;
- append-only valuations;
- deterministic affordability and same-currency settlement;
- explicit W0 financial notices.

Darian's Creator-approved opening economy seed is **USD 25.0M net worth**:
- Thorne Estate: USD 16.5M;
- investments: USD 6.5M;
- primary liquid holdings: USD 1.8M;
- other personal assets: USD 0.7M;
- liabilities: USD 0.5M.

`net worth != spendable balance`.

The schema is intentionally expandable toward payroll, employment, business ownership, property, investments, debt, markets and later regional/global economy aggregation. Future world-wealth calculations must distinguish real assets, financial claims, liabilities and consolidated net wealth to avoid double counting.

## W3.1 — Universe Object Valuation & Creation Rules — DEPLOYED

Canonical contract: `docs/UNIVERSE_OBJECT_VALUATION_RULES_V1.md`.

Canonical rule:
`has economic value != contributes independent net worth`.

All currently represented object entities and all current item definitions have explicit economic-value policy coverage, including the runtime-seeded training/diagnostic simulator objects discovered by production-copy validation.

Estate fixtures/facilities receive replacement-value truth but use `included_in_parent -> asset_thorne_estate`; they do not inflate Darian's USD 25.0M net worth.

Legacy food/water interaction proxies are excluded from independent value because inventory/resource authorities hold the real stock truth. Current food inventory derives value from live stack quantities and canonical definition unit prices; the current canonical stock value is USD 2,443.50.

Canonical initialization fails closed if a represented `object` or `item` definition is added without an explicit economic-value policy. Future runtime object-creation APIs must use the same policy boundary or atomically create the object and approved policy together.

## World element expansion policy

Phones, televisions, radios, computers, internet/network access, accounts, calendars, communication endpoints and similar elements become represented world entities/resources when a concrete feature needs possession/location/access/capability semantics. Devices/internet are never omniscient cognition channels.

## Active phase — remaining minimum World Input producers

### W4 — Information / Media Foundation — NEXT

Represent information/media truth separately from character knowledge. Minimum direction:
- information/media items;
- sources/publishers;
- publication/availability;
- credibility/provenance metadata;
- represented device/media exposure through W0 when a concrete access path exists;
- `world knows != character knows`;
- no automatic belief, Memory, concern, intention or action authority.

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

**W3 + W3.1 are production-green through Deploy #266. The canonical next minimum World Input slice is W4 Information / Media Foundation on `test`. Do not activate Mental Episode/Planning yet. Broader economy expansion remains socketed for future concrete consumers such as Jobs/Careers rather than being activated preemptively.**
