# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-19

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition or Creator drafts; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve world truth, exposure, perception, memory, Mind and action-authority separation.
- Use minimum-runnable reversible slices; prefer exemplar-first, then batch-by-pattern.
- Character-specific behavioral hard-coding is forbidden.
- Persistent branches are only `main` and `test`; normal development occurs on `test` and is promoted after validation.
- Prefer vertical completeness and operational usefulness over subsystem sprawl.
- Reconcile roadmap/bootstrap at material checkpoints and do not claim production without deploy/runtime evidence.
- Do not seed another real production character merely to test unfinished foundations.
- Creator-approved live state outranks ordinary seed/default refresh. Seed/import/reinitialize may initialize missing or unclaimed baseline state but must not silently overwrite Creator-owned state.
- Creator-created objects are staged first. Creation Sandbox approval and canonical-universe transmigration are separate authority transitions.

## Current canonical repository checkpoint

**Creator Creation I0/I1 Foundation is IMPLEMENTED / CI-GREEN / MERGED. Exact push-deploy/runtime verification remains pending independent evidence.**

Repository evidence:
- PR #281 — `Start Creator creation socket foundation`
- final head `51ef1c5267bc8d963bbf498d3b67c17bfa7f86ab`
- CI #1071: **SUCCESS**
- Skill Progression Foundation v1 Acceptance #109: **SUCCESS**
- merge `c60ba00921e1a14132c4422d1e96eed2e623b2ab`
- no schema migration.

The initial CI #1069 reached **792 passed / 2 failed**. Both failures were stale/overly literal test expectations after the approved AI Settings hierarchy change; runtime architecture did not need redesign. Narrow expectation alignment produced final green CI #1071.

### I0 — Creator authority hardening

Canonical precedence now has a reusable project-level root:

`Creator-approved live state > simulation-derived live state > canonical seed/default`.

`src/observer_sandbox/creator_authority.py` defines shared Creator authority/source recognition and ordinary seed replacement policy.

`profile_seed.import_seed()` now uses that shared contract instead of a profile-only source exception. Existing simulated state and Creator-owned profile corrections remain protected across ordinary initialization. The legacy dead-code erectile-field typo shim was removed while preserving the correct canonical field contract.

### I1 — Universal creation socket/proposal foundation

`src/observer_sandbox/creation_socket.py` establishes the initial universal proposal envelope.

Current registered proof sockets:
- Character;
- Location.

Both use the same envelope and are hard-bound to `target_scope = sandbox`.

A proposal cannot request direct canonical activation. Unknown creation types fail closed rather than becoming implicit universe vocabulary.

This is intentionally a proposal/schema foundation only. There is no Creation Sandbox persistence or canonical object mutation yet.

### Creator Creation AI settings

Canonical Telegram hierarchy:

`Creator Settings -> AI Settings -> Character AI / News Generation AI / Creator Creation AI`.

Creator Creation AI uses an independent role binding:
- scope type `engine`;
- scope id `creator_creation`;
- role `creator_creation_assist`.

It has provider/model selection plus a real structured-output capability probe. The role may draft Creation Sandbox proposals only; configuring or probing the model grants no canonical write authority.

Canonical docs:
- `docs/CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md`
- `docs/UNIVERSAL_CREATION_SOCKET_FOUNDATION_V1.md`
- `docs/CREATOR_CREATION_FULL_ROADMAP_V1.md`
- `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/CREATOR_CREATION_AI_SETTINGS_V1.md`
- `docs/CREATOR_CREATION_I0_I1_ACCEPTANCE_V1.md`

## Creator Staging & Transmigration architecture

Core rule:

**Create anywhere safely; canon nowhere automatically.**

Creator-created Character, Location, Quest, Job, Skill, Item, Organization, Service, world element, system/rule descriptor and future creation types must first exist in isolated Creation Sandbox state.

The sandbox shares approved universe engines/rules but not canonical mutable state.

Sandbox lifecycle supports revision, reroll, clone, reset, delete/archive and testing without affecting the current canonical universe.

Canonical activation is a separate explicit Creator-approved transmigration transaction.

Before transmigration, the target universe must validate:
- schema compatibility;
- references/dependencies;
- world ontology;
- realism/genre/rule policy;
- required runtime capabilities;
- conflicts and forbidden assumptions.

Therefore **schema-valid does not imply universe-compatible**. A supernatural power/system may be valid sandbox data yet be rejected by the current realistic universe. A future fantasy universe may legitimately accept the same creation type under a different target-universe policy.

