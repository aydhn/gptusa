from typing import Any
from .observer_governance_models import ObserverPaperComparisonReport, PromotionEvidenceRefresh, ObserverGovernanceGate, ObserverGovernanceDecisionResult, create_observer_governance_decision_id
from usa_signal_bot.core.enums import ObserverGovernanceDecision, ObserverGovernanceRiskFlag, ObserverGovernanceStatus
from datetime import datetime, timezone

class ObserverGovernanceDecisionBoard:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def decide(self, comparison_report: ObserverPaperComparisonReport, evidence_refresh: PromotionEvidenceRefresh, gates: list[ObserverGovernanceGate]) -> ObserverGovernanceDecisionResult:
        flags = self.collect_decision_risk_flags(comparison_report, evidence_refresh, gates)
        decision = ObserverGovernanceDecision.UNKNOWN
        status = ObserverGovernanceStatus.UNKNOWN

        if any(f in flags for f in [
            ObserverGovernanceRiskFlag.REAL_ORDER_RISK, ObserverGovernanceRiskFlag.PAPER_STATE_MUTATION_RISK,
            ObserverGovernanceRiskFlag.BROKER_ORDER_RISK, ObserverGovernanceRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
            ObserverGovernanceRiskFlag.ACTIVE_PAPER_ENABLE_RISK
        ]):
            decision = ObserverGovernanceDecision.BLOCK_OBSERVER_CANDIDATE
            status = ObserverGovernanceStatus.BLOCKED
        elif ObserverGovernanceRiskFlag.PAPER_BASELINE_MISSING in flags or ObserverGovernanceRiskFlag.OBSERVER_OUTPUT_MISSING in flags:
            decision = ObserverGovernanceDecision.REQUEST_MORE_OBSERVER_MONITORING
            status = ObserverGovernanceStatus.INSUFFICIENT_DATA
        elif ObserverGovernanceRiskFlag.EVIDENCE_MISSING in flags or ObserverGovernanceRiskFlag.EVIDENCE_STALE in flags:
            decision = ObserverGovernanceDecision.REQUEST_OBSERVATION_REVIEW_REFRESH
            status = ObserverGovernanceStatus.WARNING
        elif ObserverGovernanceRiskFlag.DRIFT_TOO_HIGH in flags:
            decision = ObserverGovernanceDecision.REQUEST_CONTROLLED_PLANNING_RETEST
            status = ObserverGovernanceStatus.WARNING
        else:
            decision = ObserverGovernanceDecision.ELIGIBLE_FOR_NON_EXECUTING_PROMOTION_DOSSIER
            status = ObserverGovernanceStatus.PASS

        return ObserverGovernanceDecisionResult(
            decision_id=create_observer_governance_decision_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            candidate_id=comparison_report.candidate_id,
            comparison_report_id=comparison_report.report_id,
            evidence_refresh_id=evidence_refresh.refresh_id,
            decision=decision, status=status, risk_flags=flags,
            rationale=self.rationale_for_decision(decision, flags),
            required_followups=self.followups_for_decision(decision, flags),
            manual_review_required=True, allowed_for_active_paper=False,
            allowed_for_broker_execution=False, allowed_for_paper_state_mutation=False,
            allowed_for_config_patch=False, warnings=[], errors=[]
        )

    def collect_decision_risk_flags(self, comparison_report: ObserverPaperComparisonReport, evidence_refresh: PromotionEvidenceRefresh, gates: list[ObserverGovernanceGate]) -> list[ObserverGovernanceRiskFlag]:
        flags = set(comparison_report.risk_flags)
        for g in gates:
            flags.update(g.risk_flags)
        return list(flags)

    def rationale_for_decision(self, decision: ObserverGovernanceDecision, flags: list[ObserverGovernanceRiskFlag]) -> str:
        return f"Decision {decision.value} based on flags: {[f.value for f in flags]}"

    def followups_for_decision(self, decision: ObserverGovernanceDecision, flags: list[ObserverGovernanceRiskFlag]) -> list[str]:
        if decision == ObserverGovernanceDecision.BLOCK_OBSERVER_CANDIDATE: return ["Immediate review required for safety flags."]
        return []

    def decision_allows_next_non_executing_stage(self, decision: ObserverGovernanceDecision) -> bool:
        return decision == ObserverGovernanceDecision.ELIGIBLE_FOR_NON_EXECUTING_PROMOTION_DOSSIER
