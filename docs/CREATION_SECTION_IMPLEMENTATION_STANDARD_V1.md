# Observer Sandbox — Creation Section Implementation Standard v1

Status: **LOCKED IMPLEMENTATION STANDARD**  
Date: 2026-08-20

## Purpose

This document is the mandatory implementation playbook for every Creator-facing Creation section in Observer Sandbox.

It was distilled from the completed Character Creation and Item Creation verticals, including the problems found while making Manual/AI creation, validation, review, approval, editing, batch composition, diagnostics and Telegram presentation work reliably.

It exists to prevent future Location, Skill, Quest, System, Organization, Service, Event, world-element and other Creation sections from repeating the same integration mistakes.

Canonical rule:

> **Do not build a new Creation section as a bespoke CRUD feature. Plug the domain into the shared Creation pipeline through a versioned schema and registered socket.**

Mandatory first action for any future Creation work:

> **Read this document before planning, coding, reviewing, extending or debugging the Creation section.**

If this standard conflicts with a newer explicit Creator instruction or a newer canonical domain contract, the newer authority wins. Any deliberate deviation from locked common behavior must be documented; changes to isolation, approval authority, pause/resume, or safety semantics require explicit Creator approval.

---

# 1. Evidence behind this standard

The standard is grounded in the two first substantial Creation verticals.

## Character Creation taught

- a universal proposal envelope is not enough; the type needs an exact domain schema;
- AI must use the represented Character vocabulary rather than invent prose keys;
- schema/registry definitions should drive AI and presentation surfaces where practical;
- Manual and AI creation must converge on the same authoritative validator and Sandbox materialization boundary;
- detailed profile review must remain human-readable and navigable even when the schema is large;
- Creator approval is the authority boundary;
- Sandbox persistence must remain separate from canonical Character state;
- `runtime_ready != running`;
- editing needs a bounded session, preview-before-apply, stale protection, audit evidence and exact pause-state restoration;
- Telegram is a control/presentation adapter, not a second implementation of Character semantics.

## Item Creation taught

- Single and Batch must reuse the same exact Item schema; Batch is orchestration, not a second Item model;
- provider structured-output schema, deterministic canonicalizer and strict validator are distinct contracts and must be compatibility-tested together;
- a validator must accept its own normalized representation on re-entry;
- AI provider forms need complete schema slots but canonical source data may remain sparse;
- registries should generate provider enum/metric/module surfaces where possible so schema and validator do not drift;
- mechanically safe canonicalization is useful, but canonicalization must not invent missing semantic facts;
- batch-local references need stable aliases, complete graph validation and one atomic write boundary;
- technical schema burden belongs in the system-side AI contract, not in the Creator's natural-language prompt;
- one bounded repair/self-correction attempt can recover deterministic representation errors, but retry must not become the normal creation path;
- review UI and raw technical export serve different needs and both are valuable;
- Creator-facing error diagnostics must expose useful sanitized detail rather than only a generic failure;
- repeated one-error-at-a-time fixes are a warning to audit the entire schema/provider/canonicalizer/validator invariant family;
- excessively fine-grained realism checks can block forward progress even when the represented object is structurally usable. Fine realism is therefore non-blocking by default unless an explicit domain contract and Creator authorization make it authoritative.

The implementation standard below converts those lessons into a required order of work.

---

# 2. Golden Creation pipeline

Every substantial Creation domain should converge on this conceptual flow:

```text
canonical versioned domain schema
        ↓
registered Creation socket / reuse map
        ↓
Manual full-schema construction ──────┐
                                      ├─> canonical proposal shape
AI full-schema structured fill ───────┘
        ↓
deterministic canonicalization of safe representation differences
        ↓
strict structural/domain validation
        ↓
dependency / same-Sandbox / graph validation
        ↓
write-free human preview + technical export
        ↓
explicit Creator approval
        ↓
one atomic Sandbox-only materialization
        ↓
approved detail / browse / observer surfaces
        ↓
Edit lifecycle: preflight -> pause if needed -> preview -> apply -> restore prior pause state
        ↓
archive/delete/cleanup
```

