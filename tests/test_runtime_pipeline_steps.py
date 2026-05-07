import pytest
from usa_signal_bot.runtime.pipeline_steps import run_paper_trading
from usa_signal_bot.core.enums import PipelineStepName, PipelineStepStatus

def test_run_paper_trading_skipped():
    class MockReq:
        paper_enabled = False

    context = {"request": MockReq()}
    res = run_paper_trading(context)

    assert res.step_name.value == "paper_trading" or res.step_name == "paper_trading"
    assert res.status.value == "skipped" or res.status == "skipped"
