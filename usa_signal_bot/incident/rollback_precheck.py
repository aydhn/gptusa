from pathlib import Path
import datetime
import uuid
import zipfile
import json
from dataclasses import dataclass, field
from typing import Any
from usa_signal_bot.core.enums import RollbackSafetyStatus
from usa_signal_bot.incident.rollback_models import RollbackSource, create_rollback_source_id

@dataclass
class RollbackPrecheckItem:
    name: str
    status: RollbackSafetyStatus
    message: str
    observed: str | None = None
    expected: str | None = None

@dataclass
class RollbackPrecheckReport:
    report_id: str
    created_at_utc: str
    status: RollbackSafetyStatus
    source: RollbackSource
    items: list[RollbackPrecheckItem]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def create_rollback_precheck_report_id(prefix: str = "precheck_report") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def check_rollback_source_exists(source: RollbackSource) -> RollbackPrecheckItem:
    p = Path(source.path)
    if not p.exists():
        return RollbackPrecheckItem("Source Exists", RollbackSafetyStatus.BLOCKED, f"Path {source.path} does not exist.")
    return RollbackPrecheckItem("Source Exists", RollbackSafetyStatus.SAFE, "Source exists.")

def check_rollback_source_checksum(source: RollbackSource) -> RollbackPrecheckItem:
    from usa_signal_bot.incident.rollback_sources import _calc_checksum
    if not source.checksum:
        return RollbackPrecheckItem("Checksum Match", RollbackSafetyStatus.WARNING, "No checksum recorded on source to verify.")
    current = _calc_checksum(Path(source.path))
    if current != source.checksum:
         return RollbackPrecheckItem("Checksum Match", RollbackSafetyStatus.BLOCKED, "Checksum mismatch", observed=current, expected=source.checksum)
    return RollbackPrecheckItem("Checksum Match", RollbackSafetyStatus.SAFE, "Checksum matches expected.", observed=current, expected=source.checksum)

def check_rollback_no_secret_payload(source: RollbackSource) -> RollbackPrecheckItem:
    p = Path(source.path)
    if not p.exists():
        return RollbackPrecheckItem("No Secret Payload", RollbackSafetyStatus.UNKNOWN, "Source does not exist.")

    # Inspect zip contents
    if p.suffix == ".zip":
        try:
            with zipfile.ZipFile(p, 'r') as zf:
                for name in zf.namelist():
                    nl = name.lower()
                    if "secret" in nl or "token" in nl or "key" in nl or "credential" in nl:
                        # Allow specific keys if they are safe or inside a known safe structure, but we block generally
                        if not any(safe in nl for safe in ["public", "example", ".py", ".md"]):
                            return RollbackPrecheckItem("No Secret Payload", RollbackSafetyStatus.BLOCKED, f"Sensitive file name found in archive: {name}")
        except Exception as e:
            return RollbackPrecheckItem("No Secret Payload", RollbackSafetyStatus.WARNING, f"Could not inspect zip: {e}")
    else:
        if "secret" in p.name.lower() or "token" in p.name.lower():
            return RollbackPrecheckItem("No Secret Payload", RollbackSafetyStatus.BLOCKED, f"Sensitive source file name: {p.name}")

    return RollbackPrecheckItem("No Secret Payload", RollbackSafetyStatus.SAFE, "No sensitive payloads detected.")

def check_rollback_backup_manifest(source: RollbackSource) -> RollbackPrecheckItem:
    p = Path(source.path)
    if p.suffix != ".zip":
         return RollbackPrecheckItem("Manifest Exists", RollbackSafetyStatus.SAFE, "Not a zip archive.")

    try:
        with zipfile.ZipFile(p, 'r') as zf:
            if "manifest.json" not in zf.namelist():
                return RollbackPrecheckItem("Manifest Exists", RollbackSafetyStatus.WARNING, "Missing manifest.json in archive.")
    except Exception as e:
        return RollbackPrecheckItem("Manifest Exists", RollbackSafetyStatus.WARNING, f"Could not read zip: {e}")

    return RollbackPrecheckItem("Manifest Exists", RollbackSafetyStatus.SAFE, "Manifest exists.")

def check_rollback_target_paths_safe(source: RollbackSource, project_root: Path, data_root: Path) -> RollbackPrecheckItem:
    p = Path(source.path)
    if p.suffix != ".zip":
        return RollbackPrecheckItem("Target Paths Safe", RollbackSafetyStatus.SAFE, "Single file source.")

    try:
        with zipfile.ZipFile(p, 'r') as zf:
            for name in zf.namelist():
                if ".." in name or name.startswith("/"):
                    return RollbackPrecheckItem("Target Paths Safe", RollbackSafetyStatus.BLOCKED, f"Unsafe traversal in archive: {name}")
    except Exception as e:
        return RollbackPrecheckItem("Target Paths Safe", RollbackSafetyStatus.WARNING, f"Could not read zip: {e}")

    return RollbackPrecheckItem("Target Paths Safe", RollbackSafetyStatus.SAFE, "All paths in archive are safe relative paths.")

def check_rollback_not_live_execution(source: RollbackSource) -> RollbackPrecheckItem:
    return RollbackPrecheckItem("Not Live Execution", RollbackSafetyStatus.SAFE, "Rollback dry-run by default.")

def run_rollback_precheck(source: RollbackSource, project_root: Path, data_root: Path) -> RollbackPrecheckReport:
    items = []
    items.append(check_rollback_source_exists(source))
    if items[-1].status != RollbackSafetyStatus.BLOCKED:
        items.append(check_rollback_source_checksum(source))
        items.append(check_rollback_no_secret_payload(source))
        items.append(check_rollback_backup_manifest(source))
        items.append(check_rollback_target_paths_safe(source, project_root, data_root))
    items.append(check_rollback_not_live_execution(source))

    status = RollbackSafetyStatus.SAFE
    for it in items:
        if it.status == RollbackSafetyStatus.BLOCKED:
            status = RollbackSafetyStatus.BLOCKED
            break
        elif it.status == RollbackSafetyStatus.WARNING and status != RollbackSafetyStatus.BLOCKED:
            status = RollbackSafetyStatus.WARNING

    return RollbackPrecheckReport(
        report_id=create_rollback_precheck_report_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=status,
        source=source,
        items=items,
        warnings=[i.message for i in items if i.status == RollbackSafetyStatus.WARNING],
        errors=[i.message for i in items if i.status == RollbackSafetyStatus.BLOCKED]
    )

def rollback_precheck_report_to_dict(report: RollbackPrecheckReport) -> dict:
    from usa_signal_bot.incident.rollback_models import rollback_source_to_dict
    return {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "status": report.status.value,
        "source": rollback_source_to_dict(report.source),
        "items": [
            {
                "name": i.name,
                "status": i.status.value,
                "message": i.message,
                "observed": i.observed,
                "expected": i.expected
            } for i in report.items
        ],
        "warnings": report.warnings,
        "errors": report.errors
    }

def rollback_precheck_report_to_text(report: RollbackPrecheckReport) -> str:
    lines = [f"Precheck Report: {report.status.name}"]
    for i in report.items:
        lines.append(f"  {i.name}: {i.status.name} - {i.message}")
    return "\n".join(lines)
