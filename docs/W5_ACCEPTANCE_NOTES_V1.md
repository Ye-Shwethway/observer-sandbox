# W5 Acceptance Notes v1

Status: **PRE-MERGE CHECKLIST**

W5 v1 is intentionally testable without a second production character by using temporary database fixtures in automated tests. These fixtures are not canonical characters and never enter production state.

Required proof:
- direct communication event persists sender and intended-recipient participation;
- recipient-scoped W0 communication stimulus links back to the authoritative event;
- co-located intended recipient receives a direct exposure;
- non-co-located intended recipient receives no exposure;
- unrelated co-located character does not receive targeted exposure;
- non-character or self-recipient misuse fails closed;
- Character Memory, mental cycles/episodes/artifacts, relationship state, and action authority are untouched;
- no Darian-specific identity or behavior exists in the W5 implementation;
- existing schema remains sufficient unless CI/runtime evidence proves otherwise.

Live character-to-character social behavior is explicitly deferred. W5 completion establishes the external communication boundary required by later Perception and Mind layers; it does not claim dialogue intelligence.
