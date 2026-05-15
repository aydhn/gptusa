from typing import Any
from usa_signal_bot.core.enums import LiquidityMapRegime
import pandas as pd
import numpy as np

def dollar_volume(rows: list[dict[str, Any]]) -> list[float]:
    return [r.get('close', 0) * r.get('volume', 0) for r in rows]

def dollar_volume_trend(rows: list[dict[str, Any]], lookback: int = 60) -> float | None:
    if len(rows) < lookback:
        return None

    dvol = dollar_volume(rows)
    recent_dvol = np.mean(dvol[-20:])
    older_dvol = np.mean(dvol[-lookback:-20])

    if older_dvol == 0:
        return 0.0

    return ((recent_dvol - older_dvol) / older_dvol) * 100

def volume_compression_score(rows: list[dict[str, Any]], lookback: int = 60) -> float | None:
    if len(rows) < lookback:
        return None

    dvol = dollar_volume(rows)
    current_dvol = np.mean(dvol[-5:])
    max_dvol = np.max(dvol[-lookback:])

    if max_dvol == 0:
        return None

    return (1.0 - (current_dvol / max_dvol)) * 100

def liquidity_thinning_score(rows: list[dict[str, Any]]) -> float | None:
     trend = dollar_volume_trend(rows)
     compression = volume_compression_score(rows)

     if trend is None or compression is None:
         return None

     score = 0
     if trend < -20:
         score += 50
     if compression > 60:
         score += 50

     return score

def classify_liquidity_map_regime(rows: list[dict[str, Any]], lookback: int = 60) -> tuple[LiquidityMapRegime, dict[str, Any]]:
    if len(rows) < lookback:
        return LiquidityMapRegime.INSUFFICIENT_DATA, {"reason": "Not enough rows"}

    dvol = dollar_volume(rows)
    avg_dvol = np.mean(dvol[-lookback:])

    thinning = liquidity_thinning_score(rows)

    evidence = {
        "avg_dollar_volume": avg_dvol,
        "thinning_score": thinning
    }

    if avg_dvol < 1_000_000:
        return LiquidityMapRegime.ILLIQUID, evidence

    if avg_dvol < 5_000_000:
        return LiquidityMapRegime.THIN, evidence

    if thinning and thinning >= 80:
        return LiquidityMapRegime.THINNING, evidence

    if avg_dvol > 50_000_000:
        return LiquidityMapRegime.DEEP, evidence

    return LiquidityMapRegime.NORMAL, evidence

def liquidity_regime_confidence(regime: LiquidityMapRegime, evidence: dict[str, Any]) -> float | None:
     if regime == LiquidityMapRegime.INSUFFICIENT_DATA:
         return None
     return 90.0

def liquidity_map_regime_to_text(regime: LiquidityMapRegime, evidence: dict[str, Any] | None = None) -> str:
    base = f"Liquidity Regime: {regime.value}"
    if evidence and 'avg_dollar_volume' in evidence:
        base += f", Avg DVol: ${evidence['avg_dollar_volume']:,.0f}"
    return base
