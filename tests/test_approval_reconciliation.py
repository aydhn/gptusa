from usa_signal_bot.paper_dry_admission.human_approval_ledger import build_default_human_approval_ledger
from usa_signal_bot.paper_dry_admission.approval_reconciliation import reconcile_human_approval_with_no_write_contract

def test_approval_reconciliation():
    ledger = build_default_human_approval_ledger()
    payload = {
        "contracts": [{"contract_id": "c1", "activation_denied": True}]
    }
    res = reconcile_human_approval_with_no_write_contract(ledger, payload)
    # Reconciled will be false because default ledger has missing scopes
    assert res["reconciled"] is False
    assert res["contract_activation_denied"] is True
