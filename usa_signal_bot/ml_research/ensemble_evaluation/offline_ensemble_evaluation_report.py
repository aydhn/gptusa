from typing import Any, Dict, List
import datetime
import json
import hashlib

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    OfflineEnsembleEvaluationReport,
    create_offline_ensemble_evaluation_report_id,
    EnsemblePrototypeSpec,
    OfflineEnsemblePredictionArtifact,
    OfflineEnsembleEvaluationMetricResult,
    BlendContributionDiagnostic,
    CandidateAgreementDiagnostic,
    EnsembleCandidateComparisonResult,
    EnsemblePrototypeQuality
)

def build_offline_ensemble_evaluation_reports(
    specs: List[EnsemblePrototypeSpec],
    prediction_artifacts: List[OfflineEnsemblePredictionArtifact],
    metric_results: List[OfflineEnsembleEvaluationMetricResult],
    blend_diagnostics: List[BlendContributionDiagnostic],
    agreement_diagnostics: List[CandidateAgreementDiagnostic],
    comparisons: List[EnsembleCandidateComparisonResult]
) -> List[OfflineEnsembleEvaluationReport]:

    reports = []
    for spec in specs:
        reports.append(build_offline_ensemble_evaluation_report_for_spec(
            spec, prediction_artifacts, metric_results, blend_diagnostics, agreement_diagnostics, comparisons
        ))
    return reports

def build_offline_ensemble_evaluation_report_for_spec(
    spec: EnsemblePrototypeSpec,
    prediction_artifacts: List[OfflineEnsemblePredictionArtifact],
    metric_results: List[OfflineEnsembleEvaluationMetricResult],
    blend_diagnostics: List[BlendContributionDiagnostic],
    agreement_diagnostics: List[CandidateAgreementDiagnostic],
    comparisons: List[EnsembleCandidateComparisonResult]
) -> OfflineEnsembleEvaluationReport:

    preds = [p for p in prediction_artifacts if p.prototype_id == spec.prototype_id]
    mets = [m for m in metric_results if m.prototype_id == spec.prototype_id]
    b_diag = [d for d in blend_diagnostics if d.prototype_id == spec.prototype_id]
    a_diag = [a for a in agreement_diagnostics if a.prototype_id == spec.prototype_id]
    comp = [c for c in comparisons if c.prototype_id == spec.prototype_id]

    report = OfflineEnsembleEvaluationReport(
        report_id=create_offline_ensemble_evaluation_report_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        prototype_id=spec.prototype_id,
        prediction_ids=[p.prediction_id for p in preds],
        metric_results=mets,
        blend_diagnostics=b_diag,
        agreement_diagnostics=a_diag,
        candidate_comparisons=comp,
        train_metric_count=sum(1 for m in mets if m.split_name == "train"),
        validation_metric_count=sum(1 for m in mets if m.split_name == "validation"),
        test_metric_count=sum(1 for m in mets if m.split_name == "test"),
        report_hash=None,
        report_valid=True,
        quality=EnsemblePrototypeQuality.ACCEPTABLE,
        offline_evaluation_only=True,
        research_data_only=True,
        offline_ml_research_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        live_inference_enabled=False,
        online_inference_enabled=False,
        threshold_optimization_performed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    report.report_hash = compute_offline_ensemble_evaluation_report_hash(report)
    return report

def compute_offline_ensemble_evaluation_report_hash(report: OfflineEnsembleEvaluationReport) -> str:
    s = f"{report.prototype_id}_{len(report.metric_results)}_{len(report.prediction_ids)}"
    return hashlib.sha256(s.encode()).hexdigest()

def validate_offline_ensemble_evaluation_reports(items: List[OfflineEnsembleEvaluationReport]) -> List[str]:
    errors = []
    for r in items:
        if not r.offline_evaluation_only:
             errors.append("not offline only")
    return errors

def offline_ensemble_evaluation_report_summary(items: List[OfflineEnsembleEvaluationReport]) -> Dict[str, Any]:
    return {"report_count": len(items)}

def offline_ensemble_evaluation_report_to_text(items: List[OfflineEnsembleEvaluationReport], limit: int = 300) -> str:
    return str(offline_ensemble_evaluation_report_summary(items))
