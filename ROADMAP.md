# Observer Sandbox Roadmap

Status: **ACTIVE**  
Roadmap synchronized: **2026-08-21**

## Operating principles

- Current Creator instruction, live repo/schema, verified runtime/DB and current CI/deploy evidence outrank remembered chat context.
- AI proposes structured facts; deterministic contracts validate, derive and mutate.
- Telegram is observer/control, never simulation authority.
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- Universal systems use expandable registry/socket patterns rather than family-specific switchboards.
- `canonical_state_fingerprint()` remains a high-value zero-canonical-mutation invariant.
- Development velocity matters: do not turn optional realism polish into a creation-blocking treadmill without explicit Creator approval.

### Mandatory Creation implementation gate

`docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md` is the canonical implementation playbook for every current/future Creator Creation section.

Before planning, coding, reviewing, extending or debugging Character/Item/Location/Skill/Quest/System/Organization/Service/Event/world-element or future Creation sockets:

1. reread the Creation Implementation Standard;
2. identify the canonical versioned domain schema;
3. if no schema exists, build/approve the schema first before AI/UI/materialization work;
4. map existing reusable contracts/sockets;
5. follow the shared Creation vertical rather than creating a bespoke CRUD path.

Core vertical:

`versioned schema -> socket/reuse map -> full Manual form + full AI structured fill -> safe canonicalization -> strict structural/domain validation -> graph/dependency validation -> write-free review + .txt export -> explicit approval -> atomic Sandbox materialization -> approved detail -> Edit Preview/Apply/Done + pause restoration -> cleanup`.

Fine-grained realism is advisory/non-blocking by default unless a domain contract and explicit Creator authorization make it authoritative.

---

## Current strategic direction — finish Location Creation, then Genesis reset

The current Real World Characters, Locations, Items and Estate fixtures are now explicitly classified as **prototype-era exemplars**, not preservation constraints.

They were created before the present Creation Sandbox, universal schemas and transmigration architecture were mature. The approved strategy is not to build a complex legacy-preservation/reincarnation bridge around them.

Instead:

> **Preserve reusable universe infrastructure; retire prototype content; rebuild canonical content from modern Sandbox creations through explicit transmigration.**

Canonical plan:

`docs/CREATOR_REAL_WORLD_RESET_AND_GENESIS_PLAN_V1.md`

Architecture decision:

`docs/LOCATION_FIRST_GENESIS_DECISION_RECORD_V1.md`

However, the Real World content reset must **not** happen yet.

A viable rebuilt world requires represented Locations before Characters can become runnable. Therefore the immediate authorized feature remains:

> **I5.11 — Sandbox Location Creation + Embedded Contents**

Location kickoff contract:

`docs/LOCATION_CREATION_KICKOFF_V1.md`

Approved sequence:

```text
complete Sandbox Location Creation
→ verify Location + embedded Item acceptance
→ audit/execute controlled prototype-content reset
→ remove/disable legacy reseeding authority
→ retain shared time/weather/economy/runtime infrastructure
→ implement Transmigration foundation against clean Real World
→ Genesis transmigration: Locations -> Items/fixtures -> Characters
→ runtime readiness / activation
→ future Reincarnation/Renewal for modern canonical content
```

The legacy Darian/Thorne Estate/Item world may be retained only as backup/archive evidence, not as active canonical content after reset.

---

## Creation Implementation Standard v1 — completed meta-foundation

The standard was synthesized after detailed review of the completed Character Creation and Item Creation implementations and their failure history.

Key locks:
- exact domain schema instead of free-form properties;
- registry/schema-driven AI and presentation surfaces;
- Manual/AI parity through one authoritative validator/materializer;
- explicit approval into isolated Sandbox state;
- `runtime_ready != running`;
- Edit preflight, Preview before Apply, stale guards and exact pause-state restoration;
- Single and Batch reuse the same exact member schema;
- provider schema/canonicalizer/validator compatibility must be tested as one boundary;
- technical schema burden belongs system-side, not in Creator prompts;
- one bounded repair attempt is recovery only;
- human-readable review + raw `.txt` export;
- safe diagnostics and Cancel/no-write semantics;
- excessive fine realism is non-blocking by default.

`AGENTS.md` carries the repository-level hard lock requiring this standard before Creation work.

---

## Current Item baseline — accepted

