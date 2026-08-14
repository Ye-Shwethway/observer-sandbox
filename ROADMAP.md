# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

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

Latest runtime deployment: **Deploy #183 `31826301329` SUCCESS**, BC-3 PR #82 merge `45c29a834828c9afc1f0a7e190b9f5904019e546`.

Post-deploy Runtime Read #12 rerun verified:
- service active/healthy;
- schema v5;
- autonomy enabled/normal, paused false, retry null, speed 1.0x;
- sim `2025-05-05T11:17:00+00:00`;
- cognition decision calls 386;
- current pending action `read` in the Living Room;
- Gemini `gemini-3.1-flash-lite` primary with tested Groq `qwen/qwen3.6-27b` fallback preserved;
- `body.weight_lb=215.0` and `body.body_fat_pct=9.0` remain live `simulated` `physiology_engine` fields;
- BC-2 activation boundary remains `2025-05-05T07:55:00+00:00`, `bootstrapped`, `stat_mutated=false`, old/new composition identical;
- all eleven BC-3 circumference fields are present in production, including `body.hips_in=39.0`;
- BC-3 fields remained authored/static and no `body_measurement_progression_settled` event existed at readback, so deployment/seed upgrade is verified while natural runtime activation is still pending.

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

## Body Composition / Measurement Program

Canonical:
- `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`
- `docs/NUTRITION_ENERGY_EVIDENCE.md`
- `docs/BODY_COMPOSITION_PROGRESSION_V1.md`
- `docs/BODY_MEASUREMENT_PROGRESSION_V1.md`

Research locks:
- no static universal `3500 kcal = 1 lb` rule;
- Weight/FM/FFM/BF% are coupled;
- sex may affect reference physiology but is not a crude hypertrophy multiplier;
- age is context, not a hard cliff;
- genetics are character-specific potential envelopes;
- hunger/energy scores are not kcal;
- protein/energy availability constrain lean adaptation;
- circumference progression combines body composition and regional training context rather than scaling every field from body weight;
- detailed fluid/glycogen/endocrine/micronutrient simulation remains deferred.

### BC-0 — Simulated Profile Re-seed Safety

**COMPLETE / DEPLOYED** via PR #69 / Deploy #175.
Ordinary re-init/deploy preserves engine-owned simulated profile state.

### BC-1 — Nutrition & Energy Evidence

**COMPLETE / DEPLOYED** via PR #70 / Deploy #176.
Provides actor-specific resting-energy reference, Compendium-informed action intensity, immutable intake/expenditure evidence and coverage-aware bounded aggregation. BC-1 itself never mutates Weight/BF.

### BC-2 — Body Composition Progression Exemplar

**COMPLETE / DEPLOYED / LIVE-ACTIVATED** via PR #78 / Deploy #182; direct activation readback via PR #79 / Runtime Read #11 and preserved after Deploy #183.

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

### BC-3 — Body Measurement Progression Batch

**COMPLETE / DEPLOYED / SEEDED / ACTIVATION PENDING NATURAL BOUNDARY** via PR #82 / Deploy #183.

Invariant:
`BC-2 bounded body-composition settlement + regional resistance evidence + authored anatomy/genetic envelope -> bounded regional measurement settlement -> atomic profile history + event`

BC-3 behavior:
- covers neck, shoulders, chest, waist, hips, biceps relaxed/flexed, triceps, forearms, thighs and calves in one batched implementation;
- consumes BC-2 settlement events as its body-composition cadence and does not introduce a second nutrition/composition authority;
- combines general FM/FFM changes with data-driven regional resistance exposure;
- small whole-body FFM effects may affect an unexposed region, while regional resistance creates an additional stronger local increment;
- uses character-specific circumference maxima/targets and activation-relative safety guards;
- preserves authored circumference values numerically at activation and prevents retroactive progression;
- changed fields, profile history and causal settlement event are atomic;
- no schema migration and no extra model call.

Darian's complete authored measurement family now includes `body.hips_in=39.0`. The reusable profile schema includes `genetics.hips_max_in`; Darian's authored hip envelope is 41.0. These values are Darian-specific canon and are not universal character ratios.

PR-head CI #698 passed the full test suite and CLI smoke checks. Disposable production-copy acceptance passed for BC-3 as well as BC-2, Strength and Stamina regression lanes. The BC-3 validator exercises candidate initialization on the production copy, proving the new authored hip fields can be added without clobbering existing engine-owned simulated state.

Post-deploy Runtime Read #12 rerun confirmed all eleven body measurements are present, with hips at 39.0 inches. The first natural BC-3 activation event had not yet occurred at that readback. Production must not be accelerated or directly mutated only to manufacture activation evidence.

## Public Repository Security — COMPLETE / PUBLIC

Canonical: `docs/PUBLIC_REPOSITORY_SECURITY.md` and `SECURITY.md`.

`Ye-Shwethway/observer-sandbox` is public. Public Readiness Hardening v1 was merged in PR #80 (`bf5e537cdeceaa6c5a8d4d61f21b67d636f01f20`) and Public Hardening Fixup v1 followed in PR #81. Public Readiness Security Audit on PR #82 also completed SUCCESS.

Security locks:
- full reachable Git-history scan uses `fetch-depth: 0`;
- potential secret values are never printed by the audit;
- `.env`, `secrets.env`, private-key formats, runtime DBs and backups are ignored;
- `pull_request_target` and `permissions: write-all` are prohibited;
- reusable production-copy validation retains an explicit same-repository fork guard;
- GitHub additionally withholds repository secrets from fork-originated `pull_request` workflows by default;
- disposable production-copy validation unsets all model and Telegram credentials;
- production credentials remain GitHub Actions secrets plus VPS `/var/lib/observer-sandbox/secrets.env` mode `0600`;
- repository `GITHUB_TOKEN` observed in public audit/read workflows has read-only contents/metadata permissions.

Post-visibility manual settings still require UI verification where the GitHub App cannot read account-level repository settings: outside-contributor workflow approval, Secret scanning/Push protection, and `main` branch/ruleset protection.

## Later profile sequence

1. observe and verify BC-3 natural production activation;
2. verify remaining post-public GitHub security settings when convenient;
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

Re-read live production first. If a natural eligible action boundary has occurred since post-deploy Runtime Read #12, verify **BC-3 activation** read-only. Do not force or accelerate production for evidence.

After BC-3 activation is naturally verified, proceed to the **skill progression family** unless the Creator gives a newer instruction.
