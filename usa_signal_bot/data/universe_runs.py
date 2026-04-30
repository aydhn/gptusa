from typing import Any
import json
import tempfile
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import ActiveUniverseSource, UniverseDataRunStatus, UniverseRunStep
from usa_signal_bot.core.exceptions import UniverseDataRunError

@dataclass
class UniverseDataRunStepResult:
    step: UniverseRunStep
    status: UniverseDataRunStatus
    started_at_utc: str
    finished_at_utc: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class UniverseDataRun:
    run_id: str
    universe_name: str
    source: ActiveUniverseSource
    source_path: Optional[str]
    provider_name: str
    timeframes: List[str]
    total_symbols: int
    status: UniverseDataRunStatus
    created_at_utc: str
    started_at_utc: Optional[str]
    finished_at_utc: Optional[str]
    steps: List[UniverseDataRunStepResult] = field(default_factory=list)
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def build_universe_run_dir(data_root: Path, run_id: str) -> Path:
    # Avoid path traversal
    clean_id = "".join(c if c.isalnum() or c in "_-" else "_" for c in run_id)
    return data_root / "universe" / "runs" / clean_id

def create_universe_data_run(
    universe_name: str,
    source: ActiveUniverseSource,
    source_path: Optional[str],
    provider_name: str,
    timeframes: List[str],
    total_symbols: int
) -> UniverseDataRun:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    clean_name = "".join(c if c.isalnum() else "_" for c in universe_name).lower()
    run_id = f"run_{clean_name}_{timestamp}"

    return UniverseDataRun(
        run_id=run_id,
        universe_name=universe_name,
        source=source,
        source_path=source_path,
        provider_name=provider_name,
        timeframes=timeframes.copy(),
        total_symbols=total_symbols,
        status=UniverseDataRunStatus.CREATED,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        started_at_utc=None,
        finished_at_utc=None
    )

def start_universe_data_run(run: UniverseDataRun) -> UniverseDataRun:
    run.status = UniverseDataRunStatus.RUNNING
    run.started_at_utc = datetime.now(timezone.utc).isoformat()
    return run

def finish_universe_data_run(run: UniverseDataRun, status: UniverseDataRunStatus) -> UniverseDataRun:
    run.status = status
    run.finished_at_utc = datetime.now(timezone.utc).isoformat()
    return run

def add_run_step_result(run: UniverseDataRun, step_result: UniverseDataRunStepResult) -> UniverseDataRun:
    run.steps.append(step_result)
    return run

def create_step_result(
    step: UniverseRunStep,
    status: UniverseDataRunStatus,
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> UniverseDataRunStepResult:
    return UniverseDataRunStepResult(
        step=step,
        status=status,
        started_at_utc=datetime.now(timezone.utc).isoformat(),
        finished_at_utc=datetime.now(timezone.utc).isoformat(),
        message=message,
        details=details or {}
    )

def write_universe_data_run(path: Path, run: UniverseDataRun) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "run_id": run.run_id,
        "universe_name": run.universe_name,
        "source": run.source.value if hasattr(run.source, 'value') else str(run.source),
        "source_path": run.source_path,
        "provider_name": run.provider_name,
        "timeframes": run.timeframes,
        "total_symbols": run.total_symbols,
        "status": run.status.value if hasattr(run.status, 'value') else str(run.status),
        "created_at_utc": run.created_at_utc,
        "started_at_utc": run.started_at_utc,
        "finished_at_utc": run.finished_at_utc,
        "steps": [
            {
                "step": s.step.value if hasattr(s.step, 'value') else str(s.step),
                "status": s.status.value if hasattr(s.status, 'value') else str(s.status),
                "started_at_utc": s.started_at_utc,
                "finished_at_utc": s.finished_at_utc,
                "message": s.message,
                "details": s.details
            }
            for s in run.steps
        ],
        "output_paths": run.output_paths,
        "warnings": run.warnings,
        "errors": run.errors
    }

    fd, temp_path_str = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    temp_path = Path(temp_path_str)

    try:
        with open(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(temp_path, path)
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise UniverseDataRunError(f"Failed to write run metadata: {e}")

    return path

def read_universe_data_run(path: Path) -> UniverseDataRun:
    if not path.exists():
        raise UniverseDataRunError(f"Run metadata not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        steps = []
        for s in data.get("steps", []):
            steps.append(UniverseDataRunStepResult(
                step=UniverseRunStep(s["step"]),
                status=UniverseDataRunStatus(s["status"]),
                started_at_utc=s["started_at_utc"],
                finished_at_utc=s["finished_at_utc"],
                message=s["message"],
                details=s.get("details", {})
            ))

        return UniverseDataRun(
            run_id=data["run_id"],
            universe_name=data["universe_name"],
            source=ActiveUniverseSource(data["source"]),
            source_path=data.get("source_path"),
            provider_name=data["provider_name"],
            timeframes=data.get("timeframes", []),
            total_symbols=data["total_symbols"],
            status=UniverseDataRunStatus(data["status"]),
            created_at_utc=data["created_at_utc"],
            started_at_utc=data.get("started_at_utc"),
            finished_at_utc=data.get("finished_at_utc"),
            steps=steps,
            output_paths=data.get("output_paths", {}),
            warnings=data.get("warnings", []),
            errors=data.get("errors", [])
        )
    except Exception as e:
        raise UniverseDataRunError(f"Failed to read run metadata {path}: {e}")

def list_universe_data_runs(data_root: Path) -> List[UniverseDataRun]:
    runs_dir = data_root / "universe" / "runs"
    if not runs_dir.exists() or not runs_dir.is_dir():
        return []

    runs = []
    for d in runs_dir.iterdir():
        if d.is_dir():
            meta_file = d / "run_metadata.json"
            if meta_file.exists():
                try:
                    runs.append(read_universe_data_run(meta_file))
                except Exception:
                    pass # Skip corrupted

    return sorted(runs, key=lambda r: r.created_at_utc, reverse=True)

def get_latest_universe_data_run(data_root: Path) -> Optional[UniverseDataRun]:
    runs = list_universe_data_runs(data_root)
    return runs[0] if runs else None

def universe_data_run_to_text(run: UniverseDataRun) -> str:
    lines = [
        "=== Universe Data Run ===",
        f"Run ID              : {run.run_id}",
        f"Universe Name       : {run.universe_name}",
        f"Status              : {run.status.value}",
        f"Source              : {run.source.value}",
        f"Provider            : {run.provider_name}",
        f"Total Symbols       : {run.total_symbols}",
        f"Timeframes          : {', '.join(run.timeframes)}",
        f"Created At (UTC)    : {run.created_at_utc}"
    ]

    if run.started_at_utc:
        lines.append(f"Started At (UTC)    : {run.started_at_utc}")
    if run.finished_at_utc:
        lines.append(f"Finished At (UTC)   : {run.finished_at_utc}")

    if run.warnings:
        lines.append("\nWarnings:")
        for w in run.warnings:
            lines.append(f" - {w}")

    if run.errors:
        lines.append("\nErrors:")
        for e in run.errors:
            lines.append(f" - {e}")

    return "\n".join(lines)
