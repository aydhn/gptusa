import pytest
from usa_signal_bot.research_execution.attribution_delta import build_attribution_delta, compare_attribution_scorecards

def test_compare_attribution_scorecards():
    b = {"alpha": 10, "beta": 5}
    c = {"alpha": 12, "beta": 4}
    delta = compare_attribution_scorecards(b, c)
    assert delta["alpha"] == 2
    assert delta["beta"] == -1

def test_build_attribution_delta_missing_payload():
    delta = build_attribution_delta(None, None)
    assert "warning" in delta
