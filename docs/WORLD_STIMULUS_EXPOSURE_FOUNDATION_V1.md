# World Stimulus / Exposure Foundation v1

Status: **CANONICAL WORLD-INPUT CONTRACT**

## Purpose

Create the minimum generic world-input substrate that can later feed the Intelligent Mind Engine without allowing world systems to directly script character thoughts, moods, plans, or behavior.

This contract sits between authoritative world facts/events and future perception/appraisal modules.

It is intentionally broader than weather. Weather, devices, media, money notices, obligations, direct communication, social events and future environmental signals should all be able to expose information through the same world-input boundary.

The foundation is socket-style: later systems add typed producers and channels without replacing this common contract.

## Mandatory Mind Engine alignment

This foundation MUST be read together with:

- `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
- `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
- `docs/HUMAN_MEMORY_DYNAMICS_V1.md`

Preserve the broader canonical chain:

`world/event truth -> stimulus availability -> character exposure -> perception/interpretation -> appraisal/thought -> memory/intention/plan -> action proposal -> action authority`

Hard separation:

`world fact != stimulus != exposure != perception != appraisal != thought != memory != action authority`

A weather record, bank balance, television program, phone notification or spoken utterance does not directly become a thought, emotion, memory or action.

## Why this layer exists

Without a shared world-input layer, future systems tend to bypass cognition in incompatible ways:

- weather might directly modify mood;
- money might directly add anxiety;
- media might appear in every character's prompt as omniscient knowledge;
- a message might become memory before the character ever receives or reads it;
- relationship logic might directly mutate trust from an utterance without interpretation.

This foundation prevents those shortcuts by representing how externally available facts become exposure candidates and then actual actor exposure.

## Core layers

### 1. Authoritative world fact/event

The source domain owns objective truth.

Examples:
- current weather state;
- an event that occurred;
- a financial balance or transaction;
- an appointment/deadline;
- a media item that was published;
- a phone message that was sent;
- a person speaking an utterance.

The stimulus layer may reference that source but does not replace it.

### 2. World stimulus

A `world_stimulus` is a bounded externally available signal that *could* reach one or more actors through a represented channel.

Examples:
- rain and cold air outdoors;
- an audible alarm;
- a television news segment;
- a phone notification;
- a direct spoken sentence;
- a bank alert;
- a calendar reminder;
- an observable injury or expression;
- a posted sign;
- an internet article available through a device/service.

A stimulus is not automatically perceived by every character.

### 3. Availability / scope

A stimulus may be limited by represented scope.

Initial scope vocabulary:
- `world` — globally available in the represented world, subject to a compatible channel;
- `location` — available within a represented location/container;
- `entity` — attached/originating from a represented entity/device/object/person;
- `character` — specifically targeted to a character;
- `audience` — targeted to an authored audience identifier or future group abstraction.

Scope is not action authority. A character still needs whatever represented physical/device/social conditions the producing subsystem requires.

### 4. Character exposure

A `character_exposure` records that a represented stimulus actually reached a character through a specific implemented channel at a simulation time.

Exposure means **the signal reached the actor's available perceptual/informational boundary**.

Exposure does not mean:
- the character understood it correctly;
- the character paid full attention;
- the character believed it;
- the character cared about it;
- the character stored it in durable memory;
- the character changed behavior.

Those belong to later perception/appraisal/memory/mind modules.

## Initial stimulus categories

The shared schema uses a small generic vocabulary:

- `environment` — weather, temperature, light, ambient conditions;
- `information` — media, signs, documents, internet content, notices;
- `communication` — utterances, messages, calls, alerts addressed through communication systems;
- `financial` — transaction/balance/bill/income-related externally surfaced information;
- `obligation` — appointment, deadline, commitment, task reminder, schedule signal;
- `social` — observable behavior/presence/expression/social situation not already represented as direct communication;
- `system` — represented world/system notification that is legitimately available to an actor;
- `other` — reserved extension category.

These are routing categories, not mental meanings.

## Initial channel vocabulary

Channels describe how the signal reaches the actor, not what the actor thinks about it:

- `visual`
- `auditory`
- `tactile`
- `environmental`
- `device`
- `media`
- `direct`
- `mixed`
- `other`

