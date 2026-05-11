# The code review shows that my "fix_repo.py" overwritten files didn't include the ones I hadn't added to the python script array.
# I will fully restore them now correctly from the blocks I generated earlier.

import os

content_budget = """from typing import Any
import statistics

from usa_signal_bot.core.enums import ResourceProfileScope, CalibrationStatus, CalibrationDecision
from usa_signal_bot.profiling.profiling_models import ResourceProfile, BudgetCalibrationResult, create_budget_calibration_id
from usa_signal_bot.profiling.resource_timer import current_utc_iso

def calculate_profile_percentiles(values: list[float], percentiles: list[float] | None = None) -> dict[str, float]:
    if not values:
        return {}

    if percentiles is None:
        percentiles = [50.0, 75.0, 90.0, 95.0, 99.0]

    sorted_vals = sorted(values)
    n = len(sorted_vals)

    result = {}
    for p in percentiles:
        idx = int(p / 100.0 * (n - 1))
        result[f"p{int(p)}"] = sorted_vals[idx]

    return result

def confidence_from_sample_count(sample_count: int) -> float:
    if sample_count == 0:
        return 0.0
    if sample_count < 3:
        return 0.2
    if sample_count < 10:
        return 0.5
    if sample_count < 30:
        return 0.8
    return 0.95

def decide_calibration_action(current_budget: dict[str, Any], recommended_budget: dict[str, Any], sample_count: int) -> CalibrationDecision:
    if sample_count < 3:
        return CalibrationDecision.REVIEW_REQUIRED

    curr_time = current_budget.get("wall_time_seconds", 0)
    rec_time = recommended_budget.get("wall_time_seconds", 0)

    if rec_time > curr_time * 1.5:
        return CalibrationDecision.SPLIT_TASK
    elif rec_time > curr_time:
        return CalibrationDecision.RAISE_BUDGET
    elif rec_time < curr_time * 0.5:
        return CalibrationDecision.LOWER_BUDGET

    return CalibrationDecision.KEEP_CURRENT

def recommend_budget_from_profiles(profiles: list[ResourceProfile], current_budget: dict[str, Any]) -> dict[str, Any]:
    wall_times = [p.wall_time_seconds for p in profiles if p.wall_time_seconds is not None]
    mem_peaks = [p.memory_peak_bytes for p in profiles if p.memory_peak_bytes is not None]

    rec_budget = dict(current_budget)

    if len(wall_times) >= 3:
        p90_time = calculate_profile_percentiles(wall_times, [90.0]).get("p90", 0)
        rec_budget["wall_time_seconds"] = p90_time * 1.2

    if len(mem_peaks) >= 3:
        p90_mem = calculate_profile_percentiles(mem_peaks, [90.0]).get("p90", 0)
        rec_budget["memory_peak_bytes"] = p90_mem * 1.2

    return rec_budget

def calibrate_budget_for_scope(scope: ResourceProfileScope, profiles: list[ResourceProfile], current_budget: dict[str, Any]) -> BudgetCalibrationResult:
    scope_profiles = [p for p in profiles if p.scope == scope]
    sample_count = len(scope_profiles)

    status = CalibrationStatus.INSUFFICIENT_DATA
    decision = CalibrationDecision.REVIEW_REQUIRED
    recommended = current_budget
    confidence = confidence_from_sample_count(sample_count)
    warnings = []

    if sample_count >= 3:
        status = CalibrationStatus.CALIBRATED
        recommended = recommend_budget_from_profiles(scope_profiles, current_budget)
        decision = decide_calibration_action(current_budget, recommended, sample_count)
    else:
        warnings.append(f"Not enough samples ({sample_count}) for scope {scope.value} to calibrate reliably.")

    return BudgetCalibrationResult(
        calibration_id=create_budget_calibration_id(),
        created_at_utc=current_utc_iso(),
        status=status,
        scope=scope,
        sample_count=sample_count,
        decision=decision,
        current_budget=current_budget,
        recommended_budget=recommended,
        confidence=confidence,
        evidence={"profiles_analyzed": sample_count},
        warnings=warnings,
        errors=[]
    )

def calibrate_all_budgets(profiles: list[ResourceProfile], current_budgets: dict[str, dict[str, Any]]) -> list[BudgetCalibrationResult]:
    results = []
    for scope_str, budget in current_budgets.items():
        try:
            scope = ResourceProfileScope(scope_str)
            result = calibrate_budget_for_scope(scope, profiles, budget)
            results.append(result)
        except ValueError:
            pass
    return results

def budget_calibration_result_to_text(result: BudgetCalibrationResult) -> str:
    lines = [
        f"Calibration for {result.scope.value} (Samples: {result.sample_count})",
        f"Status: {result.status.value}",
        f"Decision: {result.decision.value}",
        f"Confidence: {result.confidence:.2f}" if result.confidence is not None else "Confidence: N/A"
    ]
    return "\\n".join(lines)
"""

