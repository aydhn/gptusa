
from usa_signal_bot.diagnostics.diagnostic_models import DiagnosticEvent
from usa_signal_bot.core.enums import DiagnosticScope
from usa_signal_bot.diagnostics.loss_event_analysis import filter_losing_events, loss_summary

def test_filter_losing_events():
    events = [
        DiagnosticEvent("1", DiagnosticScope.TRADE, net_pnl_usd=100.0),
        DiagnosticEvent("2", DiagnosticScope.TRADE, net_pnl_usd=-50.0),
        DiagnosticEvent("3", DiagnosticScope.TRADE, net_pnl_usd=0.0),
        DiagnosticEvent("4", DiagnosticScope.TRADE, net_pnl_usd=-10.0),
    ]
    losers = filter_losing_events(events)
    assert len(losers) == 2
    assert losers[0].event_id == "2"

def test_loss_summary():
    events = [
        DiagnosticEvent("1", DiagnosticScope.TRADE, net_pnl_usd=100.0),
        DiagnosticEvent("2", DiagnosticScope.TRADE, net_pnl_usd=-50.0),
    ]
    summary = loss_summary(events)
    assert summary["total_events"] == 2
    assert summary["loss_count"] == 1
    assert summary["total_net_loss_usd"] == -50.0
