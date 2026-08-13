# Fatigue Causal Recovery + Inspect Loop Guard v1

Status: IMPLEMENTED / CI VERIFIED / PRE-MERGE DISPOSABLE PRODUCTION-COPY ACCEPTANCE VERIFIED

## Problem observed

After a training session pushed systemic fatigue above the training gate, runtime validation correctly removed `train` as an available action, but cognition did not treat systemic fatigue as a causal need requiring recovery. The model could therefore choose technically valid but low-value training-adjacent substitutions such as inspecting the Combat Mat while describing the inspection as continuation of physical training.

A second weakness was also exposed: the autonomy policy already discouraged repeated same-room `inspect` / `use` behavior, but that rule was prompt guidance only. Candidate shaping did not deterministically suppress a low-value inspection loop.

Acceleration did not create either behavior. It caused more action boundaries to occur in a short wall-clock period and therefore made the existing selection weakness much more visible.

## Causal fatigue contract

Systemic fatigue is now part of the same causal physiological-need family as sleepiness, energy, thirst, hunger, and cleanliness.

Authored thresholds reuse existing runtime/training gates rather than inventing a new scale:

- strong fatigue: `fatigue >= 55`;
- critical fatigue: `fatigue >= 70`.

Resolvers:

- strong: `rest` or `sleep`;
- critical: `rest` or `sleep`.

At a decision boundary where fatigue is the highest active need, causal action-option shaping exposes only a locally valid recovery action, or movement toward a valid resolver if one is required. Training-adjacent `inspect` / `use` behavior is not a fatigue resolver.

Current authored check order is:

`sleepiness -> energy -> fatigue -> thirst -> hunger -> cleanliness`

Critical needs continue to sort ahead of strong needs.

## Deterministic discretionary repetition guard

Recent completed action evidence is reused; no new mutable repetition counter or schema field is introduced.

Candidate shaping now applies two bounded rules after causal need shaping:

1. if the latest discretionary object interaction was `inspect` or `use`, the same action-target pair is removed from the next candidate set;
2. if the two most recent action events were `inspect` / `use` interactions in the current room, further `inspect` / `use` candidates are suppressed for the next decision boundary.

If filtering would otherwise produce no candidates, the original option set is retained as a safety fallback. This keeps inspection available when it is genuinely the only valid behavior and avoids turning the guard into a global ban.

## Disposable production-copy acceptance

Validation follows the production-safety rule: production SQLite is used only as the source of a copied baseline. All reproduced states, action execution, and synthetic repetition evidence are applied only to a temporary copied DB. The workflow does not change live runtime speed, autonomy state, profile/progression state, or Telegram delivery, and it performs zero model calls.

Acceptance workflow: `Fatigue Causal Recovery v1 Acceptance`.

Final pre-merge evidence:

- acceptance run `31703254895` — SUCCESS;
- CI run `31703255025` — SUCCESS;
- compatibility acceptance `Causal Need Resolution v2 Acceptance` run `31703255122` — SUCCESS.

The copied live baseline captured by run `31703254895` was:

- sim time: `2025-05-02T14:59:00+00:00`;
- location: Training Hall;
- current action: `move`;
- energy: `54.298`;
- fatigue: `71.285`;
- hunger: `30.514`;
- thirst: `21.441`;
- sleepiness: `28.3`;
- cleanliness: `92.278`.

The acceptance then reproduced the Creator-observed post-training condition on the disposable copy with fatigue `72.4`. Evidence:

- fatigue classified as `critical` at threshold `70.0`;
- resulting causal candidate set was exactly one `rest` action;
- `train`, `inspect`, and `use` were absent;
- a normal `rest` action for 180 simulated minutes reduced fatigue naturally from `72.4` to `46.9` through ordinary action semantics;
- after two same-room disposable `inspect` / `use` fixture events, subsequent candidates contained no `inspect` or `use` actions;
- workflow reported `production_mutated=false`, `disposable_production_copy=true`, `model_calls=0`.

The older thirst/hunger production-copy acceptance was also updated to explicitly isolate its fixture from the newly-supported fatigue need by setting copied-fixture fatigue to a comfortable value. This preserved the pre-existing causal resolver contract and returned the compatibility run to green.

## Tuning decision

No new fatigue constants were introduced. The causal cognition thresholds deliberately reuse the existing training thresholds (`55` baseline/strong and `70` hard/critical), so recovery behavior and training availability share the same physiological scale.

No Strength progression formula, Strength stimulus mapping, recovery-realization formula, detraining constant, grading rule, body measurement rule, schema version, or production data was changed in this slice.

Schema remains v4.

## Production policy

Dry-run, acceptance, tuning, and accelerated simulation must run on a disposable copy of production DB. Production is reserved for all-green merge/deploy and read-only post-deploy verification. Production runtime acceleration is not a validation mechanism.

## Follow-on

After this bounded autonomy defect is deployed and read back healthy, resume Strength Progression Live Cycle Validation & Tuning v1 under the corrected production-copy validation policy. Live production may provide read-only baseline/evidence; simulated boundary acceleration and mutation testing belong on the disposable copy.