with open('usa_signal_bot/profiling/budget_calibration.py', 'w') as f:
    f.write(content_budget.replace('\\\\n', '\\n'))

content_collector = """import time
from pathlib import Path
from typing import Any

from usa_signal_bot.core.enums import ResourceProfileScope, ResourceProfileStatus, ResourceMetricName
from usa_signal_bot.profiling.profiling_models import ResourceProfile, ResourceMetric, create_resource_profile_id, create_resource_metric_id
from usa_signal_bot.profiling.resource_timer import current_utc_iso
from usa_signal_bot.profiling.artifact_growth import measure_artifact_footprint

class ResourceProfileCollector:
    def __init__(self, data_root: Path, project_root: Path | None = None):
        self.data_root = data_root
        self.project_root = project_root

    def profile_noop(self, scope: ResourceProfileScope = ResourceProfileScope.CUSTOM) -> ResourceProfile:
        started = current_utc_iso()

        time.sleep(0.001)

        return ResourceProfile(
            profile_id=create_resource_profile_id(),
            scope=scope,
            target_name="noop",
            status=ResourceProfileStatus.COMPLETED,
            started_at_utc=started,
            completed_at_utc=current_utc_iso(),
            wall_time_seconds=0.001,
            process_time_seconds=0.001,
            memory_current_bytes=None,
            memory_peak_bytes=None,
            artifact_size_bytes=0,
            artifact_file_count=0,
            output_growth_bytes=0,
            output_growth_files=0,
            metrics=[],
            warnings=[],
            errors=[],
            metadata={"collector": "ResourceProfileCollector"}
        )

    def profile_artifact_path(self, path: Path, scope: ResourceProfileScope, target_name: str) -> ResourceProfile:
        started = current_utc_iso()
        footprint = measure_artifact_footprint(path)
        completed = current_utc_iso()

        metrics = []
        if footprint.exists:
            metrics.append(ResourceMetric(
                metric_id=create_resource_metric_id(),
                name=ResourceMetricName.ARTIFACT_SIZE_BYTES,
                value=footprint.size_bytes,
                unit="bytes",
                status=ResourceProfileStatus.COMPLETED,
                source="profile_artifact_path",
                created_at_utc=completed
            ))

            metrics.append(ResourceMetric(
                metric_id=create_resource_metric_id(),
                name=ResourceMetricName.ARTIFACT_FILE_COUNT,
                value=footprint.file_count,
                unit="files",
                status=ResourceProfileStatus.COMPLETED,
                source="profile_artifact_path",
                created_at_utc=completed
            ))

        return ResourceProfile(
            profile_id=create_resource_profile_id(),
            scope=scope,
            target_name=target_name,
            status=ResourceProfileStatus.COMPLETED if footprint.exists else ResourceProfileStatus.WARNING,
            started_at_utc=started,
            completed_at_utc=completed,
            wall_time_seconds=0.0,
            process_time_seconds=0.0,
            memory_current_bytes=None,
            memory_peak_bytes=None,
            artifact_size_bytes=footprint.size_bytes if footprint.exists else None,
            artifact_file_count=footprint.file_count if footprint.exists else None,
            output_growth_bytes=None,
            output_growth_files=None,
            metrics=metrics,
            warnings=footprint.warnings,
            errors=footprint.errors,
            metadata={"path": footprint.path}
        )

    def profile_existing_run_artifacts(self, scope: ResourceProfileScope | None = None) -> list[ResourceProfile]:
        return []

    def profile_task_simulation(self, task: Any) -> ResourceProfile:
        return self.profile_noop(ResourceProfileScope.TASK)

    def profile_command_dry_run(self, command_name: str) -> ResourceProfile:
        profile = self.profile_noop(ResourceProfileScope.COMMAND)
        profile.target_name = command_name
        profile.warnings.append("Dry-run execution - true resource bounds are estimates.")
        return profile

    def collect_lightweight_snapshot(self) -> list[ResourceProfile]:
        profiles = []
        profiles.append(self.profile_noop(ResourceProfileScope.OBSERVABILITY))

        if self.data_root.exists():
            profiles.append(self.profile_artifact_path(self.data_root, ResourceProfileScope.OBSERVABILITY, "data_root"))

        return profiles
"""

