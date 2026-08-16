# Environment / Weather Foundation v1 — Acceptance

W1 acceptance is evidence-based and intentionally narrow.

Required evidence:
- global schema migration installs environment schema v1 idempotently;
- a fresh initialized runtime contains no fabricated environment state;
- Estate-scoped environment truth resolves through represented containment;
- a more-specific descendant state overrides an ancestor state without rewriting history;
- W0 publication scopes direct ambient stimuli only to locations explicitly authored as outdoor;
- indoor locations cannot receive direct ambient exposure through W1;
- outdoor exposure is recorded through the W0 exposure table with source provenance;
- exposure does not create events, character memories or Mind cycles;
- the same APIs work for a second character without identity-specific branches;
- validation rejects unsupported vocabulary and invalid numeric ranges;
- replacement environment state supersedes prior same-scope state and retires the prior direct-ambient W0 stimulus;
- existing autonomy/action behavior remains unchanged.

The full repository CI remains the final regression checkpoint before promotion from `test` to `main`.
