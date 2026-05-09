import uuid
import datetime
from dataclasses import dataclass, field
from typing import Any
from usa_signal_bot.core.enums import (
    RetentionArtifactType,
    RetentionPolicyAction,
    CleanupCandidateStatus,
    CleanupRunStatus,
    DiskQuotaStatus,
    CleanupSafetyStatus,
    RetentionReportType,
)

@dataclass
class RetentionPolicy:
    policy_id: str
    artifact_type: RetentionArtifactType
    name: str
    enabled: bool
    keep_latest: int
    action: RetentionPolicyAction
    max_age_days: int | None = None
    max_total_size_mb: float | None = None
    protected: bool = False
    description: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class CleanupCandidate:
    candidate_id: str
    artifact_type: RetentionArtifactType
    path: str
    size_bytes: int
    recommended_action: RetentionPolicyAction
    status: CleanupCandidateStatus
    reason: str
    age_days: float | None = None
    last_modified_utc: str | None = None
    policy_id: str | None = None
    checksum: str | None = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass
class CleanupPlan:
    plan_id: str
    created_at_utc: str
    dry_run: bool
    candidates: list[CleanupCandidate]
    total_candidate_count: int
    total_candidate_size_bytes: int
    protected_count: int
    delete_candidate_count: int
    review_required_count: int
    warnings: list[str]
    errors: list[str]

@dataclass
class CleanupExecutionResult:
    execution_id: str
    created_at_utc: str
    status: CleanupRunStatus
    dry_run: bool
    plan: CleanupPlan
    deleted_paths: list[str]
    skipped_paths: list[str]
    failed_paths: list[str]
    bytes_freed: int
    warnings: list[str]
    errors: list[str]

@dataclass
class DiskQuotaConfig:
    enabled: bool
    warning_usage_pct: float
    critical_usage_pct: float
    data_root_quota_mb: float | None = None
    minimum_free_mb: float | None = None
    block_cleanup_if_unsafe: bool = True
    write_quota_reports: bool = True

@dataclass
class DiskQuotaReport:
    report_id: str
    created_at_utc: str
    status: DiskQuotaStatus
    data_root: str
    used_mb: float
    recommended_cleanup_bytes: int
    top_paths: list[dict[str, Any]]
    warnings: list[str]
    errors: list[str]
    quota_mb: float | None = None
    free_mb: float | None = None
    usage_pct: float | None = None

@dataclass
class RetentionReviewResult:
    review_id: str
    created_at_utc: str
    report_type: RetentionReportType
    policies: list[RetentionPolicy]
    safety_status: CleanupSafetyStatus
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]
    cleanup_plan: CleanupPlan | None = None
    quota_report: DiskQuotaReport | None = None

def create_retention_policy_id(name: str) -> str:
    return f"policy_{uuid.uuid4().hex[:8]}"

def create_cleanup_candidate_id(path: str) -> str:
    return f"cand_{uuid.uuid4().hex[:8]}"

def create_cleanup_plan_id(prefix: str = "cleanup_plan") -> str:
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}_{uuid.uuid4().hex[:4]}"

def create_cleanup_execution_id(prefix: str = "cleanup_exec") -> str:
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}_{uuid.uuid4().hex[:4]}"

def create_disk_quota_report_id(prefix: str = "quota") -> str:
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}_{uuid.uuid4().hex[:4]}"

def create_retention_review_id(prefix: str = "retention_review") -> str:
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}_{uuid.uuid4().hex[:4]}"

def validate_retention_policy(policy: RetentionPolicy) -> None:
    if policy.keep_latest < 0:
        raise ValueError("keep_latest cannot be negative")
    if policy.max_age_days is not None and policy.max_age_days < 0:
        raise ValueError("max_age_days must be None or positive")
    if policy.max_total_size_mb is not None and policy.max_total_size_mb < 0:
        raise ValueError("max_total_size_mb must be None or positive")
    if policy.protected and policy.action == RetentionPolicyAction.DELETE:
        raise ValueError("protected policy cannot have DELETE action")

def validate_cleanup_candidate(candidate: CleanupCandidate) -> None:
    pass

def validate_cleanup_plan(plan: CleanupPlan) -> None:
    pass

def validate_disk_quota_config(config: DiskQuotaConfig) -> None:
    if not (0 <= config.warning_usage_pct <= 100):
        raise ValueError("warning_usage_pct must be between 0 and 100")
    if not (0 <= config.critical_usage_pct <= 100):
        raise ValueError("critical_usage_pct must be between 0 and 100")
    if config.warning_usage_pct >= config.critical_usage_pct:
        raise ValueError("warning_usage_pct must be less than critical_usage_pct")

def retention_policy_to_dict(policy: RetentionPolicy) -> dict:
    import dataclasses
    d = dataclasses.asdict(policy)
    d["artifact_type"] = policy.artifact_type.value
    d["action"] = policy.action.value
    return d

def cleanup_candidate_to_dict(candidate: CleanupCandidate) -> dict:
    import dataclasses
    d = dataclasses.asdict(candidate)
    d["artifact_type"] = candidate.artifact_type.value
    d["recommended_action"] = candidate.recommended_action.value
    d["status"] = candidate.status.value
    return d

def cleanup_plan_to_dict(plan: CleanupPlan) -> dict:
    import dataclasses
    d = dataclasses.asdict(plan)
    d["candidates"] = [cleanup_candidate_to_dict(c) for c in plan.candidates]
    return d

def cleanup_execution_result_to_dict(result: CleanupExecutionResult) -> dict:
    import dataclasses
    d = dataclasses.asdict(result)
    d["status"] = result.status.value
    d["plan"] = cleanup_plan_to_dict(result.plan)
    return d

def disk_quota_config_to_dict(config: DiskQuotaConfig) -> dict:
    import dataclasses
    return dataclasses.asdict(config)

def disk_quota_report_to_dict(report: DiskQuotaReport) -> dict:
    import dataclasses
    d = dataclasses.asdict(report)
    d["status"] = report.status.value
    return d

def retention_review_result_to_dict(result: RetentionReviewResult) -> dict:
    import dataclasses
    d = dataclasses.asdict(result)
    d["report_type"] = result.report_type.value
    d["safety_status"] = result.safety_status.value
    d["policies"] = [retention_policy_to_dict(p) for p in result.policies]
    if result.cleanup_plan:
        d["cleanup_plan"] = cleanup_plan_to_dict(result.cleanup_plan)
    if result.quota_report:
        d["quota_report"] = disk_quota_report_to_dict(result.quota_report)
    return d
