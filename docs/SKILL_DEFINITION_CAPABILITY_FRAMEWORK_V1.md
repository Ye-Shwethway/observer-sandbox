# Skill Definition & Capability Framework v1

Status: RESEARCHED CANONICAL DESIGN / IMPLEMENTATION PENDING
Date: 2026-08-15

## Purpose

Give every current and future learned Skill an explicit reusable meaning before more progression mappings are added.

The existing runtime can store, grade and progress `character_skills.score`, but a score alone does not define what the Skill covers, what tasks it supports, what knowledge/abilities it depends on, what level of task the actor can attempt reliably, what failures mean, or what evidence legitimately improves it.

This framework separates those concerns so future combat, medicine, survival, technology, crafting, investigation, social, career and quest systems can consume one canonical capability contract instead of inventing ad-hoc `skill >= N` rules.

## Research basis

The design is adapted for a simulation runtime from several established competency/skill frameworks rather than copying any one framework literally.

### O*NET Content Model

O*NET separates worker **Abilities**, **Skills**, and **Knowledge** from job-side **Work Activities**, **Work Context**, and occupation-specific **Tasks**. Abilities are underlying capacities that affect acquisition/application and performance rather than learned Skills themselves.

Source: https://www.onetcenter.org/content.html

Observer Sandbox consequence:
- RAPS/physical/cognitive capacities are not silently converted into Skills;
- Skills may depend on abilities/attributes without becoming the same state;
- tasks/application contexts remain separate from the actor's learned proficiency.

### NIST NICE Framework

The NICE Framework uses Task, Knowledge and Skill (TKS) statements as modular building blocks. A Task describes work to be done; Knowledge describes concepts that must be known; Skill describes observable capacity to act. Related Knowledge and Skill statements can be clustered into Competency Areas.

Sources:
- https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/getting-started
- https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/playbook-workforce-frameworks

Observer Sandbox consequence:
- task definitions should state required/relevant Skills and Knowledge explicitly;
- Skill definitions should describe observable capability rather than occupation/job identity;
- modular statements/relations are preferred over giant domain-specific engines.

### ESCO

ESCO distinguishes knowledge concepts from skill/competence concepts and gives concepts structured metadata such as preferred/non-preferred terms, description, formal definition, scope note, reusability and relationships. Its scope notes explicitly disambiguate what is included and excluded.

Sources:
- https://esco.ec.europa.eu/en/classification/skill
- https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/scope-note
- https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skill-reusability-level

Observer Sandbox consequence:
- every Skill needs explicit inclusion/exclusion boundaries;
- aliases/display names must remain distinct from stable technical identity;
- hierarchical and related-skill relations should be first-class, not inferred from names.

### SFIA

SFIA distinguishes Knowledge, Skill and Competency by application, context, responsibility/accountability and consistency of outcome. In SFIA's practical distinction, Knowledge can exist without performance; Skill is the ability to apply knowledge to perform tasks; Competency adds reliable performance in real contexts with meaningful responsibility for outcomes. SFIA levels are also designed to be progressive, distinct and behaviorally recognisable.

Sources:
- https://sfia-online.org/en/about-sfia/about-sfia-appendices/knowledge-skill-and-competency
- https://sfia-online.org/en/about-sfia/how-sfia-works

Observer Sandbox consequence:
- controlled/simulation practice can demonstrate Skill without proving real-context reliability;
- successful live application history can later contribute competency/reliability evidence;
- proficiency bands need skill-specific behavioral anchors rather than grade labels alone.

## Canonical ontology

### Ability / Attribute

An underlying physical, cognitive, perceptual, emotional or other capacity that influences learning or performance.

Examples: strength, reflexes, manual dexterity, attention, reasoning capacity.

Authority remains the relevant Attribute/physiology engine. Abilities are **not** learned Skill proficiency.

### Knowledge

Facts, concepts, principles, procedures or information an actor knows or can retrieve.

Knowledge can support a Skill but does not prove that the actor can perform the task. Full general Knowledge-state mechanics are deferred; Skill definitions may declare knowledge dependencies/hooks now.

### Skill

A learned capacity to apply relevant knowledge and abilities to perform a defined family of observable tasks/actions.

`character_skills.score` remains the authoritative current learned Skill proficiency state.

### Task / Application

A defined thing the actor attempts to accomplish. A task has its own difficulty/challenge, context, requirements, resources/tools, risk and intended outcome.

