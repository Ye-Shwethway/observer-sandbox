# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-08-31**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
5. `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md` for current Location work
6. task-relevant canonical contracts/source
7. current branch/PR/CI/runtime evidence before completion/live claims.

For any Creator Creation work, `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md` is mandatory before material planning/coding/review/debugging.

Authority:
`current Creator instruction > live repo contracts/config/schema > verified runtime/DB > CI/deploy evidence > continuity docs > remembered chat`.

Persistent branches: `main`, `test` only.
Workflow: `test -> focused verification -> PR/CI -> merge main -> deploy/runtime verification when applicable -> continuity sync -> exact main/test sync`.
Do not infer production deployment from merge alone.

---

# Current checkpoint

The representative post-rollback Item acceptance gate remains explicitly approved and closed.

The immediate authorized feature family remains **modern Sandbox Location Creation**, because Characters and Items cannot form a runnable rebuilt world without represented spatial structure, topology and placement.

Current verified implementation progression:

- **L11.0 — closed**: explicit `location-v2` schema refinement + grading contract;
- **L11.1 — closed**: exact validator + registry/grading foundation;
- **L11.2 — closed**: isolated Sandbox Location persistence + graph materializer;
- **L11.3 — closed**: full Manual Location authoring including Guided Build + Exact JSON + Preview/export/approval;
- **L11.4 — current next slice**: complete the AI structured-fill contract.

Recent verified checkpoints:

- PR #379 / CI #1223 — approved Sandbox Character full-profile `.txt` export;
- PR #380 / CI #1225 — Guided Manual Location Builder completion;
- PR #380 merge checkpoint: `fe48d16bf9e6825e08bd12e90424dfa7636307c4` before continuity-only follow-up.

Do not make deploy/live claims from these merges alone.

Canonical current docs/contracts:

- `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`
- `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/LOCATION_CREATION_KICKOFF_V1.md`
- `docs/UNIVERSAL_LOCATION_SCHEMA_V2.md`
- `docs/LOCATION_GRADING_EVIDENCE_MATRIX_V1.md`
- `docs/WORLD_LOCATION_NODE_MODEL.md`
- `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`
- `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`
- `docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`
- `docs/CREATOR_REAL_WORLD_RESET_AND_GENESIS_PLAN_V1.md`
- `docs/LOCATION_FIRST_GENESIS_DECISION_RECORD_V1.md`

---

# Closed Location foundation

## L11.0 — Schema refinement

`location-v2` is the explicit successor to the retained v1 Location foundation. It is not a competing ontology.

It includes the approved refinement scope:

1. optional Geography;
2. explicit Boundary semantics;
3. registry-backed interface kinds;
4. registry-backed functional classes/facility/resource/capability vocabulary;
5. stable definition/configuration vs initial/live runtime-state separation;
6. minimal control/ownership semantics;
7. Location-specific universal grading evidence/profile.

## L11.1 — Exact validator / grading foundation

The exact v2 validator/canonicalizer and registry vocabulary are executable. Derived grading remains non-authored. Unknown precision remains unknown.

## L11.2 — Sandbox persistence/materializer

Validated Locations materialize only into Creation Sandbox state with stable IDs, same-Sandbox parent/reference checks, acyclic hierarchy, explicit topology projection, atomic apply and zero canonical Real World writes. Approval does not activate runtime.

## L11.3 — Manual full-schema creation

Manual Location Creation now supports:

- **Guided Build** seeded from one sparse valid `location-v2` source payload;
- all 13 supported creation-owned sections:
  - Identity
  - Structure
  - Geography
  - Spatial
  - Boundary
  - Access
  - Operations
  - Topology
  - Facilities
  - Environment
  - Control
  - Economics
  - Provenance
- one-section-at-a-time replacement JSON;
- whole-payload exact validation before each new draft revision is saved;
- invalid section update => prior revision remains intact / zero Location materialization;
- advanced Exact JSON path retained;
- write-free Preview and `.txt` export;
- explicit revision-bound Approve into Sandbox;
- same L11.2 validator/materializer path;
- no runtime activation and no canonical Real World mutation.

---

# Immediate resume — L11.4 AI Full-Schema Location Creation completion

An AI Location foundation already exists. Do not rebuild it.

Already present:

- natural-language Location intent;
- `location-v2` registry-aware authoring prompt;
- exact v2 validation;
- reroll/revision support;
- same Preview/export/Approve flow as Manual;
- same L11.2 materializer;
- unknown facts remain null/empty;
- AI cannot author grades/derived fields;
- AI cannot invent Sandbox object refs;
- no runtime/canonical activation.

Remaining L11.4 contract gaps to close:

1. **Complete provider-facing structured fill schema**
   - replace the current loose `{type: object}` provider schema;
   - derive/align the provider schema from authoritative `location-v2` structure + registries;
   - include exact required fields, nested shapes, enums and nullability supported by the provider contract;
   - final deterministic validator remains authoritative.

2. **Bounded deterministic repair**
   - at most one repair attempt;
   - repair only deterministic representation/schema-shape issues;
   - do not use repair to invent missing world facts, coordinates, value, topology or refs;
   - if repaired payload still fails exact validation => no saved draft / zero materialization.

