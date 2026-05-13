from typing import Any

from usa_signal_bot.execution.liquidity_models import (
    LiquidityMetric,
    LiquidityProfile,
    SpreadProxyEstimate,
    SlippageProxyEstimate,
    TradabilityGuardResult,
    BorrowabilityProxyResult,
    ExecutionRealismReview
)
from usa_signal_bot.execution.liquidity_metrics import liquidity_profile_to_text
from usa_signal_bot.execution.spread_proxy import spread_proxy_to_text
from usa_signal_bot.execution.slippage_proxy import slippage_proxy_to_text
from usa_signal_bot.execution.borrowability_proxy import borrowability_proxy_to_text

def liquidity_metric_to_text(metric: LiquidityMetric) -> str:
    return f"{metric.metric_name.value}: {metric.value} {metric.unit or ''}"

def tradability_guard_result_to_text(result: TradabilityGuardResult) -> str:
    lines = [
        f"Tradability Guard for {result.symbol}:",
        f"  Status: {result.status.value}",
        f"  Risk Level: {result.risk_level.value}",
    ]
    if result.reasons:
        lines.append("  Reasons:")
        for r in result.reasons:
            lines.append(f"   - {r.value if hasattr(r, 'value') else r}")
    if result.recommended_guards:
        lines.append("  Recommended Guards:")
        for g in result.recommended_guards:
            lines.append(f"   - {g}")
    if result.warnings:
        lines.append("  Warnings:")
        for w in result.warnings:
            lines.append(f"   - {w}")
    lines.append("  Note: Not investment advice. No broker order generated.")
    return "\n".join(lines)

def execution_realism_review_to_text(review: ExecutionRealismReview, limit: int = 100) -> str:
    lines = [
        "Execution Realism Review",
        f"  ID: {review.review_id}",
        f"  Time: {review.created_at_utc}",
        f"  Symbols Analysed: {len(review.symbols)}",
    ]

    blocked = sum(1 for t in review.tradability_results if t.status.value == "BLOCK_SIGNAL")
    lines.append(f"  Blocked Signals: {blocked}")

    if review.warnings:
        lines.append("  Review Warnings:")
        for w in review.warnings:
            lines.append(f"   - {w}")

    lines.append("\n  Details:")
    for t in review.tradability_results[:limit]:
        lines.append("  " + tradability_guard_result_to_text(t).replace("\n", "\n  "))

    if len(review.tradability_results) > limit:
        lines.append(f"  ... and {len(review.tradability_results) - limit} more.")

    lines.append("\n  Disclaimer: This review assesses theoretical tradability only. No live trading data is used.")
    return "\n".join(lines)

def execution_store_summary_to_text(summary: dict[str, Any]) -> str:
    lines = [
        "Execution Store Summary",
        f"  Liquidity Profiles: {summary.get('liquidity_profiles_count', 0)}",
        f"  Tradability Results: {summary.get('tradability_results_count', 0)}",
        f"  Borrowability Results: {summary.get('borrowability_results_count', 0)}",
        f"  Execution Reviews: {summary.get('execution_reviews_count', 0)}",
        f"  Latest Review: {summary.get('latest_review_path', 'None')}"
    ]
    return "\n".join(lines)

def execution_limitations_text() -> str:
    return """
========================================
EXECUTION REALISM LIMITATIONS
========================================
1. This system uses local heuristic proxies for spread, slippage, and borrowability.
2. NO real broker API is connected.
3. NO real live or demo orders are sent.
4. NO real bid/ask or Level-2 order book data is used.
5. NO real short borrow or locate data is fetched.
6. A "PASS" or "REALISTIC" status DOES NOT constitute approval for live trading.
7. This subsystem provides risk-awareness metadata for backtesting and paper trading, NOT investment advice.
========================================
"""
