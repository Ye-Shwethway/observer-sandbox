# W5 Communication Exposure Foundation v1

Status: **ACTIVE IMPLEMENTATION CONTRACT**

## Purpose

Close the final minimum World Input producer boundary before the first active Mind runtime by representing communication truth, delivery conditions, and actual actor exposure without prematurely implementing dialogue intelligence, social cognition, relationship adaptation, or a second production character.

W5 reuses the existing authoritative event log and W0 World Stimulus / Exposure Foundation. It does not create a parallel hidden conversation store when the existing contracts already represent the required truth and provenance.

Canonical chain:

`communication event truth -> communication stimulus availability -> recipient delivery/exposure -> future perception -> appraisal/social inference -> response intention -> utterance proposal -> action authority`

Hard separation:

`uttered/sent != delivered != heard/read != understood != believed != remembered != relationship change != response intention != response action`

## Current production-character constraint

Only one seeded production character currently exists. W5 v1 therefore does **not** claim natural production character-to-character behavior acceptance.

Architecture/runtime correctness is proved with generic temporary test fixtures containing two character entities. Those fixtures are test data only and are not a second canonical character seed.

Production social behavior activation remains deferred until the Foundation Completion Review authorizes the next real character seed.

## W5 v1 exemplar: direct utterance

The first runnable exemplar is direct speech because the runtime already has:
- authoritative simulation events and event participants;
- dynamic character locations;
- W0 `communication` stimulus type;
- W0 `direct` / `auditory` compatible channels;
- explicit character stimulus scopes;
- character exposure provenance.

Minimum direct-speech flow:

`represented sender speaks -> utterance event -> recipient-scoped W0 communication stimulus -> co-located intended recipient actually hears -> W0 character exposure`

The utterance event is authoritative communication truth. The W0 stimulus represents the externally available signal. The exposure records only that the signal reached the recipient boundary.

## Direct-speech delivery rule

For v1, an intended recipient hears a direct utterance only when:
- sender and recipient are represented character entities;
- both have a represented current location;
- their current locations are equal at the utterance boundary.

An intended recipient who is not co-located is still part of the utterance truth/targeting metadata but receives no exposure record.

W5 v1 does not model acoustic distance, walls, hearing impairment, interruption, language comprehension, attention, or overhearing. Those are future depth/perception concerns and must not be fabricated here.

## Persistence strategy

W5 v1 intentionally introduces **no new database schema**.

Use existing stores:
- `events` + `event_participants` for authoritative utterance truth and represented participants;
- `world_stimuli` + `world_stimulus_scopes` for communication signal availability;
- `character_exposures` for actual heard/read boundary evidence.

This keeps communication aligned with W0 and avoids duplicate delivery/exposure state.

## Device/message readiness

The W5 contract reserves the same pattern for later represented device communication:

`message truth -> represented endpoint/device delivery -> recipient access/read boundary -> W0 device communication exposure`

W5 v1 does not prebuild phones, inboxes, contacts, network simulation, batteries, or messaging UI. A later concrete consumer may add represented endpoints and delivery semantics while preserving this contract.

## Mind Engine handoff

W5 stops at exposure.

It must not:
- generate a reply;
- infer tone, intent, trustworthiness, insult, affection, threat, or social meaning;
- create a durable Character Memory merely because speech occurred;
- create a Mind episode/artifact;
- mutate relationship trust/warmth/attachment/tension;
- choose an action.

The Intelligent Mind Engine owns the later interpretation path. Target future flow remains:

`communication exposure -> perception -> memory/person-context retrieval -> appraisal/social inference -> mental episode -> response intention -> utterance/action proposal -> deterministic authority`

## Test and acceptance strategy

W5 v1 is accepted when generic fixture tests prove:
1. a direct utterance creates authoritative event truth with sender and intended recipients represented;
2. a recipient-scoped W0 communication stimulus is created with provenance back to the utterance event;
3. a co-located intended recipient receives exactly one direct exposure;
4. a non-co-located intended recipient receives no exposure;
5. unrelated characters do not receive the targeted communication;
6. invalid/non-character sender or recipient identities fail closed;
7. utterance creation does not create Character Memory, Mind artifacts/episodes, relationship mutation, or action authority;
8. the same APIs work with arbitrary fixture character IDs and contain no Darian-specific logic.

Production natural social behavior is explicitly **not** an acceptance criterion while a second canonical character does not exist.

## Sequence after W5

After W5 minimum closure:
1. audit whether a minimum Perception Runtime bridge is still missing between W0 exposure and Mind inputs;
2. implement that bridge if the audit confirms the gap;
3. proceed through the canonical Mind sequence: Mental Episode Runtime -> Attention/Appraisal/Active Concerns -> Intention -> Planning -> Social Cognition/Communication -> Relationship Adaptation;
4. perform Foundation Completion Review v2;
5. only after that review may the next real character seed be proposed.

## Non-goals

W5 v1 does not implement:
- autonomous dialogue generation;
- chatbot ping-pong;
- a conversation loop;
- a second production character;
- social appraisal or theory of mind;
- relationship adaptation;
- automatic memory encoding;
- phone/network ecosystems;
- broad acoustic simulation;
- omniscient communication context injection;
- action or world mutation authority from communication content.