with open('usa_signal_bot/profiling/resource_profile_collector.py', 'w') as f:
    f.write(content_collector)


content_loader = """import json
from pathlib import Path
from typing import Any

from usa_signal_bot.core.enums import ResourceProfileScope, ResourceMetricName, ResourceProfileStatus
from usa_signal_bot.profiling.profiling_models import ResourceProfile, ResourceMetric
from usa_signal_bot.profiling.profiling_store import resource_profiles_dir, read_resource_profile_json

def load_profiles_from_store(data_root: Path, scope: ResourceProfileScope | None = None, limit: int | None = None) -> list[ResourceProfile]:
    profiles_dir = resource_profiles_dir(data_root)
    if not profiles_dir.exists():
        return []

    profiles = []
    for profile_path in profiles_dir.glob("*.json"):
        try:
            profile_dict = read_resource_profile_json(profile_path)

            metrics = []
            for m in profile_dict.get("metrics", []):
                metrics.append(ResourceMetric(
                    metric_id=m["metric_id"],
                    name=ResourceMetricName(m["name"]),
                    value=m["value"],
                    unit=m["unit"],
                    status=ResourceProfileStatus(m["status"]),
                    source=m["source"],
                    created_at_utc=m["created_at_utc"],
                    metadata=m.get("metadata", {})
                ))

            profile = ResourceProfile(
                profile_id=profile_dict["profile_id"],
                scope=ResourceProfileScope(profile_dict["scope"]),
                target_name=profile_dict["target_name"],
                status=ResourceProfileStatus(profile_dict["status"]),
                started_at_utc=profile_dict.get("started_at_utc"),
                completed_at_utc=profile_dict.get("completed_at_utc"),
                wall_time_seconds=profile_dict.get("wall_time_seconds"),
                process_time_seconds=profile_dict.get("process_time_seconds"),
                memory_current_bytes=profile_dict.get("memory_current_bytes"),
                memory_peak_bytes=profile_dict.get("memory_peak_bytes"),
                artifact_size_bytes=profile_dict.get("artifact_size_bytes"),
                artifact_file_count=profile_dict.get("artifact_file_count"),
                output_growth_bytes=profile_dict.get("output_growth_bytes"),
                output_growth_files=profile_dict.get("output_growth_files"),
                metrics=metrics,
                warnings=profile_dict.get("warnings", []),
                errors=profile_dict.get("errors", []),
                metadata=profile_dict.get("metadata", {})
            )

            if scope is None or profile.scope == scope:
                profiles.append(profile)
        except Exception:
            pass

    profiles.sort(key=lambda p: p.started_at_utc or "", reverse=True)
    if limit is not None:
        profiles = profiles[:limit]

    return profiles

def load_runtime_duration_metrics(data_root: Path) -> list[dict[str, Any]]:
    return []

def load_taskqueue_run_metrics(data_root: Path) -> list[dict[str, Any]]:
    return []

def load_scheduler_run_metrics(data_root: Path) -> list[dict[str, Any]]:
    return []

def load_observability_metrics(data_root: Path) -> list[dict[str, Any]]:
    return []

def extract_duration_values(records: list[dict[str, Any]]) -> list[float]:
    values = []
    for r in records:
        val = r.get("duration_seconds")
        if isinstance(val, (int, float)):
            values.append(float(val))
    return values

def extract_artifact_growth_values(records: list[dict[str, Any]]) -> list[int]:
    values = []
    for r in records:
        val = r.get("output_growth_bytes")
        if isinstance(val, int):
            values.append(val)
    return values

def summarize_historical_metrics(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(records),
        "has_records": len(records) > 0
    }
"""

with open('usa_signal_bot/profiling/run_metrics_loader.py', 'w') as f:
    f.write(content_loader)

