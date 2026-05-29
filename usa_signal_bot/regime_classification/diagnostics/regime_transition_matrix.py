import pandas as pd
from collections import defaultdict
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.exceptions import RegimeTransitionMatrixError
from usa_signal_bot.core.enums import RegimeDiagnosticsQuality
from usa_signal_bot.regime_classification.diagnostics.phase129_models import (
    RegimeTransitionObservation,
    RegimeTransitionMatrix,
    create_regime_transition_observation_id,
    create_regime_transition_matrix_id,
    _now
)

def compute_transition_counts(labels: List[str]) -> Dict[str, Dict[str, int]]:
    counts = defaultdict(lambda: defaultdict(int))
    if not labels or len(labels) < 2:
        return {k: dict(v) for k, v in counts.items()}

    for i in range(len(labels) - 1):
        from_lbl = labels[i]
        to_lbl = labels[i + 1]
        if pd.isna(from_lbl) or pd.isna(to_lbl):
            continue
        counts[str(from_lbl)][str(to_lbl)] += 1

    return {k: dict(v) for k, v in counts.items()}

def compute_transition_probabilities(counts: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, float]]:
    probs = defaultdict(dict)
    for from_lbl, to_counts in counts.items():
        total_from = sum(to_counts.values())
        if total_from == 0:
            continue
        for to_lbl, count in to_counts.items():
            probs[from_lbl][to_lbl] = count / total_from
    return {k: dict(v) for k, v in probs.items()}

def build_transition_observations(symbol: Optional[str], counts: Dict[str, Dict[str, int]], probabilities: Dict[str, Dict[str, float]]) -> List[RegimeTransitionObservation]:
    obs = []
    for from_lbl, to_counts in counts.items():
        for to_lbl, count in to_counts.items():
            prob = probabilities.get(from_lbl, {}).get(to_lbl, 0.0)
            obs.append(RegimeTransitionObservation(
                observation_id=create_regime_transition_observation_id(),
                created_at_utc=_now(),
                symbol=symbol,
                from_label=from_lbl,
                to_label=to_lbl,
                transition_count=count,
                transition_probability=prob,
                self_transition=(from_lbl == to_lbl),
                research_metadata_only=True,
                produces_trade_signal=False,
                produces_order_decision=False,
                produces_portfolio_weights=False,
            ))
    return obs

def build_transition_matrix_for_labels(labels: List[str], symbol: Optional[str] = None) -> RegimeTransitionMatrix:
    valid_labels = [str(L) for L in labels if not pd.isna(L)]
    counts = compute_transition_counts(valid_labels)
    probs = compute_transition_probabilities(counts)
    obs = build_transition_observations(symbol, counts, probs)

    total = sum(sum(c.values()) for c in counts.values())
    self_total = sum(counts.get(k, {}).get(k, 0) for k in counts.keys())
    switch_total = total - self_total

    unique_labels = sorted(list(set(valid_labels)))

    dominant_transition = None
    max_count = -1
    for from_lbl, to_counts in counts.items():
        for to_lbl, count in to_counts.items():
            if from_lbl != to_lbl and count > max_count:
                max_count = count
                dominant_transition = f"{from_lbl}->{to_lbl}"

    # Entropy proxy is left for concentration_metrics, pass None here initially.

    return RegimeTransitionMatrix(
        matrix_id=create_regime_transition_matrix_id(),
        created_at_utc=_now(),
        symbol=symbol,
        labels=unique_labels,
        observations=obs,
        transition_counts=counts,
        transition_probabilities=probs,
        total_transitions=total,
        self_transition_count=self_total,
        switch_count=switch_total,
        self_transition_rate=(self_total / total) if total > 0 else 0.0,
        switch_rate=(switch_total / total) if total > 0 else 0.0,
        dominant_transition=dominant_transition if max_count > 0 else None,
        transition_entropy_proxy=None,
        transition_concentration=None,
        matrix_valid=True if total > 0 else False,
        quality=RegimeDiagnosticsQuality.HIGH if total > 0 else RegimeDiagnosticsQuality.INVALID,
        research_metadata_only=True,
        model_training_used=False,
        model_prediction_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
    )

def build_transition_matrix_for_table(symbol: Optional[str], df: pd.DataFrame, label_column: str = "regime_label_research") -> RegimeTransitionMatrix:
    if label_column not in df.columns:
        raise RegimeTransitionMatrixError(f"Column '{label_column}' not found in dataframe")
    labels = df[label_column].tolist()
    return build_transition_matrix_for_labels(labels, symbol)

def build_transition_matrices(tables: Dict[str, pd.DataFrame]) -> List[RegimeTransitionMatrix]:
    matrices = []
    for symbol, df in tables.items():
        matrices.append(build_transition_matrix_for_table(symbol, df))
    return matrices

def validate_transition_matrix(matrix: RegimeTransitionMatrix) -> List[str]:
    errors = []
    if not matrix.matrix_valid:
        errors.append("Matrix is marked invalid.")
    if matrix.switch_rate < 0 or matrix.switch_rate > 1:
        errors.append(f"Switch rate out of bounds: {matrix.switch_rate}")
    if matrix.self_transition_rate < 0 or matrix.self_transition_rate > 1:
        errors.append(f"Self-transition rate out of bounds: {matrix.self_transition_rate}")
    for from_lbl, to_probs in matrix.transition_probabilities.items():
        s = sum(to_probs.values())
        if abs(s - 1.0) > 1e-4 and s > 0:
            errors.append(f"Probabilities from {from_lbl} do not sum to 1 ({s})")
    return errors

def transition_matrix_summary(matrices: List[RegimeTransitionMatrix]) -> Dict[str, Any]:
    return {
        "matrix_count": len(matrices),
        "total_transitions": sum(m.total_transitions for m in matrices),
        "avg_switch_rate": sum(m.switch_rate for m in matrices) / len(matrices) if matrices else 0.0,
    }

def transition_matrix_to_text(matrices: List[RegimeTransitionMatrix], limit: int = 300) -> str:
    lines = ["Regime Transition Matrices"]
    for m in matrices[:limit]:
        lines.append(f"[{m.symbol or 'UNKNOWN'}] Switch Rate: {m.switch_rate:.2f}, Transitions: {m.total_transitions}, Dominant: {m.dominant_transition}")
    return "\n".join(lines)
