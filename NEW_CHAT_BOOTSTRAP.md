# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-15

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical contracts/source files
5. current live production evidence before implementation decisions.

Current Creator instruction and newer repository/CI/deploy/live evidence override older chat memory.

## Development workflow

Default:
`branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

Use production-copy validation for concrete stateful/migration risk. Never accelerate/mutate production merely to manufacture acceptance evidence.

Any new architecture/control/security invariant updates its canonical contract + ROADMAP + bootstrap in the same development cycle.

## Current verified production checkpoint

Latest runtime deployment: **Deploy #183 `31826301329` SUCCESS**, PR #82 merge `45c29a834828c9afc1f0a7e190b9f5904019e546`.

Post-deploy Runtime Read #12 rerun verified:
- service active/healthy;
- schema v5;
- autonomy enabled/normal, paused false, retry null, speed 1.0x;
- sim `2025-05-05T11:17:00+00:00`;
- decision calls 386;
- current pending action `read` in the Living Room;
- Gemini `gemini-3.1-flash-lite` primary and Groq `qwen/qwen3.6-27b` fallback preserved;
- Weight 215.0 lb and BF 9.0% remain live `simulated` `physiology_engine` fields;
- BC-2 activation boundary remains `2025-05-05T07:55:00+00:00`, `bootstrapped`, `stat_mutated=false`, old/new identical;
- all eleven BC-3 circumference fields are present, including `body.hips_in=39.0`;
- BC-3 fields are still authored/static at readback and no `body_measurement_progression_settled` event exists yet, so BC-3 is deployed and seeded but **not yet live-activated**.

A historical provider 413 occurred on an 8,645-token cognition request. It is not current retry state; cognition enrichment stays compact.

## Universal invariants

Darian/Thorne Estate are production exemplars, never reusable-engine identity.

Inventory/eating:
`Universal food definition -> concrete stack -> reachable eating context -> structured quantity -> deterministic validation -> atomic stock transition + immutable evidence`

Cognition:
`deterministic state/context -> one model proposal -> authoritative validation -> deterministic mutation`

Body composition:
`complete bounded energy/nutrition evidence + current FM/FFM + resistance evidence + recovery + genetic envelope -> deterministic settlement -> coupled Weight/BF history + audit`

Body measurements:
`BC-2 body-composition settlement + regional resistance evidence + authored anatomy/genetic envelope -> bounded regional circumference settlement -> atomic profile history + event`

## Deployed food/nutrition checkpoint

- Inventory Foundation v1 — PR #71 / Deploy #177.
- Inventory Operations v1 — PR #73 / Deploy #178.
- Food Nutrition Semantics & Visibility v1 — PR #74 / Deploy #179.
- Eating Behavior v1 — PR #76 / Deploy #180.
- Meal Choice Intelligence v1 — PR #77 / Deploy #181.

Meal Choice Intelligence is a compact enrichment inside the existing single cognition call: same-day intake/macros/meal count, latest meal timing, recent training, recovery, REE reference and character nutrition policy. No broad Mind/Behavior Engine and no extra model call.

## BC-2 Body Composition Progression

**COMPLETE / DEPLOYED / LIVE-ACTIVATED** via PR #78 / Deploy #182; direct readback via PR #79 / Runtime Read #11 and preserved after Deploy #183.

Canonical:
- `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`
- `docs/NUTRITION_ENERGY_EVIDENCE.md`
- `docs/BODY_COMPOSITION_PROGRESSION_V1.md`

Live contract:
- activation preserves numerical Weight/BF exactly and establishes a non-retroactive settlement cursor;
- 24 simulated-hour evidence-complete windows;
- incomplete evidence creates an audited no-mutation deferred window;
- Forbes/Hall bounded partition, not fixed 3,500 kcal/lb;
- separate resistance-only lean adaptation constrained by protein, energy, recovery and genetic headroom;
- Weight/BF persist together; FM/FFM/BMI remain derived views;
- no schema migration or extra model call.

## BC-3 Body Measurement Progression Batch

**COMPLETE / DEPLOYED / SEEDED / ACTIVATION PENDING NATURAL BOUNDARY** via PR #82 / Deploy #183.

Canonical: `docs/BODY_MEASUREMENT_PROGRESSION_V1.md`.

BC-3 covers one batched family:
- neck;
- shoulders;
- chest;
- waist;
- hips;
- biceps relaxed/flexed;
- triceps;
- forearms;
- thighs;
- calves.

Contract:
- consumes BC-2 bounded body-composition settlements rather than creating a second composition authority;
- combines whole-body FM/FFM signals with data-driven regional resistance exposure;
- uses character-specific structural/genetic envelopes rather than scaling every circumference from body weight;
- allows small systemic FFM effects in unexposed regions while regional resistance adds a stronger local increment;
- activation preserves authored circumference values numerically and establishes a non-retroactive cursor;
- all changed measurements persist atomically with history and one causal settlement event;
- no schema migration or extra model call.

Darian's canonical body profile now includes `body.hips_in=39.0`; the reusable profile schema also includes `genetics.hips_max_in`, with Darian's authored envelope set to 41.0. These are character-specific canon, not universal ratios.

PR-head CI #698 passed the full test suite and CLI smoke checks. BC-3, BC-2, Strength and Stamina disposable production-copy acceptances all passed, including the candidate re-initialization upgrade path that adds newly authored fields without clobbering existing simulated engine-owned state.

Post-deploy Runtime Read #12 rerun confirmed all eleven circumference fields are present in production. Their mode remained `static` and latest BC-3 settlement was null at readback. Do not accelerate or directly mutate production merely to manufacture activation evidence; observe activation after the next natural eligible completion boundary.

## Public repository security checkpoint

`Ye-Shwethway/observer-sandbox` is **PUBLIC**.

Public Readiness Hardening v1 merged via PR #80 / `bf5e537cdeceaa6c5a8d4d61f21b67d636f01f20`. Public Hardening Fixup v1 followed via PR #81. Public Readiness Security Audit on PR #82 also passed after the BC-3 changes.

Canonical:
- `docs/PUBLIC_REPOSITORY_SECURITY.md`
- `SECURITY.md`

Security invariants:
- full reachable Git history is scanned with `fetch-depth: 0`;
- `.env`, `secrets.env`, SSH/private-key formats, runtime DBs and backups remain excluded from repository content;
- `pull_request_target` and `permissions: write-all` are prohibited;
- reusable VPS-backed production-copy validation retains a same-repository fork guard;
- GitHub withholds repository secrets from fork-originated `pull_request` workflows by default;
- disposable validators unset every model credential including Groq and all Telegram credentials;
- production credentials stay in GitHub Actions Secrets and VPS `/var/lib/observer-sandbox/secrets.env` mode `0600`;
- public security-audit runners use read-only contents/metadata permissions.

The GitHub App cannot read all repository Actions/security/ruleset settings. Manual UI verification remains for:
1. outside-contributor fork workflow approval policy;
2. Secret scanning / Push protection;
3. `main` branch/ruleset protection after the private-to-public transition.

## Later sequence

1. observe and verify BC-3 natural production activation;
2. verify remaining post-public GitHub security settings when convenient;
3. skill progression family;
4. intellectual attributes;
5. mental/emotion dynamics;
6. later social/relationship/sexual physiology;
7. broad Mind/Behavior architecture only after enough feature families exist to justify it.

## Exact resume point

First re-read live production. If a natural eligible action boundary has occurred since Runtime Read #12, verify **BC-3 activation** read-only. Do not force or accelerate production for evidence.

After BC-3 activation is naturally verified, the next development family is **skill progression** unless the Creator gives a newer instruction.

Do not add economy/currency, automatic restocking, deep recipes/crafting, Character Memory, broad Mind/Behavior engines, or a second production character merely for testing as side effects.
