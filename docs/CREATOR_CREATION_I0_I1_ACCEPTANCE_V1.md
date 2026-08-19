# Creator Creation I0/I1 Acceptance v1

Status: ACCEPTANCE CONTRACT
Date: 2026-08-19

## Slice

Minimum implementation before isolated staging persistence:
- I0 — generic Creator authority precedence;
- I1 — universal creation proposal/socket foundation;
- Creator Creation AI settings role and Telegram AI Settings hierarchy.

## Required proof

1. Ordinary seed refresh cannot replace simulated live state or Creator-owned state.
2. Existing profile seed import uses the shared Creator precedence contract rather than a profile-only exception.
3. Character and Location use one proposal envelope and both target `sandbox` only.
4. Direct `canonical` target requests are rejected by the proposal validator.
5. Unregistered creation types are rejected rather than silently accepted.
6. Creator Creation AI has an independent provider/model binding from Character AI and News Generation AI.
7. Model selection remains test-before-save; capability probing cannot mutate the active binding.
8. Creator Settings exposes one `AI Settings` upper layer.
9. AI Settings exposes Character AI, News Generation AI and Creator Creation AI as separate roles.
10. Creator Creation AI text makes clear that the role can draft sandbox proposals only and has no canonical write authority.
11. No Creation Sandbox persistence, canonical creation, transmigration, new real character, or universe mutation is introduced in this slice.
12. No schema migration is required.

## Validation policy

Focused tests cover the new contracts during development. Because this is a code/runtime PR checkpoint, final repository CI remains the merge gate.