Tasks are not stored as Skill state. Actions/tasks reference Skill definitions.

### Competency / Demonstrated Capability

Evidence that an actor can apply relevant knowledge and Skill reliably in meaningful contextual or operational conditions, including consequences and responsibility for results.

v1 does **not** introduce a second competing numeric competency score. Reliability/competency is an evidence concept and future resolver input, not a replacement for `character_skills.score`.

### Learning Evidence

Immutable evidence showing legitimate practice, study-linked application, supervised work, simulation or real task performance that may contribute to Skill progression under an explicit policy.

Current Training Method evidence and `skill_practice` evidence remain valid evidence families.

### Proficiency

The actor's learned Skill level represented by `character_skills.score` and interpreted through `skill-proficiency-100-v1` for generic presentation.

A generic grade does not determine exact gameplay capability by itself. Each Skill definition provides capability anchors describing what proficiency bands mean for that Skill.

## Authority separation

### Static Skill Definition

Universal, versioned definition shared by all actors. It owns meaning and capability semantics, not actor progress.

### Character Skill State

Actor-specific state:
- `score` — authoritative current proficiency;
- `experience` — accumulated legitimate learning evidence under the current progression system;
- legacy `tier` — compatibility only;
- actor-specific history/evidence — separate immutable records/events.

### Task / Action Definition

Defines the actual attempted work and references relevant Skill/Knowledge/Ability requirements.

### Resolver

Future deterministic capability resolution consumes definitions + actor state + current context. Telegram/model prose never becomes authority.

## Skill Creation Format v1

A valid first-class Skill Definition must support the following sections. Optional sections may be empty only where the concept genuinely does not apply.

### 1. Identity

Required:
- `skill_id` — stable technical identity; lowercase snake_case;
- `name` — canonical display name;
- `revision` — semantic revision identifier;
- `status` — active/deprecated/experimental;
- `category` — broad organizational category, not capability authority;
- `skill_type` — e.g. motor, technical, cognitive, medical, fieldcraft, social, mixed;
- `reusability` — broad/transversal, cross-domain, domain-specific, narrow/specialized.

Optional:
- aliases/non-preferred terms;
- external mappings/provenance.

### 2. Definition and scope

Required:
- `definition` — concise affirmative meaning;
- `scope_includes` — explicit included task families/components;
- `scope_excludes` — explicit boundaries and nearby concepts that must not be inferred.

A definition fails validation if its meaning is merely circular (`Technology is technology skill`) or if a broad ambiguous Skill has no meaningful scope boundaries.

### 3. Hierarchy and relations

Supports:
- optional `parent_skill`;
- optional `component_skills`;
- `related_skills` with typed relations such as complementary, prerequisite, overlaps, transfer_source, transfer_target.

An umbrella Skill may exist before its component Skills are individually represented in character state. Splitting an umbrella Skill later must never fabricate child scores silently.

### 4. Knowledge dependencies

Supports named knowledge requirements/references with:
- topic/knowledge key;
- importance/relevance;
- minimum requirement where one is genuinely necessary;
- whether absence blocks the task or only penalizes performance.

Until a general Knowledge engine exists, these are declarative hooks and task-definition requirements rather than invented hidden Knowledge scores.

### 5. Ability / Attribute dependencies

Typed references to existing underlying capacities, each with:
- field/ability key;
- relevance/weight metadata;
- relationship such as prerequisite, performance_modifier, learning_modifier;
- optional threshold only when semantically justified.

Attributes influence Skill use/learning but never directly replace the Skill score.

### 6. Task / application families

Every Skill must name observable applications it can support. Each application family defines:
- stable `application_id`;
- description/outcome intent;
- task tags/domain;
- default challenge class/range;
- relevant required tools/resources/context;
- whether the Skill is primary or supporting;
- risk class and possible consequence family;
- explicit exclusions where confusion is likely.

This is the bridge between `Skill score` and gameplay.

### 7. Proficiency capability anchors

For the current 0..100 learned-Skill scale, every Skill must define behaviorally distinct anchors compatible with the existing grade thresholds:
- E: 0–19.999
- D: 20–39.999
- C: 40–59.999
- B: 60–74.999
- A: 75–89.999
- S: 90–100

The anchor is **skill-specific capability semantics**, not a duplicate grade label.

Each anchor should describe, where relevant:
- supported task complexity/challenge;
- degree of independence/supervision;
- expected consistency/quality under ordinary conditions;
- adaptation to unfamiliar cases;
- permitted risk/context boundaries;
- known limits.

