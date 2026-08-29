from pathlib import Path
import datetime
import hashlib
from usa_signal_bot.core.enums import RollbackSourceType
from usa_signal_bot.incident.rollback_models import RollbackSource, create_rollback_source_id

def _calc_checksum(p: Path) -> str | None:
    if not p.is_file():
        return None
    # Calculate sha256 only if file is less than 50MB
    if p.stat().st_size > 50 * 1024 * 1024:
        return None
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def discover_release_bundle_sources(data_root: Path) -> list[RollbackSource]:
    sources = []
    release_dir = data_root / "release" / "bundles"
    if release_dir.exists():
        for z in release_dir.glob("*.zip"):
            sources.append(RollbackSource(
                source_id=create_rollback_source_id(str(z)),
                source_type=RollbackSourceType.RELEASE_BUNDLE,
                path=str(z),
                created_at_utc=datetime.datetime.utcfromtimestamp(z.stat().st_mtime).isoformat() + "Z",
                checksum=_calc_checksum(z),
                valid=True,
                warnings=[],
                errors=[]
            ))
    return sources

def discover_backup_archive_sources(data_root: Path) -> list[RollbackSource]:
    sources = []
    backup_dir = data_root / "release" / "backups"
    if backup_dir.exists():
        for z in backup_dir.glob("*.zip"):
            sources.append(RollbackSource(
                source_id=create_rollback_source_id(str(z)),
                source_type=RollbackSourceType.BACKUP_ARCHIVE,
                path=str(z),
                created_at_utc=datetime.datetime.utcfromtimestamp(z.stat().st_mtime).isoformat() + "Z",
                checksum=_calc_checksum(z),
                valid=True,
                warnings=[],
                errors=[]
            ))
    return sources

def discover_config_profile_sources(project_root: Path) -> list[RollbackSource]:
    sources = []
    config_dir = project_root / "config"
    if config_dir.exists():
        for y in config_dir.glob("*.yaml"):
            if "example" in y.name:
                continue
            sources.append(RollbackSource(
                source_id=create_rollback_source_id(str(y)),
                source_type=RollbackSourceType.CONFIG_PROFILE,
                path=str(y),
                created_at_utc=datetime.datetime.utcfromtimestamp(y.stat().st_mtime).isoformat() + "Z",
                checksum=_calc_checksum(y),
                valid=True,
                warnings=[],
                errors=[]
            ))
    return sources

def discover_regression_baseline_sources(data_root: Path) -> list[RollbackSource]:
    sources = []
    baseline_dir = data_root / "regression" / "baselines"
    if baseline_dir.exists():
        for p in baseline_dir.glob("*.json"):
            sources.append(RollbackSource(
                source_id=create_rollback_source_id(str(p)),
                source_type=RollbackSourceType.REGRESSION_BASELINE,
                path=str(p),
                created_at_utc=datetime.datetime.utcfromtimestamp(p.stat().st_mtime).isoformat() + "Z",
                checksum=_calc_checksum(p),
                valid=True,
                warnings=[],
                errors=[]
            ))
    return sources

def discover_rollback_sources(data_root: Path, project_root: Path | None = None) -> list[RollbackSource]:
    sources = []
    sources.extend(discover_release_bundle_sources(data_root))
    sources.extend(discover_backup_archive_sources(data_root))
    sources.extend(discover_regression_baseline_sources(data_root))
    if project_root:
        sources.extend(discover_config_profile_sources(project_root))

    return sorted(sources, key=lambda x: x.created_at_utc or "", reverse=True)

def latest_valid_rollback_source(data_root: Path, source_type: RollbackSourceType | None = None) -> RollbackSource | None:
    sources = discover_rollback_sources(data_root)
    if source_type:
        sources = [s for s in sources if s.source_type == source_type]
    for s in sources:
        if s.valid:
            return s
    return None

def rollback_source_summary_to_text(sources: list[RollbackSource]) -> str:
    lines = []
    for s in sources:
        lines.append(f"{s.source_type.name} - {s.path} (Valid: {s.valid}, Date: {s.created_at_utc})")
    if not lines:
        return "No rollback sources found."
    return "\n".join(lines)
