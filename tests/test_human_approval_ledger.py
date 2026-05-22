from usa_signal_bot.paper_dry_admission.human_approval_ledger import build_default_human_approval_ledger, build_human_approval_ledger_entry
from usa_signal_bot.core.enums import HumanApprovalScope, HumanApprovalEntryStatus

def test_human_approval_ledger():
    ledger = build_default_human_approval_ledger("cand1")
    assert ledger.candidate_id == "cand1"
    assert len(ledger.missing_scopes) == 3

    entry = build_human_approval_ledger_entry(HumanApprovalScope.NOT_ACTIVATION_APPROVAL, note="acknowledged no activation")
    assert entry.status == HumanApprovalEntryStatus.RECORDED

    entry_bad = build_human_approval_ledger_entry(HumanApprovalScope.NOT_ACTIVATION_APPROVAL, note="aktif et")
    assert entry_bad.status == HumanApprovalEntryStatus.REJECTED