Future systems may add more precise channel metadata without creating parallel exposure stores.

## Devices and media expansion rule

Phone, television, radio, computer, internet access, smart-home devices and similar world elements are **represented world entities/resources**, not magical cognition channels.

When a world-input consumer genuinely requires one of these elements, expand the world model at that time using existing entity/location/resource/relationship contracts and then connect it to this stimulus/exposure layer.

Examples:

### Phone notification

`message/notification truth -> phone/device stimulus -> device belongs/is accessible to actor -> exposure -> later perception/appraisal`

The phone must be represented if the simulation needs its possession, location, battery, access or capabilities to matter.

### Television

`broadcast/media item -> TV/device output stimulus -> TV located in room -> actor present + compatible attention/action -> exposure`

A television program is not automatically known merely because a TV exists in the Estate.

### Internet

`published information item -> network/service availability -> accessible device/interface -> actor interaction/exposure -> later perception`

Do not model "the internet" as global character knowledge.

### Direct speech

`utterance event -> audible/direct stimulus -> recipient proximity/channel -> exposure -> later social perception/appraisal`

Communication later uses the same boundary rather than a separate hidden chatbot context.

## Generic data model

### `world_stimuli`

Represents externally available signals.

Conceptual fields:
- stable stimulus id;
- stimulus category/type;
- channel;
- short subject/summary;
- source type/id;
- optional source event/entity;
- payload JSON owned by the producing subsystem;
- salience 0..1 as external signal prominence, **not mental importance**;
- start/end simulation time;
- status;
- metadata/provenance.

### `world_stimulus_scopes`

Associates a stimulus with zero or more bounded availability scopes.

Conceptual fields:
- stimulus id;
- scope type;
- scope id;
- relation role;
- metadata.

A stimulus with no scope is not assumed omnipresent. Producers should explicitly provide scope unless the shared contract explicitly supports global availability.

### `character_exposures`

Records actual actor exposure.

Conceptual fields:
- exposure id;
- stimulus id;
- character id;
- simulation time;
- exposure channel;
- source location/entity when relevant;
- attention hint/strength when a producing subsystem can author it;
- status;
- metadata/provenance.

The exposure table is character-owned informational history but is not itself Character Memory.

## Salience and attention

World stimulus `salience` means externally noticeable/prominent signal strength.

It is not identical to:
- memory salience;
- emotional arousal;
- personal relevance;
- mental artifact priority;
- attention allocation.

Future perception/appraisal may combine world salience with character state, current action, sensory access, attention and individual traits.

Do not equate a loud/bright/prominent signal with guaranteed belief or emotional importance.

## Exposure eligibility

The shared API may answer bounded questions such as:

> Which active stimuli are potentially available to this actor at this represented location/time/channel?

Eligibility remains a query over represented facts. It does not automatically record exposure.

A producing/consumer subsystem records actual exposure only when its own represented rules prove that the signal reached the actor.

Examples:
- outdoor weather may expose an actor currently outdoors;
- a room television may expose an actor if the TV is on and the actor is in the compatible room/context;
- a targeted phone notification may become device exposure if the actor has access to the represented device;
- an utterance may expose a nearby recipient through direct/auditory channel.

The generic W0 foundation does not invent those domain-specific rules.

## Perception handoff

W0 stops at exposure.

Future perception should transform a bounded set of exposure records into actor-relative perceived information.

Target handoff:

```json
{
  "exposure_id": "...",
  "stimulus_id": "...",
  "channel": "device",
  "world_payload": {},
  "source_links": [],
  "exposed_at": "..."
}
```

Future perception/appraisal may add interpretation, confidence, attention and meaning, but must preserve links back to the objective stimulus/exposure provenance.

## Memory handoff

Exposure is not durable memory.

Possible future flow:

`exposure -> perception -> mental processing -> selective encoding/reinforcement`

A character may:
- be exposed and ignore it;
- perceive it but not retain it;
- misunderstand it;
- remember only the gist;
- later recall it through normal Character Memory dynamics.

W0 never inserts Character Memory rows merely because exposure occurred.

## Mind Engine handoff

Future Mind input should consume **perception-ready or perceived** actor-relative information, not the global world stimulus table.

The Mind Engine must not receive every active weather/media/message/financial record by default.

