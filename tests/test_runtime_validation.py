import pytest
from usa_signal_bot.runtime.runtime_validation import (
    validate_market_scan_request_report, validate_market_scan_result,
    validate_runtime_state, validate_pipeline_step_results,
    validate_no_live_execution_in_scan, validate_scheduled_scan_plan_report,
    assert_runtime_valid
)
from usa_signal_bot.runtime.runtime_models import MarketScanResult, MarketScanRequest, RuntimeState, PipelineStepResult, ScheduledScanPlan
from usa_signal_bot.core.enums import RuntimeMode, ScanScope, RuntimeRunStatus, PipelineStepName, PipelineStepStatus
from usa_signal_bot.core.exceptions import RuntimeValidationError

def test_runtime_validation():
    req = MarketScanRequest(run_name="t", mode=RuntimeMode.DRY_RUN, scope=ScanScope.SMALL_TEST_SET)
    assert validate_market_scan_request_report(req).valid is True

    req_inv = MarketScanRequest(run_name="", mode=RuntimeMode.DRY_RUN, scope=ScanScope.SMALL_TEST_SET)
    assert validate_market_scan_request_report(req_inv).valid is False

    res = MarketScanResult(run_id="run1", created_at_utc="", request=req, status=RuntimeRunStatus.COMPLETED)
    assert validate_market_scan_result(res).valid is True

    # Check no live execution
    req_live = MarketScanRequest(run_name="t", mode=RuntimeMode.DRY_RUN, scope=ScanScope.SMALL_TEST_SET, metadata={"live_order": True})
    res_live = MarketScanResult(run_id="run1", created_at_utc="", request=req_live, status=RuntimeRunStatus.COMPLETED)
    assert validate_no_live_execution_in_scan(res_live).valid is False

    # State validation
    state = RuntimeState(run_id="run1", mode=RuntimeMode.DRY_RUN, status=RuntimeRunStatus.COMPLETED)
    assert validate_runtime_state(state).valid is True

    # Step validation
    steps = [PipelineStepResult(step_name=PipelineStepName.PREFLIGHT, status=PipelineStepStatus.COMPLETED, duration_seconds=-1)]
    assert validate_pipeline_step_results(steps).valid is False

    # Assert
    rep = validate_market_scan_request_report(req_inv)
    with pytest.raises(RuntimeValidationError):
        assert_runtime_valid(rep)
