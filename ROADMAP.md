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
- At material checkpoints, reconcile roadmap/bootstrap state with implementation and verified runtime truth. Already-deployed work must never remain labeled as future work.

## Current production checkpoint

**A3.3 Bounded Multi-Step Destination Intent v1 is COMPLETE / DEPLOYED on top of the already-deployed W0-W4.1 world-input stack.**

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

## Continuity correction — W4/W4.1 are already deployed

The previous roadmap accidentally retained an older planning label and described W4 as `NEXT AFTER A3.3 OBSERVATION`. Repository history and current runtime/source prove W4 was implemented **before** A3.3.

Implemented lineage:
- PR #249 — W4 Information / Media Foundation + W4.1 Historical News Provider; merge `2e11b784f2c6ce651cced81d45d09c6e2977fe69`.
- PR #250 — Creator News observability/generation surface; merge `4a764a5fdf2c9cc8c77533e002188c4a295a6c3c`.
- PR #251 — autonomous simulation-time TV bulletin scheduling at 07:00 / 18:00 South Lake Tahoe local time.
- PR #252 — first-class generic Media Console `consume_media` runtime; merge `2db08335a35fa7f96e03bbb9ed1f176b44d5e8b2`.

All are ancestors of the current production checkpoint and therefore present in Deploy #287.

## A3.3 — Bounded Multi-Step Destination Intent v1 — DEPLOYED

### Architecture gap closed

Before A3.3:
- exact immediate movement authority was correctly one-hop only;
- semantic Character Memory already represented known distant Estate locations and connections;
- existing short autonomy intent started only after a move was selected and used the one-hop target as the destination;
- cognition lacked an explicit bridge from a meaningful known distant destination to the legal immediate move that begins the route.

A3.3 introduces bounded read-only route-purpose awareness:

`actor-known destination + actor-known topology + current legal first hop -> bounded route hint`.

Properties:
- maximum depth 4 hops;
- only semantic-memory-known locations participate;
- first hop must already be an exact current legal `move` option;
- hints include destination name, first-hop name, hop count, arrival affordances and `planning_only=true`;
- technical route IDs are omitted;
- hints are recomputed each decision boundary;
- no persistent Mind intention/plan is created;
- no named-character destination rule, outdoor quota, destination preference or campus script exists;
- deterministic `action_options` and committed validation remain sole execution authority.

Preserve:
`bounded route awareness != intention != plan != action authority`.

### Production observation still required

Deploy #287 proves A3.3 is live and healthy but not yet that natural autonomy will choose the previously missing inside-to-outside trip. The immediate operational checkpoint is read-only natural observation. Do not force an outing.

If ordinary decisions still fail to initiate known meaningful multi-hop destinations, inspect post-deploy cognition evidence. Any correction must remain generic and evidence-driven.

A3.3's pre-Mind planning guidance is explicit scaffolding. When MIND-F4/F5 intention/planning runtime becomes active, review/migrate durable route purpose into typed Mind artifacts/candidates and remove or reduce duplicate prompt-level guidance so two planning authorities do not coexist.

## Operational diagnostics — DEPLOYED

Creator-only Telegram surfaces:
- `/logs` — concise error/system summary
- `/logs errors [lines]` — application warnings/errors/critical records with tracebacks
- `/logs system [lines]` — systemd state and service journal
- `/logs runtime` — concise DB/runtime context
- `/logs file [lines]` — consolidated diagnostics v2 report

The app owns bounded rotating `/var/lib/observer-sandbox/runtime.log`. System journal read access is available through `systemd-journal`. Pre-Python startup failures remain deployment-diagnostic territory.

## CI / acceptance efficiency — DEPLOYED

- full CI covers runtime/code/config/test/script/pyproject or CI-workflow changes;
- specialized VPS acceptances trigger on owned surfaces rather than shared-service/docs noise;
- docs-only continuity changes do not require the full Python suite.