content_task_adapter = """from typing import Any

from usa_signal_bot.profiling.profiling_models import (
    ResourceProfile,
    BudgetCalibrationResult,
    ThrottlingRecommendation,
    ThrottlingPlan
)
from usa_signal_bot.core.enums import ThrottlingAction

def adjusted_workload_budget_from_calibration(base_budget: Any, calibration_results: list[BudgetCalibrationResult]) -> Any:
    return base_budget

def apply_throttling_to_local_task(task: Any, recommendations: list[ThrottlingRecommendation]) -> Any:
    task_id = getattr(task, 'task_id', None)
    applicable_recs = [r for r in recommendations if r.task_id == task_id or r.task_id is None]

    if not applicable_recs:
        return task

    for rec in applicable_recs:
        if rec.action == ThrottlingAction.DRY_RUN_ONLY:
            if hasattr(task, 'metadata'):
                task.metadata['throttling_hint'] = 'DRY_RUN_ONLY'

    return task

def taskqueue_budget_hints_from_profiles(profiles: list[ResourceProfile]) -> dict[str, Any]:
    hints = {}
    for p in profiles:
        hints[p.target_name] = {
            "wall_time": p.wall_time_seconds,
            "memory_peak": p.memory_peak_bytes
        }
    return hints

def taskqueue_plan_with_throttling_hints(plan: Any, throttling_plan: ThrottlingPlan) -> Any:
    if hasattr(plan, 'metadata'):
        plan.metadata['throttling_review_count'] = throttling_plan.review_count
        plan.metadata['throttling_warning_count'] = throttling_plan.warning_count

    return plan

def taskqueue_adapter_summary_to_text(summary: dict[str, Any]) -> str:
    lines = ["TaskQueue Adapter Summary:"]
    for k, v in summary.items():
        lines.append(f"  {k}: {v}")
    return "\\n".join(lines)
"""

with open('usa_signal_bot/profiling/taskqueue_adapter.py', 'w') as f:
    f.write(content_task_adapter.replace('\\\\n', '\\n'))

content_scheduler_adapter = """from typing import Any

from usa_signal_bot.core.enums import ResourceProfileScope, ThrottlingAction
from usa_signal_bot.profiling.profiling_models import ThrottlingPlan

def scheduler_hints_from_throttling_plan(plan: ThrottlingPlan) -> dict[str, Any]:
    hints = {
        "delay_scopes": [],
        "dry_run_scopes": [],
        "review_scopes": []
    }

    for rec in plan.recommendations:
        scope_val = rec.scope.value
        if rec.action == ThrottlingAction.DELAY and scope_val not in hints["delay_scopes"]:
            hints["delay_scopes"].append(scope_val)
        elif rec.action == ThrottlingAction.DRY_RUN_ONLY and scope_val not in hints["dry_run_scopes"]:
            hints["dry_run_scopes"].append(scope_val)
        elif rec.action == ThrottlingAction.REVIEW and scope_val not in hints["review_scopes"]:
            hints["review_scopes"].append(scope_val)

    return hints

def annotate_scheduler_plan_with_resource_hints(plan: Any, throttling_plan: ThrottlingPlan) -> Any:
    hints = scheduler_hints_from_throttling_plan(throttling_plan)
    if hasattr(plan, 'metadata'):
        plan.metadata['throttling_hints'] = hints
    return plan

def should_scheduler_delay_scope(scope: ResourceProfileScope, throttling_plan: ThrottlingPlan) -> bool:
    for rec in throttling_plan.recommendations:
        if rec.scope == scope and rec.action in [ThrottlingAction.DELAY, ThrottlingAction.BLOCK]:
            return True
    return False

def scheduler_adapter_summary_to_text(summary: dict[str, Any]) -> str:
    lines = ["Scheduler Adapter Summary:"]
    for k, v in summary.items():
        if isinstance(v, list):
            lines.append(f"  {k}: {', '.join(v) if v else 'None'}")
        else:
            lines.append(f"  {k}: {v}")
    return "\\n".join(lines)
"""

with open('usa_signal_bot/profiling/scheduler_adapter.py', 'w') as f:
    f.write(content_scheduler_adapter.replace('\\\\n', '\\n'))

