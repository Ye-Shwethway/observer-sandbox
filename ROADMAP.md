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

### PR #291 — Sandbox Character Configuration UX I4.1

Merged:
`ad799cc621630978fd8fda9c8ae0d4d3a5ca4a9b`

Final head:
`daf853944cc3ee08e34b23f876f2c3c8393492c8`

Evidence:
- CI #1084 — **SUCCESS**;
- schema remains v19; no migration.

I4.1 now provides owner-only inline Character configuration from:
`Sandbox World -> Characters -> Character -> Configure`.

The dashboard exposes:
- sandbox Location assignment from active represented Locations;
- automatic deterministic runtime-option refresh after Location assignment;
- explicit runtime-option refresh;
- sandbox-owned per-Character cognition AI selection from the shared enabled provider/model catalog;
- Sandbox clock state and initialization from a read-only Real World time snapshot when unconfigured;
- consolidated readiness checklist and detailed readiness link.

Acceptance proves the configured Character can reach `runtime_ready` while `autonomy_enabled=0`, and canonical-state fingerprint remains unchanged.

Canonical contract:
`docs/SANDBOX_CHARACTER_CONFIGURATION_I4_1.md`.

### PR #290 — Guided Creator Studio dual-pattern UX

Merged:
`c742309bf4c2480d8184e030b830d98cb0975b35`

Evidence:
- final CI #1083 — **SUCCESS**.

Normal Creator Studio creation no longer requires memorizing commands. Guided flow:

`Creator Studio -> Create -> Character | Location -> Build Manually | Generate with AI -> next-message input -> Draft Preview`.

Manual mode requests a name; AI mode requests a natural-language description. The next ordinary owner text message is consumed only for that bounded Studio step. Input session state is presentation-scoped and one-shot; handlers are restored after consumption/cancel. `/studio`, `/create` and `/createai` remain optional power-user shortcuts.

### PR #288 — Telegram Creator Studio I4

Merged:
`2cec0e44b85d9ffaa489344d9202594735dac13b`

Evidence:
- CI #1080 — **SUCCESS**
- Inventory Foundation v1 Acceptance #98 — **SUCCESS**
- Inventory Operations v1 Acceptance #54 — **SUCCESS**
- schema v19.

I4 established sandbox-owned proposal drafts, Manual/AI creation, Preview/Reroll/Cancel and explicit `Approve into Sandbox` for Character/Location using the universal proposal/activation path.

Canonical invariant:
`Creator intent -> Manual or AI Draft -> Sandbox Draft -> Preview -> Explicit Approve -> Sandbox Object`.

A draft is not a sandbox object. A sandbox object is not canonical. Creator Creation AI has proposal authority only and no direct sandbox-object/canonical/transmigration authority.

Canonical contract:
`docs/TELEGRAM_CREATOR_STUDIO_I4.md`.

### PR #286 — Sandbox Character + Location Vertical Proof I3

Merged:
`bf0ed6fbd508b66db026d3a4861b2237354e2691`

I3 provides isolated Character profile/skill representation using canonical field vocabulary, cycle-safe sandbox Location containment, and deterministic Character/current-Location capability projection into runtime options. The vertical can reach `runtime_ready` without canonical writes.

### PR #284 — Sandbox Runtime Readiness Foundation v1

Merged:
`afedd4a3bc966b2cd09985ad26fda87adf0347ba`

I2.5 established sandbox-owned clock/speed/pause, Character readiness state, sandbox cognition AI assignment, runtime options and Telegram Runtime/Readiness surfaces.

Lifecycle:
`created -> configured -> runtime_ready -> running -> stopped`.

Full sandbox autonomous ticking remains **not implemented**.

### PR #283 — Isolated Creation Sandbox + world-layer navigation

Merged:
`b8c92ba28f551533190d50f0ac8cb9be2fa75003`

Creation Sandbox persistence is isolated from canonical entities/relations/runtime/autonomy/history. Telegram `/start` uses `Observer Home -> Real World | Sandbox World | Creator Settings`.

### PR #281 — Creator Creation I0/I1

Merged:
`c60ba00921e1a14132c4422d1e96eed2e623b2ab`

I0 established generic Creator-authority precedence. I1 established universal Character/Location proposal sockets plus `Creator Settings -> AI Settings -> Character AI / News Generation AI / Creator Creation AI`.

## AI model architecture

