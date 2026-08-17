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

**A3.3 Bounded Multi-Step Destination Intent v1 is COMPLETE / DEPLOYED.**

Latest evidence:
- PR #264 — `Add A3.3 bounded multi-step destination intent`
- final tested head `bd813f90e6610888d0d684e8afdc022484edd280`
- CI #1052 / run `32042015607`: SUCCESS
- Cognition Capability Awareness v1 Acceptance #41: SUCCESS
- Technology Diagnostic Task Runtime v1 Acceptance #59: SUCCESS
- merge `ab196cb345ba48b6272ff286e47330005ddbf5b3`
- **Deploy #287 / run `32042149972`: SUCCESS**
- production after deploy: canonical service active, runtime log ready, SQLite readable, `PRAGMA quick_check=ok`, schema **v15**, Gemini cognition recovery validated without mutation, Telegram API healthy.

Diagnostics immediately below this checkpoint remain production-green:
- PR #258 health-probe quoting fix / Deploy #283
- PR #259 Diagnostics v1 / Deploy #284
- PR #260 path-aware CI/acceptance
- PR #261 Diagnostics v2 / Deploy #285
- PR #262 deploy-safe diagnostics hardening / Deploy #286
- production `observer` user has persistent `systemd-journal` read access for Telegram system diagnostics.

## A3.3 — Bounded Multi-Step Destination Intent v1 — DEPLOYED

### Problem closed at the architecture level

Before A3.3:
- exact immediate movement authority was correctly one-hop only;
- semantic Character Memory already represented known distant Estate locations and connections;
- existing short autonomy intent started only after a move was selected and used the one-hop target as the destination;
- cognition therefore lacked an explicit bridge from a meaningful known distant destination to the legal immediate move that begins the route.

A3.3 introduces bounded read-only route-purpose awareness:

`actor-known destination + actor-known topology + current legal first hop -> bounded route hint`.

Properties:
- maximum depth 4 hops;
- only semantic-memory-known locations participate;
- first hop must already be an exact current legal `move` option;
- hints include destination name, first-hop name, hop count, arrival affordances and `planning_only=true`;
- technical route target IDs are omitted from the planning hint;
- hints are recomputed each decision boundary;
- route awareness stores no persistent Mind intention or plan;
- access/topology/physiology changes can redirect the next decision naturally;
- no named-character destination rule, outdoor quota, destination preference or campus script exists;
- deterministic `action_options` and committed validation remain the sole execution authority.

Preserve:

`bounded route awareness != intention != plan != action authority`.

### Acceptance coverage

Focused coverage proves:
- a known distant destination can expose a purpose-bearing legal first hop while remaining absent from immediate executable targets;
- unknown destinations are not leaked from objective world topology;
- preview depth is bounded;
- authored topology changes alter preview reachability;
- absence of represented spatial memory disables the multi-hop projection;
- cognition capability context receives the projection.

The first full-CI attempt ended at 756 passed / 1 failed because the new test assumed deleting one Foyer-to-Exterior edge made Core Estate Grounds unreachable. The canonical Estate graph had a valid alternate route, so the BFS behavior was correct. The test was corrected to remove all inbound topology to the destination. Final CI and both relevant acceptance gates are green.

### Production observation still required

Deploy #287 proves the implementation is live and healthy, but it does **not** yet prove that natural autonomous behavior will choose an inside-to-outside trip. The cognition snapshots visible in the deploy health output were captured before the new deploy and cannot be used as post-deploy behavioral proof.

The next checkpoint is therefore read-only natural observation. Do not force an outing merely to make the feature look successful.

If ordinary decisions still fail to initiate known meaningful multi-hop destinations, inspect post-deploy cognition snapshots and determine whether the A3.3 route set/relevance is actually visible and useful. Any correction must remain generic and evidence-driven; do not introduce outing quotas, destination steering or a full planning engine as a shortcut.

## Operational diagnostics — DEPLOYED

Creator-only Telegram surfaces:
- `/logs` — concise error/system summary
- `/logs errors [lines]` — application warnings/errors/critical records with tracebacks
- `/logs system [lines]` — systemd state and service journal
- `/logs runtime` — concise DB/runtime context
- `/logs file [lines]` — consolidated diagnostics v2 report

