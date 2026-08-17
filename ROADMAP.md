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
- Do not seed another real production character merely to test unfinished foundations; use generic test fixtures until the foundation-completion gate is reached.

## Current production checkpoint

**W5 Communication Exposure Foundation v1 is COMPLETE / DEPLOYED.**

Latest evidence:
- PR #267 — `Add W5 communication exposure foundation`
- final tested head `03519395b89b9ba7fae3d0db8c9d1b4ad0fe102b`
- CI #1053 / run `32044642343`: SUCCESS
- merge `520ebd9d10077bf1880acf75414e29ca258dbac9`
- **Deploy #288 / run `32044773094`: SUCCESS**
- production after deploy: canonical service active, runtime log ready, SQLite readable, `PRAGMA quick_check=ok`, schema **v15 unchanged**, Gemini cognition recovery validated without mutation, Telegram API healthy.

A3.3 remains deployed below this checkpoint and continues read-only natural behavioral observation. W4/W4.1 were already deployed before A3.3.

## W5 — Communication Exposure Foundation v1 — DEPLOYED / MINIMUM COMPLETE

Canonical contracts:
- `docs/COMMUNICATION_EXPOSURE_FOUNDATION_V1.md`
- `docs/W5_IMPLEMENTATION_PLAN_V1.md`
- `docs/W5_ACCEPTANCE_NOTES_V1.md`

Runtime exemplar:
- `src/observer_sandbox/communication.py`
- `tests/test_communication_exposure_v1.py`

### Purpose

W5 closes the final minimum producer in the W0 preferred W1-W5 sequence while intentionally stopping before interpretation, reply generation, social cognition, relationship adaptation, or another production character seed.

Canonical separation:
`uttered/sent != delivered != heard/read != understood != believed != remembered != relationship change != response intention != response action`.

Canonical flow:
`communication event truth -> W0 communication stimulus -> represented delivery/exposure -> future perception -> later social appraisal/inference -> response intention -> utterance/action proposal -> deterministic authority`.

### Direct-utterance exemplar

Minimum runnable behavior:
- sender/intended recipients are represented character entities;
- utterance truth is recorded through existing `events` + `event_participants`;
- recipient-scoped W0 `communication` stimuli preserve source event/entity provenance;
- intended recipient gets W0 exposure only if co-located with sender at utterance boundary;
- non-co-located intended recipient gets no exposure;
- unrelated co-located actors do not receive targeted communication;
- invalid/non-character/self-recipient identities fail closed.

No new communication schema was needed. W5 reuses existing:
- event truth/participants;
- dynamic location state;
- W0 stimuli/scopes;
- W0 character exposures.

Schema remains v15.

### Acceptance boundary

Fixture-based automated acceptance proves architecture/runtime correctness with arbitrary temporary character IDs. Those fixtures are **not** canonical production characters.

W5 does not yet prove:
- natural live conversation between production characters;
- autonomous dialogue generation;
- social meaning/intent inference;
- reply intention;
- relationship adaptation;
- asynchronous/device-message delivery.

Do not fabricate a second production character or fake live conversation for proof.

### Future device communication

If a real later consumer requires it, preserve:
`message truth -> represented endpoint/device delivery -> recipient read/access -> W0 device exposure`.

Phones, contacts, inboxes, network availability and similar systems should be added only when concrete represented behavior needs them.

## Completed minimum World Input producer stack

### W0 — World Stimulus / Exposure — DEPLOYED
Shared external-input boundary. Availability != exposure; exposure != perception/belief/memory/thought/action authority.

### W1 / W1.1 Weather — DEPLOYED
Registry-driven historical weather through universe simulation time and W0 exposure boundaries.

### W2 Commitments / Obligations — DEPLOYED
Appointment/promise/deadline/scheduled-responsibility truth and notices without automatic planning.

### W3 / W3.1 Economy — DEPLOYED
Accounts/ledger/assets/liabilities/valuation/affordability with W0 financial notices and explicit valuation policy.

### W4 / W4.1 Information & Media — DEPLOYED
Historical simulation-time news, Media Console TV exemplar, Morning 07:00 / Evening 18:00 scheduling, generic `consume_media`, and W0 media exposure without belief/Memory/Mind bypass.

