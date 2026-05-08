from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Any
import uuid
import zipfile
from usa_signal_bot.core.enums import BackupScope, BackupStatus
from usa_signal_bot.release.artifact_collector import should_exclude_path

@dataclass
class BackupRequest:
    request_id: str
    scope: BackupScope
    output_dir: str
    include_data_cache: bool = False
    include_reports: bool = True
    include_configs: bool = True
    include_secrets: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BackupResult:
    backup_id: str
    created_at_utc: str
    status: BackupStatus
    request: BackupRequest
    backup_path: Optional[str]
    manifest_path: Optional[str]
    file_count: int
    total_size_bytes: int
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class RestoreDryRunResult:
    restore_id: str
    created_at_utc: str
    status: BackupStatus
    backup_path: str
    target_dir: str
    files_checked: int
    conflicts: List[str]
    missing_required_files: List[str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def create_backup_request(scope: BackupScope, output_dir: str) -> BackupRequest:
    return BackupRequest(
        request_id=f"req_{uuid.uuid4().hex[:8]}",
        scope=scope,
        output_dir=output_dir,
        include_secrets=False
    )

def build_backup(project_root: Path, data_root: Path, request: BackupRequest) -> BackupResult:
    if request.include_secrets:
        return BackupResult(
            backup_id="", created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=BackupStatus.FAILED, request=request, backup_path=None, manifest_path=None,
            file_count=0, total_size_bytes=0, errors=["include_secrets must be False"]
        )

    backup_id = f"backup_{uuid.uuid4().hex[:8]}"
    out_dir = Path(request.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{backup_id}.zip"

    file_count = 0
    total_size = 0

    try:
        with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Simple collection logic based on scope
            paths_to_check = []
            if request.include_configs:
                paths_to_check.append(project_root / "config")
            if request.include_reports:
                paths_to_check.append(data_root / "reports")
            if request.include_data_cache:
                paths_to_check.append(data_root / "cache")

            if request.scope == BackupScope.FULL_LOCAL_STATE:
                paths_to_check.append(data_root)

            for p in paths_to_check:
                if p.exists():
                    for root, _, files in p.walk():
                        for file in files:
                            file_path = root / file
                            if not should_exclude_path(file_path):
                                arcname = file_path.relative_to(project_root)
                                zipf.write(file_path, arcname)
                                file_count += 1
                                total_size += file_path.stat().st_size

        return BackupResult(
            backup_id=backup_id,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=BackupStatus.CREATED,
            request=request,
            backup_path=str(out_path),
            manifest_path=None,
            file_count=file_count,
            total_size_bytes=total_size
        )
    except Exception as e:
        if out_path.exists():
            out_path.unlink()
        return BackupResult(
            backup_id=backup_id, created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=BackupStatus.FAILED, request=request, backup_path=None, manifest_path=None,
            file_count=0, total_size_bytes=0, errors=[str(e)]
        )

def validate_backup(backup_path: Path) -> BackupResult:
    if not backup_path.exists():
        return BackupResult(
            backup_id="", created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=BackupStatus.FAILED, request=create_backup_request(BackupScope.REPORTS_ONLY, ""),
            backup_path=str(backup_path), manifest_path=None, file_count=0, total_size_bytes=0,
            errors=["Backup file not found"]
        )
    try:
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            files = zipf.namelist()
            return BackupResult(
                backup_id=backup_path.stem, created_at_utc=datetime.now(timezone.utc).isoformat(),
                status=BackupStatus.VALIDATED, request=create_backup_request(BackupScope.REPORTS_ONLY, ""),
                backup_path=str(backup_path), manifest_path=None, file_count=len(files), total_size_bytes=backup_path.stat().st_size
            )
    except Exception as e:
         return BackupResult(
            backup_id="", created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=BackupStatus.FAILED, request=create_backup_request(BackupScope.REPORTS_ONLY, ""),
            backup_path=str(backup_path), manifest_path=None, file_count=0, total_size_bytes=0,
            errors=[str(e)]
        )

def restore_dry_run(backup_path: Path, target_dir: Path) -> RestoreDryRunResult:
    conflicts = []
    files_checked = 0
    if not backup_path.exists():
        return RestoreDryRunResult(
            restore_id=f"rst_{uuid.uuid4().hex[:8]}", created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=BackupStatus.RESTORE_DRY_RUN_FAILED, backup_path=str(backup_path), target_dir=str(target_dir),
            files_checked=0, conflicts=[], missing_required_files=[], errors=["Backup file not found"]
        )

    try:
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            files = zipf.namelist()
            for file in files:
                files_checked += 1
                tgt = target_dir / file
                if tgt.exists():
                    conflicts.append(str(tgt))

        return RestoreDryRunResult(
            restore_id=f"rst_{uuid.uuid4().hex[:8]}",
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=BackupStatus.RESTORE_DRY_RUN_PASSED,
            backup_path=str(backup_path),
            target_dir=str(target_dir),
            files_checked=files_checked,
            conflicts=conflicts,
            missing_required_files=[]
        )
    except Exception as e:
        return RestoreDryRunResult(
            restore_id=f"rst_{uuid.uuid4().hex[:8]}", created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=BackupStatus.RESTORE_DRY_RUN_FAILED, backup_path=str(backup_path), target_dir=str(target_dir),
            files_checked=0, conflicts=[], missing_required_files=[], errors=[str(e)]
        )

def backup_result_to_dict(result: BackupResult) -> dict:
    # Simplified for serialization
    return {
        "backup_id": result.backup_id,
        "status": result.status.value,
        "file_count": result.file_count,
        "total_size_bytes": result.total_size_bytes,
        "errors": result.errors
    }

def restore_dry_run_result_to_dict(result: RestoreDryRunResult) -> dict:
    return {
        "restore_id": result.restore_id,
        "status": result.status.value,
        "files_checked": result.files_checked,
        "conflicts": result.conflicts,
        "errors": result.errors
    }

def backup_result_to_text(result: BackupResult) -> str:
    return f"Backup {result.backup_id}: {result.status.value}. Files: {result.file_count}. Errors: {len(result.errors)}"

def restore_dry_run_result_to_text(result: RestoreDryRunResult) -> str:
    return f"Restore Dry Run {result.restore_id}: {result.status.value}. Checked: {result.files_checked}. Conflicts: {len(result.conflicts)}."
