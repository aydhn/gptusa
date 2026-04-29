from usa_signal_bot.data.validation_rules import ValidationRuleResult
from usa_signal_bot.core.enums import ValidationSeverity, DataAnomalyType
from usa_signal_bot.data.anomalies import classify_anomaly_type, validation_results_to_anomaly_report, anomaly_report_to_text, has_blocking_anomalies

def test_classify_anomaly_type():
    res = ValidationRuleResult("price_consistency", False, ValidationSeverity.ERROR, "High cannot be less than low")
    t = classify_anomaly_type(res)
    assert t == DataAnomalyType.HIGH_LOW_INCONSISTENCY

def test_validation_results_to_anomaly_report():
    results = [
        ValidationRuleResult("price_consistency", False, ValidationSeverity.ERROR, "High cannot be less than low"),
        ValidationRuleResult("volume", False, ValidationSeverity.WARNING, "Zero volume")
    ]
    report = validation_results_to_anomaly_report(results, "mock", "1d")
    assert report.total_anomalies == 2
    assert report.error_count == 1
    assert report.warning_count == 1

    assert has_blocking_anomalies(report) is True

def test_anomaly_report_to_text():
    results = [
        ValidationRuleResult("price_consistency", False, ValidationSeverity.ERROR, "High cannot be less than low")
    ]
    report = validation_results_to_anomaly_report(results, "mock", "1d")
    text = anomaly_report_to_text(report)
    assert "Total Anomalies: 1" in text
    assert "HIGH_LOW_INCONSISTENCY" in text
