import inspect

from observer_sandbox.structured_ai import generate_structured


def test_structured_generation_has_separate_bounded_timeout():
    timeout = inspect.signature(generate_structured).parameters["timeout"].default
    assert timeout == 120.0
