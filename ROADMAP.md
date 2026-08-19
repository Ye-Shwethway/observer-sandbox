# Observer Sandbox Roadmap

Status: **ACTIVE**
Roadmap synchronized: **2026-08-19**

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema and verified live production outrank remembered chat context.
- AI proposes structured cognition/creation; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Use minimum-runnable reversible slices; prefer exemplar-first, then batch-by-pattern.
- Character-specific behavioral hard-coding is forbidden.
- Persistent development branches are `main` and `test`; normal work occurs on `test` and is promoted after validation.
- Reconcile roadmap/bootstrap at material checkpoints and never claim production without deploy/runtime evidence.
- Do not seed another real production character merely to test unfinished foundations.
- Explicit Creator-approved canonical state must not be silently overwritten by ordinary seed/import/reinitialize flows.

---

## Current canonical repository checkpoint

Latest merged runtime-affecting work:

### Creator Override Persistence & Progression Re-anchor Correctness v1

- PR #278 — merged.
- Merge: `b50fdc9abb7670ad9e473c24901d154a3816b171`.
- Final head before merge: `455dc95daf19760698abc250b5ef723c85615a57`.
- CI #1067: **SUCCESS**.
- Skill Progression Foundation v1 Acceptance #105: **SUCCESS**.

Closed defects:
- ordinary canonical seed import no longer overwrites Creator-controlled profile values;
- Creator edits establish new progression evidence boundaries so pre-edit evidence cannot replay against the corrected baseline;
- grade-only observer recalibration with unchanged raw value is not emitted as CHARACTER PROGRESSION.

### Body Preserve Shape Completeness v2.1

- PR #279 — merged.
- Merge: `4a176c2d53670e0415957272ed034a1e26d70500`.
- Final head before merge: `c1d1488f58bf3b4b12186fc71d1aca1ee16a986e`.
- CI #1068: **SUCCESS**.
- Strength Live Cycle Validation #124: **SUCCESS**.

Canonical docs:
- `docs/BODY_AESTHETIC_PROPORTION_GRADE_TARGETING_V2.md`
- `docs/BODY_PRESERVE_SHAPE_COMPLETENESS_V2_1.md`

Body Grade Target now uses:

`requested grade -> sex-aware primary ratio search -> registry-driven whole-body projection -> secondary-ratio drift objective -> forward grade verification -> preview -> Apply`

Preserve Shape may coherently adjust represented neck, shoulders, chest, waist, hips, biceps, triceps, forearms, thighs and calves while keeping height as a hard anchor and avoiding unrelated physiology/derived fields.

Body grading remains sex-aware, proportion-based and deterministic. Raw measurements are authoritative; grades remain read-time derived.

### Production evidence

Do not infer production solely from merge/CI.

Latest independently recorded production checkpoint in canonical continuity remains **Perception Foundation v1 / Deploy #289** until a newer deploy/runtime check is independently captured.

The Creator has subsequently observed the Body v2.1 Telegram preview behavior in the live bot, which is useful runtime evidence, but continuity should still keep deploy-number claims separate from direct observation unless the workflow run is independently recorded.

---

## Creator Character Profile Editing & Grade Targeting

Canonical docs:
- `docs/CREATOR_PROFILE_EDITING_GRADE_TARGETING_V1.md`
- `docs/CREATOR_PROFILE_EDITING_GRADE_TARGETING_ACCEPTANCE_V1.md`
- `docs/TELEGRAM_CREATOR_PROFILE_EDIT_UX_V1.md`
- `docs/BODY_AESTHETIC_PROPORTION_GRADE_TARGETING_V2.md`
- `docs/BODY_PRESERVE_SHAPE_COMPLETENESS_V2_1.md`
- `docs/CREATOR_OVERRIDE_PERSISTENCE_PROGRESSION_REANCHOR_V1.md`

Authority rule:

`explicit Creator-approved state > simulation-owned state within declared authority > canonical seed/default baseline`

Creator profile editing remains preview-first, owner-only, auditable and atomic. Entering edit mode pauses the universe and Done Editing restores the prior pause state.

Applied Creator edits are control-plane corrections, not earned character progression or autobiographical events.

---

## Creator Creation Systems — NEW PRIORITY TRACK

The next development direction is now **Creator Creation Foundation before MIND-F2**, but only to the minimum stable socket/staging threshold. Do not build the entire Creator ecosystem before returning to Mind.

Canonical new docs:
- `docs/UNIVERSAL_CREATION_SOCKET_FOUNDATION_V1.md`
- `docs/CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md`
- `docs/CREATOR_CREATION_FULL_ROADMAP_V1.md`
- `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`

### Core product goal

Creator must eventually be able to create from Telegram:
- characters;
- locations;
- items/resources/equipment;
- skills;
- jobs/roles;
- quests;
- organizations/factions;
- services/facilities;
- events/actions/world elements;
- system/rule descriptors;
- future registered creation types.

Creation may be manual or AI-assisted, but both paths converge on the same structured proposal/validation/apply contract.

AI has proposal authority only. It never receives direct canonical DB-write authority.

---

## Creation Sandbox / Staging Universe

All Creator-created content begins outside the canonical universe.

Canonical flow:

`Creator intent -> Draft -> Creation Sandbox -> compatibility validation -> Transmigration Preview -> explicit Creator approval -> Canonical Universe`

Principle:

> **Create anywhere safely; canon nowhere automatically.**

