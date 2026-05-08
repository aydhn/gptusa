from dataclasses import dataclass, field
from typing import List, Dict, Any
import datetime
import uuid
from usa_signal_bot.core.enums import OperationalMetricStatus

@dataclass
class ErrorTrendSummary:
    summary_id: str
    created_at_utc: str
    window_hours: int
    warning_count: int
    error_count: int
    critical_count: int
    top_sources: List[Dict[str, Any]]
    top_messages: List[Dict[str, Any]]
    status: OperationalMetricStatus
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def filter_events_by_window(events: List[Dict[str, Any]], window_hours: int) -> List[Dict[str, Any]]:
    now = datetime.datetime.now(datetime.timezone.utc)
    res = []
    for e in events:
        ts_str = e.get("timestamp_utc", "")
        if not ts_str: continue
        try:
            ts = datetime.datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            if not ts.tzinfo: ts = ts.replace(tzinfo=datetime.timezone.utc)
            if (now - ts).total_seconds() <= window_hours * 3600:
                res.append(e)
        except Exception:
            pass
    return res

def count_events_by_severity(events: List[Dict[str, Any]]) -> Dict[str, int]:
    counts = {"WARNING": 0, "ERROR": 0, "CRITICAL": 0}
    for e in events:
        sev = e.get("severity", "").upper()
        if sev in counts:
            counts[sev] += 1
    return counts

def top_event_sources(events: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
    counts = {}
    for e in events:
        s = e.get("source", "unknown")
        sev = e.get("severity", "").upper()
        if sev in ["WARNING", "ERROR", "CRITICAL"]:
            counts[s] = counts.get(s, 0) + 1
    sorted_s = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return [{"source": k, "count": v} for k, v in sorted_s[:limit]]

def top_event_messages(events: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
    counts = {}
    for e in events:
        s = e.get("message", "unknown")
        sev = e.get("severity", "").upper()
        if sev in ["WARNING", "ERROR", "CRITICAL"]:
            counts[s] = counts.get(s, 0) + 1
    sorted_s = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return [{"message": k, "count": v} for k, v in sorted_s[:limit]]

def build_error_trend_summary(events: List[Dict[str, Any]], window_hours: int = 24) -> ErrorTrendSummary:
    windowed = filter_events_by_window(events, window_hours)
    counts = count_events_by_severity(windowed)

    st = OperationalMetricStatus.OK
    if counts["CRITICAL"] > 0 or counts["ERROR"] > 20:
        st = OperationalMetricStatus.CRITICAL
    elif counts["ERROR"] > 5 or counts["WARNING"] > 20:
        st = OperationalMetricStatus.WARNING

    return ErrorTrendSummary(
        summary_id=f"err_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        window_hours=window_hours,
        warning_count=counts.get("WARNING", 0),
        error_count=counts.get("ERROR", 0),
        critical_count=counts.get("CRITICAL", 0),
        top_sources=top_event_sources(windowed),
        top_messages=top_event_messages(windowed),
        status=st
    )

def error_trend_summary_to_dict(summary: ErrorTrendSummary) -> dict:
    from dataclasses import asdict
    return asdict(summary)

def error_trend_summary_to_text(summary: ErrorTrendSummary) -> str:
    lines = [
        f"--- Error Trend Summary ({summary.window_hours}h) ---",
        f"Status: {summary.status.value}",
        f"Warnings: {summary.warning_count} | Errors: {summary.error_count} | Critical: {summary.critical_count}",
        "Top Sources:"
    ]
    for s in summary.top_sources: lines.append(f"  - {s['source']}: {s['count']}")
    lines.append("Top Messages:")
    for s in summary.top_messages: lines.append(f"  - {s['message'][:50]}... : {s['count']}")
    return "\n".join(lines)
