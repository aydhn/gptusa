import pytest
from usa_signal_bot.core.enums import CostSessionRegime
from usa_signal_bot.regime_costs.session_regime_cost import (
    classify_cost_session_regime, session_cost_multiplier,
    session_cost_warnings, session_regime_to_text
)

def test_session_regime_classification():
    assert classify_cost_session_regime("REGULAR") == CostSessionRegime.REGULAR
    assert classify_cost_session_regime("PREMARKET") == CostSessionRegime.PREMARKET
    assert classify_cost_session_regime("AFTER_HOURS") == CostSessionRegime.AFTER_HOURS
    assert classify_cost_session_regime("CLOSED") == CostSessionRegime.CLOSED
    assert classify_cost_session_regime("HOLIDAY") == CostSessionRegime.CLOSED
    assert classify_cost_session_regime(None) == CostSessionRegime.REGULAR

def test_session_multiplier():
    assert session_cost_multiplier(CostSessionRegime.REGULAR) == 1.0
    assert session_cost_multiplier(CostSessionRegime.PREMARKET) > 1.0
    assert session_cost_multiplier(CostSessionRegime.CLOSED) >= 5.0

def test_session_warnings():
    w = session_cost_warnings(CostSessionRegime.CLOSED)
    assert len(w) == 1
    assert "blocked" in w[0]

def test_session_text():
    t = session_regime_to_text(CostSessionRegime.PREMARKET, 2.5)
    assert "PREMARKET" in t
    assert "2.5" in t
