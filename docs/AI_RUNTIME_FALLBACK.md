# AI Runtime Cognition Fallback v1

Status: ACTIVE / AUTHORIZED

## Intent

Keep autonomous cognition available across temporary provider/model failures without masking deterministic simulation or decision-validation bugs.

## Runtime contract

Each character/role may have:

- one ordinary primary binding resolved through the existing AI binding layer; and
- at most one tested fallback provider/model stored as runtime control configuration.

The primary binding remains canonical. Fallback use is per decision call and never rewrites the saved primary binding.

## Trigger boundary

Fallback MAY run only when the primary provider/model invocation itself fails, including credential/configuration unavailability, provider HTTP failures, quota/rate limits, model/endpoint unavailability, timeout/network failures, request-limit failures, or an unusable provider response before deterministic decision validation.

Fallback MUST NOT run after a provider has returned a decision and deterministic runtime validation rejects it. Examples that must remain ordinary decision errors:

- unavailable action;
- invalid action/target pair;
- illegal duration;
- training-load or other deterministic runtime constraints.

This boundary prevents provider failover from hiding simulation/runtime bugs.

## Selection and activation

Fallback selection follows the same Creator safety pattern as primary model selection:

`provider -> fetch catalog -> select model -> real Test Model probe -> Save Fallback`

A fallback candidate cannot be saved until its real inference probe succeeds. Catalog success alone is not model-health proof.

Saving a fallback may enable that provider for runtime use, but it does not change the primary cognition binding or world/profile/progression state.

## Failure behavior

v1 performs one primary attempt and, after an eligible provider-layer failure, one configured fallback attempt. It does not create a multi-provider chain, circuit breaker, health score, or silent permanent failover.

If both primary and fallback fail, the combined provider failure returns to the existing autonomy retry/backoff path.

## Observability

A successful fallback records bounded runtime metadata:

- time used;
- primary provider/model;
- fallback provider/model;
- bounded primary error detail.

Credential values are never stored in fallback metadata or Telegram output.

## Non-goals

- automatic permanent rebinding;
- fallback on deterministic validation errors;
- ordered fallback chains beyond one fallback;
- provider health scoring/circuit breakers;
- Telegram API-key editing;
- schema v5.
