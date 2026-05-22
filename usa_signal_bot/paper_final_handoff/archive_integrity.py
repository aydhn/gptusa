from typing import List
from usa_signal_bot.paper_final_handoff.final_handoff_models import (
    SealedReadinessArchiveManifest,
    ArchiveIntegrityReport,
    create_archive_integrity_report_id,
    _ts
)
from usa_signal_bot.core.enums import ArchiveIntegrityStatus, FinalHandoffRiskFlag
from usa_signal_bot.paper_final_handoff.archive_sealing import verify_archive_seal

def validate_archive_artifact_refs(manifest: SealedReadinessArchiveManifest) -> List[str]:
    # In real implementation, checks if files exist
    return manifest.artifact_refs

def detect_archive_missing_artifacts(manifest: SealedReadinessArchiveManifest) -> List[str]:
    # Mock implementation
    return []

def detect_archive_stale_artifacts(manifest: SealedReadinessArchiveManifest) -> List[str]:
    # Mock implementation
    return []

def build_archive_integrity_report(manifest: SealedReadinessArchiveManifest) -> ArchiveIntegrityReport:
    missing = detect_archive_missing_artifacts(manifest)
    stale = detect_archive_stale_artifacts(manifest)
    is_valid = verify_archive_seal(manifest)

    status = ArchiveIntegrityStatus.PASS
    risk_flags = []

    if not is_valid:
        status = ArchiveIntegrityStatus.FAIL
        risk_flags.append(FinalHandoffRiskFlag.ARCHIVE_INTEGRITY_FAILED)
    elif missing or stale:
        status = ArchiveIntegrityStatus.WARNING
        if missing: risk_flags.append(FinalHandoffRiskFlag.EVIDENCE_MISSING)
        if stale: risk_flags.append(FinalHandoffRiskFlag.EVIDENCE_STALE)

    return ArchiveIntegrityReport(
        integrity_report_id=create_archive_integrity_report_id(),
        created_at_utc=_ts(),
        archive_id=manifest.archive_id,
        status=status,
        expected_hash=manifest.archive_hash,
        observed_hash=manifest.archive_hash if is_valid else "mismatch",
        checked_artifact_count=len(manifest.artifact_refs),
        missing_artifact_count=len(missing),
        stale_artifact_count=len(stale),
        risk_flags=risk_flags,
        warnings=[],
        errors=[]
    )

def archive_integrity_risk_flags(report: ArchiveIntegrityReport) -> List[FinalHandoffRiskFlag]:
    return report.risk_flags

def archive_integrity_report_to_text(report: ArchiveIntegrityReport) -> str:
    return f"ArchiveIntegrity: {report.status.value} (Missing: {report.missing_artifact_count}, Stale: {report.stale_artifact_count})"
