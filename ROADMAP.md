# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-19

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, verified live runtime/DB and current CI/deploy evidence outrank remembered chat context.
- AI proposes; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Creator-approved live state outranks ordinary seed/default refresh.
- Creator-created objects stage in Creation Sandbox first; sandbox approval and canonical transmigration are separate authority transitions.
- **Created is not alive.** Creation, runtime readiness and runtime execution are separate boundaries.
- Real World and Creation Sandbox mutable state must remain isolated.

## Current repository checkpoint

### PR #294 — Proactive Sandbox Observer Delivery I5.1

Merged:
`63443494231368e65c4701971765b24c9c04bdaf`

Final head:
`ec7f7e55d10ca67bcac0b652ccb66b353d0ee324`

Evidence:
- CI #1091 — **SUCCESS**;
- schema remains v20.

I5.1 wires the proven sandbox notification dispatcher into the normal runtime service loop rather than the Telegram long-poll loop. The service may deliver unseen whitelisted sandbox events even when no canonical actor is currently active.

Proactive Sandbox Updates:
- default OFF;
- first enable establishes the current sandbox event ID as baseline, so historical events are not dumped as a backlog;
- require both global Telegram notifications and Sandbox Updates to be enabled;
- aggregate whitelisted lifecycle/config/runtime-control facts only;
- advance the per-owner sandbox cursor only after successful delivery;
- retain pending events after transport failure;
- never invent autonomous sandbox activity.

`runtime_ready` remains distinct from `running`. I5.1 does not implement sandbox autonomous execution.

### PR #293 — Sandbox Observer / Notification Foundation I5

Merged:
`7b3a18cf2e5caf16171034566439e303509e816c`

Final head:
`4a2bb067228598ff54261bfdae714baba981a326`

Evidence:
- CI #1090 — **SUCCESS**;
- Inventory Foundation v1 Acceptance #104 — **SUCCESS**;
- schema v20.

Canonical contract:
`docs/SANDBOX_OBSERVER_NOTIFICATIONS_I5.md`.

I5 adds isolated `(sandbox_id, Telegram user_id)` notification preference/cursor state, a deterministic event whitelist/formatter/dispatcher, and `Sandbox World -> 📡 Observer` with update toggle, recent feed and Mark Current Seen.

Initial CI #1085 reached `817 passed / 4 failed`: three older slice tests incorrectly pinned the global schema version and one compact UI rewrite dropped Character/Location names from sandbox list text. The older acceptance responsibilities were cleaned up and list labels restored; observer semantics did not need redesign.

### PR #291 — Sandbox Character Configuration UX I4.1

Merged:
`ad799cc621630978fd8fda9c8ae0d4d3a5ca4a9b`

Evidence:
- CI #1084 — **SUCCESS**.

`Sandbox World -> Characters -> Character -> Configure` provides Location assignment, deterministic runtime-option refresh, sandbox-owned per-Character cognition AI selection, Sandbox clock initialization/state and consolidated readiness. Acceptance proves `runtime_ready` can be reached while `autonomy_enabled=0` and canonical state remains unchanged.

Canonical contract:
`docs/SANDBOX_CHARACTER_CONFIGURATION_I4_1.md`.

### PR #290 — Guided Creator Studio dual-pattern UX

Merged:
`c742309bf4c2480d8184e030b830d98cb0975b35`

Evidence:
- CI #1083 — **SUCCESS**.

Normal creation path is inline-first:
`Creator Studio -> Create -> Character | Location -> Build Manually | Generate with AI -> next-message name/description -> Draft Preview`.

Commands `/studio`, `/create`, `/createai` remain optional shortcuts. The guided next-message router is one-shot/presentation-scoped.

### PR #288 — Telegram Creator Studio I4

Merged:
`2cec0e44b85d9ffaa489344d9202594735dac13b`

Evidence:
- CI #1080 — **SUCCESS**;
- Inventory Foundation #98 — **SUCCESS**;
- Inventory Operations #54 — **SUCCESS**.

Proposal lifecycle:
`Creator intent -> Manual or AI Draft -> Sandbox Draft -> Preview -> Explicit Approve -> Sandbox Object`.

A draft is not a sandbox object. A sandbox object is not canonical. Creator Creation AI has proposal authority only.

### Earlier Creator Creation foundations

- PR #286 / I3: isolated Character profile/skills, Location containment and represented affordance projection; merge `bf0ed6fbd508b66db026d3a4861b2237354e2691`.
- PR #284 / I2.5: isolated sandbox clock/speed/pause, Character readiness, AI assignment and runtime options; merge `afedd4a3bc966b2cd09985ad26fda87adf0347ba`.
- PR #283 / I2: isolated Creation Sandbox persistence and Real World/Sandbox World Telegram layers; merge `b8c92ba28f551533190d50f0ac8cb9be2fa75003`.
- PR #281 / I0-I1: generic Creator authority + universal Character/Location proposal sockets + Creator Creation AI settings; merge `c60ba00921e1a14132c4422d1e96eed2e623b2ab`.

Lifecycle remains:
`created -> configured -> runtime_ready -> running -> stopped`.

