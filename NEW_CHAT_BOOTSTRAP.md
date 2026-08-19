# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: **2026-08-19**

## Startup / authority

Read and reconcile in order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical docs/source
5. verified production before runtime implementation decisions.

Authority:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

Persistent branches are `main` and `test`.

Default workflow:
`develop on test -> focused tests + final PR CI -> merge test into main -> automatic deploy when runtime-affecting -> production verification -> continuity sync -> test/main synchronization`.

Never claim production deployment without independent deploy/runtime evidence.

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

Initial CI #1077 reached `808 passed / 1 failed`; the only failure was a stale schema-v17 expectation in the prior sandbox acceptance. All new I3 tests passed on the first run. After narrow alignment to schema v18, final CI was green.

Canonical contract:
`docs/SANDBOX_CHARACTER_LOCATION_VERTICAL_I3.md`.

I3 provides isolated but canonical-vocabulary-compatible Character representation:
- sandbox profile values reference canonical `profile_field_definitions`;
- sandbox skills use an isolated canonical-equivalent record shape;
- unknown Character profile fields fail closed.

Location representation now supports sandbox-only parent/containment with cycle rejection.

Runtime options are deterministically projected from represented Character + current Location capabilities, limited to canonical `ACTION_NAMES`. Future Item/Element/System sockets extend these derivation sources rather than bypassing the boundary.

A Character can now reach `runtime_ready` after Location + represented options + sandbox cognition AI + sandbox clock are configured. **`runtime_ready` is still not `running`. Full sandbox autonomous execution is not implemented.**

### PR #284 — Sandbox Runtime Readiness Foundation v1

Merged:
`afedd4a3bc966b2cd09985ad26fda87adf0347ba`

Evidence:
- CI #1076 — SUCCESS;
- Inventory Foundation v1 Acceptance #94 — SUCCESS;
- schema v17 at that checkpoint.

Creation and activation are separate:
`created -> configured -> runtime_ready -> running -> stopped`.

Sandbox owns isolated sim time, speed, pause/resume, Character readiness state, Character cognition AI assignment and runtime options. Canonical Real World runtime state and canonical AI bindings remain separate.

### PR #283 — Creation Sandbox isolation + world-layer navigation

Merged:
`b8c92ba28f551533190d50f0ac8cb9be2fa75003`

Creation Sandbox uses isolated `sbx_*` IDs and separate object/relation/event state. Telegram `/start` hierarchy is:
`Observer Home -> Real World | Sandbox World | Creator Settings`.

Real World owns Universe / Characters / Runtime / History / Inventory. Sandbox World owns Universe / Characters / Locations / Runtime / History and is Creator-only.

### PR #281 — Creator Creation I0/I1

Merged:
`c60ba00921e1a14132c4422d1e96eed2e623b2ab`

Generic authority precedence:
`Creator-approved live state > simulation-owned live state > ordinary seed/default`.

I1 provides sandbox-only Character/Location proposal sockets and the `Creator Settings -> AI Settings -> Character AI / News Generation AI / Creator Creation AI` hierarchy.

## AI binding facts

Canonical Real World backend already supports per-character AI overrides through `ai_bindings` and `resolve_binding()`. Do not rebuild that resolver.

Remaining Real World gap is Telegram/configuration UX for explicit per-character assignment.

Creation Sandbox stores sandbox Character bindings separately while reusing the shared provider/model catalog. Never insert `sbx_*` Character IDs into ordinary canonical Character bindings.

## Creator Staging & Transmigration architecture

Core principles:

> **Create anywhere safely; canon nowhere automatically.**

> **schema-valid does not imply universe-compatible.**

All Creator creations begin isolated. Canonical activation requires target-universe compatibility validation plus explicit Creator approval in an atomic transmigration transaction.

Supernatural/impossible-physics systems may be sandbox-valid yet incompatible with the current realistic universe; future universe profiles may permit them. Such concepts must use future dedicated socket/system vocabulary, not arbitrary Character profile fields.

