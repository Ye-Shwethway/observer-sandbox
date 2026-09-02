# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-09-02**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
5. `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`
6. task-relevant canonical contracts/source
7. current branch/PR/CI/runtime evidence before completion/live claims.

For Creator Creation work, `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md` is mandatory.

Authority:
`current Creator instruction > live repo contracts/config/schema > verified runtime/DB > CI/deploy evidence > continuity docs > remembered chat`.

Persistent branches: `main`, `test` only.  
Workflow: `test -> focused verification -> PR/CI -> merge main -> deploy/runtime verification when applicable -> continuity sync -> exact main/test sync`.

Do not infer production deployment from merge alone.

---

# Current checkpoint

Immediate authorized feature family: **modern Sandbox Location Creation**.

Verified progression:

- ✅ L11.0 — `location-v2` schema refinement + grading contract
- ✅ L11.1 — exact validator + registry/grading foundation
- ✅ L11.2 — isolated Sandbox persistence + graph materializer
- ✅ L11.3 — Manual full-schema creation: Guided Build + Exact JSON + Preview/export/approval
- ✅ L11.4 — AI full-schema creation
- ▶ **L11.5 — Nested Composition + Embedded Items — IMPLEMENTED ON `test`, PENDING MERGE/DEPLOY/CREATOR SMOKE**
- L11.6 — Detail/Browse + Edit parity
- L11.7 — Full Location vertical acceptance

L11.5 current `test` truth:

- explicit `location-composition-v1` envelope;
- exact `location-v2` child members and exact current `item-v1` members;
- deterministic `$ref` resolution for structural parent, topology, `located_at`, and `stored_in`;
- same-Sandbox reference checks, structural cycle checks, Item storage cycle checks, container validation and whole-graph dependency validation before writes;
- one transaction for all Location + Item member materialization with rollback on failure;
- shared Creator Studio draft/revision/export/cancel infrastructure;
- Telegram `🧩 Nested Composition · Starter` first proof (`Property -> Room -> movable Item`);
- Telegram `🧾 Nested Composition · Exact JSON` replacement/input path;
- human whole-graph Preview + `.txt` export before approval;
- revision-bound whole-composition confirmation and atomic approval;
- resulting members remain not runtime-started and canonical Real World fingerprint remains unchanged.

Runtime code checkpoint `74c8d3b4cfbf88176b899a4d28ca2e44aba93891` passed CI #1232 including the selected regression set and CLI smoke. The commits after that checkpoint change continuity documentation only; `74c8d3b..latest` compare proves no runtime/source delta. Public Readiness Security Audit #210 is green. A later redundant CI run on the docs-advanced PR head became runner-stalled and is not a reason to repeat an already-green unchanged runtime suite; repository policy explicitly does not require full Python CI for docs-only changes.

Recent prior checkpoints:

- PR #379 / CI #1223 — approved Sandbox Character Full Profile `.txt` export
- PR #380 / CI #1225 — Guided Manual Location Builder
- PR #382 / CI #1226 — complete Location AI full-schema creation
- PR #383 — continuity advanced to L11.5

No deploy/live claim is implied until the current runtime-affecting PR is merged and deploy/runtime health is verified.

---

# Current Location contracts

- `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`
- `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/UNIVERSAL_LOCATION_SCHEMA_V2.md`
- `docs/LOCATION_GRADING_EVIDENCE_MATRIX_V1.md`
- `src/observer_sandbox/location_creation_schema_v2.py`
- `src/observer_sandbox/location_schema_registry_v2.py`
- `src/observer_sandbox/location_ai_contract.py`
- `src/observer_sandbox/sandbox_location_v2.py`
- `src/observer_sandbox/sandbox_location_composition.py`
- `src/observer_sandbox/creator_studio_location_composition.py`
- `src/observer_sandbox/telegram_creator_studio_location_composition_extension.py`
- `docs/WORLD_LOCATION_NODE_MODEL.md`
- `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`
- `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`
- `docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`

`location-v2` is an explicit successor to the retained v1 Location foundation, not a competing ontology.

---

# Closed Location foundation

## L11.0 — Schema / grading

`location-v2` includes Geography, Boundary, typed interfaces, registry-backed functional/facility/resource/capability semantics, definition/configuration vs initial/live runtime-state separation, minimal control/ownership and Location grading evidence/profile contracts.

Grades are derived. Creator/AI does not author final grade letters, thresholds, evaluator IDs or reference profiles.

## L11.1 — Exact validator

