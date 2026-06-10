from dataclasses import dataclass, field
from typing import Any, List, Optional
import json
from .workflow_models import (
    RepairQueueItem,
    ResearchHypothesis,
    ExperimentPlan,
    ParameterChangeProposal,
    AcceptanceGate,
    ResearchWorkflowReview,
    validate_repair_queue_item,
    validate_research_hypothesis,
    validate_parameter_change_proposal,
    validate_acceptance_gate,
    validate_experiment_plan,
    validate_research_workflow_review,
    _check_forbidden_language,
)
from ..core.exceptions import ResearchWorkflowValidationError


@dataclass
class ResearchWorkflowValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ResearchWorkflowValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[ResearchWorkflowValidationIssue]
    warnings: List[str]
    errors: List[str]


def _create_report(
    issues: List[ResearchWorkflowValidationIssue],
    warnings: List[str],
    errors: List[str],
) -> ResearchWorkflowValidationReport:
    err_count = len([i for i in issues if i.severity == "ERROR"]) + len(errors)
    return ResearchWorkflowValidationReport(
        valid=err_count == 0,
        issue_count=len(issues),
        warning_count=len([i for i in issues if i.severity == "WARNING"])
        + len(warnings),
        error_count=err_count,
        blocked_count=len([i for i in issues if i.severity == "BLOCKED"]),
        issues=issues,
        warnings=warnings,
        errors=errors,
    )


def _validate_items(
    items: List[Any], validation_func
) -> ResearchWorkflowValidationReport:
    issues = []
    errors = []
    for item in items:
        try:
            validation_func(item)
        except ResearchWorkflowValidationError as e:
            errors.append(str(e))
            issues.append(
                ResearchWorkflowValidationIssue(
                    severity="ERROR", field=None, message=str(e)
                )
            )
    return _create_report(issues, [], errors)


def validate_repair_items_report(
    items: List[RepairQueueItem],
) -> ResearchWorkflowValidationReport:
    return _validate_items(items, validate_repair_queue_item)


def validate_hypotheses_report(
    items: List[ResearchHypothesis],
) -> ResearchWorkflowValidationReport:
    return _validate_items(items, validate_research_hypothesis)


def validate_experiment_plans_report(
    items: List[ExperimentPlan],
) -> ResearchWorkflowValidationReport:
    return _validate_items(items, validate_experiment_plan)


def validate_parameter_proposals_report(
    items: List[ParameterChangeProposal],
) -> ResearchWorkflowValidationReport:
    return _validate_items(items, validate_parameter_change_proposal)


def validate_acceptance_gates_report(
    items: List[AcceptanceGate],
) -> ResearchWorkflowValidationReport:
    return _validate_items(items, validate_acceptance_gate)


def validate_research_workflow_review_report(
    item: ResearchWorkflowReview,
) -> ResearchWorkflowValidationReport:
    try:
        validate_research_workflow_review(item)
        return _create_report([], [], [])
    except ResearchWorkflowValidationError as e:
        return _create_report(
            [
                ResearchWorkflowValidationIssue(
                    severity="ERROR", field=None, message=str(e)
                )
            ],
            [],
            [str(e)],
        )


def validate_no_sensitive_data_in_workflow_payload(
    payload: dict[str, Any],
) -> ResearchWorkflowValidationReport:
    text = json.dumps(payload).lower()
    errors = []
    if "api_key" in text or "token" in text or "secret" in text or "password" in text:
        errors.append("Potential sensitive data leak detected in payload")
    issues = [
        ResearchWorkflowValidationIssue(severity="ERROR", field=None, message=e)
        for e in errors
    ]
    return _create_report(issues, [], errors)


def validate_no_live_execution_language_in_workflow(
    text: str,
) -> ResearchWorkflowValidationReport:
    errors = []
    try:
        _check_forbidden_language(text)
    except ResearchWorkflowValidationError as e:
        errors.append(str(e))
    issues = [
        ResearchWorkflowValidationIssue(severity="ERROR", field=None, message=e)
        for e in errors
    ]
    return _create_report(issues, [], errors)


def validate_no_auto_apply_or_optimizer_language(
    text: str,
) -> ResearchWorkflowValidationReport:
    # `_check_forbidden_language` handles this as well
    return validate_no_live_execution_language_in_workflow(text)


def validate_no_broker_execution_fields_in_workflow(
    payload: dict[str, Any],
) -> ResearchWorkflowValidationReport:
    text = json.dumps(payload).lower()
    errors = []
    forbidden = [
        "broker_order_id",
        "live_order_id",
        "sent_to_broker",
        "execution_venue",
        "real_fill_id",
    ]
    for f in forbidden:
        if f in text:
            errors.append(f"Forbidden broker field found: {f}")
    issues = [
        ResearchWorkflowValidationIssue(severity="ERROR", field=None, message=e)
        for e in errors
    ]
    return _create_report(issues, [], errors)


def research_workflow_validation_report_to_text(
    report: ResearchWorkflowValidationReport,
) -> str:
    lines = [f"Validation Report (Valid: {report.valid})"]
    lines.append(f"Errors: {report.error_count}, Warnings: {report.warning_count}")
    for i in report.issues:
        lines.append(f"  [{i.severity}] {i.message}")
    return "\n".join(lines)


def assert_research_workflow_valid(report: ResearchWorkflowValidationReport) -> None:
    if not report.valid:
        raise ResearchWorkflowValidationError(
            f"Research workflow validation failed: {report.errors}"
        )
