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
