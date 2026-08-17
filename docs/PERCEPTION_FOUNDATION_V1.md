# Perception Foundation v1

Status: **IMPLEMENTATION / ACCEPTANCE CANDIDATE**

## Purpose

Close the minimum architectural handoff between W0 Character Exposure and the Intelligent Mind Engine without inventing a second world-input store or prematurely implementing attention, appraisal, belief, memory encoding, social cognition, intention, or planning.

This slice exists because the canonical W0 contract explicitly stops at exposure while the Mind Engine already reserves a `perception` input socket.

Canonical chain:

`world/event truth -> W0 stimulus -> actual character exposure -> actor-relative perception input -> later appraisal/Mind -> later selective memory/intention/plan -> action proposal -> deterministic action authority`

Hard separation:

`exposure != perception input != understanding != belief != appraisal != memory != thought != intention/plan != action authority`

## Audit finding

Repository audit at the W5 production checkpoint found:

- W0 persists `world_stimuli`, explicit scopes, and `character_exposures`;
- W0 documentation says `W0 stops at exposure` and defines a future Perception handoff;
- the Intelligent Mind Engine contract already reserves `perception` as a bounded input socket;
- normal cognition context did not read `character_exposures` or expose an equivalent actor-relative perception key;
- no existing source module, schema, test surface, or canonical document implemented a separate Perception runtime under another name.

Therefore the gap is real and should be closed directly rather than bypassed or duplicated.

## Minimum design

Perception Foundation v1 is a **deterministic bounded read projection over existing W0 exposure truth**.

It does not add a persistence table or schema migration.

For one character and one current simulation time it selects only:

- exposure rows owned by that character;
- exposure status `exposed`;
- exposure simulation time not later than the current decision time;
- a bounded recent set.

It joins each exposure back to its authoritative W0 stimulus and emits a provenance-preserving actor-relative input containing:

- `exposure_id`;
- `stimulus_id`;
- stimulus routing category;
- actual exposure channel;
- bounded subject;
- producer-owned world payload;
- source/provenance links;
- exposure simulation time;
- external stimulus salience;
- optional producer-authored attention hint;
- stimulus/exposure provenance metadata.

The projection mode is:

`exposure_projection_v1`

This name is intentional. The slice proves that represented external information reached this actor and can now enter the Mind input boundary. It does **not** claim semantic comprehension or psychological interpretation.

## Cognition integration

Normal autonomous cognition already uses `MemoryAwareDecisionProvider` as the actor-context layer above the shared deterministic ModelDecisionProvider.

Perception Foundation v1 adds the bounded projection there as:

`state["perception"]`

before the same cognition call receives currently recallable Memory.

This preserves the conceptual order:

`present state + actor-relative perception + recallable memory + other represented context -> cognition proposal`

The existing Cognition Context snapshot mechanism will retain the same `perception` key because compact prompt shaping does not remove it.

## Authority rules

Perception Foundation v1 may not:

- create or alter world stimuli;
- fabricate exposure;
- infer exposure from mere stimulus eligibility;
- convert global active stimuli directly into character knowledge;
- assert that an actor understood, believed, agreed with, cared about, or correctly interpreted the content;
- create Character Memory rows;
- create Mental Cycles, Episodes, or Artifacts;
- create appraisal, concern, intention, plan, social inference, or relationship change;
- grant actions, topology, possession, device access, resources, or capabilities;
- mutate world state.

W0 remains authoritative for external stimulus/exposure provenance. Later Mind phases own interpretation and mental state. Deterministic action runtime remains sole execution authority.

## Boundedness

Default cognition projection is limited to the most recent 8 valid exposure records.

The API hard-bounds requested retrieval to 50 records.

This is context protection, not a psychological working-memory model. Attention and working-memory capacity belong to later Mind work.

## Attention hint semantics

Existing W0 `attention_hint` may be carried through unchanged because it is producer-authored exposure metadata.

It is not:

- guaranteed attention;
- personal relevance;
- appraisal priority;
- emotional arousal;
- memory salience.

MIND-F3 may later combine such external hints with character state and traits when real attention/appraisal runtime exists.

## Communication alignment

W5 direct communication now has a complete minimum external-to-Mind path:

`utterance event -> communication stimulus -> represented delivery/heard exposure -> Perception Foundation projection -> later MIND-F6 social interpretation`

This does not activate live dialogue or social response behavior by itself.

The second-production-character gate remains unchanged.

## Media / other producer alignment

The same projection consumes exposure from any W0 producer without producer-specific cognition code:

- environment/weather exposure;
- obligation notices;
- financial notices;
- information/media consumption exposure;
- communication exposure;
- future social/system exposure.

Producer-specific eligibility and exposure rules remain with those producers. Perception does not recreate them.

## Schema decision

**No schema migration.**

Reason:

The minimum handoff contains no new durable truth. It is a bounded actor-relative view derived from already-persisted W0 exposure plus stimulus provenance.

A future richer perception subsystem may justify durable perception records only when it needs represented interpretation states that cannot be reconstructed from exposure. That is not required for this slice.

## Acceptance

Perception Foundation v1 is accepted when automated tests prove:

1. actor-owned valid exposure projects to the perception socket with stimulus payload and provenance;
2. future exposure is not leaked into an earlier cognition time;
3. invalidated exposure is excluded;
4. projection creates no world event, Character Memory, Mental Cycle, Mental Episode, or Mental Artifact;
5. normal `MemoryAwareDecisionProvider` cognition context includes the bounded `perception` socket;
6. existing action authority and runtime behavior remain unchanged apart from newly available represented context;
7. full repository CI remains green;
8. production deploy/health remains green.

## Explicitly deferred

This slice does not implement:

- perceptual ambiguity resolution;
- semantic understanding;
- belief formation;
- attention allocation;
- appraisal or active concerns;
- emotion/affect;
- selective memory encoding;
- Mental Episode generation;
- intention/planning;
- social inference or reply generation;
- relationship adaptation;
- additional production characters.

Those remain in the canonical Mind sequence.

## Next architectural checkpoint

After this foundation is production-green, the external-input path needed by the canonical minimum world-input sequence is closed sufficiently to begin **MIND-F2 — Mental Episode Runtime**.

MIND-F2 must consume the existing `perception` socket rather than reading global W0 stimulus tables directly.
