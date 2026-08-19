# Observer Sandbox Roadmap

Status: ACTIVE  
Roadmap synchronized: **2026-08-20**

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, verified live runtime/DB and current CI/deploy evidence outrank remembered chat context.
- AI proposes; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Creator-approved live state outranks ordinary seed/default refresh.
- Creator-created objects stage in Creation Sandbox first; Sandbox approval and canonical transmigration are separate authority transitions.
- **Created is not alive.** Creation, runtime readiness and runtime execution are separate boundaries.
- Real World and Creation Sandbox mutable state must remain isolated.
- Reuse established Real World systems/UX for Sandbox equivalents whenever semantics match; prefer world-specific adapters over duplicate systems.

---

## Current repository checkpoint

Latest implementation checkpoint before this docs update:

### PR #309 — Split runtime controls by world

Merged:
`f74ef6395c9bd2f27b705c8c41f2a8cfadfc13c8`

Evidence:
- CI #1120 — **SUCCESS**;
- Inventory Operations v1 Acceptance #56 — **SUCCESS**;
- no schema migration.

Runtime/time controls are now explicit per world.

Real World:
`/realstatus`, `/realpause`, `/realresume`, `/realspeed <value>`, `/realtime <ISO-8601>`.

Sandbox World:
`/sandboxstatus`, `/sandboxpause`, `/sandboxresume`, `/sandboxspeed <value>`, `/sandboxtime <ISO-8601>`.

Legacy ambiguous `/pause`, `/resume`, `/speed`, `/time` no longer mutate a default world; they redirect the user to choose a world-specific command.

Manual time edits auto-pause the selected world and leave it paused until explicit resume. Real World clock rewrites invalidate stale pending autonomous actions from the old timeline and record Creator audit evidence. Sandbox time edits touch only isolated Sandbox runtime state.

Real/Sandbox inline runtime UX mirrors Pause/Resume and 1x/60x/3600x controls through separate callback namespaces.

### PR #308 — Sandbox Character Profile Browser Parity

Merged:
`35f3bdaad73ef6d1cbaa49c0509107b3b27d933f`

Evidence:
- CI #1118 — **SUCCESS**;
- Creator live Telegram verification — **PASS**;
- no schema migration.

Sandbox Character detail now exposes `📖 Profile` and reuses the established Real World profile presentation wherever semantics match:
- shared `profile_field_definitions` semantic registry;
- shared `profile_sections.v1.json` section definition;
- shared profile formatters/grade presentation;
- Sandbox-only storage reader and callback namespace;
- no fabricated Real World runtime/recovery state.

Adrian Vale is the current approved Sandbox Character fixture. He is Sandbox content only and is not canonical.

---

## Creator Character generation hardening

The current Creator Character generation contract is the result of PRs #302–#307.

### Exact profile schema fill

PR #304 merge:
`81698bf5b06b20f5153300b59048a923ff4b9395`

Flow:
`creation-owned Character field registry -> exact required profile template -> AI fills values -> deterministic validation -> draft`.

All creation-owned profile keys are required exactly once. Missing/extra profile keys are rejected. Runtime/derived-only state is not Creator seed ownership.

### Sparse skills

PR #305 merge:
`683eab88e658203273bc1958667110299a1fac63`

Skills are **not** an exact fixed-count form. They are a sparse repeating collection of relevant canonical skill rows. Unknown/duplicate/invalid skills are rejected; unrelated zero placeholders are not required.

Canonical skill vocabulary established by PR #303:
`hand_to_hand_combat, weapons, firearms, bladed_weapons, survival, navigation, climbing, emergency_response, field_medicine, tactical_planning, technology`.

### Registered data types

PR #306 merge:
`96c38ef9469057e0a259ad507a044bdbfd851e28`

`profile_field_definitions.data_type` is authoritative. RAPS-prefix alone does not imply numeric data.

### Current-age parsing

PR #307 merge:
`e9adb35c20e1f28309316690916071a2717496df`

Explicit current-age phrasing is parsed; biography milestone phrases such as `at age 20` are not treated as the Character's current age.

---

## Creator Creation implementation route

