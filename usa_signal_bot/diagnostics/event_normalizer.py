from typing import Any, Optional
from .diagnostic_models import DiagnosticEvent, create_diagnostic_event_id
from usa_signal_bot.core.enums import DiagnosticScope

def normalize_diagnostic_event(payload: dict[str, Any], scope: Optional[DiagnosticScope] = None) -> DiagnosticEvent:
    if scope is None: scope = DiagnosticScope.UNKNOWN
    return DiagnosticEvent(event_id=create_diagnostic_event_id(), scope=scope, net_pnl_usd=payload.get("net_pnl_usd"))

def diagnostic_events_from_backtest_result(result: dict[str, Any]) -> list[DiagnosticEvent]:
    return [normalize_diagnostic_event(t, DiagnosticScope.TRADE) for t in result.get("trades", [])]
