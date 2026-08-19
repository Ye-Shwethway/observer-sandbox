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

Initial CI #1079 reached `813 passed / 1 failed`; the sole failure was a prior sandbox-isolation acceptance hard-coded to schema v18. New I4 tests passed on the first run. After narrow schema-expectation alignment, CI #1080 was green.

I4 now provides:
- Sandbox World -> `🛠 Creator Studio`;
- sandbox-owned, Creator/user-scoped, revisioned proposal drafts;
- `/studio`;
- `/create character <name>`;
- `/create location <name>`;
- `/createai character <description>`;
- `/createai location <description>`;
- preview before mutation;
- AI reroll;
- cancel draft;
- explicit `Approve into Sandbox`;
- Character/Location only, using the already proven universal proposal/activation path.

Canonical invariant:

`Creator intent -> Manual or AI Draft -> Sandbox Draft -> Preview -> Explicit Approve -> Sandbox Object`

A draft is not a sandbox object. A sandbox object is not canonical.

Creator Creation AI uses its independent configured binding and may only draft structured proposals. It has no direct sandbox-object activation authority and no canonical-write/transmigration authority.

Canonical contract:
`docs/TELEGRAM_CREATOR_STUDIO_I4.md`.

### PR #286 — Sandbox Character + Location Vertical Proof I3

Merged:
`bf0ed6fbd508b66db026d3a4861b2237354e2691`

Evidence:
- CI #1078 — SUCCESS;
- Inventory Foundation v1 Acceptance #96 — SUCCESS;
- schema v18 at that checkpoint.

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

Creation Sandbox owns separate Character AI assignments while reusing the shared provider/model catalog. Never place `sbx_*` Character IDs into canonical Character bindings.

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
- `docs/TELEGRAM_CREATOR_STUDIO_I4.md`.

## Creator Creation implementation route

- I0 Creator authority hardening — **COMPLETE / MERGED**;
- I1 universal socket/proposal foundation — **COMPLETE / MERGED**;
- I2 isolated Creation Sandbox persistence/lifecycle — **COMPLETE / MERGED**;
- I2.5 sandbox runtime/time/AI/readiness ownership — **COMPLETE / MERGED**;
- I3 Character + Location vertical representation proof — **COMPLETE / MERGED**;
- I4 Telegram Creator Studio proposal lifecycle — **COMPLETE / MERGED**;
- I4.1 Creator Studio configuration UX — **NEXT**;
- I5 sandbox-specific notifications/observer flow;
- I6 target-universe compatibility/transmigration planning boundary;
- then return to MIND-F2.

## I4.1 next-slice boundary

Extend the existing Creator Studio without changing the proposal authority model.

Minimum useful configuration UX:
- choose an existing Sandbox Character;
- assign/change sandbox Location from represented Sandbox Locations;
- inspect and refresh derived runtime affordances/options;
- assign/change that Character's sandbox cognition AI model using the shared provider/model catalog;
- expose clock/readiness dependencies clearly;
- show one consolidated readiness checklist;
- allow profile/Body/Skill editing only through the existing sandbox representation vocabulary, not arbitrary keys.

Do not silently auto-run a Character when readiness becomes green. `runtime_ready` remains a separate state from `running`.

Full autonomous sandbox action execution still requires a separate safe execution adapter and explicit authorization.

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

Latest independently recorded production checkpoint in continuity remains Perception Foundation v1 / Deploy #289. PRs through #288 are repository/CI verified as recorded above. Runtime-affecting main merges trigger the canonical deploy workflow, but do not claim a newer production deployment without independent deploy/runtime evidence or explicit live verification.

## Exact resume point

**PR #288 is merged at `2cec0e44b85d9ffaa489344d9202594735dac13b` after CI #1080 SUCCESS, Inventory Foundation #98 SUCCESS and Inventory Operations #54 SUCCESS. Schema v19. Creator Studio now supports owner-only Manual/AI Character and Location drafts, Preview/Reroll/Cancel and explicit Approve into Creation Sandbox. Drafts create no sandbox object before approval and never mutate canonical state. Full sandbox autonomy execution is not implemented. Next authorized slice: I4.1 — Creator Studio Character configuration UX for Location, per-character sandbox AI, derived options and readiness. Do not add another canonical Character.**