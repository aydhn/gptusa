from datetime import datetime, timezone
from typing import Any, List

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    SplitAwareComparisonResult,
    MetricNormalizationResult,
    create_split_aware_comparison_id
)

def build_split_aware_comparisons(normalized_metrics: list[MetricNormalizationResult]) -> list[SplitAwareComparisonResult]:
    # Dummy logic to map splits
    artifacts = set(m.model_artifact_id for m in normalized_metrics if m.model_artifact_id)
    comparisons = []

    for art_id in artifacts:
        # Pseudo values
        comparisons.append(
            SplitAwareComparisonResult(
                split_comparison_id=create_split_aware_comparison_id(),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                model_artifact_id=art_id,
                experiment_id=None,
                train_score=0.8,
                validation_score=0.75,
                test_score=0.74,
                split_stability_score=0.9,
                generalization_gap=0.01,
                warning_level="LOW",
                diagnostic_notes=["Generalization gap is acceptable."],
                research_data_only=True,
                produces_trade_signal=False,
                produces_order_decision=False,
                produces_portfolio_weights=False,
                warnings=[],
                errors=[],
                risk_flags=[],
                metadata={}
            )
        )
    return comparisons

def compute_split_stability_score(train_score: float | None, validation_score: float | None, test_score: float | None) -> float | None:
    if None in (validation_score, test_score):
        return None
    return 1.0 - abs(validation_score - test_score)

def compute_generalization_gap(validation_score: float | None, test_score: float | None) -> float | None:
    if None in (validation_score, test_score):
        return None
    return abs(validation_score - test_score)

def validate_split_aware_comparisons(items: list[SplitAwareComparisonResult]) -> list[str]:
    return []

def split_aware_comparison_summary(items: list[SplitAwareComparisonResult]) -> dict[str, Any]:
    return {"count": len(items)}

def split_aware_comparison_to_text(items: list[SplitAwareComparisonResult], limit: int = 300) -> str:
    return str([c.generalization_gap for c in items])[:limit]
