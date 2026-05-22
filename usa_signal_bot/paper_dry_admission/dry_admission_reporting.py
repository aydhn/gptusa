from typing import Any
from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    DryAdmissionStep,
    PaperModeDryAdmissionPlan,
    RuntimeWriteLockProofRefresh,
    HumanApprovalLedgerEntry,
    HumanApprovalLedger,
    PaperModeDryAdmissionRun,
    DryAdmissionAuditEntry,
    DryAdmissionFullReview
)
from usa_signal_bot.paper_dry_admission.dry_admission_plan import dry_admission_plan_to_text
from usa_signal_bot.paper_dry_admission.write_lock_proof_refresh import write_lock_refresh_to_text
from usa_signal_bot.paper_dry_admission.human_approval_ledger import human_approval_ledger_to_text as _hl2txt
from usa_signal_bot.paper_dry_admission.dry_admission_audit import dry_admission_audit_to_text as _audit2txt
from usa_signal_bot.paper_dry_admission.dry_admission_report import dry_admission_full_review_to_text as _fr2txt
from usa_signal_bot.paper_dry_admission.dry_admission_report import dry_admission_limitations_text

def dry_admission_step_to_text(item: DryAdmissionStep) -> str:
    return f"Step: {item.step_name} [{item.status.value}]"

def paper_mode_dry_admission_plan_to_text(item: PaperModeDryAdmissionPlan) -> str:
    return dry_admission_plan_to_text(item)

def runtime_write_lock_proof_refresh_to_text(item: RuntimeWriteLockProofRefresh) -> str:
    return write_lock_refresh_to_text(item)

def human_approval_ledger_entry_to_text(item: HumanApprovalLedgerEntry) -> str:
    return f"[{item.status.value}] {item.scope.value}: {item.note}"

def human_approval_ledger_to_text(item: HumanApprovalLedger, limit: int = 100) -> str:
    return _hl2txt(item, limit)

def paper_mode_dry_admission_run_to_text(item: PaperModeDryAdmissionRun, limit: int = 100) -> str:
    lines = [
        f"Run ID: {item.run_id}",
        f"Status: {item.status.value}",
        f"Decision: {item.decision.value}",
        f"Steps: {len(item.steps)}",
        f"Activation Denied: {item.activation_denied}",
        f"All Writes Blocked: {item.all_writes_blocked}"
    ]
    return "\n".join(lines)

def dry_admission_audit_entry_to_text(item: DryAdmissionAuditEntry) -> str:
    return f"[{item.created_at_utc}] {item.action} on {item.entity_type}({item.entity_id}) -> {item.decision or 'N/A'}"

def dry_admission_full_review_to_text(item: DryAdmissionFullReview, limit: int = 100) -> str:
    return _fr2txt(item, limit)

def dry_admission_store_summary_to_text(summary: dict[str, Any]) -> str:
    lines = ["Dry Admission Store Summary:"]
    for k, v in summary.items():
        lines.append(f"  - {k}: {v}")
    return "\n".join(lines)
