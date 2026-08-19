# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-08-20**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical docs/source
5. verified production/runtime evidence before live claims.

Authority order:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

Persistent branches: `main`, `test` only.

Workflow:
`develop on test -> focused tests -> PR/final CI -> merge to main -> runtime deploy if applicable -> production verification -> continuity sync -> main/test synchronization`.

Do not claim production deployment from a merge alone.

---

## Current repository checkpoint

Latest merged implementation checkpoint before this continuity update:

### PR #309 — World-qualified runtime/time controls

Merged main checkpoint:
`f74ef6395c9bd2f27b705c8c41f2a8cfadfc13c8`

Evidence:
- CI #1120 — **SUCCESS**;
- Inventory Operations v1 Acceptance #56 — **SUCCESS**;
- no schema migration;
- `main == test` at the merge checkpoint before this docs-only continuity update.

Canonical command surface is now explicitly world-qualified:

Real World:
- `/realstatus`
- `/realpause`
- `/realresume`
- `/realspeed <value>`
- `/realtime <ISO-8601>`

Sandbox World:
- `/sandboxstatus`
- `/sandboxpause`
- `/sandboxresume`
- `/sandboxspeed <value>`
- `/sandboxtime <ISO-8601>`

Legacy ambiguous `/pause`, `/resume`, `/speed`, `/time` are non-mutating redirects that require the Creator/user to choose a world explicitly.

Real World and Sandbox runtime state remain isolated. Real World uses canonical runtime/autonomy state. Sandbox uses `creation_sandbox_runtime` and `sw:rt:*` controls.

Manual time-edit semantics:
- manual time edits auto-pause the selected world;
- the selected world remains paused afterward until explicitly resumed;
- `/realtime` cancels stale Real World pending autonomous actions tied to the old timeline, resets them for reevaluation, writes the new canonical time and records Creator audit evidence;
- `/sandboxtime` changes only the isolated Sandbox clock;
- changing one world must not mutate the other world.

Real World runtime UI now mirrors Sandbox runtime UX where practical: Pause/Resume plus 1x/60x/3600x controls with separate callback namespaces (`rw:rt:*` vs `sw:rt:*`).

---

## Creator Character generation checkpoint

### PR #304 — exact Character seed/profile schema fill

Merged:
`81698bf5b06b20f5153300b59048a923ff4b9395`

Creator Character AI generation moved from heuristic incremental filling to:
`existing creation-owned Character field registry -> exact required profile template -> AI fills values -> deterministic validation -> save-ready draft`.

Profile values are an **exact schema-fill contract**. Missing or extra creation-owned profile keys are rejected. Runtime/derived-only fields remain excluded from Creator seed ownership.

### PR #305 — sparse relevant-only skills

Merged:
`683eab88e658203273bc1958667110299a1fac63`

PR #304 initially overconstrained skills by requiring every canonical skill key. That was corrected.

Current rule:
- profile fields remain exact-required;
- skills are a sparse repeating collection;
- only relevant skills need to exist;
- skill keys must come from canonical vocabulary;
- unknown/duplicate/invalid skill rows are rejected;
- unrelated skills are not inserted as zero placeholders.

### PR #306 — registry data types are authoritative

Merged:
`96c38ef9469057e0a259ad507a044bdbfd851e28`

RAPS-prefixed compatibility fields are not automatically numeric. Validation follows `profile_field_definitions.data_type`. Numeric/integer RAPS values retain range validation; text/json fields keep their declared types.

### PR #307 — current-age parsing fix

Merged:
`e9adb35c20e1f28309316690916071a2717496df`

Current-age parsing accepts explicit current-age phrases such as:
- `24 years old`
- `24-year-old`
- `age: 24`
- `aged 24`

Biography/history phrases such as `at age 20 he joined...` must not be interpreted as the Character's current requested age.

### Character skill vocabulary

