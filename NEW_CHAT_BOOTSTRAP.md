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

Do not claim production deployment without deploy/runtime evidence.

---

## Current repository checkpoint

### PR #278 — Creator Override Persistence & Progression Re-anchor Correctness v1

Merged at:
`b50fdc9abb7670ad9e473c24901d154a3816b171`

Final pre-merge head:
`455dc95daf19760698abc250b5ef723c85615a57`

Evidence:
- CI #1067 — SUCCESS
- Skill Progression Foundation v1 Acceptance #105 — SUCCESS

Closed issues:
- canonical seed/import no longer silently overwrites Creator-controlled profile values;
- Creator edits establish progression re-anchor boundaries so pre-edit stimulus/evidence cannot replay against corrected values;
- unchanged raw values with only grade/evaluator reclassification do not emit false CHARACTER PROGRESSION.

Canonical contract:
`docs/CREATOR_OVERRIDE_PERSISTENCE_PROGRESSION_REANCHOR_V1.md`.

### PR #279 — Body Preserve Shape Completeness v2.1

Merged at:
`4a176c2d53670e0415957272ed034a1e26d70500`

Final pre-merge head:
`c1d1488f58bf3b4b12186fc71d1aca1ee16a986e`

Evidence:
- CI #1068 — SUCCESS
- Strength Live Cycle Validation #124 — SUCCESS

Body Grade Target Preserve Shape now performs:

`primary grade-ratio search -> registry-driven whole-body projection -> secondary-ratio drift scoring -> forward verification -> preview -> Apply`.

Represented muscular circumferences such as neck, arms, forearms, thighs and calves can follow torso changes coherently instead of being left at an unrelated scale.

Height remains a hard anchor. Physiology/derived values are not blindly scaled.

Canonical docs:
- `docs/BODY_AESTHETIC_PROPORTION_GRADE_TARGETING_V2.md`
- `docs/BODY_PRESERVE_SHAPE_COMPLETENESS_V2_1.md`

Creator has observed the new whole-body preview behavior through Telegram. Keep that distinct from exact GitHub deploy-run evidence unless a deploy run is independently recorded.

Latest independently recorded deploy checkpoint in continuity remains Perception Foundation v1 / Deploy #289.

---

## Creator authority invariant

The profile seed snap-back defect is now treated as a general architectural lesson.

Canonical precedence:

`explicit Creator-approved canonical state > live simulation-owned state within declared authority > canonical seed/default/import baseline`.

A seed initializes missing/unclaimed state. It is not allowed to silently restore an older value over explicit Creator authority.

The next Creator Creation work must generalize this protection beyond profile values.

---

## NEW PRIORITY — Creator Creation Foundation

Before resuming deeper Mind work, build only the minimum stable Creator Creation substrate.

Canonical docs:
- `docs/UNIVERSAL_CREATION_SOCKET_FOUNDATION_V1.md`
- `docs/CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md`
- `docs/CREATOR_CREATION_FULL_ROADMAP_V1.md`
- `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`

Long-term product goal:
Creator can create characters, locations, items, skills, jobs, quests, organizations, services, world elements, event/action templates and future systems from Telegram, either manually or through AI-generated structured proposals.

AI never receives direct canonical DB-write authority.

---

## Creation Sandbox / Staging Universe

Every new Creator creation begins outside the canonical universe.

Canonical flow:

`Creator intent -> Draft -> Creation Sandbox -> target-universe validation -> Transmigration Preview -> explicit Creator approval -> Canonical Universe`

Core principle:

> **Create anywhere safely; canon nowhere automatically.**

Sandbox implementation uses **shared engine, isolated state**.

Shared:
- schemas;
- validators;
- deterministic grading/runtime helpers;
- approved project rules where applicable.

Isolated:
- entities/objects;
- state;
- runtime events;
- autonomy membership;
- relationships;
- world graph mutations;
- notifications.

Sandbox objects may be reset, rerolled, cloned, archived or deleted without touching canonical state.

---

## Universal creation socket model

Do not build a bespoke CRUD backend for every type.

One generic creation envelope/registry handles:
- type + schema version;
- lifecycle;
- provenance;
- sandbox/batch identity;
- references/dependencies;
- validation;
- transmigration planning.

Type sockets add domain-specific fields/validators/hooks.

Minimum first proof:
- Character
- Location

