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

After material repository or verified-runtime checkpoints, reconcile this file and `ROADMAP.md`. Never leave deployed work described as future work.

## Current canonical checkpoint

**Perception Foundation v1 is COMPLETE / DEPLOYED on top of the complete W0-W5 minimum world-input producer stack, A3.3 bounded route awareness, Character Memory, the Mind Foundation schema/contract, and Diagnostics v2.**

Latest runtime evidence:
- PR #269 — `Add minimum Perception Foundation v1`
  - final tested head `fc33f01272773febe8431c82b29d62ca6e77d2af`
  - **CI #1054 / run `32045634180`: SUCCESS**
  - merge `ebe5bb923c90c77dd878bd6e485e20d7fc68dea7`
  - **Deploy #289 / run `32045825836`: SUCCESS**
- production health after Deploy #289:
  - canonical `observer_sandbox.service` entrypoint active;
  - runtime log ready;
  - SQLite readable and `PRAGMA quick_check=ok`;
  - schema remains **v15**; Perception Foundation required no migration;
  - Gemini cognition binding preserved at `gemini-3.1-flash-lite`;
  - cognition recovery probe `ok=true`, `mutated=false`, `validated=true`;
  - Telegram API/owner/allowed-user configuration healthy.

## Perception Foundation v1 — DEPLOYED / MINIMUM COMPLETE

Canonical contract:
- `docs/PERCEPTION_FOUNDATION_V1.md`

Runtime / acceptance:
- `src/observer_sandbox/perception.py`
- `src/observer_sandbox/memory_aware_decision.py`
- `tests/test_perception_foundation_v1.py`

### Audit result

The pre-implementation audit proved a real gap rather than a naming mismatch:
- W0 explicitly stopped at `character_exposures`;
- the Intelligent Mind Engine contract already reserved a bounded `perception` input socket;
- normal cognition did not read `character_exposures` and no equivalent perception bridge existed elsewhere in source/schema/tests/docs.

The minimum closure therefore uses a **deterministic bounded read projection** over existing W0 exposure truth instead of introducing a second external-input store.

Canonical chain:
`world/event truth -> W0 stimulus -> actual character exposure -> actor-relative perception input -> later appraisal/Mind -> later selective memory/intention/plan -> action proposal -> deterministic action authority`.

Preserve:
`exposure != perception input != understanding != belief != appraisal != memory != thought != intention/plan != action authority`.

### Runtime semantics

`recent_perception_context(...)`:
- accepts only a represented character;
- reads only that actor's `status='exposed'` rows;
- excludes exposure later than the current simulation time;
- excludes invalidated exposure;
- joins authoritative W0 stimulus payload/provenance;
- preserves stimulus/exposure IDs, routing type/channel, subject, source links, simulation time, external salience, optional producer-authored `attention_hint`, and provenance metadata;
- defaults to the most recent 8 records and hard-bounds requested retrieval to 50;
- returns mode `exposure_projection_v1`.

Normal autonomous cognition receives this projection through `MemoryAwareDecisionProvider` as:
`state["perception"]`.

This is an actor-relative external-input handoff, **not semantic comprehension**. It creates no Character Memory, Mental Cycle, Mental Episode, Mental Artifact, belief, appraisal, concern, relationship change, intention, plan, action option, or world mutation.

No schema migration was added because the minimum handoff creates no new durable truth.

### Perception proof boundary

Automated acceptance proves:
- valid actor-owned exposure reaches the perception socket with world payload and provenance;
- future exposure does not leak into an earlier decision time;
- invalidated exposure is excluded;
- the projection itself creates no events, Character Memory, Mental Cycles, Mental Episodes, or Mental Artifacts;
- normal `MemoryAwareDecisionProvider` cognition context includes `perception` while preserving existing memory and action-option context;
- full repository regression CI remains green.

Deploy #289 proves the implementation is installed and production health remains green.

Do not fabricate a production stimulus merely to manufacture a non-empty post-deploy perception snapshot. Natural future W0 exposure will provide live content evidence. This observation is useful but is **not a gate before MIND-F2**, because the generic runtime handoff is already covered by focused acceptance + full CI + production deployment health.

## W5 communication path is now externally connected to Mind input

W5 remains minimum-complete through Deploy #288 and now has the intended external-to-Mind handoff:

`utterance event truth -> recipient-scoped W0 communication stimulus -> represented heard exposure -> Perception Foundation projection -> later MIND-F6 social interpretation`.

Preserve:
`uttered/sent != delivered != heard/read != perception input != understood != believed != remembered != relationship change != response intention != response action`.

No second production character and no fake production conversation were introduced.

Canonical W5 docs:
- `docs/COMMUNICATION_EXPOSURE_FOUNDATION_V1.md`
- `docs/W5_IMPLEMENTATION_PLAN_V1.md`
- `docs/W5_ACCEPTANCE_NOTES_V1.md`

