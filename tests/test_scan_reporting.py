import pytest
from usa_signal_bot.runtime.scan_reporting import (
    pipeline_step_result_to_text, market_scan_request_to_text,
    market_scan_result_to_text, runtime_state_to_text,
    scan_summary_to_text, scheduled_scan_plan_summary_to_text,
    runtime_limitations_text
)
from usa_signal_bot.runtime.runtime_models import MarketScanResult, MarketScanRequest, PipelineStepResult, RuntimeState, ScheduledScanPlan
from usa_signal_bot.core.enums import RuntimeMode, ScanScope, RuntimeRunStatus, PipelineStepName, PipelineStepStatus

def test_scan_reporting():
    req = MarketScanRequest(run_name="t", mode=RuntimeMode.DRY_RUN, scope=ScanScope.SMALL_TEST_SET)
    res = MarketScanResult(run_id="run1", created_at_utc="", request=req, status=RuntimeRunStatus.COMPLETED)
    step = PipelineStepResult(step_name=PipelineStepName.PREFLIGHT, status=PipelineStepStatus.COMPLETED)
    state = RuntimeState(run_id="run1", mode=RuntimeMode.DRY_RUN, status=RuntimeRunStatus.COMPLETED)
    plan = ScheduledScanPlan(plan_id="p1", enabled=True, name="p1", mode=RuntimeMode.DRY_RUN, interval_minutes=60, max_runs_per_day=8, market_hours_only=False, timezone="UTC", scan_request_template=req, created_at_utc="")

    assert "preflight" in pipeline_step_result_to_text(step)
    assert "small_test_set" in market_scan_request_to_text(req)
    assert "run1" in market_scan_result_to_text(res)
    assert "Runtime State [run1]" in runtime_state_to_text(state)
    assert "Scan run1" in scan_summary_to_text(res)
    assert "Plan p1" in scheduled_scan_plan_summary_to_text(plan)
    assert "NOT investment advice" in runtime_limitations_text()