Target-universe compatibility and transmigration are later, separate gates.

AI never owns the schema, validation authority, canonical write authority, grading authority or runtime activation authority.

---

# 3. Hard Gate A — schema first

## 3.1 Do not start AI/UI before the canonical schema exists

Before implementing a new Creation section, identify its authoritative versioned creation schema.

If the schema does not exist:

1. stop Creation UI/AI implementation;
2. define and review the schema first;
3. define its validator and normalization contract;
4. then build the Creation section on top of it.

A prompt, Telegram form, JSON example or generic `properties` bag must never become the accidental schema.

## 3.2 Minimum schema responsibilities

A domain schema should define, as applicable:

- schema id/version;
- stable identity/token rules;
- required versus optional/nullable fields;
- field types and semantic meanings;
- units and normalization rules;
- enum/registry sources;
- definition-owned versus instance/runtime-owned state;
- repeatable collections;
- conditional modules/extensions;
- capabilities;
- requirements/access conditions;
- relationships and target types;
- graph constraints such as acyclicity;
- economic/value representation when relevant;
- authoritative raw facts versus derived/read-time interpretation;
- lifecycle/runtime-readiness boundaries;
- Sandbox persistence ownership;
- canonical/transmigration boundaries.

## 3.3 Schema authority

The exact domain validator is authoritative for domain semantics.

The universal Creation envelope may validate proposal metadata and common lifecycle/provenance, but it must not replace the exact type validator.

The Character and Item implementations already prove this pattern:

`generic creation envelope -> exact type-specific validator -> normalized typed proposal`.

---

# 4. Hard Gate B — reuse map and Creation socket

Before writing a domain-specific service, identify what already exists and must be reused.

At minimum review:

- `docs/CREATION_CONTRACT_REUSE_MAP_V1.md`;
- `docs/UNIVERSAL_CREATION_SOCKET_FOUNDATION_V1.md`;
- `docs/CREATION_SANDBOX_ISOLATION_V1.md`;
- the domain's authoritative canonical/runtime contracts;
- existing shared quantity, grading, requirements, economic, relation and presentation helpers relevant to the domain.

Core architecture:

> **One proposal/apply pipeline, many registered creation sockets.**

A socket/domain adapter may own its field schema, validators, dependency resolver, Sandbox instantiator, runtime hooks and later transmigration adapter. It must not create a parallel general-purpose Creation framework.

## Expand through registries/sockets

New extensible concepts should normally be additive registrations rather than central switch rewrites.

Examples:

- profile fields from profile definitions;
- Item metrics from `ItemMetricRegistry`;
- grading evaluators/dimensions/reference profiles from grading registries;
- future Skill/System/Quest extension types from their own bounded registries.

Avoid family names, character names, Item names or fixed future-type lists in runtime branching when a registry/socket can express the same semantics.

---

# 5. Full Manual form and Manual/AI parity

## 5.1 Full schema construction surface

Every meaningful Creation section must provide a way to construct the complete supported creation-owned schema.

This may be a friendly multi-step editor, section browser, Exact JSON advanced path, or a combination, but the implementation must not leave important creation-owned schema fields permanently unreachable.

A full Manual surface is both a Creator feature and a diagnostic reference for AI parity.

## 5.2 Manual and AI converge

Manual and AI paths must converge before authoritative validation/materialization:

```text
Manual builder ─┐
                ├─> same domain payload -> same validator -> same materializer
AI fill ────────┘
```

There is no AI-specific database path and no looser AI validator.

AI-only hidden state is prohibited unless it is explicit provenance/diagnostic metadata outside domain authority.

## 5.3 Single and Batch converge

Where Batch is supported:

- every member uses the exact same member schema as Single creation;
- Single may be implemented as a batch of one where that simplifies semantic parity;
- Batch adds orchestration/local references/dependency closure only;
- Batch must never replace the member schema with a generic object bag.

---

# 6. Creator AI structured-fill contract

`docs/CREATOR_AI_SCHEMA_FILL_CONTRACT_V1.md` is mandatory.

