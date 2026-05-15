from typing import Any
import pandas as pd
import numpy as np

from usa_signal_bot.core.enums import VolatilityMapRegime
from usa_signal_bot.regime_map.timeframe_resampler import normalize_ohlcv_rows

def classify_volatility_map_regime(rows: list[dict[str, Any]], lookback: int = 20) -> tuple[VolatilityMapRegime, dict[str, Any]]:
    rows = normalize_ohlcv_rows(rows)
    evidence = {
        "lookback": lookback,
        "realized_vol_pct": None,
        "atr_pct": None,
        "vol_expansion_score": None
    }

    if len(rows) < lookback + 10:
        return VolatilityMapRegime.INSUFFICIENT_DATA, evidence

    realized_vol = realized_volatility_pct(rows, lookback)
    evidence["realized_vol_pct"] = realized_vol

    atr_pct = atr_percentile_proxy(rows, lookback=60) # Compare to longer history
    evidence["atr_pct"] = atr_pct

    vol_exp = volatility_expansion_score(rows)
    evidence["vol_expansion_score"] = vol_exp

    if realized_vol is None or atr_pct is None:
        return VolatilityMapRegime.INSUFFICIENT_DATA, evidence

    # Heuristics
    if realized_vol < 1.0 and atr_pct < 20:
        return VolatilityMapRegime.COMPRESSED, evidence
    elif vol_exp is not None and vol_exp > 70 and realized_vol > 2.0:
        if realized_vol > 5.0 or atr_pct > 90:
             return VolatilityMapRegime.EXTREME, evidence
        return VolatilityMapRegime.EXPANDING, evidence
    elif realized_vol > 3.0 or atr_pct > 75:
        return VolatilityMapRegime.HIGH, evidence
    else:
        return VolatilityMapRegime.NORMAL, evidence

def realized_volatility_pct(rows: list[dict[str, Any]], lookback: int = 20) -> float | None:
    if len(rows) < lookback + 1:
        return None

    closes = [r["close"] for r in rows[-(lookback+1):]]
    returns = []
    for i in range(1, len(closes)):
        prev = closes[i-1]
        if prev > 0:
            returns.append((closes[i] - prev) / prev)
        else:
            returns.append(0)

    if not returns:
        return None

    std_dev = np.std(returns)
    # Annualized approx (assuming daily rows, approx 252 days)
    # But since this might be weekly/monthly, we just return the raw std_dev * 100 for simplicity as a proxy
    return float(std_dev * 100.0)

def calculate_atr(rows: list[dict[str, Any]], period: int = 14) -> list[float]:
    atrs = []
    if len(rows) < period + 1:
        return atrs

    tr_list = []
    for i in range(1, len(rows)):
        high = rows[i]["high"]
        low = rows[i]["low"]
        prev_close = rows[i-1]["close"]

        tr1 = high - low
        tr2 = abs(high - prev_close)
        tr3 = abs(low - prev_close)
        tr = max(tr1, tr2, tr3)
        tr_list.append(tr)

    # Simple SMA of TR for ATR proxy
    for i in range(period, len(tr_list) + 1):
        atr = sum(tr_list[i-period:i]) / period
        atrs.append(atr)

    return atrs

def atr_percentile_proxy(rows: list[dict[str, Any]], lookback: int = 60) -> float | None:
    if len(rows) < lookback + 14 + 1:
        return None

    # Get last 'lookback' ATR values
    all_rows = rows[-(lookback + 14 + 1):]
    atrs = calculate_atr(all_rows, 14)

    if not atrs or len(atrs) < 2:
        return None

    current_atr = atrs[-1]
    current_close = rows[-1]["close"]
    if current_close == 0:
        return None

    current_atr_pct = current_atr / current_close * 100

    # Calculate historical ATR%
    hist_atr_pcts = []
    for i in range(len(atrs)):
        c = all_rows[14 + i]["close"]
        if c > 0:
            hist_atr_pcts.append(atrs[i] / c * 100)

    if not hist_atr_pcts:
        return None

    # Calculate percentile
    below_count = sum(1 for val in hist_atr_pcts if val < current_atr_pct)
    return (below_count / len(hist_atr_pcts)) * 100.0

def volatility_expansion_score(rows: list[dict[str, Any]]) -> float | None:
    if len(rows) < 40:
        return None

    short_vol = realized_volatility_pct(rows, 10)
    long_vol = realized_volatility_pct(rows, 30)

    if short_vol is None or long_vol is None or long_vol == 0:
        return None

    ratio = short_vol / long_vol
    # Cap score at 100, ratio 1.0 = score 50
    score = min(100.0, max(0.0, (ratio - 0.5) * 100))
    return score

def volatility_regime_confidence(regime: VolatilityMapRegime, evidence: dict[str, Any]) -> float | None:
    if regime == VolatilityMapRegime.INSUFFICIENT_DATA:
        return 0.0
    # Simple heuristic
    return 80.0

def volatility_map_regime_to_text(regime: VolatilityMapRegime, evidence: dict[str, Any] | None = None) -> str:
    text = f"Volatility Regime: {regime.value}"
    if evidence:
         text += f" | Realized Vol: {evidence.get('realized_vol_pct', 0):.2f}%"
    return text
