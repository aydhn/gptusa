"""Gap and volume anomaly detector."""
from typing import Any

def detect_price_gap_anomalies(symbol: str, rows: list[dict[str, Any]], threshold_pct: float = 15.0) -> list[dict[str, Any]]:
    anomalies = []
    if len(rows) < 2:
        return anomalies

    for i in range(1, len(rows)):
        prev = rows[i-1]
        curr = rows[i]

        prev_close = prev.get("close")
        curr_open = curr.get("open")

        if prev_close and curr_open and prev_close > 0:
            diff_pct = abs(curr_open - prev_close) / prev_close * 100
            if diff_pct >= threshold_pct:
                anomalies.append({
                    "date": curr.get("date", "")[:10],
                    "type": "PRICE_GAP",
                    "prev_close": prev_close,
                    "curr_open": curr_open,
                    "diff_pct": diff_pct
                })
    return anomalies

def detect_volume_anomalies(symbol: str, rows: list[dict[str, Any]], multiplier_threshold: float = 10.0) -> list[dict[str, Any]]:
    anomalies = []
    if len(rows) < 2:
        return anomalies

    for i in range(1, len(rows)):
        prev = rows[i-1]
        curr = rows[i]

        prev_vol = prev.get("volume")
        curr_vol = curr.get("volume")

        if prev_vol and curr_vol and prev_vol > 0:
            multiplier = curr_vol / prev_vol
            if multiplier >= multiplier_threshold:
                anomalies.append({
                    "date": curr.get("date", "")[:10],
                    "type": "VOLUME_SPIKE",
                    "prev_volume": prev_vol,
                    "curr_volume": curr_vol,
                    "multiplier": multiplier
                })
    return anomalies

def detect_ohlcv_reset_patterns(symbol: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    anomalies = []
    # E.g., looking for days where O=H=L=C and vol=0 (often a suspended or missing day filled with prev close)
    for r in rows:
        o, h, l, c, v = r.get("open"), r.get("high"), r.get("low"), r.get("close"), r.get("volume")
        if o and h and l and c and v is not None:
            if o == h == l == c and v == 0:
                anomalies.append({
                    "date": r.get("date", "")[:10],
                    "type": "OHLC_FLAT_VOL_ZERO",
                    "price": c
                })
    return anomalies

def gap_anomaly_summary_to_text(anomalies: list[dict[str, Any]]) -> str:
    lines = [f"Anomalies ({len(anomalies)}):"]
    for a in anomalies:
        lines.append(f"  {a['date']}: {a['type']} (Details: {a})")
    if not anomalies:
        lines.append("  None.")
    return "\n".join(lines)
