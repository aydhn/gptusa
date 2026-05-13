from typing import Any
from usa_signal_bot.core.enums import TradabilityStatus, ExecutionRealismStatus
from usa_signal_bot.execution.liquidity_models import ExecutionRealismReview, TradabilityGuardResult

def attach_execution_realism_to_backtest_result(result: dict[str, Any], review: ExecutionRealismReview) -> dict[str, Any]:
    if "metadata" not in result:
        result["metadata"] = {}

    result["metadata"]["execution_realism_status"] = review.report_type.value if hasattr(review.report_type, 'value') else review.report_type

    blocked = sum(1 for r in review.tradability_results if r.status in [TradabilityStatus.BLOCK_SIGNAL, TradabilityStatus.BLOCK_BACKTEST_FILL])
    warnings = len(review.warnings)

    result["metadata"]["execution_blocked_count"] = blocked
    result["metadata"]["execution_warning_count"] = warnings

    return result

def backtest_fill_allowed_by_tradability(guard_result: TradabilityGuardResult, strict: bool = False) -> bool:
    if guard_result.status == TradabilityStatus.BLOCK_BACKTEST_FILL:
        return False

    if strict and guard_result.status in [TradabilityStatus.BLOCK_SIGNAL, TradabilityStatus.REVIEW_REQUIRED]:
        return False

    return True

def estimate_backtest_fill_penalty_bps(guard_result: TradabilityGuardResult) -> float:
    penalty = 0.0

    if guard_result.slippage_estimate and guard_result.slippage_estimate.slippage_proxy_bps:
        penalty += guard_result.slippage_estimate.slippage_proxy_bps

    if guard_result.spread_estimate and guard_result.spread_estimate.spread_proxy_bps:
        # Additional spread cost
        penalty += guard_result.spread_estimate.spread_proxy_bps / 2.0

    return penalty

def execution_realism_backtest_warnings(review: ExecutionRealismReview) -> list[str]:
    warns = []

    for w in review.warnings:
        warns.append(w)

    for tr in review.tradability_results:
        if tr.status in [TradabilityStatus.BLOCK_SIGNAL, TradabilityStatus.BLOCK_BACKTEST_FILL]:
            warns.append(f"{tr.symbol} backtest fill might be completely unrealistic due to liquidity/participation constraints.")

    return list(set(warns))

def backtest_execution_realism_summary(result: dict[str, Any]) -> dict[str, Any]:
    meta = result.get("metadata", {})
    return {
        "execution_realism_status": meta.get("execution_realism_status", "UNKNOWN"),
        "execution_blocked_count": meta.get("execution_blocked_count", 0),
        "execution_warning_count": meta.get("execution_warning_count", 0)
    }
