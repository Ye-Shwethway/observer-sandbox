# Creator Character Profile Editing & Grade Targeting v1

Status: **ACTIVE IMPLEMENTATION CONTRACT**

## Purpose

Give the Creator an explicit, character-generic control surface for correcting or deliberately retargeting represented character profile/skill facts without turning Telegram, grading, or an LLM into a second source of truth.

This slice is intentionally implemented before MIND-F2 so future Mental Episodes, appraisals, intentions and plans are not built on profile facts the Creator cannot safely correct and reconcile.

## Core authority rule

The Creator may edit represented character seed/profile statistics and skill baselines/current represented scores through this explicit control contract.

The control is **not** an ordinary simulated character action. It is Creator authority over represented canon/state and must be audit-visible.

Canonical separation:

`Creator requested edit -> validated authoritative raw value mutation -> dependent derived state/grade reconciliation -> self-knowledge/context reconciliation -> future cognition`

Never use:

`Creator requested grade -> persisted grade label as truth`.

Raw represented values remain authoritative. Grades remain derived evaluations under named grading schemes.

## Existing profile authority remains meaningful

Profile fields already declare `canonical`, `static`, `derived`, or `simulated` modes and engine authorities. Creator editing does not erase that architecture.

The editor therefore records what kind of mutation occurred:

- `canonical_correction` — the represented fact should canonically be the new value; this is not an in-world change event.
- `creator_override` — the Creator deliberately replaces a currently represented value, including an engine-owned/progression value when explicitly chosen.

A Creator override is allowed, but the affected domain must be re-anchored so the owning engine continues from the new represented value rather than silently restoring a stale baseline.

Derived values are not independent long-term authorities. When a derived field has an implemented deterministic source, prefer editing its authoritative inputs and recomputing it. If a field cannot be safely written independently, the preview must explain the dependency rather than fabricating inconsistent state.

## Universal edit surface

The runtime/UI must be character-generic. Character identity must never select a different editor algorithm.

V1 supports represented numeric/text/boolean/JSON/date profile fields through schema-aware adapters and represented skill scores through a skill adapter.

The Creator should be able to edit all represented seed/profile facts for which the repository has a writable canonical store. Guards exist to preserve structural validity, not to prevent legitimate Creator authority.

### Validity guards

At minimum:

- field must exist in the canonical profile ontology or supported collection adapter;
- value must match the declared data type;
- monotonic RAPS/Skill scores must remain within their canonical 0..100 domain;
- explicit cross-field invariants already enforced by the profile contract remain enforced (for example lower/upper or baseline/cap relationships);
- impossible writes to deterministic derived projections must fail with a clear dependency explanation;
- a mutation must be atomic: either the requested edit and its required reconciliation commit together or none of it commits.

Do not create arbitrary “realistic human” caps that are not canonical project rules merely to limit Creator editing.

## Individual field editing

Minimum flow:

`Character -> Profile/Skills -> field -> Edit -> proposed value -> preview -> Apply`

Preview must show:

- current raw value;
- proposed raw value;
- unit/type where applicable;
- current derived grade when gradeable;
- projected derived grade after the edit;
- mutation class (`canonical_correction` or `creator_override`);
- important dependent/reconciliation effects.

Apply must write the authoritative raw domain store and append audit/history provenance.

## Grading relationship

Existing grading remains read-only and dynamic:

`authoritative raw values -> named grading scheme -> field grade -> compatible section aggregate`

Changing a raw value therefore automatically changes its grade and any compatible section aggregate the next time grading is evaluated. No grade column or persisted grade authority is introduced.

Current monotonic bands used by the existing 0..100 RAPS and Skills schemes are:

- E: 0 <= value < 20
- D: 20 <= value < 40
- C: 40 <= value < 60
- B: 60 <= value < 75
- A: 75 <= value < 90
- S: 90 <= value <= 100

The wider E/D/C/B/A/S/SS/SSS/X/XX vocabulary remains canonical presentation vocabulary, but v1 inverse targeting may target only grades with an implemented numeric inverse domain in the selected grading scheme.

## Section-level grade targeting

The Creator may request a compatible section target such as:

`Physical Attributes -> Overall Grade B`

This is an **inverse grading operation**, not a grade mutation.

Canonical flow:

`target grade -> grading scheme target interval -> proposed eligible raw values -> aggregate verification -> preview -> atomic raw update -> ordinary read-time grading`

### V1 supported inverse families

V1 supports inverse targeting for monotonic 0..100 families where the target interval is deterministic:

- RAPS/Attributes sections whose aggregate is the mean of compatible `raps-100-proof-v1` fields;
- Skills sections/groups whose aggregate uses compatible `skill-proficiency-100-v1` scores when exposed by the editor.

Body grading remains read-time derived from ratios/reference ranges and composites. V1 permits individual body-input editing and automatic Body regrading, but does **not** bulk-invert Body composite grades until a canonical multi-variable inverse policy is explicitly designed. This avoids pretending one arbitrary body measurement vector uniquely represents a grade.

### Preserve-shape mode — default

Preserve the section's existing relative profile as much as possible while moving eligible values into a configuration that achieves the requested aggregate grade.

For a monotonic section:

1. compute current eligible values and their mean;
2. choose a deterministic target point inside the requested grade interval (default: interval midpoint, with a bounded epsilon below an exclusive upper threshold);
3. shift/scale values while preserving relative offsets as far as 0..100 and target-band constraints allow;
4. clamp only when required by the canonical domain;
5. make the smallest deterministic correction needed for the resulting aggregate to evaluate to the requested grade;
6. verify the existing grading engine returns the requested aggregate grade before preview/apply.

