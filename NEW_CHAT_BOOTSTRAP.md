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

### PR #291 — Sandbox Character Configuration UX I4.1

Merged:
`ad799cc621630978fd8fda9c8ae0d4d3a5ca4a9b`

Final head:
`daf853944cc3ee08e34b23f876f2c3c8393492c8`

Evidence:
- CI #1084 — **SUCCESS**;
- schema remains v19.

Canonical contract:
`docs/SANDBOX_CHARACTER_CONFIGURATION_I4_1.md`.

Sandbox Character detail now exposes `⚙️ Configure` with one consolidated inline dashboard for:
- represented Sandbox Location assignment;
- deterministic runtime-option refresh;
- isolated per-Character cognition AI selection using the shared enabled provider/model catalog;
- Sandbox clock state and initialization from a read-only Real World time snapshot;
- readiness summary and detailed readiness diagnostics.

Location assignment refreshes options immediately. A fully configured Character may reach `runtime_ready`; acceptance proves `autonomy_enabled=0` remains locked and canonical-state fingerprint stays unchanged. **I4.1 does not run the Character.**

### PR #290 — Guided Creator Studio dual-pattern UX

Merged:
`c742309bf4c2480d8184e030b830d98cb0975b35`

Evidence:
- CI #1083 — **SUCCESS**.

Normal creation path is now inline-first:
`Creator Studio -> Create -> Character | Location -> Build Manually | Generate with AI -> next-message name/description -> Draft Preview`.

The pending text-input session is UI-scoped and one-shot. It is cleared/restored after consumption or cancel. `/studio`, `/create`, `/createai` remain optional shortcuts rather than required UX.

### PR #288 — Telegram Creator Studio I4

Merged:
`2cec0e44b85d9ffaa489344d9202594735dac13b`

Evidence:
- CI #1080 — **SUCCESS**;
- Inventory Foundation #98 — **SUCCESS**;
- Inventory Operations #54 — **SUCCESS**;
- schema v19.

Proposal lifecycle:
`Creator intent -> Manual or AI Draft -> Sandbox Draft -> Preview -> Explicit Approve -> Sandbox Object`.

A draft is not a sandbox object. A sandbox object is not canonical. Creator Creation AI has proposal authority only.

### Earlier Creator Creation foundations

- PR #286 / I3: isolated Character profile/skills, Location containment, represented affordance projection; merge `bf0ed6fbd508b66db026d3a4861b2237354e2691`.
- PR #284 / I2.5: isolated sandbox clock/speed/pause, Character readiness, AI assignment and runtime options; merge `afedd4a3bc966b2cd09985ad26fda87adf0347ba`.
- PR #283 / I2: isolated Creation Sandbox persistence and Real World/Sandbox World Telegram layers; merge `b8c92ba28f551533190d50f0ac8cb9be2fa75003`.
- PR #281 / I0-I1: generic Creator authority + universal Character/Location proposal sockets + Creator Creation AI settings; merge `c60ba00921e1a14132c4422d1e96eed2e623b2ab`.

Lifecycle remains:
`created -> configured -> runtime_ready -> running -> stopped`.

Full sandbox autonomous ticking is **not implemented**.

## AI binding facts

Real World backend already supports per-character AI overrides through canonical `ai_bindings` / `resolve_binding()`. Do not rebuild that resolver. Telegram UX for explicit Real World per-character assignment remains a separate gap.

Creation Sandbox stores Character AI assignments separately while sharing provider/model catalog metadata. I4.1 exposes this isolated assignment in Telegram. Never insert `sbx_*` Character IDs into canonical bindings.

## Creator Staging & Transmigration

> **Create anywhere safely; canon nowhere automatically.**

> **schema-valid does not imply universe-compatible.**

All Creator creations begin isolated. Canonical activation requires future target-universe compatibility validation plus explicit Creator approval in an atomic transmigration transaction.

Supernatural/impossible-physics systems may be sandbox-valid yet incompatible with the current realistic universe. Future universes may use different compatibility profiles. Do not smuggle new system concepts into arbitrary Character profile keys.

Canonical docs include:
- `docs/UNIVERSAL_CREATION_SOCKET_FOUNDATION_V1.md`
- `docs/CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md`
- `docs/CREATOR_CREATION_FULL_ROADMAP_V1.md`
- `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/SANDBOX_RUNTIME_READINESS_FOUNDATION_V1.md`
- `docs/SANDBOX_CHARACTER_LOCATION_VERTICAL_I3.md`
- `docs/TELEGRAM_CREATOR_STUDIO_I4.md`
- `docs/SANDBOX_CHARACTER_CONFIGURATION_I4_1.md`.

## Immediate implementation route

- I0 Creator authority — **COMPLETE**;
- I1 universal proposal/socket core — **COMPLETE**;
- I2 isolated Creation Sandbox persistence/lifecycle — **COMPLETE**;
- I2.5 isolated sandbox runtime/time/AI/readiness — **COMPLETE**;
- I3 Character + Location representation proof — **COMPLETE**;
- I4 Creator Studio proposal lifecycle — **COMPLETE**;
- I4 guided dual-pattern creation UX — **COMPLETE**;
- I4.1 Sandbox Character configuration UX — **COMPLETE**;
- I5 sandbox-specific notifications/observer flow — **NEXT**;
- I6 target-universe compatibility/transmigration planning;
- then resume MIND-F2.

## I5 rules

I5 must observe only real Creation Sandbox state. Do not fabricate autonomous activity merely to produce notifications.

Minimum direction:
- visibly mark sandbox notifications with `🧪` / Creation Sandbox identity;
- use sandbox lifecycle/configuration/readiness/runtime events only;
- keep notification preferences/baselines separate from canonical Character notification state;
- never imply `runtime_ready` means `running`;
- if no sandbox execution event source exists, notify only on real sandbox configuration/lifecycle/readiness changes.

Full autonomous sandbox execution requires a separate sandbox-safe execution adapter and explicit implementation boundary. Do not smuggle execution into I5.

## Sandbox time controls

Sandbox Runtime buttons remain isolated from Real World time controls. Sandbox time can initialize from Real World time as a snapshot, then diverges independently.

The internal `/sandbox ...` helper is not publicly wired. Do not claim the command works until it is wired.

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

MIND-F2 remains deferred until minimum Creator Creation staging is stable.

Then:
`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real Character transmigration proposal`.

## Existing runtime locks

W0-W5 plus Perception Foundation v1 remain the completed external-input foundation. PR #278 protects Creator edits from seed/evidence snap-back. PR #279 provides Body Preserve Shape completeness.

A3.3 remains deployed. Continue read-only natural observation; do not force Darian outside. Reconcile interim route-purpose scaffolding into canonical Mind planning when F4/F5 activate.

## Production evidence boundary

Latest independently recorded production checkpoint remains Perception Foundation v1 / Deploy #289. PRs through #291 are repo/CI verified. Runtime-affecting main merges trigger deploy workflow, but do not claim a newer production deploy without independent deploy/runtime evidence or explicit live verification.

## Exact resume point

**PR #291 is merged at `ad799cc621630978fd8fda9c8ae0d4d3a5ca4a9b` after CI #1084 SUCCESS. Schema remains v19. PR #290 provides inline guided Manual/AI creation with next-message input while commands remain optional shortcuts. I4.1 provides inline Sandbox Character configuration for Location, isolated per-Character AI, deterministic runtime options, Sandbox clock and readiness. `runtime_ready != running`; autonomy remains disabled and full sandbox execution is not implemented. Next route: I5 sandbox-specific notifications/observer flow using only real sandbox state. Do not add another canonical Character.**