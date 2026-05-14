
from typing import Any, Dict, Optional
from usa_signal_bot.cost_robustness.robustness_models import CostFragilityAssessment

def attach_cost_robustness_to_signal(signal: Dict[str, Any], assessment: Optional[CostFragilityAssessment] = None) -> Dict[str, Any]:
    new_sig = dict(signal)
    if 'metadata' not in new_sig:
        new_sig['metadata'] = {}
    new_sig['metadata']['cost_robustness_attached'] = True
    return new_sig

def attach_cost_robustness_to_candidate(candidate: Dict[str, Any], assessment: Optional[CostFragilityAssessment] = None) -> Dict[str, Any]:
    new_cand = dict(candidate)
    if 'metadata' not in new_cand:
        new_cand['metadata'] = {}
    new_cand['metadata']['cost_robustness_attached'] = True
    return new_cand

def suppress_candidate_if_cost_fragile(candidate: Dict[str, Any], assessment: CostFragilityAssessment, min_score: float = 50.0) -> Dict[str, Any]:
    new_cand = dict(candidate)
    if assessment.fragility_score is not None and assessment.fragility_score < min_score:
        if 'metadata' not in new_cand:
            new_cand['metadata'] = {}
        new_cand['metadata']['suppressed_due_to_fragility'] = True
    return new_cand

def cost_robustness_rank_penalty(assessment: Optional[CostFragilityAssessment]) -> float:
    if assessment and assessment.fragility_score is not None and assessment.fragility_score < 50.0:
        return 10.0
    return 0.0

def signal_cost_robustness_summary(signal: Dict[str, Any]) -> Dict[str, Any]:
    return {"attached": signal.get('metadata', {}).get('cost_robustness_attached', False)}
