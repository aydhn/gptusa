import json
import hashlib
from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import SizingSensitivityReport, SizingSensitivityRecord, SizingPrototypeResult, SizingSensitivityKind

def build_sizing_sensitivity_report(results: list[SizingPrototypeResult]) -> SizingSensitivityReport:
    report = SizingSensitivityReport()
    report.records = build_sizing_sensitivity_records(results)
    report.report_hash = compute_sizing_sensitivity_report_hash(report)
    report.report_valid = len(validate_sizing_sensitivity_report(report)) == 0
    return report

def build_sizing_sensitivity_records(results: list[SizingPrototypeResult]) -> list[SizingSensitivityRecord]:
    # Placeholder for actual sensitivity calculations (e.g. fraction variation given 10% change in volatility proxy)
    records = []

    r1 = SizingSensitivityRecord(
        sensitivity_kind=SizingSensitivityKind.VOLATILITY_SENSITIVITY,
        value=0.0,
        sensitivity_notes=["Placeholder for volatility sensitivity"],
        sensitivity_valid=True
    )
    records.append(r1)

    r2 = SizingSensitivityRecord(
        sensitivity_kind=SizingSensitivityKind.DRAWDOWN_SENSITIVITY,
        value=0.0,
        sensitivity_notes=["Placeholder for drawdown sensitivity"],
        sensitivity_valid=True
    )
    records.append(r2)

    return records

def compute_sizing_sensitivity_report_hash(report: SizingSensitivityReport) -> str:
    data = []
    for r in report.records:
        data.append({
            "kind": r.sensitivity_kind.value,
            "value": r.value
        })
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

def validate_sizing_sensitivity_report(report: SizingSensitivityReport) -> list[str]:
    errors = []
    if report.actual_position_size_detected:
        errors.append("Actual position size detected in sensitivity report.")
    if report.target_weight_detected:
        errors.append("Target weight detected in sensitivity report.")
    if report.allocation_detected:
        errors.append("Allocation detected in sensitivity report.")
    if report.order_size_detected:
        errors.append("Order size detected in sensitivity report.")
    return errors

def sizing_sensitivity_report_summary(report: SizingSensitivityReport) -> dict[str, Any]:
    return {"record_count": len(report.records), "valid": report.report_valid}

def sizing_sensitivity_report_to_text(report: SizingSensitivityReport, limit: int = 300) -> str:
    return f"Sizing Sensitivity Report: {len(report.records)} records"[:limit]
