from typing import Any, Dict, List, Optional
from .phase142_models import (
    EnsembleCandidateReference,
    EnsembleCandidateKind,
    create_ensemble_candidate_reference_id,
    validate_ensemble_candidate_reference,
    _now
)

def build_candidate_reference_from_report(report: Dict[str, Any], validation: Optional[Dict[str, Any]] = None, prediction_artifact: Optional[Dict[str, Any]] = None) -> EnsembleCandidateReference:

    passed_validation = True
    if validation and not validation.get('passed', False):
        passed_validation = False

    candidate = EnsembleCandidateReference(
        candidate_ref_id=create_ensemble_candidate_reference_id(),
        created_at_utc=_now(),
        candidate_kind=EnsembleCandidateKind.CALIBRATION_AWARE_CANDIDATE,
        source_candidate_id=report.get('candidate_id'),
        model_artifact_id=report.get('model_artifact_id'),
        experiment_id=report.get('experiment_id'),
        model_name=report.get('model_name', "Unknown"),
        rank=report.get('rank'),
        diagnostics_report_id=report.get('report_id'),
        prediction_artifact_id=prediction_artifact.get('artifact_id') if prediction_artifact else None,
        evaluation_report_id=None,
        reliability_score=report.get('reliability_score'),
        calibration_warning_count=report.get('warning_count', 0),
        post_training_validation_passed=passed_validation,
        eligible_for_ensemble_research=passed_validation,
        eligible_for_live_use=False,
        eligible_for_paper_use=False,
        eligible_for_broker_use=False,
        eligible_for_deployment=False,
        eligible_for_strategy_activation=False,
        research_data_only=True,
        offline_ml_research_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    val_errs = validate_ensemble_candidate_reference(candidate)
    if val_errs:
        candidate.errors.extend(val_errs)
        candidate.eligible_for_ensemble_research = False

    return candidate

def build_ensemble_candidate_references(diagnostics_reports: List[Dict[str, Any]], post_training_validations: Optional[List[Dict[str, Any]]] = None, prediction_artifacts: Optional[List[Dict[str, Any]]] = None) -> List[EnsembleCandidateReference]:
    res = []

    val_map = {v.get('candidate_id'): v for v in (post_training_validations or [])}
    pred_map = {p.get('candidate_id'): p for p in (prediction_artifacts or [])}

    for r in diagnostics_reports:
        cid = r.get('candidate_id')
        res.append(build_candidate_reference_from_report(r, val_map.get(cid), pred_map.get(cid)))

    return res

def validate_ensemble_candidate_references(items: List[EnsembleCandidateReference]) -> List[str]:
    errs = []
    for item in items:
        errs.extend(validate_ensemble_candidate_reference(item))
    return errs

def ensemble_candidate_resolver_summary(items: List[EnsembleCandidateReference]) -> Dict[str, Any]:
    return {"count": len(items)}

def ensemble_candidate_resolver_to_text(items: List[EnsembleCandidateReference], limit: int = 300) -> str:
    return f"Resolved {len(items)} ensemble candidates"
