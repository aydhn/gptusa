from typing import List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    FinalSafetyBoardDecision,
    FinalSafetyBoardStatus,
    PromotionDossierRiskFlag,
    ReadinessGateStatus
)
from .dossier_models import (
    ObserverPromotionDossier,
    FinalSafetyBoardGate,
    PromotionRiskRegisterItem,
    FinalSafetyBoardReview,
    create_final_safety_board_review_id
)

class FinalSafetyBoardDecisionEngine:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def decide(self, dossier: ObserverPromotionDossier, gates: List[FinalSafetyBoardGate], risk_register: Optional[List[PromotionRiskRegisterItem]] = None) -> FinalSafetyBoardReview:
        flags = self.collect_board_risk_flags(dossier, gates)

        decision = FinalSafetyBoardDecision.PASS_FOR_STAGED_NON_EXECUTING_READINESS_PACKAGE
        if PromotionDossierRiskFlag.EVIDENCE_MISSING in flags or PromotionDossierRiskFlag.EVIDENCE_STALE in flags:
            decision = FinalSafetyBoardDecision.REQUEST_MORE_EVIDENCE
        if PromotionDossierRiskFlag.MANUAL_REVIEW_MISSING in flags:
            decision = FinalSafetyBoardDecision.REQUEST_MANUAL_REVIEW

        blocking_flags = [
            PromotionDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
            PromotionDossierRiskFlag.PAPER_STATE_MUTATION_RISK,
            PromotionDossierRiskFlag.PAPER_ORDER_RISK,
            PromotionDossierRiskFlag.BROKER_ORDER_RISK,
            PromotionDossierRiskFlag.TELEGRAM_REAL_SEND_RISK,
            PromotionDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK
        ]

        for flag in blocking_flags:
            if flag in flags:
                decision = FinalSafetyBoardDecision.BLOCK_DOSSIER
                break

        status = FinalSafetyBoardStatus.PASSED_FOR_STAGED_NON_EXECUTING_READINESS
        if decision in [FinalSafetyBoardDecision.BLOCK_DOSSIER, FinalSafetyBoardDecision.REJECT_DOSSIER]:
            status = FinalSafetyBoardStatus.BLOCKED
        elif decision in [FinalSafetyBoardDecision.REQUEST_MORE_EVIDENCE, FinalSafetyBoardDecision.REQUEST_MANUAL_REVIEW, FinalSafetyBoardDecision.REQUEST_OBSERVER_RETEST]:
            status = FinalSafetyBoardStatus.REQUEST_CHANGES

        return FinalSafetyBoardReview(
            board_review_id=create_final_safety_board_review_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=status,
            dossier_id=dossier.dossier_id,
            candidate_id=dossier.candidate_id,
            gates=gates,
            risk_register=risk_register or [],
            decision=decision,
            rationale=self.rationale_for_board_decision(decision, flags),
            required_followups=self.followups_for_board_decision(decision, flags),
            manual_review_required=True,
            allowed_for_active_paper=False,
            allowed_for_broker_execution=False,
            allowed_for_paper_state_mutation=False,
            allowed_for_config_patch=False,
            warnings=[],
            errors=[]
        )

    def collect_board_risk_flags(self, dossier: ObserverPromotionDossier, gates: List[FinalSafetyBoardGate]) -> List[PromotionDossierRiskFlag]:
        flags = set(dossier.safety_flags)
        for g in gates:
            if g.status == ReadinessGateStatus.FAIL:
                for f in g.risk_flags:
                    flags.add(f)
        return list(flags)

    def rationale_for_board_decision(self, decision: FinalSafetyBoardDecision, flags: List[PromotionDossierRiskFlag]) -> str:
        if decision == FinalSafetyBoardDecision.BLOCK_DOSSIER:
            return f"Blocked due to execution risk flags: {[f.value for f in flags]}"
        elif decision == FinalSafetyBoardDecision.REQUEST_MORE_EVIDENCE:
            return "Requested more evidence due to missing or stale components."
        elif decision == FinalSafetyBoardDecision.PASS_FOR_STAGED_NON_EXECUTING_READINESS_PACKAGE:
            return "Passed gates. Proceeding to NON-EXECUTING readiness package."
        return "Manual review required or inconclusive."

    def followups_for_board_decision(self, decision: FinalSafetyBoardDecision, flags: List[PromotionDossierRiskFlag]) -> List[str]:
        if decision == FinalSafetyBoardDecision.PASS_FOR_STAGED_NON_EXECUTING_READINESS_PACKAGE:
            return ["Proceed to create staged non-executing readiness package."]
        return ["Address missing evidence or safety risks."]
