import pytest
from usa_signal_bot.core.enums import RuntimeMode, PipelineStepName, PipelineStepStatus, ScanScope
from usa_signal_bot.runtime.runtime_models import (
    PipelineStepConfig, PipelineStepResult, MarketScanRequest, MarketScanResult,
    ScheduledScanPlan, create_runtime_run_id, create_scheduled_scan_plan_id,
    validate_market_scan_request, validate_scheduled_scan_plan
)

def test_pipeline_step_config():
    config = PipelineStepConfig(step_name=PipelineStepName.PREFLIGHT)
    assert config.enabled is True
    assert config.required is True

def test_pipeline_step_result():
    res = PipelineStepResult(step_name=PipelineStepName.PREFLIGHT, status=PipelineStepStatus.COMPLETED)
    assert res.step_name == PipelineStepName.PREFLIGHT
    assert res.status == PipelineStepStatus.COMPLETED

def test_market_scan_request():
    req = MarketScanRequest(
        run_name="test",
        mode=RuntimeMode.DRY_RUN,
        scope=ScanScope.SMALL_TEST_SET
    )
    validate_market_scan_request(req)
    assert req.run_name == "test"

    req_invalid = MarketScanRequest(
        run_name="test",
        mode=RuntimeMode.DRY_RUN,
        scope=ScanScope.SMALL_TEST_SET,
        timeframes=[]
    )
    with pytest.raises(ValueError, match="timeframes cannot be empty"):
        validate_market_scan_request(req_invalid)

def test_scheduled_scan_plan():
    req = MarketScanRequest(
        run_name="test",
        mode=RuntimeMode.DRY_RUN,
        scope=ScanScope.SMALL_TEST_SET
    )
    plan = ScheduledScanPlan(
        plan_id="plan1",
        enabled=True,
        name="test_plan",
        mode=RuntimeMode.SCHEDULE_PLAN_ONLY,
        interval_minutes=60,
        max_runs_per_day=8,
        market_hours_only=False,
        timezone="UTC",
        scan_request_template=req,
        created_at_utc="2024-01-01T00:00:00Z"
    )
    validate_scheduled_scan_plan(plan)
    assert plan.interval_minutes == 60

    plan_invalid = ScheduledScanPlan(
        plan_id="plan1",
        enabled=True,
        name="test_plan",
        mode=RuntimeMode.SCHEDULE_PLAN_ONLY,
        interval_minutes=-1,
        max_runs_per_day=8,
        market_hours_only=False,
        timezone="UTC",
        scan_request_template=req,
        created_at_utc="2024-01-01T00:00:00Z"
    )
    with pytest.raises(ValueError, match="interval_minutes must be positive"):
        validate_scheduled_scan_plan(plan_invalid)

def test_ids():
    run_id = create_runtime_run_id()
    plan_id = create_scheduled_scan_plan_id()
    assert run_id.startswith("scan_")
    assert plan_id.startswith("plan_")
