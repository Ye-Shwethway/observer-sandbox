# Skill Creation Format v1

Status: COMPLETE / DEPLOYED AS READ-ONLY DEFINITION FOUNDATION
Date: 2026-08-15

## Purpose

Turn the researched Skill Definition & Capability Framework into a machine-readable, validator-backed creation format without yet changing live task capability resolution.

Canonical research/design:
- `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`

Canonical registry:
- `config/skill_definitions.v1.json`

Loader/validator:
- `src/observer_sandbox/skill_definitions.py`

## Authority boundary

This format defines universal Skill meaning only. It does **not** own actor progression state.

Actor authority remains:
- `character_skills.score` — current learned proficiency;
- `character_skills.experience` — accumulated legitimate learning evidence;
- persisted `tier` — compatibility only;
- grade — read-time `skill-proficiency-100-v1`.

A universal Skill Definition is rejected if actor-specific state such as score, experience, tier, grade, actor id or entity id is embedded inside it.

## Registry contract

The v1 registry provides:
- stable Skill identity, revision/status/category/type/reusability;
- affirmative definition plus included/excluded scope;
- hierarchy and typed related-Skill hooks;
- declarative Knowledge requirements;
- explicit Ability/Attribute dependencies;
- observable application/task families;
- skill-specific E/D/C/B/A/S behavioral capability anchors;
- shared task challenge vocabulary: routine / standard / challenging / advanced / extreme;
- whitelisted gameplay outcome dimensions;
- explicit failure/risk/consequence boundaries;
- legitimate learning-evidence families and method references;
- bounded transfer hooks;
- deferred retention/reacquisition metadata;
- grading/presentation metadata;
- provenance, compatibility and historical-evidence migration policy.

## Technology exemplar

Technology is the only Skill Definition in the first registry exemplar.

Canonical meaning:
> Learned capacity to understand, configure, diagnose, maintain, and troubleshoot designed technical systems by applying relevant knowledge, tools, documentation, and safe procedures.

Important scope exclusions include:
- ordinary consumer use;
- theoretical knowledge without practical application;
- unrepresented fabrication/manufacturing/crafting;
- weapon operation;
- medical diagnosis/treatment;
- offensive cybersecurity or unauthorized intrusion unless represented by a separate future Skill/Application;
- novel engineering/research-grade design without explicit knowledge/task/context support.

This prevents the broad umbrella name `Technology` from becoming permission for arbitrary technical behavior.

### Dependencies

The exemplar references underlying modifiers rather than duplicate Technology-like state:
- `raps_ia.problem_solving`;
- `raps_ma.focus`.

`raps_ia.technological_aptitude` is retained only as a legacy compatibility field in provenance and is **not** used as a second Technology proficiency dependency/authority.

Knowledge requirements are declarative hooks only; no hidden Knowledge scores or general Knowledge Engine were introduced.

### First application family

`diagnose_known_system_fault`

Intended outcome: inspect represented symptoms/logs/telemetry/diagnostic feedback and produce a justified fault assessment plus safe corrective or escalation path for a known technical-system family.

Allowed challenge classes: routine through advanced.

Allowed effect dimensions are explicit rather than universal:
- feasibility;
- quality/precision;
- time/speed;
- error probability/severity;
- information gained;
- partial-failure recovery.

High-risk live systems remain outside authorization by Skill score alone and require explicit task/context/resources/knowledge/safeguards.

### Behavioral proficiency anchors

The existing generic grade thresholds remain authoritative for presentation. The Technology definition adds domain-specific behavioral meaning underneath E/D/C/B/A/S.

The anchors progressively describe:
- supported task challenge;
- independence/supervision;
- diagnostic complexity;
- adaptation to uncertainty;
- known limits and high-risk boundaries.

S/Expert still does not authorize extreme novelty or high-consequence work by score alone. SS/SSS/X/XX are not available on the current 0..100 scheme.

## Learning-evidence cross-file contract

Technology declares `skill_practice` as an allowed learning-evidence family and references `systems_diagnostic_practice`.

The validator requires all of the following simultaneously:
1. the method exists in `skill_practice_methods.v1.json`;
2. its `skill_relevance.technology` is positive;
3. `skill_progression.v1.json` explicitly whitelists the method for Technology.

This preserves the existing dual-gate progression evidence semantics and prevents a definition file from granting XP merely by naming a method.

Generic `use`, `inspect`, `research`, `monitor`, object names, and model prose remain non-evidence by implication.

## Validator guarantees

The focused validator rejects at least:
- invalid/duplicate identities;
- missing definition/scope/category/type;
- actor state embedded in universal definitions;
- unknown profile/attribute dependencies;
- missing or malformed application meaning;
- unsupported challenge/effect/risk vocabulary;
- incomplete or SS+ proficiency anchors on the current scheme;
- decreasing challenge capability at higher proficiency anchors;
- unknown practice methods;
- practice methods without positive Skill relevance;
- methods not whitelisted by Skill Progression;
- high-risk applications with weak/missing consequence boundaries;
- hierarchy cycles;
- implicit generic-action learning evidence;
- transfer rules that fabricate Skill state;
- non-deferred retention/reacquisition behavior in this v1 foundation.

## Validation / deployment evidence

PR #111 final head: `ef05a2199e94d86f8b7cc4107317f7c38104d7da`.

PR gates:
- CI #803 / run `31871844052`: SUCCESS;
- Skill Definition Format v1 Acceptance #1 / run `31871844138`: SUCCESS;
- Strength Live Cycle Validation v1 #36 / run `31871844050`: SUCCESS;
- Public Readiness Security Audit #65 / run `31871844057`: SUCCESS.

Merged as:
- `a51c9f5980ba52883572397529d61889c856dbb6`.

Deployment:
- Deploy #199 / run `31871896715`: SUCCESS;
- post-merge Skill Definition Format v1 Acceptance #2: SUCCESS;
- post-merge CI #804: SUCCESS.

Deploy readback verified:
- service active/healthy;
- schema version 5 unchanged;
- autonomy enabled, normal mode, 1.0x;
- cognition bindings preserved;
- Telegram connected;
- Technology remained `82.0 / A Advanced`.

The registry was deployed as an application artifact but is not yet consumed by live task capability resolution. Therefore this slice intentionally caused no new actor capability, score, XP or action mutation.

## Next slice

**Technology Capability Resolution exemplar.**

Minimum next invariant:
`declared Technology application + actor Technology proficiency + declared supporting attributes + represented task challenge/context/resources -> deterministic capability assessment -> bounded outcome dimensions + immutable application evidence`

The next slice must remain bounded to one application family (`diagnose_known_system_fault`) and must not become a general Knowledge Engine, giant task engine, or scattered `skill >= N` checks.

After that exemplar is proven, remaining current Skill Definitions should be batched by the established format before their missing progression/evidence paths are expanded.
