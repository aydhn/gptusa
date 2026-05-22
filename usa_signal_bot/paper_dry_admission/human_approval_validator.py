from typing import Any, List
from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    HumanApprovalLedgerEntry,
    HumanApprovalLedger
)
from usa_signal_bot.core.enums import HumanApprovalEntryStatus

def validate_human_approval_entry_safety(entry: HumanApprovalLedgerEntry) -> List[str]:
    issues = []
    if entry.activation_allowed:
        issues.append("activation_allowed is True")
    if not entry.acknowledged_not_activation:
        issues.append("acknowledged_not_activation is False")

    safe_note = entry.note.lower()
    unsafe_words = ["aktif et", "canlıya al", "emir gönder", "live approved", "sent to broker", "gerçek emir"]
    for word in unsafe_words:
        if word in safe_note:
            issues.append(f"Unsafe language in note: {word}")

    if entry.status == HumanApprovalEntryStatus.REJECTED:
        issues.append("Entry is rejected")

    return issues

def validate_human_approval_ledger_safety(ledger: HumanApprovalLedger) -> List[str]:
    issues = []
    if ledger.activation_allowed:
        issues.append("activation_allowed is True")
    if not ledger.acknowledged_not_activation:
        issues.append("acknowledged_not_activation is False")
    if ledger.allows_active_paper:
        issues.append("allows_active_paper is True")
    if ledger.allows_broker_execution:
        issues.append("allows_broker_execution is True")
    if ledger.allows_paper_state_mutation:
        issues.append("allows_paper_state_mutation is True")
    if ledger.allows_config_patch:
        issues.append("allows_config_patch is True")
    if ledger.allows_telegram_real_send:
        issues.append("allows_telegram_real_send is True")

    for entry in ledger.entries:
        issues.extend(validate_human_approval_entry_safety(entry))

    return issues

def human_approval_ledger_allows_activation(ledger: HumanApprovalLedger) -> bool:
    return any([
        ledger.activation_allowed,
        ledger.allows_active_paper,
        ledger.allows_broker_execution,
        ledger.allows_paper_state_mutation,
        ledger.allows_config_patch,
        ledger.allows_telegram_real_send
    ])

def human_approval_ledger_requires_followup(ledger: HumanApprovalLedger) -> bool:
    return len(ledger.missing_scopes) > 0 or len(validate_human_approval_ledger_safety(ledger)) > 0

def human_approval_ledger_blocks_next_stage(ledger: HumanApprovalLedger) -> bool:
    return human_approval_ledger_requires_followup(ledger) or human_approval_ledger_allows_activation(ledger)

def human_approval_validator_summary(ledger: HumanApprovalLedger) -> dict[str, Any]:
    issues = validate_human_approval_ledger_safety(ledger)
    return {
        "valid": len(issues) == 0 and len(ledger.missing_scopes) == 0,
        "issues": issues,
        "missing_scopes": ledger.missing_scopes,
        "blocks_next_stage": human_approval_ledger_blocks_next_stage(ledger)
    }

def human_approval_validator_to_text(payload: dict[str, Any]) -> str:
    lines = [
        f"Valid: {payload.get('valid', False)}",
        f"Blocks Next Stage: {payload.get('blocks_next_stage', True)}"
    ]
    missing = payload.get("missing_scopes", [])
    if missing:
        lines.append("Missing Scopes:")
        for m in missing:
            lines.append(f"  - {m}")
    issues = payload.get("issues", [])
    if issues:
        lines.append("Issues:")
        for issue in issues:
            lines.append(f"  - {issue}")
    return "\n".join(lines)
