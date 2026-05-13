"""Test adjusted price validator."""
from usa_signal_bot.corporate_actions.adjusted_price_validator import validate_adjusted_close_consistency
from usa_signal_bot.core.enums import AdjustedPriceValidationStatus

def test_adjusted_price_validator():
    rows = [
        {"close": 100.0, "adj_close": 50.0}, # Past (split)
        {"close": 100.0, "adj_close": 100.0} # Latest
    ]
    res = validate_adjusted_close_consistency("SPY", rows)
    assert res.status == AdjustedPriceValidationStatus.INCONSISTENT
    assert res.inconsistent_rows > 0
