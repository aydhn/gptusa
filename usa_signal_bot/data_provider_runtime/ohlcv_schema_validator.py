from typing import Any, Dict, List

from usa_signal_bot.core.exceptions import OhlcvSchemaValidationError

def canonical_ohlcv_columns() -> List[str]:
    return [
        "symbol",
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "adjusted_close",
        "volume",
        "source",
        "fetched_at_utc"
    ]

def validate_ohlcv_dataframe(df: Any) -> List[str]:
    errors = []
    if df is None or df.empty:
        errors.append("DataFrame is empty or None")
        return errors

    expected = canonical_ohlcv_columns()
    for col in expected:
        if col not in df.columns:
            # relax adjusted_close, source, fetched_at_utc for strict basic OHLCV
            if col in ["adjusted_close", "source", "fetched_at_utc"]:
                continue
            errors.append(f"Missing required column: {col}")

    # Volume negative check
    if "volume" in df.columns:
        if (df["volume"] < 0).any():
            errors.append("Negative volume detected")

    return errors

def validate_ohlcv_records(records: List[Dict[str, Any]]) -> List[str]:
    errors = []
    if not records:
        errors.append("Records list is empty")
        return errors

    expected = canonical_ohlcv_columns()
    for i, record in enumerate(records):
        for col in expected:
            if col in ["adjusted_close", "source", "fetched_at_utc"]:
                continue
            if col not in record:
                errors.append(f"Row {i} is missing required column: {col}")

        if "volume" in record and record["volume"] is not None:
            if float(record["volume"]) < 0:
                errors.append(f"Row {i} has negative volume")

    return errors

def normalize_ohlcv_records(records: List[Dict[str, Any]], source: str) -> List[Dict[str, Any]]:
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()

    normalized = []
    for r in records:
        n = {}
        n["symbol"] = r.get("symbol", "UNKNOWN")
        n["timestamp"] = r.get("timestamp")
        n["open"] = float(r.get("open", 0.0))
        n["high"] = float(r.get("high", 0.0))
        n["low"] = float(r.get("low", 0.0))
        n["close"] = float(r.get("close", 0.0))
        n["adjusted_close"] = float(r.get("adjusted_close", n["close"]))
        n["volume"] = float(r.get("volume", 0.0))
        n["source"] = source
        n["fetched_at_utc"] = r.get("fetched_at_utc", now)
        normalized.append(n)
    return normalized

def ohlcv_schema_validation_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors)
    }

def ohlcv_schema_validator_to_text(errors: List[str]) -> str:
    lines = [
        "=== OHLCV Schema Validator ===",
        f"Valid: {len(errors) == 0}",
        ""
    ]
    if errors:
        lines.append("Errors:")
        for e in errors:
            lines.append(f" - {e}")
    return "\n".join(lines)
