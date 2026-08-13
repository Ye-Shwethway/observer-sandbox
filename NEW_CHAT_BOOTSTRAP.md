# Observer Sandbox — New Chat Bootstrap

Status: **READY**
Last synchronized: 2026-08-14

## Startup / authority

Read `AGENTS.md`, then this file, then `ROADMAP.md`, then task-relevant contracts. Current Creator instruction and newer repository/runtime evidence override older chat memory.

## Development workflow

Default flow is now intentionally minimal:

`branch -> focused tests + CI -> merge -> automatic deploy when runtime-affecting -> read-only production check`

`docs/PRODUCTION_VALIDATION_AND_RELEASE_PROTOCOL.md` is the canonical minimal contract.

Production-copy validation is **optional**, not mandatory. Use it only for genuinely state-sensitive, migration-heavy, or otherwise high-risk changes that local tests/CI cannot cover well enough. Reuse the existing shared copy tooling when needed; do not invent new SSH/copy frameworks.

The old release-marker ceremony, deploy-trigger policy, and protocol-standardization acceptance gate are no longer part of normal development. Prefer small reversible changes and Git revert/rollback over layered release ceremony.

## Production baseline

- repo: `Ye-Shwethway/observer-sandbox`
- VPS: `/opt/observer-sandbox`
- DB: `/var/lib/observer-sandbox/observer.sqlite3`
- service: `observer-sandbox`
- schema: v4
- world revision: `thorne-estate-v3.2-training-environment`
- autonomy: enabled / normal
- latest verified speed: `5.0x` (read-only observation; re-read when exact cadence matters)
- cognition: Gemini `gemini-3.5-flash-lite`
- Telegram: connected

Latest simplified-flow deployment: **Deploy #160 `31730326878` SUCCESS** from main merge `89482e609995d8af84f33096cbc40fdd69c3ecc9`.

## Environment and training methods

Thorne Estate interior training environment v3.2 is deployed. Training Hall and Top-Class Home Gym expose the richer bounded equipment surface; exterior/Tahoe traversal remains deferred.

Training Method Semantics v1 is deployed. `config/training_methods.v1.json` provides authored method/family/workload-channel metadata. Equipment/method metadata describes workload evidence; it does not own attribute progression formulas.

## Progression state

### Strength

Strength progression is active and deployed. Free Weights remains the deliberate Strength stimulus source. Settlement is idempotent and action-boundary activated.

### Stamina

Stamina progression core + automatic activation are deployed. Pure-conditioning sources currently include:
- High-Speed Treadmill / `steady_state_cardio`
- Rowing Ergometer / `rowing_conditioning`
- Altitude Training Chamber / `altitude_conditioning`

Mixed movement/combat methods are not silently credited to Stamina.

### Agility

Agility Progression Core v1 and Automatic Activation v1 are now **merged and deployed**.

Agility uses the authored `speed_agility_drills` evidence surface with its own progression semantics. It is not a clone of Strength or Stamina. Production-copy acceptance before activation proved 20h eligibility behavior, idempotent settlement, and Strength/Stamina isolation. Deploy #160 carried the accepted Agility activation code to production.

## Core safety boundaries that remain

- Do not intentionally accelerate production for testing.
- Do not directly edit live profile/progression/world state as a test fixture.
- Keep LLM cognition proposal-only; deterministic engines own mutations.
- Creator controls remain typed/audited and follow `docs/CREATOR_CONTROL_POLICY.md`.
- Post-deploy verification is read-only unless a concrete live control change is explicitly requested.

## Expansion policy

Use exemplar-first only for genuinely new invariants. Once a pattern is proven, batch structurally equivalent follow-ons. Do not force separate acceptance/deploy ceremony for every equivalent item.

## Exact resume point

Resume physical progression expansion from the now-deployed **Agility** exemplar.

Next decide whether **Speed** is structurally equivalent enough to batch from the same `speed_agility_drills` evidence family, or whether it needs one small separate exemplar because its adaptation semantics differ materially. Keep the decision evidence-driven and minimal; do not recreate the removed release/validation process layers.
