from usa_signal_bot.regime_classification.foundation.regime_non_activation_boundary import (
    build_regime_non_activation_boundary_result,
    check_safe_language
)
from usa_signal_bot.core.enums import RegimeBoundaryStatus

def test_check_safe_language():
    assert check_safe_language("This is a regime map.") is True
    assert check_safe_language("This is a buy signal.") is False
    assert check_safe_language("We will buy the stock.") is False
    assert check_safe_language("kesin al") is False
    assert check_safe_language("Here is some macd_signal_9") is True # Contains 'signal' but not 'buy signal' or isolated forbidden word if logic permits. Wait, 'buy' is forbidden. 'signal' alone is skipped in basic check.

def test_build_regime_non_activation_boundary_result_pass():
    res = build_regime_non_activation_boundary_result(
        context_payload={"produces_trade_signal": False},
        columns=["volatility_context"],
        text="Normal description"
    )
    assert res.boundary_passed is True
    assert res.status == RegimeBoundaryStatus.PASSED
    assert res.failed_rules == 0

def test_build_regime_non_activation_boundary_result_fail():
    res = build_regime_non_activation_boundary_result(
        context_payload={"produces_trade_signal": True},
        columns=["volatility_context", "buy_signal"],
        text="Normal description"
    )
    assert res.boundary_passed is False
    assert res.status == RegimeBoundaryStatus.FAILED
    assert res.failed_rules > 0
