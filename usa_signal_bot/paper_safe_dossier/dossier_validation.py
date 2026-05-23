from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import (
    PaperSafeGateDossier, NonExecutionAcceptanceSeal, PrePaperLocalRuntimeMap, PaperSafeDossierFullReview
)
from usa_signal_bot.core.exceptions import PaperSafeDossierValidationError

@dataclass
class PaperSafeDossierValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperSafeDossierValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[PaperSafeDossierValidationIssue]
    warnings: List[str]
    errors: List[str]

def _build_report(issues: List[PaperSafeDossierValidationIssue]) -> PaperSafeDossierValidationReport:
    warnings = [i for i in issues if i.severity == "WARNING"]
    errors = [i for i in issues if i.severity == "ERROR"]
    blocked = [i for i in issues if i.severity == "BLOCKED"]
    return PaperSafeDossierValidationReport(
        valid=len(errors) == 0 and len(blocked) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=issues,
        warnings=[i.message for i in warnings],
        errors=[i.message for i in errors + blocked]
    )

def validate_paper_safe_dossier_report(item: PaperSafeGateDossier) -> PaperSafeDossierValidationReport:
    issues = []
    if not item.activation_denied: issues.append(PaperSafeDossierValidationIssue("ERROR", "activation_denied", "Must be True"))
    if item.activation_allowed: issues.append(PaperSafeDossierValidationIssue("ERROR", "activation_allowed", "Must be False"))
    if item.admission_allowed: issues.append(PaperSafeDossierValidationIssue("ERROR", "admission_allowed", "Must be False"))
    if item.transition_allowed: issues.append(PaperSafeDossierValidationIssue("ERROR", "transition_allowed", "Must be False"))
    if not item.paper_safe_gate_passed: issues.append(PaperSafeDossierValidationIssue("WARNING", "paper_safe_gate_passed", "Should be True"))
    if not item.all_writes_blocked: issues.append(PaperSafeDossierValidationIssue("ERROR", "all_writes_blocked", "Must be True"))
    if item.order_created: issues.append(PaperSafeDossierValidationIssue("ERROR", "order_created", "Must be False"))
    if item.mutation_detected: issues.append(PaperSafeDossierValidationIssue("ERROR", "mutation_detected", "Must be False"))
    if item.allows_active_paper: issues.append(PaperSafeDossierValidationIssue("ERROR", "allows_active_paper", "Must be False"))
    if item.allows_broker_execution: issues.append(PaperSafeDossierValidationIssue("ERROR", "allows_broker_execution", "Must be False"))
    if item.allows_paper_state_mutation: issues.append(PaperSafeDossierValidationIssue("ERROR", "allows_paper_state_mutation", "Must be False"))
    if item.allows_config_patch: issues.append(PaperSafeDossierValidationIssue("ERROR", "allows_config_patch", "Must be False"))
    if item.allows_telegram_real_send: issues.append(PaperSafeDossierValidationIssue("ERROR", "allows_telegram_real_send", "Must be False"))
    return _build_report(issues)

def validate_non_execution_seal_report(item: NonExecutionAcceptanceSeal) -> PaperSafeDossierValidationReport:
    issues = []
    if not item.non_execution_confirmed: issues.append(PaperSafeDossierValidationIssue("ERROR", "non_execution_confirmed", "Must be True"))
    if not item.seal_is_metadata_only: issues.append(PaperSafeDossierValidationIssue("ERROR", "seal_is_metadata_only", "Must be True"))
    return _build_report(issues)

