from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import MarketBehaviorContext
from usa_signal_bot.regime_classification.behavior_reporting.market_behavior_validation import (
    validate_market_behavior_context_report
)

def test_validate_market_behavior_context_report():
    ctx = MarketBehaviorContext()
    rep = validate_market_behavior_context_report(ctx)
    assert rep.valid

    ctx.activation_allowed = True
    rep = validate_market_behavior_context_report(ctx)
    assert not rep.valid
    assert len(rep.errors) > 0
