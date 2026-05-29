from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import MarketBehaviorContext
from usa_signal_bot.regime_classification.behavior_reporting.market_behavior_reporting import (
    market_behavior_context_to_text, market_behavior_limitations_text
)

def test_market_behavior_reporting():
    ctx = MarketBehaviorContext(context_id="test_ctx")
    txt = market_behavior_context_to_text(ctx)
    assert "test_ctx" in txt

    lim = market_behavior_limitations_text()
    assert "Phase 130" in lim
