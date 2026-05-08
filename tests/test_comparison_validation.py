import pytest
from usa_signal_bot.comparison.comparison_validation import (
    validate_comparison_run_request_report, validate_no_execution_in_comparison,
    validate_no_investment_advice_language_in_comparison, ComparisonRunRequest
)
from usa_signal_bot.core.enums import ComparisonReportType, ComparisonStatus, ExecutionRealismBucket, GapSeverity
from usa_signal_bot.comparison.comparison_models import ComparisonRunResult

def test_validate_request():
    req = ComparisonRunRequest("req1", ComparisonReportType.FULL_COMPARISON, paper_run_id="p1", backtest_run_id="b1")
    rep = validate_comparison_run_request_report(req)
    assert rep.valid
    assert rep.error_count == 0

    req_invalid = ComparisonRunRequest("req2", ComparisonReportType.FULL_COMPARISON)
    rep2 = validate_comparison_run_request_report(req_invalid)
    assert not rep2.valid
    assert rep2.error_count > 0

def test_execution_guard():
    res = ComparisonRunResult("run1", "now", ComparisonStatus.EMPTY, ComparisonRunRequest("req1", ComparisonReportType.FULL_COMPARISON), None, None, None, [], None, None, None, ExecutionRealismBucket.UNKNOWN, GapSeverity.UNKNOWN, {}, [], [])

    # Valid
    rep = validate_no_execution_in_comparison(res)
    assert rep.valid

    # Invalid (contains forbidden key)
    res.output_paths["broker_order"] = "test"
    rep2 = validate_no_execution_in_comparison(res)
    assert not rep2.valid

def test_advice_guard():
    assert validate_no_investment_advice_language_in_comparison("Just a report.").valid
    assert not validate_no_investment_advice_language_in_comparison("Kesin al bunu.").valid