## 6.1 The AI is a form filler, not a schema designer

The structured-output provider receives the actual complete supported provider-facing schema/form.

Do not compensate for a missing structured schema by writing an enormous user prompt describing field names.

Provider form rules:

- expose all canonical creation-owned fields/slots;
- use registered enums/module/metric surfaces where possible;
- use `[]` for unused arrays;
- use `null` for unknown or unused nullable scalar/object/module slots;
- derived/runtime-owned fields remain outside Creator seed authority;
- provider-required complete nullable module maps may be canonicalized to sparse source form before strict validation.

## 6.2 Natural Creator prompt

The Creator should be able to write a short natural request such as:

`Create five useful camping items.`

The system-side authoring contract carries the technical burden:

- schema semantics;
- unit/token conventions;
- relationship rules;
- module/capability dependencies;
- isolation boundary;
- evidence/null behavior;
- grading/derived-field restrictions;
- Batch local-reference syntax where applicable.

Do not require the Creator to paste schema instructions into normal prompts.

## 6.3 Strong shared system prompt

Common rules shared by Single and Batch should live in one reusable authoring contract rather than diverging prompt strings.

The prompt should instruct the model to:

- produce a validator-ready proposal on the first attempt;
- treat available schema slots as structure, not a checklist to fill with guesses;
- prefer fewer defensible facts over speculative completeness;
- use the schema's registered vocabulary;
- preserve known domain invariants;
- leave unsupported nullable values null;
- never author derived grades/evaluator authority when deterministic downstream grading owns them;
- never directly create canonical state.

## 6.4 AI binding, timeout and provenance

Use the Creator Creation AI binding/settings rather than a hidden hard-coded provider/model.

Track sufficient bounded provenance/diagnostics to identify provider/model/prompt generation context when useful.

Structured full-schema generation may need a different bounded timeout from ordinary autonomy calls. Do not blindly reuse a short autonomy timeout for large Creator forms.

A transport timeout should not automatically trigger an invisible provider retry when duplicate provider work/cost is possible; preserve the Creator's input/session for explicit retry.

---

# 7. Canonicalization boundary

Provider structured output and canonical domain source shape are allowed to differ only where strict provider schemas require transport placeholders or human-readable mechanical values need deterministic normalization.

Canonicalization may safely perform things such as:

- trim/case normalization;
- stable token normalization;
- known unit normalization;
- removal of schema-defined null/empty placeholders;
- deterministic local-ref alias normalization;
- alignment of two fields when both meanings are already unambiguously represented by the contract.

Canonicalization must **not**:

- invent missing factual quantities;
- choose a new semantic classification merely to pass validation;
- fabricate relations/owners/locations;
- create unsupported capabilities;
- silently convert subjective contradictions into new facts;
- weaken the domain validator.

Authoritative invariant:

`provider schema-shaped output -> deterministic canonicalization -> strict domain validator`.

## Mandatory compatibility proof

Tests must prove:

1. provider enum/slot surfaces match authoritative registries;
2. nullable provider placeholders canonicalize correctly;
3. valid AI form examples pass the strict validator after canonicalization;
4. normalized persisted/read-back state can be validated again;
5. invalid unsupported semantic facts still fail closed.

A validator rejecting its own normalized output is a contract bug and must be fixed before live acceptance.

---

# 8. Validation policy — block only what must block

## 8.1 Blocking by default

Creation may be blocked for authoritative structural/domain invariants such as:

- malformed schema/version;
- missing required fields;
- invalid types/enums/stable IDs;
- invalid units/ranges required by the schema;
- illegal module/capability combinations;
- invalid definition/instance/stack structure;
- malformed economic representation when that representation is required;
- invalid relationship target type;
- missing/inactive/cross-Sandbox references;
- mutually exclusive physical placement states;
- forbidden dependency cycles;
- incomplete dependency closure;
- authority/isolation violation;
- a write plan that cannot be atomic.

## 8.2 Non-blocking by default

Do **not** make creation fail merely because a generated object is imperfect in subjective or fine-grained realism dimensions.

