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

After material repository or verified-runtime checkpoints, continuity must be reconciled here and in `ROADMAP.md` where roadmap state changed. Never leave already-deployed work represented as future work.

## Current canonical checkpoint

**A3.3 Bounded Multi-Step Destination Intent v1 is COMPLETE / DEPLOYED on top of the already-deployed W0-W4.1 world-input stack and Diagnostics v2.**

Latest runtime evidence:
- A3.3 PR #264 — `Add A3.3 bounded multi-step destination intent`
  - final tested head `bd813f90e6610888d0d684e8afdc022484edd280`
  - CI #1052 / run `32042015607`: SUCCESS
  - Cognition Capability Awareness v1 Acceptance #41: SUCCESS
  - Technology Diagnostic Task Runtime v1 Acceptance #59: SUCCESS
  - merge `ab196cb345ba48b6272ff286e47330005ddbf5b3`
  - **Deploy #287 / run `32042149972`: SUCCESS**
- production health after Deploy #287:
  - canonical `observer_sandbox.service` entrypoint active;
  - runtime log ready;
  - SQLite readable and `PRAGMA quick_check=ok`;
  - schema **v15**;
  - Gemini cognition binding preserved at `gemini-3.1-flash-lite`;
  - cognition recovery probe `ok=true`, `mutated=false`, `validated=true`;
  - Telegram API/owner/allowed-user configuration healthy.

`main` and `test` were synchronized at `33b29e59d5c4bd6a7760276e06e1d93ddc8be4dd` before this continuity correction.

## Continuity correction — W4 was already implemented before A3.3

The previous PR #265 continuity text incorrectly carried an older roadmap statement forward and described W4 as future work. Repository history, current source, tests and canonical W4 contracts prove otherwise.

Implemented W4 lineage:
- PR #249 — **W4 Information / Media Foundation + W4.1 Historical News Provider**; merge `2e11b784f2c6ce651cced81d45d09c6e2977fe69`.
- PR #250 — Creator-facing News observability/generation surface; merge `4a764a5fdf2c9cc8c77533e002188c4a295a6c3c`.
- PR #251 — autonomous simulation-time TV news scheduling at South Lake Tahoe local **07:00 / 18:00**.
- PR #252 — first-class generic `consume_media` runtime; merge `2db08335a35fa7f96e03bbb9ed1f176b44d5e8b2`.

Current production through Deploy #287 includes this entire lineage.

Canonical W4 behavior:
- published/reported information is separate from objective world truth;
- existing `object_media_console` is the represented television/media device;
- historical GDELT GAL evidence is selected by **universe simulation time**, not host current time;
- scheduled Morning News and Evening News publications are driven by simulation time and do not poll AI every tick;
- publication alone does not expose content to a character;
- `consume_media` requires a represented current publication and compatible co-location;
- completed media consumption records W0 exposure;
- exposure does not automatically create belief, Memory, Mental Episode, intention, plan or action authority;
- News Generation AI uses its own `engine/information_media/news_generation` binding with source-backed deterministic fallback.

Therefore **W4 and W4.1 are DEPLOYED, not the next planned slice.**

## A3.3 — Bounded Multi-Step Destination Intent v1 — DEPLOYED

Observed root cause before A3.3:
- exact `action_options` correctly exposed only current one-hop legal moves;
- semantic Character Memory already knew distant Estate destinations and topology;
- existing short autonomy intent started only after a move had already been chosen and treated that one-hop target as the destination;
- cognition had no explicit pre-choice bridge from a meaningful known distant destination to the currently legal first hop.

A3.3 adds a generic bounded planning-awareness projection without changing action authority:
- maximum route depth: 4 hops;
- routes traverse only locations present in represented actor semantic spatial memory;
- first hop must already be an exact current legal `move` option;
- cognition receives destination name, first-hop name, route length, arrival affordances and `planning_only=true`;
- technical route IDs are omitted;
- hints are recomputed at every decision boundary;
- no persistent Mind intention/plan artifact is created;
- no destination preference, outdoor quota, named-character steering or prompt-only topology authority is introduced;
- deterministic `action_options` and committed validation remain final action authority.

Canonical boundary:
`actor-known distant destination + current legal first hop + bounded known topology -> planning hint != intention/plan != action authority`.

### A3.3 proof boundary

