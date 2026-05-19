from typing import Optional
from datetime import datetime
from usa_signal_bot.research_governance.governance_models import (
    PromotionReview, DecisionBoardResult, ReleaseCandidatePackage,
    PromotionDecision, ReleaseCandidateStatus, create_release_candidate_package_id
)

def release_candidate_status_from_decision(decision: PromotionDecision) -> ReleaseCandidateStatus:
    if decision == PromotionDecision.ACCEPT_AS_LOCAL_RESEARCH_CANDIDATE:
        return ReleaseCandidateStatus.ACCEPTED_FOR_LOCAL_RESEARCH
    if decision in [PromotionDecision.REJECT, PromotionDecision.BLOCK]:
        return ReleaseCandidateStatus.REJECTED
    return ReleaseCandidateStatus.REVIEW_READY

def build_release_candidate_from_promotion_review(review: PromotionReview, board_result: Optional[DecisionBoardResult] = None) -> ReleaseCandidatePackage:
    decision = board_result.final_decision if board_result else review.proposed_decision
    status = release_candidate_status_from_decision(decision)

    return ReleaseCandidatePackage(
        candidate_id=create_release_candidate_package_id(),
        created_at_utc=datetime.utcnow().isoformat(),
        experiment_id=review.experiment_id,
        hypothesis_id=review.hypothesis_id,
        source_review_id=review.review_id,
        status=status,
        title=f"Release Candidate for Exp {review.experiment_id}",
        description="Auto-generated local research candidate",
        candidate_config_ref=None,
        baseline_config_ref=None,
        included_artifacts=release_candidate_artifact_refs(review),
        evidence_pack_id=review.evidence_pack.evidence_pack_id if review.evidence_pack else None,
        promotion_decision=decision,
        manual_review_required=True,
        allowed_for_auto_apply=False,
        allowed_for_live_or_demo_execution=False,
        warnings=release_candidate_safety_warnings(None),
        errors=[]
    )

def release_candidate_artifact_refs(review: PromotionReview) -> list[str]:
    return []

def release_candidate_safety_warnings(candidate: Optional[ReleaseCandidatePackage]) -> list[str]:
    return ["This candidate is for local research only. It is not an approval for live trading."]

def release_candidate_to_text(candidate: ReleaseCandidatePackage) -> str:
    return f"Release Candidate: {candidate.status.value}"
