from typing import Any
from usa_signal_bot.core.enums import DataAvailabilityStatus, RefreshPriority
from usa_signal_bot.provider_orchestration.phase110_models import DataAvailabilityItem

def score_refresh_priority(item: DataAvailabilityItem) -> RefreshPriority:
    if item.status == DataAvailabilityStatus.MISSING:
        return RefreshPriority.CRITICAL
    if item.status == DataAvailabilityStatus.INSUFFICIENT_QUALITY:
        return RefreshPriority.HIGH
    if item.status == DataAvailabilityStatus.PARTIALLY_AVAILABLE:
        return RefreshPriority.HIGH
    if item.status == DataAvailabilityStatus.STALE_AVAILABLE:
        return RefreshPriority.MEDIUM
    return RefreshPriority.NONE

def refresh_priority_score(item: DataAvailabilityItem) -> float:
    priority = score_refresh_priority(item)
    if priority == RefreshPriority.CRITICAL: return 1.0
    if priority == RefreshPriority.HIGH: return 0.8
    if priority == RefreshPriority.MEDIUM: return 0.5
    if priority == RefreshPriority.LOW: return 0.2
    return 0.0

def refresh_reason(item: DataAvailabilityItem) -> str:
    if item.status == DataAvailabilityStatus.MISSING: return "Data missing"
    if item.status == DataAvailabilityStatus.INSUFFICIENT_QUALITY: return "Low quality data"
    if item.status == DataAvailabilityStatus.PARTIALLY_AVAILABLE: return "Partial coverage"
    if item.status == DataAvailabilityStatus.STALE_AVAILABLE: return "Stale data"
    return "Fresh"

def refresh_priority_scorer_summary(items: list[DataAvailabilityItem]) -> dict[str, Any]:
    critical = sum(1 for i in items if score_refresh_priority(i) == RefreshPriority.CRITICAL)
    high = sum(1 for i in items if score_refresh_priority(i) == RefreshPriority.HIGH)
    medium = sum(1 for i in items if score_refresh_priority(i) == RefreshPriority.MEDIUM)
    none = sum(1 for i in items if score_refresh_priority(i) == RefreshPriority.NONE)
    return {"CRITICAL": critical, "HIGH": high, "MEDIUM": medium, "NONE": none}

def refresh_priority_scorer_to_text(items: list[DataAvailabilityItem], limit: int = 100) -> str:
    lines = ["--- Refresh Priorities ---"]
    for i in items[:limit]:
        lines.append(f"{i.symbol}: {score_refresh_priority(i).value}")
    return "\n".join(lines)
