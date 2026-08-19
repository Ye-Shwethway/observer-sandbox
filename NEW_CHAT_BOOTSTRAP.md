# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: **2026-08-19**

## Startup / authority

Read and reconcile in order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical docs/source
5. verified production before runtime decisions.

Authority:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

Persistent branches are `main` and `test`.

Workflow:
`develop on test -> focused tests + final PR CI -> merge test into main -> automatic deploy when runtime-affecting -> production verification -> continuity sync -> main/test synchronization`.

Never claim production deployment without independent deploy/runtime evidence or explicit live verification.

## Current repository checkpoint

### PR #294 — Proactive Sandbox Observer Delivery I5.1

Merged:
`63443494231368e65c4701971765b24c9c04bdaf`

Final head:
`ec7f7e55d10ca67bcac0b652ccb66b353d0ee324`

Evidence:
- CI #1091 — **SUCCESS**;
- schema remains v20.

I5.1 connects sandbox observer delivery to the existing runtime service loop, not the Telegram polling loop. Proactive Sandbox Updates default OFF; enabling establishes a current-event baseline, preventing historical backlog spam. Delivery respects the global Telegram notification preference, aggregates only whitelisted sandbox lifecycle/config/runtime-control facts, and advances its cursor only after successful send.

No autonomous sandbox activity is invented. `runtime_ready != running` remains locked.

### PR #293 — Sandbox Observer / Notifications I5

Merged:
`7b3a18cf2e5caf16171034566439e303509e816c`

Final head:
`4a2bb067228598ff54261bfdae714baba981a326`

Evidence:
- CI #1090 — **SUCCESS**;
- Inventory Foundation #104 — **SUCCESS**;
- schema v20.

Canonical contract:
`docs/SANDBOX_OBSERVER_NOTIFICATIONS_I5.md`.

Sandbox World now exposes `📡 Observer` with sandbox-owned per-owner preference/cursor state, recent sandbox-event feed, update toggle and Mark Current Seen. Event selection is an explicit whitelist. Unknown/future events do not silently become proactive notifications.

### PR #291 — Sandbox Character Configuration UX I4.1

Merged:
`ad799cc621630978fd8fda9c8ae0d4d3a5ca4a9b`

Evidence:
- CI #1084 — **SUCCESS**.

Sandbox Character detail exposes `⚙️ Configure` for represented Location assignment, deterministic runtime-option refresh, isolated per-Character cognition AI, Sandbox clock and readiness. Acceptance proves `runtime_ready` while `autonomy_enabled=0` and canonical state unchanged.

### PR #290 — Guided Creator Studio dual-pattern UX

Merged:
`c742309bf4c2480d8184e030b830d98cb0975b35`

Evidence:
- CI #1083 — **SUCCESS**.

Normal creation flow:
`Creator Studio -> Create -> Character | Location -> Build Manually | Generate with AI -> next-message name/description -> Draft Preview`.

Commands remain optional shortcuts. Guided input is one-shot and presentation-scoped.

### PR #288 — Creator Studio I4

Merged:
`2cec0e44b85d9ffaa489344d9202594735dac13b`

Proposal lifecycle:
`Creator intent -> Manual or AI Draft -> Sandbox Draft -> Preview -> Explicit Approve -> Sandbox Object`.

A draft is not a sandbox object. A sandbox object is not canonical. Creator Creation AI has proposal authority only.

### Earlier Creator Creation foundations

- PR #286 / I3: isolated Character profile/skills, Location containment and represented affordances; merge `bf0ed6fbd508b66db026d3a4861b2237354e2691`.
- PR #284 / I2.5: isolated sandbox clock/speed/pause, Character readiness, AI assignment and runtime options; merge `afedd4a3bc966b2cd09985ad26fda87adf0347ba`.
- PR #283 / I2: isolated Creation Sandbox persistence and world-layer Telegram navigation; merge `b8c92ba28f551533190d50f0ac8cb9be2fa75003`.
- PR #281 / I0-I1: generic Creator authority, universal Character/Location proposal sockets and Creator Creation AI settings; merge `c60ba00921e1a14132c4422d1e96eed2e623b2ab`.

Lifecycle:
`created -> configured -> runtime_ready -> running -> stopped`.

Full sandbox autonomous ticking is **not implemented**.

## AI binding facts

Real World backend already supports per-character AI overrides through canonical `ai_bindings` / `resolve_binding()`. Do not rebuild that resolver. Explicit Real World Telegram per-character assignment UX remains a separate gap.

Creation Sandbox Character AI assignments are isolated while provider/model catalog metadata is shared. Never insert `sbx_*` IDs into canonical Character bindings.

