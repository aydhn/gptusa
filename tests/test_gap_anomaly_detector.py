"""Test gap anomaly detector."""
from usa_signal_bot.corporate_actions.gap_anomaly_detector import detect_price_gap_anomalies

def test_gap_anomaly_detector():
    rows = [
        {"date": "2024-01-01", "close": 100.0, "open": 99.0},
        {"date": "2024-01-02", "close": 80.0, "open": 80.0} # 20% gap down
    ]
    anomalies = detect_price_gap_anomalies("SPY", rows)
    assert len(anomalies) == 1
