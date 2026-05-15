from typing import Any
from usa_signal_bot.core.enums import MomentumRegime
import pandas as pd

def rate_of_change_pct(rows: list[dict[str, Any]], lookback: int = 20) -> float | None:
    if len(rows) <= lookback:
        return None

    current = rows[-1]['close']
    past = rows[-lookback-1]['close']

    if past == 0:
        return 0.0

    return ((current - past) / past) * 100

def momentum_acceleration_proxy(rows: list[dict[str, Any]]) -> float | None:
    roc_short = rate_of_change_pct(rows, 10)
    roc_long = rate_of_change_pct(rows, 20)

    if roc_short is None or roc_long is None:
        return None

    # Proxy for acceleration: is short term ROC outpacing long term (normalized)
    return roc_short - (roc_long / 2)

def momentum_exhaustion_score(rows: list[dict[str, Any]]) -> float | None:
    if len(rows) < 40:
        return None

    roc_recent = rate_of_change_pct(rows, 5)
    roc_older = rate_of_change_pct(rows[:-5], 20)

    if roc_recent is None or roc_older is None:
        return None

    # High older ROC but negative or flat recent ROC indicates exhaustion
    if roc_older > 10 and roc_recent < 0:
        return 80.0
    if roc_older > 15 and roc_recent < 2:
        return 60.0

    return 10.0

def classify_momentum_regime(rows: list[dict[str, Any]], lookback: int = 20) -> tuple[MomentumRegime, dict[str, Any]]:
    if len(rows) <= lookback:
         return MomentumRegime.INSUFFICIENT_DATA, {"reason": "Not enough rows"}

    roc = rate_of_change_pct(rows, lookback)
    acceleration = momentum_acceleration_proxy(rows)
    exhaustion = momentum_exhaustion_score(rows)

    if roc is None:
        return MomentumRegime.INSUFFICIENT_DATA, {"reason": "Could not compute ROC"}

    evidence = {
        "roc_pct": roc,
        "acceleration": acceleration,
        "exhaustion_score": exhaustion
    }

    if exhaustion and exhaustion > 70:
        return MomentumRegime.EXHAUSTED, evidence

    if roc > 10 and acceleration and acceleration > 2:
        return MomentumRegime.STRONG_POSITIVE, evidence

    if roc > 2:
        return MomentumRegime.POSITIVE, evidence

    if roc < -10 and acceleration and acceleration < -2:
        return MomentumRegime.STRONG_NEGATIVE, evidence

    if roc < -2:
        return MomentumRegime.NEGATIVE, evidence

    return MomentumRegime.NEUTRAL, evidence

def momentum_regime_confidence(regime: MomentumRegime, evidence: dict[str, Any]) -> float | None:
     if regime == MomentumRegime.INSUFFICIENT_DATA:
         return None
     return 75.0

def momentum_regime_to_text(regime: MomentumRegime, evidence: dict[str, Any] | None = None) -> str:
    base = f"Momentum Regime: {regime.value}"
    if evidence and 'roc_pct' in evidence:
        base += f", ROC: {evidence['roc_pct']:.2f}%"
    return base
