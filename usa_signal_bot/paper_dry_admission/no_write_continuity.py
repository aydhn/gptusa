from typing import Any, List
from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    RuntimeWriteLockProofRefresh,
    HumanApprovalLedger,
    PaperModeDryAdmissionRun
)
from usa_signal_bot.core.enums import DryAdmissionRiskFlag

def validate_no_write_admission_continuity(
    contract_payload: dict[str, Any] | None = None,
    refresh: RuntimeWriteLockProofRefresh | None = None,
    ledger: HumanApprovalLedger | None = None,
    run: PaperModeDryAdmissionRun | None = None
) -> List[str]:
    issues = []

    contract = contract_payload or {}
    if contract and not contract.get("activation_denied", False):
        issues.append("Contract does not deny activation")

    if refresh:
        if not refresh.all_writes_blocked:
            issues.append("Refresh did not block all writes")
        if refresh.mutation_detected:
            issues.append("Refresh detected mutation")
        if refresh.allows_active_paper or refresh.allows_broker_execution:
            issues.append("Refresh allows active paper or broker execution")

    if ledger:
        if ledger.activation_allowed:
            issues.append("Ledger allows activation")
        if ledger.allows_active_paper or ledger.allows_broker_execution:
            issues.append("Ledger allows active paper or broker execution")

    if run:
        if not run.activation_denied:
            issues.append("Run does not deny activation")
        if run.activation_allowed:
            issues.append("Run allows activation")
        if not run.all_writes_blocked:
            issues.append("Run did not block all writes")
        if run.mutation_detected:
            issues.append("Run detected mutation")

    return issues

def no_write_continuity_flags(payload: dict[str, Any]) -> List[DryAdmissionRiskFlag]:
    flags = []
    issues = payload.get("issues", [])
    if any("Contract" in issue for issue in issues):
        flags.append(DryAdmissionRiskFlag.NO_WRITE_CONTRACT_INVALID)
    if any("mutation" in issue.lower() for issue in issues):
        flags.append(DryAdmissionRiskFlag.PAPER_STATE_MUTATION_RISK)
    if any("allows" in issue.lower() for issue in issues):
        flags.append(DryAdmissionRiskFlag.ACTIVATION_ALLOWED_RISK)
    if any("blocked" in issue.lower() for issue in issues):
        flags.append(DryAdmissionRiskFlag.DRY_ADMISSION_WRITE_ATTEMPT)
    return flags

def no_write_continuity_is_preserved(payload: dict[str, Any]) -> bool:
    return len(payload.get("issues", [])) == 0

def no_write_continuity_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "is_preserved": no_write_continuity_is_preserved(payload),
        "issues": payload.get("issues", [])
    }

def no_write_continuity_to_text(payload: dict[str, Any]) -> str:
    lines = [
        f"Continuity Preserved: {no_write_continuity_is_preserved(payload)}"
    ]
    issues = payload.get("issues", [])
    if issues:
        lines.append("Issues:")
        for issue in issues:
            lines.append(f"  - {issue}")
    return "\n".join(lines)
