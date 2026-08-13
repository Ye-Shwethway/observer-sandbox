# Training Progression Mutation Gates

Status: ACTIVE DESIGN CONTRACT

Raw attribute mutation is **not authorized** until the progression preview stack is proven end-to-end.

Required order:
1. Adaptation Curve v1 — current-level / ceiling difficulty, read-only.
2. Stimulus Saturation / Diminishing Returns v1 — repeated/recent eligible stimulus reduces marginal yield.
3. Recovery Realization v1 — stimulus becomes adaptation only after explicit recovery/time conditions.
4. Detraining / Prolonged-Untrained Decay v1 — prolonged absence of relevant training can produce bounded regression evidence.
5. Adaptation Preview v1 — compose all factors into a deterministic projected delta without mutating raw stats.
6. Stat Mutation Gate v1 — only after all prior gates are accepted; apply tiny audited decimal raw-stat updates.

Core invariant:
`stimulus -> adaptation potential -> recovery realization -> diminishing returns / ceiling difficulty -> previewed delta -> mutation only after gate authorization`.

Regression is a separate path:
`elapsed untrained time -> detraining eligibility -> decay curve -> previewed negative delta -> mutation only after gate authorization`.

Special modifiers must remain abstract simulation modifiers (for example adaptation-rate, effective-ceiling, or recovery multipliers). They must not be implemented as real-world drug dosing or medical guidance.

Body measurements/composition remain a separate grading/progression family unless explicitly modeled later.
