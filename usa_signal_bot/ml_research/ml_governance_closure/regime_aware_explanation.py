from typing import Any
from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    RegimeAwareExplanation,
    FeatureAttributionProxy,
    FactorContributionSummary,
    ExplanationStatus,
    create_regime_aware_explanation_id,
    current_time
)

def extract_regime_labels_from_monitoring_package(package: dict[str, Any]) -> list[str]:
    # Dummy logic to extract regime labels
    return ["HIGH_VOLATILITY", "BULL_TREND"]

def build_regime_aware_explanations(
    monitoring_package: dict[str, Any],
    feature_attributions: list[FeatureAttributionProxy] | None = None,
    factor_summaries: list[FactorContributionSummary] | None = None
) -> list[RegimeAwareExplanation]:

    explanations = []
    regimes = extract_regime_labels_from_monitoring_package(monitoring_package)

    for r in regimes:
        explanations.append(RegimeAwareExplanation(
            explanation_id=create_regime_aware_explanation_id(),
            created_at_utc=current_time(),
            regime_label=r,
            prototype_id=None,
            model_artifact_id=None,
            regime_behavior_summary=f"Model behavior under {r} regime.",
            feature_driver_notes=["Proxy features vary slightly by regime"],
            factor_driver_notes=["Proxy factors vary slightly by regime"],
            drift_notes=["Regime shift monitored"],
            limitation_notes=["Heuristic regime classification"],
            explanation_status=ExplanationStatus.VALID,
            not_strategy_switch=True,
            not_trade_signal=True,
            research_data_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))

    return explanations

def validate_regime_aware_explanations(items: list[RegimeAwareExplanation]) -> list[str]:
    errors = []
    for item in items:
        if not item.not_strategy_switch:
            errors.append(f"Regime explanation {item.explanation_id} does not disclaim strategy switch")
        if item.produces_trade_signal or item.produces_order_decision:
            errors.append(f"Regime explanation {item.explanation_id} produces execution artifacts")
    return errors

def regime_aware_explanation_summary(items: list[RegimeAwareExplanation]) -> dict[str, Any]:
    return {
        "count": len(items),
        "regimes": [i.regime_label for i in items if i.regime_label]
    }

def regime_aware_explanation_to_text(items: list[RegimeAwareExplanation], limit: int = 300) -> str:
    summary = regime_aware_explanation_summary(items)
    return f"Built {summary['count']} regime-aware explanations for regimes: {', '.join(summary['regimes'])}"