Completed / merged:
- I0 Creator authority hardening;
- I1 universal socket/proposal foundation;
- I2 isolated Creation Sandbox persistence/lifecycle;
- I2.5 Sandbox runtime/time/AI/readiness ownership;
- I3 Character + Location vertical representation proof;
- I4 Telegram Creator Studio proposal lifecycle;
- guided dual-pattern Creator Studio UX;
- I4.1 Sandbox Character configuration UX;
- I5 Sandbox Observer foundation;
- I5.1 proactive Sandbox Observer delivery;
- Character exact schema generation + validation hardening (#302–#307);
- Sandbox Character Profile Browser parity (#308);
- Real/Sandbox runtime/time command and control separation (#309).

### Immediate next authorized slice

**Sandbox Profile Edit Parity — reuse the existing Real World Creator Profile Edit flow.**

Do not invent a separate editor.

Target flow:
`Sandbox Character -> Profile -> Edit Profile -> auto-pause Sandbox runtime if needed -> section -> field -> value -> Preview -> Apply -> continue or Done Editing -> restore pre-edit Sandbox pause state`.

Minimum requirements:
- reuse existing Real World profile-edit interaction/presentation where applicable;
- reuse shared registry type coercion/validation and derived-field protection;
- apply to Sandbox profile/facet/skill storage only;
- preserve Sandbox revision/audit evidence;
- restore the prior Sandbox pause state on Done Editing;
- prove canonical Real World state remains unchanged;
- do not call Real World pause controls from Sandbox edit mode.

After this slice, stop for Creator review and decide whether to return to I6 or another bounded Sandbox prerequisite.

---

## Existing Real World profile-edit contract

Real World already provides the pattern to reuse:
`Profile -> Edit Profile -> auto-pause -> edit field -> Preview -> Apply -> Done Editing -> restore previous pause state`.

Existing semantics include:
- registry-backed type validation/coercion;
- explicit preview/apply mutation boundary;
- Creator override/canonical correction semantics;
- progression re-anchor after Creator edits;
- pause-state restoration.

The Sandbox implementation should be an adapter to this contract, not a new UX/system.

---

## Creator Staging & Transmigration

> **Create anywhere safely; canon nowhere automatically.**

> **schema-valid does not imply universe-compatible.**

Lifecycle/authority direction:
`Draft -> Sandbox Approved -> Sandbox Active -> Tested/Revised -> Ready for Transmigration -> Canonical Approved -> Canonical Active`.

All Creator-created content begins in isolated staging. Canonical activation requires explicit Creator approval plus target-universe compatibility validation at a future atomic boundary.

Supernatural/impossible-physics concepts may be Sandbox-valid while incompatible with the current realistic universe and valid in a future universe profile.

Adrian Vale is currently Sandbox-approved only. Do not transmigrate him.

---

## I6 boundary when resumed

I6 is no longer the immediate next slice. When the Creator resumes it, its previously approved boundary remains **planning/validation only** unless explicitly changed.

Minimum:
- select/freeze one Sandbox object revision or snapshot;
- choose target-universe compatibility profile;
- compute dependency closure;
- run deterministic compatibility validation;
- return structured compatible/incompatible/dependency/error outcomes;
- build proposed canonical mutations without applying them;
- prove incompatible planning produces zero canonical writes.

Do not add a general multi-universe runtime or a Character canonical apply path merely as part of I6 planning.

---

## Time/control ownership

Real World canonical runtime and Creation Sandbox runtime are independent control domains.

Real World runtime commands/UI may only mutate Real World state. Sandbox runtime commands/UI may only mutate Sandbox state.

Manual time changes are privileged Creator controls and auto-pause their own world before mutation.

This separation is also the basis for automatic pause behavior during future Sandbox profile editing.

---

## Sandbox runtime status

Sandbox has isolated clock/speed/pause, Character configuration/readiness, AI binding, profile representation and observer surfaces.

`runtime_ready != running` remains locked.

Full Sandbox autonomous ticking is **not implemented** yet. Do not invent autonomous Sandbox activity merely because a Character is configured or runtime-ready.

---

## Second-character gate

No second real production Character may be activated/transmigrated before:
1. W0-W5/perception foundations remain healthy;
2. Creator profile/body controls remain stable;
3. minimum Creator Creation staging threshold is complete;
4. MIND-F2..F7 minimum foundations are complete;
5. Relationship Adaptation foundation is complete;
6. A3.3 interim planning scaffolding is reconciled;
7. Foundation Completion Review v2 passes;
8. Creator explicitly approves canonical transmigration.

Sandbox Characters do not violate this gate.

---

## Mind continuation

MIND-F2 remains deferred while the current bounded Creator Creation/Sandbox UX prerequisites are being completed.

Later route remains:
`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real Character transmigration proposal`.

---

## Existing Real World runtime locks

W0-W5 plus Perception Foundation v1 remain the completed external-input foundation.

PR #278 protects Creator progression/profile overrides from seed/evidence snap-back.

PR #279 provides Body Preserve Shape completeness.

A3.3 remains read-only/natural-observation territory. Do not force Darian outside merely to generate evidence.

---

## Production evidence boundary

Repository/CI is verified through PR #309. Creator live Telegram verification establishes that the Sandbox Profile browser from PR #308 works in the observed runtime.

Do not claim PR #309 is live merely because it merged and CI passed. Verify current boot/deploy/runtime evidence in the next chat before production-sensitive actions.

---

## Exact resume point

**Latest implementation merge before this docs-only roadmap update: PR #309 at `f74ef6395c9bd2f27b705c8c41f2a8cfadfc13c8`, CI #1120 SUCCESS, Inventory Operations Acceptance #56 SUCCESS. Real World and Sandbox runtime/time controls are explicitly world-qualified and isolated. PR #308 at `35f3bdaad73ef6d1cbaa49c0509107b3b27d933f` added Sandbox Character Profile Browser parity and was live-tested successfully by the Creator. Adrian Vale is approved in the isolated Creation Sandbox only. Next authorized slice: reuse the existing Real World Creator Profile Edit flow for Sandbox Profile Edit parity, with Sandbox-only pause/storage adapters and canonical zero-mutation proof. Do not invent a new editor. Do not transmigrate Adrian or activate another canonical Character.**
