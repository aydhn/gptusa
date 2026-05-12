from typing import Any
from datetime import datetime, timezone
import dateutil.parser

from usa_signal_bot.providers.provider_models import ProviderResponse

def validate_provider_response_schema(response: ProviderResponse) -> tuple[bool, list[str], list[str]]:
    warnings = []
    errors = []

    if not isinstance(response.data, dict):
        errors.append("Response data is not a dictionary")
        return False, warnings, errors

    for symbol, payload in response.data.items():
        if not isinstance(payload, list):
            errors.append(f"Payload for symbol {symbol} is not a list")
            continue

        valid, row_warns, row_errs = validate_ohlcv_rows(payload)
        warnings.extend([f"{symbol}: {w}" for w in row_warns])
        errors.extend([f"{symbol}: {e}" for e in row_errs])

    return len(errors) == 0, warnings, errors

def validate_ohlcv_payload(payload: dict[str, Any]) -> tuple[bool, list[str], list[str]]:
    # Simple wrapper for now
    if not isinstance(payload, dict):
        return False, [], ["Payload must be a dict"]
    return True, [], []

def validate_ohlcv_rows(rows: list[dict[str, Any]]) -> tuple[bool, list[str], list[str]]:
    warnings = []
    errors = []

    required_cols = {"datetime", "open", "high", "low", "close", "volume"}
    dates = set()

    for i, row in enumerate(rows):
        missing = required_cols - set(row.keys())
        if missing:
            errors.append(f"Row {i} missing columns: {missing}")
            continue

        try:
            o = float(row["open"])
            h = float(row["high"])
            l = float(row["low"])
            c = float(row["close"])
            v = float(row["volume"])

            if h < max(o, c):
                errors.append(f"Row {i} high ({h}) < max(open, close) ({max(o,c)})")
            if l > min(o, c):
                errors.append(f"Row {i} low ({l}) > min(open, close) ({min(o,c)})")
            if v < 0:
                errors.append(f"Row {i} volume ({v}) < 0")
            if c <= 0:
                errors.append(f"Row {i} close ({c}) <= 0")

            dt = row["datetime"]
            if not dt:
                errors.append(f"Row {i} empty datetime")
            else:
                if dt in dates:
                    warnings.append(f"Row {i} duplicate datetime: {dt}")
                dates.add(dt)

            if "adj close" in row and row["adj close"] is not None:
                ac = float(row["adj close"])
                if ac <= 0:
                    errors.append(f"Row {i} adjusted close ({ac}) <= 0")

        except (ValueError, TypeError) as e:
            errors.append(f"Row {i} numeric conversion error: {str(e)}")

    return len(errors) == 0, warnings, errors

def validate_freshness(rows: list[dict[str, Any]], max_staleness_days: int | None = None) -> tuple[bool, list[str], list[str]]:
    warnings = []
    errors = []

    if not rows:
        return False, [], ["No rows to check freshness"]

    try:
        # Assuming sorted ascending
        last_row = rows[-1]
        dt_str = last_row.get("datetime")
        if not dt_str:
            return False, [], ["Last row missing datetime"]

        dt = dateutil.parser.isoparse(dt_str)
        now = datetime.now(timezone.utc)
        diff_days = (now - dt).days

        if max_staleness_days is not None and diff_days > max_staleness_days:
            warnings.append(f"Data is stale by {diff_days} days (max {max_staleness_days})")

    except Exception as e:
        errors.append(f"Freshness check failed: {str(e)}")

    return len(errors) == 0, warnings, errors

def validate_completeness(rows: list[dict[str, Any]], min_rows: int = 20) -> tuple[bool, list[str], list[str]]:
    warnings = []
    errors = []

    if len(rows) < min_rows:
        warnings.append(f"Only {len(rows)} rows returned (expected at least {min_rows})")

    return len(errors) == 0, warnings, errors

def validate_adjusted_close_consistency(rows: list[dict[str, Any]]) -> tuple[bool, list[str], list[str]]:
    warnings = []
    errors = []

    # We could do a basic sanity check that adj_close <= close mostly,
    # but due to splits/dividends it can be tricky.
    # Just checking positivity which is handled in validate_ohlcv_rows
    return True, warnings, errors

def provider_response_validation_summary(response: ProviderResponse) -> dict[str, Any]:
    valid_schema, schema_warns, schema_errs = validate_provider_response_schema(response)

    summary = {
        "valid_schema": valid_schema,
        "schema_errors": len(schema_errs),
        "schema_warnings": len(schema_warns),
        "total_rows": response.row_count,
        "total_symbols": response.symbol_count
    }

    return summary
