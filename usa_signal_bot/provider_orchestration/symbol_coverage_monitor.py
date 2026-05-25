from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import DataAvailabilityStatus
from usa_signal_bot.provider_orchestration.phase110_models import (
    DataAvailabilityItem, DataAvailabilityReport, create_data_availability_report_id,
    validate_data_availability_report
)

def monitor_symbol_coverage(symbols: list[str], capability: str = "GET_DAILY_OHLCV", availability_items: list[DataAvailabilityItem] | None = None) -> DataAvailabilityReport:
    items = availability_items or []

    available_count = sum(1 for i in items if i.status == DataAvailabilityStatus.AVAILABLE)
    partial_count = sum(1 for i in items if i.status == DataAvailabilityStatus.PARTIALLY_AVAILABLE)
    stale_count = sum(1 for i in items if i.status == DataAvailabilityStatus.STALE_AVAILABLE)
    missing_count = sum(1 for i in items if i.status == DataAvailabilityStatus.MISSING)
    insufficient_quality_count = sum(1 for i in items if i.status == DataAvailabilityStatus.INSUFFICIENT_QUALITY)

    total = len(symbols)
    ratio = available_count / total if total > 0 else 0.0

    rep = DataAvailabilityReport(
        availability_report_id=create_data_availability_report_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        items=items,
        total_items=len(items),
        available_count=available_count,
        partial_count=partial_count,
        stale_count=stale_count,
        missing_count=missing_count,
        insufficient_quality_count=insufficient_quality_count,
        coverage_ratio=ratio,
        availability_ready=True,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )
    validate_data_availability_report(rep)
    return rep

def coverage_ratio(items: list[DataAvailabilityItem]) -> float:
    if not items: return 0.0
    avail = sum(1 for i in items if i.status == DataAvailabilityStatus.AVAILABLE)
    return avail / len(items)

def symbols_missing_coverage(symbols: list[str], items: list[DataAvailabilityItem]) -> list[str]:
    covered = {i.symbol for i in items if i.status in (DataAvailabilityStatus.AVAILABLE, DataAvailabilityStatus.PARTIALLY_AVAILABLE, DataAvailabilityStatus.STALE_AVAILABLE)}
    return [sym for sym in symbols if sym not in covered]

def symbol_coverage_monitor_to_text(report: DataAvailabilityReport, limit: int = 200) -> str:
    lines = [
        f"--- Symbol Coverage Report ---",
        f"ID: {report.availability_report_id}",
        f"Total Symbols: {report.total_items}",
        f"Available: {report.available_count}",
        f"Missing: {report.missing_count}",
        f"Coverage Ratio: {report.coverage_ratio:.2f}"
    ]
    return "\n".join(lines)
