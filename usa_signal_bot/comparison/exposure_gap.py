from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from usa_signal_bot.core.enums import ComparisonMetricStatus, GapSeverity
from usa_signal_bot.comparison.result_loaders import LoadedComparisonData

@dataclass
class ExposureGapMetrics:
    status: ComparisonMetricStatus
    paper_average_exposure: Optional[float]
    backtest_average_exposure: Optional[float]
    average_exposure_gap: Optional[float]
    paper_max_exposure: Optional[float]
    backtest_max_exposure: Optional[float]
    max_exposure_gap: Optional[float]
    paper_final_positions: Optional[int]
    backtest_final_positions: Optional[int]
    final_position_gap: Optional[int]
    exposure_gap_severity: GapSeverity
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def calculate_exposure_gap_metrics(paper_data: Union[LoadedComparisonData, Dict[str, Any]], backtest_data: Union[LoadedComparisonData, Dict[str, Any]]) -> ExposureGapMetrics:
    p_avg = extract_average_exposure(paper_data)
    b_avg = extract_average_exposure(backtest_data)

    p_max = extract_max_exposure(paper_data)
    b_max = extract_max_exposure(backtest_data)

    p_pos = extract_final_positions_count(paper_data)
    b_pos = extract_final_positions_count(backtest_data)

    avg_gap = (p_avg - b_avg) if p_avg is not None and b_avg is not None else None
    max_gap = (p_max - b_max) if p_max is not None and b_max is not None else None
    pos_gap = (p_pos - b_pos) if p_pos is not None and b_pos is not None else None

    status = ComparisonMetricStatus.INSUFFICIENT_DATA if avg_gap is None and pos_gap is None else ComparisonMetricStatus.OK

    metrics = ExposureGapMetrics(
        status=status,
        paper_average_exposure=p_avg,
        backtest_average_exposure=b_avg,
        average_exposure_gap=avg_gap,
        paper_max_exposure=p_max,
        backtest_max_exposure=b_max,
        max_exposure_gap=max_gap,
        paper_final_positions=p_pos,
        backtest_final_positions=b_pos,
        final_position_gap=pos_gap,
        exposure_gap_severity=GapSeverity.UNKNOWN
    )

    metrics.exposure_gap_severity = classify_exposure_gap_severity(metrics)
    return metrics

def _get_records(data: Union[LoadedComparisonData, Dict[str, Any]]) -> Dict[str, Any]:
    if isinstance(data, LoadedComparisonData):
        return data.records
    return data

def extract_average_exposure(data: Union[LoadedComparisonData, Dict[str, Any]]) -> Optional[float]:
    records = _get_records(data)
    perf = records.get("performance", {})
    if not perf:
        perf = records.get("analytics", {})
    return perf.get("average_exposure", perf.get("gross_exposure"))

def extract_max_exposure(data: Union[LoadedComparisonData, Dict[str, Any]]) -> Optional[float]:
    records = _get_records(data)
    perf = records.get("performance", {})
    if not perf:
        perf = records.get("analytics", {})
    return perf.get("max_exposure", perf.get("peak_exposure"))

def extract_final_positions_count(data: Union[LoadedComparisonData, Dict[str, Any]]) -> Optional[int]:
    records = _get_records(data)
    perf = records.get("performance", {})
    if not perf:
        perf = records.get("analytics", {})
    return perf.get("final_positions", perf.get("open_positions"))

def classify_exposure_gap_severity(metrics: ExposureGapMetrics) -> GapSeverity:
    if metrics.status == ComparisonMetricStatus.INSUFFICIENT_DATA:
        return GapSeverity.UNKNOWN

    if metrics.average_exposure_gap is not None and abs(metrics.average_exposure_gap) > 0.20:
        return GapSeverity.HIGH
    if metrics.final_position_gap is not None and abs(metrics.final_position_gap) > 3:
        return GapSeverity.MODERATE

    return GapSeverity.LOW

def exposure_gap_metrics_to_dict(metrics: ExposureGapMetrics) -> dict:
    from dataclasses import asdict
    d = asdict(metrics)
    if isinstance(d.get("status"), ComparisonMetricStatus):
        d["status"] = d["status"].value
    if isinstance(d.get("exposure_gap_severity"), GapSeverity):
        d["exposure_gap_severity"] = d["exposure_gap_severity"].value
    return d

def exposure_gap_metrics_to_text(metrics: ExposureGapMetrics) -> str:
    lines = ["Exposure Gap Metrics:"]
    lines.append(f"  Avg Exposure Gap: {metrics.average_exposure_gap:.2f}" if metrics.average_exposure_gap is not None else "  Avg Exposure Gap: N/A")
    lines.append(f"  Max Exposure Gap: {metrics.max_exposure_gap:.2f}" if metrics.max_exposure_gap is not None else "  Max Exposure Gap: N/A")
    lines.append(f"  Final Position Gap: {metrics.final_position_gap}" if metrics.final_position_gap is not None else "  Final Position Gap: N/A")
    lines.append(f"  Severity: {metrics.exposure_gap_severity.value}")
    return "\n".join(lines)
