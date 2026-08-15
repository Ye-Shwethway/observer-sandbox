# Skill Application Requirements v1

Status: COMPLETE / DEPLOYED / RESOLVER NOT YET WIRED
Date: 2026-08-15

## Purpose

Close the executable edge between universal Skill Definitions and deterministic capability resolution.

Phase C audit found that Technology application `required_context` and `helpful_resources` were descriptive prose only. A deterministic resolver must not parse prose or hide equivalent constants in code.

This slice adds machine-readable application requirements while preserving prose fields for presentation.

## Canonical contract

For `technology.diagnose_known_system_fault`:

- required context tags, all required:
  - `technical_system_represented`
  - `diagnostic_evidence_available`
- required resource capabilities, at least one:
  - `diagnostic_interface`
  - `diagnostic_instrumentation`
- optional/supporting resource capability:
  - `technical_documentation`
- Knowledge mode:
  - `declarative_support_only`
- declared supporting Knowledge keys:
  - `technical_systems_fundamentals`
  - `diagnostic_procedures`
  - `technical_documentation_interpretation`

Knowledge remains a declarative support concept. No hidden Knowledge score, invented prerequisite number, or full Knowledge Engine is introduced.

## Validator

`src/observer_sandbox/skill_application_requirements.py` validates executable application requirements and exposes `get_executable_skill_application(...)`.

The validator rejects:
- missing executable requirements;
- prose instead of stable lower_snake semantic IDs;
- empty required resource capability alternatives;
- duplicate/overlapping required and supporting resource semantics;
- unknown Knowledge keys;
- unsupported hidden/numeric Knowledge modes;
- unknown applications.

The original Skill Definition Format validator remains independently active.

## Authority boundaries

This contract does not:
- mutate `character_skills.score` or `experience`;
- change actor action options;
- implement capability resolution;
- infer Knowledge state;
- introduce a competency score;
- reinterpret historical evidence.

Technology revision `technology-definition-v1.1` changes executable requirement metadata only.

## Validation / deployment evidence

PR #113 final head: `c811fb3a2795979e0a81f5b8213f3ebd62e977d4`.

PR gates:
- CI #807 / run `31872236989`: SUCCESS;
- Skill Application Requirements v1 Acceptance #1 / run `31872237030`: SUCCESS;
- Skill Definition Format v1 Acceptance #3 / run `31872236960`: SUCCESS;
- Strength Live Cycle #37 / run `31872236988`: SUCCESS;
- Public Readiness Security Audit #67 / run `31872236958`: SUCCESS.

Merged as `7cfe07dc32764d322942b21748a0d26ebb8a46f7`.

Deployment:
- Deploy #200 / run `31872355878`: SUCCESS;
- post-merge Skill Application Requirements Acceptance #2 / run `31872355880`: SUCCESS;
- post-merge Skill Definition Format Acceptance #4 / run `31872355871`: SUCCESS;
- post-merge CI #808 / run `31872355861`: SUCCESS.

Deploy readback verified service healthy, schema v5, autonomy normal 1.0x, cognition and Telegram intact, and Technology still `82.0 / A Advanced`. No live capability/action behavior changed.

## Next

Implement one bounded deterministic Technology capability assessment for `diagnose_known_system_fault` using this contract.

The first resolver should classify assessment from declared proficiency-anchor challenge support plus machine-readable context/resource requirements. Supporting Attributes should be reported/consumed only according to explicit definition semantics; do not introduce hidden weighting constants. Knowledge remains declarative support until a real Knowledge-state subsystem exists.
