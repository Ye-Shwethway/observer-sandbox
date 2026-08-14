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

Use production-copy validation only when concrete stateful/migration risk justifies it. Never accelerate/mutate production merely to manufacture acceptance evidence.

Any new architecture/control invariant updates its canonical contract + ROADMAP + bootstrap in the same development cycle.

## Current verified production checkpoint

Latest deployment: **Deploy #180 `31816335698` SUCCESS**, PR #76 merge `ed297348ea0ba77d8f02e9ebec41f19643e7f175`.

Fresh read-only Runtime Read attempt 6 after deployment verified:
- service active/healthy;
- schema v5;
- world `thorne-estate-v3.3-physical-attribute-training`;
- wealthy food reserve marker remains applied once;
- autonomy enabled/normal, paused false, retry null;
- runtime speed 3.0x;
- sim `2025-05-05T06:10:00+00:00` at read time;
- Darian in the Home Gym with a 50-minute `train` action pending;
- cognition calls 363;
- Gemini `gemini-3.1-flash-lite` primary and Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram connected.

A historical provider 413 occurred on an 8,645-token cognition request. It is not the current retry state, but cognition context should remain compact rather than expanding raw histories.

## Universal invariants

Darian/Thorne Estate are production exemplars, never reusable-engine identity.

Inventory/eating:
`Universal food definition -> concrete stack -> reachable eating context -> structured quantity -> deterministic validation -> atomic stock transition + immutable evidence`

Cognition:
`deterministic state/context -> one model proposal -> authoritative validation -> deterministic mutation`

## Deployed inventory / nutrition / eating checkpoint

- Inventory Foundation v1 — PR #71 / Deploy #177.
- Inventory Operations v1 — PR #73 / Deploy #178.
- Food Nutrition Semantics & Visibility v1 — PR #74 / Deploy #179.
- Eating Behavior v1 — **PR #76 / Deploy #180**.

Eating Behavior v1 is live:
- cognition uses structured `resources`;
- meals choose exact food stack IDs + bounded quantities;
- stock/reachability/portions are deterministically validated;
- multi-food settlement is atomic;
- combined definition-based kcal/protein/carbs/fat persists in BC-1 `nutrition_intake` evidence;
- Telegram completed structured meals show items + total macros;
- legacy empty-resource compatibility applies only to already-persisted pre-v1 meals.

Canonical: `docs/EATING_BEHAVIOR_V1.md`.

## Meal Choice Intelligence v1 — CURRENT PR #77

Canonical: `docs/MEAL_CHOICE_INTELLIGENCE_V1.md`.

This is a lightweight cognition enrichment, **not** a Mind Engine or Behavior Engine.

Candidate context adds, without another LLM call:
- compact same-day intake kcal/macros/meal count;
- compact expenditure + evidence coverage;
- last meal timing/kcal/protein;
- recent 12-hour training aggregate;
- current hunger/energy/fatigue/sleepiness/thirst;
- actor-specific REE reference explicitly marked non-target;
- character-authored nutrition goal, energy intent, protein priority and dietary constraints.

Raw history is deliberately not copied into the prompt.

Darian's authored policy is maintenance-oriented: preserve a lean muscular body composition while supporting training performance, recovery and ordinary health. No dietary constraint is currently authored.

Validation: focused read-only tests + full CI + existing Eating Behavior acceptance. No new production-copy gate is needed because no schema or runtime state mutation is introduced.

## Next authorized slice — BC-2 Body Composition Progression

Current Creator instruction authorizes proceeding to BC-2 after Meal Choice Intelligence v1 is merged/deployed/read back; do not wait for a naturally timed next meal and do not force/accelerate eating for acceptance.

BC-2 safety contract:
- establish activation sim time at activation/deployment boundary;
- no retroactive pre-activation body change;
- settle only evidence-complete bounded windows;
- incomplete intake/expenditure defers settlement instead of becoming an artificial deficit;
- coupled `body.weight_lb` + `body.body_fat_pct` mutation with derived FM/FFM/BMI;
- bounded Hall/Forbes-inspired energy partition direction, not fixed 3,500 kcal/lb;
- separate resistance-training lean adaptation constrained by protein/energy/recovery/genetic headroom;
- atomic profile/history/audit;
- physiological clamps;
- no Darian engine branch or extra model call.

Natural structured-meal observations remain useful later for calibration but are not an implementation blocker under the current Creator instruction.

## Later sequence

1. finish PR #77 -> merge/deploy/readback;
2. BC-2 body composition;
3. BC-3 measurements;
4. skills;
5. intellectual attributes;
6. mental/emotion dynamics;
7. later social/relationship/sexual physiology;
8. broad Mind/Behavior architecture only after enough feature families exist to justify it.

## Exact resume point

Finish **Meal Choice Intelligence v1 PR #77** and then proceed directly to **BC-2** using activation-boundary + evidence-completeness guards.

Do not add economy/currency, automatic restocking, deep recipes/crafting, Character Memory, broad Mind/Behavior engines, or a second production character merely for testing as side effects.
