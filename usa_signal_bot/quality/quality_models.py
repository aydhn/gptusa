"""Quality models for the USA Signal Bot."""

from dataclasses import dataclass
import dataclasses
from typing import Any, Dict, List
import uuid
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    QualityDimension,
    QualityStatus,
    QualitySeverity,
    ReadinessGateStatus,
    AcceptanceDecision,
    AcceptanceScope,
    GateRuleOperator,
    QualityReportType,
)

def create_quality_issue_id(prefix: str = "q_issue") -> str:
    """Creates a unique quality issue ID."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_scorecard_id(prefix: str = "scorecard") -> str:
    """Creates a unique scorecard ID."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_gate_id(prefix: str = "gate") -> str:
    """Creates a unique gate ID."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_acceptance_id(prefix: str = "acceptance") -> str:
    """Creates a unique acceptance ID."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

@dataclass
class QualityIssue:
    issue_id: str
    dimension: QualityDimension
    severity: QualitySeverity
    status: QualityStatus
    title: str
    message: str
    field: str | None = None
    evidence: dict[str, Any] = dataclasses.field(default_factory=dict)

@dataclass
class QualityDimensionScore:
    dimension: QualityDimension
    score: float | None
    weight: float
    status: QualityStatus
    issue_count: int
    critical_count: int
    warning_count: int
    summary: str
    issues: list[QualityIssue]
    metadata: dict[str, Any] = dataclasses.field(default_factory=dict)

@dataclass
class ResearchQualityScorecard:
    scorecard_id: str
    created_at_utc: str
    report_type: QualityReportType
    overall_score: float | None
    overall_status: QualityStatus
    dimensions: list[QualityDimensionScore]
    issues: list[QualityIssue]
    warnings: list[str]
    errors: list[str]
    release_packaging_quality_score: float = 0.0
    artifact_freeze_completeness_score: float = 0.0
    bundle_manifest_quality_score: float = 0.0
    bundle_safety_score: float = 0.0
    checksum_verification_score: float = 0.0
    metadata: dict[str, Any] = dataclasses.field(default_factory=dict)

@dataclass
class GateRule:
    rule_id: str
    name: str
    dimension: QualityDimension
    operator: GateRuleOperator
    field_path: str
    threshold: Any | None = None
    lower: float | None = None
    upper: float | None = None
    required: bool = True
    severity: QualitySeverity = QualitySeverity.HIGH
    enabled: bool = True
    description: str | None = None

@dataclass
class GateRuleResult:
    rule_id: str
    name: str
    dimension: QualityDimension
    status: ReadinessGateStatus
    observed_value: Any
    message: str
    severity: QualitySeverity
    evidence: dict[str, Any] = dataclasses.field(default_factory=dict)

@dataclass
class ProductionReadinessGateResult:
    gate_id: str
    created_at_utc: str
    scope: AcceptanceScope
    status: ReadinessGateStatus
    rule_results: list[GateRuleResult]
    passed_count: int
    warning_count: int
    failed_count: int
    blocked_count: int
    warnings: list[str]
    errors: list[str]

@dataclass
class SystemAcceptanceResult:
    acceptance_id: str
    created_at_utc: str
    scope: AcceptanceScope
    decision: AcceptanceDecision
    scorecard: ResearchQualityScorecard
    gate_result: ProductionReadinessGateResult
    acceptance_summary: str
    required_actions: list[str]
    optional_actions: list[str]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def quality_issue_to_dict(issue: QualityIssue) -> dict:
    return {
        "issue_id": issue.issue_id,
        "dimension": issue.dimension.value if isinstance(issue.dimension, QualityDimension) else issue.dimension,
        "severity": issue.severity.value if isinstance(issue.severity, QualitySeverity) else issue.severity,
        "status": issue.status.value if isinstance(issue.status, QualityStatus) else issue.status,
        "title": issue.title,
        "message": issue.message,
        "field": issue.field,
        "evidence": issue.evidence,
    }

def quality_dimension_score_to_dict(score: QualityDimensionScore) -> dict:
    return {
        "dimension": score.dimension.value if isinstance(score.dimension, QualityDimension) else score.dimension,
        "score": score.score,
        "weight": score.weight,
        "status": score.status.value if isinstance(score.status, QualityStatus) else score.status,
        "issue_count": score.issue_count,
        "critical_count": score.critical_count,
        "warning_count": score.warning_count,
        "summary": score.summary,
        "issues": [quality_issue_to_dict(i) for i in score.issues],
        "metadata": score.metadata,
    }

