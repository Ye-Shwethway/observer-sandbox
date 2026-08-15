# Actor-backed Skill Capability Assessment Adapter v1

Status: COMPLETE / DEPLOYED READ-ONLY FOUNDATION

## Purpose

Connect authoritative actor Skill/Profile state to the pure Skill Capability Resolver without entering mutation, action authorization, autonomy, or evidence-emission paths.

Implementation:
- `src/observer_sandbox/actor_skill_capability.py`
- `tests/test_actor_skill_capability_adapter_v1.py`
- `.github/workflows/actor-skill-capability-adapter-v1-acceptance.yml`

Upstream:
- `docs/SKILL_CAPABILITY_RESOLUTION_V1.md`
- `config/skill_definitions.v1.json`

## Invariant

`actor_id + skill_id + application_id + explicit challenge/context/resources -> authoritative actor Skill/Profile reads -> pure capability resolver -> read-only assessment`

## Read authority

The adapter reads:
- `character_skills.score` for the requested actor/Skill;
- only Attribute fields explicitly declared by the Skill Definition.

For Technology v1.1 those supporting Attribute reads are:
- `raps_ia.problem_solving`
- `raps_ma.focus`

Undeclared profile fields are ignored. Missing declared Attribute rows become transparent `None` inputs because current v1 Attribute semantics are non-gating. Malformed declared numeric fields fail clearly rather than being guessed or coerced.

If the actor has no authoritative `character_skills` row for the requested Skill, assessment fails closed; no score is fabricated from RAPS, prose, history, or parent Skills.

## Caller-owned task inputs

The adapter does not derive challenge/context/resource capability tokens from inventory, location, object names, model prose, or ambient state.

The caller/task contract must explicitly supply them. This keeps represented task truth separate from actor capability truth and prevents hidden inference.

## Read-only proof

Focused acceptance proves an assessment does not change:
- `events` row count;
- `character_profile_history` row count;
- Skill score;
- profile values.

No learning/application evidence is emitted merely because an assessment was requested.

Tests use a synthetic generic actor (`char_capability_fixture`), not Darian as implementation identity.

## Validation evidence

PR #117: `add actor-backed Skill capability adapter v1`

Final tested head:
`f7afac11bfe736da63fe6871b32b1f900b05bf3a`

Merge:
`07b43a20f28c75cccb150f01cd8f071a5a3a08d9`

PR gates:
- Actor Skill Capability Adapter v1 Acceptance #1 / run `31873122885`: SUCCESS
- CI #815 / run `31873122797`: SUCCESS
- Public Readiness Security Audit #71 / run `31873122839`: SUCCESS

Post-merge:
- Actor Skill Capability Adapter v1 Acceptance #2 / run `31873159937`: SUCCESS
- CI #816 / run `31873159939`: SUCCESS
- Deploy #202 / run `31873159944`: SUCCESS

Production readback after Deploy #202:
- exact deployed commit `07b43a20f28c75cccb150f01cd8f071a5a3a08d9`;
- service healthy/active;
- schema v5;
- autonomy normal at 1.0x;
- Telegram/cognition preserved;
- Technology remained `82.0 / A Advanced`;
- no service-loop/autonomy integration was added, so live behavior remained intentionally unchanged.

## Next design gate

Do not jump directly from this adapter to a generic Skill action engine.

Next audit one truthful represented Technology task surface for `diagnose_known_system_fault` and determine whether existing objects/actions already own enough explicit task facts to supply:
- application id;
- challenge class;
- required context tags;
- resource capability tokens;
- target/system identity;
- bounded outcome semantics.

If not, add the smallest generic represented-task contract first. Only after that should one bounded Technology application/action evidence integration be implemented.