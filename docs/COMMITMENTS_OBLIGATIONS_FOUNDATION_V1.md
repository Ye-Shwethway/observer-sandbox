# W2 Commitments / Obligations Foundation v1

Status: **CANONICAL FOUNDATION CONTRACT**

## Purpose

Represent factual future expectations before activating Mind intention or planning runtime.

W2 owns commitment/obligation truth such as appointments, promises, deadlines and scheduled responsibilities. It may publish explicit reminder/notice availability through the shared W0 World Stimulus / Exposure boundary, but it does not decide what a character notices, thinks, prioritizes, intends or does.

## Canonical separation

Preserve:

`commitment truth != reminder/notice stimulus != exposure != perception/interpretation != concern/intention/plan != action proposal != action authority`.

A commitment can exist without a reminder. A reminder can be available without being exposed. Exposure does not prove attention, understanding, memory, concern, intention or compliance.

## Authoritative truth

W2 persists generic character-owned commitment records with:

- stable commitment id;
- owning character;
- commitment type;
- title/details;
- start and/or due simulation time;
- optional represented target entity/person;
- optional represented target location;
- lifecycle status;
- flexibility/reschedulability classification;
- source/provenance;
- extensible metadata.

Initial commitment types:

- `appointment`
- `promise`
- `deadline`
- `scheduled_responsibility`

Initial lifecycle:

- `pending`
- `active`
- `completed`
- `cancelled`
- `missed`

Initial flexibility:

- `fixed`
- `flexible`
- `reschedulable`

These vocabularies are bounded foundation terms, not separate behavioral engines.

## W0 notice producer

A represented commitment may explicitly publish a W0 stimulus with:

- `stimulus_type = obligation`;
- source provenance linked to the commitment id;
- explicit character scope;
- bounded start/end simulation time;
- a compact payload containing represented commitment facts.

Foundation v1 uses the neutral W0 `other` channel for availability-only notices when no concrete delivery mechanism has been represented. This must not be interpreted as a magical calendar, phone, alarm or omniscient cognition channel.

Publishing a W0 notice does **not** record `character_exposure` automatically. A later concrete producer/consumer must prove delivery through its represented channel before exposure is recorded.

Terminal commitment states (`completed`, `cancelled`, `missed`) retire linked active W0 notices so stale obligation availability does not remain active.

## Devices, calendars and communication

Foundation v1 does not prebuild phones, calendars, alarms, communication endpoints or internet services.

Add those world elements only when a concrete reminder/delivery consumer needs possession, location, access or capability semantics. At that point the delivery path must still use W0 and preserve exposure proof.

## Mind Engine boundary

W2 does not create:

- mental cycles;
- mental episodes;
- concern artifacts;
- goals;
- intentions;
- plans;
- action proposals.

Later Mind runtime may consume perceived commitment-related information through bounded input sockets. W2 itself remains a world-side truth/producer domain.

## Memory boundary

A commitment or reminder is not automatically Character Memory. Selective memory encoding belongs to later perception/Mind/learning flows.

## Action authority

Commitments never grant movement topology, access, possession, resources, capabilities or executable actions. Fulfilling an obligation still requires normal deterministic action options and validation.

## Generic character rule

The schema/API is character-generic. No named character receives a special commitment policy, priority rule, schedule script or compliance behavior.

## Minimum runtime API

Foundation v1 supports:

- create/read/list commitment truth;
- validated lifecycle transitions;
- explicit W0 notice publication;
- terminal-state retirement of linked active notices.

It intentionally does not implement automatic reminder scheduling, recurring calendar rules, Mind prioritization or autonomous obligation-following behavior.

## Acceptance

W2 v1 is accepted when:

- commitment schema migration is idempotent and generic;
- appointment/promise/deadline/scheduled-responsibility truth can be represented with simulation time, targets, lifecycle, flexibility and provenance;
- an explicit commitment notice can publish a character-scoped W0 `obligation` stimulus;
- notice publication does not automatically create exposure, Memory or Mind state;
- terminal commitment lifecycle retires linked active notices;
- no calendar/device/communication world element is invented without a concrete consumer;
- no character-specific behavior, intention, planning or action-authority bypass is introduced.
