import pytest
from usa_signal_bot.core.enums import MetricDeltaDirection, ComparisonOutcome, ResearchRunType, ResearchRunStatus, ExperimentExecutionMode
from usa_signal_bot.research_execution.execution_models import ResearchRun
from usa_signal_bot.research_execution.result_comparator import compare_metric, determine_comparison_outcome, compare_research_runs

def test_determine_comparison_outcome_candidate_better():
    mc1 = compare_metric("a", 10, 20, True)
    mc2 = compare_metric("b", 10, 20, True)
    mc3 = compare_metric("drawdown", 20, 21, False)
    outcome = determine_comparison_outcome([mc1, mc2, mc3])
    assert outcome == ComparisonOutcome.CANDIDATE_BETTER
