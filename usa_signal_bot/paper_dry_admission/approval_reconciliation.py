from typing import Any, List
from usa_signal_bot.paper_dry_admission.dry_admission_models import HumanApprovalLedger
from usa_signal_bot.core.enums import DryAdmissionRiskFlag
from usa_signal_bot.paper_dry_admission.no_write_ingestion import extract_no_write_contract

def reconcile_human_approval_with_no_write_contract(ledger: HumanApprovalLedger, no_write_payload: dict[str, Any]) -> dict[str, Any]:
    contract = extract_no_write_contract(no_write_payload)

    contract_denied = contract.get("activation_denied", False) if contract else False
    ledger_denied = not ledger.activation_allowed

    mismatch = False
    reasons = []

    if not contract:
        mismatch = True
        reasons.append("Missing no-write contract")
    elif contract_denied and not ledger_denied:
        mismatch = True
        reasons.append("Contract denies activation but ledger allows it")
    elif ledger.activation_allowed:
        mismatch = True
        reasons.append("Ledger activation_allowed is True")

    if ledger.missing_scopes:
        mismatch = True
        reasons.append(f"Missing ledger scopes: {ledger.missing_scopes}")

    return {
        "reconciled": not mismatch,
        "mismatch": mismatch,
        "contract_activation_denied": contract_denied,
        "ledger_activation_allowed": ledger.activation_allowed,
        "reasons": reasons
    }

def approval_reconciliation_passed(payload: dict[str, Any]) -> bool:
    return payload.get("reconciled", False)

def approval_reconciliation_risk_flags(payload: dict[str, Any]) -> List[DryAdmissionRiskFlag]:
    flags = []
    if payload.get("mismatch", False):
        flags.append(DryAdmissionRiskFlag.HUMAN_LEDGER_ACTIVATION_RISK)
    return flags

def approval_reconciliation_followups(payload: dict[str, Any]) -> List[str]:
    return payload.get("reasons", [])

def approval_reconciliation_to_text(payload: dict[str, Any]) -> str:
    lines = [
        f"Reconciled: {payload.get('reconciled', False)}",
        f"Mismatch: {payload.get('mismatch', True)}"
    ]
    reasons = payload.get("reasons", [])
    if reasons:
        lines.append("Reasons:")
        for r in reasons:
            lines.append(f"  - {r}")
    return "\n".join(lines)
