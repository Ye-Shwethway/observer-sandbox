# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-17

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve the separation of world truth, exposure, perception, memory, Mind and action authority.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Character-specific behavioral hard-coding is forbidden.
- Persistent branches are only `main` and `test`; normal development occurs on `test` and is promoted to `main` after validation.
- Prefer vertical completeness and operational usefulness over subsystem sprawl.

## Current production checkpoint

The latest runtime-affecting production checkpoint is **Production Diagnostics v2 + deploy-safe hardening**.

Verified evidence before this docs-only synchronization:
- PR #258 — production health-probe shell/SQLite quoting correction; Deploy #283: SUCCESS
- PR #259 — VPS-native runtime diagnostics v1; merge `bf02f15e2024ddd0e0583ce091af9a243982f996`; Deploy #284: SUCCESS
- PR #260 — `Make CI and acceptance checks path-aware`; merge `dd7f8cadbe7b1a5abd8efdb5ff9feb85889e1470`
- PR #261 — `Make production diagnostics error-first and system-aware`; merge `13881cb2e097b3f97e70e315cb81a265c0ee518b`; Deploy #285: SUCCESS
- PR #262 — `Make diagnostics v2 deploy-safe and production-truthful`; merge `034d0c22a4d8edf35f439774a99059aa340cb559`
- **Deploy #286 / run `32040416867`: SUCCESS**
- pre-doc-sync `main = test = 034d0c22a4d8edf35f439774a99059aa340cb559`
- production schema **v15**; economy schema v2; commitment schema v1; environment schema v2; world-input schema v1; mind schema v1.

Production follow-up on 2026-08-17 permanently granted service user `observer` read access to systemd journal through group `systemd-journal`; a direct observer-user journal read returned live `observer-sandbox.service` entries after restart. Telegram `/logs system` and `/logs file` can therefore consume unit journal evidence without recurring sudo intervention.

## Operational diagnostics — DEPLOYED

Production diagnostics are now an active reliability foundation rather than a universe-state dump.

Creator-only Telegram surfaces:
- `/logs` — concise error/system summary
- `/logs errors [lines]` — application warnings/errors/critical records with tracebacks
- `/logs system [lines]` — systemd state and service journal
- `/logs runtime` — concise DB/runtime context
- `/logs file [lines]` — consolidated diagnostics v2 report

The app owns a bounded rotating `/var/lib/observer-sandbox/runtime.log`. Recoverable and fatal exception boundaries log tracebacks. Diagnostics also include read-only SQLite integrity/schema checks and systemd service state. Secrets are not dumped.

The current deploy workflow does not install/replace `/etc/systemd/system/observer-sandbox.service`; diagnostics therefore do not rely on repo-only stdout/stderr append directives. Pre-Python startup/deploy failures remain a GitHub deploy-diagnostic concern because the bot cannot report before the process exists.

## CI / acceptance efficiency — DEPLOYED

PR #260 made CI and specialized acceptances path-aware:
- full CI is reserved for runtime/code/config/test/script/pyproject or CI-workflow changes;
- unrelated feature-specific VPS acceptances no longer fan out merely because shared service wiring or docs changed;
- each feature-owned gate still triggers on its own code/config/tests/validator/workflow paths;
- docs-only changes do not require the full Python suite.

This is the canonical fast-development policy unless concrete risk justifies broader validation.

## Completed foundation stack

Deployed:
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
- Production Diagnostics v2
- CI / acceptance path-awareness

South Lake Tahoe public traversal remains intentionally paused.

## Canonical cognition / world-input chain

Required contracts as relevant:
- `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
- `docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`
- `docs/COMMITMENTS_OBLIGATIONS_FOUNDATION_V1.md`
- `docs/MONEY_ECONOMY_FOUNDATION_V1.md`
- `docs/UNIVERSE_OBJECT_VALUATION_RULES_V1.md`
- `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`
- `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`
- `docs/HISTORICAL_WEATHER_PROVIDER_V1.md`
- `docs/WEATHER_REGION_REGISTRY_V1.md`
- `docs/TELEGRAM_UNIVERSE_OBSERVABILITY_V1.md`
- `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
- `docs/HUMAN_MEMORY_DYNAMICS_V1.md`

Preserve:
`world/event truth != stimulus availability != exposure != perception/interpretation != memory != mind state/thought != intention/plan != action proposal != action authority`.

No continuous per-minute LLM thought polling. Plans remain interruptible and never bypass deterministic action validation.

## Economy / world-input stack

### W0 — World Stimulus / Exposure — DEPLOYED

Shared external-input boundary: eligibility is not exposure; exposure is not perception/belief/memory/thought and grants no action authority.

### W1 / W1.1 Weather — DEPLOYED

Weather remains registry-driven:
`represented region -> enabled registered provider -> universe sim-time query -> cache -> W1 -> W0`.
Only South Lake Tahoe is currently represented/registered.

### W2 — Commitments / Obligations — DEPLOYED

