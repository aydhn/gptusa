import json
from pathlib import Path
from typing import List, Optional, Any
from usa_signal_bot.release.release_models import (
    ReleaseBuildResult, ReleaseManifest, OperatorRunbook, release_build_result_to_dict,
    release_manifest_to_dict, operator_runbook_to_dict
)
from usa_signal_bot.release.maintenance_models import (
    MaintenancePlan, MaintenanceRunResult, maintenance_plan_to_dict, maintenance_run_result_to_dict
)
from usa_signal_bot.release.backup_restore import BackupResult, RestoreDryRunResult, backup_result_to_dict, restore_dry_run_result_to_dict
from usa_signal_bot.release.upgrade_precheck import UpgradePrecheckResult, upgrade_precheck_result_to_dict

def release_store_dir(data_root: Path) -> Path:
    d = data_root / "release" / "builds"
    d.mkdir(parents=True, exist_ok=True)
    return d

def build_release_run_dir(data_root: Path, build_id: str) -> Path:
    d = release_store_dir(data_root) / build_id
    d.mkdir(parents=True, exist_ok=True)
    return d

def backup_store_dir(data_root: Path) -> Path:
    d = data_root / "release" / "backups"
    d.mkdir(parents=True, exist_ok=True)
    return d

def maintenance_store_dir(data_root: Path) -> Path:
    d = data_root / "release" / "maintenance"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_release_build_result_json(path: Path, result: ReleaseBuildResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(release_build_result_to_dict(result), f, indent=2)
    return path

def write_release_manifest_json_store(path: Path, manifest: ReleaseManifest) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(release_manifest_to_dict(manifest), f, indent=2)
    return path

def write_operator_runbook_markdown_store(path: Path, runbook: OperatorRunbook) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    from usa_signal_bot.release.runbook_generator import runbook_to_markdown
    path.write_text(runbook_to_markdown(runbook), encoding='utf-8')
    return path

def write_maintenance_plan_json(path: Path, plan: MaintenancePlan) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(maintenance_plan_to_dict(plan), f, indent=2)
    return path

def write_maintenance_run_result_json(path: Path, result: MaintenanceRunResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(maintenance_run_result_to_dict(result), f, indent=2)
    return path

def write_backup_result_json(path: Path, result: BackupResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(backup_result_to_dict(result), f, indent=2)
    return path

def write_restore_dry_run_result_json(path: Path, result: RestoreDryRunResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(restore_dry_run_result_to_dict(result), f, indent=2)
    return path

def write_upgrade_precheck_result_json(path: Path, result: UpgradePrecheckResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(upgrade_precheck_result_to_dict(result), f, indent=2)
    return path

def read_release_build_result_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_release_builds(data_root: Path) -> List[Path]:
    d = release_store_dir(data_root)
    if not d.exists():
        return []
    # Find all result.json files inside subdirectories
    return [p.parent for p in d.rglob("result.json")]

def get_latest_release_build_dir(data_root: Path) -> Optional[Path]:
    dirs = list_release_builds(data_root)
    if not dirs:
        return None
    return max(dirs, key=lambda d: (d / "result.json").stat().st_mtime)

def release_store_summary(data_root: Path) -> dict:
    dirs = list_release_builds(data_root)
    latest = get_latest_release_build_dir(data_root)
    return {
        "total_builds": len(dirs),
        "latest_build_dir": str(latest) if latest else None
    }
