import math
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.exceptions import TransitionConcentrationMetricsError
from usa_signal_bot.regime_classification.diagnostics.phase129_models import RegimeTransitionMatrix

def compute_transition_entropy_proxy(probabilities: Dict[str, Dict[str, float]]) -> Optional[float]:
    entropies = []
    for from_lbl, to_probs in probabilities.items():
        h = 0.0
        for p in to_probs.values():
            if p > 0:
                h -= p * math.log2(p)
        entropies.append(h)
    if not entropies:
        return None
    return sum(entropies) / len(entropies)

def compute_transition_concentration(probabilities: Dict[str, Dict[str, float]]) -> Optional[float]:
    # Herfindahl-Hirschman Index (HHI) proxy applied to transition distributions
    conc_scores = []
    for from_lbl, to_probs in probabilities.items():
        hhi = sum(p * p for p in to_probs.values())
        conc_scores.append(hhi)
    if not conc_scores:
        return None
    return sum(conc_scores) / len(conc_scores)

def compute_dominant_transition(counts: Dict[str, Dict[str, int]]) -> Optional[str]:
    max_c = -1
    dom = None
    for from_lbl, to_counts in counts.items():
        for to_lbl, count in to_counts.items():
            if count > max_c:
                max_c = count
                dom = f"{from_lbl}->{to_lbl}"
    return dom

def validate_transition_concentration_values(values: List[Optional[float]]) -> List[str]:
    errors = []
    for v in values:
        if v is not None and v < 0:
            errors.append(f"Invalid concentration value {v}")
    return errors

def transition_concentration_metrics_summary(matrices: List[RegimeTransitionMatrix]) -> Dict[str, Any]:
    return {"count": len(matrices)}
