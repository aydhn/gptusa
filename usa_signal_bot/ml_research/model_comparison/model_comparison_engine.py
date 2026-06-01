from datetime import datetime, timezone
from typing import Any, List

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    ModelComparisonScore,
    MetricNormalizationResult,
    create_model_comparison_score_id
)

def build_model_comparison_scores(normalized_metrics: list[MetricNormalizationResult]) -> list[ModelComparisonScore]:
    artifacts = set(m.model_artifact_id for m in normalized_metrics if m.model_artifact_id)
    scores = []
    for art_id in artifacts:
        arts = [m for m in normalized_metrics if m.model_artifact_id == art_id]
        scores.append(build_model_score_for_artifact(art_id, arts))
    return scores

def build_model_score_for_artifact(model_artifact_id: str, rows: list[MetricNormalizationResult]) -> ModelComparisonScore:
    comp_scores = aggregate_component_scores(rows)
    overall = compute_overall_research_score(comp_scores)

    return ModelComparisonScore(
        score_id=create_model_comparison_score_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        experiment_id=rows[0].experiment_id if rows else None,
        model_artifact_id=model_artifact_id,
        model_name=f"model_{model_artifact_id}",
        score_kind="OVERALL_RESEARCH_SCORE",
        score_value=overall,
        component_scores=comp_scores,
        metric_result_ids=[m.result_id for m in rows],
        split_name="validation",
        research_only_rankable=True,
        non_trading_score=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def aggregate_component_scores(rows: list[MetricNormalizationResult]) -> dict[str, Any]:
    return {r.metric_name: r.normalized_value for r in rows if r.normalized_value is not None}

def compute_overall_research_score(component_scores: dict[str, Any]) -> float | None:
    if not component_scores:
        return None
    return sum(component_scores.values()) / len(component_scores)

def validate_model_comparison_scores(items: list[ModelComparisonScore]) -> list[str]:
    return []

def model_comparison_summary(items: list[ModelComparisonScore]) -> dict[str, Any]:
    return {"count": len(items)}

def model_comparison_to_text(items: list[ModelComparisonScore], limit: int = 300) -> str:
    return str([s.score_value for s in items])[:limit]