PR #303 established the reusable canonical vocabulary:
`hand_to_hand_combat, weapons, firearms, bladed_weapons, survival, navigation, climbing, emergency_response, field_medicine, tactical_planning, technology`.

Aliases/categories normalize into that vocabulary. The Creator generation path no longer relies on background keyword heuristics to force exact skill coverage.

---

## Adrian Vale — current Sandbox fixture

Creator generated Adrian Vale successfully after the #304–#307 fixes, using MiniMax-M3 for the successful fast structured draft, and explicitly approved him into the isolated Creation Sandbox.

Important authority boundary:
- Adrian is **Sandbox-approved / Sandbox-active content**;
- Adrian is **not a canonical Real World Character**;
- this does **not** open or bypass the second-character transmigration gate.

The approved Adrian profile is useful as the current live Sandbox Character fixture for profile/config/runtime UX development.

Creator live verification on 2026-08-20 confirmed the Sandbox Profile browser works correctly after PR #308.

---

## PR #308 — Sandbox Character Profile Browser Parity

Merged:
`35f3bdaad73ef6d1cbaa49c0509107b3b27d933f`

Evidence:
- CI #1118 — **SUCCESS**;
- no schema migration;
- Creator live Telegram verification — **PASS**.

Sandbox Character cards now expose `📖 Profile` before configuration/readiness controls.

Reuse-first architecture is locked:
- same `profile_field_definitions` semantic registry;
- same `profile_sections.v1.json` section configuration;
- same Real World Telegram profile formatters/presentation where data semantics match;
- Sandbox-specific data reader/storage adapter;
- Sandbox callback/navigation namespace remains isolated;
- do not fabricate Real World runtime/recovery data that Sandbox does not yet represent.

Goal: Real World and Sandbox Character profile UX should remain as similar as possible while preserving storage/runtime isolation.

---

## Existing Creator Profile Edit flow to reuse

Do **not** invent a new profile-edit workflow for Sandbox.

Real World already has the desired Creator flow:
`Profile -> Edit Profile -> auto-pause universe if needed -> choose section/field -> enter new value -> Preview -> Apply -> continue editing -> Done Editing -> restore pre-edit pause state`.

Existing reusable semantics include:
- registry-backed type coercion/validation;
- derived-field protection;
- old -> new proposal preview;
- explicit Apply boundary;
- Creator override/canonical-correction mutation classes;
- Creator progression re-anchor so old training/action evidence does not immediately snap an edited value back;
- universe pause state remembered and restored on Done Editing.

Sandbox implementation should reuse the same **interaction contract and presentation** with a Sandbox storage/runtime adapter. Draft editing, Sandbox-active Character editing and Real World live-profile editing are different mutation targets, but should share UX and validation components where possible.

For an already-approved Sandbox Character such as Adrian:
`Sandbox Character -> Edit Profile -> Sandbox runtime auto-pause if needed -> edit/preview/apply -> Done Editing -> restore prior Sandbox pause state`.

Do not call Real World `set_autonomy_paused()` from Sandbox editing.

---

## Immediate next authorized slice

**NEXT: Sandbox Profile Edit Parity / Existing Creator Profile Edit reuse.**

Minimum scope:
1. add Edit Profile access from Sandbox Character Profile/Character surfaces;
2. reuse the existing section -> field -> value -> preview -> apply UX and formatters;
3. use the shared field registry and existing validation semantics;
4. apply only to isolated Sandbox profile/facet/skill storage;
5. auto-pause only the Sandbox runtime while editing an active Sandbox Character;
6. restore the pre-edit Sandbox pause state on Done Editing;
7. never mutate canonical Real World profile/runtime tables;
8. preserve revision/audit evidence for Sandbox edits;
9. prove Real World state fingerprint remains unchanged.

Keep this slice narrow. Do not combine it with I6 transmigration apply or full sandbox autonomous ticking.

---

## Creator Creation route status

