from pathlib import Path
from usa_signal_bot.runtime.pipeline_steps import PipelineStepRunner
from usa_signal_bot.runtime.runtime_models import PipelineStepConfig, MarketScanRequest
from usa_signal_bot.core.enums import PipelineStepName, PipelineStepStatus, RuntimeMode, ScanScope

def test_pipeline_step_runner_preflight(tmp_path):
    runner = PipelineStepRunner(tmp_path)
    req = MarketScanRequest(run_name="t", mode=RuntimeMode.DRY_RUN, scope=ScanScope.SMALL_TEST_SET)
    context = {"request": req}

    res = runner.run_preflight(context)
    assert res.status == PipelineStepStatus.COMPLETED
    assert res.step_name == PipelineStepName.PREFLIGHT

def test_pipeline_step_runner_universe_resolve(tmp_path):
    runner = PipelineStepRunner(tmp_path)
    req = MarketScanRequest(run_name="t", mode=RuntimeMode.DRY_RUN, scope=ScanScope.SMALL_TEST_SET)
    context = {"request": req}

    res = runner.run_universe_resolve(context)
    assert res.status == PipelineStepStatus.COMPLETED
    assert "SPY" in context["resolved_symbols"]

def test_pipeline_step_runner_unimplemented(tmp_path):
    runner = PipelineStepRunner(tmp_path)
    req = MarketScanRequest(run_name="t", mode=RuntimeMode.DRY_RUN, scope=ScanScope.SMALL_TEST_SET)
    context = {"request": req}

    config = PipelineStepConfig(step_name="NOT_A_REAL_STEP") # type: ignore
    res = runner.run_step(config, context)
    assert res.status == PipelineStepStatus.FAILED
    assert len(res.errors) > 0
