from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import platform
import sys
from typing import List, Optional
import uuid
from usa_signal_bot.core.enums import UpgradePrecheckStatus
from usa_signal_bot.release.artifact_collector import is_secret_like_path, should_exclude_path

@dataclass
class UpgradePrecheckItem:
    name: str
    status: UpgradePrecheckStatus
    message: str
    observed: Optional[str] = None
    expected: Optional[str] = None

@dataclass
class UpgradePrecheckResult:
    precheck_id: str
    created_at_utc: str
    status: UpgradePrecheckStatus
    items: List[UpgradePrecheckItem]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def check_python_version() -> UpgradePrecheckItem:
    ver = sys.version_info
    observed = f"{ver.major}.{ver.minor}.{ver.micro}"
    expected = "3.10+"
    if ver.major == 3 and ver.minor >= 10:
        return UpgradePrecheckItem("Python Version", UpgradePrecheckStatus.PASSED, "Python version OK.", observed, expected)
    return UpgradePrecheckItem("Python Version", UpgradePrecheckStatus.FAILED, "Python 3.10+ is required.", observed, expected)

def check_requirements_file(project_root: Path) -> UpgradePrecheckItem:
    req = project_root / "requirements.txt"
    if req.exists():
        return UpgradePrecheckItem("Requirements File", UpgradePrecheckStatus.PASSED, "requirements.txt found.")
    return UpgradePrecheckItem("Requirements File", UpgradePrecheckStatus.WARNING, "requirements.txt not found.")

def check_config_files(project_root: Path) -> UpgradePrecheckItem:
    cfg = project_root / "config/default.yaml"
    if cfg.exists():
        return UpgradePrecheckItem("Config File", UpgradePrecheckStatus.PASSED, "default.yaml found.")
    return UpgradePrecheckItem("Config File", UpgradePrecheckStatus.WARNING, "default.yaml not found.")

def check_data_directories(data_root: Path) -> UpgradePrecheckItem:
    dirs = ["universe", "cache", "reports"]
    missing = [d for d in dirs if not (data_root / d).exists()]
    if not missing:
        return UpgradePrecheckItem("Data Directories", UpgradePrecheckStatus.PASSED, "All required data directories exist.")
    return UpgradePrecheckItem("Data Directories", UpgradePrecheckStatus.WARNING, f"Missing directories: {missing}")

def check_no_secret_files_in_release_scope(project_root: Path) -> UpgradePrecheckItem:
    secrets = []
    # Search root and config for secrets
    for d in [project_root, project_root / "config"]:
        if d.exists():
            for f in d.iterdir():
                if f.is_file() and is_secret_like_path(f):
                    secrets.append(f.name)
    if not secrets:
        return UpgradePrecheckItem("No Secrets in Scope", UpgradePrecheckStatus.PASSED, "No secret-like files detected in sensitive paths.")
    return UpgradePrecheckItem("No Secrets in Scope", UpgradePrecheckStatus.WARNING, f"Found potential secret files: {secrets}")

def check_regression_smoke_available(project_root: Path) -> UpgradePrecheckItem:
    if (project_root / "usa_signal_bot" / "app" / "cli.py").exists():
        return UpgradePrecheckItem("Regression Smoke CLI", UpgradePrecheckStatus.PASSED, "CLI exists.")
    return UpgradePrecheckItem("Regression Smoke CLI", UpgradePrecheckStatus.WARNING, "CLI missing.")

def run_upgrade_precheck(project_root: Path, data_root: Path) -> UpgradePrecheckResult:
    items = [
        check_python_version(),
        check_requirements_file(project_root),
        check_config_files(project_root),
        check_data_directories(data_root),
        check_no_secret_files_in_release_scope(project_root),
        check_regression_smoke_available(project_root)
    ]

    failed = [i for i in items if i.status == UpgradePrecheckStatus.FAILED]
    blocked = [i for i in items if i.status == UpgradePrecheckStatus.BLOCKED]
    warnings = [i for i in items if i.status == UpgradePrecheckStatus.WARNING]

    overall = UpgradePrecheckStatus.PASSED
    if blocked: overall = UpgradePrecheckStatus.BLOCKED
    elif failed: overall = UpgradePrecheckStatus.FAILED
    elif warnings: overall = UpgradePrecheckStatus.WARNING

    err_msgs = [f"{i.name}: {i.message}" for i in blocked + failed]
    warn_msgs = [f"{i.name}: {i.message}" for i in warnings]

    return UpgradePrecheckResult(
        precheck_id=f"chk_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=overall,
        items=items,
        warnings=warn_msgs,
        errors=err_msgs
    )

def upgrade_precheck_item_to_dict(item: UpgradePrecheckItem) -> dict:
    return {"name": item.name, "status": item.status.value, "message": item.message, "observed": item.observed, "expected": item.expected}

def upgrade_precheck_result_to_dict(result: UpgradePrecheckResult) -> dict:
    return {
        "precheck_id": result.precheck_id,
        "status": result.status.value,
        "items": [upgrade_precheck_item_to_dict(i) for i in result.items],
        "warnings": result.warnings,
        "errors": result.errors
    }

def upgrade_precheck_result_to_text(result: UpgradePrecheckResult) -> str:
    lines = [f"Upgrade Precheck (ID: {result.precheck_id}) - Status: {result.status.value}"]
    for i in result.items:
        lines.append(f"- [{i.status.value}] {i.name}: {i.message}")
    return "\n".join(lines)
