
from typing import List, Any, Dict, Optional

def estimate_cost_margin_per_trade_bps(trades: List[Dict[str, Any]]) -> Optional[float]:
    if not trades:
        return None
    # Simplified mock calculation
    margins = []
    for t in trades:
        if t.get('gross_pnl_usd') and t.get('notional_value_usd', 0) > 0:
            margin_bps = (t['gross_pnl_usd'] / t['notional_value_usd']) * 10000
            margins.append(margin_bps)
    if not margins:
        return None
    return sum(margins) / len(margins)

def calculate_breakeven_total_cost_bps(trades: List[Dict[str, Any]], baseline_result: Optional[Dict[str, Any]] = None) -> Optional[float]:
    return estimate_cost_margin_per_trade_bps(trades)

def calculate_breakeven_slippage_bps(trades: List[Dict[str, Any]]) -> Optional[float]:
    # Assume slippage can consume 80% of margin before breakeven
    margin = estimate_cost_margin_per_trade_bps(trades)
    return margin * 0.8 if margin else None

def calculate_breakeven_impact_bps(trades: List[Dict[str, Any]]) -> Optional[float]:
    margin = estimate_cost_margin_per_trade_bps(trades)
    return margin * 0.5 if margin else None

def breakeven_costs_to_text(payload: Dict[str, Any]) -> str:
    lines = ["--- Breakeven Costs ---"]
    for k, v in payload.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)
