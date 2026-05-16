from typing import Any, Dict, List, Optional
from usa_signal_bot.allocation.allocation_models import PositionSizeResult, CapitalState, RiskBudget
from usa_signal_bot.allocation.adaptive_sizing_engine import AdaptiveSizingEngine
from usa_signal_bot.allocation.capital_state import default_capital_state
from usa_signal_bot.allocation.risk_budget import default_risk_budget
from usa_signal_bot.allocation.candidate_adapter import sizing_input_from_candidate

def attach_sizing_to_backtest_trade(trade: Dict[str, Any], result: PositionSizeResult) -> Dict[str, Any]:
    t = dict(trade)
    t["sizing_mode"] = result.mode.value
    t["local_notional_usd"] = result.final_notional_usd
    t["local_quantity"] = result.final_quantity
    t["sizing_status"] = result.status.value
    t["risk_pct_equity"] = result.risk_pct_equity
    t["adjustments"] = [a.reason.value for a in result.adjustments]
    return t

def apply_adaptive_sizing_to_backtest_result(result: Dict[str, Any], capital_state: Optional[CapitalState] = None, risk_budget: Optional[RiskBudget] = None) -> Dict[str, Any]:
    state = capital_state or default_capital_state()
    budget = risk_budget or default_risk_budget()
    engine = AdaptiveSizingEngine()

    trades = result.get("trades", [])
    sized_trades = []

    for t in trades:
        cand = {
            "symbol": t.get("symbol", "UNKNOWN"),
            "strategy": t.get("strategy_name", "UNKNOWN"),
            "side": t.get("side"),
            "close": t.get("entry_price")
        }
        inp = sizing_input_from_candidate(cand)
        res = engine.size_position(inp, state, budget)
        sized_t = attach_sizing_to_backtest_trade(t, res)
        sized_trades.append(sized_t)

    res_dict = dict(result)
    res_dict["trades"] = sized_trades
    res_dict["sizing_metadata"] = backtest_sizing_summary(res_dict)
    res_dict["warnings"] = res_dict.get("warnings", []) + backtest_sizing_warnings(res_dict)
    return res_dict

def backtest_sizing_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    trades = result.get("trades", [])
    blocked = sum(1 for t in trades if t.get("sizing_status") == "BLOCKED")
    approved = sum(1 for t in trades if t.get("sizing_status") == "APPROVED")
    return {
        "total_sized_trades": len(trades),
        "approved_sizes": approved,
        "blocked_sizes": blocked
    }

def backtest_sizing_warnings(result: Dict[str, Any]) -> List[str]:
    trades = result.get("trades", [])
    if any(t.get("sizing_status") == "BLOCKED" for t in trades):
        return ["Some trades were blocked by adaptive sizing in backtest."]
    return []
