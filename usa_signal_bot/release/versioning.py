from datetime import datetime, timezone
import platform
import logging
import subprocess
from pathlib import Path
from typing import Optional
from usa_signal_bot.release.release_models import ReleaseVersion

logger = logging.getLogger(__name__)


def get_git_commit_safe(project_root: Optional[Path] = None) -> Optional[str]:
    try:
        cwd = project_root if project_root else Path.cwd()
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=2,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        logger.warning("Failed to get git commit: %s", e)
    return None


def get_git_branch_safe(project_root: Optional[Path] = None) -> Optional[str]:
    try:
        cwd = project_root if project_root else Path.cwd()
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=2,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        logger.warning("Failed to get git branch: %s", e)
    return None


def get_project_version(default: str = "0.0.0-local") -> str:
    # Future improvement: read from pyproject.toml or setup.py if available
    return default


def create_build_id(version: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"build_{version.replace('.', '_')}_{timestamp}"


def build_release_version(
    version: Optional[str] = None, project_root: Optional[Path] = None
) -> ReleaseVersion:
    ver = version if version else get_project_version()
    return ReleaseVersion(
        version=ver,
        build_id=create_build_id(ver),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        git_commit=get_git_commit_safe(project_root),
        git_branch=get_git_branch_safe(project_root),
        python_version=platform.python_version(),
        platform=platform.platform(),
    )


def normalize_version_string(version: str) -> str:
    return version.strip().lower()


def version_to_text(version: ReleaseVersion) -> str:
    lines = [
        f"Version: {version.version}",
        f"Build ID: {version.build_id}",
        f"Created At (UTC): {version.created_at_utc}",
        f"Git Commit: {version.git_commit or 'Unknown'}",
        f"Git Branch: {version.git_branch or 'Unknown'}",
        f"Python Version: {version.python_version or 'Unknown'}",
        f"Platform: {version.platform or 'Unknown'}",
    ]
    return "\n".join(lines)
