from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from usa_signal_bot.strategies.signal_contract import StrategySignal, validate_strategy_signal
from usa_signal_bot.core.enums import SignalLifecycleStatus, SignalQualityStatus
from usa_signal_bot.core.exceptions import SignalValidationError

@dataclass
class SignalValidationIssue:
    signal_id: Optional[str]
    symbol: Optional[str]
    severity: str
    field: Optional[str]
    message: str

@dataclass
class SignalValidationReport:
    valid: bool
    total_signals: int
    valid_signals: int
    invalid_signals: int
    issues: List[SignalValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_signal_list(signals: List[StrategySignal]) -> SignalValidationReport:
    issues = []
    warnings = []
    errors = []
    valid_count = 0
    invalid_count = 0

    if not signals:
        warnings.append("Empty signal list")
        return SignalValidationReport(
            valid=True,
            total_signals=0,
            valid_signals=0,
            invalid_signals=0,
            issues=[],
            warnings=warnings,
            errors=[]
        )

    for signal in signals:
        try:
            validate_strategy_signal(signal)
            valid_count += 1
        except Exception as e:
            invalid_count += 1
            issues.append(SignalValidationIssue(
                signal_id=getattr(signal, "signal_id", "UNKNOWN"),
                symbol=getattr(signal, "symbol", "UNKNOWN"),
                severity="ERROR",
                field=None,
                message=str(e)
            ))

    # Check for duplicates
    dup_issues = validate_signal_uniqueness(signals)
    if dup_issues:
        issues.extend(dup_issues)
        for issue in dup_issues:
            if issue.severity == "ERROR":
                invalid_count += 1
                valid_count -= 1

    # Check confidence distribution
    conf_issues = validate_signal_confidence_distribution(signals)
    for issue in conf_issues:
        issues.append(issue)
        if issue.severity == "WARNING":
            warnings.append(issue.message)

    has_errors = any(i.severity == "ERROR" for i in issues)
    for i in issues:
        if i.severity == "ERROR" and i.message not in errors:
            errors.append(i.message)

    return SignalValidationReport(
        valid=not has_errors,
        total_signals=len(signals),
        valid_signals=valid_count,
        invalid_signals=invalid_count,
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_signal_uniqueness(signals: List[StrategySignal]) -> List[SignalValidationIssue]:
    issues = []
    seen = set()
    for signal in signals:
        sid = getattr(signal, "signal_id", None)
        if sid:
            if sid in seen:
                issues.append(SignalValidationIssue(
                    signal_id=sid,
                    symbol=getattr(signal, "symbol", "UNKNOWN"),
                    severity="ERROR",
                    field="signal_id",
                    message=f"Duplicate signal_id: {sid}"
                ))
            seen.add(sid)
    return issues

def validate_signal_confidence_distribution(signals: List[StrategySignal]) -> List[SignalValidationIssue]:
    issues = []
    high_conf_count = sum(1 for s in signals if getattr(s, "confidence", 0) > 0.8)

    if len(signals) > 0:
        ratio = high_conf_count / len(signals)
        if ratio > 0.5 and len(signals) >= 5:
            issues.append(SignalValidationIssue(
                signal_id=None,
                symbol=None,
                severity="WARNING",
                field="confidence",
                message=f"High proportion ({ratio:.1%}) of signals have very high confidence (>0.8). Possible overconfidence."
            ))
    return issues

def signal_validation_report_to_text(report: SignalValidationReport) -> str:
    lines = [
        "--- Signal Validation Report ---",
        f"Valid: {report.valid}",
        f"Total Signals: {report.total_signals}",
        f"Valid Signals: {report.valid_signals}",
        f"Invalid Signals: {report.invalid_signals}"
    ]

    if report.errors:
        lines.append("Errors:")
        for e in report.errors:
            lines.append(f"  - {e}")

    if report.warnings:
        lines.append("Warnings:")
        for w in report.warnings:
            lines.append(f"  - {w}")

    return "\n".join(lines)

def assert_signals_valid(report: SignalValidationReport) -> None:
    if not report.valid:
        raise SignalValidationError(f"Signal validation failed with {report.invalid_signals} invalid signals. Errors: {report.errors}")


def validate_scored_signal(signal: StrategySignal) -> List[SignalValidationIssue]:
    issues = []
    issues.extend(validate_signal_score_breakdown(signal))
    issues.extend(validate_confluence_fields(signal))

    if signal.lifecycle_status == SignalLifecycleStatus.REJECTED and signal.quality_status == SignalQualityStatus.ACCEPTED:
        issues.append(SignalValidationIssue(
            signal_id=signal.signal_id,
            symbol=signal.symbol,
            severity="WARNING",
            field="lifecycle_status",
            message="Lifecycle status is REJECTED but quality status is ACCEPTED"
        ))

    return issues

def validate_signal_score_breakdown(signal: StrategySignal) -> List[SignalValidationIssue]:
    issues = []
    if not isinstance(signal.score_breakdown, dict):
        issues.append(SignalValidationIssue(
            signal_id=signal.signal_id,
            symbol=signal.symbol,
            severity="ERROR",
            field="score_breakdown",
            message="score_breakdown must be a dict"
        ))
    return issues

def validate_confluence_fields(signal: StrategySignal) -> List[SignalValidationIssue]:
    issues = []
    if signal.confluence_score is not None:
        if not (0.0 <= signal.confluence_score <= 100.0):
            issues.append(SignalValidationIssue(
                signal_id=signal.signal_id,
                symbol=signal.symbol,
                severity="ERROR",
                field="confluence_score",
                message=f"confluence_score must be between 0.0 and 100.0, got {signal.confluence_score}"
            ))
    return issues