Non-blocking by default includes:

- exact consumer-product performance realism;
- detailed performance-ratio plausibility;
- subjective quality/aesthetics;
- optimal price realism;
- optional inferred specifications not necessary for schema integrity.

AI prompting may encourage reasonable plausibility, and review may expose questionable facts, but such checks become hard validators only when:

1. the domain has an explicit authoritative contract for the fact;
2. the reliability value exceeds the implementation/retry cost;
3. the Creator explicitly authorizes the new blocking boundary when it materially tightens existing creation behavior.

This rule is intentionally derived from the Item Creation rollback to the `b59e632...` behavior baseline. Forward creation velocity must not be lost to endless realism micro-gates.

## 8.3 Repeated error rule

If a new live error appears in a contract family that has already failed multiple times, do not patch only the displayed field.

Audit together:

- provider schema;
- shared registries;
- system prompt;
- canonicalizer;
- strict validator;
- normalized persistence/read-back;
- Manual path;
- Single/Batch parity;
- relevant UI adapter.

Fix the invariant family once.

---

# 9. Bounded AI self-correction

A single deterministic repair attempt may be used when a structured AI proposal fails because the model supplied a repairable represented fact.

Rules:

- maximum one automatic regeneration/repair by default;
- provide the sanitized deterministic rejection reason to the repair prompt;
- rerun the exact same authoritative canonicalization/validation afterward;
- never relax the validator on the retry;
- never silently switch to Manual or another model/provider;
- if the second attempt fails, show a bounded actionable failure and preserve a clean session for explicit retry.

Self-correction is a recovery mechanism, not the expected normal path. A high retry rate means the provider schema/system prompt/canonicalizer needs improvement.

---

# 10. Reusable Creator Studio UX

New Creation sections should feel like the same Creator Studio, not unrelated mini-apps.

## 10.1 Entry pattern

Use the common navigation hierarchy where relevant:

`Observer Home -> Sandbox World -> Creator Studio -> Create -> <Domain>`

Offer only modes the domain actually supports, typically:

- AI creation from natural language;
- Manual/full-form creation;
- advanced Exact JSON when valuable for diagnostics/power use;
- Batch mode only when the domain has coherent batch semantics.

## 10.2 Telegram typing indicator — “shadow texting”

For AI generation that can take noticeable time:

- send Telegram `typing` chat action immediately;
- refresh it at an appropriate interval while the provider call remains active;
- stop naturally when the response/failure message is sent;
- do not show fake progress percentages;
- deterministic/manual paths should not incur unnecessary typing/provider behavior.

This is part of the reusable Creator AI UX, not a one-off Item feature.

## 10.3 Review must be human-facing

Normal Telegram review should:

- use display names instead of technical IDs where possible;
- resolve local refs to human names;
- translate internal enums to readable labels;
- hide null/unused fields;
- group fields into stable domain sections;
- use human units/money formatting;
- paginate large profiles/details rather than exceeding Telegram limits;
- retain review actions after rerender/navigation.

Telegram does not own schema semantics. It renders descriptors/query/service output.

## 10.4 Common actions

Where meaningful, use consistent actions and semantics:

- `Approve into Sandbox` / `Approve`;
- `Edit`;
- `Export .txt`;
- `Back`;
- `Cancel`;
- `Done Editing`;
- `Delete` / cleanup only on already-materialized objects.

`Back` means navigation. `Cancel` means abandon the current draft/session operation without applying it.

---

# 11. Raw `.txt` technical export

Complex Single drafts and especially Batch drafts should provide an auditable raw `.txt` export.

The pretty Telegram review and raw export intentionally serve different purposes.

## Telegram review

Human-readable, concise, names resolved, internal refs hidden when possible.

## Technical export

May preserve:

- exact structured payload;
- canonical/internal refs;
- local batch refs;
- detailed modules/relationships;
- revision/provenance useful for debugging.

Requirements:

- export is read-only and must not mutate the draft;
- use filesystem-safe, type-aware, human-identifiable filenames;
- include revision where the workflow has draft revision semantics;
- do not inject read-time derived grades or other second authorities into a raw source-of-truth export unless the domain contract explicitly defines them as source data.

