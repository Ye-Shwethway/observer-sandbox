# Universal Character Engine Contract

Status: ACTIVE

## Purpose

Observer Sandbox uses Darian Thorne as the first richly specified exemplar, not as the identity baked into universe rules. Every reusable simulation, cognition, progression, physiology, action, observer and control engine must operate on actor/entity ids and domain data so the same engine can later serve any compatible character without copying or rewriting engine logic.

## Boundary

Character-specific content is allowed and expected:
- canonical profile facts;
- authored personality/routine/autonomy policy;
- runtime-default content;
- character-specific preferences, habits, skills and history;
- named convenience UI aliases such as `/darian`;
- initial bootstrap fixtures such as the current Thorne Estate + Darian seed.

Universal engine logic must not depend on a named character identity. In particular, reusable engine/control/query paths must not silently default to `char_darian`, load Darian's authored policy for another actor, or use Darian-specific thresholds merely because Darian is the current production exemplar.

## Actor selection

Runtime actor selection follows this order:
1. an explicit valid `actor_id` supplied by the caller;
2. a valid configured universe `default_actor_id`;
3. the sole existing character when the universe contains exactly one character.

If multiple characters exist and there is no valid configured default, an implicit actor lookup must fail closed and require an explicit actor id. It must never guess Darian or the first row returned by SQLite.

The current single-character production universe may therefore continue to behave exactly as before while removing named-character assumptions from reusable APIs.

## Character configuration

Character-specific files are resolved through the character configuration registry rather than hard-coded paths in engines. The registry may point to:
- canonical profile content;
- runtime defaults;
- authored autonomy/cognition policy;
- future character-scoped configuration that is genuinely content rather than universal rule logic.

A model decision provider for actor A must load actor A's registered policy. If no policy is registered, it must fail explicitly rather than silently fall back to Darian's policy.

## Universal progression rule

Progression engines must follow the reusable form:

`actor_id + authoritative current field value + eligible event/action evidence + domain policy + recovery/context + limits -> deterministic settlement + history/event evidence`

Darian's current values, genetics and training history are exemplar inputs to that rule. They are not progression constants.

Attribute-specific or domain-specific policies are allowed where physiology differs. Character-specific progression code branches are not.

When a new progression family is introduced, prefer:
- one bounded exemplar to prove a genuinely new causal invariant;
- a shared/policy-driven engine contract;
- batch activation for structurally equivalent fields after the exemplar passes.

Where practical, regression tests for universal engines should include at least one synthetic non-Darian actor so identity leakage is caught before additional production characters are introduced.

## Global versus actor-scoped controls

Universe-global controls such as simulation pause and speed apply to the universe. Actor-scoped autonomy/cognition state remains per actor.

A global resume must wake every enabled idle actor that reaches a decision boundary; it must not wake only the default/exemplar actor. Presentation or compatibility readbacks may project one configured default actor, but that projection is not the underlying source of truth.

## Architecture relationship

This contract preserves the canonical runtime expression:

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

The actor slot is generic. Character identity enters through profile/configuration/state data, not through named branches inside the runtime engine.

## Acceptance boundary

A universalization change is acceptable when:
- reusable runtime/cognition/control APIs no longer require a Darian literal as their implicit identity;
- policy lookup is character-registry driven;
- ambiguous multi-character implicit selection fails closed;
- existing single-character Darian behavior remains compatible;
- global controls remain global;
- a synthetic non-Darian regression proves that Darian policy is not silently reused;
- no schema-v5 migration is introduced solely for this contract.