Manual and AI creation must converge on the same structured proposal pipeline.

---

## Transmigration compatibility

Sandbox creation is not automatically eligible for canon.

Transmigration requires:

`freeze sandbox revision -> schema/dependency validation -> target universe selection -> universe compatibility -> canonical conflict check -> deterministic mutation plan -> Creator preview -> explicit approval -> atomic activation`.

Failure must produce zero canonical writes.

Important distinction:

> **schema-valid does not imply universe-compatible.**

The current production universe remains realism-constrained. Supernatural/magic/impossible-physics systems may exist in sandbox experiments but must be rejected for this target universe unless its policy explicitly allows them.

Future separate universes may allow different physics, technology, supernatural or capability systems through their own universe compatibility profiles.

---

## Full Creator Creation roadmap

Detailed canonical roadmap:
`docs/CREATOR_CREATION_FULL_ROADMAP_V1.md`.

Tracks:
- C0 Creator Authority & Canonical Protection
- C1 Universal Creation Socket Foundation
- C2 Creation Sandbox / Staging Universe
- C3 Character + Location Vertical Proof
- C4 Telegram Creator Studio v1
- C5 Transmigration Foundation
- C6 Universe Compatibility Profiles
- C7 Creation Type Expansion
- C8 Rich Batch Worldbuilding
- C9 Multiple Universe Creation

This is the long-term roadmap only. Do not implement all tracks before returning to Mind.

---

## Immediate minimum implementation

Canonical:
`docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`.

Implement next:

1. I0 — general Creator authority/no-snap-back hardening;
2. I1 — universal proposal/socket core;
3. I2 — isolated Creation Sandbox;
4. I3 — Character + Location sandbox proof;
5. I4 — minimum Telegram Creator Studio with Manual + AI Draft;
6. I5 — separate sandbox Telegram notifications;
7. I6 — target-universe compatibility/transmigration planning boundary.

Do not build all creation types yet.

---

## Second-character gate remains closed

The project rule remains:

> Do not add another real production character until Mind/Relationship foundations and Foundation Completion Review are complete.

A sandbox Character **does not count as a real production character** because it has no canonical universe membership.

Character transmigration to the current canonical production universe remains blocked until:
1. W0-W5/perception foundations remain healthy;
2. Creator profile/body controls are stable;
3. MIND-F2..F7 minimum foundations are complete;
4. Relationship Adaptation foundation is complete;
5. A3.3 interim planning scaffolding is reconciled;
6. Foundation Completion Review v2 passes;
7. Creator explicitly approves transmigration.

The next real character remains live multi-character acceptance, never a test dummy.

---

## Mind Engine continuation

Canonical:
`docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`.

MIND-F2 is temporarily deferred while the minimum Creator Creation staging foundation is built.

Resume MIND-F2 as soon as all are true:
- Creator authority no-snap-back invariant is regression-tested;
- Character/Location creation sockets exist;
- Creation Sandbox isolation is proven;
- minimum Telegram Creator Studio can create/manage those sandbox objects;
- manual and AI modes share one proposal/apply path;
- compatibility/transmigration planning boundary exists;
- second-character canonical activation remains gated.

Then continue:

`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2`.

---

## Existing completed external-input foundation

Minimum stack remains:
- W0 World Stimulus / Exposure
- W1 / W1.1 Weather
- W2 Commitments / Obligations
- W3 / W3.1 Economy / Valuation
- W4 / W4.1 Information / Media
- W5 Communication Exposure
- Perception Foundation v1

A3.3 Bounded Multi-Step Destination Intent remains deployed. Continue read-only natural observation; do not force Darian outside. When F4/F5 activate, reconcile duplicate interim route-purpose scaffolding into canonical Mind intention/planning.

---

## Exact resume point

**PR #278 and PR #279 are merged and CI-green. Creator profile edits are protected against ordinary seed snap-back/evidence replay, and Body Preserve Shape now propagates across represented muscular measurements. The next authorized work is the minimum Creator Creation staging implementation: I0 authority hardening -> I1 socket/proposal core -> I2 isolated Creation Sandbox -> I3 Character/Location proof -> I4 Telegram Creator Studio -> I5 sandbox notifications -> I6 compatibility/transmigration planning. Do not add another canonical character. Resume MIND-F2 once this minimum staging threshold is stable.**
