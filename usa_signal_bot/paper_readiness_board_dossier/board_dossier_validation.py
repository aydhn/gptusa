from dataclasses import dataclass, field
from typing import Any
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import (
    PaperReadinessBoardDossier,
    AcceptanceBoardSeal,
    ShadowLaunchBlockerEvent,
    BoardDossierFullReview
)

@dataclass
class BoardDossierValidationIssue:
    severity: str
    message: str
    issue_field: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class BoardDossierValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[BoardDossierValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_board_dossier_report(item: PaperReadinessBoardDossier) -> BoardDossierValidationReport:
    issues = []

    if not item.sealed:
        issues.append(BoardDossierValidationIssue("ERROR", "Dossier must be sealed", "sealed"))
    if not item.immutable:
        issues.append(BoardDossierValidationIssue("ERROR", "Dossier must be immutable", "immutable"))
    if not item.activation_denied:
        issues.append(BoardDossierValidationIssue("BLOCK", "activation_denied must be True", "activation_denied"))
    if item.activation_allowed:
        issues.append(BoardDossierValidationIssue("BLOCK", "activation_allowed must be False", "activation_allowed"))
    if item.admission_allowed:
        issues.append(BoardDossierValidationIssue("BLOCK", "admission_allowed must be False", "admission_allowed"))
    if item.transition_allowed:
        issues.append(BoardDossierValidationIssue("BLOCK", "transition_allowed must be False", "transition_allowed"))
    if item.shadow_launch_allowed:
        issues.append(BoardDossierValidationIssue("BLOCK", "shadow_launch_allowed must be False", "shadow_launch_allowed"))
    if item.paper_mode_launch_allowed:
        issues.append(BoardDossierValidationIssue("BLOCK", "paper_mode_launch_allowed must be False", "paper_mode_launch_allowed"))
    if not item.all_writes_blocked:
        issues.append(BoardDossierValidationIssue("BLOCK", "all_writes_blocked must be True", "all_writes_blocked"))
    if item.order_created:
        issues.append(BoardDossierValidationIssue("BLOCK", "order_created must be False", "order_created"))
    if item.mutation_detected:
        issues.append(BoardDossierValidationIssue("BLOCK", "mutation_detected must be False", "mutation_detected"))
    if item.allows_active_paper:
        issues.append(BoardDossierValidationIssue("BLOCK", "allows_active_paper must be False", "allows_active_paper"))
    if item.allows_broker_execution:
        issues.append(BoardDossierValidationIssue("BLOCK", "allows_broker_execution must be False", "allows_broker_execution"))
    if item.allows_paper_state_mutation:
        issues.append(BoardDossierValidationIssue("BLOCK", "allows_paper_state_mutation must be False", "allows_paper_state_mutation"))
    if item.allows_config_patch:
        issues.append(BoardDossierValidationIssue("BLOCK", "allows_config_patch must be False", "allows_config_patch"))
    if item.allows_telegram_real_send:
        issues.append(BoardDossierValidationIssue("BLOCK", "allows_telegram_real_send must be False", "allows_telegram_real_send"))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    blocked = [i.message for i in issues if i.severity == "BLOCK"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return BoardDossierValidationReport(
        valid=len(errors) == 0 and len(blocked) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=issues,
        warnings=warnings,
        errors=errors + blocked
    )

def validate_acceptance_board_seal_report(item: AcceptanceBoardSeal) -> BoardDossierValidationReport:
    issues = []

    if item.allows_shadow_launch:
        issues.append(BoardDossierValidationIssue("BLOCK", "allows_shadow_launch must be False", "allows_shadow_launch"))
    if item.allows_paper_mode_launch:
        issues.append(BoardDossierValidationIssue("BLOCK", "allows_paper_mode_launch must be False", "allows_paper_mode_launch"))
    if item.allows_active_paper:
        issues.append(BoardDossierValidationIssue("BLOCK", "allows_active_paper must be False", "allows_active_paper"))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    blocked = [i.message for i in issues if i.severity == "BLOCK"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return BoardDossierValidationReport(
        valid=len(errors) == 0 and len(blocked) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=issues,
        warnings=warnings,
        errors=errors + blocked
    )

def validate_shadow_launch_blocker_event_report(item: ShadowLaunchBlockerEvent) -> BoardDossierValidationReport:
    issues = []

    if not item.blocked:
        issues.append(BoardDossierValidationIssue("BLOCK", "Event must be blocked", "blocked"))
    if item.shadow_launch_allowed:
        issues.append(BoardDossierValidationIssue("BLOCK", "shadow_launch_allowed must be False", "shadow_launch_allowed"))
    if item.paper_mode_launch_allowed:
        issues.append(BoardDossierValidationIssue("BLOCK", "paper_mode_launch_allowed must be False", "paper_mode_launch_allowed"))
    if item.active_paper_enabled:
        issues.append(BoardDossierValidationIssue("BLOCK", "active_paper_enabled must be False", "active_paper_enabled"))
    if item.order_created:
        issues.append(BoardDossierValidationIssue("BLOCK", "order_created must be False", "order_created"))
    if item.paper_state_mutated:
        issues.append(BoardDossierValidationIssue("BLOCK", "paper_state_mutated must be False", "paper_state_mutated"))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    blocked = [i.message for i in issues if i.severity == "BLOCK"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return BoardDossierValidationReport(
        valid=len(errors) == 0 and len(blocked) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=issues,
        warnings=warnings,
        errors=errors + blocked
    )

def validate_board_dossier_full_review_report(item: BoardDossierFullReview) -> BoardDossierValidationReport:
    all_issues = []

    for d in item.dossiers:
        rep = validate_board_dossier_report(d)
        all_issues.extend(rep.issues)

    for s in item.acceptance_board_seals:
        rep = validate_acceptance_board_seal_report(s)
        all_issues.extend(rep.issues)

    for e in item.shadow_launch_blocker_events:
        rep = validate_shadow_launch_blocker_event_report(e)
        all_issues.extend(rep.issues)

    errors = [i.message for i in all_issues if i.severity == "ERROR"]
    blocked = [i.message for i in all_issues if i.severity == "BLOCK"]
    warnings = [i.message for i in all_issues if i.severity == "WARNING"]

    return BoardDossierValidationReport(
        valid=len(errors) == 0 and len(blocked) == 0,
        issue_count=len(all_issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=all_issues,
        warnings=warnings,
        errors=errors + blocked
    )

def validate_no_sensitive_data_in_board_dossier_payload(payload: dict[str, Any]) -> BoardDossierValidationReport:
    issues = []
    import json
    text = json.dumps(payload, default=str).lower()
    if "api_key" in text or "secret" in text or "token" in text or "password" in text:
        issues.append(BoardDossierValidationIssue("BLOCK", "Potential token/secret/api_key leak detected"))

    return BoardDossierValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=0,
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_no_live_execution_language_in_board_dossier(text: str) -> BoardDossierValidationReport:
    issues = []
    t = text.lower()
    banned = ["live approved", "sent to broker", "kesin al", "garanti", "canlıya al", "gerçek emir", "kesin kâr"]
    for word in banned:
        if word in t:
            issues.append(BoardDossierValidationIssue("BLOCK", f"Live execution language detected: {word}"))

    return BoardDossierValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=0,
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_no_active_paper_language_in_board_dossier(text: str) -> BoardDossierValidationReport:
    issues = []
    t = text.lower()
    banned = ["paper'a uygula", "aktif et", "candidate kesin iyi"]
    for word in banned:
        if word in t:
            issues.append(BoardDossierValidationIssue("BLOCK", f"Active paper language detected: {word}"))

    return BoardDossierValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=0,
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_no_shadow_launch_language_in_board_dossier(text: str) -> BoardDossierValidationReport:
    issues = []
    t = text.lower()
    banned = ["shadow launch başlat", "paper mode başlat"]
    for word in banned:
        if word in t:
            issues.append(BoardDossierValidationIssue("BLOCK", f"Shadow launch language detected: {word}"))

    return BoardDossierValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=0,
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_no_paper_state_mutation_fields_in_board_dossier(payload: dict[str, Any]) -> BoardDossierValidationReport:
    issues = []
    import json
    text = json.dumps(payload, default=str)
    banned = [
        "paper_state_committed",
        "paper_order_executed",
        "paper_order_created",
        "portfolio_state_mutated",
        "position_mutated",
        "cash_mutated",
        "equity_mutated"
    ]
    for word in banned:
        if f'"{word}": true' in text or f'"{word}": True' in text:
            issues.append(BoardDossierValidationIssue("BLOCK", f"Paper state mutation field detected true: {word}"))

    return BoardDossierValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=0,
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_no_broker_execution_fields_in_board_dossier(payload: dict[str, Any]) -> BoardDossierValidationReport:
    issues = []
    import json
    text = json.dumps(payload, default=str)
    banned = [
        "broker_order_id",
        "live_order_id",
        "sent_to_broker",
        "execution_venue",
        "real_fill_id"
    ]
    for word in banned:
        if f'"{word}"' in text:
            issues.append(BoardDossierValidationIssue("BLOCK", f"Broker execution field detected: {word}"))

    return BoardDossierValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=0,
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def board_dossier_validation_report_to_text(report: BoardDossierValidationReport) -> str:
    lines = [f"Validation Report (Valid: {report.valid})"]
    if report.issues:
        lines.append(f"  Issues ({report.issue_count}):")
        for i in report.issues:
            lines.append(f"    - [{i.severity}] {i.message} ({i.issue_field or 'general'})")
    return "\n".join(lines)

def assert_board_dossier_valid(report: BoardDossierValidationReport) -> None:
    if not report.valid:
        from usa_signal_bot.core.exceptions import BoardDossierValidationError
        raise BoardDossierValidationError(f"Validation failed with {report.blocked_count} blocking issues and {report.error_count} errors.")
