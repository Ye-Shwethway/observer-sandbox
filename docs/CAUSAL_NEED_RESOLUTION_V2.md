# Causal Need Resolution v3

Status: CANDIDATE — exemplar + batch expansion

## Proven predecessor

v1 fixed repeated hunger inspection by adding real edible provisions and causal hunger routing. v2 extended the same deterministic pattern to thirst and was subsequently Creator live-verified.

## v3 goal

Close the current physiological recovery family before expanding more simulation systems. The authored priority order remains authoritative:

`sleepiness -> energy -> thirst -> hunger -> cleanliness`

Critical needs still outrank strong needs.

## Exemplar-first development pattern

### Exemplar — Energy

Energy proves the missing directionality invariant. Hunger/thirst/sleepiness are high-is-bad and require a reducing effect; energy is low-is-bad and requires an increasing effect.

A recovery option is causal only when its direct authored effect or intrinsic per-hour action effect moves the active need toward health. For strong low energy, `rest` is therefore a valid local resolver because its intrinsic effect raises energy. Discretionary training is hidden until the active need clears.

### Batch expansion — Sleepiness + Cleanliness

Once direction-aware evaluation is established by Energy, equivalent remaining needs use the same resolver engine in the same branch/PR:

- strong sleepiness -> local `rest` or `sleep` when causally available;
- critical sleepiness -> `sleep` only, routing toward a sleep-capable object when needed;
- poor cleanliness -> `shower`, routing toward the Master Bathroom when needed;
- thirst/hunger keep their accepted `drink`/`eat` behavior unchanged.

Both direct object effects and intrinsic per-hour action effects are valid causal evidence. Resolver selection never invents a second priority score: `decision_signals.needs_attention` remains authoritative.

## Acceptance contract

One development batch must prove:

1. Energy exemplar: low energy exposes only causal recovery and materially increases energy.
2. Strong sleepiness suppresses discretionary training; critical sleepiness routes toward Bed rather than accepting generic rest.
3. Poor cleanliness routes toward Shower and local showering clears the strong condition.
4. Existing hunger/thirst deterministic behavior remains green.
5. Mixed strong needs preserve the authored same-level ordering.
6. Full CI is green.
7. Candidate code passes the existing disposable production-copy causal-resolution gate before merge/deploy.

No schema change, inventory system, new scoring system, or unrelated world expansion is part of v3.
