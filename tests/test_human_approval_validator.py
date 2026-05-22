from usa_signal_bot.paper_dry_admission.human_approval_ledger import build_default_human_approval_ledger, build_human_approval_ledger_entry
from usa_signal_bot.paper_dry_admission.human_approval_validator import validate_human_approval_ledger_safety
from usa_signal_bot.core.enums import HumanApprovalScope

def test_human_approval_validator():
    ledger = build_default_human_approval_ledger()
    issues = validate_human_approval_ledger_safety(ledger)
    assert len(issues) == 0

    entry = build_human_approval_ledger_entry(HumanApprovalScope.NOT_ACTIVATION_APPROVAL, note="aktif et")
    ledger.entries.append(entry)
    issues_bad = validate_human_approval_ledger_safety(ledger)
    assert len(issues_bad) > 0
    assert any("aktif et" in issue for issue in issues_bad)
