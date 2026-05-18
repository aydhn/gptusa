import pytest
from usa_signal_bot.research_execution.diagnostics_delta import build_diagnostics_delta, compare_diagnostic_scorecards

def test_compare_diagnostic_scorecards():
    b = {"health": 90, "stability": 80}
    c = {"health": 95, "stability": 80}
    delta = compare_diagnostic_scorecards(b, c)
    assert delta["health"] == 5
    assert delta["stability"] == 0

def test_build_diagnostics_delta_missing_payload():
    delta = build_diagnostics_delta(None, None)
    assert "warning" in delta
