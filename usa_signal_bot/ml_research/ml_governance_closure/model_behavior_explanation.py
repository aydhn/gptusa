from typing import Any
from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    ModelBehaviorExplanation,
    FeatureAttributionProxy,
    FactorContributionSummary,
    ExplanationScope,
    ExplanationStatus,
    create_model_behavior_explanation_id,
    current_time
)

def build_behavior_summary_text(feature_attributions: list[FeatureAttributionProxy], factor_summaries: list[FactorContributionSummary]) -> str:
    top_features = [f.feature_name for f in feature_attributions if f.rank and f.rank <= 3]
    top_factors = [f.factor_name for f in factor_summaries if f.contribution_rank and f.contribution_rank <= 2]

    parts = ["This model relies on multiple factors and features."]
    if top_factors:
        parts.append(f"Key factor drivers include {', '.join(top_factors)}.")
    if top_features:
        parts.append(f"Key feature proxies include {', '.join(top_features)}.")
    return " ".join(parts)

def build_model_behavior_explanations(
    feature_attributions: list[FeatureAttributionProxy],
    factor_summaries: list[FactorContributionSummary],
    monitoring_package: dict[str, Any] | None = None
) -> list[ModelBehaviorExplanation]:

    top_drivers = [f.feature_name for f in feature_attributions if f.rank and f.rank <= 5]

    exp = ModelBehaviorExplanation(
        explanation_id=create_model_behavior_explanation_id(),
        created_at_utc=current_time(),
        model_artifact_id=None,
        prototype_id=None,
        scope=ExplanationScope.MODEL_LEVEL,
        behavior_summary=build_behavior_summary_text(feature_attributions, factor_summaries),
        key_drivers=top_drivers,
        known_limitations=["No live inference capability", "Not investment advice"],
        drift_sensitivity_notes=["Monitored via Phase 144 baseline"],
        calibration_notes=["Metadata summary only"],
        regime_notes=["Derived from Phase 131 heuristics"],
        explanation_status=ExplanationStatus.VALID,
        not_investment_advice=True,
        not_trade_signal=True,
        not_deployment_artifact=True,
        research_data_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    return [exp]

def validate_model_behavior_explanations(items: list[ModelBehaviorExplanation]) -> list[str]:
    errors = []
    for item in items:
        if not item.not_investment_advice:
            errors.append(f"Explanation {item.explanation_id} does not disclaim investment advice")
        if not item.not_trade_signal:
            errors.append(f"Explanation {item.explanation_id} does not disclaim trade signal")
        if item.investment_advice or item.produces_trade_signal or item.produces_order_decision or item.produces_portfolio_weights:
            errors.append(f"Explanation {item.explanation_id} produces execution artifacts")
    return errors

def model_behavior_explanation_summary(items: list[ModelBehaviorExplanation]) -> dict[str, Any]:
    return {
        "count": len(items),
        "valid_count": len([i for i in items if i.explanation_status == ExplanationStatus.VALID])
    }

def model_behavior_explanation_to_text(items: list[ModelBehaviorExplanation], limit: int = 300) -> str:
    summary = model_behavior_explanation_summary(items)
    return f"Built {summary['count']} model behavior explanations."
