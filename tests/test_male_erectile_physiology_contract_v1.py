from __future__ import annotations

import copy

import pytest

from observer_sandbox.db import connect
from observer_sandbox.profile_seed import ProfileSeedError, load_seed, validate_seed
from observer_sandbox.runtime import initialize


def _canonical_seed():
    return load_seed("config/characters/darian.canonical.json")


def test_darian_canonical_has_required_erectile_physiology(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        seed = _canonical_seed()
        validate_seed(conn, seed)
        values = seed["values"]
        assert values["sexual_anatomy.baseline_erectile_function"]["value"] == 95.0
        assert values["sexual_anatomy.erection_firmness_cap"]["value"] == 98.0


def test_male_seed_missing_erectile_baseline_fails_closed(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    seed = copy.deepcopy(_canonical_seed())
    del seed["values"]["sexual_anatomy.baseline_erectile_function"]
    with connect(db) as conn:
        with pytest.raises(ProfileSeedError, match="Male canonical profiles require"):
            validate_seed(conn, seed)


def test_male_baseline_cannot_exceed_cap(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    seed = copy.deepcopy(_canonical_seed())
    seed["values"]["sexual_anatomy.baseline_erectile_function"]["value"] = 99.0
    seed["values"]["sexual_anatomy.erection_firmness_cap"]["value"] = 98.0
    with connect(db) as conn:
        with pytest.raises(ProfileSeedError, match="cannot exceed"):
            validate_seed(conn, seed)


def test_non_male_seed_does_not_require_male_specific_fields(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    seed = copy.deepcopy(_canonical_seed())
    seed["values"]["identity.sex"]["value"] = "female"
    for field in (
        "sexual_anatomy.penis_length_in",
        "sexual_anatomy.penis_girth_in",
        "genetics.penis_length_in",
        "genetics.penis_girth_in",
        "sexual_anatomy.baseline_erectile_function",
        "sexual_anatomy.erection_firmness_cap",
    ):
        seed["values"].pop(field, None)
    with connect(db) as conn:
        validate_seed(conn, seed)
