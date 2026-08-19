# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-19

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, verified live runtime/DB and current CI/deploy evidence outrank remembered chat context.
- AI proposes; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Use minimum-runnable reversible slices; do not add another canonical character merely to test unfinished foundations.
- Creator-approved live state outranks ordinary seed/default refresh.
- Creator-created objects are staged first; Creation Sandbox approval and canonical transmigration are separate authority transitions.
- **Created is not alive.** Character creation and runtime activation are separate lifecycle boundaries.
- Real World and Creation Sandbox mutable runtime state must remain isolated.

## Current repository checkpoint

### PR #284 — Sandbox Runtime Readiness Foundation v1

Merged:
`afedd4a3bc966b2cd09985ad26fda87adf0347ba`

Final head:
`eba84ad89b6690a18f3818a40ef972b699479ac1`

Evidence:
- CI #1076 — **SUCCESS**
- Inventory Foundation v1 Acceptance #94 — **SUCCESS**
- schema v17.

Initial CI #1075 reached `803 passed / 1 failed`. The only failure was an I2 test hard-coded to schema v16. It was aligned to v17 plus the new sandbox runtime tables; runtime implementation did not require redesign.

I2.5 now provides sandbox-owned:
- simulation clock;
- speed and pause state;
- Character activation/readiness state;
- per-sandbox-Character cognition AI assignment using the shared provider/model catalog;
- represented runtime/action options;
- readiness evaluation and lifecycle cleanup;
- Telegram Sandbox Runtime and Character Runtime Readiness surfaces.

Canonical rule:

`created -> configured -> runtime_ready -> running -> stopped`

A sandbox Character may become `runtime_ready` only when all are true:
1. active sandbox Character exists;
2. active sandbox Location is assigned;
3. at least one represented runtime/action option exists;
4. explicit sandbox cognition AI binding exists;
5. sandbox clock is configured.

Full sandbox autonomous ticking is **not** implemented yet. `runtime_ready` must not be presented as `running`.

Canonical contract:
`docs/SANDBOX_RUNTIME_READINESS_FOUNDATION_V1.md`.

### PR #283 — Isolated Creation Sandbox state + world-layer navigation

Merged:
`b8c92ba28f551533190d50f0ac8cb9be2fa75003`

Evidence:
- final CI #1074 — SUCCESS;
- Inventory Foundation #92 — SUCCESS;
- Inventory Operations #52 — SUCCESS;
- schema v16 at that checkpoint.

Creation Sandbox persistence is isolated from canonical `entities`, `relations`, runtime/autonomy membership and ordinary history. Sandbox objects use `sbx_*` IDs and support Character/Location activation, binding, inspection, archive/delete/reset. Acceptance proves canonical-state fingerprint stability across sandbox-only operations.

Telegram `/start` now uses upper world layers:

`Observer Home -> Real World | Sandbox World | Creator Settings`.

Real World owns existing Universe / Characters / Runtime / History / Inventory surfaces.

Sandbox World owns sandbox Universe / Characters / Locations / Runtime / History surfaces.

### PR #281 — Creator Creation I0/I1 Foundation

Merged:
`c60ba00921e1a14132c4422d1e96eed2e623b2ab`

Evidence:
- CI #1071 — SUCCESS;
- Skill Progression Foundation v1 Acceptance #109 — SUCCESS.

I0 provides generic Creator-authority precedence:

`Creator-approved live state > simulation-owned live state > ordinary seed/default`.

I1 provides shared sandbox-only Character/Location proposal sockets and the Creator Settings -> AI Settings -> Character AI / News Generation AI / Creator Creation AI hierarchy.

## AI model architecture

Canonical Real World backend already supports character-scoped AI bindings through `ai_bindings` and `resolve_binding()` precedence. Character-specific backend infrastructure therefore does not need rebuilding.

Current gap: Telegram Character AI settings do not yet fully expose an explicit per-Real-World-character assignment workflow. Treat this as a configuration UX follow-up, not a resolver redesign.

Creation Sandbox uses a separate assignment table. Do not write `sbx_*` Character IDs into canonical character bindings.

Architecture:

`shared provider/model catalog -> scope-owned Character binding -> scope-owned cognition runtime`.

## Creator Staging & Transmigration architecture

Core rules:

> **Create anywhere safely; canon nowhere automatically.**

> **schema-valid does not imply universe-compatible.**

All Creator-created Character, Location, Quest, Job, Skill, Item, Organization, Service, world element and future system/rule descriptors begin in isolated Creation Sandbox state.

