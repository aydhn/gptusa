from usa_signal_bot.execution.borrowability_proxy import estimate_borrowability_proxy
from usa_signal_bot.core.enums import BorrowabilityProxyStatus, ExecutionRiskLevel

def test_borrowability_proxy():
    rows = [{"close": 100, "volume": 1000000}]
    b = estimate_borrowability_proxy("SPY", rows)
    assert b.status == BorrowabilityProxyStatus.LIKELY_EASY
    assert b.score == 100.0
