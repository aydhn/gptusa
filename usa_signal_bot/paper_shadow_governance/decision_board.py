from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import (
    ShadowGovernanceDecision, ShadowComparisonOutcome, ShadowAcceptanceStatus, ShadowGovernanceRiskFlag
)
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowDecisionBoardResult, ShadowAcceptanceScorecard, ShadowSessionComparisonReport,
    create_shadow_decision_board_result_id, utc_now_iso
)

class ShadowRehearsalDecisionBoard:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def collect_decision_risk_flags(self, scorecard: ShadowAcceptanceScorecard, report: Optional[ShadowSessionComparisonReport] = None) -> List[ShadowGovernanceRiskFlag]:
        return scorecard.risk_flags

    def rationale_for_decision(self, decision: ShadowGovernanceDecision, flags: List[ShadowGovernanceRiskFlag]) -> str:
        if decision == ShadowGovernanceDecision.BLOCK_SHADOW_CANDIDATE:
            return "Blocked due to critical safety risks."
        return f"Decision: {decision.value}"

    def followups_for_decision(self, decision: ShadowGovernanceDecision, flags: List[ShadowGovernanceRiskFlag]) -> List[str]:
        return ["Review manually"]

    def decide_from_scorecard(self, scorecard: ShadowAcceptanceScorecard, outcome: ShadowComparisonOutcome) -> ShadowDecisionBoardResult:
        flags = self.collect_decision_risk_flags(scorecard)
        if scorecard.overall_status == ShadowAcceptanceStatus.BLOCKED:
            dec = ShadowGovernanceDecision.BLOCK_SHADOW_CANDIDATE
        elif scorecard.overall_status == ShadowAcceptanceStatus.FAIL:
            dec = ShadowGovernanceDecision.REJECT_SHADOW_CANDIDATE
        elif scorecard.overall_status == ShadowAcceptanceStatus.INSUFFICIENT_DATA:
            dec = ShadowGovernanceDecision.REQUEST_MORE_SHADOW_DATA
        elif outcome == ShadowComparisonOutcome.CANDIDATE_BETTER and scorecard.overall_status == ShadowAcceptanceStatus.PASS:
            dec = ShadowGovernanceDecision.ACCEPT_AS_SANDBOXED_PAPER_CANDIDATE
        else:
            dec = ShadowGovernanceDecision.ACCEPT_FOR_MORE_SHADOW_TESTING

        return ShadowDecisionBoardResult(
            decision_id=create_shadow_decision_board_result_id(),
            created_at_utc=utc_now_iso(),
            comparison_report_id=None,
            scorecard_id=scorecard.scorecard_id,
            decision=dec,
            outcome=outcome,
            acceptance_status=scorecard.overall_status,
            risk_flags=flags,
            rationale=self.rationale_for_decision(dec, flags),
            required_followups=self.followups_for_decision(dec, flags),
            manual_review_required=True,
            allowed_for_real_orders=False,
            allowed_for_paper_state_mutation=False,
            allowed_for_telegram_real_send=False,
            allowed_for_production_config_write=False,
            warnings=[], errors=[]
        )

    def decide_from_comparison(self, report: ShadowSessionComparisonReport) -> ShadowDecisionBoardResult:
        if not report.acceptance_scorecard:
            raise ValueError("Comparison report must have an acceptance scorecard.")
        res = self.decide_from_scorecard(report.acceptance_scorecard, report.outcome)
        res.comparison_report_id = report.report_id
        return res
