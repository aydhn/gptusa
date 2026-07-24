from usa_signal_bot.calendar.calendar_models import SessionValidationResult

"""Provider calendar adapter."""
from typing import Any
from usa_signal_bot.providers.provider_models import (
    ProviderResponse,
    ProviderQualityScore,
)
from usa_signal_bot.core.enums import SessionValidationStatus
from usa_signal_bot.calendar.market_calendar import LocalMarketCalendar


def attach_calendar_metadata_to_provider_response(
    response: ProviderResponse, calendar: LocalMarketCalendar
) -> ProviderResponse:
    if not response.data:
        return response

    validation_results = validate_provider_response_calendar_alignment(
        response, calendar
    )

    if "calendar_validation" not in response.metadata:
        response.metadata["calendar_validation"] = {}

    for res in validation_results:
        response.metadata["calendar_validation"][res.symbol] = {
            "status": (
                res.status.value if hasattr(res.status, "value") else str(res.status)
            ),
            "missing_trading_days": res.missing_trading_days,
            "non_trading_day_rows": res.non_trading_day_rows,
            "early_close_rows": res.early_close_rows,
        }

    return response


def provider_response_calendar_summary(
    response: ProviderResponse, calendar: LocalMarketCalendar
) -> dict[str, Any]:
    validation_results = validate_provider_response_calendar_alignment(
        response, calendar
    )

    total_missing = 0
    total_non_trading = 0
    invalid_symbols = 0
    warning_symbols = 0

    invalid_status = SessionValidationStatus.INVALID
    warning_status = SessionValidationStatus.WARNING

    for r in validation_results:
        total_missing += r.missing_trading_days
        total_non_trading += r.non_trading_day_rows
        status = r.status
        if status is invalid_status:
            invalid_symbols += 1
        elif status is warning_status:
            warning_symbols += 1

    return {
        "symbols_checked": len(validation_results),
        "invalid_symbols": invalid_symbols,
        "warning_symbols": warning_symbols,
        "total_missing_days": total_missing,
        "total_non_trading_rows": total_non_trading,
    }


def calendar_quality_adjustment_from_session_validation(
    result: SessionValidationResult,
) -> dict[str, Any]:
    adjustment = {"score_multiplier": 1.0, "reasons": []}

    if result.status == SessionValidationStatus.INVALID:
        adjustment["score_multiplier"] *= 0.5
        adjustment["reasons"].append("Session validation INVALID.")
    elif result.status == SessionValidationStatus.WARNING:
        adjustment["score_multiplier"] *= 0.9
        adjustment["reasons"].append("Session validation WARNING.")

    if result.non_trading_day_rows > 0:
        adjustment["score_multiplier"] *= 0.8
        adjustment["reasons"].append(
            f"Contains {result.non_trading_day_rows} non-trading day rows."
        )

    if result.missing_trading_days > 5:
        adjustment["score_multiplier"] *= 0.85
        adjustment["reasons"].append(
            f"Missing {result.missing_trading_days} trading days."
        )

    return adjustment


def provider_quality_with_calendar_adjustment(
    score: ProviderQualityScore, session_results: list[SessionValidationResult]
) -> ProviderQualityScore:
    if not session_results:
        return score

    # Aggregate adjustments
    total_multiplier = 1.0
    all_reasons = []

    for res in session_results:
        adj = calendar_quality_adjustment_from_session_validation(res)
        if adj["score_multiplier"] < 1.0:
            total_multiplier *= adj["score_multiplier"]
            all_reasons.extend(adj["reasons"])

    # Apply floor to multiplier so we don't zero it completely just due to calendar issues
    total_multiplier = max(0.2, total_multiplier)

    adjusted_score = score.final_score * total_multiplier

    new_metadata = dict(score.metadata)
    if all_reasons:
        new_metadata["calendar_adjustment_reasons"] = list(set(all_reasons))
        new_metadata["calendar_multiplier"] = total_multiplier

    # Create new score instance to maintain immutability pattern if applicable
    return ProviderQualityScore(
        score_id=score.score_id,
        created_at_utc=score.created_at_utc,
        provider_name=score.provider_name,
        overall_status=score.overall_status,  # We keep original status or recalculate it depending on threshold
        final_score=adjusted_score,
        dimensions=score.dimensions,
        metadata=new_metadata,
    )


def validate_provider_response_calendar_alignment(
    response: ProviderResponse, calendar: LocalMarketCalendar
) -> list[SessionValidationResult]:
    from usa_signal_bot.calendar.session_validation import (
        validate_rows_against_calendar,
    )

    results = []
    for symbol, rows in response.data.items():
        if rows:
            res = validate_rows_against_calendar(symbol, rows, calendar)
            results.append(res)
    return results
