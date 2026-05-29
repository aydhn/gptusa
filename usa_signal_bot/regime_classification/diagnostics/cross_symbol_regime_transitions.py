import pandas as pd
from collections import defaultdict
from typing import Any, Dict, List

from usa_signal_bot.core.exceptions import CrossSymbolRegimeTransitionError
from usa_signal_bot.regime_classification.diagnostics.phase129_models import RegimeTransitionMatrix
from usa_signal_bot.regime_classification.diagnostics.regime_transition_matrix import build_transition_matrix_for_labels

def build_cross_symbol_transition_matrix(tables: Dict[str, pd.DataFrame]) -> RegimeTransitionMatrix:
    all_labels = []
    for df in tables.values():
        if "regime_label_research" in df.columns:
            all_labels.extend(df["regime_label_research"].dropna().tolist())

    return build_transition_matrix_for_labels(all_labels, symbol="CROSS_SYMBOL_AGG")

def compute_cross_symbol_label_distribution(tables: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    dist = defaultdict(int)
    total = 0
    for df in tables.values():
        if "regime_label_research" in df.columns:
            for L in df["regime_label_research"].dropna():
                dist[str(L)] += 1
                total += 1

    probs = {k: v / total for k, v in dist.items()} if total > 0 else {}
    return {"counts": dict(dist), "probabilities": probs}

def compute_cross_symbol_switch_summary(matrices: List[RegimeTransitionMatrix]) -> Dict[str, Any]:
    if not matrices:
        return {}
    avg_switch = sum(m.switch_rate for m in matrices) / len(matrices)
    max_switch = max(m.switch_rate for m in matrices)
    min_switch = min(m.switch_rate for m in matrices)
    return {"avg_switch_rate": avg_switch, "max_switch_rate": max_switch, "min_switch_rate": min_switch}

def validate_cross_symbol_transition_outputs(payload: Dict[str, Any]) -> List[str]:
    return []

def cross_symbol_regime_transitions_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"summary": "cross_symbol_available"}

def cross_symbol_regime_transitions_to_text(payload: Dict[str, Any]) -> str:
    return "Cross-Symbol Regime Transitions generated."