content_policy = """from dataclasses import dataclass, field
from typing import Any
import uuid

from usa_signal_bot.core.enums import ResourceProfileScope, ThrottlingAction
from usa_signal_bot.core.exceptions import ThrottlingPolicyError

@dataclass
class ThrottlingPolicy:
    policy_id: str
    scope: ResourceProfileScope
    enabled: bool
    max_wall_time_seconds: float | None
    max_memory_peak_mb: float | None
    max_output_growth_mb: float | None
    max_file_growth_count: int | None
    action_on_warning: ThrottlingAction
    action_on_critical: ThrottlingAction
    description: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

def default_throttling_policies() -> list[ThrottlingPolicy]:
    policies = []

    policies.append(ThrottlingPolicy(
        policy_id=f"policy_{uuid.uuid4().hex[:8]}",
        scope=ResourceProfileScope.SCAN,
        enabled=True,
        max_wall_time_seconds=1800.0,
        max_memory_peak_mb=4096.0,
        max_output_growth_mb=512.0,
        max_file_growth_count=5000,
        action_on_warning=ThrottlingAction.WARN,
        action_on_critical=ThrottlingAction.REDUCE_SCOPE,
        description="Default policy for SCAN operations"
    ))

    policies.append(ThrottlingPolicy(
        policy_id=f"policy_{uuid.uuid4().hex[:8]}",
        scope=ResourceProfileScope.BACKTEST,
        enabled=True,
        max_wall_time_seconds=7200.0,
        max_memory_peak_mb=6144.0,
        max_output_growth_mb=1024.0,
        max_file_growth_count=10000,
        action_on_warning=ThrottlingAction.WARN,
        action_on_critical=ThrottlingAction.SPLIT,
        description="Default policy for BACKTEST operations"
    ))

    policies.append(ThrottlingPolicy(
        policy_id=f"policy_{uuid.uuid4().hex[:8]}",
        scope=ResourceProfileScope.REGRESSION,
        enabled=True,
        max_wall_time_seconds=3600.0,
        max_memory_peak_mb=4096.0,
        max_output_growth_mb=512.0,
        max_file_growth_count=5000,
        action_on_warning=ThrottlingAction.WARN,
        action_on_critical=ThrottlingAction.DELAY,
        description="Default policy for REGRESSION operations"
    ))

    policies.append(ThrottlingPolicy(
        policy_id=f"policy_{uuid.uuid4().hex[:8]}",
        scope=ResourceProfileScope.RETENTION,
        enabled=True,
        max_wall_time_seconds=600.0,
        max_memory_peak_mb=1024.0,
        max_output_growth_mb=10.0,
        max_file_growth_count=100,
        action_on_warning=ThrottlingAction.WARN,
        action_on_critical=ThrottlingAction.DRY_RUN_ONLY,
        description="Default policy for RETENTION operations"
    ))

    return policies

def policy_for_profile_scope(scope: ResourceProfileScope, policies: list[ThrottlingPolicy] | None = None) -> ThrottlingPolicy:
    if policies is None:
        policies = default_throttling_policies()

    for p in policies:
        if p.scope == scope:
            return p

    return ThrottlingPolicy(
        policy_id=f"policy_fallback_{uuid.uuid4().hex[:8]}",
        scope=scope,
        enabled=True,
        max_wall_time_seconds=300.0,
        max_memory_peak_mb=1024.0,
        max_output_growth_mb=100.0,
        max_file_growth_count=1000,
        action_on_warning=ThrottlingAction.WARN,
        action_on_critical=ThrottlingAction.REVIEW,
        description="Fallback policy"
    )

def load_throttling_policies_from_config(config_dict: dict[str, Any] | None = None) -> list[ThrottlingPolicy]:
    return default_throttling_policies()

def throttling_policy_to_dict(policy: ThrottlingPolicy) -> dict:
    return {
        "policy_id": policy.policy_id,
        "scope": policy.scope.value,
        "enabled": policy.enabled,
        "max_wall_time_seconds": policy.max_wall_time_seconds,
        "max_memory_peak_mb": policy.max_memory_peak_mb,
        "max_output_growth_mb": policy.max_output_growth_mb,
        "max_file_growth_count": policy.max_file_growth_count,
        "action_on_warning": policy.action_on_warning.value,
        "action_on_critical": policy.action_on_critical.value,
        "description": policy.description,
        "metadata": policy.metadata
    }

def validate_throttling_policy(policy: ThrottlingPolicy) -> None:
    if policy.max_wall_time_seconds is not None and policy.max_wall_time_seconds < 0:
        raise ThrottlingPolicyError("max_wall_time_seconds cannot be negative")
    if policy.max_memory_peak_mb is not None and policy.max_memory_peak_mb < 0:
        raise ThrottlingPolicyError("max_memory_peak_mb cannot be negative")
    if policy.max_output_growth_mb is not None and policy.max_output_growth_mb < 0:
        raise ThrottlingPolicyError("max_output_growth_mb cannot be negative")
    if policy.max_file_growth_count is not None and policy.max_file_growth_count < 0:
        raise ThrottlingPolicyError("max_file_growth_count cannot be negative")

def throttling_policies_to_text(policies: list[ThrottlingPolicy]) -> str:
    lines = []
    for p in policies:
        lines.append(f"Policy: {p.scope.value} (Enabled: {p.enabled})")
        lines.append(f"  Max Wall Time: {p.max_wall_time_seconds}s")
        lines.append(f"  Max Memory Peak: {p.max_memory_peak_mb}MB")
        lines.append(f"  Critical Action: {p.action_on_critical.value}")
    return "\\n".join(lines)
"""

