from dataclasses import dataclass, field
from typing import List, Optional
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.core.enums import DataQualityStatus
from usa_signal_bot.core.exceptions import DataValidationError

@dataclass
class DataQualityIssue:
    symbol: Optional[str] = None
    timestamp_utc: Optional[str] = None
    severity: str = "WARNING"
    field: Optional[str] = None
    message: str = ""

@dataclass
class DataQualityReport:
    provider_name: str = ""
    timeframe: str = ""
    total_bars: int = 0
    valid_bars: int = 0
    invalid_bars: int = 0
    symbols_checked: List[str] = field(default_factory=list)
    missing_symbols: List[str] = field(default_factory=list)
    issues: List[DataQualityIssue] = field(default_factory=list)
    status: DataQualityStatus = DataQualityStatus.OK

def validate_ohlcv_bar_quality(bar: OHLCVBar) -> List[DataQualityIssue]:
    """Validates a single bar for data quality issues."""
    issues = []

    if bar.high < bar.low:
        issues.append(DataQualityIssue(
            symbol=bar.symbol, timestamp_utc=bar.timestamp_utc,
            severity="ERROR", field="high/low",
            message=f"High ({bar.high}) is less than Low ({bar.low})"
        ))

    if bar.volume < 0:
        issues.append(DataQualityIssue(
            symbol=bar.symbol, timestamp_utc=bar.timestamp_utc,
            severity="ERROR", field="volume",
            message=f"Volume is negative: {bar.volume}"
        ))

    if bar.open <= 0 or bar.high <= 0 or bar.low <= 0 or bar.close <= 0:
        issues.append(DataQualityIssue(
            symbol=bar.symbol, timestamp_utc=bar.timestamp_utc,
            severity="ERROR", field="price",
            message="One or more price fields are <= 0"
        ))

    return issues

def validate_ohlcv_bars_quality(bars: List[OHLCVBar], expected_symbols: List[str], provider_name: str, timeframe: str) -> DataQualityReport:
    """Validates a collection of bars against expected conditions."""
    report = DataQualityReport(
        provider_name=provider_name,
        timeframe=timeframe,
        symbols_checked=expected_symbols.copy()
    )

    if not bars:
        report.status = DataQualityStatus.ERROR
        report.issues.append(DataQualityIssue(severity="ERROR", message="No bars provided for validation."))
        report.missing_symbols = expected_symbols.copy()
        return report

    symbol_bar_counts = {sym: 0 for sym in expected_symbols}
    seen_timestamps = set()

    for bar in bars:
        report.total_bars += 1

        # Check if symbol was expected
        if bar.symbol not in expected_symbols:
            report.issues.append(DataQualityIssue(
                symbol=bar.symbol, severity="WARNING", field="symbol",
                message=f"Unexpected symbol {bar.symbol} found in data."
            ))

        symbol_bar_counts[bar.symbol] = symbol_bar_counts.get(bar.symbol, 0) + 1

        # Duplicate timestamp check
        key = (bar.symbol, bar.timestamp_utc)
        if key in seen_timestamps:
            report.issues.append(DataQualityIssue(
                symbol=bar.symbol, timestamp_utc=bar.timestamp_utc,
                severity="WARNING", field="timestamp_utc",
                message="Duplicate timestamp for symbol"
            ))
        seen_timestamps.add(key)

        # Bar level issues
        bar_issues = validate_ohlcv_bar_quality(bar)
        if bar_issues:
            report.invalid_bars += 1
            report.issues.extend(bar_issues)
        else:
            report.valid_bars += 1

    # Check for missing symbols
    for sym, count in symbol_bar_counts.items():
        if count == 0:
            report.missing_symbols.append(sym)
            report.issues.append(DataQualityIssue(
                symbol=sym, severity="WARNING", field="symbol",
                message="No data returned for expected symbol"
            ))

    # Determine status
    has_errors = any(i.severity == "ERROR" for i in report.issues)
    has_warnings = any(i.severity == "WARNING" for i in report.issues)

    if has_errors or report.valid_bars == 0:
        report.status = DataQualityStatus.ERROR
    elif has_warnings:
        report.status = DataQualityStatus.WARNING

    return report

def data_quality_report_to_text(report: DataQualityReport) -> str:
    """Formats a DataQualityReport into a readable text summary."""
    lines = [
        f"Data Quality Report ({report.provider_name} - {report.timeframe})",
        f"Status: {report.status.value}",
        f"Total Bars: {report.total_bars}",
        f"Valid Bars: {report.valid_bars}",
        f"Invalid Bars: {report.invalid_bars}",
        f"Symbols Checked: {len(report.symbols_checked)}",
        f"Missing Symbols: {len(report.missing_symbols)}"
    ]
    if report.issues:
        lines.append("Issues:")
        # Limit printed issues to avoid huge spam
        for i, issue in enumerate(report.issues[:10]):
            sym_part = f"[{issue.symbol}]" if issue.symbol else ""
            ts_part = f"@{issue.timestamp_utc}" if issue.timestamp_utc else ""
            lines.append(f"  - {issue.severity} {sym_part}{ts_part} {issue.field or ''}: {issue.message}")
        if len(report.issues) > 10:
             lines.append(f"  ... and {len(report.issues) - 10} more issues.")

    return "\n".join(lines)

def assert_data_quality_acceptable(report: DataQualityReport, allow_warnings: bool = True) -> None:
    """Raises DataValidationError if quality is not acceptable."""
    if report.status == DataQualityStatus.ERROR:
        raise DataValidationError(f"Data quality check failed: {report.invalid_bars} invalid bars. {len(report.missing_symbols)} missing symbols.")
    if not allow_warnings and report.status == DataQualityStatus.WARNING:
        raise DataValidationError("Data quality check raised warnings which are not allowed.")