Completed:
- I0 Creator authority
- I1 universal proposal/socket core
- I2 isolated Creation Sandbox persistence/lifecycle
- I2.5 isolated Sandbox runtime/time/AI/readiness
- I3 Character + Location representation proof
- I4 Creator Studio proposal lifecycle
- guided dual-pattern Creator Studio UX
- I4.1 Sandbox Character configuration UX
- I5 Sandbox Observer foundation
- I5.1 proactive Sandbox Observer delivery
- exact Character seed/profile schema-fill hardening (#302–#307)
- Sandbox Character Profile browser parity (#308)
- explicit Real/Sandbox runtime/time command split (#309)

Current local route:
`Sandbox Profile Edit parity -> Creator review -> then decide whether to resume I6 transmigration planning or another bounded Sandbox runtime/UX prerequisite`.

I6 is therefore **not the immediate next slice anymore**. When resumed, I6 remains planning/validation only unless the Creator explicitly changes that boundary.

---

## Creator Staging & Transmigration locks

> **Create anywhere safely; canon nowhere automatically.**

> **schema-valid does not imply universe-compatible.**

Lifecycle/authority concept:
`Draft -> Sandbox Approved -> Sandbox Active -> Tested/Revised -> Ready for Transmigration -> Canonical Approved -> Canonical Active`.

Sandbox and canonical storage/runtime remain isolated. Nothing transmigrates automatically.

Future transmigration must validate target-universe compatibility and dependencies, be atomic, and produce zero canonical writes on failure.

Supernatural/impossible concepts may be valid in a Sandbox or future universe but incompatible with the current realistic Real World.

The second canonical Character gate remains closed. Adrian's Sandbox existence does not violate that gate.

---

## Second-character gate

Do not activate/transmigrate a second real production Character until all required gates remain satisfied, including:
1. W0-W5/perception foundations healthy;
2. Creator profile/body controls stable;
3. minimum Creator Creation staging threshold complete;
4. MIND-F2..F7 minimum foundations complete;
5. Relationship Adaptation foundation complete;
6. A3.3 interim planning scaffolding reconciled;
7. Foundation Completion Review v2 passes;
8. Creator explicitly approves canonical transmigration.

---

## Existing runtime locks

W0-W5 plus Perception Foundation v1 remain the completed external-input foundation.

PR #278 protects Creator-edited progression/profile values from canonical seed/evidence snap-back.

PR #279 provides Body Preserve Shape completeness.

A3.3 remains read-only/natural-observation territory. Do not force Darian outside merely to produce evidence.

Full Sandbox autonomous ticking is still **not implemented**. `runtime_ready != running` remains a hard distinction.

---

## Production evidence boundary

Repository/CI evidence is current through PR #309. Creator also directly verified the Sandbox Profile browser after #308 in Telegram.

Do not infer that PR #309 is live in production solely from merge/CI. A new chat should verify current boot/deploy/runtime evidence before making live-runtime claims or running production-sensitive acceptance.

---

## Exact resume point

**Repository checkpoint before continuity-doc commit: PR #309 merged at `f74ef6395c9bd2f27b705c8c41f2a8cfadfc13c8`; CI #1120 SUCCESS; Inventory Operations Acceptance #56 SUCCESS. Real World and Sandbox runtime/time controls are now explicitly world-qualified. Legacy `/pause|resume|speed|time` no longer mutate a default world. Manual time edits auto-pause only the selected world, and Real World time rewrites invalidate stale pending autonomous actions. PR #308 merged at `35f3bdaad73ef6d1cbaa49c0509107b3b27d933f`; Creator live-tested Sandbox Character Profile browsing successfully. Adrian Vale has been explicitly approved into the isolated Creation Sandbox and is not canonical. Next authorized implementation slice: reuse the existing Real World Creator Profile Edit flow for Sandbox Profile Edit parity, with Sandbox-only pause/storage adapters and Real World zero-mutation proof. Do not invent a new editor. Do not transmigrate Adrian or add a second canonical Character.**
