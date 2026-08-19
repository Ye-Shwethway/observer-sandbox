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
- **Created is not alive.** Character creation, runtime readiness and runtime execution are separate lifecycle boundaries.
- Real World and Creation Sandbox mutable runtime state must remain isolated.

## Current repository checkpoint

### PR #286 — Sandbox Character + Location Vertical Proof I3

Merged:
`bf0ed6fbd508b66db026d3a4861b2237354e2691`

Final head:
`a84d9233f2e57d4401c738bc29619de5c55c35dc`

Evidence:
- CI #1078 — **SUCCESS**
- Inventory Foundation v1 Acceptance #96 — **SUCCESS**
- schema v18.

Initial CI #1077 reached `808 passed / 1 failed`. The only failure was the prior I2.5 acceptance hard-coded to schema v17. All new I3 representation, containment and affordance tests passed on the first run. Narrow schema-expectation alignment produced final green CI #1078.

I3 now provides:
- sandbox-owned Character profile values using canonical `profile_field_definitions` as shared vocabulary;
- sandbox-owned Character skill rows with canonical-equivalent record shape;
- sandbox Location parent/containment with cycle rejection;
- deterministic Character + current-Location capability projection into canonical action-name runtime options;
- end-to-end proof that Location + represented options + cognition AI + sandbox clock can reach `runtime_ready` without canonical writes.

Unknown Character profile fields fail closed. New concepts such as supernatural powers must use future dedicated creation sockets/system vocabulary rather than arbitrary Character profile fields.

Canonical contract:
`docs/SANDBOX_CHARACTER_LOCATION_VERTICAL_I3.md`.

### PR #284 — Sandbox Runtime Readiness Foundation v1

Merged:
`afedd4a3bc966b2cd09985ad26fda87adf0347ba`

Evidence:
- CI #1076 — SUCCESS;
- Inventory Foundation v1 Acceptance #94 — SUCCESS;
- schema v17 at that checkpoint.

I2.5 established sandbox-owned clock/speed/pause, Character readiness state, per-sandbox-Character cognition AI assignment, represented runtime options, lifecycle cleanup and Telegram Runtime/Readiness surfaces.

Canonical lifecycle:
`created -> configured -> runtime_ready -> running -> stopped`.

Full sandbox autonomous ticking is still **not implemented**. `runtime_ready` must not be presented as `running`.

### PR #283 — Isolated Creation Sandbox state + world-layer navigation

Merged:
`b8c92ba28f551533190d50f0ac8cb9be2fa75003`

Evidence:
- CI #1074 — SUCCESS;
- Inventory Foundation #92 — SUCCESS;
- Inventory Operations #52 — SUCCESS.

Creation Sandbox persistence is isolated from canonical `entities`, `relations`, runtime/autonomy membership and ordinary history. Telegram `/start` uses `Observer Home -> Real World | Sandbox World | Creator Settings`.

### PR #281 — Creator Creation I0/I1 Foundation

Merged:
`c60ba00921e1a14132c4422d1e96eed2e623b2ab`

Evidence:
- CI #1071 — SUCCESS;
- Skill Progression Foundation v1 Acceptance #109 — SUCCESS.

I0 provides generic Creator authority precedence:
`Creator-approved live state > simulation-owned live state > ordinary seed/default`.

I1 provides shared sandbox-only Character/Location proposal sockets and the `Creator Settings -> AI Settings -> Character AI / News Generation AI / Creator Creation AI` hierarchy.

## AI model architecture

Canonical Real World backend already supports Character-scoped AI bindings through `ai_bindings` and `resolve_binding()` precedence. Do not rebuild that resolver.

Remaining Real World gap is Telegram/configuration UX for explicit per-character assignment.

Creation Sandbox stores sandbox Character bindings separately while reusing the shared provider/model catalog. Never write `sbx_*` Character IDs into canonical Character bindings.

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
- `docs/SANDBOX_RUNTIME_READINESS_FOUNDATION_V1.md`
- `docs/SANDBOX_CHARACTER_LOCATION_VERTICAL_I3.md`.

## Creator Creation implementation route

- I0 Creator authority hardening — **COMPLETE / MERGED**;
- I1 universal socket/proposal foundation — **COMPLETE / MERGED**;
- I2 isolated Creation Sandbox persistence/lifecycle — **COMPLETE / MERGED**;
- I2.5 sandbox runtime/time/AI/readiness ownership — **COMPLETE / MERGED**;
- I3 Character + Location vertical representation proof — **COMPLETE / MERGED**;
- I4 Telegram Creator Studio: manual + AI draft + preview/edit/reroll + sandbox approval + readiness configuration — **NEXT**;
- I5 sandbox-specific notifications/observer flow;
- I6 target-universe compatibility/transmigration planning boundary;
- then return to MIND-F2.

## I4 next-slice boundary

Build the minimum owner-only Creator Studio using the already proven proposal and sandbox services.

Minimum UX:
- Create;
- Sandbox Creations;
- Character / Location;
- Build Manually | Generate with AI;
- Preview / Edit / Reroll / Validate;
- explicit Approve into Sandbox;
- reset/delete/manage existing sandbox creations.

Manual and AI modes must converge on the same structured proposal schema and validation/apply boundary. AI has no direct DB or canonical-write authority.

Character configuration should expose the existing readiness dependencies rather than pretending creation means activation: Location assignment, represented affordances/options, sandbox cognition AI assignment and sandbox clock configuration.

Do not start full autonomous sandbox execution in I4 unless a separate safe sandbox execution adapter is explicitly authorized and implemented.

## Time/control ownership

Real World canonical clock/speed/pause remain in canonical runtime state. Creation Sandbox owns independent clock/speed/pause state.

Sandbox Runtime button controls are separate from Real World. An internal `/sandbox ...` command helper exists but is not yet wired as a public Telegram command; do not document it as live until wiring is completed.

## Second-character gate

No second real production Character may be activated/transmigrated into the current universe before:
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

External-input stack remains W0-W5 plus Perception Foundation v1. Creator profile/body corrections remain protected by PR #278; Body Preserve Shape completeness remains merged through PR #279.

A3.3 Bounded Multi-Step Destination Intent remains deployed. Continue read-only natural observation; do not force Darian outside. Reconcile interim route-purpose scaffolding when F4/F5 become canonical.

## Production evidence boundary

Latest independently recorded deploy checkpoint in continuity remains Perception Foundation v1 / Deploy #289. PRs #278-#286 are repository/CI verified as recorded above. Runtime-affecting merges trigger the canonical main-push deploy workflow, but do not claim a newer production deployment without independent deploy/runtime evidence or explicit live verification.

## Exact resume point

**PR #286 is merged at `bf0ed6fbd508b66db026d3a4861b2237354e2691` after CI #1078 SUCCESS and Inventory Foundation Acceptance #96 SUCCESS. Schema is v18. Sandbox Character profile/skills now reuse canonical vocabulary in isolated storage; sandbox Locations support cycle-safe containment; represented Character/current-Location capabilities deterministically derive runtime options; the vertical can reach `runtime_ready` without canonical mutations. Full sandbox autonomy execution is not implemented. Next authorized slice: I4 — minimum Telegram Creator Studio and readiness configuration. Do not add another canonical Character.**