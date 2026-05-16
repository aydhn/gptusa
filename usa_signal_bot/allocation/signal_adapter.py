from typing import Any, Dict, List
from usa_signal_bot.core.enums import PositionSizeStatus
from usa_signal_bot.allocation.allocation_models import SizingInput, PositionSizeResult, CapitalState, RiskBudget, create_sizing_input_id
from usa_signal_bot.allocation.adaptive_sizing_engine import AdaptiveSizingEngine

def sizing_input_from_signal(signal: Dict[str, Any]) -> SizingInput:
    return SizingInput(
        sizing_input_id=create_sizing_input_id(signal.get("symbol", "UNKNOWN")),
        symbol=signal.get("symbol", "UNKNOWN"),
        strategy_name=signal.get("strategy_name", "UNKNOWN"),
        side=signal.get("side"),
        reference_price=signal.get("trigger_price") or signal.get("reference_price"),
        signal_score=signal.get("signal_score"),
        atr_pct=signal.get("atr_pct"),
        stop_distance_pct=signal.get("stop_distance_pct"),
        metadata=signal.get("metadata", {})
    )

def attach_position_size_to_signal(signal: Dict[str, Any], result: PositionSizeResult) -> Dict[str, Any]:
    sig = dict(signal)
    if "metadata" not in sig:
        sig["metadata"] = {}

    sig["metadata"]["local_notional_usd"] = result.final_notional_usd
    sig["metadata"]["local_quantity"] = result.final_quantity
    sig["metadata"]["position_size_status"] = result.status.value
    sig["metadata"]["risk_pct_equity"] = result.risk_pct_equity
    sig["metadata"]["sizing_is_paper_only"] = True
    return sig

def apply_sizing_to_signals(signals: List[Dict[str, Any]], engine: AdaptiveSizingEngine, capital_state: CapitalState, risk_budget: RiskBudget) -> List[Dict[str, Any]]:
    sized_signals = []
    for sig in signals:
        inp = sizing_input_from_signal(sig)
        res = engine.size_position(inp, capital_state, risk_budget)
        sized_sig = attach_position_size_to_signal(sig, res)
        sized_sig = suppress_signal_if_size_blocked(sized_sig, res)
        sized_signals.append(sized_sig)
    return sized_signals

def suppress_signal_if_size_blocked(signal: Dict[str, Any], result: PositionSizeResult) -> Dict[str, Any]:
    sig = dict(signal)
    if result.status in [PositionSizeStatus.BLOCKED, PositionSizeStatus.SUPPRESSED]:
        sig["status"] = "SUPPRESSED"
        if "metadata" not in sig:
            sig["metadata"] = {}
        sig["metadata"]["suppression_reason"] = f"Sizing status is {result.status.value}"
    return sig

def signal_sizing_summary(signals: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_approved = sum(1 for s in signals if s.get("metadata", {}).get("position_size_status") == PositionSizeStatus.APPROVED.value)
    total_blocked = sum(1 for s in signals if s.get("status") == "SUPPRESSED" and "Sizing status" in s.get("metadata", {}).get("suppression_reason", ""))
    return {
        "total_approved_signals": total_approved,
        "total_size_blocked_signals": total_blocked
    }