Exact v2 validation/canonicalization is executable. Unknown precision remains unknown. Completeness remains derived, not authored.

## L11.2 — Sandbox persistence/materializer

Validated Locations materialize only into Creation Sandbox state with stable IDs, same-Sandbox graph checks, acyclic hierarchy, explicit topology projection and atomic apply. Approval does not activate runtime and does not mutate canonical Real World state.

## L11.3 — Manual full-schema creation

Manual supports Guided Build from sparse valid `location-v2`, all 13 creation-owned sections, one-section replacement with whole-payload revalidation and revision increments, advanced Exact JSON, write-free Preview + `.txt`, Cancel/no-write and revision-bound explicit approval through the L11.2 materializer.

## L11.4 — AI full-schema creation

AI Location uses short natural-language Creator intent, complete strict provider-facing `location-v2` structured schema, authoritative registry-backed nested shapes/enums, final deterministic `validate_location_payload_v2()` authority, at most one deterministic representation-only repair pass, reroll through the same draft/revision model, best-effort Telegram typing feedback and the same Preview/export/approval/materializer as Manual.

---

# L11.5 — Nested Composition + Embedded Items

Current implementation uses the smallest explicit composition envelope:

`location-composition-v1 = {schema_version, locations:[{ref,payload: exact location-v2}], items:[{ref,payload: exact item-v1}]}`

Locks:

- no generic `contents` bag;
- no weaker duplicate Location/Item schemas;
- deterministic local refs resolve before writes;
- child structural relation = `contains`;
- movable Item placement = `located_at`;
- typed container storage = `stored_in`;
- ownership remains independent;
- topology may target active same-Sandbox Locations or same-composition Location refs;
- invalid member/ref/cycle/dependency => zero materialized writes;
- Preview/export remain member-write-free;
- one explicit revision-bound approval applies the whole graph atomically;
- no runtime activation;
- `canonical_state_fingerprint()` remains unchanged.

The Telegram smoke path after successful production deploy is:

`Creator Studio -> Create -> Location -> 🧩 Nested Composition · Starter -> review Property/Room/Item -> optional Export -> Approve Whole Composition -> Confirm Whole Composition`.

Do not call this live/testable until deploy runtime health and Telegram API connectivity have passed for the merged checkpoint.

---

# Next after L11.5 production verification

Proceed to **L11.6 — Detail/Browse + Edit Parity**:

- approved Location browse/detail;
- readable hierarchy/topology/facility/environment/economic facts;
- Location GradeProfile presentation;
- Edit using the same exact schema/validator;
- stale guard;
- Preview -> Apply -> Done;
- audit and exact pause restoration only where a real Sandbox runtime race exists;
- cleanup/archive parity.

Do not enter destructive Real World reset/Genesis work until L11.7 closes.

---

# Approved Real World Genesis direction — later

Current Darian, Thorne Estate and legacy Item/fixture/inventory content are prototype-era exemplars, not preservation constraints.

Approved principle:

> **Preserve reusable universe infrastructure; retire prototype content; rebuild canonical content from modern Sandbox creations through explicit transmigration.**

Destructive reset is **not authorized before L11.7**.

After Location acceptance:

`prototype keep/wipe audit -> remove legacy reseeding -> controlled Real World content reset -> preserve reusable systems -> Transmigration foundation -> Genesis Locations -> Items/fixtures -> Characters -> readiness/affordances -> explicit activation`

A Character cannot be activated without a valid represented Location.

---

# Future Reincarnation

`modern canonical v1 -> Renew in Sandbox -> edit/regenerate/test -> compatibility + diff -> explicit Creator approval -> canonical v2`

Do not build a complex legacy preservation bridge.

---

## Retained universal locks

- Create anywhere safely; canon nowhere automatically.
- No automatic transmigration.
- Target-universe compatibility precedes canonical promotion.
- `runtime_ready != running`; Created is not alive.
- Full autonomous Sandbox ticking remains separately unauthorized.
- Fine realism remains non-blocking unless explicitly authorized.
- Current Real World prototype content still exists until reset is actually implemented and verified.
- Do not make deploy/live claims without current evidence.

## Exact resume sentence

**Merge PR #384 using the already-green runtime checkpoint because subsequent commits are docs-only by exact compare, then verify the automatic production deploy including runtime health and Telegram API connectivity. Once production is green, have the Creator smoke-test `Creator Studio -> Create -> Location -> Nested Composition · Starter -> Preview/Export -> Approve Whole Composition -> Confirm`. If that passes, close L11.5 and proceed to L11.6 Detail/Browse + Edit parity.**
