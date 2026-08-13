# Fatigue Causal Recovery + Inspect Loop Guard v1

Status: COMPLETE / CI VERIFIED / DISPOSABLE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED / LIVE HEALTH VERIFIED

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

Final pre-merge evidence on head `cb500d9319aa6247c7db2132dbc52f70fa917aec`:

- Fatigue Causal Recovery v1 Acceptance #5 run `31703588566` — SUCCESS;
- CI #471 run `31703588016` — SUCCESS;
- Causal Need Resolution v2 compatibility Acceptance #17 run `31703587998` — SUCCESS.

The earlier evidence-bearing acceptance run `31703254895` captured this copied live baseline:

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

## Merge, release, and production readback

- PR #27 merged as `31484c561948d84e97d5c677f15cd1ced7f8ad89`;
- release marker commit `9121904f3db9009af32e30dbb925c5c60cd837cb`;
- post-release CI #473 run `31703753642` — SUCCESS;
- Deploy Observer Sandbox #153 run `31703753498` — SUCCESS.

Deploy readback confirmed:

- service `active` and runtime `healthy=true`;
- schema version `4`;
- autonomy enabled, normal mode, not paused;
- configured Gemini cognition binding preserved;
- Telegram API connected.

The same readback observed live sim time `2025-05-02T15:14:00+00:00`, fatigue `70.91`, and a currently pending `inspect` action. That pending action existed at deploy/readback time and is not evidence that the new selection guard failed, because deployment preserves an already-planned action; the new causal selection applies at the next cognition decision boundary.

The readback also showed runtime speed `2.0`. This was not changed by the deploy or by this slice's validation. Because production control mutation is outside dry-run validation policy, the implementation did not silently alter it. The live speed value remains a separate Creator/runtime-control state to reconcile before any future production observation that assumes `1x`.

## Production policy

Dry-run, acceptance, tuning, and accelerated simulation must run on a disposable copy of production DB. Production is reserved for all-green merge/deploy and read-only post-deploy verification. Production runtime acceleration is not a validation mechanism.

## Follow-on

Resume Strength Progression Live Cycle Validation & Tuning v1 under the corrected production-copy validation policy. Live production may provide read-only baseline/evidence; simulated boundary acceleration and mutation testing belong on the disposable copy.