Existing filename pattern examples:

- `creator-studio-character-<name>-rN.txt`;
- `creator-studio-item-<name>-rN.txt`;
- `creator-studio-item-batch-<first-name>-plus-<count>-rN.txt`.

Future domains should follow the same style.

---

# 12. Draft, Cancel and session semantics

Before explicit approval, Creation is proposal work.

Required behavior:

- preview/inspection does not materialize domain state;
- Cancel is available from meaningful pre-approval stages;
- Cancel abandons the draft/session cleanly;
- failed AI generation must not create partial Sandbox objects;
- provider failures should preserve enough input/session state for explicit retry where practical;
- stale callbacks/session IDs fail safely;
- a rerender or error must not silently destroy a valid earlier draft unless replacement was explicit.

No Creation flow should rely on “the user probably will not press the old button.” Use revision/session/stale guards where the operation can mutate state.

---

# 13. Preview and approval authority

## 13.1 Preview first

The full domain payload or dependency graph must be validated without domain writes before approval.

Preview should represent the same normalized facts that will be applied.

## 13.2 Explicit Creator approval

No AI completion, Manual form completion or preview completion is approval.

Materialization requires an explicit Creator action.

## 13.3 Revalidate at Apply

Do not trust a stale preview blindly.

Before materialization, use the saved proposal/revision/stale guard and rerun the authoritative checks needed to prove that the proposed state and dependencies are still legal.

---

# 14. Batch / graph creation

Batch-native domains must use dependency-closure semantics.

Required pattern:

`validate every member -> resolve local/existing refs -> validate whole graph -> preview -> allocate/write atomically`.

Requirements:

- stable batch-local refs;
- deterministic alias normalization if human-readable refs are accepted;
- forward refs may be supported when the graph can resolve them before writes;
- target types validated;
- active same-Sandbox existing targets only;
- structural cycles rejected where the relation requires acyclicity;
- all object IDs allocated before relationship writes when needed;
- one transaction/savepoint for the coherent batch;
- any failure means all-or-nothing rollback;
- one invalid member must not partially create the rest.

Batch is orchestration over exact member schemas, never a relaxed generic schema.

---

# 15. Sandbox isolation and materialization

All ordinary Creation approval initially materializes into Creation Sandbox state only.

Required invariant:

```text
canonical_state_before == canonical_state_after
```

Use `canonical_state_fingerprint()` in acceptance tests for meaningful Creation/materialization/delete paths.

Creation must not accidentally write canonical:

- entities/definitions;
- canonical relations;
- canonical profiles;
- canonical economy/net-worth;
- canonical runtime/autonomy state;
- world graph;
- other Real World authority tables.

Sandbox object IDs remain distinct from canonical IDs.

`Created != running` and `runtime_ready != running` remain hard locks.

Approval must not:

- start autonomy;
- make a Character alive/running;
- grant runtime affordances merely because a capability field exists;
- transmigrate the object;
- silently merge Sandbox facts into Real World.

---

# 16. Edit parity

A completed Creation vertical is not truly reusable if the Creator can create a rich object but cannot correct the same represented facts afterward.

## 16.1 Reuse creation schema

The Edit surface should reconstruct the authoritative domain payload and reuse the same validator instead of defining a second edit schema.

Where practical, recursive/schema-driven discovery should automatically expose new registered fields/modules so every extension does not require a new Telegram branch.

Only lock identity/runtime fields that are genuinely immutable by contract.

## 16.2 Edit lifecycle

Default flow:

```text
preflight current object/session
    ↓
record prior pause state
    ↓
pause relevant Sandbox/runtime if concurrent simulation could race the edit
    ↓
select field/section
    ↓
parse + validate proposed value
    ↓
Preview before/after
    ↓
Apply or Cancel Preview
    ↓
continue editing while still paused
    ↓
Done Editing
    ↓
restore exact prior pause state
```

Required:

- stale baseline/proposal guard;
- audit successful changes;
- raw authoritative fields change only on Apply;
- derived/read-time interpretation recomputes from raw state;
- entry/render failure after pause/session mutation must roll back the session/pause mutation.

---

# 17. Time pause / resume contract

Creation and Edit are different.

## Creation drafts

Draft generation/review should not arbitrarily pause the universe merely because the Creator is composing a new isolated object.

## Editing represented state

When editing an object whose current state can race autonomous simulation:

- preflight before mutating pause state;
- record whether the relevant universe/Sandbox was already paused;
- pause if it was running;
- keep it paused for the complete edit session, including previews and successive Apply operations;
- `Cancel Preview` does not end edit mode;
- `Done Editing`/session close restores the state that existed before entry;
- if it was already paused, leave it paused;
- never blindly resume after Save/Cancel/Done;
- applying one field does not auto-resume.

The UI should clearly state when Creator Edit Mode has paused simulation.

---

# 18. Error and diagnostic UX

Errors must be safe **and** useful.

Distinguish at least:

- provider/transport failure;
- structured-output/parsing failure;
- deterministic contract rejection;
- stale/session failure;
- dependency/reference failure;
- materialization/database failure;
- presentation/callback failure.

Creator-facing diagnostics may expose:

- exception class;
- sanitized bounded reason;
- provider status/reason where safe;
- bounded parser cause.

Never expose:

- credentials/tokens/API keys;
- authorization headers;
- unbounded provider bodies;
- raw tracebacks containing secrets.

Broad Telegram exception handlers must not erase the root cause without an owner diagnostic path.

Callback routing/composition is part of acceptance: a feature is not complete if its button is rendered but another extension intercepts the callback.

---

# 19. Delete, archive and cleanup

Materialized Sandbox objects need a bounded lifecycle.

Delete/cleanup should:

- verify selected objects are active and belong to the expected Sandbox/domain scope;
- validate the entire selected cleanup set before writes;
- understand dependent rows/relations/cascades;
- clean orphan shared definitions when domain policy permits and no remaining instance needs them;
- use one atomic transaction for a coherent multi-object cleanup;
- audit the mutation;
- preserve canonical fingerprint;
- never widen a Character/Item cleanup action into unrelated Location/system deletion merely because generic Sandbox rows share storage.

Archive and delete semantics should be explicit rather than interchangeable hidden state changes.

---

# 20. Runtime hooks and future transmigration

A Creation socket may describe optional runtime hooks, but Creation must not prebuild or invoke every runtime subsystem.

Examples:

- Character -> future autonomy/profile runtime registration;
- Location -> spatial graph registration;
- Skill -> progression registry integration;
- Quest -> quest engine registration;
- System/rule-module -> registered trusted engine adapter.

AI-created `system` or `rule-module` objects are descriptors/config proposals, not arbitrary executable code. Runtime implementation remains trusted registered project code.

Transmigration is a separate future process:

`Sandbox object -> dependency closure -> target universe compatibility validation -> explicit approval -> canonical adaptation`.

No ordinary Creation section should sneak in a direct canonical promotion path.

---

# 21. Mandatory automated acceptance matrix

Use the smallest task-relevant tests during iteration, but before release a new Creation vertical must cover the applicable entries below.

## Schema and contract

- canonical schema/version is known;
- required/nullable/type/enum rules;
- registry/provider schema parity;
- full Manual representative payload;
- full AI structured-fill representative payload;
- Manual/AI converge on same validator/materializer;
- provider form null/empty canonicalization;
- canonicalizer only performs safe mechanical normalization;
- normalized state revalidates successfully;
- unsupported semantic values still fail closed.

## AI

- short natural Creator prompt works;
- system prompt contains common authoring rules;
- provider binding/settings respected;
- timeout behavior appropriate;
- typing indicator used on slow AI path;
- structured generation failure is distinguishable;
- one bounded self-correction attempt if enabled;
- second failure stops cleanly rather than looping.

## Preview / UI / export