Transmigration is atomic: failure leaves canonical state unchanged.

## Creator Creation implementation route

Full roadmap is C0-C9 in `docs/CREATOR_CREATION_FULL_ROADMAP_V1.md`.

Minimum current implementation route is intentionally smaller:

- I0 Creator authority hardening — **COMPLETE / MERGED**;
- I1 universal socket/proposal foundation — **COMPLETE / MERGED**;
- I2 isolated Creation Sandbox persistence/lifecycle — **NEXT**;
- I3 Character + Location end-to-end sandbox proof;
- I4 Telegram Creator Studio minimum surface: manual build + AI draft + preview/edit/reroll + explicit sandbox approval;
- I5 sandbox-specific observer/notification surface;
- I6 target-universe compatibility/transmigration planning and proof without unlocking the second real character gate;
- then return to MIND-F2.

Do not prebuild every creation type in I2-I6. Character + Location are the initial vertical proof; later Quest/Job/Skill/Item/System sockets expand by the same registry pattern.

## Second-character seed/transmigration gate

Do not activate/transmigrate another real production character into the current universe before:
1. W0-W5 minimum external inputs — satisfied;
2. Perception handoff — satisfied;
3. Creator profile editing + Body v2 production verification;
4. minimum Creator Creation staging threshold;
5. MIND-F2..F7 minimum foundations;
6. Relationship Adaptation foundation;
7. A3.3 interim planning scaffolding reconciliation;
8. Foundation Completion Review v2;
9. explicit Creator authorization of the target character's canonical transmigration.

Sandbox characters do not violate this gate because they are not canonical-universe participants.

## Creator Character Profile Editing & Body Targeting

Creator profile editing remains preview-first, atomic and auditable. Raw represented values remain authoritative; grades remain read-time derived.

Body Preserve Shape targeting v2.1 is merged through PR #279 and now propagates grade-target adjustments through represented muscular circumferences while retaining target-grade forward verification and hard anchors such as height.

Creator profile corrections are protected from ordinary seed snap-back through the generic authority contract established in I0.

## Perception Foundation v1 — DEPLOYED / MINIMUM COMPLETE

Latest independently verified production checkpoint remains:
- PR #269
- CI #1054 / run `32045634180`: SUCCESS
- merge `ebe5bb923c90c77dd878bd6e485e20d7fc68dea7`
- Deploy #289 / run `32045825836`: SUCCESS
- service/runtime log/SQLite/Telegram/cognition recovery healthy;
- schema v15.

Do not claim a newer production deployment until independent push-deploy/runtime evidence is available.

## Completed minimum external-input stack

- W0 World Stimulus / Exposure — DEPLOYED
- W1 / W1.1 Weather — DEPLOYED
- W2 Commitments / Obligations — DEPLOYED
- W3 / W3.1 Economy / Valuation — DEPLOYED
- W4 / W4.1 Information / Media — DEPLOYED
- W5 Communication Exposure — DEPLOYED
- Perception Foundation v1 — DEPLOYED

## Intelligent Mind Engine route

Canonical: `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`.

MIND-F2 remains the next Mind slice but is intentionally deferred until the minimum Creator Creation staging threshold is reached.

Then:
`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real character transmigration proposal`.

No sandbox character automatically becomes Memory/Mind/social canon for current-universe characters.

## A3.3 — Bounded Multi-Step Destination Intent v1

A3.3 remains deployed. Continue read-only natural observation of inside-to-outside multi-hop initiation; do not force an outing. When F4/F5 activate, migrate/retire duplicate interim route-purpose scaffolding into canonical Mind intention/plan flow.

## Operational diagnostics

Creator-only Telegram diagnostics remain available beneath Creator Settings.

## World / spatial lock

Estate-first scope remains active. Broader public South Lake Tahoe traversal stays closed until explicitly authorized.

## Exact resume point

**PR #281 is merged at `c60ba00921e1a14132c4422d1e96eed2e623b2ab` after CI #1071 SUCCESS and Skill Progression Acceptance #109 SUCCESS. I0/I1 now provide generic Creator authority precedence, sandbox-only Character/Location creation proposal sockets, an independent Creator Creation AI binding/probe, and the `Creator Settings -> AI Settings` hierarchy. No Creation Sandbox persistence, canonical creation/transmigration, schema migration, or second character was introduced. Exact newer deployment evidence is not independently verified. Next implementation slice: I2 — isolated Creation Sandbox persistence/lifecycle.**