import os
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from usa_signal_bot.core.enums import RetentionArtifactType


def classify_retention_artifact(path: Path, data_root: Path) -> RetentionArtifactType:
    try:
        rel_path = path.relative_to(data_root)
        parts = rel_path.parts

        if len(parts) >= 2:
            if parts[0] == "runtime" and parts[1] == "scans":
                return RetentionArtifactType.RUNTIME_SCAN
            if parts[0] in ("backtesting", "backtests"):
                return RetentionArtifactType.BACKTEST_RUN
            if parts[0] == "basket":
                return RetentionArtifactType.BASKET_RUN
            if parts[0] == "paper" and parts[1] == "runs":
                return RetentionArtifactType.PAPER_RUN
            if parts[0] == "paper" and parts[1] == "analytics":
                return RetentionArtifactType.PAPER_ANALYTICS
            if parts[0] == "comparison":
                return RetentionArtifactType.COMPARISON_RUN
            if parts[0] == "quality":
                return RetentionArtifactType.QUALITY_RUN
            if parts[0] == "regression" and parts[1] == "runs":
                return RetentionArtifactType.REGRESSION_RUN
            if parts[0] == "release" and parts[1] == "builds":
                return RetentionArtifactType.RELEASE_BUILD
            if parts[0] == "release" and parts[1] == "backups":
                return RetentionArtifactType.BACKUP
            if parts[0] == "observability" and parts[1] == "logs":
                return RetentionArtifactType.OBSERVABILITY_LOG
            if parts[0] == "observability" and parts[1] == "reports":
                return RetentionArtifactType.OBSERVABILITY_REPORT
            if parts[0] == "notifications":
                return RetentionArtifactType.NOTIFICATION_RUN
            if parts[0] in ("tmp", "temp"):
                return RetentionArtifactType.TEMP_FILE
    except ValueError:
        pass

    return RetentionArtifactType.UNKNOWN


def artifact_age_days(path: Path) -> float | None:
    try:
        mtime = path.stat().st_mtime
        now = datetime.now(timezone.utc).timestamp()
        return (now - mtime) / (24 * 3600)
    except OSError:
        return None


def artifact_size_bytes(path: Path) -> int:
    try:
        if path.is_file():
            return path.stat().st_size
        elif path.is_dir():
            total = 0
            for dirpath, _, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total += os.path.getsize(fp)
            return total
        return 0
    except OSError:
        return 0


def artifact_last_modified_utc(path: Path) -> str | None:
    try:
        mtime = path.stat().st_mtime
        return datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()
    except OSError:
        return None


def artifact_checksum_if_small(path: Path, max_size_bytes: int = 1048576) -> str | None:
    try:
        if not path.is_file():
            return None
        if path.stat().st_size > max_size_bytes:
            return None
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None


def discover_retention_artifacts(
    data_root: Path, include_files: bool = True, include_dirs: bool = True
) -> list[Path]:
    artifacts = []
    if not data_root.exists() or not data_root.is_dir():
        return artifacts

    for dirpath, dirnames, filenames in os.walk(data_root):
        dp = Path(dirpath)
        if dp == data_root:
            continue

        rel = dp.relative_to(data_root)

        if (
            len(rel.parts) >= 2
            and classify_retention_artifact(dp, data_root)
            != RetentionArtifactType.UNKNOWN
        ):
            if include_dirs:
                artifacts.append(dp)
            dirnames[:] = []
            continue

        if include_files:
            for f in filenames:
                file_path = dp / f
                if (
                    classify_retention_artifact(file_path, data_root)
                    != RetentionArtifactType.UNKNOWN
                ):
                    artifacts.append(file_path)

    return artifacts


def group_artifacts_by_type(
    paths: list[Path], data_root: Path
) -> dict[RetentionArtifactType, list[Path]]:
    grouped = {t: [] for t in RetentionArtifactType}
    for p in paths:
        t = classify_retention_artifact(p, data_root)
        grouped[t].append(p)
    return grouped


def summarize_artifact_group(paths: list[Path], data_root: Path) -> dict[str, Any]:
    return {
        "count": len(paths),
        "total_size_bytes": sum(artifact_size_bytes(p) for p in paths),
        "types": {
            t.value: len(ps)
            for t, ps in group_artifacts_by_type(paths, data_root).items()
        },
    }
