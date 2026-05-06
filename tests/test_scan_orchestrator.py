from pathlib import Path
from usa_signal_bot.runtime.scan_orchestrator import MarketScanOrchestrator
from usa_signal_bot.runtime.runtime_models import MarketScanRequest
from usa_signal_bot.core.enums import RuntimeMode, ScanScope, PipelineStepName

def test_build_default_step_configs():
    orch = MarketScanOrchestrator(Path("/tmp"))
    req = MarketScanRequest("test", RuntimeMode.MANUAL_ONCE, ScanScope.SMALL_TEST_SET, notify=True)

    configs = orch.build_default_step_configs(req)
    notify_config = next((c for c in configs if c.step_name == PipelineStepName.NOTIFICATION), None)
    assert notify_config is not None
    assert notify_config.enabled == True
