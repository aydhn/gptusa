
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import CalendarValidationStatus
from usa_signal_bot.event_impact.phase112_models import CalendarAwareValidationResult, CalendarAwareAnomaly, create_calendar_aware_validation_id, _now
from usa_signal_bot.event_impact.calendar_gap_validator import detect_calendar_gaps
from usa_signal_bot.event_impact.calendar_price_jump_validator import detect_calendar_price_jumps
from usa_signal_bot.event_impact.calendar_volume_anomaly_validator import detect_calendar_volume_anomalies
from usa_signal_bot.event_impact.calendar_timestamp_validator import detect_calendar_timestamp_issues

def calendar_validation_status_from_anomalies(anomalies: List[CalendarAwareAnomaly]) -> CalendarValidationStatus:
    if not anomalies:
        return CalendarValidationStatus.PASS
    if any(not a.explained_by_event for a in anomalies):
        return CalendarValidationStatus.WARNING_UNEXPLAINED
    return CalendarValidationStatus.WARNING_EXPLAINED_BY_EVENT

def run_calendar_aware_validation(symbol: str, records: List[Dict[str, Any]], events: Optional[List[Dict[str, Any]]] = None) -> CalendarAwareValidationResult:
    evs = events or []

    gaps = detect_calendar_gaps(records, evs, symbol)
    jumps = detect_calendar_price_jumps(records, evs, symbol)
    vols = detect_calendar_volume_anomalies(records, evs, symbol)
    times = detect_calendar_timestamp_issues(records, evs, symbol)

    all_anomalies = gaps + jumps + vols + times
    status = calendar_validation_status_from_anomalies(all_anomalies)

    return CalendarAwareValidationResult(
        validation_id=create_calendar_aware_validation_id(),
        created_at_utc=_now(),
        symbol=symbol,
        status=status,
        anomalies=all_anomalies,
        explained_anomaly_count=sum(1 for a in all_anomalies if a.explained_by_event),
        unexplained_anomaly_count=sum(1 for a in all_anomalies if not a.explained_by_event),
        schema_error_count=0,
        timestamp_error_count=len(times),
        event_context_used=len(evs) > 0,
        research_context_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False
    )

def run_calendar_aware_validation_batch(symbol_records: Dict[str, List[Dict[str, Any]]], events: Optional[List[Dict[str, Any]]] = None) -> List[CalendarAwareValidationResult]:
    return [run_calendar_aware_validation(sym, recs, events) for sym, recs in symbol_records.items()]

def calendar_aware_validation_summary(results: List[CalendarAwareValidationResult]) -> Dict[str, Any]:
    return {"total": len(results)}

def calendar_aware_validation_to_text(results: List[CalendarAwareValidationResult], limit: int = 200) -> str:
    return f"Validated {len(results)} symbols."
