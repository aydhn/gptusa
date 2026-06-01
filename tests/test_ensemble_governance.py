import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_governance import build_ensemble_governance_result

def test_build_gov():
    gov = build_ensemble_governance_result([], [], [])
    assert gov.governance_passed is True
    assert gov.live_use_allowed is False
