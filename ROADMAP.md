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
- Do not seed another real production character merely to test unfinished foundations; use generic fixtures until the foundation-completion gate is reached.

## Current production checkpoint

**Perception Foundation v1 is COMPLETE / DEPLOYED.**

Latest evidence:
- PR #269 — `Add minimum Perception Foundation v1`
- final tested head `fc33f01272773febe8431c82b29d62ca6e77d2af`
- **CI #1054 / run `32045634180`: SUCCESS**
- merge `ebe5bb923c90c77dd878bd6e485e20d7fc68dea7`
- **Deploy #289 / run `32045825836`: SUCCESS**
- production after deploy: canonical service active, runtime log ready, SQLite readable, `PRAGMA quick_check=ok`, schema **v15 unchanged**, Gemini cognition recovery validated without mutation, Telegram API healthy.

W5 remains deployed below this checkpoint through Deploy #288. A3.3 remains deployed and continues read-only natural inside-to-outside observation independently.

## Perception Foundation v1 — DEPLOYED / MINIMUM COMPLETE

Canonical contract:
- `docs/PERCEPTION_FOUNDATION_V1.md`

Runtime / acceptance:
- `src/observer_sandbox/perception.py`
- `src/observer_sandbox/memory_aware_decision.py`
- `tests/test_perception_foundation_v1.py`

### Audit finding

The required pre-Mind audit found a genuine missing handoff:
- W0 persisted authoritative stimuli/scopes and `character_exposures`, then intentionally stopped at exposure;
- the Mind Foundation reserved `perception` as a distinct bounded input;
- normal cognition did not read exposure rows and no equivalent bridge existed elsewhere.

Therefore Perception Foundation v1 adds the smallest generic bridge instead of a parallel external-input model.

Canonical flow:
`world/event truth -> W0 stimulus -> actual actor exposure -> actor-relative perception input -> later Mind interpretation -> selective memory/intention/plan -> action proposal -> deterministic authority`.

Canonical separation:
`exposure != perception input != understanding != belief != appraisal != memory != thought != intention/plan != action authority`.

### Minimum runtime

Perception v1 is a deterministic bounded read projection over existing W0 exposure/stimulus truth:
- actor-owned `status='exposed'` rows only;
- no future exposure relative to current simulation time;
- invalidated exposure excluded;
- W0 payload/provenance retained;
- stimulus/exposure IDs, channel/type/subject/source links, time, external salience, optional `attention_hint`, and producer metadata exposed as bounded actor context;
- default most-recent limit 8; API hard cap 50;
- projection mode `exposure_projection_v1`.

Normal autonomous cognition receives this context through `MemoryAwareDecisionProvider` at `state["perception"]`.

No new table/schema was introduced because no new durable truth is required at this layer. Schema remains v15.

Perception v1 does not create or imply:
- understanding or belief;
- appraisal/attention allocation/active concern;
- Character Memory;
- Mental Cycle/Episode/Artifact;
- relationship meaning/change;
- intention or plan;
- action option/authority;
- world mutation.

### Acceptance boundary

Automated acceptance + full CI prove:
- valid actor exposure projects with payload/provenance;
- future and invalidated exposures are excluded;
- projection is read-only with respect to events/Memory/Mind;
- normal production cognition provider path includes the `perception` socket;
- existing regressions stay green.

Deploy #289 proves production installation and health.

A naturally occurring post-deploy W0 exposure may later provide a non-empty live perception snapshot. Do not inject a fake production stimulus for acceptance. That observation is not a gate before MIND-F2.

## Completed minimum World Input producer + Perception handoff stack

### W0 — World Stimulus / Exposure — DEPLOYED
Shared external-input boundary. Availability != exposure; exposure != perception/belief/memory/thought/action authority.

### W1 / W1.1 Weather — DEPLOYED
Registry-driven historical weather through universe simulation time and W0 exposure boundaries.

### W2 Commitments / Obligations — DEPLOYED
Appointment/promise/deadline/scheduled-responsibility truth and notices without automatic planning.

### W3 / W3.1 Economy — DEPLOYED
Accounts/ledger/assets/liabilities/valuation/affordability with W0 financial notices and explicit valuation policy.

### W4 / W4.1 Information & Media — DEPLOYED
Historical simulation-time news, Media Console TV exemplar, 07:00 / 18:00 scheduling, generic `consume_media`, and W0 media exposure without belief/Memory/Mind bypass.

### W5 Communication Exposure — DEPLOYED
Generic communication event truth and targeted co-location exposure foundation. Social interpretation/response remains later Mind work.

### Perception Foundation v1 — DEPLOYED
Generic W0 exposure -> actor-relative Mind-input projection with provenance and no interpretation/mutation.

**The preferred W0 W1-W5 minimum producer sequence and the minimum exposure-to-perception handoff are now complete at foundation level.**

## W5 communication path after Perception closure

External communication can now follow:
`utterance event -> recipient-scoped W0 communication stimulus -> represented delivery/heard exposure -> Perception v1 input -> later MIND-F6 social interpretation`.

