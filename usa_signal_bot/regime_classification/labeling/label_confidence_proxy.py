import pandas as pd
from typing import Any
from usa_signal_bot.core.enums import RegimeLabelConfidenceKind
from usa_signal_bot.regime_classification.labeling.phase128_models import HeuristicRegimeLabelResult

def compute_score_gap_confidence(top_score: float | None, second_score: float | None) -> float:
    if top_score is None:
        return 0.0
    if second_score is None:
        return 100.0
    gap = top_score - second_score
    # Cap at 100, scale arbitrary 0-50 gap to 0-100 confidence
    return min(max(gap * 2.0, 0.0), 100.0)

def compute_score_level_confidence(top_score: float | None) -> float:
    if top_score is None:
        return 0.0
    return min(max(top_score, 0.0), 100.0)

def compute_candidate_agreement_confidence(score_summary: dict[str, Any]) -> float:
    # Example heuristic
    gap = score_summary.get("score_gap")
    if gap is None:
        return 0.0
    if gap < 5.0:
        return 20.0
    if gap < 15.0:
        return 60.0
    return 90.0

def compute_data_quality_confidence(row: pd.Series) -> float:
    # High confidence if no missing values in feature columns
    # As a simple proxy
    nulls = row.isna().sum()
    if nulls == 0:
        return 100.0
    if nulls < 5:
        return 80.0
    return 40.0

def combine_label_confidence(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)

def confidence_kind_from_values(confidence: float, conflict_count: int = 0) -> RegimeLabelConfidenceKind:
    if confidence < 40.0 or conflict_count > 1:
        return RegimeLabelConfidenceKind.LOW_CONFIDENCE
    return RegimeLabelConfidenceKind.SCORE_GAP_CONFIDENCE

def validate_label_confidence_values(values: list[float]) -> list[str]:
    errors = []
    for v in values:
        if v < 0.0 or v > 100.0:
            errors.append(f"Confidence value out of range (0-100): {v}")
    return errors

def label_confidence_proxy_summary(results: list[HeuristicRegimeLabelResult]) -> dict[str, Any]:
    confs = [r.confidence_score for r in results]
    avg = sum(confs) / len(confs) if confs else 0.0
    low = sum(1 for r in results if r.confidence_kind == RegimeLabelConfidenceKind.LOW_CONFIDENCE)
    return {
        "average_confidence": avg,
        "low_confidence_count": low
    }
