"""Corporate action models."""
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    CorporateActionType,
    CorporateActionSource,
    CorporateActionSeverity,
    CorporateActionGuardStatus,
    AdjustedPriceValidationStatus,
    CorporateActionReportType
)

@dataclass
class CorporateActionEvent:
    event_id: str
    symbol: str
    action_type: CorporateActionType
    ex_date: str
    value: float | None
    ratio_numerator: float | None
    ratio_denominator: float | None
    source: CorporateActionSource
    confidence: float | None
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class AdjustedPriceValidationResult:
    validation_id: str
    symbol: str
    created_at_utc: str
    status: AdjustedPriceValidationStatus
    row_count: int
    adjusted_rows: int
    inconsistent_rows: int
    max_abs_diff_pct: float | None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class CorporateActionGuardResult:
    guard_id: str
    symbol: str
    created_at_utc: str
    status: CorporateActionGuardStatus
    severity: CorporateActionSeverity
    events: list[CorporateActionEvent]
    adjusted_validation: AdjustedPriceValidationResult | None
    detected_splits: list[dict[str, Any]]
    detected_dividends: list[dict[str, Any]]
    gap_anomalies: list[dict[str, Any]]
    recommended_guards: list[str]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class CorporateActionReviewResult:
    review_id: str
    created_at_utc: str
    report_type: CorporateActionReportType
    symbols: list[str]
    guard_results: list[CorporateActionGuardResult]
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def corporate_action_event_to_dict(event: CorporateActionEvent) -> dict[str, Any]:
    return {
        "event_id": event.event_id,
        "symbol": event.symbol,
        "action_type": event.action_type.value if hasattr(event.action_type, "value") else str(event.action_type),
        "ex_date": event.ex_date,
        "value": event.value,
        "ratio_numerator": event.ratio_numerator,
        "ratio_denominator": event.ratio_denominator,
        "source": event.source.value if hasattr(event.source, "value") else str(event.source),
        "confidence": event.confidence,
        "notes": event.notes,
        "metadata": event.metadata
    }

def adjusted_price_validation_result_to_dict(result: AdjustedPriceValidationResult) -> dict[str, Any]:
    return {
        "validation_id": result.validation_id,
        "symbol": result.symbol,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value if hasattr(result.status, "value") else str(result.status),
        "row_count": result.row_count,
        "adjusted_rows": result.adjusted_rows,
        "inconsistent_rows": result.inconsistent_rows,
        "max_abs_diff_pct": result.max_abs_diff_pct,
        "warnings": result.warnings,
        "errors": result.errors,
        "metadata": result.metadata
    }

def corporate_action_guard_result_to_dict(result: CorporateActionGuardResult) -> dict[str, Any]:
    return {
        "guard_id": result.guard_id,
        "symbol": result.symbol,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value if hasattr(result.status, "value") else str(result.status),
        "severity": result.severity.value if hasattr(result.severity, "value") else str(result.severity),
        "events": [corporate_action_event_to_dict(e) for e in result.events],
        "adjusted_validation": adjusted_price_validation_result_to_dict(result.adjusted_validation) if result.adjusted_validation else None,
        "detected_splits": result.detected_splits,
        "detected_dividends": result.detected_dividends,
        "gap_anomalies": result.gap_anomalies,
        "recommended_guards": result.recommended_guards,
        "warnings": result.warnings,
        "errors": result.errors,
        "metadata": result.metadata
    }

def corporate_action_review_result_to_dict(result: CorporateActionReviewResult) -> dict[str, Any]:
    return {
        "review_id": result.review_id,
        "created_at_utc": result.created_at_utc,
        "report_type": result.report_type.value if hasattr(result.report_type, "value") else str(result.report_type),
        "symbols": result.symbols,
        "guard_results": [corporate_action_guard_result_to_dict(g) for g in result.guard_results],
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors
    }

def validate_corporate_action_event(event: CorporateActionEvent) -> None:
    from usa_signal_bot.core.exceptions import CorporateActionValidationError
    if not event.symbol:
        raise CorporateActionValidationError("Symbol cannot be empty.")
    try:
        datetime.strptime(event.ex_date, "%Y-%m-%d")
    except ValueError:
        raise CorporateActionValidationError(f"Invalid date format, expected YYYY-MM-DD: {event.ex_date}")

    if event.confidence is not None and (event.confidence < 0.0 or event.confidence > 1.0):
        raise CorporateActionValidationError(f"Confidence must be between 0.0 and 1.0: {event.confidence}")

    if event.action_type == CorporateActionType.SPLIT:
        if event.ratio_numerator is not None and event.ratio_numerator <= 0:
            raise CorporateActionValidationError(f"Split ratio numerator must be positive: {event.ratio_numerator}")
        if event.ratio_denominator is not None and event.ratio_denominator <= 0:
            raise CorporateActionValidationError(f"Split ratio denominator must be positive: {event.ratio_denominator}")

def validate_adjusted_price_validation_result(result: AdjustedPriceValidationResult) -> None:
    pass

def validate_corporate_action_guard_result(result: CorporateActionGuardResult) -> None:
    pass

def create_corporate_action_event_id(symbol: str, action_type: CorporateActionType, ex_date: str) -> str:
    act_str = action_type.value if hasattr(action_type, "value") else str(action_type)
    return f"ca_{symbol}_{act_str}_{ex_date}"

def create_adjusted_price_validation_id(symbol: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"adj_val_{symbol}_{timestamp}"

def create_corporate_action_guard_id(symbol: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"ca_guard_{symbol}_{timestamp}"

def create_corporate_action_review_id(prefix: str = "corp_action_review") -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{prefix}_{timestamp}"
