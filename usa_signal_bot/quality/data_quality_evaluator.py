from typing import Any, Dict

def get_paper_observer_quality_dimensions(payload: Dict[str, Any]) -> Dict[str, Any]:
    dims = {
        "paper_observer_enrollment_quality_score": 100,
        "locked_observer_runtime_safety_score": 100,
        "parallel_monitoring_quality_score": 100,
        "observer_drift_detection_quality_score": 100,
        "observer_non_execution_safety_score": 100
    }

    # Mock integration logic
    if not payload.get("controlled_planning_review"):
        dims["paper_observer_enrollment_quality_score"] -= 20

    if payload.get("allow_active_paper") is True:
        dims["locked_observer_runtime_safety_score"] = 0
        dims["observer_non_execution_safety_score"] = 0

    if payload.get("drifts_detected", 0) > 0:
        dims["observer_drift_detection_quality_score"] += 10 # completeness

    return dims

def enrich_quality_scorecard_with_observer_dims(scorecard: Dict[str, Any], observer_payload: Dict[str, Any]) -> Dict[str, Any]:
    scorecard.update(get_paper_observer_quality_dimensions(observer_payload))
    return scorecard


def get_promotion_dossier_quality_dimensions(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "promotion_dossier_quality_score": 100,
        "final_safety_board_completeness_score": 100,
        "readiness_package_safety_score": 100,
        "evidence_index_quality_score": 100,
        "non_execution_compliance_score": 100
    }


def get_readiness_rehearsal_quality_dimensions(payload: Dict[str, Any]) -> Dict[str, Any]:
    dims = {
        "readiness_rehearsal_quality_score": 100,
        "stage_rehearsal_safety_score": 100,
        "final_review_lock_quality_score": 100,
        "guarded_handoff_registry_quality_score": 100,
        "handoff_evidence_completeness_score": 100
    }

    if payload.get("failed_stage_count", 0) > 0 or payload.get("blocked_stage_count", 0) > 0:
        dims["stage_rehearsal_safety_score"] -= 20
        dims["readiness_rehearsal_quality_score"] -= 10

    if payload.get("final_lock_valid") is True:
        dims["final_review_lock_quality_score"] = 100
    elif payload.get("final_lock_valid") is False:
        dims["final_review_lock_quality_score"] = 0
        dims["readiness_rehearsal_quality_score"] -= 20

    if payload.get("missing_evidence_count", 0) > 0:
        dims["handoff_evidence_completeness_score"] -= (10 * payload.get("missing_evidence_count", 1))

    if payload.get("has_active_paper_risk") or payload.get("has_broker_risk") or payload.get("has_config_patch_risk"):
        dims["stage_rehearsal_safety_score"] = 0
        dims["readiness_rehearsal_quality_score"] = 0
        dims["final_review_lock_quality_score"] = 0
        dims["guarded_handoff_registry_quality_score"] = 0

    return {k: max(0, min(100, v)) for k, v in dims.items()}

def enrich_quality_scorecard_with_readiness_rehearsal_dims(scorecard: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    scorecard.update(get_readiness_rehearsal_quality_dimensions(payload))
    return scorecard
