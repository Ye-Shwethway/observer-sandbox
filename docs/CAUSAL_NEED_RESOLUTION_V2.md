# Causal Need Resolution v3

Status: COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED

## Scope

This closes the current five-need physiological recovery family while preserving the authored priority order:

`sleepiness -> energy -> thirst -> hunger -> cleanliness`

Critical needs outrank strong needs.

## Exemplar-first development pattern

### Exemplar — Energy

Energy proved the missing directionality invariant. Hunger/thirst/sleepiness are high-is-bad and require a reducing effect; energy is low-is-bad and requires an increasing effect.

A recovery option is causal only when its direct authored effect or intrinsic per-hour action effect moves the active need toward health. For strong low energy, `rest` is a valid local resolver because its intrinsic effect raises energy. Discretionary training is hidden until the active need clears.

### Batch expansion — Sleepiness + Cleanliness

After the Energy directionality pattern was established, equivalent remaining needs were added in the same branch/PR:

- strong sleepiness -> local `rest` or `sleep` when causally available;
- critical sleepiness -> `sleep` only, routing toward a sleep-capable object when needed;
- poor cleanliness -> `shower`, routing toward the Master Bathroom when needed;
- thirst/hunger retain their deployed `drink`/`eat` behavior.

Both direct object effects and intrinsic per-hour action effects are valid causal evidence. Resolver selection does not invent a second priority score; `decision_signals.needs_attention` remains authoritative.

## Validation

The batch proved:

1. low Energy exposes only causal recovery and materially increases Energy;
2. strong Sleepiness suppresses discretionary training;
3. critical Sleepiness routes toward Bed rather than accepting generic rest;
4. poor Cleanliness routes toward Shower and local showering clears the strong condition;
5. Hunger/Thirst deterministic behavior remains green;
6. mixed strong needs preserve the authored same-level ordering;
7. full CI and the disposable production-copy causal-resolution gate are green.

Evidence:
- PR #24 merge `e1e6d79479fa4d2ae837c395ec3b2fdb7391dc8f`;
- CI #451 `31698384623` SUCCESS;
- Causal Need Resolution v2 Acceptance #12 `31698384587` SUCCESS (existing production-copy harness reused as the compatibility gate);
- release `ab60e3d1f95100324bcaa638299eef1ba32e5036`;
- Deploy #150 `31698521410` SUCCESS.

No schema change, inventory system, new scoring system, or unrelated world expansion was introduced.
