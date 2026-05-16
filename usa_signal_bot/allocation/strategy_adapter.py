from typing import Any, Dict, List, Optional
from usa_signal_bot.allocation.allocation_models import SizingInput, create_sizing_input_id, PositionSizeResult

def sizing_input_from_strategy_adapted_candidate(candidate: Dict[str, Any]) -> SizingInput:
    inp = SizingInput(
        sizing_input_id=create_sizing_input_id(candidate.get("symbol", "UNKNOWN")),
        symbol=candidate.get("symbol", "UNKNOWN"),
        strategy_name=candidate.get("strategy", "UNKNOWN"),
        side=candidate.get("side"),
        reference_price=candidate.get("close"),
        signal_score=candidate.get("composite_score", candidate.get("score")),
        ensemble_consensus_score=strategy_ensemble_confidence_for_sizing(candidate),
        metadata={}
    )

    gate_decision = candidate.get("strategy_gate_decision", "PASS")
    if gate_decision in ["BLOCK", "SUPPRESS"]:
         inp.metadata["alignment"] = {"status": "BLOCK_SIGNAL"}

    return inp

def strategy_ensemble_confidence_for_sizing(candidate: Dict[str, Any]) -> Optional[float]:
    ensemble = candidate.get("ensemble_data")
    if ensemble and isinstance(ensemble, dict):
        return ensemble.get("consensus_score")
    return None

def apply_strategy_adaptation_to_sizing_input(input_payload: SizingInput, adaptation_payload: Optional[Dict[str, Any]] = None) -> SizingInput:
    if not adaptation_payload:
        return input_payload

    inp = SizingInput(
        sizing_input_id=input_payload.sizing_input_id,
        symbol=input_payload.symbol,
        strategy_name=input_payload.strategy_name,
        side=input_payload.side,
        reference_price=input_payload.reference_price,
        signal_score=input_payload.signal_score,
        signal_confidence=input_payload.signal_confidence,
        ensemble_consensus_score=adaptation_payload.get("consensus_score", input_payload.ensemble_consensus_score),
        regime_alignment_score=input_payload.regime_alignment_score,
        transition_risk_score=input_payload.transition_risk_score,
        liquidity_score=input_payload.liquidity_score,
        execution_realism_score=input_payload.execution_realism_score,
        cost_robustness_score=input_payload.cost_robustness_score,
        atr_pct=input_payload.atr_pct,
        stop_distance_pct=input_payload.stop_distance_pct,
        requested_notional_usd=input_payload.requested_notional_usd,
        metadata=dict(input_payload.metadata)
    )

    if adaptation_payload.get("gate_decision") in ["BLOCK", "SUPPRESS"]:
        inp.metadata["alignment"] = {"status": "BLOCK_SIGNAL"}

    return inp

def strategy_sizing_adjustment_summary(results: List[PositionSizeResult]) -> Dict[str, Any]:
    blocked_by_strategy = sum(1 for r in results if any(a.reason.value == "REGIME_CONFLICT" or "BLOCK_SIGNAL" in a.description for a in r.adjustments))
    return {
        "blocked_by_strategy_gate": blocked_by_strategy
    }

def strategy_sizing_adapter_to_text(payload: Dict[str, Any]) -> str:
    return f"Strategy Blocks: {payload.get('blocked_by_strategy_gate', 0)}"
