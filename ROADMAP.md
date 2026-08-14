# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-14

## Operating principles

- Python/SQLite runtime and live world state are authoritative.
- AI proposes structured cognition; deterministic engines own mutation.
- Telegram is an observer/control adapter, never a simulation engine.
- Preserve the LEGO runtime contract:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian/Thorne Estate are first rich production exemplars, never reusable-engine identity.
- Reusable runtime/cognition/progression/query/control/inventory/nutrition logic is actor/entity/definition-id driven.
- Prefer minimum-runnable reversible slices.
- One bounded exemplar for a genuinely new invariant; structurally equivalent follow-ons batch by pattern.
- Default flow: `branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`.
- Production-copy validation is required for concrete stateful/migration risk.
- Never accelerate/directly mutate production merely to manufacture acceptance evidence.

## Current verified production baseline

Latest runtime deployment: **Deploy #182 `31818968380` SUCCESS**, BC-2 PR #78 merge `ed00f7bdf89b1471fd34c4c4b8a0dd16eefac04f`.

BC-2 live readback observability was merged separately in PR #79, merge `e8912d29b2aa2631a396518751cf9cbbe3d6b546`. Runtime Read #11 then verified:
- service active/healthy;
- schema v5;
- autonomy enabled/normal, paused false, retry null, speed 3.0x;
- sim `2025-05-05T08:34:00+00:00` at readback;
- cognition decision calls 372;
- Gemini `gemini-3.1-flash-lite` primary with tested Groq `qwen/qwen3.6-27b` fallback preserved;
- a transient Gemini 503 had already been handled through the configured fallback; current retry remained null;
- Telegram/runtime state continued naturally;
- `body.weight_lb=215.0` and `body.body_fat_pct=9.0` are live `simulated` fields owned by `physiology_engine`;
- BC-2 activation boundary is `2025-05-05T07:55:00+00:00`;
- activation event status `bootstrapped`, `stat_mutated=false`, old/new composition identical;
- derived activation composition: FM 19.35 lb, FFM 195.65 lb, BMI 26.167763.

A historical provider 413 occurred on an 8,645-token cognition request. It is not current retry state. Cognition enrichment remains compact rather than copying raw histories.

## Completed runtime/profile foundations

- schema v4 composable runtime foundation, operationally extended by schema v5 inventory stacks;
- P0/P0.5 foundation + dynamic provider layer;
- P1 continuous autonomy;
- P2 Telegram Observer/Profile/Control;
- P2.3 Creator AI Control v1;
- Runtime Cognition Fallback v1;
- Telegram Home lifecycle;
- Universal Character Engine;
- Dynamic Resource Awareness / Choice Breadth;
- Object Familiarity / Inspect Utility Guard;
- fatigue/recovery, targeted training, readiness/effectiveness/effective load;
- Minimum Training Stimulus + Session Load/Recovery Guard;
- causal needs + sleep/circadian behavior;
- Training Method Semantics v1;
- Physical Attribute Progression Framework v1 for Strength, Stamina, Agility, Speed, Reflexes, Endurance, Flexibility.

## Universal Item / Eating Program

Core invariant:
`Universal definition -> concrete stack -> reachable action context -> structured quantity -> deterministic validation -> state transition + immutable evidence`

- Inventory Foundation v1 — **COMPLETE / DEPLOYED** via PR #71 / Deploy #177.
- Inventory Operations v1 — **COMPLETE / DEPLOYED** via PR #73 / Deploy #178.
- Food Nutrition Semantics & Visibility v1 — **COMPLETE / DEPLOYED** via PR #74 / Deploy #179.
- Eating Behavior v1 — **COMPLETE / DEPLOYED** via PR #76 / Deploy #180.
- Meal Choice Intelligence v1 — **COMPLETE / DEPLOYED** via PR #77 / Deploy #181.

Meal Choice Intelligence uses the existing single cognition call and adds compact same-day intake/macros/meal-count, latest meal timing, recent training, recovery, actor REE reference and character nutrition policy. It is not a broad Mind/Behavior Engine and introduces no extra model call.

Canonical:
- `docs/EATING_BEHAVIOR_V1.md`
- `docs/MEAL_CHOICE_INTELLIGENCE_V1.md`

## Body Composition Program

Canonical:
- `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`
- `docs/NUTRITION_ENERGY_EVIDENCE.md`
- `docs/BODY_COMPOSITION_PROGRESSION_V1.md`

Research locks:
- no static universal `3500 kcal = 1 lb` rule;
- Weight/FM/FFM/BF% are coupled;
- sex may affect reference physiology but is not a crude hypertrophy multiplier;
- age is context, not a hard cliff;
- genetics are character-specific potential envelopes;
- hunger/energy scores are not kcal;
- protein/energy availability constrain lean adaptation;
- detailed fluid/glycogen/endocrine/micronutrient simulation remains deferred.

### BC-0 — Simulated Profile Re-seed Safety

**COMPLETE / DEPLOYED** via PR #69 / Deploy #175.
Ordinary re-init/deploy preserves engine-owned simulated profile state.

### BC-1 — Nutrition & Energy Evidence

**COMPLETE / DEPLOYED** via PR #70 / Deploy #176.
Provides actor-specific resting-energy reference, Compendium-informed action intensity, immutable intake/expenditure evidence and coverage-aware bounded aggregation. BC-1 itself never mutates Weight/BF.

