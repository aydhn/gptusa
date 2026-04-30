from usa_signal_bot.data.readiness import DataReadinessItem
from usa_signal_bot.core.enums import PipelineRunStatus
import pytest
from unittest.mock import Mock, patch
from usa_signal_bot.data.active_universe_pipeline import (
    ActiveUniverseDataPipeline,
    ActiveUniversePipelineRequest
)
from usa_signal_bot.data.multitimeframe import MultiTimeframeDataResult
from usa_signal_bot.data.coverage import DataCoverageReport, DataCoverageStatus
from usa_signal_bot.data.readiness import DataReadinessReport, DataReadinessStatus
from usa_signal_bot.universe.readiness_gate import UniverseReadinessGateCriteria

def test_active_pipeline_success(tmp_path):
    # Setup dummy data structure
    uni_dir = tmp_path / "universe"
    uni_dir.mkdir()
    (uni_dir / "watchlist.csv").write_text("symbol,asset_type\nAAPL,stock\n")

    mock_mtf = Mock()
    mock_mtf.run_for_universe.return_value = (
        type("MockMTFResult", (), {"failed_symbols": 0, "successful_symbols": 1, "total_symbols": 1, "warnings": [], "errors": []})(),
        DataCoverageReport(report_id="cov", coverages=[]),
        DataReadinessReport(report_id="ready", items=[DataReadinessItem(symbol="AAPL", timeframe="1d", status=DataReadinessStatus.READY)])
    )

    pipeline = ActiveUniverseDataPipeline(mock_mtf, tmp_path)

    req = ActiveUniversePipelineRequest(
        fallback_to_watchlist=True,
        readiness_criteria=UniverseReadinessGateCriteria(
            min_symbol_score=0.0, # accept everything
            min_required_timeframes=0,
            required_primary_timeframe="1d",
            allow_partial_symbols=True,
            min_eligible_symbol_ratio=0.0,
            max_failed_symbol_ratio=1.0
        ),
        write_reports=False,
        write_eligible_outputs=False
    )

    # Should run and return success because criteria is 0
    res = pipeline.run(req)
    assert res.success == True
    assert res.run.status.value == "COMPLETED"

def test_active_pipeline_failure_no_symbols(tmp_path):
    uni_dir = tmp_path / "universe"
    uni_dir.mkdir()
    (uni_dir / "watchlist.csv").write_text("symbol,asset_type\n") # Empty

    pipeline = ActiveUniverseDataPipeline(Mock(), tmp_path)
    req = ActiveUniversePipelineRequest(fallback_to_watchlist=True)

    from usa_signal_bot.core.exceptions import ActiveUniversePipelineError
    with pytest.raises(ActiveUniversePipelineError):
        pipeline.run(req)
