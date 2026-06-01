import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_family_specs import build_default_ensemble_family_specs

def test_family_specs():
    specs = build_default_ensemble_family_specs()
    assert len(specs) > 0
    for s in specs:
        assert s.fitting_allowed_in_phase142 is False
        assert s.final_prediction_allowed_in_phase142 is False
        assert s.implementation_deferred_to_phase143 is True