### BC-2 — Body Composition Progression Exemplar

**COMPLETE / DEPLOYED / LIVE-ACTIVATED** via PR #78 / Deploy #182; direct activation readback via PR #79 / Runtime Read #11.

Invariant:
`complete bounded BC-1 evidence + current FM/FFM + resistance-training evidence + recovery + genetic envelope -> deterministic 24h settlement -> atomic Weight/BF history + event`

Live behavior:
- first completed-action boundary activated `body.weight_lb` + `body.body_fat_pct` as simulated `physiology_engine` fields with no numerical change;
- pre-activation history cannot create retroactive gain/loss;
- 24 simulated-hour settlement windows;
- incomplete evidence creates an audited no-mutation deferred window rather than an artificial deficit;
- passive partition uses Forbes small-change FFM share and Hall tissue-change energy densities rather than a fixed 3,500-kcal rule;
- only training methods whose workload channels include `resistance` qualify for separate RT lean adaptation;
- protein factor saturates at the 1.6 g/kg/day policy reference;
- RT adaptation is constrained by energy availability, recovery, resistance effective minutes, genetic FFM headroom and sustainable BF-floor headroom;
- only Weight/BF persist; FM/FFM/BMI remain derived views;
- coupled history/event writes are atomic;
- no extra LLM call, Darian-specific engine branch or schema migration.

## Public Repository Security — COMPLETE / PUBLIC

Canonical: `docs/PUBLIC_REPOSITORY_SECURITY.md` and `SECURITY.md`.

`Ye-Shwethway/observer-sandbox` is now public. Public Readiness Hardening v1 was merged in PR #80 (`bf5e537cdeceaa6c5a8d4d61f21b67d636f01f20`). After the visibility flip, queued private-quota CI resumed on a standard GitHub-hosted runner and CI #680 completed SUCCESS.

Public Hardening Fixup v1 corrected two audit false positives (`page_token` and `DEFAULT_SECRET_FILE`) without weakening concrete credential signatures. Public Readiness Security Audit #2 then passed with:
- `PUBLIC_READINESS_SECRET_AUDIT=PASS`;
- `full_history_high_confidence_secret_findings=0`;
- `PUBLIC_READINESS_WORKFLOW_POLICY=PASS`.

Security locks:
- full reachable Git-history scan uses `fetch-depth: 0`;
- potential secret values are never printed by the audit;
- `.env`, `secrets.env`, private-key formats, runtime DBs and backups are ignored;
- `pull_request_target` and `permissions: write-all` are prohibited;
- reusable production-copy validation retains an explicit same-repository fork guard;
- GitHub additionally withholds repository secrets from fork-originated `pull_request` workflows by default;
- disposable production-copy validation unsets all model and Telegram credentials;
- production credentials remain GitHub Actions secrets plus VPS `/var/lib/observer-sandbox/secrets.env` mode `0600`;
- repository `GITHUB_TOKEN` observed in the public security audit had read-only contents/metadata permissions.

Post-visibility manual settings still require UI verification where the GitHub App cannot read account-level repository settings: outside-contributor workflow approval, Secret scanning/Push protection, and `main` branch/ruleset protection.

### BC-3 — Body Measurement Progression Batch — NEXT DEVELOPMENT SLICE

After the post-public settings check, resume immediately with BC-3. Do not split structurally equivalent circumference fields into repetitive PR/deploy cycles.

BC-3 direction:
- neck, shoulders, chest, waist, hips, biceps relaxed/flexed, triceps, forearms, thighs and calves;
- combine live body composition with regional training stimulus/anatomy and character-specific structural/genetic envelopes;
- never derive every circumference from body weight alone;
- prove any genuinely new measurement invariant once, then batch structurally equivalent measurement fields in one PR/deploy cycle.

## Later profile sequence

1. verify post-public GitHub security settings;
2. BC-3 measurement progression batch;
3. skill progression family;
4. intellectual attributes;
5. mental/emotion dynamics;
6. later relationship/social/sexual physiology when prerequisites mature;
7. broad Mind/Behavior architecture only after enough real feature signals exist to justify it.

## Future universal object/inventory expansion

Proceed by family when needed:
1. movable containers + carried inventory;
2. fixed storage capacity semantics;
3. training equipment definitions + concrete instances;
4. tools/electronics/books/medical supplies;
5. clothing/equipped-state;
6. materials/crafting when justified;
7. economy: ownership transfer, vendors, pricing, currency/accounts, transactions, scarcity/replenishment.

## Deferred boundaries

Do not add as side effects:
- broad Mind Engine / Behavior Engine now;
- Character Memory Engine;
- multi-fallback/circuit-breaker/provider-health expansion;
- Telegram secret/model-parameter editing;
- second production character solely for testing;
- automatic economy restocking;
- full RPG encumbrance/capacity UI;
- arbitrary-depth nested containers;
- spoilage/deep recipe graph;
- currency/shops/economy simulation;
- generalized crafting;
- detailed endocrine/micronutrient/organ metabolic simulation;
- estate exterior/Tahoe traversal.

## Exact resume point

Finish the post-public GitHub settings verification, then proceed to **BC-3 Body Measurement Progression Batch**.
