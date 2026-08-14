# Meal Choice Intelligence v1

Status: **IMPLEMENTATION CANDIDATE**
Synchronized: 2026-08-14

## Purpose

Improve autonomous food selection without creating a separate Mind Engine or Behavior Engine.

The existing cognition call remains the decision-maker. This slice adds compact deterministic decision context so the model can consider accumulated intake, meal timing, training/recovery demand and character nutrition policy when choosing among the authoritative food/portion options provided by Eating Behavior v1.

Core invariant:

`persisted nutrition/training evidence + current physiology + character nutrition policy + authoritative food choices -> one existing cognition decision -> deterministic meal validation/settlement`

No additional model call is introduced.

## Compact cognition context

`meal_choice_context` contains only bounded aggregates rather than raw history:

- same-simulation-day intake kcal, protein, carbohydrate and fat;
- same-day completed meal count;
- same-day estimated expenditure and evidence coverage ratio;
- last completed meal time, minutes ago, kcal and protein when available;
- completed training count/minutes in the previous 12 simulated hours and time since the latest session;
- current hunger, energy, fatigue, sleepiness and thirst;
- actor-specific resting-energy reference, explicitly labeled as a reference rather than a daily calorie target;
- character-authored nutrition goal, energy intent, protein priority and dietary constraints.

This compact form deliberately avoids copying raw meal/event history into the prompt. A previous production cognition error showed that oversized prompts can hit provider TPM/request limits, so bounded aggregate context is part of the reliability contract.

## Character policy vs universal engine

The reusable engine does not contain Darian-specific branches.

Character nutrition priorities live in the selected character's autonomy policy. Darian's first production policy currently states a maintenance-oriented goal: preserve a lean muscular body composition while supporting training performance, recovery and ordinary health. Protein is contextually prioritized after training/recovery demand, not maximized in every meal. No dietary constraint is currently authored.

Future characters may carry different nutrition policies without changing meal-choice code.

## Authority boundaries

- The model may use the context to choose intent only.
- `config/items.v1.json` remains authoritative for food nutrition.
- Eating Behavior v1 remains authoritative for concrete stack reachability, portion bounds, stock validation and atomic settlement.
- The model does not calculate authoritative macros, mutate inventory, write body composition, or convert REE into a daily calorie target.
- Hunger/energy need scores remain separate from kcal accounting.

## Relationship to future engines

This slice is intentionally not a Mind Engine or Behavior Engine. Those broader systems should be designed after more character/world feature families are available, so they can integrate real signals instead of prematurely abstracting over missing systems.

For now, feature-specific deterministic context plus one general cognition call is the preferred lightweight architecture.

## Validation

Required before merge:

- focused unit coverage for same-day intake, last-meal timing, recent-training aggregation, actor-specific REE reference and character policy;
- proof that context generation is read-only and does not add events/model calls;
- full repository CI;
- existing Eating Behavior v1 acceptance remains green.

No production-copy validation is required because the slice adds no schema migration or production-state mutation.

## Next authorized slice

After Meal Choice Intelligence v1 is merged/deployed/read back, proceed to **BC-2 — Body Composition Progression Exemplar**.

BC-2 must use an activation boundary and evidence-complete bounded windows so deployment does not retroactively mutate body state from legacy/incomplete history. Natural Eating Behavior continues autonomously in production; it does not need to be forced or accelerated merely to unblock BC-2 implementation.
