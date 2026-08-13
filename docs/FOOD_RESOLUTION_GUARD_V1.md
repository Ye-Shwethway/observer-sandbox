# Food Resolution Guard v1

Status: COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED / CREATOR LIVE BEHAVIOR VERIFICATION PENDING

## Incident

Production observation on simulated 2025-05-02 showed Darian at strong hunger repeatedly choosing `Inspect -> Supply Shelves` in Food Supply Storage. Inspection had no authored hunger-reducing effect, so passive drift made hunger worse. The unresolved need then lost behavioral priority and autonomy resumed training.

## Root cause

1. `Supply Shelves` was inspect-only and Food Supply Storage had no edible object.
2. Autonomy policy allowed a persistent physiological need to justify repetition without requiring the repeated action to causally improve that need.
3. Strong-needs guidance was soft cognition guidance; generic inspect/train options remained exposed even when a real recovery action should dominate.
4. The model's known action vocabulary could remain broader than the authoritative `action_options` set.

## Fix

### World affordance

Add `obj_thorne_estate_food_storage_provisions` / **Stored Food Provisions** to Food Supply Storage.

- capabilities: `inspect`, `eat`
- authored eat effects:
  - hunger `-50`
  - energy `+8`
  - thirst `+2`

`Supply Shelves` remains inspect-only. The shelf itself is not food.

World revision is `thorne-estate-v3.1-food-resolution`.

### Deterministic strong-hunger option shaping

When hunger is strong or critical under the character's current need policy, and no different critical physiological need competes:

1. If a local authored `eat` option reduces `needs.hunger`, expose only local hunger resolvers.
2. Otherwise find rooms containing authored hunger-reducing `eat` affordances and expose only shortest-path first-hop `move` options toward the nearest resolver room(s).
3. If no authored resolver or route exists, preserve the original options rather than deadlocking autonomy; the missing world data remains observable.

This v1 deliberately activates deterministic need shaping for **hunger only**. Other needs may use the same exemplar pattern later.

### Model vocabulary

The model's known action vocabulary is derived from the authoritative current `action_options` when any options exist. This closes the gap where a verb absent from the option set could still be emitted because it existed in the global action vocabulary.

### Repetition contract

A persistent physiological need no longer justifies repeating an inspect/use action merely because the need remains. Repetition is legitimate only when the action has an authored effect that improves the need or makes concrete causal movement toward an authored resolver.

## Acceptance and deployment evidence

- PR #22 merge `6117b4b8f08ae3afc8d0db6849a7aa061a34b51f`.
- Food Resolution Guard v1 Acceptance #4 run `31691041378` SUCCESS on a disposable production DB copy.
- Activity Semantics Batch 1 Acceptance #6 SUCCESS after the world-seed change.
- Full CI #435 run `31691041444` SUCCESS.
- release commit `0906d3c06961482fa6c327caf9cfd8e172e51d12`.
- Deploy Observer Sandbox #148 run `31691179483` SUCCESS.
- production readback: service active/healthy, schema v4, world revision `thorne-estate-v3.1-food-resolution`, Gemini cognition binding preserved, Telegram connected.

The acceptance reproduction used the observed strong-hunger state in Food Supply Storage and proved:

- Stored Food Provisions are seeded and edible;
- Supply Shelves remain inspect-only;
- strong-hunger cognition options contain only `Eat -> Stored Food Provisions` in that room;
- training/inspect cannot displace the unresolved hunger while the guard applies;
- eating materially lowers hunger below the strong threshold;
- no model call is required for the deterministic proof;
- the real production DB was unchanged during pre-merge acceptance.

At deployment readback Darian still had a pre-existing `inspect` action that had been planned before the new guard was live. Deployment deliberately preserves an already-pending action rather than cancelling it. The new guard applies at the next cognition/planning boundary after that action completes.
