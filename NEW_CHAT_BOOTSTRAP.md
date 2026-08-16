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

## Current canonical checkpoint

**W3 Money / Economy Foundation v1 and W3.1 Universe Object Valuation & Creation Rules v1 are COMPLETE / DEPLOYED.**

Latest production evidence:
- W3 PR #232 — `Add W3 Money Economy Foundation v1`
  - tested head `b47fe188ea064308a2c83e3b21c4014d3364245d`
  - CI #1001 / run `31961595256`: SUCCESS — 705 passed
  - merge `135fee320c5f137b6f748f312d4105aa00b010e7`
  - Deploy #265 / run `31961742114`: SUCCESS
- W3.1 PR #233 — `Add W3.1 Universe Object Valuation Rules v1`
  - tested head `68fdb631e828bc4707bce631a19decb3e970ab03`
  - CI #1004 / run `31962052231`: SUCCESS — 710 passed
  - merge `ac07817979a55ca3846e5efee570c56493bd23c3`
  - **Deploy #266 / run `31962148301`: SUCCESS**
- main schema **v14**
- economy schema **v2**
- commitment schema v1
- environment schema v2
- world-input schema v1
- mind schema v1

## Required cognition / world-input read order

1. `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
2. `docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`
3. `docs/COMMITMENTS_OBLIGATIONS_FOUNDATION_V1.md`
4. `docs/MONEY_ECONOMY_FOUNDATION_V1.md`
5. `docs/UNIVERSE_OBJECT_VALUATION_RULES_V1.md`
6. `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`
7. `docs/HISTORICAL_WEATHER_PROVIDER_V1.md`
8. `docs/WEATHER_REGION_REGISTRY_V1.md`
9. `docs/TELEGRAM_UNIVERSE_OBSERVABILITY_V1.md`
10. `docs/HUMAN_MEMORY_DYNAMICS_V1.md`
11. `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
12. task-relevant world/profile/runtime docs only.

## Canonical layer separation

Preserve:
`world/event truth != stimulus availability != character exposure != perception != memory != mind/thought != intention/plan != action proposal != action authority`.

Economy specifically:
`economic truth != financial notice availability != exposure != perception/interpretation != memory != concern/thought != intention/plan != action proposal != action authority`.

MIND-F0 remains behavior-neutral. Current autonomy does not automatically create thoughts or plans.

## Deployed World Input stack

- W0 World Stimulus / Exposure Foundation
- W1 Environment / Weather Foundation
- W1.1 Historical Weather Provider
- Creator Universe Weather & Geography Observability
- Weather Region Registry v1
- W2 Commitments / Obligations Foundation v1
- **W3 Money / Economy Foundation v1**
- **W3.1 Universe Object Valuation & Creation Rules v1**

## W3 runtime state

W3 is a minimum active runtime on an expandable economic spine:
- generic economic entities: character, household, company, organization, government, trust, other;
- financial accounts with integer minor-unit balances;
- immutable transaction headers with signed ledger entries;
- assets, liabilities and append-only valuations;
- deterministic affordability/same-currency settlement;
- explicit W0 financial notices only.

No jobs, salaries, banks/cards, interest, taxes, dynamic markets, FX, business P&L or macroeconomic simulation is activated yet. These later systems should plug into W3 rather than replace it.

### Darian economy seed

Creator-approved canonical opening scale:
- Thorne Estate: USD 16.5M
- investments: USD 6.5M
- primary liquid holdings: USD 1.8M
- other personal assets: USD 0.7M
- liabilities: USD 0.5M
- **net worth: USD 25.0M**

`net worth != spendable balance`.

## W3.1 object valuation state

Canonical rule:
`has economic value != contributes independent net worth`.

All currently represented `object` entities and all current inventory `item` definitions have explicit value-policy coverage. Production-copy validation exposed 13 additional runtime-seeded training/diagnostic simulator objects beyond the base world JSON; those are included in the canonical coverage set.

Estate-installed components have replacement-value truth but are `included_in_parent` under `asset_thorne_estate`, so they do not double-count against Darian's USD 25M net worth.

Legacy `Stored Food Provisions`, `Drinking Water` and `Meal Ingredients` objects are excluded resource proxies; actual stock truth is held by inventory/resource authorities.

Current food inventory derives value from live quantities + item-definition unit values. At the deployed canonical seed quantities it totals **USD 2,443.50**. This stock value is not automatically added to Darian's personal net worth.

Canonical initialization fails closed if a represented world object or item definition lacks an explicit economic-value policy. Future runtime object creation must use the same value-policy boundary or atomically create an object and approved policy together.

## Global economy expansion direction

The Creator expects W3 to remain easily expandable toward Jobs/Careers and potentially a full global economy, including later aggregate concepts such as world total wealth.

Future aggregation must distinguish:
- real/non-financial assets;
- financial claims between entities;
- liabilities;
- consolidated net wealth;
- valuation time/method/currency.

Do not sum asset values and corresponding financial claims blindly; prevent macro-level double counting.

## Weather / geography state

Weather remains:
`represented region -> registered provider -> universe sim-time query -> cache -> W1 -> W0`.
Only South Lake Tahoe is currently registered/represented for weather.

Estate-first spatial scope remains active. No public-road edge from Main Security Gate, Tahoe-backcountry edge from Concealed Forest Passage, or water-travel edge from Hidden Dock is open.

## Next world-input sequence

Completed:
1. W0 World Stimulus / Exposure
2. W1 Environment / Weather
3. W1.1 Historical Weather Provider
4. Creator Universe Weather & Geography Observability
5. Weather Region Registry v1
6. W2 Commitments / Obligations
7. W3 Money / Economy Foundation
8. W3.1 Universe Object Valuation & Creation Rules

Next:
9. **W4 Information / Media Foundation**
10. W5 Communication Exposure Foundation
11. MIND-F2 Mental Episode Runtime only after minimum external-input foundations are sufficient.

## W4 direction

Represent information/media truth before interpretation:
- information/media items;
- source/publisher and provenance;
- publication/availability;
- credibility metadata;
- represented access/device/media exposure through W0 when a concrete path exists;
- `world knows != character knows`;
- no automatic belief, Memory, concern, intention, plan or action authority.

## Exact resume point

**W3 + W3.1 are production-green through Deploy #266. Final continuity sync is documentation-only. Once `main`/`test` are synchronized at that docs checkpoint, W4 Information / Media Foundation is canonical NEXT unless the Creator gives a different instruction. Do not activate Mental Episode/Planning runtime yet.**