def research_quality_scorecard_to_dict(scorecard: ResearchQualityScorecard) -> dict:
    return {
        "scorecard_id": scorecard.scorecard_id,
        "created_at_utc": scorecard.created_at_utc,
        "report_type": scorecard.report_type.value if isinstance(scorecard.report_type, QualityReportType) else scorecard.report_type,
        "overall_score": scorecard.overall_score,
        "overall_status": scorecard.overall_status.value if isinstance(scorecard.overall_status, QualityStatus) else scorecard.overall_status,
        "dimensions": [quality_dimension_score_to_dict(d) for d in scorecard.dimensions],
        "issues": [quality_issue_to_dict(i) for i in scorecard.issues],
        "warnings": scorecard.warnings,
        "errors": scorecard.errors,
        "metadata": scorecard.metadata,
    }

def gate_rule_to_dict(rule: GateRule) -> dict:
    return {
        "rule_id": rule.rule_id,
        "name": rule.name,
        "dimension": rule.dimension.value if isinstance(rule.dimension, QualityDimension) else rule.dimension,
        "operator": rule.operator.value if isinstance(rule.operator, GateRuleOperator) else rule.operator,
        "field_path": rule.field_path,
        "threshold": rule.threshold,
        "lower": rule.lower,
        "upper": rule.upper,
        "required": rule.required,
        "severity": rule.severity.value if isinstance(rule.severity, QualitySeverity) else rule.severity,
        "enabled": rule.enabled,
        "description": rule.description,
    }

def gate_rule_result_to_dict(result: GateRuleResult) -> dict:
    return {
        "rule_id": result.rule_id,
        "name": result.name,
        "dimension": result.dimension.value if isinstance(result.dimension, QualityDimension) else result.dimension,
        "status": result.status.value if isinstance(result.status, ReadinessGateStatus) else result.status,
        "observed_value": result.observed_value,
        "message": result.message,
        "severity": result.severity.value if isinstance(result.severity, QualitySeverity) else result.severity,
        "evidence": result.evidence,
    }

def production_readiness_gate_result_to_dict(result: ProductionReadinessGateResult) -> dict:
    return {
        "gate_id": result.gate_id,
        "created_at_utc": result.created_at_utc,
        "scope": result.scope.value if isinstance(result.scope, AcceptanceScope) else result.scope,
        "status": result.status.value if isinstance(result.status, ReadinessGateStatus) else result.status,
        "rule_results": [gate_rule_result_to_dict(r) for r in result.rule_results],
        "passed_count": result.passed_count,
        "warning_count": result.warning_count,
        "failed_count": result.failed_count,
        "blocked_count": result.blocked_count,
        "warnings": result.warnings,
        "errors": result.errors,
    }

def system_acceptance_result_to_dict(result: SystemAcceptanceResult) -> dict:
    return {
        "acceptance_id": result.acceptance_id,
        "created_at_utc": result.created_at_utc,
        "scope": result.scope.value if isinstance(result.scope, AcceptanceScope) else result.scope,
        "decision": result.decision.value if isinstance(result.decision, AcceptanceDecision) else result.decision,
        "scorecard": research_quality_scorecard_to_dict(result.scorecard),
        "gate_result": production_readiness_gate_result_to_dict(result.gate_result),
        "acceptance_summary": result.acceptance_summary,
        "required_actions": result.required_actions,
        "optional_actions": result.optional_actions,
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors,
    }

def validate_quality_issue(issue: QualityIssue) -> None:
    if not issue.issue_id:
        raise ValueError("issue_id is required")
    if not issue.title:
        raise ValueError("title is required")
    if not issue.message:
        raise ValueError("message is required")

def validate_quality_dimension_score(score: QualityDimensionScore) -> None:
    if score.weight < 0:
        raise ValueError("weight cannot be negative")
    if score.score is not None and (score.score < 0 or score.score > 100):
        raise ValueError("score must be between 0 and 100")

def validate_research_quality_scorecard(scorecard: ResearchQualityScorecard) -> None:
    if not scorecard.scorecard_id:
        raise ValueError("scorecard_id is required")
    if scorecard.overall_score is not None and (scorecard.overall_score < 0 or scorecard.overall_score > 100):
        raise ValueError("overall_score must be between 0 and 100")
    for dim in scorecard.dimensions:
        validate_quality_dimension_score(dim)
    for issue in scorecard.issues:
        validate_quality_issue(issue)

def validate_gate_rule(rule: GateRule) -> None:
    if not rule.rule_id:
        raise ValueError("rule_id is required")
    if not rule.name:
        raise ValueError("name is required")
    if not rule.field_path:
        raise ValueError("field_path is required")

def validate_system_acceptance_result(result: SystemAcceptanceResult) -> None:
    if not result.acceptance_id:
        raise ValueError("acceptance_id is required")
    validate_research_quality_scorecard(result.scorecard)

    # Acceptance PASS is not a live trading approval
    if result.decision in [AcceptanceDecision.ACCEPTED_FOR_LOCAL_RESEARCH, AcceptanceDecision.ACCEPTED_WITH_WARNINGS]:
        # Additional checks can be added here
        pass