## Completed minimum World Input + handoff stack

Foundation-complete at the current minimum scope:
- W0 World Stimulus / Exposure Foundation
- W1 Environment / Weather Foundation
- W1.1 Historical Weather Provider
- W2 Commitments / Obligations Foundation
- W3 Money / Economy Foundation
- W3.1 Universe Object Valuation & Creation Rules
- W4 Information / Media Foundation
- W4.1 Historical News Provider
- first-class Media Console consumption / W0 exposure
- W5 Communication Exposure Foundation v1
- **Perception Foundation v1 — W0 exposure -> actor-relative Mind input handoff**

The preferred W0 W1-W5 minimum producer sequence and its minimum exposure-to-perception handoff are now closed sufficiently to begin Mind runtime activation.

## Exact next implementation checkpoint — MIND-F2 Mental Episode Runtime

Read `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md` before implementation.

MIND-F2 should activate the already-reserved Mental Cycle / Mental Episode substrate at **meaningful bounded cognition boundaries**, not through continuous per-minute LLM thought polling.

Minimum responsibilities:
- character-owned Mental Episode creation at justified decision/cognition boundaries;
- consume represented current state, the existing `perception` socket, recallable Character Memory and other authorized context;
- preserve provenance/links to represented inputs where applicable;
- make episodes inspectable/auditable without turning them into world truth;
- keep action proposal and deterministic action authority separate;
- avoid prematurely implementing F3 attention/appraisal, F4 intention, F5 planning, F6 social cognition, or F7 relationship adaptation except for typed sockets already reserved by the foundation.

Do not let MIND-F2 read global W0 stimuli directly. External information must arrive through actor-owned exposure -> `perception`.

Canonical continuation:
`MIND-F2 Mental Episode Runtime -> MIND-F3 Attention/Appraisal/Active Concerns -> MIND-F4 Intention -> MIND-F5 Planning -> MIND-F6 Social Cognition/Communication -> MIND-F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real character seed`.

## Second-character seed gate

Do not seed the next real production character merely to exercise unfinished Mind/social foundations.

Current gate:
1. W0-W5 minimum producers — **satisfied**;
2. exposure-to-perception handoff — **satisfied by Perception Foundation v1**;
3. MIND-F2..F7 minimum foundations;
4. reconcile interim A3.3 planning scaffolding into canonical Mind intention/planning where appropriate;
5. Foundation Completion Review v2;
6. only then may the next real production character seed be proposed/authorized.

That character should become live multi-character acceptance evidence, not a development test dummy.

## A3.3 — Bounded Multi-Step Destination Intent v1 — DEPLOYED / NATURAL OBSERVATION CONTINUES

A3.3 remains production-green through Deploy #287 and independent of Mind progression.

It provides actor-known bounded route-purpose awareness (max 4 hops) while exact executable movement remains deterministic current `action_options` authority. No full Mind plan exists yet.

Natural production proof for the previously missing inside-to-outside initiation remains read-only observation. Do not force an outing. If the gap persists after ordinary opportunities, inspect evidence and make only generic corrections.

When MIND-F4/F5 activate, reconcile A3.3/interim purpose scaffolding into typed Mind intention/plan flow and reduce/remove duplicate prompt-level planning guidance.

## W4 / W5 continuity

W4/W4.1 were implemented before A3.3 and remain deployed. W5 was deployed in PR #267 / Deploy #288. Publication, communication availability, delivery/exposure, perception, belief, Memory, Mind and action authority remain distinct layers.

## Operational diagnostics — DEPLOYED

- PR #258 — health-probe quoting fix / Deploy #283;
- PR #259 — Diagnostics v1 / Deploy #284;
- PR #260 — path-aware CI/acceptance triggers;
- PR #261 — Diagnostics v2 / Deploy #285;
- PR #262 — deploy-safe/production-truth correction / Deploy #286.

Creator-only Telegram diagnostics remain:
`/logs`, `/logs errors [lines]`, `/logs system [lines]`, `/logs runtime`, `/logs file [lines]`.

The production `observer` user has persistent `systemd-journal` read access.

## Estate / outside-world lock

Estate-first scope remains active. Broader South Lake Tahoe traversal remains intentionally paused: no public-road edge from Main Security Gate, Tahoe-backcountry edge from Concealed Forest Passage, or water-travel edge from Hidden Dock is open.

## Exact resume point

**Perception Foundation v1 is production-green through PR #269 / CI #1054 / Deploy #289, with schema v15 unchanged. The previously missing W0 exposure -> actor-relative perception socket is now closed through a bounded provenance-preserving read projection and no Memory/Mind/action mutation. The exact next implementation slice is MIND-F2 Mental Episode Runtime. Continue F2 -> F3 -> F4 -> F5 -> F6 -> F7, then Foundation Completion Review v2 before any next real production character seed. A3.3 inside-to-outside natural observation continues independently and must not be forced.**
