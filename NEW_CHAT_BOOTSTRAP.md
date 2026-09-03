# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-09-03**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
5. `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md` for Creator Creation work
6. task-relevant canonical plans/contracts/source
7. current branch/PR/CI/runtime evidence before completion/live claims.

Authority:
`current Creator instruction > live repo contracts/config/schema > verified runtime/DB > CI/deploy evidence > continuity docs > remembered chat`.

Persistent branches: `main`, `test` only.  
Workflow: `test -> focused verification -> PR/CI -> merge main -> deploy/runtime verification when applicable -> continuity sync -> exact main/test sync`.

Do not infer production deployment from merge alone.

---

# Current checkpoint

## ✅ Modern Sandbox Location Creation — FULL VERTICAL ACCEPTED

All Location slices are closed:

- ✅ L11.0 — `location-v2` schema refinement + grading contract
- ✅ L11.1 — exact validator + registry/grading foundation
- ✅ L11.2 — isolated Sandbox persistence + graph materializer
- ✅ L11.3 — Manual full-schema creation
- ✅ L11.4 — AI full-schema creation
- ✅ L11.5 — Nested Composition + Embedded Items
- ✅ L11.6 — Detail/Browse + Edit + Cleanup parity
- ✅ **L11.7 — Full Location Vertical Acceptance**

Final acceptance authority:
- `docs/LOCATION_VERTICAL_ACCEPTANCE_V1.md`
- `tests/test_location_vertical_acceptance_v1.py`
- PR #407 — Full Location Vertical Acceptance
- CI #1281 — representative acceptance green after correcting a test-only DB-column assumption
- CI #1282 — final acceptance rerun + CLI init/status smoke green
- PR #407 merge: `c3e8cbb556d0037c8310261398c19a0939bec09a`

L11.7 required **no production implementation patch**. CI #1280 exposed only an acceptance-test mistake: the test guessed `creation_sandbox_item_instances.source_json`. The test was corrected to use approved `get_sandbox_item()` output, then acceptance passed.

## Accepted Location vertical

The accepted current scope includes:

- exact `location-v2` schema/normalization;
- registry-backed location kinds, functions, facilities/resources/capabilities/utilities and topology vocabulary;
- partial/unknown geography without fabrication;
- physical/open/mixed boundary semantics;
- access policy separate from operating state;
- property -> building -> room and property -> outdoor-zone hierarchy;
- explicit typed interfaces/topology;
- atomic same-Sandbox graph materialization;
- nested Location compositions and embedded heterogeneous Item kinds;
- deterministic `$ref` resolution and cycle/dependency rejection;
- Manual Guided/Exact JSON and AI full-schema parity;
- write-free Preview and `.txt` export;
- revision-bound explicit approval;
- approved browse/detail;
- Creator-friendly field Edit: `Section -> Field -> friendly input/choice -> changed-field Preview -> Apply -> Continue/Done`;
- raw JSON only as explicit Advanced fallback;
- source-fingerprint stale protection and graph preflight;
- dependency-aware fail-closed cleanup with explicit confirmation;
- canonical Real World isolation;
- approved Locations remain not runtime-active.

## Grading lock

Current Location grading activates **completeness only**. This is intentional:

- grades are derived, never authored by AI/Creator;
- `GradeProfile.overall` remains `None`;
- spatial scale, infrastructure/facility capability, connectivity and asset value remain evidence/reference gated;
- security remains deferred until raw security evidence exists;
- missing evidence/reference means ungraded, not invented precision.

## Transactional canonical-isolation lock

For Sandbox mutation paths that prove Real World isolation:

`acquire writer transaction -> canonical fingerprint before -> Sandbox-only writes -> canonical fingerprint after -> mismatch => rollback / match => commit`

Never compare across an unlocked or post-commit window.

---

# Current strategic direction — Genesis transition

Location-first prerequisite is now satisfied.

Approved principle:

> **Preserve reusable universe infrastructure; retire prototype content; rebuild canonical content from modern Sandbox creations through explicit transmigration.**

Current Real World Darian, Thorne Estate and legacy Item/fixture/inventory content remain prototype-era exemplar content until the future reset is explicitly performed.

## ▶ NEXT — G1 Prototype Content Reset Audit & Contract

G1 is an **audit/contract slice**, not the destructive reset itself.

It must determine exact keep/wipe scope and cleanup ordering before any canonical mutation. At minimum audit:

- prototype Characters and Character-owned runtime/state;
- Thorne Estate / legacy Location rows and graph projections;
- legacy Items, fixtures, inventory, definitions and economic profiles;
- bootstrap/reseed paths capable of recreating retired content;
- generic reusable universe infrastructure that must survive;
- references/dependencies that constrain deletion order;
- canonical services/tables that are infrastructure rather than prototype content;
- rollback/backup and verification requirements for later destructive execution.

G1 should produce a reviewed reset contract with explicit **KEEP**, **WIPE**, **RESEED-AUTHORITY REMOVE**, and **ORDER/DEPENDENCY** sets. It must not perform the destructive reset.

Later sequence:

1. **G1 — Prototype Content Reset Audit & Contract**
2. **G2 — Remove legacy reseeding authority**
3. **G3 — Controlled Real World content reset**
4. **G4 — Transmigration Foundation**
5. **G5 — Genesis Transmigration** — Locations -> Items/fixtures/containers -> Characters -> readiness/affordances -> explicit activation

A Character cannot be activated without a valid represented Location.

---

# Retained universal locks

- Create anywhere safely; canon nowhere automatically.
- No automatic transmigration.
- Schema-valid does not imply universe-compatible.
- Target-universe compatibility precedes canonical promotion.
- `runtime_ready != running`; Created is not alive.
- Full autonomous Sandbox ticking remains separately unauthorized.
- AI proposes facts; deterministic contracts validate/derive/mutate.
- No automatic overall Location grade without explicit composite semantics.
- Prototype Real World content still exists until reset is actually implemented and verified.
- **G1 is audit/contract only; no destructive Real World mutation is authorized by entering G1.**
- Do not make deploy/live claims without current evidence.

## Exact resume sentence

**Location Creation is fully accepted through L11.7 / PR #407 / CI #1282. Begin G1 Prototype Content Reset Audit & Contract: inventory exact KEEP/WIPE/reseed-removal/dependency-order sets without performing destructive canonical mutation.**
