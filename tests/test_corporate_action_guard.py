"""Test corporate action guard."""
from usa_signal_bot.corporate_actions.corporate_action_guard import CorporateActionGuard
from usa_signal_bot.core.enums import CorporateActionGuardStatus

def test_corporate_action_guard():
    guard = CorporateActionGuard()
    rows = [
        {"date": "2024-01-01", "close": 100.0, "open": 99.0, "adj_close": 50.0, "volume": 1000},
        {"date": "2024-01-02", "close": 50.0, "open": 50.0, "adj_close": 50.0, "volume": 2000}
    ]
    res = guard.evaluate_symbol_rows("SPY", rows)
    # Adjusted price inconsistency + massive gap = REVIEW_REQUIRED
    assert res.status in [CorporateActionGuardStatus.BLOCK_SIGNAL, CorporateActionGuardStatus.REVIEW_REQUIRED]
