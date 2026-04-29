import uuid
from dataclasses import dataclass, field
from typing import Any, List, Optional
from usa_signal_bot.core.enums import ValidationSeverity, DataAnomalyType
from usa_signal_bot.data.validation_rules import ValidationRuleResult

@dataclass
class DataAnomaly:
    anomaly_id: str
    anomaly_type: DataAnomalyType
    severity: ValidationSeverity
    symbol: Optional[str]
    timestamp_utc: Optional[str]
    field: Optional[str]
    message: str
    details: dict = __import__("dataclasses").field(default_factory=dict)

@dataclass
class DataAnomalyReport:
    report_id: str
    provider_name: str
    timeframe: str
    created_at_utc: str
    total_anomalies: int
    error_count: int
    warning_count: int
    info_count: int
    anomalies: List[DataAnomaly]

def classify_anomaly_type(result: ValidationRuleResult) -> DataAnomalyType:
    rn = result.rule_name
    msg = result.message.lower()

    if rn == "required_fields":
        return DataAnomalyType.MISSING_REQUIRED_FIELD
    if rn == "price_consistency":
        if "high cannot be less than low" in msg or "high must be >=" in msg or "low must be <=" in msg:
            return DataAnomalyType.HIGH_LOW_INCONSISTENCY
        return DataAnomalyType.INVALID_PRICE
    if rn == "volume":
        if "negative" in msg:
            return DataAnomalyType.NEGATIVE_VOLUME
        if "zero" in msg:
            return DataAnomalyType.ZERO_VOLUME
    if rn == "duplicate":
        return DataAnomalyType.DUPLICATE_BAR
    if rn == "sequence":
        return DataAnomalyType.NON_MONOTONIC_TIMESTAMP
    if rn == "missing_symbol" or (rn == "symbol" and "empty" in msg):
        return DataAnomalyType.MISSING_SYMBOL
    if rn == "empty_dataset":
        return DataAnomalyType.EMPTY_DATASET

    return DataAnomalyType.UNKNOWN

def validation_result_to_anomaly(result: ValidationRuleResult) -> DataAnomaly:
    return DataAnomaly(
        anomaly_id=str(uuid.uuid4()),
        anomaly_type=classify_anomaly_type(result),
        severity=result.severity,
        symbol=result.symbol,
        timestamp_utc=result.timestamp_utc,
        field=result.field,
        message=result.message,
        details=result.details
    )

def validation_results_to_anomaly_report(results: List[ValidationRuleResult], provider_name: str, timeframe: str) -> DataAnomalyReport:
    from usa_signal_bot.utils.time_utils import utc_now
    anomalies = [validation_result_to_anomaly(r) for r in results if not r.passed]

    return DataAnomalyReport(
        report_id=str(uuid.uuid4()),
        provider_name=provider_name,
        timeframe=timeframe,
        created_at_utc=utc_now().isoformat(),
        total_anomalies=len(anomalies),
        error_count=sum(1 for a in anomalies if a.severity in (ValidationSeverity.ERROR, ValidationSeverity.CRITICAL)),
        warning_count=sum(1 for a in anomalies if a.severity == ValidationSeverity.WARNING),
        info_count=sum(1 for a in anomalies if a.severity == ValidationSeverity.INFO),
        anomalies=anomalies
    )

def anomaly_report_to_text(report: DataAnomalyReport) -> str:
    lines = [
        f"Data Anomaly Report ({report.provider_name} - {report.timeframe})",
        f"Total Anomalies: {report.total_anomalies} (Errors/Crit: {report.error_count}, Warnings: {report.warning_count})",
    ]
    if report.anomalies:
        lines.append("Anomalies:")
        for a in report.anomalies[:10]:
            sym = f"[{a.symbol}]" if a.symbol else ""
            ts = f"@{a.timestamp_utc}" if a.timestamp_utc else ""
            lines.append(f"  - {a.severity.value} | {a.anomaly_type.value} | {sym}{ts} {a.field or ''}: {a.message}")
        if len(report.anomalies) > 10:
             lines.append(f"  ... and {len(report.anomalies) - 10} more anomalies.")
    return "\n".join(lines)

def anomaly_report_to_dict(report: DataAnomalyReport) -> dict:
    from dataclasses import asdict
    return asdict(report)

def has_blocking_anomalies(report: DataAnomalyReport) -> bool:
    return report.error_count > 0
