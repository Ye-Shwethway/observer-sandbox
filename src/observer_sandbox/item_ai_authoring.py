from __future__ import annotations


DEFAULT_ITEM_AI_AUTHORING_INSTRUCTION = (
    "ITEM AUTHORING CONTRACT: produce a validator-ready proposal on the first attempt. "
    "Treat the schema as available structure, not a checklist of facts to invent. Populate a field or metric only when it is explicitly requested, directly supported by the Item description/specification, or a conservative ordinary inference. If support is weak or ambiguous, leave the nullable slot null. "
    "Use stable lowercase machine tokens for definition.key, definition.tags, symbolic units/labels, valuation_method and batch refs; keep human-readable wording in name and description. "
    "KIND/MOBILITY RULE: fixture Items are structurally fixed and therefore must use mobility='fixed'. Use fixture only for installed/anchored/static world objects; ordinary portable gear, tools, containers and consumables must not be mislabeled as fixtures merely because they can be placed somewhere. "
    "Keep module semantics and capabilities aligned: nutrition requires a genuinely stackable consumable and capability 'eat'; container requires capability 'store'; resistance_training requires capability 'train'. Do not add eat/store/train when the corresponding module is absent. "
    "STACK RULE: ordinary single objects are non-stackable unique Items with no stack module. Only genuinely fungible/countable grouped goods are stackable; then stack canonical_unit, initial_quantity and instance mode/quantity/unit must agree exactly. "
    "NUTRITION BASIS RULE: nutrition.basis_quantity is the number of stack canonical units covered by the listed nutrition facts, not the Item's physical mass or serving weight. For discrete units such as bar, bottle, can, packet or piece, use basis_quantity=1 when the nutrition values describe one unit unless there is explicit evidence for a multi-unit basis. Never copy a physical mass such as 50 g into basis_quantity when nutrition.unit is 'bar'. The nutrition basis must not exceed the represented initial stack quantity. "
    "METRIC EVIDENCE RULE: do not fill every available metric slot. Use dedicated container.capacity_volume and resistance_training.resistance_load rather than duplicating them in generic metrics. Numeric water_resistance_depth requires explicit immersion/submersion evidence such as a stated depth, waterproof/submersible rating or suitable IP rating; words such as 'water-resistant', 'rugged' or 'outdoor' alone do not justify a depth value. "
    "METRIC COHERENCE RULE: interacting numeric facts must describe one physically plausible Item. In particular, power, runtime and energy_capacity must be mutually plausible; do not independently guess all three. If one cannot be supported consistently, leave it null. Charge time, stored energy and charging/output power must not imply obviously contradictory behavior. For ordinary lighting equipment, luminous_flux and power together imply luminous efficacy, so keep the ratio plausible for real consumer hardware; never pair a high lumen value with unrealistically tiny electrical power merely to fill both slots. If power is uncertain, prefer null over a speculative value. "
    "Keep mass, external dimensions, container capacity, payload, performance and other represented facts mutually plausible for the same object. Prefer fewer defensible facts over many speculative ones. "
    "Do not author derived grades, grading thresholds, evaluator ids, reference profiles or an overall grade; grading is deterministic downstream. "
)


__all__ = ["DEFAULT_ITEM_AI_AUTHORING_INSTRUCTION"]