3. **Telegram typing feedback**
   - send typing/action feedback during AI generation and reroll so long model calls do not look dead;
   - Telegram remains adapter only.

4. **Convergence proof**
   - AI and Manual still land in the exact same source payload contract;
   - same draft revision model;
   - same Preview/export;
   - same explicit approval confirmation;
   - same L11.2 materializer;
   - `canonical_state_fingerprint()` unchanged by draft/review/failed AI generation.

Do **not** start L11.5 nested composition before this closes.

---

# Location grading lock

Reuse:

`authoritative Location facts + registered grading sockets + universe policy/reference profiles -> derived Location GradeProfile`

`location-completeness-v1` remains the mandatory representation-completeness dimension.

Evidence/reference-gated dimensions:

- completeness — mandatory;
- spatial scale — magnitude only, kind/reference aware;
- infrastructure/facility capability — registry evidence based;
- connectivity/mobility — graph evidence based and separate from access;
- asset value — economy/reference gated;
- security/protection — deferred until authoritative raw security evidence exists.

Rules:

- AI/Creator does not author final grade letters/thresholds/evaluator ids/reference profiles;
- missing evidence/reference => ungraded dimension;
- no automatic overall Location grade without explicit composite semantics;
- Location grades never automatically grant access or satisfy Character requirements.

---

# Later Location slice sequence

- **L11.5** Nested Composition + Embedded Items
- **L11.6** Approved Detail/Browse + Edit Parity
- **L11.7** Full Location Vertical Acceptance

All Location work follows the shared Creation pipeline:

`versioned schema -> registered socket -> Manual/AI same exact payload -> canonicalize -> strict validate -> graph/dependency validate -> write-free preview/export -> explicit Sandbox approval -> atomic materialization -> detail/browse -> Edit Preview/Apply/Done -> cleanup`

No automatic runtime activation or Real World mutation.

---

# Structural Location locks

- stable technical identity independent of display path/name;
- `contains` = structural hierarchy;
- `connected_to` / interfaces = traversable topology;
- `located_at` = dynamic physical presence;
- access authorization != topology != current operating state;
- one canonical structural parent in first implementation;
- structural hierarchy must be acyclic;
- parent/interface refs resolve only within valid same-Sandbox/dependency scope;
- unknown geometry/geography remains unknown;
- no arbitrary generic `contents` bag;
- nested child Locations reuse exact Location schema;
- embedded Items reuse exact Item member schema/Batch semantics;
- whole composition validates before one atomic apply;
- movable Items normally use `located_at`, or `stored_in` when a valid typed container exists;
- ownership remains independent.

---

# Recent Character export parity

Already-created active Sandbox Characters expose **📄 Export Full Profile (.txt)** from both Character detail and Profile menu.

The export reads current approved Sandbox profile persistence, so Creator-edited current values are exported rather than stale original creation values. It includes profile fields, Skills, Preferences, Hobbies, Habits and object/provenance context. Live runtime-owned changing state is intentionally outside the profile export.

Export is read-only and reuses the existing Telegram text-document delivery path.

---

# Approved Real World Genesis direction — later

Current Darian, Thorne Estate and legacy Item/fixture/inventory world are prototype-era exemplars, not preservation constraints.

Approved principle:

> **Preserve reusable universe infrastructure; retire prototype content; rebuild canonical content from modern Sandbox creations through explicit transmigration.**

The destructive reset is **not authorized before L11.7 Location acceptance**.

After Location acceptance:

`prototype keep/wipe audit -> remove/disable legacy reseeding -> controlled Real World content reset -> preserve time/weather/economy/AI/runtime/schema foundations -> Transmigration foundation -> Genesis Locations -> Items/fixtures -> Characters -> readiness/affordances -> explicit activation`

A Character cannot be activated without a valid represented Location.

---

# Reincarnation / Renewal — future

Reincarnation is reserved for modern canonical content originally created through the modern Creation/Transmigration contracts:

`modern canonical v1 -> Renew in Sandbox -> edit/regenerate/test -> compatibility + diff -> explicit Creator approval -> canonical v2`

Do not build a complex legacy-upgrade bridge for current prototype content.

---

## Retained universal locks

- Create anywhere safely; canon nowhere automatically.
- Sandbox-created content never transmigrates automatically.
- Target-universe compatibility precedes transmigration.
- `runtime_ready != running`; Created is not alive.
- `canonical_state_fingerprint()` remains a core isolation proof.
- Full autonomous Sandbox ticking remains separately unauthorized.
- Fine-grained realism remains non-blocking by default unless an explicit domain contract + Creator authorization changes that.
- Until reset is actually implemented/verified, current Real World prototype content still exists; do not claim otherwise.
- Do not make deploy/live claims without current evidence.

## Exact resume sentence

**Continue L11.4 from the existing AI Location foundation. Replace the loose provider output schema with the complete authoritative `location-v2` structured fill schema, add at most one bounded deterministic repair attempt, add Telegram typing feedback, and prove AI/Manual still converge on the same exact validator, draft revision model, Preview/export, revision-bound approval and L11.2 materializer. Then merge green and only afterward begin L11.5 nested Location + embedded Item composition.**
