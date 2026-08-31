# Observer Sandbox Roadmap

Status: **ACTIVE**  
Roadmap synchronized: **2026-08-31**

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

Manual Location authoring now provides:

- Guided Build from a sparse valid `location-v2` draft;
- all 13 creation-owned sections: Identity, Structure, Geography, Spatial, Boundary, Access, Operations, Topology, Facilities, Environment, Control, Economics, Provenance;
- one-section-at-a-time replacement with whole-payload revalidation and revision increment;
- advanced Exact JSON path;
- write-free Preview and `.txt` export;
- Cancel/no materialization;
- revision-bound explicit approval using the same L11.2 materializer.

## ✅ L11.4 — AI Full-Schema Creation

Closed through PR #382 / CI #1226.

The AI Location path now provides:

- short natural-language Creator intent;
- complete strict provider-facing `location-v2` structured fill schema instead of loose `{type: object}`;
- registry-backed nested enums/shapes aligned with the authoritative v2 contract;
- final authority remains `validate_location_payload_v2()`;
- at most one deterministic representation-only repair pass;
- repair may remove non-authoritative grade/derived metadata and normalize safe representation details, but cannot invent missing Location facts, coordinates, topology or refs;
- semantic-invalid/missing required content fails closed with no saved draft or materialization;
- AI reroll uses the same schema/validator/revision model;
- best-effort Telegram `typing` feedback during Location AI generation/reroll;
- typing transport failures cannot affect Creation semantics;
- same Preview/export/revision-bound approval/L11.2 materializer as Manual;
- no runtime activation and no canonical Real World mutation.

Verified merge checkpoint for this slice: `7c9d6febb3668cfb32040b92788085eb73e28c30` before continuity-only follow-up.

## ▶ L11.5 — Nested Composition + Embedded Items — CURRENT NEXT SLICE

**Goal:** create useful spatial graphs atomically rather than isolated empty nodes.

Required contract:

- nested child Locations reuse exact current `location-v2` member payloads;
- embedded Items reuse exact current Item schema / Batch semantics;
- do not invent a weaker Location/Item sub-schema;
- do not introduce an arbitrary generic `contents` JSON bag;
- batch-local refs must be deterministic and resolvable before writes;
- child structural placement uses `contains` semantics;
- movable Items normally use `located_at`;
- Item in a valid typed container uses `stored_in`;
- ownership remains independent of placement;
- topology destinations may resolve to active same-Sandbox Locations or same-composition local refs;
- validate the whole dependency graph before any materialization;
- any invalid member/ref/cycle/dependency => zero materialized writes;
- one explicit approval must apply the complete composition atomically;
- write-free Preview and raw export must show nested contents before approval;
- resulting objects remain not runtime-active and canonical Real World fingerprint remains unchanged.

Implementation should first audit/reuse existing Item Batch local-ref/atomic materializer patterns and existing Location v2 graph materializer before defining the smallest shared composition envelope.

## L11.6 — Detail/Browse + Edit Parity

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

**Begin L11.5 by auditing the existing Item Batch local-ref/atomic materializer and current Location v2 materializer. Define the smallest shared composition envelope that embeds exact `location-v2` child payloads and exact current Item payloads, resolves deterministic local refs for parent/topology/placement/storage, validates the entire graph before writes, previews/exports the whole composition, and applies it in one Sandbox-only atomic approval. Do not create a generic contents bag or weaker duplicate schemas.**