Bounded path:

`relevant authoritative state -> eligible stimulus -> actual exposure -> perception -> bounded Mind socket`

This keeps cognition from becoming omniscient and limits context growth.

## Authority / mutation rules

- Source world systems own their authoritative facts.
- W0 owns stimulus availability and exposure provenance.
- Perception owns actor-relative interpreted sensory/information state.
- Memory owns retained/recalled knowledge.
- Mind owns active internal interpretation/thought/artifacts.
- Deterministic action runtime owns executable action authority and world mutation.

No W0 API may grant:
- topology;
- possession;
- device access;
- money;
- action capability;
- relationship change;
- memory insertion;
- mental appraisal;
- action execution.

## World-system producer contract

Every future producer that feeds cognition through world inputs should document:

1. authoritative source truth;
2. what creates/updates the stimulus;
3. availability/scope rules;
4. what proves actual exposure;
5. what data is passed to perception;
6. what remains outside Mind authority;
7. how stale/expired stimuli are retired.

Examples include weather, media, economy, communications and obligations.

## Initial expansion sequence

After W0 foundation, preferred minimum consumer order is:

1. **W1 Environment / Weather Foundation**
   - weather/temperature/precipitation/wind/light/daylight facts;
   - outdoor/indoor exposure boundaries;
   - deterministic environmental affordance/comfort inputs where represented;
   - no direct mood modifier.

2. **W2 Commitments / Obligations Foundation**
   - appointments, deadlines, promises, scheduled obligations;
   - due/start times, flexibility and status;
   - reminders as stimuli/exposures;
   - no automatic intention/plan creation.

3. **W3 Money / Economy Minimum Foundation**
   - balances/resources, transactions, income/expense obligations, affordability;
   - financial alerts/notices through W0;
   - no direct anxiety or behavior modifier.

4. **W4 Information / Media Foundation**
   - information/media items, sources, publication/availability, credibility metadata;
   - device/media exposure through W0;
   - world knows != character knows.

5. **W5 Communication Exposure Foundation**
   - sender/recipient/channel/content/delivery/read-or-heard boundary;
   - utterances/messages become W0 stimuli and exposure records;
   - interpretation/response belongs to later Social Cognition.

Then the first **Mental Episode Runtime** can consume richer actor-relative inputs.

## Batch-by-pattern rule

Do not force W1-W5 into five oversized independent architectures if they share proven W0 patterns.

Use:

`W0 contract -> first producer exemplar -> batch structurally equivalent producers when clear`

Add world elements such as phones, televisions, network access, accounts, calendars or communication endpoints when a concrete producer/consumer needs them. Do not prebuild unused world complexity.

## Observability direction

Future Creator-facing observer surfaces may distinguish:
- World / Environment — objective facts;
- Exposure — what external signals actually reached a character;
- Memory — what was retained;
- Mind — what is mentally active/interpreted;
- Cognition Context — exact model injection.

W0 v1 does not require a Telegram Exposure browser yet, but persistence/query APIs must make one possible without redesign.

## Branch / development hygiene

Persistent repository branches are only:
- `main`
- `test`

Normal development uses `test` and promotes reviewed/validated work to `main`. Do not create per-slice `agent/*` branches unless a truly exceptional isolation need is explicitly approved. If an exceptional temporary branch is ever used, it must be deleted immediately after merge/closure.

## Non-goals

W0 does not implement:
- weather itself;
- phones/TV/internet merely for decoration;
- full media ecosystem;
- banking/economy simulation;
- communication dialogue;
- perception interpretation;
- emotion/appraisal;
- automatic memory encoding;
- thought generation;
- planning;
- relationship adaptation;
- omniscient world-to-prompt injection.

## Acceptance

W0 is accepted when:
- this contract is canonical and referenced by Mind/world development guidance;
- schema persists generic stimuli, scopes and character exposures;
- migration is idempotent and character-generic;
- API can create/query scoped active stimuli and record/read exposure without mutating Mind, Memory or world truth;
- exposure provenance links back to represented sources;
- source/category/channel vocabularies are bounded and validated;
- a second character can use the same schema/API without new behavior code;
- no direct mental or behavioral modifiers are introduced;
- current autonomy/action behavior remains unchanged.
