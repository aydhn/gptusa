from typing import Any, List
from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    HumanApprovalLedgerEntry,
    HumanApprovalLedger,
    create_human_approval_ledger_entry_id,
    create_human_approval_ledger_id
)
from usa_signal_bot.core.enums import (
    HumanApprovalScope,
    HumanApprovalEntryStatus,
    HumanApprovalLedgerStatus,
    HumanApprovalLedgerDecision
)

def required_human_approval_scopes() -> List[HumanApprovalScope]:
    return [
        HumanApprovalScope.NO_WRITE_REVIEW_ACKNOWLEDGEMENT,
        HumanApprovalScope.SAFETY_REVIEW_ACKNOWLEDGEMENT,
        HumanApprovalScope.NOT_ACTIVATION_APPROVAL
    ]

def build_human_approval_ledger_entry(
    scope: HumanApprovalScope,
    reviewer_id: str | None = None,
    candidate_id: str | None = None,
    note: str | None = None
) -> HumanApprovalLedgerEntry:

    note_val = note or "No note provided"

    status = HumanApprovalEntryStatus.RECORDED
    if "aktif et" in note_val.lower() or "canlıya al" in note_val.lower():
        status = HumanApprovalEntryStatus.REJECTED

    return HumanApprovalLedgerEntry(
        ledger_entry_id=create_human_approval_ledger_entry_id(),
        scope=scope,
        note=note_val,
        status=status,
        reviewer_id=reviewer_id,
        candidate_id=candidate_id,
        acknowledged_no_write=True,
        acknowledged_not_activation=True,
        activation_allowed=False
    )

def build_default_human_approval_ledger(candidate_id: str | None = None) -> HumanApprovalLedger:
    return build_human_approval_ledger([], candidate_id)

def build_human_approval_ledger(entries: List[HumanApprovalLedgerEntry], candidate_id: str | None = None) -> HumanApprovalLedger:
    req_scopes = [s.value for s in required_human_approval_scopes()]
    completed = [e.scope.value for e in entries if e.status == HumanApprovalEntryStatus.RECORDED]
    missing = [s for s in req_scopes if s not in completed]

    status = HumanApprovalLedgerStatus.HUMAN_ACKNOWLEDGED_NO_WRITE if not missing else HumanApprovalLedgerStatus.WAITING_HUMAN_REVIEW
    decision = HumanApprovalLedgerDecision.RECORD_HUMAN_ACKNOWLEDGEMENT_NO_ACTIVATION if not missing else HumanApprovalLedgerDecision.REQUEST_HUMAN_REVIEW

    for e in entries:
        if e.status == HumanApprovalEntryStatus.REJECTED:
            status = HumanApprovalLedgerStatus.BLOCKED
            decision = HumanApprovalLedgerDecision.BLOCK
            break

    return HumanApprovalLedger(
        ledger_id=create_human_approval_ledger_id(),
        status=status,
        decision=decision,
        candidate_id=candidate_id,
        entries=entries,
        required_scopes=req_scopes,
        completed_scopes=completed,
        missing_scopes=missing,
        acknowledged_no_write=True,
        acknowledged_not_activation=True,
        activation_allowed=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False
    )

def human_approval_ledger_summary(ledger: HumanApprovalLedger) -> dict[str, Any]:
    return {
        "ledger_id": ledger.ledger_id,
        "status": ledger.status.value,
        "decision": ledger.decision.value,
        "missing_scopes": ledger.missing_scopes,
        "entry_count": len(ledger.entries)
    }

def human_approval_ledger_to_text(ledger: HumanApprovalLedger, limit: int = 100) -> str:
    lines = [
        f"Ledger ID: {ledger.ledger_id}",
        f"Status: {ledger.status.value}",
        f"Decision: {ledger.decision.value}",
        f"Missing Scopes: {', '.join(ledger.missing_scopes) if ledger.missing_scopes else 'None'}",
        f"Entries: {len(ledger.entries)}"
    ]
    return "\n".join(lines)
