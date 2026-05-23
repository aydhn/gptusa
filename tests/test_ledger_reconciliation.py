from usa_signal_bot.core.enums import LedgerReconciliationStatus, LedgerReconciliationDecision
from usa_signal_bot.paper_admission_review.ledger_reconciliation import reconcile_human_approval_ledger

def test_reconcile_human_approval_ledger():
    payload = {
        "human_approval_ledger": {
            "completed_scopes": {
                "NO_WRITE_REVIEW_ACKNOWLEDGEMENT": True,
                "SAFETY_REVIEW_ACKNOWLEDGEMENT": True,
                "EVIDENCE_REVIEW_ACKNOWLEDGEMENT": True,
                "NOT_ACTIVATION_APPROVAL": True
            },
            "acknowledged_no_write": True,
            "acknowledged_not_activation": True,
            "activation_allowed": False
        }
    }
    report = reconcile_human_approval_ledger(payload)
    assert report.status == LedgerReconciliationStatus.RECONCILED
    assert report.decision == LedgerReconciliationDecision.ACCEPT_NO_WRITE_ACKNOWLEDGEMENT

    unsafe_payload = {
        "human_approval_ledger": {
            "completed_scopes": [],
            "notes": "canlıya al"
        }
    }
    report = reconcile_human_approval_ledger(unsafe_payload)
    assert report.status == LedgerReconciliationStatus.BLOCKED
    assert report.decision == LedgerReconciliationDecision.REQUEST_UNSAFE_NOTE_REVIEW
