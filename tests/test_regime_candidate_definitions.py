import pytest
from usa_signal_bot.regime_classification.feature_engineering.regime_candidate_definitions import (
    build_default_regime_candidate_definitions,
    validate_regime_candidate_definitions
)

def test_build_default_regime_candidate_definitions():
    defs = build_default_regime_candidate_definitions()
    assert len(defs) > 0
    errors = validate_regime_candidate_definitions(defs)
    assert len(errors) == 0