SS/SSS/X/XX remain unavailable on the current 0..100 scheme and must not be invented through these anchors.

### 8. Difficulty / challenge model

Skill definitions declare the challenge vocabulary they use. v1 canonical generic classes are:
- `routine`
- `standard`
- `challenging`
- `advanced`
- `extreme`

These are task-difficulty classes, not grades. A later resolver may map exact task requirements and contextual modifiers onto them.

Definitions may narrow or annotate these classes but must not create arbitrary hidden numeric checks in downstream code.

### 9. Gameplay effects

A Skill definition states which result dimensions it is allowed to influence, such as:
- success/feasibility;
- quality/precision;
- time/speed;
- resource efficiency;
- error probability/severity;
- information gained;
- stealth/detection exposure;
- recovery from partial failure;
- available action variants/options.

A Skill does not automatically modify every dimension. Effects are whitelisted per definition/application family.

### 10. Failure, risk and consequence semantics

Where relevant, define:
- whether failure/partial success is possible;
- consequence family;
- risk severity bounds;
- whether high-risk contexts require stronger proficiency, tools, knowledge, supervision or demonstrated reliability;
- safeguards against treating practice/simulation evidence as proof of high-risk live competence.

This section is especially important for medical, combat, hazardous technical and other consequential Skills.

### 11. Acquisition / learning evidence policy

A definition declares allowed evidence families, for example:
- structured Training Method evidence;
- purpose-built `skill_practice` simulation/practice evidence;
- future topic-aware study/knowledge evidence where appropriate;
- supervised application;
- live application/task outcomes.

The definition may reference progression method IDs, but the existing Skill Progression engine remains the score/XP mutation authority.

Generic `use`, `inspect`, `research`, model reason prose or object names never become learning evidence implicitly.

### 12. Transfer / cross-training hooks

Explicit typed transfer rules may describe legitimate cross-training between Skills.

Rules must be authored and bounded; lexical similarity or shared category does not create transfer automatically.

No transfer rule may silently create a previously unrepresented child Skill score.

### 13. Retention / reacquisition hooks

Definitions may declare future retention semantics such as:
- motor-heavy / knowledge-heavy / mixed;
- decay eligibility;
- refresher/reacquisition support;
- minimum evidence required before decay can be modeled.

Actual Skill Retention/Decay remains deferred until the broader definition/evidence foundation is proven.

### 14. Grading / observability / presentation

Required:
- grading scheme reference (`skill-proficiency-100-v1` for current Skills);
- friendly label/short description;
- presentation category/order metadata;
- sensitivity classification if needed.

Grades remain read-time derived; definition metadata must not persist a competing grade.

### 15. Provenance and compatibility

Required:
- canonical revision/source;
- authored rationale/research notes where needed;
- compatibility aliases or legacy field mappings;
- explicit migration notes for semantic changes.

Historical evidence is never silently reinterpreted after a definition revision. A semantic revision that changes evidence meaning must declare a migration/reconciliation policy.

## Minimum machine-readable shape

Phase B should introduce one registry (provisional name `config/skill_definitions.v1.json`) containing universal definitions. Character seeds reference only `skill_id` plus actor state; they do not duplicate the Skill's meaning.

Conceptual shape:

```json
{
  "revision": "skill-definitions-v1",
  "skills": {
    "technology": {
      "name": "Technology",
      "category": "technical",
      "skill_type": "technical",
      "definition": "...",
      "scope_includes": ["..."],
      "scope_excludes": ["..."],
      "relations": {},
      "knowledge_requirements": [],
      "ability_dependencies": [],
      "applications": [],
      "proficiency_anchors": {},
      "challenge_model": "generic-five-class-v1",
      "gameplay_effects": [],
      "risk": {},
      "learning_evidence": {},
      "transfer": [],
      "retention": {},
      "grading_scheme": "skill-proficiency-100-v1",
      "provenance": {}
    }
  }
}
```

The exact schema belongs to Phase B and must be validator-backed rather than relying on comments/free-form convention.

## Capability resolution direction

Future deterministic resolution should conceptually be:

`Task definition + Skill Definition + actor Skill state + required Knowledge + relevant Abilities/Attributes + tools/resources + environment/context + reliability evidence -> eligibility/challenge resolution -> deterministic outcome dimensions + immutable application evidence`

