from dataclasses import dataclass, field
from typing import Any, List
import json
from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    PaperModeDryAdmissionPlan,
    PaperModeDryAdmissionRun,
    RuntimeWriteLockProofRefresh,
    HumanApprovalLedger,
    DryAdmissionFullReview
)

@dataclass
class DryAdmissionValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class DryAdmissionValidationReport:
    valid: bool = True
    issue_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocked_count: int = 0
    issues: List[DryAdmissionValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def add_issue(self, severity: str, field_name: str | None, message: str):
        self.issues.append(DryAdmissionValidationIssue(severity, field_name, message))
        self.issue_count += 1
        if severity == "WARNING":
            self.warning_count += 1
            self.warnings.append(message)
        elif severity == "ERROR":
            self.error_count += 1
            self.errors.append(message)
            self.valid = False
        elif severity == "BLOCK":
            self.blocked_count += 1
            self.errors.append(message)
            self.valid = False

def validate_dry_admission_plan_report(item: PaperModeDryAdmissionPlan) -> DryAdmissionValidationReport:
    r = DryAdmissionValidationReport()
    if item.execution_enabled: r.add_issue("ERROR", "execution_enabled", "Must be False")
    if item.active_paper_enabled: r.add_issue("ERROR", "active_paper_enabled", "Must be False")
    if item.broker_execution_enabled: r.add_issue("ERROR", "broker_execution_enabled", "Must be False")
    if item.paper_state_mutation_enabled: r.add_issue("ERROR", "paper_state_mutation_enabled", "Must be False")
    if item.config_patch_enabled: r.add_issue("ERROR", "config_patch_enabled", "Must be False")
    if item.telegram_real_send_enabled: r.add_issue("ERROR", "telegram_real_send_enabled", "Must be False")
    return r

def validate_dry_admission_run_report(item: PaperModeDryAdmissionRun) -> DryAdmissionValidationReport:
    r = DryAdmissionValidationReport()
    if item.activation_allowed: r.add_issue("ERROR", "activation_allowed", "Must be False")
    if not item.activation_denied: r.add_issue("ERROR", "activation_denied", "Must be True")
    if not item.all_writes_blocked: r.add_issue("ERROR", "all_writes_blocked", "Must be True")
    if item.mutation_detected: r.add_issue("ERROR", "mutation_detected", "Must be False")
    for s in item.steps:
        if s.write_attempted or s.order_attempted or s.broker_send_attempted or s.config_patch_attempted or s.telegram_real_send_attempted or s.active_paper_enable_attempted or s.mutation_detected:
            r.add_issue("ERROR", "steps", f"Step {s.step_name} has invalid attempt flag")
    return r

def validate_write_lock_refresh_report(item: RuntimeWriteLockProofRefresh) -> DryAdmissionValidationReport:
    r = DryAdmissionValidationReport()
    if not item.all_writes_blocked: r.add_issue("ERROR", "all_writes_blocked", "Must be True")
    if item.unblocked_write_attempt_count > 0: r.add_issue("ERROR", "unblocked_write_attempt_count", "Must be 0")
    if item.allows_active_paper: r.add_issue("ERROR", "allows_active_paper", "Must be False")
    if item.allows_broker_execution: r.add_issue("ERROR", "allows_broker_execution", "Must be False")
    return r

def validate_human_approval_ledger_report(item: HumanApprovalLedger) -> DryAdmissionValidationReport:
    r = DryAdmissionValidationReport()
    if item.activation_allowed: r.add_issue("ERROR", "activation_allowed", "Must be False")
    if not item.acknowledged_not_activation: r.add_issue("WARNING", "acknowledged_not_activation", "Should be True")
    if item.allows_active_paper: r.add_issue("ERROR", "allows_active_paper", "Must be False")
    return r

def validate_no_live_execution_language_in_dry_admission(text: str) -> DryAdmissionValidationReport:
    r = DryAdmissionValidationReport()
    text_lower = text.lower()
    unsafe = ["live approved", "sent to broker", "kesin al", "garanti", "paper'a uygula", "canlıya al", "gerçek emir", "aktif et", "kesin kâr", "candidate kesin iyi"]
    for u in unsafe:
        if u in text_lower:
            r.add_issue("ERROR", "text", f"Contains unsafe language: {u}")
    return r

def validate_no_active_paper_language_in_dry_admission(text: str) -> DryAdmissionValidationReport:
    r = DryAdmissionValidationReport()
    if "active paper enable" in text.lower():
        r.add_issue("WARNING", "text", "Contains 'active paper enable'")
    return r

def validate_no_broker_execution_fields_in_dry_admission(payload: dict[str, Any]) -> DryAdmissionValidationReport:
    r = DryAdmissionValidationReport()
    payload_str = json.dumps(payload)
    unsafe = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    for u in unsafe:
        if u in payload_str:
            r.add_issue("ERROR", "payload", f"Contains unsafe broker field: {u}")
    return r

def validate_no_paper_state_mutation_fields_in_dry_admission(payload: dict[str, Any]) -> DryAdmissionValidationReport:
    r = DryAdmissionValidationReport()
    # If the payload explicitly sets these to True, it's a mutation.
    if payload.get("paper_state_committed") is True: r.add_issue("ERROR", "payload", "paper_state_committed is True")
    if payload.get("paper_order_executed") is True: r.add_issue("ERROR", "payload", "paper_order_executed is True")
    if payload.get("portfolio_state_mutated") is True: r.add_issue("ERROR", "payload", "portfolio_state_mutated is True")
    return r

def validate_no_sensitive_data_in_dry_admission_payload(payload: dict[str, Any]) -> DryAdmissionValidationReport:
    r = DryAdmissionValidationReport()
    payload_str = json.dumps(payload).lower()
    if "api_key" in payload_str or "secret" in payload_str or "token" in payload_str:
        if "dummy" not in payload_str and "mock" not in payload_str:
            r.add_issue("WARNING", "payload", "Potential secret/token leak detected")
    return r

def validate_dry_admission_full_review_report(item: DryAdmissionFullReview) -> DryAdmissionValidationReport:
    r = DryAdmissionValidationReport()

    for p in item.plans:
        pr = validate_dry_admission_plan_report(p)
        if not pr.valid: r.valid = False; r.errors.extend(pr.errors)

    for run in item.runs:
        rr = validate_dry_admission_run_report(run)
        if not rr.valid: r.valid = False; r.errors.extend(rr.errors)

    for w in item.write_lock_refreshes:
        wr = validate_write_lock_refresh_report(w)
        if not wr.valid: r.valid = False; r.errors.extend(wr.errors)

    for l in item.human_ledgers:
        lr = validate_human_approval_ledger_report(l)
        if not lr.valid: r.valid = False; r.errors.extend(lr.errors)

    txt_val = validate_no_live_execution_language_in_dry_admission(json.dumps(dry_admission_full_review_to_dict(item)))
    if not txt_val.valid: r.valid = False; r.errors.extend(txt_val.errors)

    dict_val = dry_admission_full_review_to_dict(item)
    br_val = validate_no_broker_execution_fields_in_dry_admission(dict_val)
    if not br_val.valid: r.valid = False; r.errors.extend(br_val.errors)

    pm_val = validate_no_paper_state_mutation_fields_in_dry_admission(dict_val)
    if not pm_val.valid: r.valid = False; r.errors.extend(pm_val.errors)

    return r

def dry_admission_validation_report_to_text(report: DryAdmissionValidationReport) -> str:
    lines = [
        f"Valid: {report.valid}",
        f"Issues: {report.issue_count} (Errors: {report.error_count}, Warnings: {report.warning_count}, Blocked: {report.blocked_count})"
    ]
    if report.errors:
        lines.append("Errors:")
        for e in report.errors: lines.append(f"  - {e}")
    if report.warnings:
        lines.append("Warnings:")
        for w in report.warnings: lines.append(f"  - {w}")
    return "\n".join(lines)

def assert_dry_admission_valid(report: DryAdmissionValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Dry admission validation failed: {report.errors}")
