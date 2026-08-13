# Cross-domain production-copy gate: preserve Stamina compatibility, then validate Agility exemplar.
from validate_stamina_conditioning_source_batch_v1_base import main as stamina_main
from validate_agility_progression_exemplar_v1 import main as agility_main


def main() -> int:
    assert stamina_main() == 0
    assert agility_main() == 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
