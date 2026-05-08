import json
import uuid
import datetime
from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path
from usa_signal_bot.core.enums import OperationalMetricStatus

@dataclass
class RunDurationSummary:
    summary_id: str
    created_at_utc: str
    source: str
    run_count: int
    average_duration_seconds: Optional[float]
    max_duration_seconds: Optional[float]
    slow_run_count: int
    status: OperationalMetricStatus
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def summarize_duration_values(values: List[float], source: str, slow_threshold_seconds: float = 300.0) -> RunDurationSummary:
    errs = []
    vals = []
    for v in values:
        if v < 0:
            errs.append(f"Negative duration found: {v}")
        else:
            vals.append(v)

    c = len(vals)
    if c == 0:
        return RunDurationSummary(
            summary_id=f"dur_{uuid.uuid4().hex[:8]}",
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            source=source,
            run_count=0,
            average_duration_seconds=None,
            max_duration_seconds=None,
            slow_run_count=0,
            status=OperationalMetricStatus.WARNING,
            warnings=["No valid duration values found"],
            errors=errs
        )

    avg = sum(vals) / c
    mx = max(vals)
    slow = sum(1 for x in vals if x > slow_threshold_seconds)

    return RunDurationSummary(
        summary_id=f"dur_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source=source,
        run_count=c,
        average_duration_seconds=avg,
        max_duration_seconds=mx,
        slow_run_count=slow,
        status=OperationalMetricStatus.OK if slow < (c * 0.5) else OperationalMetricStatus.WARNING,
        warnings=[],
        errors=errs
    )

def _collect_durations_from_runs(base_dir: Path, json_name: str, duration_key: str) -> List[float]:
    durs = []
    if not base_dir.exists(): return durs
    for d in base_dir.iterdir():
        if d.is_dir():
            p = d / json_name
            if p.exists():
                try:
                    with open(p, "r") as f:
                        data = json.load(f)
                        if duration_key in data:
                            durs.append(float(data[duration_key]))
                except Exception:
                    pass
    return durs

def collect_run_durations_from_scan_runs(data_root: Path) -> RunDurationSummary:
    durs = _collect_durations_from_runs(data_root / "runtime" / "scans", "scan_report.json", "duration_seconds")
    return summarize_duration_values(durs, "scan_runs")

def collect_run_durations_from_regression_runs(data_root: Path) -> RunDurationSummary:
    durs = _collect_durations_from_runs(data_root / "regression" / "runs", "result.json", "duration_seconds")
    return summarize_duration_values(durs, "regression_runs", slow_threshold_seconds=600.0)

def collect_run_durations_from_quality_runs(data_root: Path) -> RunDurationSummary:
    durs = _collect_durations_from_runs(data_root / "quality" / "runs", "result.json", "duration_seconds")
    return summarize_duration_values(durs, "quality_runs", slow_threshold_seconds=600.0)

def run_duration_summary_to_dict(summary: RunDurationSummary) -> dict:
    from dataclasses import asdict
    return asdict(summary)

def run_duration_summary_to_text(summary: RunDurationSummary) -> str:
    lines = [
        f"--- Run Duration Summary: {summary.source} ---",
        f"Status: {summary.status.value} | Runs: {summary.run_count}",
    ]
    if summary.run_count > 0:
        lines.append(f"Avg Duration: {summary.average_duration_seconds:.2f}s | Max: {summary.max_duration_seconds:.2f}s")
        lines.append(f"Slow Runs: {summary.slow_run_count}")
    return "\n".join(lines)
