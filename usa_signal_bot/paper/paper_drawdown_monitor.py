from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from usa_signal_bot.paper.paper_models import PaperEquitySnapshot
from usa_signal_bot.core.enums import PaperDrawdownStatus
from usa_signal_bot.paper.paper_equity_analytics import calculate_paper_drawdown_series, extract_equity_values

@dataclass
class PaperDrawdownThresholds:
    warning_drawdown_pct: float
    breach_drawdown_pct: float
    critical_drawdown_pct: float
    current_drawdown_warning_pct: float

@dataclass
class PaperDrawdownEvent:
    event_id: str
    timestamp_utc: str
    status: PaperDrawdownStatus
    drawdown_pct: float
    threshold_pct: float
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperDrawdownReport:
    report_id: str
    created_at_utc: str
    status: PaperDrawdownStatus
    current_drawdown_pct: Optional[float]
    max_drawdown_pct: Optional[float]
    events: List[PaperDrawdownEvent]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def default_paper_drawdown_thresholds() -> PaperDrawdownThresholds:
    return PaperDrawdownThresholds(
        warning_drawdown_pct=5.0,
        breach_drawdown_pct=10.0,
        critical_drawdown_pct=20.0,
        current_drawdown_warning_pct=5.0
    )

def validate_paper_drawdown_thresholds(thresholds: PaperDrawdownThresholds) -> None:
    if not (thresholds.warning_drawdown_pct < thresholds.breach_drawdown_pct < thresholds.critical_drawdown_pct):
        raise ValueError("Drawdown thresholds must be ordered: warning < breach < critical")
    if any(t < 0 for t in [thresholds.warning_drawdown_pct, thresholds.breach_drawdown_pct, thresholds.critical_drawdown_pct, thresholds.current_drawdown_warning_pct]):
         raise ValueError("Drawdown thresholds cannot be negative")

def classify_paper_drawdown(drawdown_pct: Optional[float], thresholds: PaperDrawdownThresholds) -> PaperDrawdownStatus:
    if drawdown_pct is None:
        return PaperDrawdownStatus.UNKNOWN
    if drawdown_pct >= thresholds.critical_drawdown_pct:
        return PaperDrawdownStatus.CRITICAL
    if drawdown_pct >= thresholds.breach_drawdown_pct:
        return PaperDrawdownStatus.BREACH
    if drawdown_pct >= thresholds.warning_drawdown_pct:
        return PaperDrawdownStatus.WARNING
    return PaperDrawdownStatus.NORMAL

def build_paper_drawdown_events(snapshots: List[PaperEquitySnapshot], thresholds: PaperDrawdownThresholds) -> List[PaperDrawdownEvent]:
    events = []
    if not snapshots:
        return events
    values = extract_equity_values(snapshots)
    series = calculate_paper_drawdown_series(values)

    current_status = PaperDrawdownStatus.NORMAL

    for idx, item in enumerate(series):
        dd_pct = item["drawdown_pct"]
        status = classify_paper_drawdown(dd_pct, thresholds)

        if status != current_status and status != PaperDrawdownStatus.NORMAL:
            threshold = 0.0
            if status == PaperDrawdownStatus.WARNING: threshold = thresholds.warning_drawdown_pct
            elif status == PaperDrawdownStatus.BREACH: threshold = thresholds.breach_drawdown_pct
            elif status == PaperDrawdownStatus.CRITICAL: threshold = thresholds.critical_drawdown_pct

            events.append(PaperDrawdownEvent(
                event_id=f"dd_event_{idx}_{datetime.now(timezone.utc).timestamp()}",
                timestamp_utc=snapshots[idx].timestamp_utc,
                status=status,
                drawdown_pct=dd_pct,
                threshold_pct=threshold,
                message=f"Drawdown {status.value}: {dd_pct:.2f}% >= {threshold:.2f}%"
            ))
            current_status = status
        elif status == PaperDrawdownStatus.NORMAL and current_status != PaperDrawdownStatus.NORMAL:
            current_status = PaperDrawdownStatus.NORMAL

    return events

def monitor_paper_drawdown(snapshots: List[PaperEquitySnapshot], thresholds: Optional[PaperDrawdownThresholds] = None) -> PaperDrawdownReport:
    if thresholds is None:
        thresholds = default_paper_drawdown_thresholds()
    validate_paper_drawdown_thresholds(thresholds)

    if not snapshots:
        return PaperDrawdownReport(
            report_id=f"dd_report_{datetime.now(timezone.utc).timestamp()}",
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=PaperDrawdownStatus.INSUFFICIENT_DATA,
            current_drawdown_pct=None,
            max_drawdown_pct=None,
            events=[],
            warnings=["No equity snapshots provided."],
            errors=[]
        )

    values = extract_equity_values(snapshots)
    series = calculate_paper_drawdown_series(values)

    current_dd_pct = series[-1]["drawdown_pct"]
    max_dd_pct = max([item["drawdown_pct"] for item in series])

    # Status is based on current drawdown for warning if it exceeds current_warning
    # and max drawdown for overall severity.
    status = classify_paper_drawdown(current_dd_pct, thresholds)

    events = build_paper_drawdown_events(snapshots, thresholds)

    return PaperDrawdownReport(
        report_id=f"dd_report_{datetime.now(timezone.utc).timestamp()}",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        current_drawdown_pct=current_dd_pct,
        max_drawdown_pct=max_dd_pct,
        events=events,
        warnings=[],
        errors=[]
    )

def paper_drawdown_event_to_dict(event: PaperDrawdownEvent) -> Dict[str, Any]:
    return {
        "event_id": event.event_id,
        "timestamp_utc": event.timestamp_utc,
        "status": event.status.value,
        "drawdown_pct": event.drawdown_pct,
        "threshold_pct": event.threshold_pct,
        "message": event.message,
        "metadata": event.metadata
    }

def paper_drawdown_report_to_dict(report: PaperDrawdownReport) -> Dict[str, Any]:
    return {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "status": report.status.value,
        "current_drawdown_pct": report.current_drawdown_pct,
        "max_drawdown_pct": report.max_drawdown_pct,
        "events": [paper_drawdown_event_to_dict(e) for e in report.events],
        "warnings": report.warnings,
        "errors": report.errors
    }

def paper_drawdown_report_to_text(report: PaperDrawdownReport) -> str:
    lines = [
        "--- Paper Drawdown Report ---",
        f"Status: {report.status.value}",
    ]
    if report.current_drawdown_pct is not None:
         lines.append(f"Current Drawdown %: {report.current_drawdown_pct:.2f}%")
    if report.max_drawdown_pct is not None:
         lines.append(f"Max Drawdown %: {report.max_drawdown_pct:.2f}%")

    if report.events:
        lines.append("\nEvents:")
        for event in report.events:
            lines.append(f"- [{event.timestamp_utc}] {event.status.value}: {event.drawdown_pct:.2f}% (Threshold: {event.threshold_pct:.2f}%)")

    if report.warnings:
        lines.append("\nWarnings: " + ", ".join(report.warnings))
    if report.errors:
        lines.append("\nErrors: " + ", ".join(report.errors))

    lines.append("")
    return "\n".join(lines)
