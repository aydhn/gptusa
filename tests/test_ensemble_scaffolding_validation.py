import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_scaffolding_validation import validate_no_unsafe_ensemble_scaffolding_fields

def test_val():
    res = validate_no_unsafe_ensemble_scaffolding_fields({})
    assert res.valid is True
