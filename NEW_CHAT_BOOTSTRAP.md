# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-08-20**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
5. `docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`
6. `docs/ITEM_GRADING_COVERAGE_FOUNDATION_V1.md`
7. task-relevant canonical contracts/source
8. current branch/PR/CI/runtime evidence before completion or live claims.

Authority:
`current Creator instruction > live repo contracts/config/schema > verified runtime/DB > CI/deploy evidence > continuity docs > remembered chat`.

Persistent branches: `main`, `test` only.
Workflow: `test -> focused verification -> PR/CI -> merge main -> deploy/runtime verification when applicable -> continuity sync -> exact main/test sync`.
Do not infer production deployment from merge alone.

---

## Current checkpoint — deliberate Item rollback baseline

Creator explicitly chose commit **`b59e632aa8e31647b85eeb244a4436c31e9e1e9d`** (`Fix Item nutrition basis semantics`, PR #369) as the acceptable Item Creation baseline after later realism tightening caused repeated rejection loops and slowed development.

Rollback PR **#372** restored the repository tree exactly to that checkpoint while preserving Git history. PR #372 merged to `main` as:

`6fe07ec4fde0375b29477c026e4ace991f8834ce`

The rollback intentionally removes later Item changes from:
- PR #370 — luminous-efficacy blocking validation;
- PR #371 — fixture-mobility reconciliation/tightening;
- interrupted post-#371 realism simplification work on `test`.

**Do not re-add or further tighten fine-grained Item realism validation unless the Creator explicitly authorizes it.** Development velocity now outranks chasing small realism imperfections in generated Item drafts.

The chosen `b59e632...` baseline still includes the earlier accepted Item schema/canonicalizer work, broad grading foundation, schema-validator compatibility audit, shared AI authoring guidance, metric coherence/evidence validation through PR #367, prompt refinement through PR #368, and nutrition-basis semantics through PR #369. Treat that exact behavior as intentional unless a concrete structural blocker appears.

---

## Item creation acceptance policy now

Creation-blocking validation should focus on **structural correctness and safe Sandbox materialization**, not exhaustive real-world realism.

Retain and respect hard contracts such as:
- schema/type validity;
- stable machine tokens/refs;
- valid batch-local references;
- stack/instance/module structural consistency;
- module/capability contracts already present in the chosen baseline;
- atomic whole-batch validation/materialization;
- Sandbox isolation and canonical Real World non-mutation.

Do **not** restart a whack-a-mole cycle for small plausible numeric imperfections. If a draft is structurally valid and reasonably usable, prefer forward progress. Fine-grained realism can be improved later as advisory quality work rather than continuously expanding the creation blocker.

Creator-side prompts should remain short and natural. Technical schema burden belongs in the system-side creation contract/canonicalizer, not in long user prompts.

---

## Item/grading foundation retained

I5.2–I5.10 remain complete and must not be rebuilt.

Key completed slices include:
- Universal Item Schema + Single/Batch materialization;
- Item/container relations and atomic operations;
- Universal Location Schema v1;
- Item Edit parity with pause-state restoration and stale guard;
- Character/Item cleanup controls;
- Item economics display and AI authoring normalization;
- Universal Grading Socket v1 (PR #360);
- broad Item Grading Coverage Foundation (PR #362);
- batch ref canonicalization and module/capability reconciliation;
- schema/canonicalizer/validator compatibility audit;
- shared single+batch Creator AI authoring contract;
- nutrition-basis semantics (PR #369).

Grading remains derived from authoritative raw facts. AI does not author final grades/thresholds. Item grade describes the Item; requirement grade describes the interaction. Overall Item grade remains absent without an explicit composite contract.

Locked Item ontology:
`Definition -> unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations remain distinct: `contains`, `located_at`, `stored_in`, `owned_by`, `carried_by`, `equipped_by`. Ownership is orthogonal to physical placement/storage.

---

## Immediate resume point

1. Verify production/runtime has deployed rollback merge `6fe07ec4fde0...` or later before claiming live rollback completion.
2. Generate **one** small Item Batch with a very short natural Creator prompt.
3. Judge primarily on structural usability, schema validity, sensible module/metric capture and successful preview/approval flow — **not microscopic realism optimization**.
4. If structurally acceptable, approve the batch and verify approved Item details.
5. Exercise one metric-bearing Item through Edit -> Preview -> Apply -> Done and confirm pre-edit pause restoration + canonical Real World isolation.
6. Then close the representative Item acceptance gate and proceed to **I5.11 — Sandbox Location Creation + Embedded Contents**.

Do not mass-regenerate old Items before this representative acceptance pass.

---

## Retained system locks

- Create anywhere safely; canon nowhere automatically.
- Sandbox-created content never transmigrates automatically.
- Target-universe compatibility validation must precede transmigration.
- `runtime_ready != running`; Created is not alive.
- `canonical_state_fingerprint()` remains a high-value zero-canonical-mutation invariant.
- Full autonomous Sandbox ticking remains unauthorized unless Creator explicitly expands scope.
- Adrian Vale remains Sandbox-only.
- Second Real World Character gate remains closed until later Mind + Relationship work.

---

## Exact resume sentence

**Creator deliberately rolled Item Creation back to the `b59e632aa8e3` behavior because later fine-grained realism tightening caused repeated rejection loops and blocked progress. Rollback PR #372 restored that exact tree and merged as `6fe07ec4fde0375b29477c026e4ace991f8834ce`. Do not re-tighten Item realism without explicit authorization. Verify that rollback commit (or later) is live, run one short natural-language representative Item Batch, accept it based mainly on structural/schema usability rather than microscopic realism, approve + verify one Item Edit/Apply/Done pass, then proceed to I5.11 Sandbox Location Creation + Embedded Contents.**
