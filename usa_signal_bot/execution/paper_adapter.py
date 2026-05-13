from typing import Any
from usa_signal_bot.core.enums import TradabilityStatus, ExecutionRealismStatus
from usa_signal_bot.execution.liquidity_models import TradabilityGuardResult

def attach_execution_realism_to_paper_order(order: dict[str, Any], guard_result: TradabilityGuardResult) -> dict[str, Any]:
    if "metadata" not in order:
        order["metadata"] = {}

    order["metadata"]["tradability_status"] = guard_result.status.value
    order["metadata"]["execution_risk"] = guard_result.risk_level.value

    if guard_result.slippage_estimate and guard_result.slippage_estimate.slippage_proxy_bps:
        order["metadata"]["estimated_slippage_bps"] = guard_result.slippage_estimate.slippage_proxy_bps

    if guard_result.spread_estimate and guard_result.spread_estimate.spread_proxy_bps:
         order["metadata"]["estimated_spread_bps"] = guard_result.spread_estimate.spread_proxy_bps

    if guard_result.status in [TradabilityStatus.BLOCK_SIGNAL, TradabilityStatus.BLOCK_BACKTEST_FILL]:
        order["metadata"]["paper_fill_disallowed"] = True

    return order

def paper_fill_allowed_by_tradability(guard_result: TradabilityGuardResult) -> bool:
    if guard_result.status in [TradabilityStatus.BLOCK_SIGNAL, TradabilityStatus.BLOCK_BACKTEST_FILL]:
        return False
    return True

def estimate_paper_fill_price_adjustment(order: dict[str, Any], guard_result: TradabilityGuardResult) -> dict[str, Any]:
    price_adj = {"slippage_bps": 0.0, "spread_bps": 0.0, "total_bps_penalty": 0.0}

    if guard_result.slippage_estimate and guard_result.slippage_estimate.slippage_proxy_bps:
        price_adj["slippage_bps"] = guard_result.slippage_estimate.slippage_proxy_bps

    if guard_result.spread_estimate and guard_result.spread_estimate.spread_proxy_bps:
        price_adj["spread_bps"] = guard_result.spread_estimate.spread_proxy_bps

    price_adj["total_bps_penalty"] = price_adj["slippage_bps"] + (price_adj["spread_bps"] / 2.0)

    return price_adj

def paper_execution_realism_warnings(guard_result: TradabilityGuardResult) -> list[str]:
    warns = []

    if guard_result.status == TradabilityStatus.BLOCK_BACKTEST_FILL:
        warns.append("Paper fill is blocked due to high participation or extreme execution risk.")
    elif guard_result.status == TradabilityStatus.REVIEW_REQUIRED:
        warns.append("Paper fill uses optimistic slippage but requires manual review.")

    for r in guard_result.reasons:
        warns.append(f"Reason: {r.value}")

    return warns

def paper_execution_realism_summary(order: dict[str, Any]) -> dict[str, Any]:
    meta = order.get("metadata", {})
    return {
        "tradability_status": meta.get("tradability_status", "UNKNOWN"),
        "execution_risk": meta.get("execution_risk", "UNKNOWN"),
        "paper_fill_disallowed": meta.get("paper_fill_disallowed", False),
        "estimated_slippage_bps": meta.get("estimated_slippage_bps", 0.0),
        "estimated_spread_bps": meta.get("estimated_spread_bps", 0.0)
    }