Transmigration remains a separate Creator-approved atomic transaction after target-universe validation. Supernatural/impossible-physics systems may be valid sandbox content yet remain incompatible with the current realistic universe; a future universe profile may accept them.

Canonical docs:
- `docs/UNIVERSAL_CREATION_SOCKET_FOUNDATION_V1.md`
- `docs/CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md`
- `docs/CREATOR_CREATION_FULL_ROADMAP_V1.md`
- `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/SANDBOX_RUNTIME_READINESS_FOUNDATION_V1.md`.

## Creator Creation implementation route

- I0 Creator authority hardening — **COMPLETE / MERGED**;
- I1 universal socket/proposal foundation — **COMPLETE / MERGED**;
- I2 isolated Creation Sandbox persistence/lifecycle — **COMPLETE / MERGED**;
- I2.5 sandbox runtime/time/AI/readiness ownership — **COMPLETE / MERGED**;
- I3 Character + Location vertical representation proof — **NEXT**;
- I4 Telegram Creator Studio: manual + AI draft + preview/edit/reroll + sandbox approval + configuration;
- I5 sandbox-specific notifications/observer flow;
- I6 target-universe compatibility/transmigration planning boundary;
- then return to MIND-F2.

## I3 next-slice boundary

I3 should enrich Character and Location using existing ontology rather than inventing parallel ad-hoc data.

Character minimum:
- canonical-equivalent identity/profile/body representation where reusable;
- skills/preferences/capabilities only through existing definitions;
- sandbox lifecycle and readiness presentation.

Location minimum:
- type/category;
- parent/containment;
- represented affordances/elements;
- enough real local choices to derive sandbox runtime options.

Do not hand-author fake runtime options solely to make readiness green. Options should be derived from represented location/elements/capabilities or explicitly approved universal actions.

I3 may prove `runtime_ready`; it must not start full autonomous sandbox execution until sandbox adapters can safely read/write sandbox-owned character/profile/location/state.

## Time/control ownership

Real World canonical clock/speed/pause remain in canonical runtime state.

Creation Sandbox owns an independent clock/speed/pause namespace. Telegram Sandbox Runtime currently supports explicit button controls and initialization from Real World time as a one-time copy; changing sandbox controls must not mutate Real World time state.

A `/sandbox ...` command helper exists internally but is not yet wired as a public Telegram command. Do not document the command as live until wiring is completed.

## Second-character gate

No second real production character may be activated/transmigrated into the current universe before:
1. W0-W5/perception foundations remain healthy;
2. Creator profile/body controls remain stable;
3. minimum Creator Creation staging threshold is complete;
4. MIND-F2..F7 minimum foundations are complete;
5. Relationship Adaptation foundation is complete;
6. A3.3 interim planning scaffolding is reconciled;
7. Foundation Completion Review v2 passes;
8. Creator explicitly approves that Character's canonical transmigration.

Sandbox Characters do not violate this gate because they are not canonical-universe participants.

## Mind Engine continuation

MIND-F2 remains deferred until the minimum Creator Creation threshold is stable.

Then:
`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real character transmigration proposal`.

## Existing completed foundations

External-input stack remains W0-W5 plus Perception Foundation v1.

Creator profile/body corrections remain protected by PR #278; Body Preserve Shape completeness remains merged through PR #279.

A3.3 Bounded Multi-Step Destination Intent remains deployed. Continue read-only natural observation; do not force Darian outside. Reconcile interim route-purpose scaffolding when F4/F5 become canonical.

## Production evidence boundary

Latest independently recorded deploy checkpoint in continuity remains Perception Foundation v1 / Deploy #289. PRs #278-#284 are repository/CI verified as recorded above. Runtime-affecting merges trigger the canonical main-push deploy workflow, but do not claim a newer production deployment without independent deploy/runtime evidence or explicit live verification.

## Exact resume point

**PR #284 is merged at `afedd4a3bc966b2cd09985ad26fda87adf0347ba` after CI #1076 SUCCESS and Inventory Foundation Acceptance #94 SUCCESS. Schema is v17. Creation Sandbox now owns isolated clock/speed/pause, sandbox Character readiness state, sandbox-only cognition AI assignments, runtime options, and Telegram Runtime/Readiness surfaces. Character creation does not imply activation; full sandbox autonomy ticking is not implemented. Next authorized slice: I3 Character + Location vertical representation with real affordance-derived choices, stopping at `runtime_ready`. Do not add another canonical character.**