# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-08-20**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
5. `docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md` for grading work
6. task-relevant canonical contracts/source
7. current branch/PR/CI/runtime evidence before completion or live claims.

Authority:
`current Creator instruction > live repo contracts/config/schema > verified runtime/DB > CI/deploy evidence > continuity docs > remembered chat`.

Persistent branches: `main`, `test` only.
Workflow: `test -> focused verification -> PR/CI -> merge main -> deploy/runtime verification when applicable -> continuity sync -> exact main/test sync`.
Do not infer production deployment from merge alone.

---

## Current checkpoint

### Fresh Item Edit live acceptance — PASS

Creator live verification confirmed PR #358's physical-quantity idempotence fix works: freshly-created/approved Items can now enter Item Edit successfully despite persisted normalized `{kind,value,unit}` quantities.

PR #358 merge: `9c93739655fc6981a8c5bfd31a7c83a4cce16f62`; CI #1194 passed.

The earlier `modules.physical.mass.kind` failure was a current validator self-normalization bug, not merely legacy data. Current contract accepts authoring `{value,unit}` and its own normalized `{kind,value,unit}` only with the correct physical dimension; unrelated extras remain invalid.

### Universal Grading Socket Architecture v1 — repository accepted

Creator approved a socket-first grading architecture so unbounded Item/future-universe content does not require one hard-coded grading table per entity family.

PR **#360** merged at:
`9155a94bc75b800d4a10f2a39993647c78d11d9c`

CI **#1195**: **SUCCESS** — targeted regression + CLI smoke.

New canonical doc:
`docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`.

Core invariant:
`authoritative raw state + registered grading sockets + universe policy -> derived GradePlan -> deterministic GradeProfile`.

Implemented sockets:
- `EvaluatorSpec` / evaluator registry;
- `DimensionSpec` / dimension registry;
- `ReferenceProfile` registry;
- `UniverseGradingPolicy`;
- rebuildable `GradePlan`;
- deterministic `GradeProfile` resolution.

Current Item integration:
- reuses existing `item-resistance-load-v1` through registered `item / resistance_load`;
- 55 lb-equivalent training resistance remains S;
- Creator draft review and approved Sandbox Item detail show human-facing grading such as `Resistance Load: S · Expert`;
- ordinary Items with no registered applicable dimension explicitly show that no grading dimension applies yet;
- raw `.txt` export remains non-authoritative authoring data and does not gain GradePlan fields;
- no DB migration or persisted new grade authority.

Default realistic-universe policy explicitly allowlists current legitimate dimensions/evaluators and caps current Item load grading at S. Merely registering a future supernatural dimension does not admit it into the realistic universe.

Deployment/live Telegram rendering for PR #360 remains separately unverified unless Creator/runtime evidence confirms it.

---

## Grading semantic locks

Canonical vocabulary remains:
`E < D < C < B < A < S < SS < SSS < X < XX`.

Rules:
- shared vocabulary, domain-specific evaluators;
- raw facts remain authority;
- arbitrary numeric fields are not automatically gradeable;
- missing evidence/reference => ungraded, not fabricated precision;
- overall grade requires an explicit composite scheme/evaluator;
- **Item Grade describes the item. Requirement Grade describes the interaction.**
- Item grade never automatically becomes a Character requirement;
- Location grade never automatically becomes access authorization;
- new universe-specific dimensions require explicit universe-policy allowance.

Future gradeable concepts should normally be added through:
`EvaluatorSpec + DimensionSpec + optional ReferenceProfile + UniverseGradingPolicy allowance`
without editing Item-family switches or resolver core.

---

## Retained Creator / Item foundation

I5.2 through I5.10 remain complete and must not be rebuilt:
- reuse map;
- universal physical quantity/measurement;
- cross-domain grading;
- requirements/access;
- Universal Item Schema v1;
- single + batch Item materialization;
- Item/container operations;
- Universal Location Schema v1.

Item Creator Studio also retains Single/Batch AI/manual creation, strict validation, realism/self-correction, human review + raw export, approved details/economics, Item Edit parity/diagnostics, and Character/Item batch cleanup.

Sandbox/Real World isolation, no automatic transmigration, `runtime_ready != running`, relation ontology, canonical fingerprint safety and no unauthorized full Sandbox autonomous ticking remain locked.

---

## Immediate next development order

Creator changed the order before I5.11: continue **Item Grading Coverage expansion** on top of the accepted socket architecture, then return to Location creation.

Next bounded grading work should:
1. verify PR #360 live Telegram grading presentation when deployed;
2. add additional evidence-backed reusable Item dimensions/reference profiles rather than Item-family switches;
3. add a structured AI applicability-plan proposal only where useful, with every proposed dimension/evaluator/reference resolved through registries + universe policy + evidence before deterministic grading;
4. keep unknown/uncovered Items valid and explicitly ungraded;
5. avoid invented thresholds/reference baselines;
6. add overall Item grade only when an explicit defensible composite contract exists.

After the intended Item grading coverage checkpoint is accepted, resume **I5.11 — Sandbox Location Creation + Embedded Contents**.

Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed. Full autonomous Sandbox ticking remains separately unauthorized.

---

## Exact resume sentence

**Fresh Item Edit is live-confirmed working after PR #358. PR #360 is merged at `9155a94bc75b800d4a10f2a39993647c78d11d9c` with CI #1195 green and establishes Universal Grading Socket Architecture v1 plus first Item coverage: registry-driven resistance-load grading, explicit ungraded state for uncovered Items, universe-policy gating, and grading in draft/approved Item views without new persisted grade authority. Verify #360 live when available, continue evidence-backed Item Grading Coverage expansion through sockets rather than Item-family hard-coding, then resume I5.11.**
