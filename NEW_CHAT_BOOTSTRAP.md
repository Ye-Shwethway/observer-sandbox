# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-14

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

Latest runtime deployment: **Deploy #182 `31818968380` SUCCESS**, PR #78 merge `ed00f7bdf89b1471fd34c4c4b8a0dd16eefac04f`.

PR #79 merge `e8912d29b2aa2631a396518751cf9cbbe3d6b546` added direct read-only BC-2 evidence to Runtime Read. Runtime Read #11 verified:
- service active/healthy;
- schema v5;
- autonomy enabled/normal, paused false, retry null, speed 3.0x;
- sim `2025-05-05T08:34:00+00:00`;
- decision calls 372;
- Gemini `gemini-3.1-flash-lite` primary and Groq `qwen/qwen3.6-27b` fallback preserved;
- transient Gemini 503 had been handled by fallback, with current retry null;
- Weight 215.0 lb and BF 9.0% are live `simulated` `physiology_engine` fields;
- BC-2 activation boundary `2025-05-05T07:55:00+00:00` is `bootstrapped`, `stat_mutated=false`, old/new identical;
- derived activation FM 19.35 lb, FFM 195.65 lb, BMI 26.167763.

A historical provider 413 occurred on an 8,645-token cognition request. It is not current retry state; cognition enrichment stays compact.

## Universal invariants

Darian/Thorne Estate are production exemplars, never reusable-engine identity.

Inventory/eating:
`Universal food definition -> concrete stack -> reachable eating context -> structured quantity -> deterministic validation -> atomic stock transition + immutable evidence`

Cognition:
`deterministic state/context -> one model proposal -> authoritative validation -> deterministic mutation`

Body composition:
`complete bounded energy/nutrition evidence + current FM/FFM + resistance evidence + recovery + genetic envelope -> deterministic settlement -> coupled Weight/BF history + audit`

## Deployed food/nutrition checkpoint

- Inventory Foundation v1 — PR #71 / Deploy #177.
- Inventory Operations v1 — PR #73 / Deploy #178.
- Food Nutrition Semantics & Visibility v1 — PR #74 / Deploy #179.
- Eating Behavior v1 — PR #76 / Deploy #180.
- Meal Choice Intelligence v1 — PR #77 / Deploy #181.

Meal Choice Intelligence is a compact enrichment inside the existing single cognition call: same-day intake/macros/meal count, latest meal timing, recent training, recovery, REE reference and character nutrition policy. No broad Mind/Behavior Engine and no extra model call.

## BC-2 Body Composition Progression

**COMPLETE / DEPLOYED / LIVE-ACTIVATED** via PR #78 / Deploy #182; direct readback via PR #79 / Runtime Read #11.

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

## Public repository security checkpoint

`Ye-Shwethway/observer-sandbox` is now **PUBLIC**.

Public Readiness Hardening v1 merged via PR #80 / `bf5e537cdeceaa6c5a8d4d61f21b67d636f01f20`. After the visibility transition, previously queued CI resumed on a standard GitHub-hosted runner and CI #680 passed.

Public Hardening Fixup v1 refined the audit's generic assignment detector to remove two false positives while preserving concrete credential signatures. Public Readiness Security Audit #2 passed with:
- `PUBLIC_READINESS_SECRET_AUDIT=PASS`;
- `full_history_high_confidence_secret_findings=0`;
- `PUBLIC_READINESS_WORKFLOW_POLICY=PASS`.

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
- the public security-audit runner reported `GITHUB_TOKEN` Contents: read / Metadata: read.

The GitHub App cannot read all repository Actions/security/ruleset settings. Before resuming BC-3, manually verify in the UI:
1. outside-contributor fork workflow approval policy;
2. Secret scanning / Push protection;
3. `main` branch/ruleset protection after the private-to-public transition.

## Next development slice — BC-3 Body Measurement Progression Batch

Do not split structurally equivalent circumference fields into repetitive PR/deploy cycles.

BC-3 target family:
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

Measurements must combine live body composition + regional training/anatomical context + character-specific structural/genetic envelopes. Never derive every circumference from body weight alone.

## Later sequence

1. verify post-public GitHub security settings;
2. BC-3 measurement batch;
3. skills;
4. intellectual attributes;
5. mental/emotion dynamics;
6. later social/relationship/sexual physiology;
7. broad Mind/Behavior architecture only after enough feature families exist to justify it.

## Exact resume point

Finish the post-public GitHub settings verification, then resume **BC-3 Body Measurement Progression Batch**.

Do not add economy/currency, automatic restocking, deep recipes/crafting, Character Memory, broad Mind/Behavior engines, or a second production character merely for testing as side effects.
