from typing import Any
import pandas as pd

from usa_signal_bot.core.enums import MomentumRegime
from usa_signal_bot.regime_map.timeframe_resampler import normalize_ohlcv_rows

def classify_momentum_regime(rows: list[dict[str, Any]], lookback: int = 20) -> tuple[MomentumRegime, dict[str, Any]]:
    rows = normalize_ohlcv_rows(rows)
    evidence = {
        "lookback": lookback,
        "roc_pct": None,
        "acceleration": None,
        "exhaustion_score": None
    }

    if len(rows) < lookback + 10:
        return MomentumRegime.INSUFFICIENT_DATA, evidence

    roc = rate_of_change_pct(rows, lookback)
    evidence["roc_pct"] = roc

    accel = momentum_acceleration_proxy(rows)
    evidence["acceleration"] = accel

    exh = momentum_exhaustion_score(rows)
    evidence["exhaustion_score"] = exh

    if roc is None:
        return MomentumRegime.INSUFFICIENT_DATA, evidence

    if roc > 10.0:
        if accel and accel > 0 and (exh is None or exh < 60):
            return MomentumRegime.STRONG_POSITIVE, evidence
        if exh and exh >= 70:
            return MomentumRegime.EXHAUSTED, evidence
        return MomentumRegime.POSITIVE, evidence
    elif roc > 0:
        if exh and exh >= 70:
             return MomentumRegime.EXHAUSTED, evidence
        return MomentumRegime.POSITIVE, evidence
    elif roc < -10.0:
        return MomentumRegime.STRONG_NEGATIVE, evidence
    elif roc < 0:
        return MomentumRegime.NEGATIVE, evidence
    else:
        return MomentumRegime.NEUTRAL, evidence

def rate_of_change_pct(rows: list[dict[str, Any]], lookback: int = 20) -> float | None:
    if len(rows) < lookback + 1:
        return None
    current = rows[-1]["close"]
    past = rows[-(lookback + 1)]["close"]
    if past == 0:
        return 0.0
    return (current - past) / past * 100.0

def momentum_acceleration_proxy(rows: list[dict[str, Any]]) -> float | None:
    # Compare recent ROC to older ROC
    if len(rows) < 40:
        return None
    roc_recent = rate_of_change_pct(rows, 10)
    roc_older = rate_of_change_pct(rows[:-10], 10)

    if roc_recent is None or roc_older is None:
        return None

    return roc_recent - roc_older

def momentum_exhaustion_score(rows: list[dict[str, Any]]) -> float | None:
    # Proxy for exhaustion: large run up followed by slowing momentum or divergence
    if len(rows) < 30:
        return None

    roc_30 = rate_of_change_pct(rows, 30)
    if roc_30 is None or roc_30 <= 0:
        return 0.0 # Not exhausted upside

    accel = momentum_acceleration_proxy(rows)
    if accel is None:
        return None

    # If up 20% but acceleration is negative, exhaustion is high
    score = 0.0
    if roc_30 > 15.0 and accel < 0:
        score = min(100.0, 50.0 + (roc_30 - 15) * 2 + abs(accel) * 5)
    return score

def momentum_regime_confidence(regime: MomentumRegime, evidence: dict[str, Any]) -> float | None:
    if regime == MomentumRegime.INSUFFICIENT_DATA:
        return 0.0
    return 75.0

def momentum_regime_to_text(regime: MomentumRegime, evidence: dict[str, Any] | None = None) -> str:
    text = f"Momentum Regime: {regime.value}"
    if evidence:
        roc = evidence.get('roc_pct')
        if roc is not None:
             text += f" | ROC: {roc:.2f}%"
    return text
