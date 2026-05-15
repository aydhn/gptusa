from typing import Dict, Any, Optional, List
from usa_signal_bot.regime_costs.regime_cost_models import CostRegimeSnapshot, AdaptiveExecutionRealismDecision
from usa_signal_bot.core.enums import AdaptiveExecutionDecision, CombinedCostRegime

def attach_regime_cost_to_signal(signal: Dict[str, Any], snapshot: CostRegimeSnapshot, decision: Optional[AdaptiveExecutionRealismDecision] = None) -> Dict[str, Any]:
    signal["metadata"] = signal.get("metadata", {})
    signal["metadata"]["cost_regime"] = snapshot.combined_regime.value
    if decision:
        signal["metadata"]["adaptive_execution_decision"] = decision.decision.value
    return signal

def attach_regime_cost_to_candidate(candidate: Dict[str, Any], snapshot: CostRegimeSnapshot, decision: Optional[AdaptiveExecutionRealismDecision] = None) -> Dict[str, Any]:
    candidate["metadata"] = candidate.get("metadata", {})
    candidate["metadata"]["cost_regime"] = snapshot.combined_regime.value
    if decision:
        candidate["metadata"]["adaptive_execution_decision"] = decision.decision.value
    return suppress_candidate_if_regime_cost_blocked(candidate, decision)

def regime_cost_rank_penalty(snapshot: CostRegimeSnapshot, decision: Optional[AdaptiveExecutionRealismDecision] = None) -> float:
    # A simple heuristic penalty to lower the rank score of candidates in bad regimes.
    if snapshot.combined_regime == CombinedCostRegime.BLOCKED:
        return 1.0 # 100% penalty
    if snapshot.combined_regime == CombinedCostRegime.HIGH_RISK:
        return 0.5 # 50% penalty
    if snapshot.combined_regime == CombinedCostRegime.STRESSED:
        return 0.25 # 25% penalty
    if snapshot.combined_regime in (CombinedCostRegime.CONSERVATIVE, CombinedCostRegime.INSUFFICIENT_DATA):
        return 0.1 # 10% penalty
    return 0.0

def suppress_candidate_if_regime_cost_blocked(candidate: Dict[str, Any], decision: Optional[AdaptiveExecutionRealismDecision]) -> Dict[str, Any]:
    if decision and decision.decision in (AdaptiveExecutionDecision.BLOCK_FILL_SIMULATION, AdaptiveExecutionDecision.BLOCK_SIGNAL_METADATA):
        candidate["metadata"]["suppressed_by_regime"] = True
    return candidate

def candidate_regime_cost_summary(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    suppressed = sum(1 for c in candidates if c.get("metadata", {}).get("suppressed_by_regime"))
    return {
        "total_candidates": len(candidates),
        "suppressed_by_regime": suppressed
    }
