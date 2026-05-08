import datetime
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional
from usa_signal_bot.core.enums import OperationalMetricStatus

@dataclass
class ArtifactMetricsSummary:
    summary_id: str
    created_at_utc: str
    artifact_counts: Dict[str, int]
    latest_paths: Dict[str, Optional[str]]
    stale_artifacts: List[str]
    missing_artifacts: List[str]
    status: OperationalMetricStatus
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def count_dirs(path: Path) -> int:
    if not path.exists(): return 0
    return len([x for x in path.iterdir() if x.is_dir()])

def latest_dir(path: Path) -> Optional[Path]:
    if not path.exists(): return None
    dirs = [x for x in path.iterdir() if x.is_dir()]
    if not dirs: return None
    return sorted(dirs, key=lambda x: x.stat().st_mtime, reverse=True)[0]

def detect_missing_core_artifacts(data_root: Path) -> List[str]:
    core = [
        "runtime/scans",
        "paper/runs",
        "comparison/runs",
        "quality/runs",
        "regression/runs",
        "release/builds"
    ]
    missing = []
    for c in core:
        p = data_root / c
        if not p.exists() or count_dirs(p) == 0:
            missing.append(c)
    return missing

def detect_stale_artifacts(data_root: Path, max_age_hours: int = 72) -> List[str]:
    core = [
        "runtime/scans",
        "paper/runs",
        "comparison/runs",
        "quality/runs"
    ]
    stale = []
    now = datetime.datetime.now()
    for c in core:
        p = data_root / c
        latest = latest_dir(p)
        if latest:
            age = (now - datetime.datetime.fromtimestamp(latest.stat().st_mtime)).total_seconds()
            if age > max_age_hours * 3600:
                stale.append(f"{c} (latest is {age/3600:.1f}h old)")
    return stale

def collect_artifact_metrics(data_root: Path) -> ArtifactMetricsSummary:
    core = [
        "runtime/scans",
        "paper/runs",
        "paper/analytics",
        "comparison/runs",
        "quality/runs",
        "regression/runs",
        "release/builds"
    ]

    counts = {}
    latests = {}
    for c in core:
        p = data_root / c
        counts[c] = count_dirs(p)
        l = latest_dir(p)
        latests[c] = str(l) if l else None

    missing = detect_missing_core_artifacts(data_root)
    stale = detect_stale_artifacts(data_root)

    st = OperationalMetricStatus.OK
    if missing or stale:
        st = OperationalMetricStatus.WARNING

    return ArtifactMetricsSummary(
        summary_id=f"art_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        artifact_counts=counts,
        latest_paths=latests,
        stale_artifacts=stale,
        missing_artifacts=missing,
        status=st
    )

def artifact_metrics_summary_to_dict(summary: ArtifactMetricsSummary) -> dict:
    from dataclasses import asdict
    return asdict(summary)

def artifact_metrics_summary_to_text(summary: ArtifactMetricsSummary) -> str:
    lines = [
        f"--- Artifact Metrics Summary ---",
        f"Status: {summary.status.value}",
        "Counts:"
    ]
    for k, v in summary.artifact_counts.items(): lines.append(f"  - {k}: {v}")
    if summary.missing_artifacts:
        lines.append(f"Missing Core: {', '.join(summary.missing_artifacts)}")
    if summary.stale_artifacts:
        lines.append(f"Stale: {', '.join(summary.stale_artifacts)}")
    return "\n".join(lines)