Canonical docs:
- `docs/UNIVERSAL_CREATION_SOCKET_FOUNDATION_V1.md`
- `docs/CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md`
- `docs/CREATOR_CREATION_FULL_ROADMAP_V1.md`
- `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/SANDBOX_RUNTIME_READINESS_FOUNDATION_V1.md`
- `docs/SANDBOX_CHARACTER_LOCATION_VERTICAL_I3.md`.

## Immediate implementation route

- I0 Creator authority hardening — **COMPLETE / MERGED**;
- I1 universal proposal/socket core — **COMPLETE / MERGED**;
- I2 isolated Creation Sandbox persistence/lifecycle — **COMPLETE / MERGED**;
- I2.5 isolated sandbox runtime/time/AI/readiness — **COMPLETE / MERGED**;
- I3 Character + Location vertical representation proof — **COMPLETE / MERGED**;
- I4 Telegram Creator Studio with Manual + AI Draft + preview/edit/reroll + explicit sandbox approval + readiness configuration — **NEXT**;
- I5 sandbox-specific Telegram notifications;
- I6 target-universe compatibility/transmigration planning boundary;
- then resume MIND-F2.

## I4 rules

Use the existing universal proposal path for both manual and AI creation. Do not create separate backends.

Minimum owner-only Creator Studio should provide:
- Create;
- Sandbox Creations;
- Character / Location;
- Build Manually | Generate with AI;
- Preview / Edit / Reroll / Validate;
- explicit Approve into Sandbox;
- reset/delete/manage existing sandbox creations.

AI may generate a structured draft only. It has no direct DB or canonical-write authority.

Character configuration should expose existing readiness requirements: Location assignment, represented affordances/options, sandbox cognition AI assignment and sandbox clock configuration. Creation must not imply activation.

Do not enable full autonomous sandbox execution in I4 unless a separate safe sandbox execution adapter is explicitly authorized and implemented.

## Sandbox time controls

Sandbox Runtime button surface exists and is separate from Real World runtime controls. Sandbox clock can be initialized from current Real World time as a one-time copied value, then diverges independently.

An internal `/sandbox ...` command helper exists but is not yet wired into public Telegram command handling. Do not claim `/sandbox` works until that wiring is added.

## Second-character gate remains closed

Do not activate/transmigrate another real production Character before:
1. W0-W5/perception foundations remain healthy;
2. Creator profile/body controls remain stable;
3. minimum Creator Creation staging threshold is complete;
4. MIND-F2..F7 minimum foundations are complete;
5. Relationship Adaptation foundation is complete;
6. A3.3 interim planning scaffolding is reconciled;
7. Foundation Completion Review v2 passes;
8. Creator explicitly approves canonical transmigration.

Sandbox Characters do not violate this gate.

## Mind Engine continuation

MIND-F2 remains deferred until minimum Creator Creation staging is stable.

Then:
`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real character transmigration proposal`.

## Existing runtime locks

W0-W5 plus Perception Foundation v1 remain the completed external-input foundation. PR #278 protects Creator edits from ordinary seed snap-back/evidence replay. PR #279 provides Body Preserve Shape completeness.

A3.3 remains deployed. Continue read-only natural observation; do not force Darian outside. Reconcile interim route-purpose scaffolding into canonical Mind planning when F4/F5 activate.

## Production evidence boundary

Latest independently recorded production checkpoint remains Perception Foundation v1 / Deploy #289. PRs #278-#286 are repo/CI verified. Runtime-affecting main merges trigger the canonical deploy workflow, but do not claim a newer production deploy without independent deploy/runtime evidence or explicit live verification.

## Exact resume point

**PR #286 is merged at `bf0ed6fbd508b66db026d3a4861b2237354e2691` after CI #1078 SUCCESS and Inventory Foundation Acceptance #96 SUCCESS. Schema v18. Sandbox Character profile/skills reuse canonical vocabulary in isolated state; sandbox Location containment is cycle-safe; represented Character/current-Location capabilities derive runtime options; the vertical can reach `runtime_ready` without canonical mutations. Full sandbox autonomous execution is not implemented. Next authorized slice: I4 minimum Telegram Creator Studio and readiness configuration. Do not add another canonical Character.**