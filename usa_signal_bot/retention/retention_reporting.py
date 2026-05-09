import json
from pathlib import Path
from typing import Any
from usa_signal_bot.retention.retention_models import (
    RetentionPolicy, CleanupCandidate, CleanupPlan, CleanupExecutionResult,
    DiskQuotaReport, RetentionReviewResult
)
from usa_signal_bot.retention.retention_validation import RetentionValidationReport

def retention_policy_to_text(policy: RetentionPolicy) -> str:
    return f"[{policy.artifact_type.value}] {policy.name}: Action={policy.action.value}, Keep={policy.keep_latest}"

def retention_policies_report_to_text(policies: list[RetentionPolicy]) -> str:
    return "\n".join(retention_policy_to_text(p) for p in policies)

def cleanup_candidate_to_text(candidate: CleanupCandidate) -> str:
    return f"{candidate.status.value}: {candidate.path} ({candidate.size_bytes} bytes) - {candidate.reason}"

def cleanup_plan_to_text(plan: CleanupPlan, limit: int = 50) -> str:
    lines = [
        f"Cleanup Plan: {plan.plan_id}",
        f"Dry Run: {plan.dry_run}",
        f"Total Candidates: {plan.total_candidate_count}",
        f"Delete Candidates: {plan.delete_candidate_count}",
        f"Review Required: {plan.review_required_count}",
        f"Protected: {plan.protected_count}",
        f"Total Size to Free: {plan.total_candidate_size_bytes / (1024*1024):.2f} MB",
        "",
        "Candidates (Top):"
    ]
    for c in plan.candidates[:limit]:
        lines.append(f"  - {cleanup_candidate_to_text(c)}")
    return "\n".join(lines)

def cleanup_execution_result_to_text(result: CleanupExecutionResult, limit: int = 50) -> str:
    lines = [
        f"Cleanup Execution: {result.execution_id}",
        f"Status: {result.status.value}",
        f"Dry Run: {result.dry_run}",
        f"Bytes Freed: {result.bytes_freed / (1024*1024):.2f} MB",
        f"Deleted: {len(result.deleted_paths)}, Skipped: {len(result.skipped_paths)}, Failed: {len(result.failed_paths)}"
    ]
    return "\n".join(lines)

def disk_quota_report_to_text(report: DiskQuotaReport) -> str:
    from usa_signal_bot.retention.disk_quota_guard import disk_quota_report_to_text as dqrt
    return dqrt(report)

def retention_review_result_to_text(result: RetentionReviewResult, limit: int = 50) -> str:
    lines = [
        f"Retention Review: {result.review_id}",
        f"Safety Status: {result.safety_status.value}",
        "",
        "--- Policies ---",
        retention_policies_report_to_text(result.policies),
        ""
    ]
    if result.quota_report:
        lines.extend(["--- Quota ---", disk_quota_report_to_text(result.quota_report), ""])
    if result.cleanup_plan:
        lines.extend(["--- Plan ---", cleanup_plan_to_text(result.cleanup_plan, limit), ""])

    lines.extend([
        "--- Limitations ---",
        retention_limitations_text()
    ])
    return "\n".join(lines)

def retention_store_summary_to_text(summary: dict[str, Any]) -> str:
    return json.dumps(summary, indent=2)

def retention_limitations_text() -> str:
    return "Disclaimer: Local cleanup only. No broker API calls or live/demo orders are generated. Not investment advice. Dry-run recommended."

def write_retention_report_json(path: Path, result: RetentionReviewResult, validation_report: RetentionValidationReport | None = None) -> Path:
    from usa_signal_bot.retention.retention_store import write_retention_review_result_json
    return write_retention_review_result_json(path, result)
