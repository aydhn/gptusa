from typing import Any
from usa_signal_bot.core.enums import VolatilityMapRegime
import pandas as pd
import numpy as np

def realized_volatility_pct(rows: list[dict[str, Any]], lookback: int = 20) -> float | None:
    if len(rows) < lookback + 1:
        return None

    df = pd.DataFrame(rows[-lookback-1:])
    df['returns'] = df['close'].pct_change()

    vol = df['returns'].std() * np.sqrt(252) * 100 # Annualized percentage

    if pd.isna(vol):
        return None
    return float(vol)

def atr_percentile_proxy(rows: list[dict[str, Any]], lookback: int = 60) -> float | None:
    if len(rows) < lookback + 14: # Need 14 periods for ATR + lookback
        return None

    df = pd.DataFrame(rows)

    # Simple ATR approximation
    df['tr1'] = df['high'] - df['low']
    df['tr2'] = abs(df['high'] - df['close'].shift(1))
    df['tr3'] = abs(df['low'] - df['close'].shift(1))
    df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
    df['atr'] = df['tr'].rolling(window=14).mean()

    # Normalize ATR by close price to get a percentage
    df['atr_pct'] = (df['atr'] / df['close']) * 100

    atr_series = df['atr_pct'].dropna().tail(lookback)

    if len(atr_series) < lookback:
        return None

    current_atr = atr_series.iloc[-1]

    # Calculate rank/percentile
    percentile = (atr_series <= current_atr).mean() * 100
    return float(percentile)

def volatility_expansion_score(rows: list[dict[str, Any]]) -> float | None:
    # Compare recent vol to older vol
    recent_vol = realized_volatility_pct(rows, 10)
    older_vol = realized_volatility_pct(rows[:-10] if len(rows) > 10 else rows, 20)

    if recent_vol is None or older_vol is None or older_vol == 0:
        return None

    return (recent_vol / older_vol) * 100

def classify_volatility_map_regime(rows: list[dict[str, Any]], lookback: int = 20) -> tuple[VolatilityMapRegime, dict[str, Any]]:
    if len(rows) < 60: # Require at least 60 days for a decent baseline
        return VolatilityMapRegime.INSUFFICIENT_DATA, {"reason": "Not enough rows"}

    realized_vol = realized_volatility_pct(rows, lookback)
    atr_percentile = atr_percentile_proxy(rows, 60)
    expansion_score = volatility_expansion_score(rows)

    if realized_vol is None or atr_percentile is None:
        return VolatilityMapRegime.INSUFFICIENT_DATA, {"reason": "Could not compute volatility metrics"}

    evidence = {
        "realized_volatility_annualized": realized_vol,
        "atr_percentile": atr_percentile,
        "expansion_score": expansion_score
    }

    if atr_percentile < 20 and realized_vol < 15:
        return VolatilityMapRegime.COMPRESSED, evidence

    if expansion_score and expansion_score > 150: # Volatility expanding rapidly
         return VolatilityMapRegime.EXPANDING, evidence

    if atr_percentile > 80 or realized_vol > 40:
        return VolatilityMapRegime.EXTREME, evidence

    if atr_percentile > 60 or realized_vol > 25:
        return VolatilityMapRegime.HIGH, evidence

    return VolatilityMapRegime.NORMAL, evidence

def volatility_regime_confidence(regime: VolatilityMapRegime, evidence: dict[str, Any]) -> float | None:
    if regime == VolatilityMapRegime.INSUFFICIENT_DATA:
        return None
    return 80.0

def volatility_map_regime_to_text(regime: VolatilityMapRegime, evidence: dict[str, Any] | None = None) -> str:
    base = f"Volatility Regime: {regime.value}"
    if evidence and 'realized_volatility_annualized' in evidence:
        base += f", Realized Vol: {evidence['realized_volatility_annualized']:.1f}%"
    return base
