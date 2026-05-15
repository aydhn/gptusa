from typing import Any

from usa_signal_bot.core.enums import LiquidityMapRegime
from usa_signal_bot.regime_map.timeframe_resampler import normalize_ohlcv_rows

def classify_liquidity_map_regime(rows: list[dict[str, Any]], lookback: int = 60) -> tuple[LiquidityMapRegime, dict[str, Any]]:
    rows = normalize_ohlcv_rows(rows)
    evidence = {
        "lookback": lookback,
        "avg_dollar_volume": None,
        "thinning_score": None
    }

    if len(rows) < lookback:
        return LiquidityMapRegime.INSUFFICIENT_DATA, evidence

    recent_rows = rows[-lookback:]
    dvol = [r["close"] * r["volume"] for r in recent_rows if r["volume"] is not None]

    if not dvol:
        return LiquidityMapRegime.INSUFFICIENT_DATA, evidence

    avg_dvol = sum(dvol) / len(dvol)
    evidence["avg_dollar_volume"] = avg_dvol

    thinning = liquidity_thinning_score(rows)
    evidence["thinning_score"] = thinning

    # Arbitrary thresholds, should be configurable
    if avg_dvol < 2_000_000:
        return LiquidityMapRegime.ILLIQUID, evidence
    elif avg_dvol < 10_000_000:
        return LiquidityMapRegime.THIN, evidence
    elif thinning and thinning > 60:
        return LiquidityMapRegime.THINNING, evidence
    elif avg_dvol > 100_000_000:
        return LiquidityMapRegime.DEEP, evidence
    else:
        return LiquidityMapRegime.NORMAL, evidence

def dollar_volume_trend(rows: list[dict[str, Any]], lookback: int = 60) -> float | None:
    if len(rows) < lookback * 2:
        return None

    recent = rows[-lookback:]
    past = rows[-(lookback*2):-lookback]

    recent_dvol = sum([r["close"] * r.get("volume", 0) for r in recent]) / len(recent)
    past_dvol = sum([r["close"] * r.get("volume", 0) for r in past]) / len(past)

    if past_dvol == 0:
        return 0.0

    return (recent_dvol - past_dvol) / past_dvol * 100.0

def volume_compression_score(rows: list[dict[str, Any]], lookback: int = 60) -> float | None:
    trend = dollar_volume_trend(rows, lookback)
    if trend is None:
        return None
    if trend < 0:
        return min(100.0, abs(trend) * 2)
    return 0.0

def liquidity_thinning_score(rows: list[dict[str, Any]]) -> float | None:
    # Proxy
    return volume_compression_score(rows, 30)

def liquidity_regime_confidence(regime: LiquidityMapRegime, evidence: dict[str, Any]) -> float | None:
    if regime == LiquidityMapRegime.INSUFFICIENT_DATA:
        return 0.0
    return 90.0

def liquidity_map_regime_to_text(regime: LiquidityMapRegime, evidence: dict[str, Any] | None = None) -> str:
    text = f"Liquidity Regime: {regime.value}"
    if evidence:
        dvol = evidence.get("avg_dollar_volume")
        if dvol is not None:
             text += f" | Avg DVol: ${dvol:,.2f}"
    return text
