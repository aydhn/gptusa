from usa_signal_bot.allocation.adaptive_sizing_engine import AdaptiveSizingEngine
from usa_signal_bot.allocation.capital_state import default_capital_state
from usa_signal_bot.allocation.risk_budget import default_risk_budget
from usa_signal_bot.allocation.allocation_models import SizingInput, create_sizing_input_id
from usa_signal_bot.core.enums import PositionSizeStatus

def test_adaptive_sizing_engine_valid():
    cs = default_capital_state(100000.0)
    rb = default_risk_budget()
    engine = AdaptiveSizingEngine()
    inp = SizingInput(create_sizing_input_id("SPY"), "SPY", "Test", "LONG", 100.0, 50.0, 50.0, None, None, None, None, None, None, None, None, None)
    res = engine.size_position(inp, cs, rb)
    assert res.status in [PositionSizeStatus.APPROVED, PositionSizeStatus.REDUCED, PositionSizeStatus.CAPPED]
    assert res.final_notional_usd is not None
    assert res.final_notional_usd > 0
