from typing import Any, Dict, List, Optional
from usa_signal_bot.allocation.allocation_models import CapitalState, RiskBudget
from usa_signal_bot.allocation.backtest_adapter import apply_adaptive_sizing_to_backtest_result

def apply_adaptive_sizing_to_walk_forward_result(result: Dict[str, Any], capital_state_by_window: Optional[Dict[str, CapitalState]] = None, risk_budget: Optional[RiskBudget] = None) -> Dict[str, Any]:
    wf_res = dict(result)
    windows = wf_res.get("windows", [])

    sized_windows = []
    for w in windows:
        window_id = w.get("window_id", "default")
        cstate = capital_state_by_window.get(window_id) if capital_state_by_window else None
        sized_w = apply_adaptive_sizing_to_backtest_result(w, capital_state=cstate, risk_budget=risk_budget)
        sized_windows.append(sized_w)

    wf_res["windows"] = sized_windows
    wf_res["sizing_metadata"] = walk_forward_sizing_summary(wf_res)
    wf_res["sizing_stability"] = walk_forward_sizing_stability(wf_res)
    wf_res["warnings"] = wf_res.get("warnings", []) + walk_forward_sizing_warnings(wf_res)
    return wf_res

def walk_forward_sizing_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    windows = result.get("windows", [])
    total_approved = sum(w.get("sizing_metadata", {}).get("approved_sizes", 0) for w in windows)
    total_blocked = sum(w.get("sizing_metadata", {}).get("blocked_sizes", 0) for w in windows)
    return {
        "total_approved_sizes_across_windows": total_approved,
        "total_blocked_sizes_across_windows": total_blocked
    }

def walk_forward_sizing_stability(result: Dict[str, Any]) -> Dict[str, Any]:
    windows = result.get("windows", [])
    if not windows:
        return {"status": "UNKNOWN"}

    blocked_counts = [w.get("sizing_metadata", {}).get("blocked_sizes", 0) for w in windows]
    max_blocked = max(blocked_counts) if blocked_counts else 0
    if max_blocked > len(windows) * 2: # heuristic
        return {"status": "UNSTABLE", "note": "High number of blocked sizes in some windows."}
    return {"status": "STABLE"}

def walk_forward_sizing_warnings(result: Dict[str, Any]) -> List[str]:
    stab = walk_forward_sizing_stability(result)
    if stab.get("status") == "UNSTABLE":
        return ["Walk-forward sizing shows instability. Many trades were blocked in some windows."]
    return []
