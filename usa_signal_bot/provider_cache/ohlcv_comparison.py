from typing import Any
from usa_signal_bot.core.exceptions import OhlcvComparisonError

def compare_ohlcv_records(source_a: list[dict[str, Any]], source_b: list[dict[str, Any]], tolerance_pct: float = 0.5) -> dict[str, Any]:
    if not source_a or not source_b:
        return {"error": "Missing source data"}

    last_a = source_a[-1]
    last_b = source_b[-1]

    close_a = float(last_a.get("close", 0)) if last_a.get("close") else None
    close_b = float(last_b.get("close", 0)) if last_b.get("close") else None

    close_diff = compute_close_diff_pct(close_a, close_b)

    vol_a = float(last_a.get("volume", 0)) if last_a.get("volume") else None
    vol_b = float(last_b.get("volume", 0)) if last_b.get("volume") else None
    vol_diff = compute_volume_diff_pct(vol_a, vol_b)

    row_diff = row_count_diff(source_a, source_b)
    ts_align = timestamp_alignment_score(source_a, source_b)

    material = False
    if close_diff is not None and close_diff > tolerance_pct:
        material = True
    if row_diff > 0:
        material = True

    return {
        "close_diff_pct": close_diff,
        "volume_diff_pct": vol_diff,
        "row_count_diff": row_diff,
        "timestamp_alignment": ts_align,
        "material_difference": material
    }

def compute_close_diff_pct(a: float | None, b: float | None) -> float | None:
    if a is None or b is None or a == 0:
        return None
    return abs(a - b) / abs(a) * 100.0

def compute_volume_diff_pct(a: float | None, b: float | None) -> float | None:
    if a is None or b is None or a == 0:
        return None
    return abs(a - b) / abs(a) * 100.0

def timestamp_alignment_score(source_a: list[dict[str, Any]], source_b: list[dict[str, Any]]) -> float | None:
    ts_a = set(r.get("timestamp") for r in source_a if r.get("timestamp"))
    ts_b = set(r.get("timestamp") for r in source_b if r.get("timestamp"))
    if not ts_a or not ts_b: return 0.0

    common = ts_a.intersection(ts_b)
    return len(common) / max(len(ts_a), len(ts_b)) * 100.0

def row_count_diff(source_a: list[dict[str, Any]], source_b: list[dict[str, Any]]) -> int:
    return abs(len(source_a) - len(source_b))

def ohlcv_comparison_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"material_diff": payload.get("material_difference", False)}

def ohlcv_comparison_to_text(payload: dict[str, Any]) -> str:
    return f"Material Difference: {payload.get('material_difference', False)}"
