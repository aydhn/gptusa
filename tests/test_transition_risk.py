from usa_signal_bot.regime_map.transition_risk import aggregate_transition_risk
from usa_signal_bot.core.enums import RegimeTransitionRisk

def test_aggregate_empty():
    assert aggregate_transition_risk([]) == RegimeTransitionRisk.NONE
