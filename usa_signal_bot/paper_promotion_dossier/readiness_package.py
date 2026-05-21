from typing import Any, Dict, List
from datetime import datetime, timezone
from usa_signal_bot.core.enums import ReadinessPackageStatus, FinalSafetyBoardDecision
from .dossier_models import (
    ObserverPromotionDossier,
    FinalSafetyBoardReview,
    StagedPaperReadinessPackage,
    create_staged_readiness_package_id
)
from .readiness_stage_plan import default_readiness_stage_plans

def build_staged_paper_readiness_package(dossier: ObserverPromotionDossier, board_review: FinalSafetyBoardReview) -> StagedPaperReadinessPackage:
    status = ReadinessPackageStatus.CREATED
    if board_review.decision != FinalSafetyBoardDecision.PASS_FOR_STAGED_NON_EXECUTING_READINESS_PACKAGE:
        status = ReadinessPackageStatus.BLOCKED

    stage_plans = default_readiness_stage_plans(dossier)

    return StagedPaperReadinessPackage(
        package_id=create_staged_readiness_package_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        dossier_id=dossier.dossier_id,
        board_review_id=board_review.board_review_id,
        candidate_id=dossier.candidate_id,
        stage_plans=stage_plans,
        evidence_refs=dossier.evidence_index.evidence_refs if dossier.evidence_index else [],
        safety_flags=dossier.safety_flags,
        package_summary={"stage_count": len(stage_plans)},
        allowed_for_active_paper=False,
        allowed_for_broker_execution=False,
        allowed_for_paper_state_mutation=False,
        allowed_for_config_patch=False,
        warnings=[],
        errors=[]
    )

def validate_readiness_package_safety(package: StagedPaperReadinessPackage) -> List[str]:
    warnings = []
    if package.allowed_for_active_paper: warnings.append("Package illegally enables active paper.")
    if package.allowed_for_broker_execution: warnings.append("Package illegally enables broker execution.")
    if package.allowed_for_paper_state_mutation: warnings.append("Package illegally enables paper state mutation.")
    if package.allowed_for_config_patch: warnings.append("Package illegally enables config patch.")
    return warnings

def readiness_package_summary(package: StagedPaperReadinessPackage) -> Dict[str, Any]:
    return {
        "package_id": package.package_id,
        "status": package.status.value,
        "stage_count": len(package.stage_plans),
        "allowed_for_active_paper": package.allowed_for_active_paper
    }

def readiness_package_to_text(package: StagedPaperReadinessPackage) -> str:
    return f"Readiness Package {package.package_id}. Status: {package.status.value}. Stages: {len(package.stage_plans)}."
