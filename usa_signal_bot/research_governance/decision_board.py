from typing import Any
from datetime import datetime
from usa_signal_bot.research_governance.governance_models import (
    GovernanceEvidencePack, PromotionReview, DecisionBoardResult, DecisionBoardMode,
    PromotionDecision, PromotionEligibility, GovernanceRiskFlag, GovernanceChecklistItem,
    GovernanceReviewStatus, create_promotion_review_id, create_decision_board_result_id
)
from usa_signal_bot.research_governance.evidence_pack import build_evidence_pack_from_comparison_report
from usa_signal_bot.research_governance.eligibility_scoring import calculate_promotion_eligibility_score, classify_promotion_eligibility
from usa_signal_bot.research_governance.leakage_overfit_review import review_leakage_overfit_flags, leakage_overfit_risk_flags

class GovernanceDecisionBoard:
    def __init__(self, mode: DecisionBoardMode = DecisionBoardMode.CONSERVATIVE):
        self.mode = mode

    def build_checklist(self, evidence_pack: GovernanceEvidencePack, comparison_payload: dict[str, Any]) -> list[GovernanceChecklistItem]:
        checklist = []
        checklist.extend(review_leakage_overfit_flags(comparison_payload, evidence_pack))
        return checklist

    def collect_risk_flags(self, evidence_pack: GovernanceEvidencePack, checklist_items: list[GovernanceChecklistItem]) -> list[GovernanceRiskFlag]:
        flags = []
        for item in checklist_items:
            flags.extend(item.risk_flags)
        return flags

    def review_comparison_report(self, comparison_payload: dict[str, Any]) -> PromotionReview:
        evidence_pack = build_evidence_pack_from_comparison_report(comparison_payload)
        checklist = self.build_checklist(evidence_pack, comparison_payload)
        flags = self.collect_risk_flags(evidence_pack, checklist)

        score = calculate_promotion_eligibility_score(evidence_pack, checklist)
        eligibility = classify_promotion_eligibility(score, flags)

        decision = PromotionDecision.REJECT
        if eligibility == PromotionEligibility.ELIGIBLE:
            decision = PromotionDecision.ACCEPT_AS_LOCAL_RESEARCH_CANDIDATE
        elif eligibility == PromotionEligibility.BLOCKED:
            decision = PromotionDecision.BLOCK
        elif eligibility == PromotionEligibility.INSUFFICIENT_DATA:
            decision = PromotionDecision.REQUEST_MORE_DATA
        elif eligibility == PromotionEligibility.CONDITIONALLY_ELIGIBLE:
            decision = PromotionDecision.APPROVE_FOR_MORE_RESEARCH

        # Hard block if leakage fail
        if GovernanceRiskFlag.POSSIBLE_LEAKAGE in flags:
            decision = PromotionDecision.BLOCK

        return PromotionReview(
            review_id=create_promotion_review_id(),
            created_at_utc=datetime.utcnow().isoformat(),
            experiment_id=comparison_payload.get("experiment_id"),
            hypothesis_id=comparison_payload.get("hypothesis_id"),
            status=GovernanceReviewStatus.COMPLETED,
            eligibility=eligibility,
            proposed_decision=decision,
            eligibility_score=score,
            evidence_pack=evidence_pack,
            checklist_items=checklist,
            risk_flags=flags,
            manual_review_required=True,
            allowed_for_auto_promotion=False,
            allowed_for_config_patch=False,
            allowed_for_order_routing=False,
            rationale="Automated local governance review",
            warnings=[], errors=[]
        )

    def decide(self, review: PromotionReview) -> DecisionBoardResult:
        decision = review.proposed_decision
        flags = review.risk_flags

        # apply stricter mode rules if necessary
        if self.mode == DecisionBoardMode.CONSERVATIVE and decision == PromotionDecision.APPROVE_FOR_MORE_RESEARCH:
            decision = PromotionDecision.REQUEST_MORE_DATA

        return DecisionBoardResult(
            board_result_id=create_decision_board_result_id(),
            created_at_utc=datetime.utcnow().isoformat(),
            mode=self.mode,
            review_id=review.review_id,
            candidate_id=None,
            final_decision=decision,
            eligibility=review.eligibility,
            passed_check_count=sum(1 for c in review.checklist_items if c.status.value == "PASS"),
            warning_check_count=sum(1 for c in review.checklist_items if c.status.value == "WARNING"),
            failed_check_count=sum(1 for c in review.checklist_items if c.status.value == "FAIL"),
            risk_flags=flags,
            rationale="Decision based on eligibility",
            required_followups=self.required_followups_for_decision(decision, flags),
            allowed_for_auto_promotion=False,
            allowed_for_config_patch=False,
            allowed_for_order_routing=False,
            warnings=[], errors=[]
        )

    def final_decision_from_review(self, review: PromotionReview) -> PromotionDecision:
        return self.decide(review).final_decision

    def required_followups_for_decision(self, decision: PromotionDecision, flags: list[GovernanceRiskFlag]) -> list[str]:
        return ["manual_review"]