The app owns a bounded rotating `/var/lib/observer-sandbox/runtime.log`. System journal read access is permanently available to the production service user through `systemd-journal` membership. Pre-Python startup failures remain deployment-diagnostic territory because the Telegram process does not yet exist at that boundary.

## CI / acceptance efficiency — DEPLOYED

CI/acceptance path-awareness remains active:
- full CI covers runtime/code/config/test/script/pyproject or CI-workflow changes;
- specialized VPS acceptances trigger on their owned surfaces instead of shared-service/docs noise;
- docs-only continuity changes do not require the full Python suite.

## Completed foundation stack

Deployed:
- Character Profile / Skills and adaptive-profile foundations
- Estate spatial/reachability and outdoor-affordance foundation
- Universal Character Autonomy
- Character Memory + Semantic Spatial Memory + Human Memory Dynamics
- Intelligent Mind Engine Foundation v1
- **A3.3 Bounded Multi-Step Destination Intent v1**
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

## Canonical cognition / mobility chain

Preserve:
`world/event truth != stimulus availability != exposure != perception/interpretation != memory != mind state/thought != intention/plan != action proposal != action authority`.

Mobility additionally preserves:
`legal route existence != ordinary choice preference`.

- legal one-hop moves derive from deterministic topology/access;
- repetition may affect choice but not delete legal transit edges;
- actor-known distant geography may inform bounded route purpose without granting movement authority;
- strong/critical biological need-resolution remains a separate deliberate causal override;
- no named-character route behavior is permitted.

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

Darian's Creator-approved opening economy seed remains **USD 25.0M net worth**.

`net worth != spendable balance`.

### W3.1 — Universe Object Valuation & Creation Rules — DEPLOYED

Canonical rule:
`has economic value != contributes independent net worth`.

Current represented objects/items have explicit value-policy coverage. Estate fixtures are included in the parent Estate asset rather than double-counted. Future runtime object creation must preserve the same valuation-policy boundary.

## Remaining minimum World Input producers

### W4 — Information / Media Foundation — NEXT AFTER A3.3 OBSERVATION

Represent information/media truth separately from character knowledge:
- information/media items;
- source/publisher and provenance;
- publication/availability;
- credibility metadata;
- represented access/device/media exposure through W0 when a concrete path exists;
- `world knows != character knows`;
- no automatic belief, Memory, concern, intention or action authority;
- apply Telegram observability parity where Creator-useful state exists.

Do not begin W4 merely to avoid observing the newly deployed autonomy correction. First establish whether the demonstrated inside-to-outside gap is actually resolved in natural production behavior.

### W5 — Communication Exposure Foundation

Sender/recipient/channel/content/delivery boundary, message/utterance stimulus creation, actual read/heard exposure, and later interpretation/response through social cognition.

## Mind sequence after sufficient minimum world inputs

- MIND-F2 Mental Episode Runtime
- MIND-F3 Attention / Appraisal / Active Concerns
- MIND-F4 Intention Foundation
- MIND-F5 Planning
- MIND-F6 Social Cognition / Communication
- MIND-F7 Relationship Adaptation

A3.3 deliberately does not activate these layers.

## World / spatial lock

Estate-first scope remains active. Broader public traversal stays closed: no public-road edge from Main Security Gate, no Tahoe-backcountry edge from Concealed Forest Passage, and no water-travel edge from Hidden Dock unless a later authorized slice changes those contracts.

## Current exact resume point

**A3.3 Bounded Multi-Step Destination Intent v1 is production-green through Deploy #287. The immediate next action is read-only natural production observation of ordinary autonomous decisions. Verify whether post-deploy cognition uses bounded route-purpose hints to begin meaningful multi-hop travel, especially the previously missing indoor-to-outdoor transition. Do not force an outing. If confirmed, proceed to W4 Information / Media Foundation as the next planned product slice. If not confirmed after reasonable ordinary decision opportunities, inspect post-deploy cognition evidence and make only a bounded generic correction supported by that evidence.**