## Completed foundation stack

Deployed:
- Character Profile / Skills and adaptive-profile foundations
- Estate spatial/reachability and outdoor-affordance foundation
- Universal Character Autonomy
- Character Memory + Semantic Spatial Memory + Human Memory Dynamics
- Intelligent Mind Engine Foundation v1 schema/contract
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
- **W4 Information / Media Foundation v1**
- **W4.1 Historical News Provider v1**
- **Autonomous simulation-time Morning/Evening TV bulletin scheduler**
- **First-class Media Console media-consumption / W0 exposure bridge**
- Production Diagnostics v2
- CI / acceptance path-awareness

South Lake Tahoe public traversal remains intentionally paused.

## Canonical cognition / world-input chain

Preserve:
`world/event truth != stimulus availability != exposure != perception/interpretation != memory != mind state/thought != intention/plan != action proposal != action authority`.

Mobility additionally preserves:
`legal route existence != ordinary choice preference`.

- legal one-hop moves derive from deterministic topology/access;
- repetition may affect choice but not delete legal transit edges;
- actor-known distant geography may inform bounded route purpose without granting movement authority;
- strong/critical biological need-resolution remains a separate deliberate causal override;
- no named-character route behavior is permitted.

## World-input stack

### W0 — World Stimulus / Exposure — DEPLOYED

Shared external-input boundary: eligibility is not exposure; exposure is not perception/belief/memory/thought and grants no action authority.

### W1 / W1.1 Weather — DEPLOYED

Weather remains registry-driven:
`represented region -> enabled registered provider -> universe sim-time query -> cache -> W1 -> W0`.
Only South Lake Tahoe is currently represented/registered.

### W2 — Commitments / Obligations — DEPLOYED

Commitment truth supports appointment, promise, deadline and scheduled responsibility. Notices do not automatically create plans or behavior.

### W3 — Money / Economy Foundation — DEPLOYED

Provides generic economic entities, financial accounts, immutable transaction/ledger truth, assets, liabilities, append-only valuations, deterministic affordability/settlement and W0 financial notices.

Darian's Creator-approved opening economy seed remains **USD 25.0M net worth**.

`net worth != spendable balance`.

### W3.1 — Universe Object Valuation & Creation Rules — DEPLOYED

Canonical rule:
`has economic value != contributes independent net worth`.

Current represented objects/items have explicit value-policy coverage. Estate fixtures are included in the parent Estate asset rather than double-counted. Future runtime object creation must preserve the same valuation-policy boundary.

### W4 — Information / Media Foundation — DEPLOYED

Canonical chain:
`source/world evidence -> information item -> publication/availability -> represented media device/channel -> W0 stimulus -> actual exposure -> later perception/appraisal -> later Memory/Mind`.

Implemented minimum:
- generic sources/publishers, provenance and credibility metadata;
- generic information items and bounded publication windows;
- existing Media Console reused as TV exemplar;
- W0 information/media stimuli;
- exposure only after represented compatible consumption;
- no automatic belief, Memory, Mental Episode, intention or action authority;
- independent News Generation AI binding with deterministic source-backed fallback;
- Creator-facing News observability/generation diagnostics.

### W4.1 — Historical News Provider — DEPLOYED

`universe simulation time -> GDELT GAL historical evidence -> normalized W4 source records -> optional AI editorial bulletin -> W0 TV publication/stimulus`.

Historical-time selection prevents current server headlines from leaking into the earlier simulation timeline.

### W4 media-consumption bridge — DEPLOYED

- Morning News at 07:00 and Evening News at 18:00 South Lake Tahoe local time;
- service loop performs bounded due-slot scheduling rather than per-tick AI generation;
- `consume_media` is a generic action offered only for an available publication at a represented local media device;
- completed consumption records W0 exposure;
- publication/exposure content does not bypass Memory/Mind boundaries.

