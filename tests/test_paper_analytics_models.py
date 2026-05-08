from usa_signal_bot.paper.paper_analytics_models import (
    PaperEquityMetrics,
    PaperTradeMetrics,
    PaperExposureMetrics,
    PaperRiskMetrics,
    PaperPerformanceReport,
    create_paper_performance_report_id,
    paper_performance_report_to_dict
)
from usa_signal_bot.core.enums import (
    PaperMetricStatus, PaperRiskLevel, PaperDrawdownStatus,
    PaperRiskLimitStatus, PaperPerformanceBucket, PaperTrendDirection, PaperAnalyticsReportType, PaperAnalyticsStatus
)

def test_paper_performance_report_serialization():
    eq = PaperEquityMetrics(PaperMetricStatus.OK, 100, 110, 10, 10.0, 115, 95, 20, 17.4, 5, 4.3, 10)
    tr = PaperTradeMetrics(PaperMetricStatus.OK, 5, 5, 0, 3, 2, 0, 0.6, 0.4, 10, -5, 2, 30, 10, 20, 3.0, 4.0, 15, -6, 2, 1)
    ex = PaperExposureMetrics(PaperMetricStatus.OK, 1000, 2000, 1000, 2000, 5, 10, 3, 0.5, 0.8)
    ri = PaperRiskMetrics(PaperMetricStatus.OK, PaperRiskLevel.LOW, PaperDrawdownStatus.NORMAL, PaperRiskLimitStatus.WITHIN_LIMIT, 17.4, 4.3, 0.8, 0.2, 3, 0.1, False)

    report = PaperPerformanceReport(
        report_id=create_paper_performance_report_id(),
        created_at_utc="2023-01-01T00:00:00Z",
        report_type=PaperAnalyticsReportType.FULL_SUMMARY,
        status=PaperAnalyticsStatus.COMPLETED,
        account_id="acc1",
        source_run_id="run1",
        equity_metrics=eq,
        trade_metrics=tr,
        exposure_metrics=ex,
        risk_metrics=ri,
        performance_bucket=PaperPerformanceBucket.STRONG,
        trend_direction=PaperTrendDirection.IMPROVING
    )

    d = paper_performance_report_to_dict(report)
    assert d["report_id"] == report.report_id
    assert d["equity_metrics"]["total_return_pct"] == 10.0
    assert d["trade_metrics"]["win_rate"] == 0.6
    assert d["exposure_metrics"]["max_gross_exposure"] == 2000
    assert d["risk_metrics"]["risk_level"] == "LOW"
    assert d["performance_bucket"] == "STRONG"
