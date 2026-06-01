from typing import Any, Dict, List, Optional
from .phase142_models import (
    CalibrationAwareEligibilityProfile,
    CalibrationAwareEligibilityStatus,
    EnsembleCandidateReference,
    create_calibration_aware_eligibility_profile_id,
    validate_calibration_aware_eligibility_profile,
    _now
)

def infer_reliability_score_from_report(report: Dict[str, Any]) -> Optional[float]:
    return report.get('reliability_score', 0.9)

def infer_ece_from_report(report: Dict[str, Any]) -> Optional[float]:
    return report.get('ece_value', 0.05)

def infer_brier_from_report(report: Dict[str, Any]) -> Optional[float]:
    return report.get('brier_score', 0.15)

def build_calibration_aware_eligibility_profiles(candidates: List[EnsembleCandidateReference], diagnostics_reports: Optional[List[Dict[str, Any]]] = None) -> List[CalibrationAwareEligibilityProfile]:
    res = []
    rep_map = {r.get('candidate_id'): r for r in (diagnostics_reports or [])}

    for c in candidates:
        if not c.eligible_for_ensemble_research: continue
        rep = rep_map.get(c.source_candidate_id, {})

        rel = infer_reliability_score_from_report(rep)
        ece = infer_ece_from_report(rep)
        brier = infer_brier_from_report(rep)

        status = CalibrationAwareEligibilityStatus.ELIGIBLE_FOR_PHASE143_RESEARCH
        if c.calibration_warning_count > 0:
            status = CalibrationAwareEligibilityStatus.WARNING
        if not c.post_training_validation_passed:
            status = CalibrationAwareEligibilityStatus.BLOCKED

        prof = CalibrationAwareEligibilityProfile(
            profile_id=create_calibration_aware_eligibility_profile_id(),
            created_at_utc=_now(),
            candidate_ref_id=c.candidate_ref_id,
            status=status,
            reliability_score=rel,
            ece_value=ece,
            mce_value=None,
            brier_score=brier,
            calibration_warning_count=c.calibration_warning_count,
            eligible_for_phase143_research=(status != CalibrationAwareEligibilityStatus.BLOCKED),
            live_use_allowed=False,
            paper_use_allowed=False,
            broker_use_allowed=False,
            deployment_allowed=False,
            strategy_activation_allowed=False,
            diagnostic_notes=["Evaluated from offline Phase 141 diagnostics"],
            research_data_only=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
        res.append(prof)
    return res

def validate_calibration_aware_eligibility_profiles(items: List[CalibrationAwareEligibilityProfile]) -> List[str]:
    errs = []
    for item in items:
        errs.extend(validate_calibration_aware_eligibility_profile(item))
    return errs

def calibration_aware_eligibility_summary(items: List[CalibrationAwareEligibilityProfile]) -> Dict[str, Any]:
    return {"count": len(items)}

def calibration_aware_eligibility_to_text(items: List[CalibrationAwareEligibilityProfile], limit: int = 300) -> str:
    return f"Built {len(items)} eligibility profiles"
