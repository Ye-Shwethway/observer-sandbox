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

**A3.3 Bounded Multi-Step Destination Intent v1 is COMPLETE / DEPLOYED on top of Diagnostics v2 and the existing W0-W3.1 world-input/economy stack.**

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

Diagnostics continuity immediately below A3.3:
- PR #258 — production health-probe quoting fix; Deploy #283 SUCCESS.
- PR #259 — Diagnostics v1; Deploy #284 SUCCESS.
- PR #260 — path-aware CI/acceptance triggers.
- PR #261 — Diagnostics v2 error-first/system-aware; Deploy #285 SUCCESS.
- PR #262 — diagnostics deploy-safety/production-truth correction; merge `034d0c22a4d8edf35f439774a99059aa340cb559`; Deploy #286 / run `32040416867` SUCCESS.
- production `observer` service user is permanently in `systemd-journal`; direct observer-user journal read was verified, so `/logs system` and `/logs file` have persistent non-sudo unit-journal access.

## A3.3 — Bounded Multi-Step Destination Intent v1 — DEPLOYED

Observed root cause before A3.3:
- exact `action_options` correctly exposed only current one-hop legal moves;
- semantic Character Memory already knew distant Estate destinations and topology;
- existing short autonomy intent started only **after** a move had already been chosen and treated that one-hop target as the destination;
- therefore cognition had no explicit pre-choice bridge from a meaningful known distant destination to the currently legal first hop.

A3.3 adds a generic bounded planning-awareness projection without changing action authority:
- maximum route depth: 4 hops;
- routes traverse only locations present in represented actor semantic spatial memory;
- the first hop must already be an exact current legal `move` option;
- cognition receives destination name, first-hop name, route length, arrival affordances and `planning_only=true`;
- technical destination/first-hop IDs are intentionally omitted from route hints;
- hints are recomputed at every decision boundary;
- no persistent Mind intention/plan artifact is created;
- no destination preference, outdoor quota, Darian-specific steering, or prompt-only topology authority is introduced;
- exact executable action/target pairs and committed validation remain deterministic `action_options` authority.

Canonical boundary:

`actor-known distant destination + current legal first hop + bounded known topology -> planning hint != intention/plan != action authority`.

The first CI attempt exposed a test-fixture assumption, not a runtime defect: removing one Foyer-to-Exterior edge did not make Core Estate Grounds unreachable because the canonical Estate graph contains a legitimate alternate known route. The test was corrected to remove all authored inbound topology to the destination; the final suite and both relevant acceptance gates passed.

### What A3.3 has and has not proven

Proven:
- bounded route-purpose context is generated correctly in tests;
- unknown locations are not leaked from objective topology;
- route depth is bounded;
- topology changes are reflected;
- no represented spatial memory means no multi-hop world-truth projection;
- cognition capability context receives the A3.3 projection;
- production deployment and health are green.

Not yet proven:
- natural production behavior has not yet demonstrated that Darian will actually initiate an inside-to-outside trip because of A3.3. Deploy/recovery evidence proves the new code is live and healthy, but the available cognition snapshots printed during Deploy #287 predated the deploy and therefore are not evidence of a post-deploy A3.3 choice.

**Do not force an outing to manufacture acceptance.** Observe ordinary autonomous decisions. If the inside-to-outside gap persists after enough normal decision opportunities, inspect post-deploy cognition snapshots first and refine the generic bounded route-awareness relevance/selection only if evidence points there. Do not add an outdoor quota or character-specific behavior rule.

## Universal cognition / mobility invariants

Preserve:
`world/event truth != stimulus availability != exposure != perception/interpretation != memory != mind state/thought != intention/plan != action proposal != action authority`.

Mobility:
`legal route existence != ordinary choice preference`.

- Raw topology/access authority determines legal one-hop movement.
- Ordinary repetition must not hide otherwise legal transit edges.
- Known geography may support bounded planning but may not grant an executable move absent from current `action_options`.
- Strong/critical biological need-resolution remains a deliberate causal override.
- No named-character destination steering, outing quotas or campus scripts.

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

W4 Information / Media Foundation remains the next planned world-input product slice after the current A3.3 production observation checkpoint unless the Creator reprioritizes.

## Estate / outside-world lock

Estate-first scope remains active. Existing Estate campus/exterior locations are represented and usable where topology permits. Broader South Lake Tahoe traversal remains intentionally paused: no public-road edge from Main Security Gate, Tahoe-backcountry edge from Concealed Forest Passage, or water-travel edge from Hidden Dock is open.

## Exact resume point

**A3.3 Bounded Multi-Step Destination Intent v1 is production-green through Deploy #287. The immediate next step is read-only natural production observation: allow ordinary autonomous decisions to occur and verify whether post-deploy cognition uses bounded destination hints to initiate purposeful multi-hop movement, especially the previously missing inside-to-outside case. Do not force Darian outside and do not add further steering. If natural observation confirms the gap is resolved, resume the planned W4 Information / Media Foundation. If it does not, inspect post-deploy cognition evidence and make only an evidence-driven generic correction.**
