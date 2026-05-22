from typing import Any, List
from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    PaperModeDryAdmissionPlan,
    PaperModeDryAdmissionRun,
    RuntimeWriteLockProofRefresh,
    HumanApprovalLedger
)
from usa_signal_bot.core.enums import DryAdmissionRiskFlag

def collect_dry_admission_safety_flags(
    plan: PaperModeDryAdmissionPlan | None = None,
    run: PaperModeDryAdmissionRun | None = None,
    refresh: RuntimeWriteLockProofRefresh | None = None,
    ledger: HumanApprovalLedger | None = None
) -> List[DryAdmissionRiskFlag]:
    flags = set()

    if plan:
        if plan.execution_enabled or plan.active_paper_enabled or plan.broker_execution_enabled:
            flags.add(DryAdmissionRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
        if plan.paper_state_mutation_enabled:
            flags.add(DryAdmissionRiskFlag.PAPER_STATE_MUTATION_RISK)
        if plan.config_patch_enabled:
            flags.add(DryAdmissionRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
        if plan.telegram_real_send_enabled:
            flags.add(DryAdmissionRiskFlag.TELEGRAM_REAL_SEND_RISK)

    if run:
        if run.activation_allowed:
            flags.add(DryAdmissionRiskFlag.ACTIVATION_ALLOWED_RISK)
        if run.mutation_detected:
            flags.add(DryAdmissionRiskFlag.PAPER_STATE_MUTATION_RISK)
        if not run.all_writes_blocked:
            flags.add(DryAdmissionRiskFlag.DRY_ADMISSION_WRITE_ATTEMPT)
        for f in run.safety_flags:
            flags.add(f)

    if refresh:
        if refresh.allows_active_paper or refresh.allows_broker_execution:
            flags.add(DryAdmissionRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
        if refresh.allows_paper_state_mutation or refresh.mutation_detected:
            flags.add(DryAdmissionRiskFlag.PAPER_STATE_MUTATION_RISK)
        if not refresh.all_writes_blocked or refresh.unblocked_write_attempt_count > 0:
            flags.add(DryAdmissionRiskFlag.WRITE_LOCK_BYPASS_RISK)

    if ledger:
        if ledger.activation_allowed or ledger.allows_active_paper:
            flags.add(DryAdmissionRiskFlag.HUMAN_LEDGER_ACTIVATION_RISK)
        if not ledger.acknowledged_not_activation:
            flags.add(DryAdmissionRiskFlag.ACTIVATION_ALLOWED_RISK)

    return list(flags)

def dry_admission_has_blocking_flags(flags: List[DryAdmissionRiskFlag]) -> bool:
    # All risk flags are considered blocking for dry admission.
    return len(flags) > 0

def validate_dry_admission_safety(
    plan: PaperModeDryAdmissionPlan | None = None,
    run: PaperModeDryAdmissionRun | None = None,
    refresh: RuntimeWriteLockProofRefresh | None = None,
    ledger: HumanApprovalLedger | None = None
) -> List[str]:
    issues = []
    flags = collect_dry_admission_safety_flags(plan, run, refresh, ledger)

    for flag in flags:
        issues.append(f"Safety violation detected: {flag.value}")

    return issues

def dry_admission_safety_summary(flags: List[DryAdmissionRiskFlag]) -> dict[str, Any]:
    return {
        "valid": not dry_admission_has_blocking_flags(flags),
        "blocking": dry_admission_has_blocking_flags(flags),
        "flags": [f.value for f in flags]
    }

def dry_admission_safety_validator_to_text(payload: dict[str, Any]) -> str:
    lines = [
        f"Safety Valid: {payload.get('valid', False)}",
        f"Blocking: {payload.get('blocking', True)}"
    ]
    flags = payload.get("flags", [])
    if flags:
        lines.append("Flags:")
        for f in flags:
            lines.append(f"  - {f}")
    return "\n".join(lines)
