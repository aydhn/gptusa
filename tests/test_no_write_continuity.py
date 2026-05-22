from usa_signal_bot.paper_dry_admission.no_write_continuity import validate_no_write_admission_continuity
from usa_signal_bot.paper_dry_admission.human_approval_ledger import build_default_human_approval_ledger

def test_no_write_continuity():
    ledger = build_default_human_approval_ledger()
    contract = {"activation_denied": True}
    issues = validate_no_write_admission_continuity(contract_payload=contract, ledger=ledger)
    assert len(issues) == 0

    ledger.activation_allowed = True
    issues_bad = validate_no_write_admission_continuity(contract_payload=contract, ledger=ledger)
    assert len(issues_bad) > 0
