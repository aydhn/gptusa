
from typing import Any, List, Optional
import datetime
from usa_signal_bot.core.enums import PaperReadinessBoardDecision, PaperReadinessBoardRiskFlag, PaperReadinessBoardStatus, ReadinessBoardGateStatus
from usa_signal_bot.paper_readiness_board.readiness_board_models import (
    PaperReadinessBoardReview, PaperReadinessBoardGate, WriteBlockedRuntimeAdapterProof, ActivationFirewallEvent,
    create_board_review_id, validate_paper_readiness_board_review
)
from usa_signal_bot.paper_readiness_board.eligibility_checker import evaluate_paper_readiness_board_eligibility, board_status_from_decision

class PaperReadinessBoardDecisionEngine:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def decide(self, confirmation_payload: dict, gates: List[PaperReadinessBoardGate], write_block_proof: Optional[WriteBlockedRuntimeAdapterProof] = None, activation_events: Optional[List[ActivationFirewallEvent]] = None) -> PaperReadinessBoardReview:
        flags = self.collect_board_risk_flags(confirmation_payload, gates, write_block_proof, activation_events)
        base_decision = evaluate_paper_readiness_board_eligibility(confirmation_payload)

        if any(g.status in [ReadinessBoardGateStatus.FAIL, ReadinessBoardGateStatus.BLOCKED] for g in gates):
            base_decision = PaperReadinessBoardDecision.BLOCK
        if flags:
            if PaperReadinessBoardRiskFlag.HUMAN_REVIEW_BUNDLE_MISSING in flags:
                base_decision = PaperReadinessBoardDecision.REQUEST_MANUAL_REVIEW
            else:
                base_decision = PaperReadinessBoardDecision.BLOCK

        if write_block_proof and (not write_block_proof.all_writes_blocked or write_block_proof.unblocked_write_attempt_count > 0):
            base_decision = PaperReadinessBoardDecision.BLOCK

        status = board_status_from_decision(base_decision)

        review = PaperReadinessBoardReview(
            board_review_id=create_board_review_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            status=status,
            decision=base_decision,
            candidate_id=confirmation_payload.get("candidate_id"),
            source_confirmation_review_id=confirmation_payload.get("review_id"),
            source_human_review_bundle_id=None,
            source_activation_denied_registry_id=None,
            gates=gates,
            write_block_proofs=[write_block_proof] if write_block_proof else [],
            activation_firewall_events=activation_events or [],
            readiness_confidence="HIGH" if base_decision == PaperReadinessBoardDecision.PASS_WITH_ACTIVATION_DENIED else "LOW",
            evidence_refs=[],
            required_followups=self.followups_for_board_decision(base_decision, flags),
            safety_flags=flags,
            manual_review_required=True,
            activation_denied=True,
            activation_allowed=False,
            allows_active_paper=False,
            allows_broker_execution=False,
            allows_paper_state_mutation=False,
            allows_config_patch=False,
            allows_telegram_real_send=False,
            warnings=[],
            errors=[]
        )
        validate_paper_readiness_board_review(review)
        return review

    def collect_board_risk_flags(self, confirmation_payload: dict, gates: List[PaperReadinessBoardGate], write_block_proof: Optional[WriteBlockedRuntimeAdapterProof] = None, activation_events: Optional[List[ActivationFirewallEvent]] = None) -> List[PaperReadinessBoardRiskFlag]:
        flags = []
        # basic checks
        if write_block_proof and not write_block_proof.all_writes_blocked:
            flags.append(PaperReadinessBoardRiskFlag.WRITE_ATTEMPT_NOT_BLOCKED)
        if activation_events and any(not e.blocked for e in activation_events):
            flags.append(PaperReadinessBoardRiskFlag.ACTIVATION_ALLOWED_RISK)
        return flags

    def rationale_for_board_decision(self, decision: PaperReadinessBoardDecision, flags: List[PaperReadinessBoardRiskFlag]) -> str:
        return f"Decision: {decision.value}, Flags: {[f.value for f in flags]}"

    def followups_for_board_decision(self, decision: PaperReadinessBoardDecision, flags: List[PaperReadinessBoardRiskFlag]) -> List[str]:
        if decision == PaperReadinessBoardDecision.BLOCK:
            return ["Review blocking flags."]
        return ["Maintain activation denied."]
