from pathlib import Path
from usa_signal_bot.runtime.pipeline_steps import PipelineStepRunner
from usa_signal_bot.runtime.runtime_models import MarketScanRequest, PipelineStepConfig
from usa_signal_bot.core.enums import RuntimeMode, ScanScope, PipelineStepName, PipelineStepStatus

def test_run_notification_disabled():
    runner = PipelineStepRunner(Path("/tmp"))
    req = MarketScanRequest("test", RuntimeMode.MANUAL_ONCE, ScanScope.SMALL_TEST_SET, timeframes=["1d"], provider_name="dummy", notify=False)
    ctx = {"request": req}

    conf = PipelineStepConfig(PipelineStepName.NOTIFICATION)
    res = runner.run_step(conf, ctx)
    assert res.status == PipelineStepStatus.SKIPPED

def test_run_notification_enabled():
    runner = PipelineStepRunner(Path("/tmp"))
    req = MarketScanRequest("test", RuntimeMode.MANUAL_ONCE, ScanScope.SMALL_TEST_SET, timeframes=["1d"], provider_name="dummy", notify=True)
    ctx = {"request": req, "run_id": "r1"}

    conf = PipelineStepConfig(PipelineStepName.NOTIFICATION)
    res = runner.run_step(conf, ctx)
    assert res.status == PipelineStepStatus.COMPLETED
    assert "alert_evaluations" in res.summary