- preview performs zero domain materialization writes;
- human review hides internal noise and resolves names/refs;
- large detail paginates/renders safely;
- review actions survive rerender/navigation;
- raw `.txt` export contains auditable structured facts;
- export filename is domain/type-aware and safe;
- export itself makes no state change;
- Cancel makes no approved-domain write.

## Batch / graph

- exact member schema reused;
- duplicate/unknown/invalid refs fail;
- forward refs work if supported;
- relation target types validated;
- cycles fail where forbidden;
- one invalid member -> zero batch materialization;
- transaction failure -> full rollback;
- Single/Batch semantic parity proven where both exist.

## Approval / isolation

- explicit approval required;
- saved proposal is revalidated/stale-checked;
- materialization is atomic;
- correct Sandbox-owned tables/services receive state;
- canonical tables receive no new domain state;
- `canonical_state_fingerprint()` unchanged;
- no autonomous runtime activation;
- no automatic transmigration.

## Edit

- owner/Creator-only edit authorization where appropriate;
- entry preflight succeeds before pause mutation;
- running state pauses;
- already-paused state remains paused;
- field edit -> preview -> Apply works;
- raw value unchanged before Apply;
- stale preview fails safely;
- Apply reuses authoritative validator;
- edit session remains paused after one Apply;
- Cancel Preview makes no mutation;
- Done restores exact prior pause state;
- entry/render failure restores pause/session state;
- newly registered ordinary fields/modules are discoverable without bespoke branches where architecture promises schema-driven editing.

## Delete / lifecycle

- delete/archive scope correct;
- dependency handling correct;
- multi-delete atomicity where supported;
- audit exists;
- canonical fingerprint unchanged.

## Integration / release

- callback routing reaches the intended handler;
- CLI/init/status smoke where relevant;
- focused regressions green;
- PR CI/gates green;
- runtime-affecting merge deploys through standard workflow;
- deployment is verified separately from merge status;
- one representative Creator live pass succeeds before declaring live acceptance.

---

# 22. Definition of Done

A Creation section is complete only when its **vertical** is usable, not merely when a schema or database write exists.

Minimum Definition of Done:

1. this standard was reread before implementation;
2. canonical domain schema exists and is versioned;
3. reuse/socket mapping is explicit;
4. Manual/full-form path exists or an explicit justified equivalent is documented;
5. AI receives the full structured schema and a shared strong system prompt;
6. Manual/AI use the same validator/materializer;
7. schema -> canonicalizer -> validator compatibility is tested;
8. preview is write-free;
9. approval is explicit and Sandbox-only;
10. coherent batches apply atomically when Batch exists;
11. Creator gets human review and raw `.txt` export for complex drafts;
12. Cancel/error paths are safe and usable;
13. AI waits expose Telegram typing feedback;
14. approved object is browsable in the expected observer/detail surface;
15. rich created state has an Edit path with Preview/Apply and correct pause/resume semantics where runtime races matter;
16. delete/archive/cleanup scope is safe;
17. canonical isolation is proven;
18. focused tests and final PR CI pass;
19. runtime deploy/live state is verified separately when applicable;
20. continuity docs are updated and `main == test` is restored after merge.

---

# 23. Anti-patterns — do not repeat

The following designs caused or would cause repeat failures and are prohibited unless an explicit newer contract replaces the rule:

- building Telegram UI or AI prompts before the domain schema;
- treating generic `properties` as a substitute for exact type schema;
- Manual and AI using different authoritative payloads/validators;
- Batch inventing a looser member schema;
- provider schema enums/modules drifting from validator registries;
- expecting a long Creator prompt to compensate for missing structured schema;
- AI filling every nullable slot merely because it exists;
- canonicalizer repairing semantic meaning rather than mechanical representation;
- validator rejecting the representation produced by its own normalizer;
- retrying repeatedly instead of fixing first-attempt authoring/contract compatibility;
- patching one live validation error at a time when the entire invariant family is mismatched;
- making subjective/fine realism a hard creation gate without explicit value/authorization;
- partial batch writes before dependency closure validation;
- hiding technical IDs in Telegram but offering no raw audit export;
- pretty review only, with no inspectable source payload for complex drafts;
- rendering a button without testing callback composition/routing;
- pausing runtime before edit preflight and failing to roll back on entry/render failure;
- blindly resuming on Save/Done even when the universe was already paused;
- applying one edit and auto-resuming before the edit session ends;
- AI writing canonical state directly;
- Creation approval starting autonomy/runtime automatically;
- assuming a successful merge proves production deployment;
- creating a new CRUD framework for every future domain.

