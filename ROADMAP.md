# Observer Sandbox Roadmap

Status: **ACTIVE**  
Roadmap synchronized: **2026-09-02**

## Operating principles

- Current Creator instruction, live repo/schema, verified runtime/DB and current CI/deploy evidence outrank remembered chat context.
- AI proposes structured facts; deterministic contracts validate, derive and mutate.
- Telegram is observer/control, never simulation authority.
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- Universal systems use expandable registry/socket patterns rather than family-specific switchboards.
- `canonical_state_fingerprint()` remains a high-value zero-canonical-mutation invariant.
- Development velocity matters: optional realism polish does not become a blocking treadmill without explicit Creator approval.

## Mandatory Creation gate

Before Creator Creation planning/coding/review/debugging, read:

`docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`

Core vertical:

`versioned schema -> registered socket/reuse map -> Manual full-schema + AI full-schema -> canonicalize -> strict validate -> dependency/graph validate -> write-free preview + .txt -> explicit approval -> atomic Sandbox materialization -> approved detail -> Edit Preview/Apply/Done -> cleanup`

A new Creation domain must not be built as bespoke CRUD.

---

# Current strategic direction — Location first, then Genesis

The current Real World Darian/Thorne Estate/legacy Item world is prototype-era exemplar content and is not a preservation constraint.

Approved principle:

> **Preserve reusable universe infrastructure; retire prototype content; rebuild canonical content from modern Sandbox creations through explicit transmigration.**

Canonical Genesis plan: `docs/CREATOR_REAL_WORLD_RESET_AND_GENESIS_PLAN_V1.md`  
Decision record: `docs/LOCATION_FIRST_GENESIS_DECISION_RECORD_V1.md`

The destructive reset is **not authorized yet**. Full Location acceptance must close first.

---

# Current Location authority

Detailed plan: `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`

Current schema/runtime contracts include:

- `docs/UNIVERSAL_LOCATION_SCHEMA_V2.md`;
- `docs/LOCATION_GRADING_EVIDENCE_MATRIX_V1.md`;
- `src/observer_sandbox/location_creation_schema_v2.py`;
- `src/observer_sandbox/location_schema_registry_v2.py`;
- `src/observer_sandbox/location_ai_contract.py`;
- `src/observer_sandbox/sandbox_location_v2.py`;
- `src/observer_sandbox/sandbox_location_composition.py`;
- `src/observer_sandbox/creator_studio_location_composition.py`;
- `src/observer_sandbox/telegram_creator_studio_location_composition_extension.py`;
- `docs/WORLD_LOCATION_NODE_MODEL.md`;
- `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`;
- `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`;
- `docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`.

`location-v2` is an explicit successor to the retained v1 foundation, not a competing ontology.

## Grading lock

`authoritative Location facts + registered grading sockets + universe policy/reference profiles -> derived Location GradeProfile`

- completeness — mandatory;
- spatial scale — evidence/reference gated;
- infrastructure/facility capability — evidence/reference gated;
- connectivity — graph/context gated;
- asset value — economy/reference gated;
- security — deferred until raw security evidence exists;
- no AI/Creator-authored grade letters/thresholds/evaluator IDs;
- no automatic overall Location grade without explicit composite semantics.

---

# Location implementation slices

## ✅ L11.0 — Schema Refinement + Grading Contract

Closed. `location-v2` locks Geography, Boundary, typed interfaces, registry-backed functional/facility/resource/capability semantics, definition-vs-runtime state separation, minimal control/ownership and grading evidence contracts.

## ✅ L11.1 — Exact Validator + Registry/Grading Foundation

Closed. Exact v2 validation/canonicalization and registry foundations are executable; completeness grading is derived, not authored.

## ✅ L11.2 — Sandbox Persistence + Graph Materializer

Closed. Validated Locations materialize only into isolated Sandbox persistence with stable IDs, same-Sandbox graph checks, acyclic structural hierarchy, typed graph projection, atomic materialization, no runtime activation and canonical isolation.

## ✅ L11.3 — Manual Full-Schema Creation

Closed through PR #380 / CI #1225.

Manual Location authoring provides Guided Build over all 13 creation-owned sections, advanced Exact JSON, whole-payload revalidation, write-free Preview/export, Cancel/no-write and revision-bound Sandbox approval.

## ✅ L11.4 — AI Full-Schema Creation

Closed through PR #382 / CI #1226.

AI Location uses the complete strict provider-facing `location-v2` fill contract, exact deterministic validation, at most one bounded representation-only repair, reroll/typing feedback and the same Preview/export/approval/materializer as Manual.

## ▶ L11.5 — Nested Composition + Embedded Items — IMPLEMENTED, PENDING PRODUCTION/CREATOR SMOKE