Full sandbox autonomous ticking is **not implemented**.

## AI model architecture

Real World backend already supports Character-scoped bindings through `ai_bindings` / `resolve_binding()`. Do not rebuild that resolver. Explicit Telegram UX for Real World per-character assignment remains a separate gap.

Creation Sandbox owns separate Character AI assignments while reusing the shared provider/model catalog. Never place `sbx_*` Character IDs into canonical Character bindings.

## Creator Staging & Transmigration

> **Create anywhere safely; canon nowhere automatically.**

> **schema-valid does not imply universe-compatible.**

All Creator-created content begins in isolated staging state. Transmigration is a separate Creator-approved atomic boundary after target-universe compatibility validation.

Supernatural/system concepts may be sandbox-valid while incompatible with the current realistic universe and valid in a future universe profile. Do not smuggle new concepts into arbitrary Character profile keys.

Canonical docs:
- `docs/UNIVERSAL_CREATION_SOCKET_FOUNDATION_V1.md`
- `docs/CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md`
- `docs/CREATOR_CREATION_FULL_ROADMAP_V1.md`
- `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/SANDBOX_RUNTIME_READINESS_FOUNDATION_V1.md`
- `docs/SANDBOX_CHARACTER_LOCATION_VERTICAL_I3.md`
- `docs/TELEGRAM_CREATOR_STUDIO_I4.md`
- `docs/SANDBOX_CHARACTER_CONFIGURATION_I4_1.md`
- `docs/SANDBOX_OBSERVER_NOTIFICATIONS_I5.md`.

## Creator Creation implementation route

- I0 Creator authority hardening — **COMPLETE / MERGED**;
- I1 universal socket/proposal foundation — **COMPLETE / MERGED**;
- I2 isolated Creation Sandbox persistence/lifecycle — **COMPLETE / MERGED**;
- I2.5 sandbox runtime/time/AI/readiness ownership — **COMPLETE / MERGED**;
- I3 Character + Location vertical representation proof — **COMPLETE / MERGED**;
- I4 Telegram Creator Studio proposal lifecycle — **COMPLETE / MERGED**;
- I4 guided dual-pattern UX — **COMPLETE / MERGED**;
- I4.1 Sandbox Character configuration UX — **COMPLETE / MERGED**;
- I5 Sandbox Observer foundation — **COMPLETE / MERGED**;
- I5.1 proactive Sandbox Observer delivery — **COMPLETE / MERGED**;
- I6 target-universe compatibility/transmigration planning contract — **NEXT**;
- then return to MIND-F2.

## I6 next-slice boundary

I6 is **planning/validation only**. The production second-Character gate remains closed.

Minimum:
- select/freeze one sandbox object revision or explicit sandbox snapshot;
- choose a target universe compatibility profile;
- compute dependency closure;
- run a deterministic compatibility-validator interface;
- return structured compatible/incompatible/dependency/error results;
- build proposed canonical mutations without applying them;
- prove incompatible planning creates zero canonical writes.

Recommended disposable proof:
- a harmless compatible Location can produce a canonical promotion plan in test state without application;
- an intentionally impossible/supernatural exemplar is rejected against the current realistic universe profile;
- no Character may be promoted to the Real World during I6.

Do not add a general multi-universe runtime or actual canonical apply path in I6.

## Time/control ownership

Real World canonical clock/speed/pause remain canonical runtime state. Creation Sandbox owns independent clock/speed/pause state.

Sandbox Runtime button controls are separate from Real World. The internal `/sandbox ...` command helper remains not publicly wired.

## Second-character gate

No second real production Character may be activated/transmigrated before:
1. W0-W5/perception foundations remain healthy;
2. Creator profile/body controls remain stable;
3. minimum Creator Creation staging threshold is complete;
4. MIND-F2..F7 minimum foundations are complete;
5. Relationship Adaptation foundation is complete;
6. A3.3 interim planning scaffolding is reconciled;
7. Foundation Completion Review v2 passes;
8. Creator explicitly approves the canonical transmigration.

Sandbox Characters do not violate this gate.

## Mind continuation

MIND-F2 remains deferred through I6. Then:
`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real Character transmigration proposal`.

## Production evidence boundary

Latest independently recorded production checkpoint in continuity remains Perception Foundation v1 / Deploy #289. PRs #293 and #294 are repository/CI verified, and runtime-affecting merges should trigger the deploy workflow, but production success is **not independently verified here**. Telegram/live runtime evidence may establish a newer production checkpoint later.

## Exact resume point

**I5 + I5.1 are merged. PR #293 merge `7b3a18cf2e5caf16171034566439e303509e816c`, CI #1090 SUCCESS, Inventory Foundation #104 SUCCESS, schema v20. PR #294 merge `63443494231368e65c4701971765b24c9c04bdaf`, CI #1091 SUCCESS. Sandbox World now has a Creator-only Observer feed and a proactive delivery path for real sandbox lifecycle/config/runtime-control events with isolated preference/cursor state and no backlog-on-enable. No autonomous sandbox action execution exists. Next route: I6 target-universe compatibility/transmigration planning contract only. Do not add or promote another canonical Character.**
