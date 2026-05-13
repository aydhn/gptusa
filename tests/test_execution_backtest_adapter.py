from usa_signal_bot.execution.backtest_adapter import (
    attach_execution_realism_to_backtest_result,
    backtest_fill_allowed_by_tradability
)
from usa_signal_bot.execution.liquidity_models import ExecutionRealismReview, TradabilityGuardResult
from usa_signal_bot.core.enums import ExecutionReportType, TradabilityStatus

def test_backtest_adapter():
    review = ExecutionRealismReview(
        review_id="id",
        created_at_utc="",
        report_type=ExecutionReportType.FULL_EXECUTION_REVIEW,
        symbols=["SPY"],
        liquidity_profiles=[],
        tradability_results=[],
        borrowability_results=[]
    )
    res = {}
    res = attach_execution_realism_to_backtest_result(res, review)
    assert res["metadata"]["execution_blocked_count"] == 0