## Remaining minimum World Input producer

### W5 — Communication Exposure Foundation — NEXT DEFAULT WORLD-INPUT SLICE

Minimum contract:
- sender / recipient / channel / content / delivery truth;
- message or utterance becomes a W0 `communication` stimulus;
- represented delivery/read/heard conditions determine actual exposure;
- exposure does not automatically imply understanding, belief, memory, relationship change or response;
- interpretation and response belong to later Social Cognition;
- add represented devices/endpoints only when a concrete communication path needs them; do not prebuild a full phone/internet ecosystem.

W5 is the only remaining producer in the canonical W0 preferred minimum W1-W5 sequence. The sequence is guidance and may be reprioritized by the Creator.

## Intelligent Mind Engine route — PRE-PLANNED CANONICAL SEQUENCE

`docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md` is already the canonical integration contract. Its foundation schema/socket layer exists; the following phases activate richer character-owned mental runtime.

### MIND-F2 — Mental Episode Runtime

Activate bounded Mental Episodes at meaningful cognition boundaries rather than continuous LLM polling. Supported episode modes are designed for task-focused, spontaneous, reflective, prospective, social and evaluative processing.

### MIND-F3 — Attention / Appraisal / Active Concerns

Transform bounded actor-relative perceived/recalled inputs into attention allocation, appraisal and active concern state. External stimulus salience is not automatically mental importance.

### MIND-F4 — Intention Foundation

Introduce typed intention candidates/artifacts owned by the character Mind. Intention may influence proposals but never becomes executable action authority.

### MIND-F5 — Planning

Introduce bounded plan candidates/artifacts and continuity across steps while preserving deterministic validation and world topology. This phase must reconcile the interim A3.3 multi-hop purpose scaffolding and prevent duplicate planning authorities.

### MIND-F6 — Social Cognition / Communication

Consume represented communication/social exposure, Memory/person context and current state to form social appraisal/inference and response intentions. Direct communication does not bypass perception or Mind.

### MIND-F7 — Relationship Adaptation

Adapt relationship interpretation/state downstream of represented shared events, exposure, memory and social cognition rather than directly mutating trust/relationship from raw utterances.

### Foundation hierarchy already reserved

The Mind foundation already defines:
- Mental Cycle
- Mental Episode
- Mental Artifact types including `concern`, `goal`, `intention`, `plan`, `social_inference`, `appraisal`, `working_item`
- typed links to memories/events/entities/locations/actions/artifacts
- input sockets for present state, profile, physiology, current action, perception, recallable memories, active mental artifacts, relationships, goals, world and communication context
- output sockets for episodes, artifact changes, intention/plan candidates, social inference and action proposal.

Default product route:
`W5 -> MIND-F2 -> MIND-F3 -> MIND-F4 -> MIND-F5 -> MIND-F6 -> MIND-F7`.

This is not a demand to exhaustively finish every possible world feature before Mind work. The canonical Mind contract explicitly allows bounded mental work once required inputs are sufficiently represented.

## World / spatial lock

Estate-first scope remains active. Broader public traversal stays closed: no public-road edge from Main Security Gate, no Tahoe-backcountry edge from Concealed Forest Passage, and no water-travel edge from Hidden Dock unless a later authorized slice changes those contracts.

## Current exact resume point

**A3.3 is production-green through Deploy #287 and remains under read-only natural observation for the inside-to-outside behavioral proof. W4/W4.1 and first-class Media Console news consumption are already deployed and must not be treated as future work. For new implementation, the default next minimum world-input slice is W5 Communication Exposure Foundation unless the Creator reprioritizes. After sufficient W5 coverage, continue the already-authored Mind route MIND-F2 -> F3 -> F4 -> F5 -> F6 -> F7. When MIND-F4/F5 become active, explicitly reconcile and retire/reduce interim A3.3 prompt-level planning scaffolding so deterministic action authority remains singular.**
