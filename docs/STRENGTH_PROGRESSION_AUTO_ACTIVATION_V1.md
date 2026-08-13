# Strength Progression Automatic Activation v1

Status: ACTIVATION CANDIDATE

Scope remains **Free Weights + Strength only**. This slice wires the already-accepted idempotent settlement core into continuous production autonomy at bounded simulated action-completion boundaries.

## Trigger policy

The 2-second service poll is **not** a progression clock. Progression policy is evaluated only after an action actually completes and simulated time advances.

`strength-progression-auto-activation-v1` settles only when one of these is true:

1. **Bootstrap** — no prior `strength_progression_settled` cursor exists. The settlement core performs a non-mutating bootstrap and marks pre-feature Strength stimulus consumed.
2. **Eligible Strength stimulus** — an unconsumed positive Strength stimulus is at least 48 simulated hours old and current recovery is not hard-blocked. It settles at the next completed-action boundary.
3. **Detraining checkpoint** — no eligible stimulus requires immediate settlement, but at least 24 simulated hours have elapsed since the last settlement and Strength-training history exists.

Otherwise activation skips settlement entirely and writes no progression event.

## Event-volume bound

- No Strength-training history after bootstrap: no daily progression checkpoint spam.
- With Strength-training history: pure time-decay settlement occurs at most once per 24 simulated hours.
- Eligible recovered Strength stimulus may cause an earlier settlement so it is not delayed to the next daily checkpoint.
- Same/older simulated boundaries are skipped.

## Ordering

At action completion:

`action completes -> progression due check -> optional Strength settlement -> refreshed snapshot -> next cognition decision -> Creator completion notification`

This ordering lets the next cognition boundary observe the updated raw Strength if a tiny progression change occurs, while progression failure remains downstream/best-effort and cannot roll back the completed action or stop continuous autonomy.

## Activation safety

The settlement core already proves:
- non-retroactive bootstrap;
- one-time stimulus consumption;
- >=48h positive recovery gate;
- exact detraining interval integration with training resets;
- same-boundary replay no-op;
- profile history + audit evidence for mutations.

This activation slice must additionally prove that repeated action-completion checks remain sparse and that the live production DB is untouched during pre-merge acceptance.

No other attributes, skills, body measurements or composition progression are included in this first mutation activation exemplar.