The implementation now provides:

- explicit `location-composition-v1` envelope;
- nested child Locations using exact `location-v2` payloads;
- embedded Items using exact current `item-v1` payloads;
- deterministic `$ref` local references;
- structural parent, local topology, Item `located_at` and typed `stored_in` resolution;
- same-Sandbox ref validation, parent-cycle rejection, Item storage-cycle rejection and container-target validation;
- whole dependency graph validation before writes;
- one transaction across all Location + Item members with full rollback on failure;
- stable Sandbox IDs and normal Location/Item persistence/readback;
- shared Creator Studio draft/revision/cancel/export infrastructure;
- Telegram `Nested Composition · Starter` first proof: `Property -> child Room -> movable Item`;
- Telegram `Nested Composition · Exact JSON` path for complete envelope replacement;
- human whole-graph Preview + `.txt` export before approval;
- revision-bound whole-composition confirmation and one atomic approval;
- no runtime activation and no canonical Real World mutation.

Code checkpoint `74c8d3b4cfbf88176b899a4d28ca2e44aba93891` passed CI #1232 including selected regression and CLI smoke. Commits after that checkpoint are continuity-only by exact compare; Public Readiness Security Audit #210 is green. Verify the merged production deploy and Creator Telegram smoke before marking L11.5 fully closed.

Expected production smoke path:

`Creator Studio -> Create -> Location -> Nested Composition · Starter -> Preview/Export -> Approve Whole Composition -> Confirm Whole Composition`

## L11.6 — Detail/Browse + Edit Parity

**NEXT after L11.5 production/Creator smoke.**

Expose hierarchy/topology/facility/environment/economic facts and derived Location GradeProfile. Edit reuses exact schema/validator with stale guard, Preview/Apply/Done, audit and exact pause restoration only where a real Sandbox runtime race exists.

## L11.7 — Full Location Vertical Acceptance

Prove property/building and room/outdoor graphs, explicit topology, unknown geography without fabrication, boundary semantics, facilities/resources, grading, nested Locations, embedded Items, Manual/AI parity, atomic approval, failure/no-write behavior, Edit parity, Real World fingerprint stability and non-activation after approval.

Only after L11.7 closes does the Genesis transition begin.

---

# Recent Character UX parity

PR #379 / CI #1223 added read-only **Full Profile `.txt` export** for approved Sandbox Characters from both Character detail and Profile menu.

It exports current approved Sandbox profile values—including Creator edits—plus Skills, Preferences, Hobbies and Habits, while intentionally excluding live runtime-owned changing state. Export is read-only and reuses the shared Telegram document delivery path.

---

# After Location acceptance — Genesis transition

1. **G1 — Prototype Content Reset Audit & Contract** — exact keep/wipe sets and cleanup order.
2. **G2 — Remove legacy reseeding authority** — Darian/Thorne Estate/legacy Item bootstrap cannot resurrect retired content.
3. **G3 — Controlled Real World content reset** — retire prototype content while preserving reusable infrastructure.
4. **G4 — Transmigration Foundation** — freeze Sandbox revision -> schema/dependency validation -> target-universe compatibility -> conflict/id resolution -> Creator preview -> explicit approval -> atomic canonical materialization -> provenance.
5. **G5 — Genesis Transmigration** — Locations/root topology -> Items/fixtures/containers + placement -> Characters + valid starting Location -> readiness/affordances -> explicit activation.

A Character cannot be activated without a valid represented Location.

Preserve reusable time/clock, weather/environment, economy/money, AI/provider, generic event/action/runtime, physiology/effects, Mind/Memory, grading/requirements/quantity/economic-value and Creation infrastructure.

---

# Future Reincarnation / Renewal

Reincarnation is modern-to-modern canonical renewal, not preservation of prototype-era content:

`modern canonical v1 -> Renew in Sandbox -> edit/regenerate/test -> compatibility + diff -> Creator approval -> canonical v2`

---

## Retained locks

- no automatic transmigration;
- target-universe compatibility before canonical promotion;
- `runtime_ready != running`;
- full autonomous Sandbox ticking remains separately unauthorized;
- missing grading evidence/reference => ungraded, not invented precision;
- Location grade never automatically becomes access authorization;
- overall grade requires explicit composite semantics;
- current Real World prototype content still exists until future reset is actually implemented and verified;
- do not make deploy/live claims without current evidence.

## Exact resume point

**Merge PR #384 using the already-green runtime code checkpoint because subsequent commits are docs-only by exact compare, then require the automatic production deploy to pass runtime health and Telegram API connectivity. Have the Creator smoke-test Nested Composition · Starter through Preview/Export and whole-composition approval. If that passes, mark L11.5 closed and begin L11.6 approved Location Detail/Browse + Edit parity.**
