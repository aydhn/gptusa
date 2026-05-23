from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    PaperModeAdmissionReviewStatus,
    PaperModeAdmissionReviewDecision,
    AdmissionReviewRiskFlag,
    AdmissionReviewGateStatus,
    LedgerReconciliationStatus
)
from .admission_review_models import (
    PaperModeAdmissionReview,
    AdmissionReviewGate,
    LedgerReconciliationReport,
    AdmissionEvidenceSeal,
    create_admission_review_id
)
from .eligibility_checker import admission_review_safety_flags_from_dry_admission, admission_review_status_from_decision
from .ledger_reconciliation import ledger_reconciliation_risk_flags
from .dry_admission_ingestion import extract_dry_admission_candidate_id, extract_dry_admission_run, extract_write_lock_refresh, extract_human_approval_ledger

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

class GuardedPaperModeAdmissionReviewDecisionEngine:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative
        self.critical_risk_flags = [
             AdmissionReviewRiskFlag.REAL_ORDER_RISK,
             AdmissionReviewRiskFlag.PAPER_ORDER_RISK,
             AdmissionReviewRiskFlag.BROKER_ORDER_RISK,
             AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK,
             AdmissionReviewRiskFlag.PAPER_POSITION_MUTATION_RISK,
             AdmissionReviewRiskFlag.PAPER_PORTFOLIO_MUTATION_RISK,
             AdmissionReviewRiskFlag.PAPER_CASH_MUTATION_RISK,
             AdmissionReviewRiskFlag.PAPER_EQUITY_MUTATION_RISK,
             AdmissionReviewRiskFlag.TELEGRAM_REAL_SEND_RISK,
             AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
             AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
             AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK,
             AdmissionReviewRiskFlag.TRANSITION_CHECKPOINT_INVALID,
             AdmissionReviewRiskFlag.SECRET_RISK
        ]

    def collect_admission_risk_flags(self, dry_admission_payload: Dict[str, Any], gates: List[AdmissionReviewGate], reconciliation: Optional[LedgerReconciliationReport] = None) -> List[AdmissionReviewRiskFlag]:
        flags = []
        flags.extend(admission_review_safety_flags_from_dry_admission(dry_admission_payload))
        for gate in gates:
             flags.extend(gate.risk_flags)
        if reconciliation:
             flags.extend(reconciliation.safety_flags)
        else:
             flags.extend(ledger_reconciliation_risk_flags(extract_human_approval_ledger(dry_admission_payload)))

        # Deduplicate
        return list(set(flags))

    def followups_for_admission_decision(self, decision: PaperModeAdmissionReviewDecision, flags: List[AdmissionReviewRiskFlag]) -> List[str]:
        followups = []
        if decision == PaperModeAdmissionReviewDecision.REQUEST_DRY_ADMISSION_REFRESH:
             followups.append("Refresh dry admission payload")
        if decision == PaperModeAdmissionReviewDecision.REQUEST_LEDGER_RECONCILIATION:
             followups.append("Complete ledger reconciliation")
        if decision == PaperModeAdmissionReviewDecision.REQUEST_WRITE_LOCK_REFRESH:
             followups.append("Refresh write lock proof")
        if decision == PaperModeAdmissionReviewDecision.REQUEST_MANUAL_REVIEW:
             followups.append("Perform manual review")
        return followups

    def rationale_for_admission_decision(self, decision: PaperModeAdmissionReviewDecision, flags: List[AdmissionReviewRiskFlag]) -> str:
        if decision == PaperModeAdmissionReviewDecision.BLOCK:
             return f"Blocked due to critical safety flags: {[f.value for f in flags if f in self.critical_risk_flags]}"
        if decision == PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT:
             return "All gates passed, ledger reconciled, no write continuity preserved. Not an active paper enable."
        return f"Decision: {decision.value}"

    def decide(self, dry_admission_payload: Dict[str, Any], gates: List[AdmissionReviewGate], reconciliation: Optional[LedgerReconciliationReport] = None, evidence_seal: Optional[AdmissionEvidenceSeal] = None) -> PaperModeAdmissionReview:
        flags = self.collect_admission_risk_flags(dry_admission_payload, gates, reconciliation)

        has_critical_risk = any(f in self.critical_risk_flags for f in flags)

        run = extract_dry_admission_run(dry_admission_payload)
        write_lock = extract_write_lock_refresh(dry_admission_payload)

        decision = PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT

        if has_critical_risk:
             decision = PaperModeAdmissionReviewDecision.BLOCK
        elif not run or run.get("status") in ["FAILED", "STALE"] or any(g.status == AdmissionReviewGateStatus.FAIL and g.gate_name == "dry_admission_completed_no_write" for g in gates):
             decision = PaperModeAdmissionReviewDecision.REQUEST_DRY_ADMISSION_REFRESH
        elif not reconciliation or reconciliation.status != LedgerReconciliationStatus.RECONCILED:
             decision = PaperModeAdmissionReviewDecision.REQUEST_LEDGER_RECONCILIATION
        elif not write_lock or write_lock.get("status") != "VALIDATED" or any(g.status == AdmissionReviewGateStatus.FAIL and g.gate_name == "write_lock_refresh_valid" for g in gates):
             decision = PaperModeAdmissionReviewDecision.REQUEST_WRITE_LOCK_REFRESH
        elif "manual_review_required" in dry_admission_payload and dry_admission_payload.get("manual_review_required") and (not reconciliation or reconciliation.status != LedgerReconciliationStatus.RECONCILED):
             decision = PaperModeAdmissionReviewDecision.REQUEST_MANUAL_REVIEW

        status = admission_review_status_from_decision(decision)
        followups = self.followups_for_admission_decision(decision, flags)
        rationale = self.rationale_for_admission_decision(decision, flags)

        return PaperModeAdmissionReview(
             admission_review_id=create_admission_review_id(),
             created_at_utc=_now(),
             status=status,
             decision=decision,
             gates=gates,
             evidence_refs=dry_admission_payload.get("evidence_refs", []),
             required_followups=followups,
             manual_review_required=True,
             activation_denied=True,
             activation_allowed=False,
             all_writes_blocked=True,
             mutation_detected=False,
             transition_allowed=False,
             allows_active_paper=False,
             allows_broker_execution=False,
             allows_paper_state_mutation=False,
             allows_config_patch=False,
             allows_telegram_real_send=False,
             safety_flags=flags,
             warnings=[rationale] if decision != PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT else [],
             errors=[],
             candidate_id=extract_dry_admission_candidate_id(dry_admission_payload),
             source_dry_admission_review_id=dry_admission_payload.get("review_id"),
             source_dry_admission_run_id=run.get("run_id") if run else None,
             source_write_lock_refresh_id=write_lock.get("refresh_id") if write_lock else None,
             source_human_ledger_id=reconciliation.source_ledger_id if reconciliation else None,
             ledger_reconciliation=reconciliation,
             evidence_seal=evidence_seal
        )
