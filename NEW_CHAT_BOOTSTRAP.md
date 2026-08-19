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

### PR #288 — Telegram Creator Studio I4

Merged:
`2cec0e44b85d9ffaa489344d9202594735dac13b`

Final head:
`418df9ac8e4b45875f26f1c267657b21675b3f96`

Evidence:
- CI #1080 — **SUCCESS**
- Inventory Foundation v1 Acceptance #98 — **SUCCESS**
- Inventory Operations v1 Acceptance #54 — **SUCCESS**
- schema v19.

Initial CI #1079 reached `813 passed / 1 failed`; the only failure was a prior sandbox-isolation assertion hard-coded to schema v18. New I4 tests passed on the first run. Narrow schema alignment produced final green CI #1080.

Canonical contract:
`docs/TELEGRAM_CREATOR_STUDIO_I4.md`.

Creator Studio now provides owner-only:
- Sandbox World -> `🛠 Creator Studio`;
- `/studio`;
- `/create character <name>`;
- `/create location <name>`;
- `/createai character <description>`;
- `/createai location <description>`;
- draft preview;
- AI reroll;
- cancel;
- explicit Approve into Sandbox.

Proposal lifecycle:

`Creator intent -> Manual or AI Draft -> Sandbox Draft -> Preview -> Explicit Approve -> Sandbox Object`.

A draft is not a sandbox object. A sandbox object is not canonical. Creator Creation AI has proposal authority only and cannot directly activate sandbox objects, write canonical universe state or transmigrate creations.

### PR #286 — Sandbox Character + Location Vertical Proof I3

Merged:
`bf0ed6fbd508b66db026d3a4861b2237354e2691`

I3 provides isolated Character profile/skills using canonical profile vocabulary, cycle-safe Location containment and deterministic Character/current-Location capability projection into runtime options. The vertical can reach `runtime_ready` without canonical writes.

### PR #284 — Sandbox Runtime Readiness Foundation

Merged:
`afedd4a3bc966b2cd09985ad26fda87adf0347ba`

Lifecycle:
`created -> configured -> runtime_ready -> running -> stopped`.

Sandbox owns separate clock/speed/pause, Character readiness, sandbox cognition AI assignment and runtime options. Full sandbox autonomous ticking remains **not implemented**.

### PR #283 — Creation Sandbox isolation + world layers

Merged:
`b8c92ba28f551533190d50f0ac8cb9be2fa75003`

Telegram `/start` hierarchy:
`Observer Home -> Real World | Sandbox World | Creator Settings`.

Sandbox objects use isolated `sbx_*` identities and separate object/relation/event/runtime state.

### PR #281 — Creator Creation I0/I1

Merged:
`c60ba00921e1a14132c4422d1e96eed2e623b2ab`

Generic authority precedence:
`Creator-approved live state > simulation-owned live state > ordinary seed/default`.

AI settings hierarchy:
`Creator Settings -> AI Settings -> Character AI / News Generation AI / Creator Creation AI`.

## AI binding facts

Real World backend already supports per-character AI overrides through `ai_bindings` / `resolve_binding()`. Do not rebuild that resolver.

Remaining Real World gap is Telegram UX for explicit per-character assignment.

Creation Sandbox stores sandbox Character AI assignments separately while sharing the provider/model catalog. Never insert `sbx_*` Character IDs into canonical bindings.

## Creator Staging & Transmigration

> **Create anywhere safely; canon nowhere automatically.**

> **schema-valid does not imply universe-compatible.**

All Creator creations begin isolated. Canonical activation requires target-universe compatibility validation plus explicit Creator approval in a future atomic transmigration transaction.

Supernatural/impossible-physics systems may be sandbox-valid yet incompatible with the current realistic universe. Future universes may use different compatibility profiles. Do not smuggle new system concepts into arbitrary Character profile keys.

Canonical docs:
- `docs/UNIVERSAL_CREATION_SOCKET_FOUNDATION_V1.md`
- `docs/CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md`
- `docs/CREATOR_CREATION_FULL_ROADMAP_V1.md`
- `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/SANDBOX_RUNTIME_READINESS_FOUNDATION_V1.md`
- `docs/SANDBOX_CHARACTER_LOCATION_VERTICAL_I3.md`
- `docs/TELEGRAM_CREATOR_STUDIO_I4.md`.

## Immediate implementation route

- I0 Creator authority hardening — **COMPLETE**;
- I1 universal proposal/socket core — **COMPLETE**;
- I2 isolated Creation Sandbox persistence/lifecycle — **COMPLETE**;
- I2.5 isolated sandbox runtime/time/AI/readiness — **COMPLETE**;
- I3 Character + Location representation proof — **COMPLETE**;
- I4 Telegram Creator Studio proposal lifecycle — **COMPLETE**;
- I4.1 Creator Studio Character configuration UX — **NEXT**;
- I5 sandbox-specific notifications;
- I6 target-universe compatibility/transmigration planning;
- then resume MIND-F2.

## I4.1 rules

Extend existing Studio; do not create another creation backend.

Minimum next UX:
- select a Sandbox Character;
- assign/change a represented Sandbox Location;
- inspect/refresh derived runtime options;
- assign/change sandbox cognition AI from shared provider/model catalog;
- expose sandbox clock state;
- show one consolidated readiness checklist;
- profile/Body/Skill editing only through existing sandbox representation vocabulary.

Do not automatically run a Character when readiness becomes green. `runtime_ready != running`.

Full sandbox autonomous execution still requires a separate sandbox-safe execution adapter and explicit authorization.

## Sandbox time controls

Sandbox Runtime buttons are live and isolated from Real World time controls. Sandbox time can initialize from Real World time as a one-time copy, then diverge independently.

An internal `/sandbox ...` helper exists but is not publicly wired. Do not claim that command works until it is wired.

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

Latest independently recorded production checkpoint remains Perception Foundation v1 / Deploy #289. PRs through #288 are repo/CI verified. Runtime-affecting main merges trigger deploy workflow, but do not claim a newer deploy without independent deploy/runtime evidence or explicit live verification.

## Exact resume point

**PR #288 is merged at `2cec0e44b85d9ffaa489344d9202594735dac13b` after CI #1080 SUCCESS, Inventory Foundation #98 SUCCESS and Inventory Operations #54 SUCCESS. Schema v19. Creator Studio now supports owner-only Manual/AI Character and Location drafts, Preview/Reroll/Cancel and explicit Approve into Creation Sandbox. Drafts do not create sandbox objects before approval and never mutate canonical state. Full sandbox autonomy execution is not implemented. Next authorized slice: I4.1 — Sandbox Character configuration UX for Location, per-character sandbox AI, derived runtime options and readiness. Do not add another canonical Character.**