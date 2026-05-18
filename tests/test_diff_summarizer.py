import pytest
from usa_signal_bot.core.enums import MetricDeltaDirection
from usa_signal_bot.research_execution.execution_models import MetricComparison
from usa_signal_bot.research_execution.diff_summarizer import summarize_metric_deltas

def test_summarize_metric_deltas():
    c1 = MetricComparison("c1", "m1", 10, 20, 10, 100, MetricDeltaDirection.IMPROVED, "imp", [], [], {})
    c2 = MetricComparison("c2", "m2", 20, 10, -10, -50, MetricDeltaDirection.WORSENED, "wor", [], [], {})
    summ = summarize_metric_deltas([c1, c2])
    assert summ["total"] == 2
