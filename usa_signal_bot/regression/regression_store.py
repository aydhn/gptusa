import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.regression.regression_models import RegressionRunResult, RegressionStepResult, ReleaseRehearsalResult, regression_run_result_to_dict, regression_step_result_to_dict, release_rehearsal_result_to_dict

def regression_store_dir(data_root: Path) -> Path:
    return data_root / "regression"

def golden_store_dir(data_root: Path) -> Path:
    return regression_store_dir(data_root) / "golden"

def baseline_snapshot_dir(data_root: Path) -> Path:
    return regression_store_dir(data_root) / "baselines"

def build_regression_run_dir(data_root: Path, run_id: str) -> Path:
    return regression_store_dir(data_root) / "runs" / run_id

def build_release_rehearsal_dir(data_root: Path, rehearsal_id: str) -> Path:
    return regression_store_dir(data_root) / "releases" / rehearsal_id

def write_regression_run_result_json(path: Path, result: RegressionRunResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(regression_run_result_to_dict(result), f, indent=2)
    return path

def write_regression_step_results_jsonl(path: Path, results: List[RegressionStepResult]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for r in results:
            f.write(json.dumps(regression_step_result_to_dict(r)) + "\n")
    return path

def write_release_rehearsal_result_json(path: Path, result: ReleaseRehearsalResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(release_rehearsal_result_to_dict(result), f, indent=2)
    return path

def write_regression_drift_report_json(path: Path, report: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    from usa_signal_bot.regression.regression_drift import regression_drift_report_to_dict
    with open(path, "w") as f:
        json.dump(regression_drift_report_to_dict(report), f, indent=2)
    return path

def write_regression_manifest_json(path: Path, result: RegressionRunResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump({
            "run_id": result.run_id,
            "status": result.status.value,
            "outputs": result.output_paths
        }, f, indent=2)
    return path

def write_regression_validation_report_json(path: Path, report: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    from dataclasses import asdict
    with open(path, "w") as f:
         json.dump(asdict(report), f, indent=2)
    return path

def read_regression_run_result_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def read_release_rehearsal_result_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_regression_runs(data_root: Path) -> List[Path]:
    runs_dir = regression_store_dir(data_root) / "runs"
    if not runs_dir.exists():
        return []
    return sorted([p for p in runs_dir.iterdir() if p.is_dir()], key=lambda x: x.stat().st_mtime, reverse=True)

def list_release_rehearsals(data_root: Path) -> List[Path]:
    releases_dir = regression_store_dir(data_root) / "releases"
    if not releases_dir.exists():
        return []
    return sorted([p for p in releases_dir.iterdir() if p.is_dir()], key=lambda x: x.stat().st_mtime, reverse=True)

def get_latest_regression_run_dir(data_root: Path) -> Optional[Path]:
    runs = list_regression_runs(data_root)
    return runs[0] if runs else None

def get_latest_release_rehearsal_dir(data_root: Path) -> Optional[Path]:
    releases = list_release_rehearsals(data_root)
    return releases[0] if releases else None

def regression_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "runs_count": len(list_regression_runs(data_root)),
        "releases_count": len(list_release_rehearsals(data_root))
    }
