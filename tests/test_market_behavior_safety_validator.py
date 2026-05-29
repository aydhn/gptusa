from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import MarketBehaviorContext
from usa_signal_bot.regime_classification.behavior_reporting.market_behavior_safety_validator import (
    validate_market_behavior_context_safety, market_behavior_text_has_trade_or_execution_language
)

def test_validate_market_behavior_context_safety():
    ctx = MarketBehaviorContext()
    errs = validate_market_behavior_context_safety(ctx)
    assert not errs

    ctx.activation_allowed = True
    errs = validate_market_behavior_context_safety(ctx)
    assert len(errs) > 0

def test_market_behavior_text_has_trade_or_execution_language():
    assert market_behavior_text_has_trade_or_execution_language("This is a sell signal")
    assert market_behavior_text_has_trade_or_execution_language("Wait for entry point")
    assert not market_behavior_text_has_trade_or_execution_language("This is a safe report")
    assert not market_behavior_text_has_trade_or_execution_language("macd_signal_9 crossed zero")