Creator selected commit `b59e632aa8e31647b85eeb244a4436c31e9e1e9d` (`Fix Item nutrition basis semantics`, PR #369) as the acceptable Item Creation behavior after later realism checks caused repeated rejection loops.

Rollback PR #372 restored the repository tree to that behavior while preserving history, merged as:

`6fe07ec4fde0375b29477c026e4ace991f8834ce`

Policy lock:

> Do not reintroduce or further tighten fine-grained Item realism validation without explicit Creator authorization.

The representative post-rollback multi-class Item Batch was reviewed and explicitly **approved by Creator on 2026-08-21**. Treat the representative Item acceptance gate as closed for roadmap sequencing; do not regenerate the same proof merely to delay Location work.

Retained Item foundation includes:
- Universal Item Schema + Single/Batch materialization;
- Item/container relations and atomic operations;
- Item Edit parity with pause-state restoration/stale guard;
- Character/Item cleanup controls;
- economics display and AI authoring normalization;
- Universal Grading Socket v1;
- broad Item metric/grading foundation;
- batch ref canonicalization;
- schema/canonicalizer/validator compatibility audit;
- shared Single+Batch AI authoring contract;
- nutrition-basis semantics.

Locked Item ontology:

`Definition -> unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations remain distinct: `contains`, `located_at`, `stored_in`, `owned_by`, `carried_by`, `equipped_by`.

---

# CURRENT AUTHORIZED SLICE — I5.11 Sandbox Location Creation + Embedded Contents

Mandatory kickoff:
- read `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`;
- read `docs/UNIVERSAL_LOCATION_SCHEMA_V1.md`;
- read `docs/LOCATION_CREATION_KICKOFF_V1.md`;
- reuse `docs/CREATION_CONTRACT_REUSE_MAP_V1.md` and shared Creation socket/isolation contracts;
- review existing Character/Item Creation/Edit implementations for reuse points.

Do **not** create a second Location schema.

Required implementation pattern:
- complete Manual/full-schema Location construction surface;
- complete provider-facing AI Location fill form aligned to the exact canonical Location schema;
- strong shared system-side authoring contract so natural Creator prompts are sufficient;
- safe canonicalization + exact Location validation;
- human preview + raw `.txt` technical export;
- AI `typing` feedback;
- Cancel/no-write semantics;
- explicit Creator approval;
- strict Sandbox-only Location materialization;
- active same-Sandbox parent validation;
- acyclic structural parent graph;
- structural parent uses `contains`;
- interface/topology destinations validate active same-Sandbox Locations;
- embedded Items reuse exact current Item member schemas/contracts/storage;
- no arbitrary `contents` bag;
- movable Items normally use `located_at`, or exact `stored_in` typed containers;
- validate the whole Location + contents graph before writes;
- one atomic apply/rollback;
- approved Location detail/browse;
- Location Edit reuses the same schema/validator and standard Preview/Apply/Done lifecycle;
- exact pause-state restoration where a runtime race actually requires pausing;
- no automatic runtime readiness;
- no autonomous execution/ticking;
- no canonical writes.

Acceptance must prove Manual/AI parity, parent/cycle validation, embedded Item parity, atomic no-write failure, write-free preview/export, Sandbox isolation, approved readback, Edit parity and `canonical_state_fingerprint()` stability.

---

# AFTER I5.11 — Genesis transition, not ordinary feature expansion

After Location Creation acceptance, pause automatic progression through the old I5.12–I5.15 sequence and reconcile those slices against the approved Genesis transition.

Next phase:

## G1 — Prototype Content Reset Audit & Contract

Define exact keep/wipe sets and dependency-safe deletion order.

Wipe target includes prototype-era:
- Characters;
- Locations / Estate graph;
- Items, fixtures, inventory content;
- content-specific relations/state tied only to those exemplars.

Preserve reusable infrastructure including time/clock, weather/environment, economy/money, AI/provider, generic event/action/runtime, physiology/effects, Mind/Memory, Creation and schema/validator foundations.

## G2 — Remove legacy reseeding authority

Current initialization paths that recreate Darian/Thorne Estate/legacy inventory must be removed, disabled, generalized or converted to optional test fixtures before production reset.

A restart/deploy must not silently resurrect retired prototype content.

## G3 — Controlled Real World Content Reset

Take bounded backup/archive evidence, perform deterministic cleanup, verify no active orphaned references, and retain shared system infrastructure.

## G4 — Transmigration Foundation

Reuse the approved `docs/CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md`.

Transmigration remains:

`freeze Sandbox revision -> schema/dependency validation -> target-universe compatibility -> canonical ID/ref resolution -> conflict check -> mutation plan -> Creator preview -> explicit approval -> atomic canonical transaction -> provenance`.

## G5 — Genesis Transmigration

Expected dependency-safe order:

1. Location/root spatial graph;
2. Items/fixtures/containers and placement;
3. Characters and valid starting Location binding;
4. runtime readiness/affordance validation;
5. explicit runtime activation.

A Character must not be activated without a valid represented Location.

---

## Future Reincarnation / Renewal

Reincarnation remains planned, but it is no longer a legacy-upgrade mechanism.

Its intended role is to renew **modern canonical content that originally entered through the modern Creation/Transmigration contracts**:

`canonical v1 -> Renew in Sandbox -> edit/regenerate/test -> compatibility + diff -> Creator approval -> canonical v2`.

This keeps legacy prototype cleanup simple and reserves Reincarnation for schema-compatible future evolution.

---

## Retained system locks

- Sandbox-created content never transmigrates automatically.
- Target-universe compatibility/policy validation precedes transmigration.
- `runtime_ready != running`; Created is not alive.
- `canonical_state_fingerprint()` remains a core isolation proof.
- Full autonomous Sandbox ticking remains unauthorized unless Creator explicitly expands scope.
- Current prototype production character/world content is disposable exemplar content under the approved Genesis plan.
- Until reset is actually executed, do not make unverified claims that Real World is already clean or rebuilt.

---

## Exact resume point

**Item representative acceptance is approved and closed. The immediate authorized slice is I5.11 Sandbox Location Creation + Embedded Contents using the existing `UNIVERSAL_LOCATION_SCHEMA_V1.md`, the mandatory `CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`, and `LOCATION_CREATION_KICKOFF_V1.md`. Do not wipe the current Real World yet. After Location Creation acceptance, perform the approved Genesis transition: audit/reset prototype Darian/Thorne Estate/legacy Item content, remove legacy reseeding authority while preserving reusable time/weather/economy/runtime foundations, then implement Transmigration against the clean Real World and rebuild canonical content in dependency-safe order: Locations first, then Items/fixtures, then Characters, then readiness/activation. Future Reincarnation is for modern canonical content, not for preserving the current prototype era.**
