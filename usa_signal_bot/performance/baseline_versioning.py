from datetime import datetime, timezone
import uuid
from typing import Dict, Any, Optional

from usa_signal_bot.core.enums import BaselineStatus
from usa_signal_bot.performance.baseline_models import PerformanceBaseline

def create_baseline_version(prefix: str = "baseline") -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{prefix}_v_{timestamp}_{uuid.uuid4().hex[:6]}"

def parse_baseline_version(version: str) -> Dict[str, Any]:
    parts = version.split("_")
    return {
        "original": version,
        "prefix": parts[0] if parts else "unknown",
        "parsed_timestamp": parts[2] if len(parts) > 2 else None,
        "uuid_short": parts[3] if len(parts) > 3 else None
    }

def supersede_baseline(old: PerformanceBaseline, new: PerformanceBaseline) -> PerformanceBaseline:
    # return the mutated old baseline, we don't delete but mark it superseded
    old.status = BaselineStatus.SUPERSEDED
    old.metadata["superseded_by"] = new.baseline_id
    old.metadata["superseded_at"] = datetime.now(timezone.utc).isoformat()
    return old

def mark_baseline_stale(baseline: PerformanceBaseline, reason: Optional[str] = None) -> PerformanceBaseline:
    baseline.status = BaselineStatus.STALE
    baseline.metadata["stale_reason"] = reason or "Time decay threshold reached"
    baseline.metadata["stale_at"] = datetime.now(timezone.utc).isoformat()
    return baseline

def baseline_version_to_text(version: str) -> str:
    parsed = parse_baseline_version(version)
    return f"Version: {version} (Generated: {parsed['parsed_timestamp']})"
