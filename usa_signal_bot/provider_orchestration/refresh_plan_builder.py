from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import DataAvailabilityStatus, RefreshPlanStatus, RefreshPriority
from usa_signal_bot.provider_orchestration.phase110_models import (
    DataAvailabilityItem, DataAvailabilityReport, RefreshPlanItem, RefreshPlanReport,
    create_refresh_plan_item_id, create_refresh_plan_report_id, validate_refresh_plan_report
)
from usa_signal_bot.provider_orchestration.refresh_priority_scorer import score_refresh_priority, refresh_reason

def build_refresh_plan_item(item: DataAvailabilityItem) -> RefreshPlanItem:
    priority = score_refresh_priority(item)
    status = RefreshPlanStatus.PLANNED_FUTURE_REFRESH if priority != RefreshPriority.NONE else RefreshPlanStatus.NOT_REQUIRED

    return RefreshPlanItem(
        refresh_item_id=create_refresh_plan_item_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        symbol=item.symbol,
        capability=item.capability,
        interval=item.interval,
        provider_name=item.provider_name,
        status=status,
        priority=priority,
        reason=refresh_reason(item),
        stale=item.status == DataAvailabilityStatus.STALE_AVAILABLE,
        missing=item.status == DataAvailabilityStatus.MISSING,
        low_quality=item.status == DataAvailabilityStatus.INSUFFICIENT_QUALITY,
        source_disagreement=False,
        refresh_required_future=priority != RefreshPriority.NONE,
        dry_run_only=True,
        network_allowed_now=False,
        paid_api_allowed=False,
        scraping_allowed=False,
        html_parsing_allowed=False,
        broker_allowed=False,
        order_allowed=False,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def build_refresh_plan_report(availability_report: DataAvailabilityReport) -> RefreshPlanReport:
    items = [build_refresh_plan_item(i) for i in availability_report.items]

    refresh_required = sum(1 for i in items if i.refresh_required_future)
    high_priority = sum(1 for i in items if i.priority in (RefreshPriority.CRITICAL, RefreshPriority.HIGH))
    blocked = sum(1 for i in items if i.status == RefreshPlanStatus.BLOCKED)

    rep = RefreshPlanReport(
        refresh_report_id=create_refresh_plan_report_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        items=items,
        total_items=len(items),
        refresh_required_count=refresh_required,
        high_priority_count=high_priority,
        blocked_count=blocked,
        dry_run_only=True,
        network_allowed_now=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )
    validate_refresh_plan_report(rep)
    return rep

def refresh_plan_summary(report: RefreshPlanReport) -> dict[str, Any]:
    return {
        "total": report.total_items,
        "requires_refresh": report.refresh_required_count,
        "high_priority": report.high_priority_count
    }

def refresh_plan_to_text(report: RefreshPlanReport, limit: int = 200) -> str:
    lines = [
        f"--- Refresh Plan ---",
        f"ID: {report.refresh_report_id}",
        f"Requires Refresh: {report.refresh_required_count}",
        f"High Priority: {report.high_priority_count}"
    ]
    return "\n".join(lines)