Real World backend already supports Character-scoped bindings through `ai_bindings` / `resolve_binding()`. Do not rebuild that resolver.

Remaining Real World gap: explicit Telegram UX for assigning per-character AI overrides.

Creation Sandbox owns separate Character AI assignments while reusing the shared provider/model catalog. I4.1 now exposes that sandbox assignment through Telegram. Never place `sbx_*` Character IDs into canonical Character bindings.

## Creator Staging & Transmigration

> **Create anywhere safely; canon nowhere automatically.**

> **schema-valid does not imply universe-compatible.**

All Creator-created Character, Location, Quest, Job, Skill, Item, Organization, Service, world element and future system/rule descriptors begin in isolated staging state.

Transmigration remains a separate Creator-approved atomic transaction after target-universe compatibility validation. Supernatural systems may be valid in Sandbox but incompatible with the current realistic universe and acceptable in a future universe profile.

Canonical docs:
- `docs/UNIVERSAL_CREATION_SOCKET_FOUNDATION_V1.md`
- `docs/CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md`
- `docs/CREATOR_CREATION_FULL_ROADMAP_V1.md`
- `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/SANDBOX_RUNTIME_READINESS_FOUNDATION_V1.md`
- `docs/SANDBOX_CHARACTER_LOCATION_VERTICAL_I3.md`
- `docs/TELEGRAM_CREATOR_STUDIO_I4.md`
- `docs/SANDBOX_CHARACTER_CONFIGURATION_I4_1.md`.

## Creator Creation implementation route

- I0 Creator authority hardening — **COMPLETE / MERGED**;
- I1 universal socket/proposal foundation — **COMPLETE / MERGED**;
- I2 isolated Creation Sandbox persistence/lifecycle — **COMPLETE / MERGED**;
- I2.5 sandbox runtime/time/AI/readiness ownership — **COMPLETE / MERGED**;
- I3 Character + Location vertical representation proof — **COMPLETE / MERGED**;
- I4 Telegram Creator Studio proposal lifecycle — **COMPLETE / MERGED**;
- I4 UX guided dual-pattern refinement — **COMPLETE / MERGED**;
- I4.1 Sandbox Character configuration UX — **COMPLETE / MERGED**;
- I5 sandbox-specific notifications/observer flow — **NEXT**;
- I6 target-universe compatibility/transmigration planning boundary;
- then return to MIND-F2.

## I5 next-slice boundary

Build sandbox-specific observer/notification flow without reusing canonical Character notification state.

Minimum direction:
- Sandbox notification identity must be visibly marked `🧪` and never appear as canonical-world activity;
- sandbox Character/runtime events must be sourced only from Creation Sandbox event/runtime state;
- notification preferences/baselines must not contaminate canonical Character notification baselines;
- no notification may imply `runtime_ready` means `running`;
- if there is no sandbox execution/event source yet, I5 should remain bounded to configuration/lifecycle/readiness notifications rather than inventing autonomous actions.

Full autonomous sandbox action execution still requires a separate sandbox-safe execution adapter and explicit implementation boundary. Do not smuggle execution into I5.

## Time/control ownership

Real World canonical clock/speed/pause remain canonical runtime state. Creation Sandbox owns independent clock/speed/pause state.

Sandbox Runtime button controls are separate from Real World. The internal `/sandbox ...` command helper is still not publicly wired; do not document it as live.

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

Sandbox Characters do not violate this gate.

## Mind continuation

MIND-F2 remains deferred until the minimum Creator Creation threshold is stable.

Then:
`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real Character transmigration proposal`.

## Production evidence boundary

Latest independently recorded production checkpoint in continuity remains Perception Foundation v1 / Deploy #289. PRs through #291 are repository/CI verified as recorded above. Runtime-affecting main merges trigger the canonical deploy workflow, but do not claim a newer production deployment without independent deploy/runtime evidence or explicit live verification.

## Exact resume point

**PR #291 is merged at `ad799cc621630978fd8fda9c8ae0d4d3a5ca4a9b` after CI #1084 SUCCESS. Schema remains v19. Creator Studio has guided inline Manual/AI input from PR #290, and Sandbox Characters now have an inline Configure dashboard for Location, isolated per-Character AI, deterministic options, clock and readiness. A fully configured Character may reach `runtime_ready`, but autonomy remains disabled and full sandbox execution is not implemented. Next route: I5 sandbox-specific notifications/observer flow, bounded to real sandbox state only. Do not add another canonical Character.**