from __future__ import annotations

from observer_sandbox.skill_definitions import EXPECTED_ANCHORS, load_validated_skill_definitions


def main() -> None:
    registry = load_validated_skill_definitions()
    skills = registry["skills"]
    print("Skill Definition Format v1: VALID")
    print(f"registry_revision={registry['revision']}")
    print(f"skill_count={len(skills)}")
    print(f"skill_ids={','.join(sorted(skills))}")
    for skill_id in sorted(skills):
        definition = skills[skill_id]
        anchors = definition["proficiency_anchors"]
        applications = definition["applications"]
        methods = definition["learning_evidence"].get("practice_method_ids") or []
        assert tuple(anchors) == EXPECTED_ANCHORS
        print(
            f"skill={skill_id} applications={len(applications)} "
            f"anchors={','.join(anchors)} practice_methods={','.join(methods) or 'none'}"
        )


if __name__ == "__main__":
    main()
