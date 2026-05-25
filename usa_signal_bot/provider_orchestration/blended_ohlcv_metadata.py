from typing import Any
from usa_signal_bot.core.enums import SourceBlendMethod

def build_blended_ohlcv_metadata(symbol: str, included_sources: list[str], method: SourceBlendMethod, record_count: int, confidence_score: float | None = None) -> dict[str, Any]:
    return {
        "symbol": symbol,
        "included_sources": included_sources,
        "method": method.value,
        "record_count": record_count,
        "confidence_score": confidence_score,
        "is_blended_metadata": True,
        "contains_trade_signal": False,
        "contains_order_decision": False
    }

def validate_blended_ohlcv_metadata(payload: dict[str, Any]) -> list[str]:
    errors = []
    if payload.get("contains_trade_signal", True):
        errors.append("contains_trade_signal must be False")
    if payload.get("contains_order_decision", True):
        errors.append("contains_order_decision must be False")
    return errors

def blended_ohlcv_metadata_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "symbol": payload.get("symbol"),
        "method": payload.get("method"),
        "confidence": payload.get("confidence_score")
    }

def blended_ohlcv_metadata_to_text(payload: dict[str, Any]) -> str:
    lines = ["--- Blended OHLCV Metadata ---"]
    for k, v in payload.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)
