"""Adjusted close consistency validation."""
from typing import Any
from datetime import datetime, timezone
import math

from usa_signal_bot.core.enums import AdjustedPriceValidationStatus
from usa_signal_bot.corporate_actions.corporate_action_models import AdjustedPriceValidationResult, create_adjusted_price_validation_id
from usa_signal_bot.core.exceptions import AdjustedPriceValidationError

def validate_adjusted_close_consistency(symbol: str, rows: list[dict[str, Any]], tolerance_pct: float = 0.5) -> AdjustedPriceValidationResult:
    created_at = datetime.now(timezone.utc).isoformat()
    validation_id = create_adjusted_price_validation_id(symbol)

    if not rows:
        return AdjustedPriceValidationResult(
            validation_id=validation_id,
            symbol=symbol,
            created_at_utc=created_at,
            status=AdjustedPriceValidationStatus.INSUFFICIENT_DATA,
            row_count=0,
            adjusted_rows=0,
            inconsistent_rows=0,
            max_abs_diff_pct=None,
            warnings=["No rows provided."],
            errors=[]
        )

    adjusted_cnt = 0
    inconsistent_cnt = 0
    max_diff = 0.0

    missing_adj_close = False
    negative_close = False

    for r in rows:
        close = r.get("close")
        adj_close = r.get("adj_close")

        if close is None:
            continue

        if close < 0:
            negative_close = True

        if adj_close is None:
            missing_adj_close = True
            continue

        if adj_close < 0:
            negative_close = True

        adjusted_cnt += 1

        if close > 0:
            # We don't compare strictly if close != adj_close unless it's the very last day.
            # Usually adj_close == close for the most recent day, and differs backwards.
            # But we can calculate a ratio. For this check, if we just want to know if it's "inconsistent",
            # we might just flag if ratio drops suddenly (handled in rows_with_adjustment_ratio_change).
            # The 'consistency' check often ensures recent close == adj_close
            pass

    # Simple check: Does the most recent row have close == adj_close?
    warnings = []
    errors = []
    status = AdjustedPriceValidationStatus.CONSISTENT

    if negative_close:
        errors.append("Negative close or adj_close detected.")
        raise AdjustedPriceValidationError("Negative prices are invalid.")

    if missing_adj_close or adjusted_cnt == 0:
        warnings.append("Missing adjusted close data.")
        status = AdjustedPriceValidationStatus.MISSING_ADJUSTED_DATA

    else:
        # Check if latest day close == adj_close (within tolerance)
        latest_row = rows[-1]
        c = latest_row.get("close")
        a = latest_row.get("adj_close")
        if c and a and c > 0:
            diff_pct = abs(c - a) / c * 100
            max_diff = diff_pct
            if diff_pct > tolerance_pct:
                inconsistent_cnt += 1
                warnings.append(f"Latest adj_close ({a}) differs from close ({c}) by {diff_pct:.2f}% (tolerance {tolerance_pct}%)")
                status = AdjustedPriceValidationStatus.WARNING

        # Also check ratio jumps
        jumps = rows_with_adjustment_ratio_change(rows, threshold_pct=5.0)
        if jumps:
            inconsistent_cnt += len(jumps)
            warnings.append(f"Found {len(jumps)} rows with adjustment ratio jump.")
            status = AdjustedPriceValidationStatus.INCONSISTENT

    return AdjustedPriceValidationResult(
        validation_id=validation_id,
        symbol=symbol,
        created_at_utc=created_at,
        status=status,
        row_count=len(rows),
        adjusted_rows=adjusted_cnt,
        inconsistent_rows=inconsistent_cnt,
        max_abs_diff_pct=max_diff,
        warnings=warnings,
        errors=errors
    )

def adjusted_close_diff_pct(row: dict[str, Any]) -> float | None:
    c = row.get("close")
    a = row.get("adj_close")
    if c is not None and a is not None and c > 0:
        return abs(c - a) / c * 100
    return None

def rows_with_adjustment_ratio_change(rows: list[dict[str, Any]], threshold_pct: float = 5.0) -> list[dict[str, Any]]:
    jumps = []
    prev_ratio = None

    for r in rows:
        c = r.get("close")
        a = r.get("adj_close")
        if c and a and c > 0:
            ratio = a / c
            if prev_ratio is not None and prev_ratio > 0:
                change_pct = abs(ratio - prev_ratio) / prev_ratio * 100
                if change_pct > threshold_pct:
                    jumps.append(r)
            prev_ratio = ratio

    return jumps

def adjusted_price_validation_to_text(result: AdjustedPriceValidationResult) -> str:
    lines = [
        f"Adjusted Price Validation: {result.symbol} -> {result.status.value if hasattr(result.status, 'value') else str(result.status)}",
        f"  Total Rows: {result.row_count}",
        f"  Adjusted Rows: {result.adjusted_rows}",
        f"  Inconsistent Rows: {result.inconsistent_rows}",
    ]
    if result.max_abs_diff_pct is not None:
        lines.append(f"  Max Diff (Latest): {result.max_abs_diff_pct:.2f}%")

    for w in result.warnings:
        lines.append(f"  WARN: {w}")
    for e in result.errors:
        lines.append(f"  ERROR: {e}")

    return "\n".join(lines)