def validate_pre_paper_runtime_map_report(item: PrePaperLocalRuntimeMap) -> PaperSafeDossierValidationReport:
    issues = []
    if not item.map_is_metadata_only: issues.append(PaperSafeDossierValidationIssue("ERROR", "map_is_metadata_only", "Must be True"))
    for comp in item.component_items:
         if comp.write_allowed or comp.order_allowed or comp.broker_allowed or comp.config_patch_allowed or comp.telegram_real_send_allowed or comp.activation_allowed or comp.paper_admission_allowed:
             issues.append(PaperSafeDossierValidationIssue("ERROR", "component_items", f"Component {comp.component_name} has dangerous allows"))
    for route in item.route_items:
         if route.write_allowed or route.order_allowed or route.broker_allowed or route.config_patch_allowed or route.telegram_real_send_allowed or route.activation_allowed or route.paper_admission_allowed:
             issues.append(PaperSafeDossierValidationIssue("ERROR", "route_items", f"Route {route.route_name} has dangerous allows"))
    return _build_report(issues)

def validate_paper_safe_dossier_full_review_report(item: PaperSafeDossierFullReview) -> PaperSafeDossierValidationReport:
    issues = []
    for d in item.dossiers:
        issues.extend(validate_paper_safe_dossier_report(d).issues)
    for s in item.non_execution_seals:
        issues.extend(validate_non_execution_seal_report(s).issues)
    for m in item.runtime_maps:
        issues.extend(validate_pre_paper_runtime_map_report(m).issues)
    return _build_report(issues)

def validate_no_sensitive_data_in_dossier_payload(payload: Dict[str, Any]) -> PaperSafeDossierValidationReport:
    issues = []
    text = json.dumps(payload)
    if "api_key" in text.lower() or "secret" in text.lower() or "token" in text.lower():
         issues.append(PaperSafeDossierValidationIssue("ERROR", "payload", "Potential secret leak in payload"))
    return _build_report(issues)

def validate_no_live_execution_language_in_dossier(text: str) -> PaperSafeDossierValidationReport:
    issues = []
    text_lower = text.lower()
    bad_phrases = ["live approved", "sent to broker", "kesin al", "garanti", "gerçek emir", "kesin kâr"]
    for phrase in bad_phrases:
         if phrase in text_lower:
             issues.append(PaperSafeDossierValidationIssue("ERROR", "text", f"Live execution language detected: {phrase}"))
    return _build_report(issues)

def validate_no_active_paper_language_in_dossier(text: str) -> PaperSafeDossierValidationReport:
    issues = []
    text_lower = text.lower()
    bad_phrases = ["paper'a uygula", "canlıya al", "aktif et", "candidate kesin iyi"]
    for phrase in bad_phrases:
         if phrase in text_lower:
             issues.append(PaperSafeDossierValidationIssue("ERROR", "text", f"Active paper language detected: {phrase}"))
    return _build_report(issues)

def validate_no_paper_state_mutation_fields_in_dossier(payload: Dict[str, Any]) -> PaperSafeDossierValidationReport:
    issues = []
    bad_fields = ["paper_state_committed", "paper_order_executed", "paper_order_created", "portfolio_state_mutated", "position_mutated", "cash_mutated", "equity_mutated"]
    for field in bad_fields:
        if payload.get(field) is True:
             issues.append(PaperSafeDossierValidationIssue("ERROR", field, f"Mutation field {field} must not be True"))
    return _build_report(issues)

def validate_no_broker_execution_fields_in_dossier(payload: Dict[str, Any]) -> PaperSafeDossierValidationReport:
    issues = []
    bad_fields = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    for field in bad_fields:
         if field in payload and payload[field] is not None:
             issues.append(PaperSafeDossierValidationIssue("ERROR", field, f"Broker field {field} is present"))
    return _build_report(issues)

def paper_safe_dossier_validation_report_to_text(report: PaperSafeDossierValidationReport) -> str:
    lines = [f"Validation Report - Valid: {report.valid}"]
    lines.append(f"Errors: {report.error_count} | Warnings: {report.warning_count} | Blocked: {report.blocked_count}")
    for i in report.issues:
        lines.append(f"[{i.severity}] {i.field}: {i.message}")
    return "\n".join(lines)

def assert_paper_safe_dossier_valid(report: PaperSafeDossierValidationReport) -> None:
    if not report.valid:
        raise PaperSafeDossierValidationError("Paper Safe Dossier Validation Failed:\n" + paper_safe_dossier_validation_report_to_text(report))
