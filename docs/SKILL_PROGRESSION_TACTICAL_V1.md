# Tactical Planning Skill Progression v1

Status: COMPLETE / DEPLOYED / LIVE-ACTIVATED

## Purpose

Apply the proven Skill Progression Foundation pattern to the next represented learned skill whose runtime already has explicit structured practice evidence: **Tactical Planning**.

This is a follow-on-by-pattern slice. It adds no new progression architecture.

## Authority

The Skill Progression Foundation authority contract is unchanged:

- `character_skills.score` = current demonstrated proficiency;
- `character_skills.experience` = accumulated legitimate post-activation learning/practice evidence;
- persisted `tier` = legacy/compatibility only;
- grade = read-time `skill-proficiency-100-v1` derivation;
- model prose, action reason text and Telegram are never progression authority.

Historical RAPS skill-like snapshots remain non-authoritative compatibility data and are not independently mutated.

## Evidence mapping

Tactical Planning consumes only completed Training Method evidence whose canonical method semantics explicitly include tactical work:

- `vr_tactical_drills` — relevance `1.00`, direct tactical practice;
- `ai_combat_simulation` — relevance `0.80`, mixed `combat + tactical` cross-training.

Combat methods without tactical semantics, such as `combat_mat_drills`, do not improve Tactical Planning merely because they are combat activities.

The `0.80` weight is bounded gameplay semantics for a mixed-purpose method, not a scientific learning coefficient.

## Progression calculation

The existing generic engine is reused unchanged:

`effective training minutes / 60 * method relevance -> raw learning units`

followed by:
- 24-sim-hour recent-practice saturation;
- current-proficiency diminishing returns;
- bounded score gain and cumulative experience;
- hard score cap `100`;
- immutable `skill_progression_settled` evidence;
- consumed-action-event idempotency.

## Activation safety

Initialization/deployment performs the same zero-gain activation bootstrap as Hand-to-Hand:
- represented score/experience are preserved;
- already-existing eligible history is cursor-consumed;
- historical XP/score are never invented;
- only genuinely future eligible practice may adapt the skill;
- ordinary re-initialization preserves earned state.

## Observability

Legitimate Tactical Planning score changes automatically reuse Character Change Observability & Notification Foundation v1:
- Profile delta arrows;
- `0.10` cumulative Skill significance;
- immediate grade-transition significance;
- generic Skills grading;
- per-character stat-notification controls;
- aggregated/debounced Character Progression pushes.

No Tactical-specific Telegram subsystem exists.

## Acceptance / deployment evidence

PR #106 final tested head: `404aab50803ab189b12845073f12f89d269f544f`.

PR validation:
- CI #793 / run `31870068073`: SUCCESS;
- Tactical Planning Acceptance #1 / run `31870068176`: SUCCESS on a disposable production copy;
- Hand-to-Hand Skill Progression Foundation Acceptance #4 / run `31870068174`: SUCCESS;
- Public Readiness Security Audit #60 / run `31870068116`: SUCCESS;
- Strength Live Cycle Validation #34 / run `31870068087`: SUCCESS.

Merged as `fc0fb067681f1b6481eab330a21cc902ed44b497`.

Deployment:
- Deploy #197 / run `31870118116`: SUCCESS;
- post-merge CI #794 / run `31870118123`: SUCCESS;
- post-merge Tactical Acceptance #2 / run `31870118233`: SUCCESS;
- post-merge Hand-to-Hand Foundation Acceptance #5 / run `31870118205`: SUCCESS.

Deploy readback verified service healthy, schema v5, autonomy normal at 1.0x, cognition bindings preserved, and Telegram connected. Live Tactical Planning remained at its represented `92.0 / S Expert` baseline after activation, proving deployment caused no retroactive score jump. Production was not moved, trained, accelerated or otherwise manipulated to manufacture a progression occurrence.

## Why the other represented skills remain deferred

The runtime still lacks sufficiently specific structured learning evidence for:
- **Weapons** — current Armory affordances are inspect/use, not weapon-practice semantics;
- **Survival** — current obstacle training represents conditioning/movement, not fieldcraft evidence;
- **Technology** — terminal/workstation use and generic Research Desk activity do not encode a technical topic or work product;
- **Field Medicine** — Diagnostic Station use does not encode medical practice/treatment evidence.

The generic `research` action has no topic/domain semantics and was explicitly introduced without skill XP/progression. Never guess these skills upward from action names or model reason prose.

## Next architectural requirement

Before enabling the remaining represented skills, introduce a **bounded structured Skill Evidence Semantics** family that can represent legitimate practice/task evidence without inventing knowledge from generic actions. Use one safe exemplar, then batch structurally equivalent mappings.

Skill retention/decay/reacquisition remains deferred until acquisition evidence coverage is broader.
