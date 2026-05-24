from dataclasses import dataclass, field
from typing import Any
import re
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import (
    LocalPaperAdmissionSimulatorGateDossier,
    SimulatorAcceptanceSeal,
    PaperSandboxRuntimeAdmissionBlockerEvent,
    SimulatorDossierFullReview
)

@dataclass
class SimulatorDossierValidationIssue:
    severity: str
    message: str
    field: str | None = None
    details_dict: dict[str, Any] = None

@dataclass
class SimulatorDossierValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[SimulatorDossierValidationIssue]
    warnings: list[str]
    errors: list[str]

def _create_report(issues: list[SimulatorDossierValidationIssue]) -> SimulatorDossierValidationReport:
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    errors = [i.message for i in issues if i.severity == "ERROR"]
    blocked = [i.message for i in issues if i.severity == "BLOCKED"]

    return SimulatorDossierValidationReport(
        valid=len(errors) == 0 and len(blocked) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_simulator_dossier_report(item: LocalPaperAdmissionSimulatorGateDossier) -> SimulatorDossierValidationReport:
    issues = []
    if not item.activation_denied:
        issues.append(SimulatorDossierValidationIssue("ERROR", "activation_denied is false"))
    if item.activation_allowed:
        issues.append(SimulatorDossierValidationIssue("ERROR", "activation_allowed is true"))
    if item.admission_allowed:
        issues.append(SimulatorDossierValidationIssue("ERROR", "admission_allowed is true"))
    if item.transition_allowed:
        issues.append(SimulatorDossierValidationIssue("ERROR", "transition_allowed is true"))
    if item.simulator_admission_allowed:
        issues.append(SimulatorDossierValidationIssue("ERROR", "simulator_admission_allowed is true"))
    if item.local_paper_simulator_allowed:
        issues.append(SimulatorDossierValidationIssue("ERROR", "local_paper_simulator_allowed is true"))
    if item.sandbox_runtime_admission_allowed:
        issues.append(SimulatorDossierValidationIssue("ERROR", "sandbox_runtime_admission_allowed is true"))
    if item.paper_sandbox_runtime_allowed:
        issues.append(SimulatorDossierValidationIssue("ERROR", "paper_sandbox_runtime_allowed is true"))
    if item.rehearsal_allowed:
        issues.append(SimulatorDossierValidationIssue("ERROR", "rehearsal_allowed is true"))
    if item.paper_mode_rehearsal_allowed:
        issues.append(SimulatorDossierValidationIssue("ERROR", "paper_mode_rehearsal_allowed is true"))
    if not item.all_writes_blocked:
        issues.append(SimulatorDossierValidationIssue("ERROR", "all_writes_blocked is false"))
    if item.order_created:
        issues.append(SimulatorDossierValidationIssue("ERROR", "order_created is true"))
    if item.mutation_detected:
        issues.append(SimulatorDossierValidationIssue("ERROR", "mutation_detected is true"))
    if item.allows_active_paper:
        issues.append(SimulatorDossierValidationIssue("ERROR", "allows_active_paper is true"))
    if item.allows_broker_execution:
        issues.append(SimulatorDossierValidationIssue("ERROR", "allows_broker_execution is true"))
    if item.allows_paper_state_mutation:
        issues.append(SimulatorDossierValidationIssue("ERROR", "allows_paper_state_mutation is true"))
    if item.allows_config_patch:
        issues.append(SimulatorDossierValidationIssue("ERROR", "allows_config_patch is true"))
    if item.allows_telegram_real_send:
        issues.append(SimulatorDossierValidationIssue("ERROR", "allows_telegram_real_send is true"))
    return _create_report(issues)

def validate_simulator_acceptance_seal_report(item: SimulatorAcceptanceSeal) -> SimulatorDossierValidationReport:
    issues = []
    if item.allows_sandbox_runtime_admission:
        issues.append(SimulatorDossierValidationIssue("ERROR", "allows_sandbox_runtime_admission is true"))
    if item.allows_paper_sandbox_runtime:
        issues.append(SimulatorDossierValidationIssue("ERROR", "allows_paper_sandbox_runtime is true"))
    return _create_report(issues)

def validate_sandbox_runtime_admission_blocker_event_report(item: PaperSandboxRuntimeAdmissionBlockerEvent) -> SimulatorDossierValidationReport:
    issues = []
    if not item.blocked:
        issues.append(SimulatorDossierValidationIssue("ERROR", "blocked is false"))
    if item.sandbox_runtime_admission_allowed:
        issues.append(SimulatorDossierValidationIssue("ERROR", "sandbox_runtime_admission_allowed is true"))
    if item.paper_sandbox_runtime_allowed:
        issues.append(SimulatorDossierValidationIssue("ERROR", "paper_sandbox_runtime_allowed is true"))
    if item.active_paper_enabled:
        issues.append(SimulatorDossierValidationIssue("ERROR", "active_paper_enabled is true"))
    if item.order_created:
        issues.append(SimulatorDossierValidationIssue("ERROR", "order_created is true"))
    if item.paper_state_mutated:
        issues.append(SimulatorDossierValidationIssue("ERROR", "paper_state_mutated is true"))
    return _create_report(issues)

def validate_simulator_dossier_full_review_report(item: SimulatorDossierFullReview) -> SimulatorDossierValidationReport:
    all_issues = []
    for d in item.dossiers:
        all_issues.extend(validate_simulator_dossier_report(d).issues)
    for s in item.acceptance_seals:
        all_issues.extend(validate_simulator_acceptance_seal_report(s).issues)
    for e in item.sandbox_runtime_admission_blocker_events:
        all_issues.extend(validate_sandbox_runtime_admission_blocker_event_report(e).issues)
    return _create_report(all_issues)

def validate_no_sensitive_data_in_simulator_dossier_payload(payload: dict[str, Any]) -> SimulatorDossierValidationReport:
    issues = []
    s = str(payload).lower()
    for secret in ["api_key", "secret", "token", "password"]:
        if secret in s:
            issues.append(SimulatorDossierValidationIssue("ERROR", f"Potential secret found: {secret}"))
    return _create_report(issues)

def validate_no_live_execution_language_in_simulator_dossier(text: str) -> SimulatorDossierValidationReport:
    issues = []
    s = text.lower()
    for phrase in ["live approved", "sent to broker", "kesin al", "garanti", "gerçek emir", "kesin kâr"]:
        if phrase in s:
            issues.append(SimulatorDossierValidationIssue("ERROR", f"Live execution language found: {phrase}"))
    return _create_report(issues)

def validate_no_active_paper_language_in_simulator_dossier(text: str) -> SimulatorDossierValidationReport:
    issues = []
    s = text.lower()
    for phrase in ["paper'a uygula", "canlıya al", "aktif et", "candidate kesin iyi"]:
        if phrase in s:
            issues.append(SimulatorDossierValidationIssue("ERROR", f"Active paper language found: {phrase}"))
    return _create_report(issues)

def validate_no_sandbox_runtime_admission_language(text: str) -> SimulatorDossierValidationReport:
    issues = []
    s = text.lower()
    for phrase in ["sandbox runtime başlat", "sandbox admission aç", "paper sandbox aç"]:
        if phrase in s:
            issues.append(SimulatorDossierValidationIssue("ERROR", f"Sandbox runtime admission language found: {phrase}"))
    return _create_report(issues)

def validate_no_paper_state_mutation_fields_in_simulator_dossier(payload: dict[str, Any]) -> SimulatorDossierValidationReport:
    issues = []
    keys = str(payload.keys())
    for f in ["paper_state_committed", "paper_order_executed", "paper_order_created", "portfolio_state_mutated", "position_mutated", "cash_mutated", "equity_mutated"]:
        if f in keys:
            issues.append(SimulatorDossierValidationIssue("ERROR", f"Paper state mutation field found: {f}"))
    return _create_report(issues)

def validate_no_broker_execution_fields_in_simulator_dossier(payload: dict[str, Any]) -> SimulatorDossierValidationReport:
    issues = []
    keys = str(payload.keys())
    for f in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
        if f in keys:
            issues.append(SimulatorDossierValidationIssue("ERROR", f"Broker execution field found: {f}"))
    return _create_report(issues)

def simulator_dossier_validation_report_to_text(report: SimulatorDossierValidationReport) -> str:
    lines = [
        "--- Simulator Dossier Validation Report ---",
        f"Valid: {report.valid}",
        f"Issues: {report.issue_count}",
        f"Errors: {report.error_count}"
    ]
    for issue in report.issues:
        lines.append(f"  - [{issue.severity}] {issue.message}")
    return "\n".join(lines)

def assert_simulator_dossier_valid(report: SimulatorDossierValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Simulator dossier is not valid: {report.errors}")