with open('usa_signal_bot/profiling/throttling_policy.py', 'w') as f:
    f.write(content_policy.replace('\\\\n', '\\n'))

content_engine = """from typing import Any

from usa_signal_bot.core.enums import ThrottlingAction, ThrottlingSeverity, ThrottlingReason, ResourceProfileStatus, ResourceProfileScope
from usa_signal_bot.profiling.profiling_models import (
    ResourceProfile,
    ThrottlingRecommendation,
    ThrottlingPlan,
    BudgetCalibrationResult,
    create_throttling_recommendation_id,
    create_throttling_plan_id
)
from usa_signal_bot.profiling.throttling_policy import ThrottlingPolicy, default_throttling_policies, policy_for_profile_scope
from usa_signal_bot.profiling.resource_timer import current_utc_iso

class AdaptiveThrottlingEngine:
    def __init__(self, policies: list[ThrottlingPolicy] | None = None):
        self.policies = policies if policies is not None else default_throttling_policies()

    def classify_profile_severity(self, profile: ResourceProfile, policy: ThrottlingPolicy) -> ThrottlingSeverity:
        if not policy.enabled:
            return ThrottlingSeverity.NONE

        severity = ThrottlingSeverity.NONE

        if profile.wall_time_seconds is not None and policy.max_wall_time_seconds is not None:
            if profile.wall_time_seconds > policy.max_wall_time_seconds:
                severity = ThrottlingSeverity.CRITICAL
            elif profile.wall_time_seconds > policy.max_wall_time_seconds * 0.8:
                severity = max(severity, ThrottlingSeverity.HIGH)

        if profile.memory_peak_bytes is not None and policy.max_memory_peak_mb is not None:
            peak_mb = profile.memory_peak_bytes / (1024 * 1024)
            if peak_mb > policy.max_memory_peak_mb:
                severity = ThrottlingSeverity.CRITICAL
            elif peak_mb > policy.max_memory_peak_mb * 0.8:
                severity = max(severity, ThrottlingSeverity.HIGH)

        if profile.output_growth_bytes is not None and policy.max_output_growth_mb is not None:
            growth_mb = profile.output_growth_bytes / (1024 * 1024)
            if growth_mb > policy.max_output_growth_mb:
                severity = ThrottlingSeverity.CRITICAL
            elif growth_mb > policy.max_output_growth_mb * 0.8:
                severity = max(severity, ThrottlingSeverity.HIGH)

        if profile.status == ResourceProfileStatus.INSUFFICIENT_DATA:
            if severity in [ThrottlingSeverity.NONE, ThrottlingSeverity.LOW]:
                severity = ThrottlingSeverity.MODERATE

        return severity

    def reasons_for_profile(self, profile: ResourceProfile, policy: ThrottlingPolicy) -> list[ThrottlingReason]:
        reasons = []
        if profile.status == ResourceProfileStatus.INSUFFICIENT_DATA:
            reasons.append(ThrottlingReason.INSUFFICIENT_PROFILE_DATA)

        if profile.wall_time_seconds is not None and policy.max_wall_time_seconds is not None:
            if profile.wall_time_seconds > policy.max_wall_time_seconds * 0.8:
                reasons.append(ThrottlingReason.TIME_BUDGET)

        if profile.memory_peak_bytes is not None and policy.max_memory_peak_mb is not None:
            peak_mb = profile.memory_peak_bytes / (1024 * 1024)
            if peak_mb > policy.max_memory_peak_mb * 0.8:
                reasons.append(ThrottlingReason.RAM_BUDGET)

        if profile.output_growth_bytes is not None and policy.max_output_growth_mb is not None:
            growth_mb = profile.output_growth_bytes / (1024 * 1024)
            if growth_mb > policy.max_output_growth_mb * 0.8:
                reasons.append(ThrottlingReason.HIGH_OUTPUT_GROWTH)

        return reasons

    def evaluate_profile(self, profile: ResourceProfile) -> list[ThrottlingRecommendation]:
        policy = policy_for_profile_scope(profile.scope, self.policies)
        severity = self.classify_profile_severity(profile, policy)

        if severity == ThrottlingSeverity.NONE and profile.status != ResourceProfileStatus.INSUFFICIENT_DATA:
            return []

        reasons = self.reasons_for_profile(profile, policy)
        action = ThrottlingAction.ALLOW
        msg = f"Profile {profile.target_name} shows {severity.value} resource pressure."

        if severity == ThrottlingSeverity.CRITICAL:
            action = policy.action_on_critical
            if action in [ThrottlingAction.BLOCK, ThrottlingAction.SKIP]:
                action = ThrottlingAction.REVIEW

        elif severity in [ThrottlingSeverity.HIGH, ThrottlingSeverity.MODERATE]:
            action = policy.action_on_warning

        if ThrottlingReason.HIGH_OUTPUT_GROWTH in reasons and action == ThrottlingAction.ALLOW:
            action = ThrottlingAction.DRY_RUN_ONLY

        if ThrottlingReason.INSUFFICIENT_PROFILE_DATA in reasons:
            action = ThrottlingAction.REVIEW
            msg = "Insufficient profile data, review recommended before heavy execution."

        rec = ThrottlingRecommendation(
            recommendation_id=create_throttling_recommendation_id(),
            task_id=profile.target_name,
            scope=profile.scope,
            action=action,
            severity=severity,
            reasons=reasons,
            message=msg,
            suggested_changes={},
            evidence={"profile_id": profile.profile_id}
        )
        return [rec]

    def evaluate_calibration_result(self, result: BudgetCalibrationResult) -> list[ThrottlingRecommendation]:
        recs = []
        if result.decision in [ThrottlingAction.SPLIT.value, ThrottlingAction.REDUCE_SCOPE.value, "SPLIT_TASK", "THROTTLE_TASK", "REVIEW_REQUIRED"]:
            action = ThrottlingAction.REVIEW
            if "SPLIT" in result.decision:
                action = ThrottlingAction.SPLIT

            recs.append(ThrottlingRecommendation(
                recommendation_id=create_throttling_recommendation_id(),
                task_id=None,
                scope=result.scope,
                action=action,
                severity=ThrottlingSeverity.MODERATE,
                reasons=[ThrottlingReason.HISTORICAL_SLOW_RUN],
                message=f"Calibration suggests {result.decision} for {result.scope.value}",
                suggested_changes={},
                evidence={"calibration_id": result.calibration_id}
            ))
        return recs

    def build_plan(self, profiles: list[ResourceProfile], calibration_results: list[BudgetCalibrationResult] | None = None) -> ThrottlingPlan:
        recs = []
        for p in profiles:
            recs.extend(self.evaluate_profile(p))

        if calibration_results:
            for c in calibration_results:
                recs.extend(self.evaluate_calibration_result(c))

        blocked_count = sum(1 for r in recs if r.action == ThrottlingAction.BLOCK)
        warning_count = sum(1 for r in recs if r.action == ThrottlingAction.WARN)
        review_count = sum(1 for r in recs if r.action == ThrottlingAction.REVIEW)

        return ThrottlingPlan(
            plan_id=create_throttling_plan_id(),
            created_at_utc=current_utc_iso(),
            status=ResourceProfileStatus.COMPLETED,
            recommendations=recs,
            blocked_count=blocked_count,
            warning_count=warning_count,
            review_count=review_count,
            output_paths={},
            warnings=[],
            errors=[]
        )
"""

with open('usa_signal_bot/profiling/throttling_engine.py', 'w') as f:
    f.write(content_engine.replace('\\\\n', '\\n'))
