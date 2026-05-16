from typing import Any, Dict
from usa_signal_bot.allocation.allocation_models import CapitalState, RiskBudget, SizingInput, SizingAdjustment, PositionSizeResult, AllocationReview

def capital_state_to_text(item: CapitalState) -> str:
    from usa_signal_bot.allocation.capital_state import capital_state_to_text as cs_to_text
    return cs_to_text(item)

def risk_budget_to_text(item: RiskBudget) -> str:
    from usa_signal_bot.allocation.risk_budget import risk_budget_to_text as rb_to_text
    return rb_to_text(item)

def sizing_input_to_text(item: SizingInput) -> str:
    text = f"Sizing Input [{item.symbol}]\n"
    text += f"Strategy: {item.strategy_name}\n"
    text += f"Reference Price: {item.reference_price}\n"
    text += f"Signal Score: {item.signal_score}\n"
    return text

def sizing_adjustment_to_text(item: SizingAdjustment) -> str:
    return f"- {item.reason.value}: x{item.multiplier:.2f} ({item.description})"

def position_size_result_to_text(item: PositionSizeResult) -> str:
    text = f"Position Size Result [{item.symbol}]\n"
    text += f"Status: {item.status.value}\n"
    text += f"Mode: {item.mode.value}\n"
    if item.status.value in ["BLOCKED", "SUPPRESSED"]:
        text += "SIZE BLOCKED OR SUPPRESSED.\n"
    else:
        text += f"Recommended Local Quantity: {item.final_quantity}\n"
        text += f"Recommended Local Notional: {item.final_notional_usd}\n"
        text += f"Risk Pct Equity: {item.risk_pct_equity:.2f}%\n"

    if item.adjustments:
        text += "Adjustments:\n"
        for a in item.adjustments:
            text += sizing_adjustment_to_text(a) + "\n"

    text += "Note: This is local sizing metadata, NOT a live broker order and NOT investment advice.\n"
    return text

def allocation_review_to_text(item: AllocationReview, limit: int = 100) -> str:
    lines = [
        f"Allocation Review [{item.review_id}]",
        f"Created: {item.created_at_utc}",
        f"Mode: {item.mode.value}",
        f"Total Sized Results: {len(item.sizing_results)}",
        f"Blocked: {item.blocked_count}, Capped: {item.capped_count}, Throttled: {item.throttled_count}",
        f"Total Allocated Notional: {item.total_allocated_notional_usd}",
        ""
    ]
    if item.capital_state:
        lines.append(capital_state_to_text(item.capital_state))
    if item.risk_budget:
        lines.append(risk_budget_to_text(item.risk_budget))

    lines.append("Results Sample:")
    for res in item.sizing_results[:limit]:
        lines.append(position_size_result_to_text(res))

    lines.append(allocation_limitations_text())
    return "\n".join(lines)

def allocation_store_summary_to_text(summary: Dict[str, Any]) -> str:
    if not summary.get("exists", False):
        return "Allocation store does not exist."
    return (
        f"Allocation Store Summary:\n"
        f"Capital States: {summary.get('capital_states_count', 0)}\n"
        f"Risk Budgets: {summary.get('risk_budgets_count', 0)}\n"
        f"Allocation Reviews: {summary.get('reviews_count', 0)}\n"
    )

def allocation_limitations_text() -> str:
    return """
ALLOCATION LIMITATIONS & DISCLAIMER:
- Capital state is local/simulated, not a real broker balance.
- Position size is local metadata, not a live broker order.
- This output is NOT investment advice.
- A 'PASS' or 'APPROVED' sizing is NOT a live trading approval.
- The system operates purely in dry-run/paper mode.
"""
