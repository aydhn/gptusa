from typing import Any
import hashlib
import json

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    ExplainabilityReport,
    ExplainabilityInputReference,
    FeatureAttributionProxy,
    FactorContributionSummary,
    ModelBehaviorExplanation,
    RegimeAwareExplanation,
    CalibrationAwareExplanation,
    EnsembleExplanation,
    MLClosureQuality,
    create_explainability_report_id,
    current_time
)

def compute_explainability_report_hash(report: ExplainabilityReport) -> str:
    # A simple deterministic hash of the IDs of the contents
    components = (
        [i.input_ref_id for i in report.input_references] +
        [i.attribution_id for i in report.feature_attributions] +
        [i.summary_id for i in report.factor_summaries] +
        [i.explanation_id for i in report.behavior_explanations] +
        [i.explanation_id for i in report.regime_explanations] +
        [i.explanation_id for i in report.calibration_explanations] +
        [i.explanation_id for i in report.ensemble_explanations]
    )
    content_str = json.dumps(components, sort_keys=True)
    return hashlib.sha256(content_str.encode("utf-8")).hexdigest()

def build_explainability_report(
    input_references: list[ExplainabilityInputReference],
    feature_attributions: list[FeatureAttributionProxy],
    factor_summaries: list[FactorContributionSummary],
    behavior_explanations: list[ModelBehaviorExplanation],
    regime_explanations: list[RegimeAwareExplanation],
    calibration_explanations: list[CalibrationAwareExplanation],
    ensemble_explanations: list[EnsembleExplanation]
) -> ExplainabilityReport:

    report = ExplainabilityReport(
        report_id=create_explainability_report_id(),
        created_at_utc=current_time(),
        input_references=input_references,
        feature_attributions=feature_attributions,
        factor_summaries=factor_summaries,
        behavior_explanations=behavior_explanations,
        regime_explanations=regime_explanations,
        calibration_explanations=calibration_explanations,
        ensemble_explanations=ensemble_explanations,
        report_hash=None, # Computed below
        report_valid=True,
        quality=MLClosureQuality.HIGH,
        explainability_metadata_only=True,
        heavy_dependency_used=False,
        shap_lime_dependency_used=False,
        research_data_only=True,
        offline_ml_research_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        live_inference_enabled=False,
        live_monitoring_enabled=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    report.report_hash = compute_explainability_report_hash(report)
    return report

def validate_explainability_report(report: ExplainabilityReport) -> list[str]:
    errors = []
    if not report.explainability_metadata_only:
        errors.append("Report must be marked explainability_metadata_only")
    if report.heavy_dependency_used:
        errors.append("Report indicates heavy dependencies used (e.g. sklearn, torch, etc)")
    if report.shap_lime_dependency_used:
        errors.append("Report indicates SHAP/LIME used")
    if report.activation_allowed or report.strategy_activation_allowed or report.deployment_allowed:
        errors.append("Report allows activation/deployment")
    if report.live_inference_enabled or report.live_monitoring_enabled:
        errors.append("Report enables live inference/monitoring")
    if report.produces_trade_signal or report.produces_order_decision or report.produces_portfolio_weights:
        errors.append("Report produces execution artifacts")
    if report.investment_advice:
        errors.append("Report marked as investment advice")
    return errors

def explainability_report_summary(report: ExplainabilityReport) -> dict[str, Any]:
    return {
        "report_id": report.report_id,
        "valid": report.report_valid,
        "input_count": len(report.input_references),
        "feature_attribution_count": len(report.feature_attributions),
        "factor_summary_count": len(report.factor_summaries),
        "behavior_explanations_count": len(report.behavior_explanations),
        "regime_explanations_count": len(report.regime_explanations),
        "calibration_explanations_count": len(report.calibration_explanations),
        "ensemble_explanations_count": len(report.ensemble_explanations)
    }

def explainability_report_to_text(report: ExplainabilityReport, limit: int = 300) -> str:
    summary = explainability_report_summary(report)
    return (
        f"Explainability Report {summary['report_id']} - Valid: {summary['valid']}\n"
        f"  Features: {summary['feature_attribution_count']}, Factors: {summary['factor_summary_count']}\n"
        f"  Behaviors: {summary['behavior_explanations_count']}, Regimes: {summary['regime_explanations_count']}\n"
        f"  Calibrations: {summary['calibration_explanations_count']}, Ensembles: {summary['ensemble_explanations_count']}"
    )