## Creator Staging & Transmigration

> **Create anywhere safely; canon nowhere automatically.**

> **schema-valid does not imply universe-compatible.**

All Creator creations begin isolated. Canonical activation requires target-universe compatibility validation plus explicit Creator approval in a future atomic transmigration transaction.

Supernatural/impossible-physics concepts may be sandbox-valid yet incompatible with the current realistic universe. Future universe profiles may permit them. Do not smuggle new system concepts into arbitrary Character profile keys.

Canonical docs include:
- `docs/UNIVERSAL_CREATION_SOCKET_FOUNDATION_V1.md`
- `docs/CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md`
- `docs/CREATOR_CREATION_FULL_ROADMAP_V1.md`
- `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/SANDBOX_RUNTIME_READINESS_FOUNDATION_V1.md`
- `docs/SANDBOX_CHARACTER_LOCATION_VERTICAL_I3.md`
- `docs/TELEGRAM_CREATOR_STUDIO_I4.md`
- `docs/SANDBOX_CHARACTER_CONFIGURATION_I4_1.md`
- `docs/SANDBOX_OBSERVER_NOTIFICATIONS_I5.md`.

## Immediate implementation route

- I0 Creator authority — **COMPLETE**;
- I1 universal proposal/socket core — **COMPLETE**;
- I2 isolated Creation Sandbox persistence/lifecycle — **COMPLETE**;
- I2.5 isolated sandbox runtime/time/AI/readiness — **COMPLETE**;
- I3 Character + Location representation proof — **COMPLETE**;
- I4 Creator Studio proposal lifecycle — **COMPLETE**;
- I4 guided dual-pattern creation UX — **COMPLETE**;
- I4.1 Sandbox Character configuration UX — **COMPLETE**;
- I5 Sandbox Observer foundation — **COMPLETE**;
- I5.1 proactive Sandbox Observer delivery — **COMPLETE**;
- I6 target-universe compatibility/transmigration planning contract — **NEXT**;
- then resume MIND-F2.

## I6 rules

I6 is planning/validation only. Do not create an actual canonical apply path for a Character.

Minimum:
- freeze/select a sandbox object revision or explicit sandbox snapshot;
- choose a target universe compatibility profile;
- compute dependency closure;
- expose a deterministic compatibility-validator interface;
- return structured result taxonomy;
- build proposed canonical mutations without applying them;
- prove incompatible planning creates zero canonical writes.

Recommended proof:
- compatible harmless Location -> valid promotion plan in disposable/test state;
- intentionally supernatural/impossible exemplar -> rejected by current realistic target profile;
- Character promotion remains gate-blocked.

Do not build a full multi-universe runtime in I6.

## Sandbox time / observer controls

Sandbox Runtime buttons remain isolated from Real World time controls. Sandbox time may initialize from a Real World timestamp snapshot and then diverge independently.

Sandbox Observer proactive updates default OFF and are opt-in. Observer feed history remains viewable independently of proactive delivery.

The internal `/sandbox ...` helper is still not publicly wired.

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

## Mind continuation

MIND-F2 remains deferred through I6. Then:
`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real Character transmigration proposal`.

## Existing runtime locks

W0-W5 plus Perception Foundation v1 remain the completed external-input foundation. PR #278 protects Creator edits from seed/evidence snap-back. PR #279 provides Body Preserve Shape completeness.

A3.3 remains deployed. Continue read-only natural observation; do not force Darian outside. Reconcile interim route-purpose scaffolding into canonical Mind planning when F4/F5 activate.

## Production evidence boundary

Latest independently recorded production checkpoint remains Perception Foundation v1 / Deploy #289. PRs #293 and #294 are repository/CI verified. Their runtime-affecting main merges should trigger deployment, but a newer production deploy is **not independently verified here**. Direct Telegram/runtime evidence can establish a newer live checkpoint.

## Exact resume point

**I5 and I5.1 are merged. PR #293 merge `7b3a18cf2e5caf16171034566439e303509e816c`, CI #1090 SUCCESS, Inventory Foundation #104 SUCCESS, schema v20. PR #294 merge `63443494231368e65c4701971765b24c9c04bdaf`, CI #1091 SUCCESS. Sandbox World has a Creator-only Observer feed and opt-in proactive delivery for real sandbox lifecycle/config/runtime-control events, with isolated cursor state and no historical backlog on enable. Full sandbox autonomous execution is not implemented. Next authorized slice: I6 target-universe compatibility/transmigration planning contract only. Do not add or promote another canonical Character.**