Sandbox architecture is **shared engine, isolated state**:
- approved schemas/rules/validators are reused;
- sandbox state is isolated;
- canonical runtime/events/relationships/autonomy are not mutated;
- sandbox objects can be reset, cloned, rerolled, archived or deleted safely;
- sandbox Telegram observability is Creator-only and visually separate from canonical Observer output.

---

## Universal Creation Socket Foundation

Do not implement bespoke CRUD pipelines per type.

One shared creation envelope/registry handles:
- type/schema identity;
- lifecycle;
- provenance;
- sandbox scope;
- validation;
- dependency/reference graph;
- batch creation;
- transmigration planning.

Type-specific sockets provide their own fields/validators/hooks.

Minimum first proof:
1. Character
2. Location

This is intentionally enough to validate the ontology and isolation architecture without broad subsystem sprawl.

---

## Transmigration and target-universe compatibility

Transmigration is not blind merge/copy.

Canonical pipeline:

`freeze sandbox revision -> validate schema/dependencies -> select target universe -> compatibility checks -> conflict checks -> deterministic canonical mutation plan -> Creator preview -> explicit approval -> atomic activation`

Failure produces **zero canonical writes**.

A structurally valid sandbox creation may still be incompatible with the target universe.

Current production universe remains realism-constrained. A sandbox supernatural power/system may be valid as sandbox content but must be rejected from this universe unless target-universe policy explicitly supports it.

Future separate universes may adopt different physics, technology, supernatural or capability policies without changing the generic creation socket architecture.

Key rule:

> **schema-valid does not imply universe-compatible.**

---

## Creator Creation full roadmap

Canonical detailed roadmap: `docs/CREATOR_CREATION_FULL_ROADMAP_V1.md`.

Tracks:

- **C0** Creator Authority & Canonical Protection
- **C1** Universal Creation Socket Foundation
- **C2** Creation Sandbox / Staging Universe
- **C3** Character + Location Vertical Proof
- **C4** Telegram Creator Studio v1
- **C5** Transmigration Foundation
- **C6** Universe Compatibility Profiles
- **C7** Creation Type Expansion
- **C8** Rich Batch Worldbuilding
- **C9** Multiple Universe Creation

Long-term roadmap is documented now; implementation remains minimum-first.

---

## Immediate implementation plan

Canonical: `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`.

Implement only:

1. **I0 — Creator authority hardening**
   - generalize no-snap-back invariant beyond profile-specific code.

2. **I1 — Universal proposal/socket core**
   - registry, proposal envelope, validation, sandbox/batch identity;
   - initial Character + Location sockets only.

3. **I2 — Isolated Creation Sandbox**
   - sandbox namespace/state, delete/reset, canonical leakage guards.

4. **I3 — Character + Location sandbox vertical proof**
   - no canonical Darian/relationship/autonomy connection.

5. **I4 — Telegram Creator Studio minimum**
   - manual + AI draft modes;
   - preview/edit/reroll/validate/approve into sandbox.

6. **I5 — Sandbox Telegram notifications**
   - explicitly separate from canonical Observer notifications.

7. **I6 — Transmigration planning/compatibility boundary**
   - plan/validate only is sufficient before Mind resumes;
   - production character activation remains gate-blocked.

---

## Relationship to Mind Engine

Mind Engine remains canonical and required.

Canonical doc: `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`.

MIND-F2 is **deferred temporarily**, not replaced.

Return to MIND-F2 once the minimum Creator Creation threshold is proven:
- Creator authority no-snap-back invariant regression-tested;
- universal proposal/socket foundation stable;
- isolated Creation Sandbox proven;
- Character + Location sandbox proof complete;
- minimum Telegram Creator Studio works;
- compatibility/transmigration planning boundary exists;
- second-character canonical promotion remains blocked.

Then continue:

`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2`

Later Creator creation sockets expand incrementally alongside/after Mind work.

---

## Second-character canonical gate

The prior gate remains intact.

**Creating a character in Creation Sandbox does not count as adding another real production character.**

Character transmigration into the current canonical production universe remains blocked until:
1. W0-W5 minimum external inputs remain healthy;
2. Perception handoff remains healthy;
3. Creator profile/body controls are production-stable;
4. MIND-F2..F7 minimum foundations are complete;
5. Relationship Adaptation foundation is complete;
6. A3.3 interim planning scaffolding is reconciled;
7. Foundation Completion Review v2 passes;
8. Creator explicitly approves transmigration.

The next canonical character remains live multi-character architecture acceptance, not a test dummy.

---

## Completed minimum external-input stack

- W0 World Stimulus / Exposure — complete/deployed
- W1 / W1.1 Weather — complete/deployed
- W2 Commitments / Obligations — complete/deployed
- W3 / W3.1 Economy / Valuation — complete/deployed
- W4 / W4.1 Information / Media — complete/deployed
- W5 Communication Exposure — complete/deployed
- Perception Foundation v1 — complete/deployed

A3.3 Bounded Multi-Step Destination Intent remains deployed; continue read-only natural observation and migrate duplicate interim route-purpose scaffolding when F4/F5 activate.

---

## Exact resume point

**Current repository has PR #278 and PR #279 merged, closing Creator profile seed snap-back/evidence-replay issues and completing whole-body Preserve Shape targeting. The next authorized development direction is docs-first Creator Creation Foundation. Full C0-C9 roadmap is recorded, but implementation must follow the minimum I0-I6 plan: universal socket/proposal foundation + isolated Creation Sandbox + Character/Location proof + minimum Telegram Creator Studio + compatibility/transmigration planning. Do not add another canonical character. Return to MIND-F2 after that minimum staging threshold is stable.**
