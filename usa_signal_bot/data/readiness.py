from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path
from ..core.domain import BaseDomainModel
from ..core.enums import DataReadinessStatus, DataCoverageStatus
from .coverage import DataCoverageReport
from .timeframes import is_intraday_timeframe
import json
import datetime

@dataclass
class DataReadinessCriteria(BaseDomainModel):
    min_ready_pair_ratio: float = 0.70
    min_symbol_coverage_ratio: float = 0.70
    require_primary_timeframe: bool = True
    allow_partial_intraday: bool = True
    max_error_count: int = 0
    max_warning_ratio: float = 0.30

@dataclass
class DataReadinessItem(BaseDomainModel):
    symbol: str = ""
    timeframe: str = ""
    ready: bool = False
    status: DataReadinessStatus = DataReadinessStatus.UNKNOWN
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)

@dataclass
class DataReadinessReport(BaseDomainModel):
    report_id: str = ""
    created_at_utc: str = ""
    provider_name: str = ""
    symbols: list[str] = field(default_factory=list)
    timeframes: list[str] = field(default_factory=list)
    overall_status: DataReadinessStatus = DataReadinessStatus.UNKNOWN
    readiness_score: float = 0.0
    ready_items: int = 0
    partial_items: int = 0
    failed_items: int = 0
    items: list[DataReadinessItem] = field(default_factory=list)
    blocking_reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

def default_readiness_criteria() -> DataReadinessCriteria:
    return DataReadinessCriteria()

def evaluate_readiness_from_coverage(
    coverage_report: DataCoverageReport,
    criteria: Optional[DataReadinessCriteria] = None
) -> DataReadinessReport:
    import uuid
    if criteria is None:
        criteria = default_readiness_criteria()

    report = DataReadinessReport(
        report_id=str(uuid.uuid4()),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        provider_name=coverage_report.provider_name,
        symbols=coverage_report.symbols,
        timeframes=coverage_report.timeframes
    )

    primary_tf = coverage_report.timeframes[0] if coverage_report.timeframes else "1d"
    primary_failed = False
    total_score = 0.0

    for cov in coverage_report.coverages:
        item = DataReadinessItem(symbol=cov.symbol, timeframe=cov.timeframe)

        # Scoring logic
        item.score = cov.coverage_ratio * 100.0

        if cov.status == DataCoverageStatus.COMPLETE:
            item.ready = True
            item.status = DataReadinessStatus.READY
        elif cov.status == DataCoverageStatus.PARTIAL:
            if is_intraday_timeframe(cov.timeframe) and criteria.allow_partial_intraday:
                item.ready = True # Allowed to be partial
                item.status = DataReadinessStatus.PARTIAL
                item.reasons.append("Partial intraday allowed")
            else:
                item.ready = False
                item.status = DataReadinessStatus.PARTIAL
                item.reasons.append("Partial coverage not allowed for this timeframe")
        else:
            item.ready = False
            item.status = DataReadinessStatus.NOT_READY
            item.reasons.append(f"Coverage status is {cov.status.value}")

        if not item.ready and cov.timeframe == primary_tf and criteria.require_primary_timeframe:
            primary_failed = True
            report.blocking_reasons.append(f"Primary timeframe {primary_tf} failed for {cov.symbol}")

        if item.status == DataReadinessStatus.READY:
            report.ready_items += 1
        elif item.status == DataReadinessStatus.PARTIAL:
            report.partial_items += 1
        else:
            report.failed_items += 1

        total_score += item.score
        report.items.append(item)

    total_items = len(report.items)
    if total_items > 0:
        report.readiness_score = total_score / total_items
        ready_ratio = report.ready_items / total_items

        if primary_failed:
            report.overall_status = DataReadinessStatus.NOT_READY
        elif ready_ratio >= criteria.min_ready_pair_ratio:
            report.overall_status = DataReadinessStatus.READY
        elif ready_ratio + (report.partial_items/total_items) >= criteria.min_ready_pair_ratio:
            report.overall_status = DataReadinessStatus.PARTIAL
        else:
            report.overall_status = DataReadinessStatus.NOT_READY
            report.blocking_reasons.append(f"Ready ratio {ready_ratio:.2f} below minimum {criteria.min_ready_pair_ratio}")
    else:
        report.overall_status = DataReadinessStatus.NOT_READY
        report.blocking_reasons.append("No data to evaluate")

    return report

def readiness_report_to_text(report: DataReadinessReport) -> str:
    lines = [
        f"Data Readiness Report: {report.report_id}",
        f"Created: {report.created_at_utc}",
        f"Overall Status: {report.overall_status.value} (Score: {report.readiness_score:.1f}/100)",
        f"Items: {report.ready_items} ready, {report.partial_items} partial, {report.failed_items} failed",
    ]
    if report.blocking_reasons:
        lines.append("Blocking Reasons:")
        for r in report.blocking_reasons:
            lines.append(f"  - {r}")

    lines.append("---")
    for item in report.items:
        r_str = f" [{', '.join(item.reasons)}]" if item.reasons else ""
        lines.append(f"{item.symbol} ({item.timeframe}): {item.status.value} (Score: {item.score:.1f}){r_str}")
    return "\n".join(lines)

def readiness_report_to_dict(report: DataReadinessReport) -> dict:
    from ..core.serialization import dataclass_to_dict
    return dataclass_to_dict(report)

def write_readiness_report_json(path: Path, report: DataReadinessReport) -> Path:
    with open(path, 'w') as f:
        json.dump(readiness_report_to_dict(report), f, indent=2)
    return path

def assert_data_ready(report: DataReadinessReport) -> None:
    from ..core.exceptions import DataReadinessError
    if report.overall_status in [DataReadinessStatus.NOT_READY, DataReadinessStatus.FAILED]:
        raise DataReadinessError(f"Data is not ready. Status: {report.overall_status.value}. Blocking reasons: {report.blocking_reasons}")

def readiness_items_by_symbol(report: DataReadinessReport) -> dict[str, list[DataReadinessItem]]:
    result = {}
    for item in report.items:
        if item.symbol not in result:
            result[item.symbol] = []
        result[item.symbol].append(item)
    return result

def symbol_readiness_score(report: DataReadinessReport, symbol: str) -> float:
    items = [i for i in report.items if i.symbol == symbol]
    if not items:
        return 0.0

    ready_count = sum(1 for i in items if i.status == DataReadinessStatus.READY)
    return (ready_count / len(items)) * 100.0

def symbol_ready_timeframes(report: DataReadinessReport, symbol: str) -> list[str]:
    return [i.timeframe for i in report.items if i.symbol == symbol and i.status == DataReadinessStatus.READY]

def symbol_missing_or_failed_timeframes(report: DataReadinessReport, symbol: str) -> tuple[list[str], list[str]]:
    items = [i for i in report.items if i.symbol == symbol]
    missing = [i.timeframe for i in items if i.status in (DataReadinessStatus.NOT_READY, DataReadinessStatus.UNKNOWN)]
    failed = [i.timeframe for i in items if i.status == DataReadinessStatus.FAILED]
    return missing, failed
