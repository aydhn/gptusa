import pytest
from usa_signal_bot.core.enums import GapSeverity, ComparisonMetricStatus
from usa_signal_bot.comparison.exposure_gap import (
    calculate_exposure_gap_metrics, extract_average_exposure,
    extract_final_positions_count, classify_exposure_gap_severity,
    exposure_gap_metrics_to_text
)

def test_exposure_gap_metrics():
    p_data = {"performance": {"average_exposure": 0.5, "final_positions": 5}}
    b_data = {"analytics": {"gross_exposure": 0.4, "open_positions": 4}}

    res = calculate_exposure_gap_metrics(p_data, b_data)

    assert res.status == ComparisonMetricStatus.OK
    assert res.average_exposure_gap == pytest.approx(0.1)
    assert res.final_position_gap == 1

def test_severity_classification():
    p_data = {"performance": {"average_exposure": 0.8}}
    b_data = {"performance": {"average_exposure": 0.5}}
    res = calculate_exposure_gap_metrics(p_data, b_data)

    sev = classify_exposure_gap_severity(res)
    assert sev == GapSeverity.HIGH

def test_text_output():
    p_data = {"performance": {"average_exposure": 0.5}}
    b_data = {"performance": {"average_exposure": 0.5}}
    res = calculate_exposure_gap_metrics(p_data, b_data)
    txt = exposure_gap_metrics_to_text(res)
    assert "Avg Exposure Gap: 0.00" in txt
