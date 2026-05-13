"""Test split detector."""
from usa_signal_bot.corporate_actions.split_detector import detect_possible_splits

def test_split_detector():
    rows = [
        {"date": "2024-01-01", "close": 100.0, "open": 99.0, "volume": 1000},
        {"date": "2024-01-02", "close": 50.0, "open": 50.0, "volume": 2000} # 2:1 split
    ]
    cands = detect_possible_splits("SPY", rows)
    assert len(cands) == 1
    assert cands[0]["inferred_ratio"] == 2.0
