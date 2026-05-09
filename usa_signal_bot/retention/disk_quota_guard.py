import datetime
import shutil
from pathlib import Path
from typing import Any
from usa_signal_bot.core.enums import DiskQuotaStatus
from usa_signal_bot.retention.retention_models import (
    DiskQuotaConfig, DiskQuotaReport, CleanupCandidate, create_disk_quota_report_id
)

def default_disk_quota_config() -> DiskQuotaConfig:
    return DiskQuotaConfig(
        enabled=True,
        warning_usage_pct=80.0,
        critical_usage_pct=90.0
    )

class DiskQuotaGuard:
    def __init__(self, data_root: Path, config: DiskQuotaConfig | None = None):
        self.data_root = data_root
        self.config = config if config is not None else default_disk_quota_config()

    def build_quota_report(self) -> DiskQuotaReport:
        from usa_signal_bot.retention.artifact_classifier import artifact_size_bytes

        used_bytes = artifact_size_bytes(self.data_root)
        used_mb = used_bytes / (1024 * 1024)

        quota_mb = self.config.data_root_quota_mb
        free_mb = None
        usage_pct = None

        if quota_mb is not None:
             usage_pct = (used_mb / quota_mb) * 100 if quota_mb > 0 else 100
             free_mb = max(0, quota_mb - used_mb)
        else:
             try:
                 total, used, free = shutil.disk_usage(str(self.data_root))
                 quota_mb = total / (1024 * 1024)
                 free_mb = free / (1024 * 1024)
                 usage_pct = (used / total) * 100 if total > 0 else 100
             except OSError:
                 pass

        status = self.classify_quota_status(usage_pct, free_mb)

        report = DiskQuotaReport(
            report_id=create_disk_quota_report_id(),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            status=status,
            data_root=str(self.data_root),
            used_mb=used_mb,
            recommended_cleanup_bytes=0,
            top_paths=self.top_disk_usage_paths(),
            quota_mb=quota_mb,
            free_mb=free_mb,
            usage_pct=usage_pct,
            warnings=[],
            errors=[]
        )

        report.recommended_cleanup_bytes = self.estimate_required_cleanup_bytes(report)
        return report

    def estimate_required_cleanup_bytes(self, report: DiskQuotaReport) -> int:
        if report.status in (DiskQuotaStatus.OK, DiskQuotaStatus.UNKNOWN):
            return 0

        target_pct = self.config.warning_usage_pct - 5.0
        if report.quota_mb and report.usage_pct:
             if report.usage_pct > target_pct:
                  target_mb = report.quota_mb * (target_pct / 100)
                  return int(max(0, (report.used_mb - target_mb) * 1024 * 1024))
        return 0

    def recommend_cleanup_by_size(self, candidates: list[CleanupCandidate], target_bytes: int) -> list[CleanupCandidate]:
        from usa_signal_bot.core.enums import CleanupCandidateStatus

        valid = [c for c in candidates if c.status not in (CleanupCandidateStatus.PROTECTED, CleanupCandidateStatus.SKIPPED)]
        valid.sort(key=lambda c: c.size_bytes, reverse=True)

        recommended = []
        accumulated = 0
        for c in valid:
             if accumulated >= target_bytes:
                 break
             recommended.append(c)
             accumulated += c.size_bytes

        return recommended

    def classify_quota_status(self, usage_pct: float | None, free_mb: float | None = None) -> DiskQuotaStatus:
        if usage_pct is None:
            return DiskQuotaStatus.UNKNOWN

        if usage_pct >= self.config.critical_usage_pct:
            return DiskQuotaStatus.CRITICAL
        if usage_pct >= self.config.warning_usage_pct:
            return DiskQuotaStatus.WARNING

        if self.config.minimum_free_mb is not None and free_mb is not None:
             if free_mb < self.config.minimum_free_mb:
                  return DiskQuotaStatus.WARNING

        return DiskQuotaStatus.OK

    def top_disk_usage_paths(self, limit: int = 20) -> list[dict[str, Any]]:
        from usa_signal_bot.retention.artifact_classifier import discover_retention_artifacts, artifact_size_bytes
        artifacts = discover_retention_artifacts(self.data_root)

        sized = []
        for p in artifacts:
             try:
                 sized.append({"path": str(p), "size": artifact_size_bytes(p)})
             except Exception:
                 pass

        sized.sort(key=lambda x: x["size"], reverse=True)
        return sized[:limit]

def disk_quota_report_to_text(report: DiskQuotaReport) -> str:
    lines = [
        f"Status: {report.status.value}",
        f"Usage: {report.used_mb:.2f} MB / {report.quota_mb:.2f} MB ({report.usage_pct:.1f}%)",
        f"Recommended Cleanup: {report.recommended_cleanup_bytes / (1024*1024):.2f} MB"
    ]
    return "\n".join(lines)