### W5 Communication Exposure — DEPLOYED
Generic direct communication truth and targeted co-location exposure foundation. Social interpretation/response remains later Mind work.

**The preferred W0 W1-W5 minimum producer sequence is now complete at foundation level.**

## Next checkpoint — Perception-gap audit

Before activating MIND-F2, audit the current repository for the exact handoff from W0 `character_exposures` into actor-relative perceived information.

Relevant canonical facts:
- W0 explicitly stops at exposure and describes a later perception handoff;
- exposure means the signal reached the actor boundary, not that it was understood or believed;
- Intelligent Mind Engine Foundation treats perceived information as a distinct layer and reserves bounded `perception` input.

Do not create a new Perception subsystem merely because the name is absent. First inspect source/runtime for an equivalent already-implemented bridge.

Audit decision:
- **bridge already sufficient** -> document evidence and proceed to MIND-F2;
- **bridge genuinely missing** -> implement the smallest generic Perception Runtime required to convert represented exposures into bounded actor-relative perceived inputs with provenance, while creating no belief, durable Memory, appraisal, intention, plan or action authority.

## Intelligent Mind Engine route — PRE-PLANNED CANONICAL SEQUENCE

After the Perception-gap decision:

### MIND-F2 — Mental Episode Runtime
Activate bounded character-owned mental episodes at meaningful cognition boundaries, not continuous thought polling.

### MIND-F3 — Attention / Appraisal / Active Concerns
Represent actor-relative attention, interpreted significance and unresolved active concern state. External salience is not mental importance.

### MIND-F4 — Intention Foundation
Typed near-term intention candidates/artifacts may influence proposals but never become executable authority.

### MIND-F5 — Planning
Bounded plan candidates/artifacts and multi-step continuity grounded in recallable memory and authoritative present state. Reconcile/retire duplicate A3.3 interim planning guidance here.

### MIND-F6 — Social Cognition / Communication
Interpret represented W5 communication/social exposure using perception, person-context/memory and active Mind state; form social inference and response intentions. No chatbot ping-pong shortcut.

### MIND-F7 — Relationship Adaptation
Adapt relationship state downstream of represented social evidence and interpretation rather than raw communication directly mutating trust/attachment/etc.

Canonical product route:
`Perception-gap audit -> [minimum Perception Runtime only if required] -> MIND-F2 -> MIND-F3 -> MIND-F4 -> MIND-F5 -> MIND-F6 -> MIND-F7 -> Foundation Completion Review v2 -> next real character seed`.

## Second-character seed gate

A second real production character is intentionally deferred until the foundation stack can support that character without using them as a development scaffold.

Required gate:
1. W0-W5 minimum producer foundations complete — **now satisfied**;
2. perception handoff audited/closed;
3. MIND-F2..F7 minimum foundations complete;
4. interim A3.3 planning scaffolding reconciled into canonical Mind planning where appropriate;
5. Foundation Completion Review v2 confirms no blocking cross-system foundation gap;
6. only then propose/authorize the next canonical character seed.

The second character should serve as live multi-character architecture acceptance, not as a test dummy required to make unfinished communication/social systems function.

## A3.3 — Bounded Multi-Step Destination Intent v1 — DEPLOYED / OBSERVATION CONTINUES

A3.3 provides actor-known bounded route-purpose hints (max 4 hops) while deterministic one-hop `action_options` remain sole movement authority.

Natural proof of the previously missing inside-to-outside initiation is still being observed read-only. Do not force an outing. This observation is independent of W5/Mind implementation progress.

When MIND-F4/F5 activate, migrate/reconcile any durable route purpose into typed Mind intention/plan flow and reduce/remove duplicate prompt-level scaffolding.

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

**W5 Communication Exposure Foundation v1 is production-green through Deploy #288. No second character was seeded and no fake production conversation was used. The next implementation task is a source/runtime Perception-gap audit. Add a minimal Perception Runtime only if evidence proves the exposure-to-perception bridge is absent; otherwise proceed directly to MIND-F2. Continue through F2-F7, then run Foundation Completion Review v2 before any next real character seed. A3.3 natural inside-to-outside observation continues independently.**