Commitment truth supports appointment, promise, deadline and scheduled responsibility. Notices remain world-input availability and do not automatically create plans or behavior.

### W3 — Money / Economy Foundation — DEPLOYED

Provides generic economic entities, financial accounts, immutable transaction/ledger truth, assets, liabilities, append-only valuations, deterministic affordability/settlement and W0 financial notices.

Darian's Creator-approved opening economy seed remains **USD 25.0M net worth**:
- Thorne Estate: USD 16.5M
- investments: USD 6.5M
- primary liquid holdings: USD 1.8M
- other personal assets: USD 0.7M
- liabilities: USD 0.5M

`net worth != spendable balance`.

### W3.1 — Universe Object Valuation & Creation Rules — DEPLOYED

Canonical rule:
`has economic value != contributes independent net worth`.

Current represented objects/items have explicit value-policy coverage. Estate fixtures are included in the parent Estate asset rather than double-counted. Future runtime object creation must preserve the same valuation-policy boundary.

## Mobility / observer semantics — DEPLOYED INVARIANTS

Canonical mobility boundary:
`legal route existence != ordinary choice preference`.

- deterministically legal one-hop movement remains visible through ordinary recent-use/repetition shaping;
- repetition is cognition context, not topology deletion;
- preferences/habits may influence selection, not legal route existence;
- strong/critical biological need-resolution is a separate deliberate causal guard;
- no Darian-specific outdoor quota, destination steering or estate script.

Telegram location access presentation mirrors authored semantics such as Open, Resident, Private, Restricted, Closed or Locked; presentation does not invent denial.

## Current unresolved autonomy observation

A live behavior gap remains unresolved and is now a candidate for the next bounded phase:
- when already outdoors, the actor can remain outdoors naturally for long periods;
- from indoor locations, the actor does not reliably initiate the multi-hop transition toward known outdoor destinations;
- outdoor destinations, topology knowledge, nature preference, outdoor affordances and emerging outdoor habits are already represented;
- immediate `action_options` expose legal adjacent first hops, while a desired semantic destination may be several hops away;
- example shape: `Living Room -> Grand Foyer -> Mansion Exterior -> Core Estate Grounds`.

Leading hypothesis:
**the current decision surface lacks a generic destination-intent / bounded reachable-preview bridge that gives an intermediate legal first hop purpose toward a known multi-step destination.**

This remains hypothesis-only. It must be tested against source/runtime behavior before implementation. Do not solve it with character-specific prompts, outdoor quotas, topology rewriting or premature MIND-F2/F4/F5 activation.

## Remaining minimum World Input producers

### W4 — Information / Media Foundation — EXISTING ROADMAP CANDIDATE

Represent information/media truth separately from character knowledge:
- information/media items;
- source/publisher and provenance;
- publication/availability;
- credibility metadata;
- represented access/device/media exposure through W0 when a concrete path exists;
- `world knows != character knows`;
- no automatic belief, Memory, concern, intention or action authority;
- apply Telegram observability parity where Creator-useful state exists.

### W5 — Communication Exposure Foundation

Sender/recipient/channel/content/delivery boundary, message/utterance stimulus creation, actual read/heard exposure, and later interpretation/response through social cognition.

## Mind sequence after sufficient minimum world inputs

- MIND-F2 Mental Episode Runtime
- MIND-F3 Attention / Appraisal / Active Concerns
- MIND-F4 Intention Foundation
- MIND-F5 Planning
- MIND-F6 Social Cognition / Communication
- MIND-F7 Relationship Adaptation

The unresolved inside->outside behavior gap does **not** by itself authorize jumping to these layers.

## World / spatial lock

Current Estate boundary remains closed to broader public traversal: no public-road edge from Main Security Gate, no Tahoe-backcountry edge from Concealed Forest Passage, and no water-travel edge from Hidden Dock unless a later authorized slice changes those contracts.

## Current decision point

No new runtime implementation is authorized by this documentation sync.

Two legitimate next-phase candidates must be compared before coding:
1. **Generic Multi-Step Destination Intent / Reachable Preview correction** — investigate and, only if confirmed, close the indoor->outdoor autonomy transition gap without adding character-specific steering or a full planning engine.
2. **W4 Information / Media Foundation** — continue the existing world-input roadmap.

Selection should prioritize the smallest slice that fixes a demonstrated production behavior gap while preserving architecture and vertical completeness. If the autonomy gap can be fixed by a bounded universal bridge using existing topology, memory/knowledge, preferences/history and deterministic action authority, it should be considered before adding another broad world-input producer. If investigation shows the behavior is already supported or the gap requires premature planning architecture, defer it and proceed with W4.

## Exact resume point

**Production is green through Deploy #286 with diagnostics v2 and persistent observer-user journal access. The repo was synchronized at `034d0c22...` before this docs-only continuity change. Next action is proposal/selection only: compare the generic inside->outside multi-step autonomy gap with W4 and define the minimum-runnable next slice. Do not activate runtime changes until the Creator approves the proposal.**