This still does not activate autonomous dialogue, semantic understanding, reply intention or relationship adaptation, and no second production character has been seeded.

## Intelligent Mind Engine route — ACTIVE NEXT SEQUENCE

`docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md` remains the canonical integration contract. The existing schema already reserves Mental Cycles, Mental Episodes, Mental Artifacts and typed links/sockets. Do not create a competing Mind store.

### MIND-F2 — Mental Episode Runtime — **NEXT**

Activate bounded character-owned Mental Episodes at meaningful cognition boundaries rather than continuous/per-minute LLM thought polling.

Minimum design goals:
- use the existing Mental Cycle/Episode substrate;
- create episodes only at justified bounded cognition/decision boundaries;
- consume authorized present state plus the existing actor-relative `perception` socket and recallable Character Memory;
- preserve traceability to represented inputs/events/memories/entities where relevant;
- keep internal mental interpretation separate from world truth;
- keep episodes distinct from durable Character Memory;
- keep action proposal separate from deterministic execution authority;
- expose enough state for diagnostics/acceptance without dumping uncontrolled chain-of-thought text;
- do not prebuild F3-F7 behavior merely because their schema sockets exist.

External world information must enter MIND-F2 through represented exposure -> Perception, never by querying global active W0 stimuli as if the actor knew them.

### MIND-F3 — Attention / Appraisal / Active Concerns
Represent actor-relative relevance, interpreted significance, attention allocation and unresolved active concern state. External producer salience/`attention_hint` is evidence, not automatically mental importance.

### MIND-F4 — Intention Foundation
Typed near-term intention candidates/artifacts may influence proposals but never become executable authority.

### MIND-F5 — Planning
Bounded plan candidates/artifacts and multi-step continuity grounded in recallable memory, perception and authoritative present state. Reconcile/retire duplicate A3.3 interim planning guidance here.

### MIND-F6 — Social Cognition / Communication
Interpret W5 communication/social exposure through Perception plus person-context/Memory and active Mind state; form social inference and response intentions. No chatbot ping-pong shortcut.

### MIND-F7 — Relationship Adaptation
Adapt relationship interpretation/state downstream of represented social evidence, perception, memory and social cognition rather than raw utterances directly mutating trust/attachment/etc.

Canonical product route:
`MIND-F2 -> MIND-F3 -> MIND-F4 -> MIND-F5 -> MIND-F6 -> MIND-F7 -> Foundation Completion Review v2 -> next real character seed`.

## Second-character seed gate

A second real production character is intentionally deferred until the foundation stack can support that character without using them as a development scaffold.

Required gate:
1. W0-W5 minimum producer foundations — **satisfied**;
2. exposure-to-perception handoff — **satisfied**;
3. MIND-F2..F7 minimum foundations;
4. interim A3.3 planning scaffolding reconciled into canonical Mind planning where appropriate;
5. Foundation Completion Review v2 confirms no blocking cross-system foundation gap;
6. only then propose/authorize the next canonical production character seed.

The second character should become live multi-character architecture acceptance, not a test dummy needed to make unfinished social systems work.

## A3.3 — Bounded Multi-Step Destination Intent v1 — DEPLOYED / OBSERVATION CONTINUES

A3.3 provides actor-known bounded route-purpose hints (max 4 hops) while deterministic one-hop `action_options` remain sole movement authority.

Natural proof of the previously missing inside-to-outside initiation is still being observed read-only. Do not force an outing. This observation is independent of current Mind implementation progress.

When MIND-F4/F5 activate, migrate/reconcile durable route purpose into typed Mind intention/plan flow and reduce/remove duplicate prompt-level scaffolding.

## Operational diagnostics — DEPLOYED

Creator-only Telegram surfaces:
- `/logs`
- `/logs errors [lines]`
- `/logs system [lines]`
- `/logs runtime`
- `/logs file [lines]`

Runtime log, systemd state/journal, read-only SQLite checks and persistent service-user journal access remain production-green.

## CI / acceptance efficiency — DEPLOYED

Full CI covers runtime/code/config/test/script/pyproject/CI changes. Specialized VPS acceptances are path-aware. Docs-only continuity changes do not require full Python pytest.

## World / spatial lock

Estate-first scope remains active. Broader public South Lake Tahoe traversal stays closed: no public-road edge from Main Security Gate, no Tahoe-backcountry edge from Concealed Forest Passage, and no water-travel edge from Hidden Dock unless later explicitly authorized.

## Current exact resume point

**Perception Foundation v1 is production-green through PR #269 / CI #1054 / Deploy #289 with schema v15 unchanged. The audited W0 exposure -> actor-relative perception gap is now closed through a bounded provenance-preserving read projection. The exact next implementation task is MIND-F2 Mental Episode Runtime, using the existing Mind substrate and the new `perception` socket without bypassing world/exposure/memory/action-authority boundaries. Continue F2-F7, then Foundation Completion Review v2 before any next real production character seed. A3.3 natural inside-to-outside observation continues independently.**
