from dataclasses import dataclass, field
from typing import Any, List, Optional
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    DryRunBridgeContext,
    DryRunProposal,
    DryRunBridgeSession,
    DryRunBridgeReview
)

@dataclass
class DryRunBridgeValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class DryRunBridgeValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[DryRunBridgeValidationIssue]
    warnings: List[str]
    errors: List[str]

def _create_report(issues: List[DryRunBridgeValidationIssue]) -> DryRunBridgeValidationReport:
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    errors = [i.message for i in issues if i.severity == "ERROR"]
    blocked = [i.message for i in issues if i.severity == "BLOCKED"]
    return DryRunBridgeValidationReport(
        valid=len(errors) == 0 and len(blocked) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_dry_run_context_report(item: DryRunBridgeContext) -> DryRunBridgeValidationReport:
    issues = []
    if item.allow_paper_state_mutation:
        issues.append(DryRunBridgeValidationIssue("ERROR", "allow_paper_state_mutation", "allow_paper_state_mutation true invalid"))
    if item.allow_paper_orders:
        issues.append(DryRunBridgeValidationIssue("ERROR", "allow_paper_orders", "allow_paper_orders true invalid"))
    if item.allow_broker_orders:
        issues.append(DryRunBridgeValidationIssue("ERROR", "allow_broker_orders", "allow_broker_orders true invalid"))
    if item.allow_telegram_real_send:
        issues.append(DryRunBridgeValidationIssue("ERROR", "allow_telegram_real_send", "allow_telegram_real_send true invalid"))
    if item.allow_production_config_write:
        issues.append(DryRunBridgeValidationIssue("ERROR", "allow_production_config_write", "allow_production_config_write true invalid"))
    if item.allow_active_paper_enable:
        issues.append(DryRunBridgeValidationIssue("ERROR", "allow_active_paper_enable", "allow_active_paper_enable true invalid"))
    return _create_report(issues)

def validate_dry_run_proposals_report(items: List[DryRunProposal]) -> DryRunBridgeValidationReport:
    issues = []
    for item in items:
        if item.is_real_order:
            issues.append(DryRunBridgeValidationIssue("ERROR", "is_real_order", "is_real_order true invalid"))
        if item.will_mutate_paper_state:
            issues.append(DryRunBridgeValidationIssue("ERROR", "will_mutate_paper_state", "will_mutate_paper_state true invalid"))
        if item.will_send_to_broker:
            issues.append(DryRunBridgeValidationIssue("ERROR", "will_send_to_broker", "will_send_to_broker true invalid"))
    return _create_report(issues)

def validate_dry_run_session_report(item: DryRunBridgeSession) -> DryRunBridgeValidationReport:
    issues = []
    if item.context:
        report = validate_dry_run_context_report(item.context)
        issues.extend(report.issues)
    report = validate_dry_run_proposals_report(item.proposals)
    issues.extend(report.issues)
    for c in item.human_checkpoints:
        if c.allows_active_paper:
            issues.append(DryRunBridgeValidationIssue("ERROR", "allows_active_paper", "allows_active_paper true invalid"))
        if c.allows_broker_execution:
            issues.append(DryRunBridgeValidationIssue("ERROR", "allows_broker_execution", "allows_broker_execution true invalid"))
        if c.allows_config_patch:
            issues.append(DryRunBridgeValidationIssue("ERROR", "allows_config_patch", "allows_config_patch true invalid"))
    return _create_report(issues)

def validate_dry_run_review_report(item: DryRunBridgeReview) -> DryRunBridgeValidationReport:
    issues = []
    for s in item.sessions:
        report = validate_dry_run_session_report(s)
        issues.extend(report.issues)
    return _create_report(issues)

def validate_no_sensitive_data_in_dry_run_payload(payload: dict[str, Any]) -> DryRunBridgeValidationReport:
    issues = []
    def _check(d: dict):
        for k, v in d.items():
            if "token" in k.lower() or "secret" in k.lower() or "api_key" in k.lower():
                if v != "[REDACTED]":
                    issues.append(DryRunBridgeValidationIssue("ERROR", k, "Secret/token leaked"))
            if isinstance(v, dict):
                _check(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        _check(item)
    _check(payload)
    return _create_report(issues)

def validate_no_live_execution_language_in_dry_run(text: str) -> DryRunBridgeValidationReport:
    issues = []
    unsafe = ["live approved", "sent to broker", "kesin al", "garanti", "paper'a uygula", "canlıya al", "gerçek emir", "aktif et", "kesin kâr", "candidate kesin iyi"]
    for u in unsafe:
        if u in text.lower():
            issues.append(DryRunBridgeValidationIssue("ERROR", None, f"Live execution language found: {u}"))
    return _create_report(issues)

def validate_no_real_order_language_in_dry_run(text: str) -> DryRunBridgeValidationReport:
    return validate_no_live_execution_language_in_dry_run(text)

def validate_no_paper_state_mutation_fields_in_dry_run(payload: dict[str, Any]) -> DryRunBridgeValidationReport:
    issues = []
    fields = ["paper_state_committed", "paper_order_executed", "portfolio_state_mutated"]
    def _check(d: dict):
        for k, v in d.items():
            if k in fields and v is True:
                issues.append(DryRunBridgeValidationIssue("ERROR", k, f"Paper mutation field {k} is True"))
            if isinstance(v, dict):
                _check(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        _check(item)
    _check(payload)
    return _create_report(issues)

def validate_no_broker_execution_fields_in_dry_run(payload: dict[str, Any]) -> DryRunBridgeValidationReport:
    issues = []
    fields = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    def _check(d: dict):
        for k, v in d.items():
            if k in fields and v is not None:
                issues.append(DryRunBridgeValidationIssue("ERROR", k, f"Broker field {k} is present"))
            if isinstance(v, dict):
                _check(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        _check(item)
    _check(payload)
    return _create_report(issues)

def dry_run_bridge_validation_report_to_text(report: DryRunBridgeValidationReport) -> str:
    valid_str = "VALID" if report.valid else "INVALID"
    return f"Validation Report: {valid_str} (Errors: {report.error_count}, Warnings: {report.warning_count})"

def assert_dry_run_bridge_valid(report: DryRunBridgeValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Dry-run bridge validation failed: {report.errors}")
