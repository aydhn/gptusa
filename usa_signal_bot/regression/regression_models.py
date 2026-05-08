from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    SnapshotComparisonStatus,
    RegressionDriftSeverity,
    GoldenDatasetStatus,
    RegressionArtifactType,
    RegressionStepName,
    RegressionStepStatus,
    RegressionRunStatus,
    ReleaseRehearsalScope,
    ReleaseCandidateStatus
)

@dataclass
class GoldenDatasetSpec:
    dataset_id: str
    name: str
    symbols: List[str]
    timeframe: str
    start_date: str
    end_date: str
    row_count_per_symbol: int
    status: GoldenDatasetStatus
    created_at_utc: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class GoldenSnapshot:
    snapshot_id: str
    name: str
    artifact_type: RegressionArtifactType
    created_at_utc: str
    checksum: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegressionStepResult:
    step_name: RegressionStepName
    status: RegressionStepStatus
    started_at_utc: Optional[str] = None
    completed_at_utc: Optional[str] = None
    duration_seconds: Optional[float] = None
    output_paths: Dict[str, str] = field(default_factory=dict)
    summary: Dict[str, Any] = field(default_factory=dict)
    snapshot: Optional[GoldenSnapshot] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class RegressionRunRequest:
    request_id: str
    scope: ReleaseRehearsalScope
    dataset_name: str
    use_existing_golden: bool = True
    update_baseline: bool = False
    compare_snapshots: bool = True
    write_outputs: bool = True
    fail_on_snapshot_drift: bool = False
    max_allowed_warnings: int = 20
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegressionRunResult:
    run_id: str
    created_at_utc: str
    status: RegressionRunStatus
    request: RegressionRunRequest
    dataset_spec: Optional[GoldenDatasetSpec] = None
    step_results: List[RegressionStepResult] = field(default_factory=list)
    snapshot_comparison: Dict[str, Any] = field(default_factory=dict)
    release_candidate_status: ReleaseCandidateStatus = ReleaseCandidateStatus.UNKNOWN
    manifest_path: Optional[str] = None
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class ReleaseRehearsalResult:
    rehearsal_id: str
    created_at_utc: str
    scope: ReleaseRehearsalScope
    status: ReleaseCandidateStatus
    regression_result: RegressionRunResult
    quality_acceptance_path: Optional[str] = None
    passed_steps: int = 0
    warning_steps: int = 0
    failed_steps: int = 0
    blocked_steps: int = 0
    required_actions: List[str] = field(default_factory=list)
    optional_actions: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    output_paths: Dict[str, str] = field(default_factory=dict)


def golden_dataset_spec_to_dict(spec: GoldenDatasetSpec) -> dict:
    return {
        "dataset_id": spec.dataset_id,
        "name": spec.name,
        "symbols": spec.symbols,
        "timeframe": spec.timeframe,
        "start_date": spec.start_date,
        "end_date": spec.end_date,
        "row_count_per_symbol": spec.row_count_per_symbol,
        "status": spec.status.value,
        "created_at_utc": spec.created_at_utc,
        "metadata": spec.metadata
    }

def golden_snapshot_to_dict(snapshot: GoldenSnapshot) -> dict:
    return {
        "snapshot_id": snapshot.snapshot_id,
        "name": snapshot.name,
        "artifact_type": snapshot.artifact_type.value,
        "created_at_utc": snapshot.created_at_utc,
        "checksum": snapshot.checksum,
        "payload": snapshot.payload,
        "metadata": snapshot.metadata
    }

def regression_step_result_to_dict(result: RegressionStepResult) -> dict:
    return {
        "step_name": result.step_name.value,
        "status": result.status.value,
        "started_at_utc": result.started_at_utc,
        "completed_at_utc": result.completed_at_utc,
        "duration_seconds": result.duration_seconds,
        "output_paths": result.output_paths,
        "summary": result.summary,
        "snapshot": golden_snapshot_to_dict(result.snapshot) if result.snapshot else None,
        "warnings": result.warnings,
        "errors": result.errors
    }

def regression_run_request_to_dict(request: RegressionRunRequest) -> dict:
    return {
        "request_id": request.request_id,
        "scope": request.scope.value,
        "dataset_name": request.dataset_name,
        "use_existing_golden": request.use_existing_golden,
        "update_baseline": request.update_baseline,
        "compare_snapshots": request.compare_snapshots,
        "write_outputs": request.write_outputs,
        "fail_on_snapshot_drift": request.fail_on_snapshot_drift,
        "max_allowed_warnings": request.max_allowed_warnings,
        "metadata": request.metadata
    }

def regression_run_result_to_dict(result: RegressionRunResult) -> dict:
    return {
        "run_id": result.run_id,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value,
        "request": regression_run_request_to_dict(result.request),
        "dataset_spec": golden_dataset_spec_to_dict(result.dataset_spec) if result.dataset_spec else None,
        "step_results": [regression_step_result_to_dict(s) for s in result.step_results],
        "snapshot_comparison": result.snapshot_comparison,
        "release_candidate_status": result.release_candidate_status.value,
        "manifest_path": result.manifest_path,
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors
    }

def release_rehearsal_result_to_dict(result: ReleaseRehearsalResult) -> dict:
    return {
        "rehearsal_id": result.rehearsal_id,
        "created_at_utc": result.created_at_utc,
        "scope": result.scope.value,
        "status": result.status.value,
        "regression_result": regression_run_result_to_dict(result.regression_result),
        "quality_acceptance_path": result.quality_acceptance_path,
        "passed_steps": result.passed_steps,
        "warning_steps": result.warning_steps,
        "failed_steps": result.failed_steps,
        "blocked_steps": result.blocked_steps,
        "required_actions": result.required_actions,
        "optional_actions": result.optional_actions,
        "warnings": result.warnings,
        "errors": result.errors,
        "output_paths": result.output_paths
    }

def validate_golden_dataset_spec(spec: GoldenDatasetSpec) -> None:
    if not spec.symbols:
        raise ValueError("symbols cannot be empty")
    if not spec.timeframe:
        raise ValueError("timeframe cannot be empty")
    if spec.row_count_per_symbol <= 0:
        raise ValueError("row_count_per_symbol must be positive")

def validate_golden_snapshot(snapshot: GoldenSnapshot) -> None:
    if not snapshot.checksum:
        raise ValueError("checksum cannot be empty")

def validate_regression_step_result(result: RegressionStepResult) -> None:
    if result.duration_seconds is not None and result.duration_seconds < 0:
        raise ValueError("duration_seconds cannot be negative")

def validate_regression_run_request(request: RegressionRunRequest) -> None:
    if request.max_allowed_warnings < 0:
        raise ValueError("max_allowed_warnings cannot be negative")
    if request.update_baseline:
        pass # Note: Requires documentation warning per constraints

def validate_regression_run_result(result: RegressionRunResult) -> None:
    if result.status == RegressionRunStatus.COMPLETED and result.release_candidate_status == ReleaseCandidateStatus.PASSED:
        if "live execution" in " ".join(result.warnings).lower() or "investment advice" in " ".join(result.warnings).lower():
           pass # Handled by upper validation

def create_golden_dataset_id(prefix: str = "golden_ds") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_golden_snapshot_id(name: str) -> str:
    return f"snap_{name}_{uuid.uuid4().hex[:8]}"

def create_regression_request_id(prefix: str = "reg_req") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_regression_run_id(prefix: str = "regression") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}_{uuid.uuid4().hex[:6]}"

def create_release_rehearsal_id(prefix: str = "release_rehearsal") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}_{uuid.uuid4().hex[:6]}"
