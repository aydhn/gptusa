from typing import Any

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
