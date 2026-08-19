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

### PR #284 — Sandbox Runtime Readiness Foundation v1

Merged:
`afedd4a3bc966b2cd09985ad26fda87adf0347ba`

Final head:
`eba84ad89b6690a18f3818a40ef972b699479ac1`

Evidence:
- CI #1076 — **SUCCESS**
- Inventory Foundation v1 Acceptance #94 — **SUCCESS**
- schema v17.

Initial CI #1075 reached `803 passed / 1 failed`; the sole failure was a stale schema-v16 assertion. New I2.5 behavior tests passed. After alignment to schema v17, final CI was green.

Canonical contract:
`docs/SANDBOX_RUNTIME_READINESS_FOUNDATION_V1.md`.

Creation and activation are separate:

`created -> configured -> runtime_ready -> running -> stopped`.

A sandbox Character reaches `runtime_ready` only when all exist:
- active Character;
- active sandbox Location assignment;
- represented runtime/action options;
- explicit sandbox cognition AI binding;
- configured sandbox clock.

Full sandbox autonomous ticking is not implemented. Do not describe `runtime_ready` as `running`.

Sandbox owns isolated:
- sim time;
- speed;
- pause/resume state;
- Character activation/readiness state;
- Character cognition AI assignment;
- runtime options.

Canonical Real World runtime state and canonical AI bindings remain separate.

### PR #283 — Creation Sandbox isolation + world-layer navigation

Merged:
`b8c92ba28f551533190d50f0ac8cb9be2fa75003`

Evidence:
- CI #1074 — SUCCESS;
- Inventory Foundation #92 — SUCCESS;
- Inventory Operations #52 — SUCCESS.

Sandbox objects use isolated `sbx_*` IDs and separate object/relation/event tables. Character/Location create, bind, inspect, archive/delete/reset are sandbox-only. Acceptance proves canonical-state fingerprint stability.

Telegram `/start` hierarchy:

`Observer Home -> Real World | Sandbox World | Creator Settings`.

Real World:
- Universe;
- Characters;
- Runtime;
- History;
- Inventory.

Sandbox World:
- Universe;
- Characters;
- Locations;
- Runtime;
- History.

Sandbox World is Creator-only.

### PR #281 — Creator Creation I0/I1

Merged:
`c60ba00921e1a14132c4422d1e96eed2e623b2ab`

Evidence:
- CI #1071 — SUCCESS;
- Skill Progression Foundation v1 Acceptance #109 — SUCCESS.

Generic authority precedence:
`Creator-approved live state > simulation-owned live state > ordinary seed/default`.

I1 provides sandbox-only Character/Location proposal sockets and the Creator Settings -> AI Settings -> Character AI / News Generation AI / Creator Creation AI hierarchy.

## AI binding facts

Canonical Real World backend already supports per-character AI overrides through `ai_bindings` and `resolve_binding()`.

Do not rebuild that resolver.

Remaining Real World gap is Telegram/configuration UX for explicit per-character assignment.

Creation Sandbox stores sandbox Character bindings separately while reusing the shared provider/model catalog:

`shared provider/model catalog -> sandbox-owned Character binding -> future sandbox cognition adapter`.

Never insert `sbx_*` Character IDs into ordinary canonical character bindings.

## Creator Staging & Transmigration architecture

Core principles:

> **Create anywhere safely; canon nowhere automatically.**

> **schema-valid does not imply universe-compatible.**

All Creator creations begin isolated. Canonical activation requires target-universe compatibility validation plus explicit Creator approval in an atomic transmigration transaction.

Supernatural/impossible-physics systems may be sandbox-valid yet incompatible with the current realistic universe; future universe profiles may permit them.

Canonical docs:
- `docs/UNIVERSAL_CREATION_SOCKET_FOUNDATION_V1.md`
- `docs/CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md`
- `docs/CREATOR_CREATION_FULL_ROADMAP_V1.md`
- `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/SANDBOX_RUNTIME_READINESS_FOUNDATION_V1.md`.

## Immediate implementation route

- I0 Creator authority hardening — **COMPLETE / MERGED**;
- I1 universal proposal/socket core — **COMPLETE / MERGED**;
- I2 isolated Creation Sandbox persistence/lifecycle — **COMPLETE / MERGED**;
- I2.5 isolated sandbox runtime/time/AI/readiness — **COMPLETE / MERGED**;
- I3 Character + Location vertical representation proof — **NEXT**;
- I4 Telegram Creator Studio with Manual + AI Draft + configuration;
- I5 sandbox-specific Telegram notifications;
- I6 target-universe compatibility/transmigration planning boundary;
- then resume MIND-F2.

## I3 rules

Reuse existing ontology; do not invent parallel ad-hoc Character/Profile/Location systems.

Character should gain meaningful identity/profile/body/skill/capability representation.

Location should gain parent/containment plus represented affordances/elements.

Runtime options must be derived from represented content or explicitly approved universal actions; do not fabricate options simply to make readiness pass.

I3 may prove `runtime_ready`, but must not enable full autonomous sandbox execution until sandbox adapters can safely read/write sandbox-owned profile/location/runtime state.

## Sandbox time controls

Sandbox Runtime Telegram button surface exists and is separate from Real World runtime controls. Sandbox clock can be initialized from the current Real World time as a one-time copied value, then diverges independently.

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

W0-W5 plus Perception Foundation v1 remain the completed external-input foundation.

PR #278 protects Creator edits from ordinary seed snap-back/evidence replay. PR #279 provides Body Preserve Shape completeness.

A3.3 remains deployed. Continue read-only natural observation; do not force Darian outside. Reconcile interim route-purpose scaffolding into canonical Mind planning when F4/F5 activate.

## Production evidence boundary

Latest independently recorded production checkpoint remains Perception Foundation v1 / Deploy #289. PRs #278-#284 are repo/CI verified. Runtime-affecting main merges trigger the canonical deploy workflow, but do not claim a newer production deploy without independent deploy/runtime evidence or explicit live verification.

## Exact resume point

**PR #284 is merged at `afedd4a3bc966b2cd09985ad26fda87adf0347ba` after CI #1076 SUCCESS and Inventory Foundation Acceptance #94 SUCCESS. Schema v17. Creation Sandbox owns isolated clock/speed/pause, Character readiness state, sandbox-only cognition AI assignments, runtime options, and Telegram Runtime/Readiness surfaces. Creation does not imply activation; full sandbox autonomous ticking is not implemented. Next authorized slice: I3 Character + Location vertical representation with real affordance-derived options, stopping at `runtime_ready`. Do not add another canonical Character.**