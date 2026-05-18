from dataclasses import dataclass, field
from typing import Any
import uuid

from usa_signal_bot.core.enums import (
    ResearchRunStatus,
    ResearchRunType,
    ExperimentExecutionMode,
    ExperimentArtifactType,
    ComparisonOutcome,
    MetricDeltaDirection,
    GateEvaluationMode,
    ResearchExecutionReportType
)
from usa_signal_bot.core.exceptions import ResearchExecutionValidationError
from usa_signal_bot.core.serialization import enum_to_value

@dataclass
class ConfigSnapshot:
    snapshot_id: str
    created_at_utc: str
    snapshot_type: ResearchRunType
    config_hash: str
    config_payload: dict[str, Any]
    source_ref: str | None
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ExperimentRunContext:
    context_id: str
    created_at_utc: str
    experiment_id: str | None
    hypothesis_id: str | None
    run_type: ResearchRunType
    execution_mode: ExperimentExecutionMode
    config_snapshot: ConfigSnapshot | None
    validation_plan: dict[str, Any]
    acceptance_gates: list[dict[str, Any]]
    data_scope: dict[str, Any]
    allowed_to_modify_config: bool
    allowed_to_send_orders: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ExperimentArtifact:
    artifact_id: str
    created_at_utc: str
    artifact_type: ExperimentArtifactType
    run_id: str | None
    path: str | None
    payload_summary: dict[str, Any]
    checksum: str | None
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ResearchRun:
    run_id: str
    created_at_utc: str
    experiment_id: str | None
    hypothesis_id: str | None
    run_type: ResearchRunType
    status: ResearchRunStatus
    execution_mode: ExperimentExecutionMode
    context: ExperimentRunContext | None
    artifacts: list[ExperimentArtifact]
    metrics: dict[str, Any]
    started_at_utc: str | None
    completed_at_utc: str | None
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class MetricComparison:
    comparison_id: str
    metric_name: str
    baseline_value: float | None
    candidate_value: float | None
    delta_value: float | None
    delta_pct: float | None
    direction: MetricDeltaDirection
    interpretation: str
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class AcceptanceGateEvaluation:
    evaluation_id: str
    gate_type: str
    gate_status: str
    evaluation_mode: GateEvaluationMode
    baseline_value: Any | None
    candidate_value: Any | None
    threshold: Any | None
    passed: bool | None
    explanation: str
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ExperimentComparisonReport:
    report_id: str
    created_at_utc: str
    experiment_id: str | None
    baseline_run_id: str | None
    candidate_run_id: str | None
    outcome: ComparisonOutcome
    metric_comparisons: list[MetricComparison]
    gate_evaluations: list[AcceptanceGateEvaluation]
    attribution_delta: dict[str, Any]
    diagnostics_delta: dict[str, Any]
    summary: dict[str, Any]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ResearchExecutionReview:
    review_id: str
    created_at_utc: str
    report_type: ResearchExecutionReportType
    runs: list[ResearchRun]
    comparison_reports: list[ExperimentComparisonReport]
    artifacts: list[ExperimentArtifact]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def config_snapshot_to_dict(item: ConfigSnapshot) -> dict:
    return {
        "snapshot_id": item.snapshot_id,
        "created_at_utc": item.created_at_utc,
        "snapshot_type": enum_to_value(item.snapshot_type),
        "config_hash": item.config_hash,
        "config_payload": item.config_payload,
        "source_ref": item.source_ref,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def experiment_run_context_to_dict(item: ExperimentRunContext) -> dict:
    return {
        "context_id": item.context_id,
        "created_at_utc": item.created_at_utc,
        "experiment_id": item.experiment_id,
        "hypothesis_id": item.hypothesis_id,
        "run_type": enum_to_value(item.run_type),
        "execution_mode": enum_to_value(item.execution_mode),
        "config_snapshot": config_snapshot_to_dict(item.config_snapshot) if item.config_snapshot else None,
        "validation_plan": item.validation_plan,
        "acceptance_gates": item.acceptance_gates,
        "data_scope": item.data_scope,
        "allowed_to_modify_config": item.allowed_to_modify_config,
        "allowed_to_send_orders": item.allowed_to_send_orders,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def experiment_artifact_to_dict(item: ExperimentArtifact) -> dict:
    return {
        "artifact_id": item.artifact_id,
        "created_at_utc": item.created_at_utc,
        "artifact_type": enum_to_value(item.artifact_type),
        "run_id": item.run_id,
        "path": item.path,
        "payload_summary": item.payload_summary,
        "checksum": item.checksum,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def research_run_to_dict(item: ResearchRun) -> dict:
    return {
        "run_id": item.run_id,
        "created_at_utc": item.created_at_utc,
        "experiment_id": item.experiment_id,
        "hypothesis_id": item.hypothesis_id,
        "run_type": enum_to_value(item.run_type),
        "status": enum_to_value(item.status),
        "execution_mode": enum_to_value(item.execution_mode),
        "context": experiment_run_context_to_dict(item.context) if item.context else None,
        "artifacts": [experiment_artifact_to_dict(a) for a in item.artifacts],
        "metrics": item.metrics,
        "started_at_utc": item.started_at_utc,
        "completed_at_utc": item.completed_at_utc,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def metric_comparison_to_dict(item: MetricComparison) -> dict:
    return {
        "comparison_id": item.comparison_id,
        "metric_name": item.metric_name,
        "baseline_value": item.baseline_value,
        "candidate_value": item.candidate_value,
        "delta_value": item.delta_value,
        "delta_pct": item.delta_pct,
        "direction": enum_to_value(item.direction),
        "interpretation": item.interpretation,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def acceptance_gate_evaluation_to_dict(item: AcceptanceGateEvaluation) -> dict:
    return {
        "evaluation_id": item.evaluation_id,
        "gate_type": item.gate_type,
        "gate_status": item.gate_status,
        "evaluation_mode": enum_to_value(item.evaluation_mode),
        "baseline_value": item.baseline_value,
        "candidate_value": item.candidate_value,
        "threshold": item.threshold,
        "passed": item.passed,
        "explanation": item.explanation,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def experiment_comparison_report_to_dict(item: ExperimentComparisonReport) -> dict:
    return {
        "report_id": item.report_id,
        "created_at_utc": item.created_at_utc,
        "experiment_id": item.experiment_id,
        "baseline_run_id": item.baseline_run_id,
        "candidate_run_id": item.candidate_run_id,
        "outcome": enum_to_value(item.outcome),
        "metric_comparisons": [metric_comparison_to_dict(mc) for mc in item.metric_comparisons],
        "gate_evaluations": [acceptance_gate_evaluation_to_dict(ge) for ge in item.gate_evaluations],
        "attribution_delta": item.attribution_delta,
        "diagnostics_delta": item.diagnostics_delta,
        "summary": item.summary,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def research_execution_review_to_dict(item: ResearchExecutionReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": enum_to_value(item.report_type),
        "runs": [research_run_to_dict(r) for r in item.runs],
        "comparison_reports": [experiment_comparison_report_to_dict(cr) for cr in item.comparison_reports],
        "artifacts": [experiment_artifact_to_dict(a) for a in item.artifacts],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors
    }

def validate_config_snapshot(item: ConfigSnapshot) -> None:
    for k in item.config_payload:
        if any(secret_term in k.lower() for secret_term in ["api_key", "token", "secret", "password"]):
            if item.config_payload[k] and item.config_payload[k] != "[REDACTED]":
                raise ResearchExecutionValidationError("Config snapshot contains unredacted secret.")

def validate_experiment_run_context(item: ExperimentRunContext) -> None:
    if item.allowed_to_modify_config:
        raise ResearchExecutionValidationError("allowed_to_modify_config MUST be false.")
    if item.allowed_to_send_orders:
        raise ResearchExecutionValidationError("allowed_to_send_orders MUST be false.")

def validate_research_run(item: ResearchRun) -> None:
    if item.context:
        validate_experiment_run_context(item.context)

def validate_experiment_comparison_report(item: ExperimentComparisonReport) -> None:
    pass

def create_config_snapshot_id(prefix: str = "config_snapshot") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_experiment_run_context_id(prefix: str = "run_context") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_experiment_artifact_id(prefix: str = "artifact") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_research_run_id(prefix: str = "research_run") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_metric_comparison_id(metric_name: str) -> str:
    return f"comp_{metric_name}_{uuid.uuid4().hex[:8]}"

def create_acceptance_gate_evaluation_id(gate_type: str) -> str:
    return f"eval_{gate_type}_{uuid.uuid4().hex[:8]}"

def create_experiment_comparison_report_id(prefix: str = "comparison_report") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_research_execution_review_id(prefix: str = "research_execution_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
