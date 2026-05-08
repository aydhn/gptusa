from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
import uuid
from usa_signal_bot.release.release_models import ReleaseVersion

@dataclass
class ChangelogEntry:
    entry_id: str
    version: str
    date_utc: str
    title: str
    changes: List[str]
    warnings: List[str] = field(default_factory=list)

def generate_changelog_entry_for_release(version: ReleaseVersion, phase_summary_paths: List[Path]) -> ChangelogEntry:
    changes = []
    warnings = []

    for path in phase_summary_paths:
        if path.exists():
            try:
                content = path.read_text(encoding='utf-8')
                lines = [line.strip() for line in content.splitlines() if line.strip().startswith("- ")]
                changes.extend(lines)
            except Exception as e:
                warnings.append(f"Failed to read {path.name}: {e}")
        else:
            warnings.append(f"Phase summary file not found: {path.name}")

    if not changes:
        changes.append("- Maintenance and stability improvements.")

    return ChangelogEntry(
        entry_id=f"cl_entry_{uuid.uuid4().hex[:8]}",
        version=version.version,
        date_utc=datetime.now(timezone.utc).date().isoformat(),
        title=f"Release {version.version}",
        changes=changes,
        warnings=warnings
    )

def generate_changelog_from_docs(project_root: Path) -> List[ChangelogEntry]:
    # Placeholder: currently generates a single entry for the current state
    from usa_signal_bot.release.versioning import build_release_version
    version = build_release_version(project_root=project_root)
    docs_dir = project_root / "docs"
    summary_files = list(docs_dir.glob("PHASE_*_SUMMARY.md")) if docs_dir.exists() else []
    entry = generate_changelog_entry_for_release(version, summary_files)
    return [entry]

def changelog_entry_to_dict(entry: ChangelogEntry) -> dict:
    return {
        "entry_id": entry.entry_id,
        "version": entry.version,
        "date_utc": entry.date_utc,
        "title": entry.title,
        "changes": entry.changes,
        "warnings": entry.warnings
    }

def changelog_entries_to_markdown(entries: List[ChangelogEntry]) -> str:
    lines = ["# Changelog\n"]
    lines.append("*Disclaimer: This software is for local research only and does not constitute investment advice.*\n")

    for entry in entries:
        lines.append(f"## [{entry.version}] - {entry.date_utc}")
        lines.append(f"### {entry.title}")
        if entry.changes:
            lines.extend(entry.changes)
        else:
            lines.append("- No recorded changes.")
        lines.append("")

    return "\n".join(lines)

def write_changelog_markdown(path: Path, entries: List[ChangelogEntry]) -> Path:
    md = changelog_entries_to_markdown(entries)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(md, encoding='utf-8')
    return path

def read_existing_changelog(path: Path) -> Optional[str]:
    if path.exists():
        try:
            return path.read_text(encoding='utf-8')
        except Exception:
            pass
    return None
