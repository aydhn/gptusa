import pytest
from usa_signal_bot.data.readiness import (
    default_readiness_criteria, evaluate_readiness_from_coverage,
    readiness_report_to_text, assert_data_ready
)
from usa_signal_bot.data.coverage import DataCoverageReport, SymbolTimeframeCoverage
from usa_signal_bot.core.enums import DataCoverageStatus, DataReadinessStatus
from usa_signal_bot.core.exceptions import DataReadinessError

def test_default_readiness_criteria():
    crit = default_readiness_criteria()
    assert crit.min_ready_pair_ratio == 0.70
    assert crit.require_primary_timeframe is True

def test_evaluate_readiness_ready():
    cov = DataCoverageReport(
        timeframes=["1d"],
        coverages=[
            SymbolTimeframeCoverage(symbol="AAPL", timeframe="1d", status=DataCoverageStatus.COMPLETE, coverage_ratio=1.0)
        ]
    )
    report = evaluate_readiness_from_coverage(cov)
    assert report.overall_status == DataReadinessStatus.READY

def test_evaluate_readiness_partial():
    cov = DataCoverageReport(
        timeframes=["1d", "15m"],
        coverages=[
            SymbolTimeframeCoverage(symbol="AAPL", timeframe="1d", status=DataCoverageStatus.COMPLETE, coverage_ratio=1.0),
            SymbolTimeframeCoverage(symbol="AAPL", timeframe="15m", status=DataCoverageStatus.PARTIAL, coverage_ratio=0.6)
        ]
    )
    report = evaluate_readiness_from_coverage(cov)
    # Intraday partial is allowed, but score might make it partial overall depending on criteria
    assert report.overall_status == DataReadinessStatus.READY or report.overall_status == DataReadinessStatus.PARTIAL

def test_evaluate_readiness_primary_failed():
    cov = DataCoverageReport(
        timeframes=["1d", "15m"],
        coverages=[
            SymbolTimeframeCoverage(symbol="AAPL", timeframe="1d", status=DataCoverageStatus.EMPTY, coverage_ratio=0.0),
            SymbolTimeframeCoverage(symbol="AAPL", timeframe="15m", status=DataCoverageStatus.COMPLETE, coverage_ratio=1.0)
        ]
    )
    report = evaluate_readiness_from_coverage(cov)
    assert report.overall_status == DataReadinessStatus.NOT_READY

def test_assert_data_ready():
    report = evaluate_readiness_from_coverage(DataCoverageReport(timeframes=["1d"], coverages=[]))
    with pytest.raises(DataReadinessError):
        assert_data_ready(report)

def test_readiness_report_to_text():
    cov = DataCoverageReport(
        timeframes=["1d"],
        coverages=[
            SymbolTimeframeCoverage(symbol="AAPL", timeframe="1d", status=DataCoverageStatus.COMPLETE, coverage_ratio=1.0)
        ]
    )
    report = evaluate_readiness_from_coverage(cov)
    text = readiness_report_to_text(report)
    assert "READY" in text
    assert "AAPL" in text
