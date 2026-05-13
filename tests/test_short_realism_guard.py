from usa_signal_bot.execution.short_realism_guard import evaluate_short_realism
from usa_signal_bot.core.enums import TradabilityStatus

def test_short_realism_guard():
    rows = [{"close": 100, "volume": 1000000}]
    res = evaluate_short_realism("SPY", rows)
    assert res.status == TradabilityStatus.TRADABLE
