from pathlib import Path
from usa_signal_bot.runtime.scan_orchestrator import MarketScanOrchestrator
from usa_signal_bot.runtime.runtime_models import MarketScanRequest
from usa_signal_bot.core.enums import RuntimeMode, ScanScope, RuntimeRunStatus

def test_market_scan_orchestrator_dry_run(tmp_path):
    orch = MarketScanOrchestrator(tmp_path)
    req = MarketScanRequest(
        run_name="test_dry",
        mode=RuntimeMode.DRY_RUN,
        scope=ScanScope.SMALL_TEST_SET,
        write_outputs=False
    )
    result = orch.run_scan(req)
    assert result.status == RuntimeRunStatus.COMPLETED
    assert len(result.step_results) > 0
    assert not orch.lock_manager.is_locked()

def test_market_scan_orchestrator_stop(tmp_path):
    orch = MarketScanOrchestrator(tmp_path)
    orch.stop_manager.request_stop("testing stop")
    req = MarketScanRequest(
        run_name="test_stop",
        mode=RuntimeMode.DRY_RUN,
        scope=ScanScope.SMALL_TEST_SET,
        write_outputs=False
    )
    result = orch.run_scan(req)
    assert result.status == RuntimeRunStatus.FAILED
    assert 'Safe stop' in result.errors[0]