Proven by tests/deploy:
- bounded route-purpose context;
- unknown-location non-leakage;
- bounded route depth;
- topology-sensitive preview;
- no spatial memory -> no multi-hop projection;
- cognition integration;
- production deployment/health.

Still pending:
- read-only natural production observation that ordinary autonomy actually initiates the previously missing inside-to-outside multi-hop trip.

Do not force an outing to manufacture acceptance. If the gap persists after normal decision opportunities, inspect post-deploy cognition evidence and make only a generic evidence-driven correction. Do not add an outdoor quota or character-specific rule.

The interim multi-hop guidance is explicitly temporary scaffolding. When MIND-F4/F5 intention/planning becomes active, reconcile it into typed Mind intention/plan flow and remove/reduce duplicate prompt-level planning guidance.

## Operational diagnostics — DEPLOYED

- PR #258 — production health-probe quoting fix / Deploy #283 SUCCESS.
- PR #259 — Diagnostics v1 / Deploy #284 SUCCESS.
- PR #260 — path-aware CI/acceptance triggers.
- PR #261 — Diagnostics v2 error-first/system-aware / Deploy #285 SUCCESS.
- PR #262 — deploy-safe/production-truth correction; merge `034d0c22a4d8edf35f439774a99059aa340cb559`; Deploy #286 SUCCESS.

Creator-only Telegram diagnostics:
- `/logs`
- `/logs errors [lines]`
- `/logs system [lines]`
- `/logs runtime`
- `/logs file [lines]`

The production `observer` user has persistent `systemd-journal` read access. Pre-Python startup failures remain deployment-diagnostic territory.

## Deployed World Input / economy stack

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
- **W4 Information / Media Foundation v1**
- **W4.1 Historical News Provider v1**
- **Autonomous simulation-time Morning/Evening TV bulletin scheduling**
- **First-class Media Console `consume_media` runtime and W0 exposure bridge**

## Canonical route into the Intelligent Mind Engine

The sequence was already planned in the canonical W0 and Mind contracts. Do not rediscover or replace it from chat memory.

Default remaining sequence:
1. **W5 Communication Exposure Foundation** — sender/recipient/channel/content/delivery/read-or-heard boundary through W0; no automatic interpretation or response.
2. **MIND-F2 Mental Episode Runtime** — activate bounded character-owned Mental Episodes at meaningful cognition boundaries.
3. **MIND-F3 Attention / Appraisal / Active Concerns** — actor-relative relevance, appraisal and concern state.
4. **MIND-F4 Intention Foundation** — typed intention candidates/artifacts without bypassing deterministic action authority.
5. **MIND-F5 Planning** — bounded plan artifacts/candidates and route/task continuity; reconcile interim A3.3 prompt scaffolding here.
6. **MIND-F6 Social Cognition / Communication** — interpret represented communication/social exposure and form response intentions.
7. **MIND-F7 Relationship Adaptation** — relationship interpretation/adaptation downstream of represented events, exposure and social cognition.

This ordering is planning guidance, not permission to prebuild unused complexity and not a claim that every possible world system must be exhaustive before MIND-F2. The Mind contract permits bounded mental work once the required input sockets are sufficiently represented.

Preserve the authority chain:
`world/event truth -> stimulus availability -> exposure -> perception/interpretation -> memory -> Mind episode/artifacts -> intention/plan -> action proposal -> deterministic action authority`.

## Estate / outside-world lock

Estate-first scope remains active. Existing Estate campus/exterior locations are represented and usable where topology permits. Broader South Lake Tahoe traversal remains intentionally paused: no public-road edge from Main Security Gate, Tahoe-backcountry edge from Concealed Forest Passage, or water-travel edge from Hidden Dock is open.

## Exact resume point

**A3.3 is production-green through Deploy #287 and W4/W4.1/media consumption are already deployed. The immediate operational checkpoint is still read-only natural observation of A3.3 inside-to-outside behavior; this observation is independent of W4 and must not be described as a gate before W4. For new implementation work, the canonical next minimum world-input slice is W5 Communication Exposure Foundation unless the Creator reprioritizes. After sufficient W5 input coverage, follow the already-planned Mind sequence MIND-F2 -> F3 -> F4 -> F5 -> F6 -> F7, preserving the Mind/world/memory/action authority boundaries and reconciling interim A3.3 planning scaffolding when intention/planning becomes real runtime.**
