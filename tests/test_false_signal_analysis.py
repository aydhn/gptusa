
from usa_signal_bot.diagnostics.diagnostic_models import DiagnosticEvent
from usa_signal_bot.core.enums import DiagnosticScope
from usa_signal_bot.diagnostics.false_signal_analysis import identify_false_positive_events

def test_identify_false_positive_events():
    events = [
        DiagnosticEvent("1", DiagnosticScope.SIGNAL, signal_score=80.0, net_pnl_usd=-100.0), # False positive
        DiagnosticEvent("2", DiagnosticScope.SIGNAL, signal_score=80.0, net_pnl_usd=100.0),  # True positive
        DiagnosticEvent("3", DiagnosticScope.SIGNAL, signal_score=40.0, net_pnl_usd=-100.0), # True negative
    ]
    fp = identify_false_positive_events(events, min_signal_score=70.0)
    assert len(fp) == 1
    assert fp[0].event_id == "1"
