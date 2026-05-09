import datetime
from pathlib import Path
from typing import Any
from usa_signal_bot.core.enums import RetentionArtifactType, RetentionPolicyAction, CleanupCandidateStatus
from usa_signal_bot.retention.retention_models import (
    RetentionPolicy, CleanupCandidate, CleanupPlan,
    create_cleanup_candidate_id, create_cleanup_plan_id
)
from usa_signal_bot.retention.artifact_classifier import (
    discover_retention_artifacts, classify_retention_artifact,
    artifact_age_days, artifact_size_bytes, artifact_last_modified_utc, group_artifacts_by_type
)
from usa_signal_bot.retention.protected_paths import is_protected_path, explain_protected_path

class CleanupPlanner:
    def __init__(self, data_root: Path, project_root: Path | None = None, policies: list[RetentionPolicy] | None = None):
        from usa_signal_bot.retention.retention_policies import default_retention_policies
        self.data_root = data_root
        self.project_root = project_root
        self.policies = policies if policies is not None else default_retention_policies()

    def build_plan(self, dry_run: bool = True, artifact_types: list[RetentionArtifactType] | None = None) -> CleanupPlan:
        all_artifacts = discover_retention_artifacts(self.data_root)

        grouped = group_artifacts_by_type(all_artifacts, self.data_root)
        candidates = []

        types_to_process = artifact_types if artifact_types else list(RetentionArtifactType)

        for art_type in types_to_process:
            if art_type == RetentionArtifactType.UNKNOWN:
                continue

            paths = grouped.get(art_type, [])
            if not paths:
                continue

            paths.sort(key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)

            from usa_signal_bot.retention.retention_policies import policy_for_artifact_type
            policy = policy_for_artifact_type(self.policies, art_type)

            keep_set = self.apply_keep_latest(paths, policy) if policy else set(paths)

            for i, path in enumerate(paths):
                candidate = self.evaluate_artifact(path, art_type, policy, rank_index=i, keep_set=keep_set)
                if candidate:
                    candidates.append(candidate)

        protected_count = sum(1 for c in candidates if c.status == CleanupCandidateStatus.PROTECTED)
        delete_count = sum(1 for c in candidates if c.status == CleanupCandidateStatus.CANDIDATE)
        review_count = sum(1 for c in candidates if c.status == CleanupCandidateStatus.REVIEW_REQUIRED)
        total_size = sum(c.size_bytes for c in candidates if c.status == CleanupCandidateStatus.CANDIDATE)

        return CleanupPlan(
            plan_id=create_cleanup_plan_id(),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            dry_run=dry_run,
            candidates=candidates,
            total_candidate_count=len(candidates),
            total_candidate_size_bytes=total_size,
            protected_count=protected_count,
            delete_candidate_count=delete_count,
            review_required_count=review_count,
            warnings=[],
            errors=[]
        )

    def apply_keep_latest(self, paths: list[Path], policy: RetentionPolicy) -> set[Path]:
        if policy.keep_latest is None or policy.keep_latest < 0:
            return set(paths)
        return set(paths[:policy.keep_latest])

    def should_candidate_delete(self, path: Path, policy: RetentionPolicy, keep_set: set[Path]) -> tuple[bool, str]:
        if path in keep_set:
            return False, f"Kept by keep_latest ({policy.keep_latest})"

        age = artifact_age_days(path)
        if policy.max_age_days is not None and age is not None and age > policy.max_age_days:
            return True, f"Exceeds max_age_days ({policy.max_age_days})"

        return True, "Outside of keep_latest window"

    def evaluate_artifact(self, path: Path, artifact_type: RetentionArtifactType, policy: RetentionPolicy | None, rank_index: int | None = None, keep_set: set[Path] | None = None) -> CleanupCandidate | None:
        if not path.exists():
            return None

        size = artifact_size_bytes(path)
        age = artifact_age_days(path)
        mtime = artifact_last_modified_utc(path)

        status = CleanupCandidateStatus.SKIPPED
        action = RetentionPolicyAction.SKIP
        reason = "No policy applicable"

        if is_protected_path(path, self.project_root, self.data_root):
            status = CleanupCandidateStatus.PROTECTED
            action = RetentionPolicyAction.SKIP
            reason = explain_protected_path(path, self.project_root, self.data_root) or "Protected path"
        elif policy:
            action = policy.action
            should_del, del_reason = self.should_candidate_delete(path, policy, keep_set or set())

            if not should_del:
                status = CleanupCandidateStatus.SKIPPED
                reason = del_reason
            else:
                if action == RetentionPolicyAction.DELETE:
                    status = CleanupCandidateStatus.CANDIDATE
                    reason = del_reason
                elif action == RetentionPolicyAction.REVIEW:
                    status = CleanupCandidateStatus.REVIEW_REQUIRED
                    reason = del_reason
                else:
                    status = CleanupCandidateStatus.SKIPPED
                    reason = f"Action is {action.value}"

        return CleanupCandidate(
            candidate_id=create_cleanup_candidate_id(str(path)),
            artifact_type=artifact_type,
            path=str(path),
            size_bytes=size,
            age_days=age,
            last_modified_utc=mtime,
            policy_id=policy.policy_id if policy else None,
            recommended_action=action,
            status=status,
            reason=reason
        )

    def summarize_plan(self, plan: CleanupPlan) -> dict[str, Any]:
        return {
            "plan_id": plan.plan_id,
            "dry_run": plan.dry_run,
            "total_candidates": plan.total_candidate_count,
            "delete_count": plan.delete_candidate_count,
            "freed_bytes_estimated": plan.total_candidate_size_bytes,
            "review_required": plan.review_required_count,
            "protected": plan.protected_count
        }
