"""Test dividend detector."""
from usa_signal_bot.corporate_actions.dividend_detector import detect_possible_dividend_adjustments

def test_dividend_detector():
    rows = [
        {"date": "2024-01-01", "close": 100.0, "open": 99.0},
        {"date": "2024-01-02", "close": 99.0, "open": 99.0} # 1.0 drop
    ]
    cands = detect_possible_dividend_adjustments("SPY", rows)
    assert len(cands) == 1
    assert cands[0]["estimated_dividend"] == 1.0
