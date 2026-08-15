# Skill Capability Resolution v1

Status: COMPLETE / DEPLOYED PURE RESOLUTION FOUNDATION

## Purpose

Skill Capability Resolution v1 turns a validated universal Skill Definition plus explicit task inputs into a bounded deterministic capability assessment without inventing hidden scores, probability, authorization, or learning effects.

First exemplar:
`technology.diagnose_known_system_fault`.

Implementation:
- `src/observer_sandbox/skill_capability.py`
- `tests/test_skill_capability_resolution_v1.py`
- `.github/workflows/technology-capability-resolution-v1-acceptance.yml`

Upstream contracts:
- `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`
- `docs/SKILL_CREATION_FORMAT_V1.md`
- `docs/SKILL_APPLICATION_REQUIREMENTS_V1.md`
- `config/skill_definitions.v1.json`

## Core invariant

`Skill Definition + actor proficiency + current proficiency anchor + requested challenge + machine-readable context/resources + declared supporting inputs -> deterministic capability assessment`

The result is an assessment, not permission to execute an action.

## Status semantics

### supported

Returned only when:
- the application declares the requested challenge class;
- the actor's current proficiency anchor supports the requested challenge;
- every required context tag is present;
- at least one required-any resource capability is present; and
- every declared supporting resource capability is present.

### constrained

Returned when all mandatory gates pass but one or more supporting resource capabilities are absent.

This is deliberately distinct from unsupported: the task family is within current declared capability, but available support is incomplete.

### unsupported

Returned when any mandatory capability condition fails, including:
- application does not declare the requested challenge;
- current proficiency anchor does not support the requested challenge;
- required context is missing;
- required-any resource capability is missing.

## Proficiency authority

The resolver consumes `character_skills.score` semantics through the canonical read-time `skill-proficiency-100-v1` grading contract.

It does not use scattered numeric thresholds such as `technology >= 75`.

Challenge eligibility comes from the Skill Definition's grade-specific behavioral anchor. For Technology v1.1:
- E/D: routine;
- C: routine + standard;
- B: routine + standard + challenging;
- A/S: routine + standard + challenging + advanced.

The application itself also has an explicit challenge envelope. `diagnose_known_system_fault` does not declare `extreme`, so even an S actor does not gain extreme authorization or support by score alone.

## Knowledge boundary

Technology Knowledge requirements currently use:
`declarative_support_only`.

The resolver exposes those supporting Knowledge keys and records `knowledge_assessed = false`.

There is no hidden Knowledge score, no inferred Knowledge gate, and no substitute Knowledge Engine.

## Ability / Attribute boundary

Technology declares:
- `raps_ia.problem_solving`
- `raps_ma.focus`

v1 reports available values as transparent inputs only. They do not modify status, challenge eligibility, success probability, or quality.

This is intentional. The definition currently declares these fields as relevant dependencies but does not yet define an executable modifier function. A future modifier model must first become explicit, validator-backed definition semantics rather than appearing as hidden resolver constants.

Legacy `raps_ia.technological_aptitude` remains compatibility provenance only and is not a second Technology proficiency authority.

## Non-goals / safety boundaries

v1 does not:
- authorize actions;
- create or mutate actions;
- create random success/failure rolls;
- mutate Skill score or XP;
- create a second competency score;
- infer real-world reliability from practice evidence;
- create a Knowledge Engine;
- let an LLM decide deterministic capability;
- authorize high-risk live technical work from Skill score alone.

## Validation evidence

PR #115: `add deterministic Technology capability resolution v1`

Final tested head:
`d5ab4cf867a5dd47ea5f4ba22b41cff412dbbe79`

Merge:
`2609d4bde93d0a188db4ff398a90792b1cec759d`

PR gates:
- Technology Capability Resolution v1 Acceptance #1 / run `31872730382`: SUCCESS
- CI #811 / run `31872730342`: SUCCESS
- Public Readiness Security Audit #69 / run `31872730326`: SUCCESS

Post-merge:
- Technology Capability Resolution v1 Acceptance #2 / run `31872775640`: SUCCESS
- CI #812 / run `31872775683`: SUCCESS
- Deploy #201 / run `31872775593`: SUCCESS

Production readback after Deploy #201 verified:
- deployed commit `2609d4bde93d0a188db4ff398a90792b1cec759d`;
- service healthy/active;
- schema v5;
- autonomy normal at 1.0x;
- Telegram connected;
- cognition bindings preserved;
- Technology remained `82.0 / A Advanced`;
- no live capability/action behavior or actor progression was forced or changed merely to prove the resolver.

## Next minimum-runnable slice

**Actor-backed Skill Capability Assessment Adapter v1**.

Minimum invariant:
`actor_id + skill_id + application_id + explicit challenge/context/resources -> read authoritative actor Skill/Profile inputs -> pure Skill Capability Resolver -> read-only assessment`

Constraints:
- read `character_skills.score` as proficiency authority;
- read only definition-declared Attribute inputs;
- no mutation and no action authorization;
- no target/system facts invented by the adapter;
- caller must supply represented task context/resource capabilities explicitly until a real task/target contract owns them;
- no learning evidence emitted merely for assessment;
- no autonomous technical action added in this slice.

Only after this adapter is proven should one represented Technology application/action evidence integration be considered.