---

# 24. New Creation section kickoff checklist

Copy this checklist into planning/PR notes for every new domain.

## Before code

- [ ] Read `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`.
- [ ] Read `docs/CREATION_CONTRACT_REUSE_MAP_V1.md` and `docs/UNIVERSAL_CREATION_SOCKET_FOUNDATION_V1.md`.
- [ ] Identify the canonical domain schema and version.
- [ ] If no schema exists, build/approve it first and stop UI/AI work until then.
- [ ] Identify reusable quantity/grading/requirements/economy/relation/runtime contracts.
- [ ] Define the domain Creation socket/adapter boundary.
- [ ] Define Sandbox-owned persistence and canonical-isolation proof.
- [ ] Decide whether Batch is meaningful and what dependency graph it permits.
- [ ] Decide what is structural/blocking versus advisory/non-blocking.

## Authoring

- [ ] Complete Manual/full-schema construction surface planned.
- [ ] Complete provider-facing AI fill schema generated from canonical registries where possible.
- [ ] Shared system-side AI authoring contract written.
- [ ] Short natural Creator prompt sufficient.
- [ ] Safe canonicalization boundary documented.
- [ ] Schema/canonicalizer/validator compatibility matrix tested.

## UX

- [ ] Reuse Creator Studio navigation/actions.
- [ ] AI typing indicator implemented.
- [ ] Human review implemented.
- [ ] Raw `.txt` export implemented for complex drafts/batches.
- [ ] Cancel/Back semantics explicit.
- [ ] Safe actionable diagnostics implemented.
- [ ] Approved browse/detail surface implemented.

## Apply / Edit / lifecycle

- [ ] Write-free preview.
- [ ] Explicit approval.
- [ ] Atomic Sandbox materialization.
- [ ] `canonical_state_fingerprint()` unchanged.
- [ ] No runtime/autonomy start.
- [ ] Edit reuses creation schema/validator.
- [ ] Edit preflight before pause mutation.
- [ ] Preview -> Apply -> Done flow.
- [ ] Previous pause state restored exactly.
- [ ] Delete/archive/cleanup safe and auditable.

## Release

- [ ] Focused tests/regressions green.
- [ ] PR CI/gates green.
- [ ] Merge to `main` through normal workflow.
- [ ] Runtime-affecting deploy verified independently.
- [ ] One representative live Creator acceptance pass.
- [ ] `NEW_CHAT_BOOTSTRAP.md` / `ROADMAP.md` updated.
- [ ] `main == test` exact sync restored.

---

# 25. Immediate application — I5.11 Location Creation

The next planned Creation domain is **I5.11 — Sandbox Location Creation + Embedded Contents**.

It must begin by rereading this standard.

A Location schema already exists in `docs/UNIVERSAL_LOCATION_SCHEMA_V1.md`, so I5.11 does **not** need to invent another Location schema. It must map that schema into the shared Creation pipeline and reuse the exact Item Batch contract for embedded Items.

The expected high-level flow is:

`strict Location schema -> full Manual/AI Location fill -> exact validation -> embedded Item member schemas -> complete Location+Item graph preview -> one atomic Sandbox-only apply -> Location detail/Edit lifecycle`.

Existing Location semantics remain locked:

- same-Sandbox active parent validation;
- acyclic structural hierarchy;
- structural parent uses `contains`;
- dynamic movable presence uses `located_at`;
- `stored_in` is for storage/container semantics;
- interface destinations validate active same-Sandbox Locations;
- no arbitrary untyped `contents` bag;
- no automatic runtime readiness/running state;
- no canonical writes.

This standard is the implementation gate before that work begins.
