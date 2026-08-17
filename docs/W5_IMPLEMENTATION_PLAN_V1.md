# W5 Implementation Plan v1

Status: **ACTIVE / BOUNDED FOUNDATION RUN**

## Goal

Complete the minimum communication world-input foundation without seeding another production character and without implementing social intelligence before the Mind Engine layers that own interpretation and response.

## Slice A — Direct Communication Truth + Exposure

Implement now:
- generic direct utterance API;
- authoritative `communication_utterance` event with sender and intended-recipient participants;
- recipient-scoped W0 `communication` stimulus using the `direct` channel;
- deterministic co-location delivery rule for intended recipients;
- W0 exposure only for recipients who are actually co-located at the utterance boundary;
- generic fixture-based acceptance tests;
- no Memory, Mind, relationship, or action mutation.

Reuse:
- `events` / `event_participants`;
- dynamic `located_at` runtime;
- `world_stimuli` / `world_stimulus_scopes`;
- `character_exposures`.

No schema migration is expected for Slice A.

## Slice B — Contract closure / device readiness

Do not prebuild a phone ecosystem. After Slice A is green, audit whether any additional generic delivery state is genuinely required for future asynchronous/device communication. Add only a minimum reusable socket if direct event + W0 provenance cannot represent the required distinction.

Potential future flow:

`message truth -> represented endpoint/device delivery -> read/access boundary -> W0 device exposure`

This remains deferred until a concrete represented endpoint or consumer requires it.

## Production activation boundary

There is currently no second canonical production character. Therefore:
- do not fabricate a production conversation;
- do not seed a test NPC into production;
- do not claim natural social acceptance from fixture tests;
- keep W5 production behavior dormant unless a legitimate represented sender/recipient pair exists later.

Fixture tests prove architecture/runtime correctness only.

## Post-W5 foundation sequence

After W5 minimum closure:
1. Perception-gap audit between W0 exposure and Mind inputs;
2. minimum Perception Runtime bridge if the gap is confirmed;
3. MIND-F2 Mental Episode Runtime;
4. MIND-F3 Attention / Appraisal / Active Concerns;
5. MIND-F4 Intention Foundation;
6. MIND-F5 Planning;
7. MIND-F6 Social Cognition / Communication foundation behavior;
8. MIND-F7 Relationship Adaptation;
9. Foundation Completion Review v2;
10. only then propose the next real character seed and run live multi-character acceptance.

## Acceptance boundary

W5 v1 may be marked minimum-complete when:
- the canonical communication contract is documented;
- direct utterance truth and targeted exposure run through generic existing stores;
- fixture acceptance proves co-location delivery and non-delivery boundaries;
- no character identity controls behavior;
- no direct Memory/Mind/relationship/action mutation occurs;
- CI and production deployment are healthy;
- continuity docs clearly state that live social behavior remains unproven until a later real second-character seed.
