from typing import Any
from usa_signal_bot.core.enums import TransactionSide, TransactionCostReportType
from usa_signal_bot.transaction_costs.cost_models import (
    TransactionCostInput,
    TransactionCostBreakdown,
    FeeScheduleProxy,
    SlippageCurve,
    MarketImpactEstimate,
    FillSimulationResult,
    CostAdjustedTradeResult,
    TransactionCostReview
)
from usa_signal_bot.transaction_costs.fee_schedule import fee_schedule_to_text
from usa_signal_bot.transaction_costs.slippage_curves import slippage_curve_to_text
from usa_signal_bot.transaction_costs.market_impact import market_impact_to_text
from usa_signal_bot.transaction_costs.fill_simulator import fill_simulation_result_to_text
from usa_signal_bot.transaction_costs.cost_adjusted_trade import cost_adjusted_trade_result_to_text

def transaction_cost_input_to_text(payload: TransactionCostInput) -> str:
    return (f"Cost Input [{payload.symbol}]: Side={payload.side.value if isinstance(payload.side, TransactionSide) else payload.side}, "
            f"Qty={payload.quantity}, Notional=${payload.notional_usd}, Price=${payload.price}")

def transaction_cost_breakdown_to_text(item: TransactionCostBreakdown) -> str:
    lines = [
        f"Cost Breakdown [{item.symbol}] (ID: {item.breakdown_id})",
        f"  Total Cost: ${item.total_cost_usd} ({item.total_cost_bps} bps)"
    ]
    if item.components_usd:
        lines.append("  Components USD:")
        for k, v in item.components_usd.items():
            lines.append(f"    {k}: ${v:.2f}")
    if item.components_bps:
        lines.append("  Components BPS:")
        for k, v in item.components_bps.items():
            lines.append(f"    {k}: {v:.2f} bps")
    if item.warnings:
        lines.append("  Warnings:")
        for w in item.warnings:
            lines.append(f"    - {w}")
    return "\n".join(lines)

def fee_schedule_proxy_to_text(item: FeeScheduleProxy) -> str:
    return fee_schedule_to_text(item)

def transaction_cost_review_to_text(item: TransactionCostReview, limit: int = 100) -> str:
    lines = [
        f"Transaction Cost Review (ID: {item.review_id})",
        f"Type: {item.report_type.value if isinstance(item.report_type, TransactionCostReportType) else item.report_type}",
        f"Date: {item.created_at_utc}",
        f"Symbols: {', '.join(item.symbols[:5])}{'...' if len(item.symbols) > 5 else ''}",
        ""
    ]

    if item.cost_breakdowns:
        lines.append("--- Cost Breakdowns ---")
        for b in item.cost_breakdowns[:limit]:
            lines.append(transaction_cost_breakdown_to_text(b))
            lines.append("")

    if item.impact_estimates:
        lines.append("--- Market Impact Estimates ---")
        for i in item.impact_estimates[:limit]:
            lines.append(market_impact_to_text(i))
            lines.append("")

    if item.fill_results:
        lines.append("--- Fill Simulations ---")
        for f in item.fill_results[:limit]:
            lines.append(fill_simulation_result_to_text(f))
            lines.append("")

    if item.adjusted_trade_results:
        lines.append("--- Cost Adjusted Trades ---")
        for a in item.adjusted_trade_results[:limit]:
            lines.append(cost_adjusted_trade_result_to_text(a))
            lines.append("")

    if item.warnings:
        lines.append("--- Global Warnings ---")
        for w in item.warnings:
            lines.append(f"  - {w}")

    lines.append("")
    lines.append(transaction_cost_limitations_text())

    return "\n".join(lines)

def cost_store_summary_to_text(summary: dict[str, Any]) -> str:
    lines = [
        "Transaction Cost Store Summary:",
        f"  Breakdowns: {summary.get('breakdowns', 0)}",
        f"  Slippage Curves: {summary.get('slippage_curves', 0)}",
        f"  Market Impacts: {summary.get('market_impacts', 0)}",
        f"  Fill Simulations: {summary.get('fill_simulations', 0)}",
        f"  Adjusted Trades: {summary.get('adjusted_trades', 0)}",
        f"  Reviews: {summary.get('reviews', 0)}"
    ]
    return "\n".join(lines)

def transaction_cost_limitations_text() -> str:
    return (
        "LIMITATIONS & DISCLAIMER:\n"
        "1. No real broker orders or live executions are performed.\n"
        "2. No real order book data or level-2 feeds are used.\n"
        "3. Slippage and market impact are estimated via heuristic curves and models.\n"
        "4. Fee schedules are approximations (proxies) and not official billing models.\n"
        "5. The output is for local research realism only and is NOT investment advice.\n"
        "6. Cost-adjusted results do not guarantee real-world trading outcomes or fill certainty."
    )
