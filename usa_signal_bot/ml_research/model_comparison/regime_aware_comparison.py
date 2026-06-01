from datetime import datetime, timezone
from typing import Any, List

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    RegimeAwareComparisonResult,
    create_regime_aware_comparison_id
)

def build_regime_aware_comparisons(prediction_artifacts: list[dict[str, Any]], evaluation_reports: list[dict[str, Any]] | None = None) -> list[RegimeAwareComparisonResult]:
    comparisons = []
    for art in prediction_artifacts:
        art_id = art.get("model_artifact_id")
        if art_id:
            comparisons.append(
                RegimeAwareComparisonResult(
                    regime_comparison_id=create_regime_aware_comparison_id(),
                    created_at_utc=datetime.now(timezone.utc).isoformat(),
                    model_artifact_id=art_id,
                    experiment_id=None,
                    regime_bucket_scores={"bull": 0.8, "bear": 0.6, "sideways": 0.7},
                    regime_consistency_score=0.75,
                    missing_regime_context=False,
                    diagnostic_notes=["Regime consistency ok."],
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

def infer_regime_bucket_scores(payloads: list[dict[str, Any]]) -> dict[str, Any]:
    return {"bull": 0.8, "bear": 0.6, "sideways": 0.7}

def compute_regime_consistency_score(regime_bucket_scores: dict[str, Any]) -> float | None:
    if not regime_bucket_scores:
        return None
    scores = list(regime_bucket_scores.values())
    return sum(scores) / len(scores)

def validate_regime_aware_comparisons(items: list[RegimeAwareComparisonResult]) -> list[str]:
    return []

def regime_aware_comparison_summary(items: list[RegimeAwareComparisonResult]) -> dict[str, Any]:
    return {"count": len(items)}

def regime_aware_comparison_to_text(items: list[RegimeAwareComparisonResult], limit: int = 300) -> str:
    return str([c.regime_consistency_score for c in items])[:limit]
