# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-15

## Startup / authority

Read and reconcile in order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical docs/source
5. verified production before runtime implementation decisions.

Authority:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

Default workflow:
`branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

Use **exemplar-first, then batch-by-pattern**. Never manipulate production merely to manufacture evidence.

## Current verified deployment

Latest runtime deployment: **Deploy #217 / run `31884052059` SUCCESS**, Represented Accident Casualty Producer v1, PR #144 merge `1068432c1933aa189f9ec4af5b7d33c86c54877d`.

Final tested PR head: `5c380474d4b92a091b9af09cf48e9954aaf4ac4b`.

Validation:
- **CI #876 / run `31884011651` SUCCESS**;
- **486 tests passed in 27.59s**;
- fresh DB `init` and `status` succeeded;
- schema remains v5.

Production readback after Deploy #217:
- service active/healthy; production init succeeded;
- autonomy enabled, normal mode, 1x, retry `null`, pending action present;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram connected with owner/allowed-user configuration present;
- sim time naturally advanced to `2025-05-06T09:50:00+00:00`;
- Darian was naturally `idle` in Darian's Master Suite;
- no live accident, fall, casualty state, lifecycle event, or synthetic casualty was created or forced for proof.

Exact represented-accident producer behavior is CI/ephemeral-fixture evidence. Production deployment proves the module loads safely; it is not evidence that a live accident occurred.

Production parent Skill values remain:
- H2H 90/S
- Weapons 87/A
- Survival 85/A
- Tactical Planning 92/S
- Technology 82/A
- Field Medicine 75/A.

## Recent completed chain

- Represented Skill Runtime Batch v1 — PR #133 / Deploy #211
- Controlled H2H Sparring Runtime v1 — PR #134 / Deploy #212
- Controlled H2H Interaction Pattern Generalization v1 — PR #136 / Deploy #213
- Represented Consequence State Foundation v1 — PR #138 / Deploy #214
- Field Medicine Stabilization Consequence Consumer v1 — PR #140 / Deploy #215
- Casualty State Origin & Lifecycle Contract v1 — PR #142 / Deploy #216
- **Represented Accident Casualty Producer v1 — PR #144 / Deploy #217.**

## Current casualty/consequence architecture

Generic represented consequence mutation remains:
`validated represented task -> deterministic consequence authorization -> bounded pre-existing simulated-state mutation -> causal event evidence`.

Casualty lifecycle owner:
`explicit source event + casualty role -> initialize only simulated medical.deterioration_risk -> causal lifecycle evidence`.

The lifecycle contract still owns state creation/clear. Risk zero never auto-clears and does not assert healing, diagnosis resolution, or definitive treatment.

Field Medicine stabilization remains a consumer of pre-existing casualty state only. It requires one distinct colocated casualty plus explicit represented `field_medical_supplies`, and only reduces `medical.deterioration_risk`. It does not diagnose, definitively treat, deplete supplies, or award XP.

## Represented Accident Casualty Producer v1

Implementation: `src/observer_sandbox/represented_accident_casualty.py`.
Design note: `docs/REPRESENTED_ACCIDENT_CASUALTY_PRODUCER_V1.md`.

Canonical path:

`typed represented accident -> represented_accident_occurred -> explicit casualty-role binding -> initialize_casualty_state(...) -> casualty_state_initialized`

V1 intentionally proves one accident invariant only:
- accident kind: `represented_fall`.

Finite abstract risk classes:
- `low -> 25`
- `moderate -> 50`
- `high -> 75`

These are abstract deterioration-risk initialization classes, not wound diagnoses or medical recommendations.

The producer requires:
- stable `incident_id`;
- existing represented character;
- existing spatial location;
- casualty currently located at that exact location;
- explicit simulation time;
- finite accident kind and risk class.

No free-form accident description is accepted.

The source event creates no injury, diagnosis, incapacity, treatment, or state mutation. It binds the character explicitly as role `casualty`, then the canonical lifecycle API creates `medical.deterioration_risk`.

Source-event emission and lifecycle initialization share one SQLite savepoint. Failure rolls both back. Repeating the same `incident_id` with identical semantics is idempotent; conflicting reuse fails closed.

## Hard boundaries

- controlled H2H remains scored-only and non-casualty-producing;
- Weapons remains a separate high-risk resource/target/safety/consequence review;
- no autonomous random accidents or probability tables;
- no universal Hazard/Injury Engine;
- no wounds/bleeding/diagnosis/death/incapacity;
- no automatic deterioration/recovery;
- no production accident/casualty fixture merely for proof;
- lifecycle/application/consequence evidence is not learning evidence.

## Next canonical direction

**Field Medicine Assessment Read-Only Runtime v1 — REVIEW NEXT / not yet implemented.**

The project now has a legitimate typed casualty origin plus lifecycle state. Reconcile the existing `field_medicine.assess_field_casualty` application and add the smallest represented assessment task/runtime that can observe an explicitly represented casualty's existing deterioration state without creating or mutating it.

Preserve:
- assessment must not manufacture casualty state;
- assessment output is informational/application evidence only unless a separately authorized consequence exists;
- no diagnosis engine or treatment graph;
- no automatic Field Medicine XP;
- no synthetic production casualty for proof;
- batch only structurally equivalent assessment follow-ons after one bounded exemplar is proven.

## Exact resume point

**Represented Accident Casualty Producer v1 is complete through PR #144 final tested head `5c380474d4b92a091b9af09cf48e9954aaf4ac4b`, merge `1068432c1933aa189f9ec4af5b7d33c86c54877d`, CI #876 / run `31884011651` with 486 passing tests plus fresh-DB init/status, and Deploy #217 / run `31884052059` SUCCESS. The first real casualty-state producer now proves typed `represented_fall` + stable incident identity + exact represented casualty/location + finite abstract risk class -> explicit `represented_accident_occurred` casualty-role event -> atomic canonical lifecycle initialization of only simulated `medical.deterioration_risk`, with no injury diagnosis, incapacity, XP, autonomous random accident, or fabricated production casualty. Review Field Medicine assessment as a read-only represented consumer next.**