This keeps a character's relative strengths/weaknesses instead of flattening every field.

### Normalize mode

Set eligible fields toward one deterministic representative value in the requested interval and verify the resulting aggregate grade.

Normalize is explicit because it intentionally reduces intra-section variation.

### Preview and confirmation

A section-grade request must never silently mutate the profile.

Preview shows:

- target section and grading scheme;
- target grade and numeric interval;
- mode (`preserve_shape` or `normalize`);
- every raw field that will change: old -> proposed;
- projected individual grades;
- projected section aggregate value/grade;
- excluded/non-gradeable fields and why they are excluded.

Only an explicit Creator Apply action commits the proposal.

## Progression and baseline reconciliation

A direct Creator edit must not be undone by stale progression bookkeeping.

For an affected field/skill with active progression:

- update the represented current value in the canonical domain store;
- re-anchor any progression/change-observer baseline that would otherwise interpret the correction as ordinary earned progress or replay a stale notification;
- preserve unrelated historical progression evidence unless it directly encodes the superseded canonical fact;
- future progression continues from the corrected/overridden represented value under the normal owning engine.

A Creator edit should not emit a false “earned progression” notification merely because the numeric value changed through control authority. Creator audit/confirmation is the notification for the control action.

## Character self-knowledge and Memory reconciliation

A canonical correction must not create false autobiography.

Example: correcting a height value must not create an episodic memory equivalent to “I suddenly became this height.”

V1 reconciliation policy:

- do not wipe Character Memory;
- preserve unrelated episodic experiences;
- identify active semantic/self-knowledge records that explicitly derive from or contradict corrected profile facts when such records exist;
- supersede/retire only those stale records;
- ensure future cognition reads the new authoritative profile value;
- when a profile-derived semantic self-knowledge record is required by an existing consumer, regenerate/update it with provenance linking it to the Creator correction rather than inventing an in-world event;
- ordinary event memories remain historical truth unless their content is itself a profile-derived canonical assertion being corrected.

Current seed semantic memory may contain other knowledge kinds (for example spatial familiarity) and must not be touched merely because a profile field changed.

## Cognition and future Mind reconciliation

Cognition context is an observability snapshot, not durable character truth. New cognition wakes naturally rebuild from authoritative current profile/state and therefore must see the corrected values.

No historical Cognition Context snapshot is rewritten; it remains evidence of what a past model call actually received.

Before MIND-F2 is active, v1 only needs a generic future reconciliation hook/contract for Mind-owned records.

After Mind activation, a Creator profile correction may require targeted reconciliation of affected active mental artifacts. The future rule is:

- preserve historical episode records as historical represented mental activity;
- mark/retire only active artifacts whose premises are invalidated by the correction;
- never wipe the whole Mind because one profile fact changed;
- F3-F7 modules own their domain-specific reevaluation semantics.

## Auditability

Each applied edit or grade-target batch must be traceable with at least:

- character id;
- Creator/control source;
- mutation class;
- affected domain/field(s);
- old and new raw values;
- requested target grade/mode where applicable;
- simulation time and real/runtime timestamp where available;
- reason/note if supplied;
- reconciliation metadata.

Existing `character_profile_history` should be reused for scalar profile value history where suitable. Skills and cross-domain batches require equivalent audit metadata without pretending grade labels are authoritative state.

## Telegram / Creator UX direction

The surface is Creator-only and should extend the existing Character/Profile control UX rather than introducing a second profile browser.

Minimum actions:

- `Edit Value`
- `Set Section Grade` when the section has an invertible grading scheme
- preview
- `Apply`
- `Cancel`

Sensitive/intimate fields continue to obey existing owner/private presentation policy.

Buttons/navigation follow the canonical Telegram design rules already used by the project: edit-in-place where practical, Back for hierarchy navigation, Close to dismiss the surface, Cancel for the current edit operation.

## Non-goals for v1

Do not add:

- persisted grade columns/grade authority;
- whole-character cross-family overall-grade targeting;
- arbitrary inverse Body physique generation;
- LLM-selected raw profile values;
- automatic character-specific balancing;
- Darian-specific mutation rules;
- broad Memory reset;
- historical Cognition Context rewriting;
- fake in-world events for canonical corrections;
- F2 Mental Episode behavior.

## Acceptance

V1 is accepted when automated/disposable-state tests prove:

1. a Creator-authorized generic scalar profile field can be edited with schema/type validation and audit history;
2. a gradeable raw RAPS field edit is immediately reflected by the existing read-time field/section grade without persisted grade state;
3. a represented skill score can be explicitly edited and existing skill grading follows the new raw score;
4. Physical Attributes can be previewed and atomically retargeted to Grade B using preserve-shape mode, with the existing grading engine verifying the resulting aggregate;
5. normalize mode produces a valid requested monotonic target grade;
6. invalid field/type/range/cross-field proposals fail without partial mutation;
7. progression/change-notification baselines are re-anchored where necessary rather than reporting the Creator correction as earned progress;
8. unrelated Character Memory remains unchanged and stale profile-derived self-knowledge is reconciled only when present;
9. no historical Cognition Context is rewritten;
10. no Mental Cycle/Episode/Artifact is created in this slice;
11. implementation is character-generic and no named-character behavior is encoded;
12. production deployment can be verified without mutating Darian's live profile merely for acceptance.

## Next checkpoint

After this control foundation is production-green and continuity is synchronized, resume:

`MIND-F2 Mental Episode Runtime -> MIND-F3 -> F4 -> F5 -> F6 -> F7 -> Foundation Completion Review v2 -> next real production character seed`.