Important boundaries:
- a Skill score is one input, not the entire outcome;
- low underlying ability may constrain a physically/cognitively dependent task without erasing learned Skill;
- high underlying ability does not fabricate training/Skill proficiency;
- controlled practice evidence proves practice capability, not automatically high-risk operational reliability;
- the LLM may propose an action and explain intent but never invent capability authorization.

## Umbrella Skills and future expansion

The six current Skills are broad umbrella concepts. v1 should preserve them rather than exploding the profile into dozens of fabricated child scores.

Current review set:
- Hand-to-Hand Combat
- Weapons
- Survival
- Tactical Planning
- Technology
- Field Medicine

The format supports future component Skills. Example conceptual decomposition only:
- Technology -> systems diagnostics, communications systems, computing, electronics;
- Survival -> navigation, shelter/fieldcraft, tracking, environmental resource management;
- Weapons -> categories may later split only when gameplay actually requires distinct evidence/capability;
- Field Medicine -> assessment/stabilization and other components may split only when medically justified and represented safely.

A child becomes first-class actor state only through an explicit migration/creation rule with legitimate evidence or authored baseline. Parent scores are never copied into children automatically.

## Relationship to existing systems

### Skill Progression Foundation

Remains valid. `character_skills.score` and `experience` authority does not change.

### Skill Evidence Semantics

Remains valid. Existing typed practice evidence becomes one allowed learning-evidence family referenced by definitions.

### Universal Profile Grading

Remains valid. It supplies generic E–S interpretation; definitions add behavioral capability meaning underneath those bands.

### Character Change Observability

Remains valid. It observes authoritative score changes, not definition metadata.

### RAPS skill-like legacy fields

Remain non-authoritative compatibility/profile fields. The new definition registry must not make them a second Skill state.

## Validation rules for Phase B

The machine-readable Skill Creation Format validator should fail if:
- `skill_id` is unstable/invalid or duplicate;
- definition/name/category/type is missing;
- broad definition has empty scope boundaries;
- relations reference unknown Skills without an explicit deferred/external marker;
- proficiency anchors are missing, overlap incorrectly or contradict current score bands;
- an application has no observable outcome meaning;
- a high-risk application omits risk/consequence boundaries;
- learning evidence references unknown method families;
- generic action names/prose are treated as implicit evidence;
- unsupported grade bands SS+ are attached to the current 0..100 scheme;
- a definition attempts to persist actor score/XP/grade;
- cyclic parent/component hierarchy is created;
- transfer rules imply automatic score fabrication.

## Phased implementation plan

### Phase A — research + ontology/design

This document. No runtime/schema mutation.

### Phase B — Skill Creation Format v1 + validator

Add a machine-readable registry/schema/validator and one complete **Technology** definition. Keep it read-only with respect to runtime gameplay until validation passes.

Technology is the preferred exemplar because its typed practice evidence path already exists, minimizing new variables.

### Phase C — Technology capability exemplar

Wire one bounded Technology application/task family into deterministic capability resolution using the definition registry. Reuse the existing Technology score and practice evidence; do not invent new XP or actor state.

### Phase D — current-skill definition batch

Once the definition/resolution pattern is proven, batch the remaining current Skills by pattern. Do not split broad umbrella Skills prematurely.

### Phase E — resume missing evidence/progression coverage

Only after semantic definitions exist, add missing Field Medicine/Survival/Weapons learning evidence using their actual scope and risk contracts.

## Explicit non-goals for v1

Do not build as side effects:
- a full general Knowledge Engine;
- a second competency score system;
- careers/jobs/quests/economy;
- giant skill trees;
- dozens of speculative subskills;
- arbitrary `skill >= N` checks scattered through gameplay;
- LLM-authoritative capability or progression;
- Skill Retention/Decay before definition/evidence coverage is broad enough;
- retroactive reinterpretation of historical evidence.

## Acceptance criterion for the foundation

The foundation is ready for implementation when a new Skill can be created from the format and a reviewer can answer, without reading custom engine code:
1. what the Skill means;
2. what it explicitly includes/excludes;
3. what knowledge/abilities support it;
4. what observable tasks it applies to;
5. what each current proficiency band behaviorally permits/limits;
6. what task difficulty/risk means;
7. which outcome dimensions the Skill may affect;
8. what counts as legitimate learning evidence;
9. how it relates/transfers to other Skills;
10. how future retention/migration/presentation are expected to work.
