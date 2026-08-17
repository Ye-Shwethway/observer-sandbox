# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-17

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

The latest runtime-affecting production checkpoint is **Production Diagnostics v2 + deploy-safe hardening**, on top of the previously deployed world-input/economy/mobility stack.

Latest verified repository/runtime evidence before this documentation sync:
- `main = test = 034d0c22a4d8edf35f439774a99059aa340cb559`
- PR #258 — production health-probe shell/SQLite quoting correction; Deploy #283: SUCCESS
- PR #259 — VPS-native runtime diagnostics v1; merge `bf02f15e2024ddd0e0583ce091af9a243982f996`; Deploy #284: SUCCESS
- PR #260 — `Make CI and acceptance checks path-aware`; merge `dd7f8cadbe7b1a5abd8efdb5ff9feb85889e1470`
- PR #261 — `Make production diagnostics error-first and system-aware`; merge `13881cb2e097b3f97e70e315cb81a265c0ee518b`; Deploy #285: SUCCESS
- PR #262 — `Make diagnostics v2 deploy-safe and production-truthful`; merge `034d0c22a4d8edf35f439774a99059aa340cb559`
- **Deploy #286 / run `32040416867`: SUCCESS**
- production schema: **v15**
- economy schema v2; commitment schema v1; environment schema v2; world-input schema v1; mind schema v1.

### Production diagnostics v2 contract

Creator-only Telegram diagnostics are operational and intentionally error-first:
- `/logs` — concise health/error summary
- `/logs errors [lines]` — application WARNING/ERROR/CRITICAL records with traceback continuation
- `/logs system [lines]` — systemd state + unit journal
- `/logs runtime` — concise runtime/DB context, excluding giant cognition-state dumps
- `/logs file [lines]` — consolidated diagnostics v2 text report

Guaranteed app-side evidence includes the rotating `/var/lib/observer-sandbox/runtime.log`, traceback-capable logging at recoverable/fatal exception boundaries, SQLite integrity/schema context and systemd service state.

The deployed systemd unit is not rewritten by the normal deploy workflow. PR #262 therefore removed the false `service-stderr.log` dependency instead of pretending repo-only unit directives were active in production.

Production infrastructure follow-up on 2026-08-17 permanently added service user `observer` to group `systemd-journal` and restarted `observer-sandbox.service`. A direct `sudo -u observer journalctl -u observer-sandbox.service ...` test returned live service journal lines. Therefore normal diagnostics now have persistent non-sudo unit-journal read access. Pre-Python startup/deploy failures remain covered by the GitHub deploy failure diagnostic artifact because the Telegram bot cannot report before the process exists.

## Previously completed product stack

Production already includes:
- Character Profile / Skills and adaptive-profile foundations
- Estate spatial/reachability and outdoor-affordance foundation
- Universal Character Autonomy
- Character Memory + Semantic Spatial Memory + Human Memory Dynamics
- Intelligent Mind Engine Foundation v1
- W0 World Stimulus / Exposure Foundation
- W1 Environment / Weather Foundation
- W1.1 Historical Weather Provider
- Creator Universe Weather & Geography Observability
- Weather Region Registry v1
- W2 Commitments / Obligations Foundation v1
- W3 Money / Economy Foundation v1
- W3.1 Universe Object Valuation & Creation Rules v1
- Telegram Economy/Identity Observability Parity
- Transit Route / Telegram Access Semantics correction

The earlier W3/W3.1 checkpoint remains historically valid, but Deploy #268 is no longer the latest production checkpoint.

## Required cognition / world-input read order

For cognition/world-input work read, as relevant:
1. `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
2. `docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`
3. `docs/COMMITMENTS_OBLIGATIONS_FOUNDATION_V1.md`
4. `docs/MONEY_ECONOMY_FOUNDATION_V1.md`
5. `docs/UNIVERSE_OBJECT_VALUATION_RULES_V1.md`
6. `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`
7. `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`
8. `docs/HISTORICAL_WEATHER_PROVIDER_V1.md`
9. `docs/WEATHER_REGION_REGISTRY_V1.md`
10. `docs/TELEGRAM_UNIVERSE_OBSERVABILITY_V1.md`
11. `docs/HUMAN_MEMORY_DYNAMICS_V1.md`
12. `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
13. task-relevant world/profile/runtime docs only.

Preserve:
`world/event truth != stimulus availability != character exposure != perception != memory != mind/thought != intention/plan != action proposal != action authority`.

MIND-F0 remains behavior-neutral. Do not activate Mental Episode/Planning runtime merely to fix ordinary movement selection.

## Universal autonomy / mobility invariants

Character-specific behavioral hard-coding is forbidden.

Preserve:
`legal route existence != ordinary choice preference`.

- raw topology/access authority decides whether one-hop movement is legal;
- ordinary repetition shaping must not hide otherwise legal transit edges;
- preferences, habits and discretionary behavior may influence choice, not topology;
- strong/critical biological need-resolution may deliberately narrow proposal surfaces;
- do not add Darian-specific outdoor quotas, destination steering, mansion-exit scripts or bespoke autonomy prompts.

Spatial movement remains graph-based. `contains` is structural containment; `connected_to` is traversable topology; `located_at` is dynamic presence. Deterministic routing derives from authored topology and access state.

## Telegram observability parity

Creator-useful authoritative state should appear in the semantically relevant Telegram surface in the same bounded feature slice when such a surface exists, unless explicitly documented as not relevant yet.

Telegram remains downstream/read-only. Viewing diagnostics/profile/world state must not mutate simulation, create exposure, create cognition/memory, or grant action authority.

## Current observed autonomy gap

A current live-behavior observation remains unresolved:
- once the actor is outdoors, outdoor behavior can persist naturally;
- from indoor rooms, the actor does not appear to form the multi-step transition needed to reach known outdoor destinations naturally;
- outdoor destinations, outdoor affordances, nature preference and emerging outdoor habits are represented;
- from an indoor room such as Living Room, immediate `action_options` expose only adjacent legal first hops; an outdoor destination may require an intermediate hop such as Grand Foyer before Mansion Exterior / Estate Grounds;
- therefore the leading hypothesis is a **generic multi-step destination-intent / reachable-preview bridge gap**, not missing outdoor semantics and not a need for an outdoor quota.

This is still an investigation hypothesis, not an implemented fix. Any correction must remain universal and deterministic-authority-safe.

## World-input roadmap status

The previously documented product-roadmap next slice remains:
- W4 Information / Media Foundation
- then W5 Communication Exposure Foundation
- then MIND-F2 Mental Episode Runtime only after minimum external-input foundations are sufficient.

However, current Creator direction requires a fresh next-phase proposal after this documentation synchronization. Do not assume W4 should outrank the unresolved autonomy/mobility behavior gap without evaluating both against current production needs.

## Exact resume point

**Diagnostics v2 is production-green through Deploy #286, production journal access is permanently usable by the `observer` service user, and `main`/`test` were synchronized at merge `034d0c22...` before this docs-only continuity update. No new runtime implementation is currently authorized. Next: propose the best next minimum-runnable phase, explicitly comparing the unresolved generic inside->outside multi-step autonomy gap against the existing W4 Information / Media roadmap candidate. Do not activate character-specific steering or Mental Episode/Planning as a shortcut.**
