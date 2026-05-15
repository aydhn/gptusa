from typing import Any
from usa_signal_bot.regime_map.regime_map_models import (
    TimeframeRegimeSnapshot,
    MultiTimeframeRegimeConfirmation,
    CrossSectionalRegimeMap,
    SymbolRegimeAlignment,
    RegimeTransitionSignal,
    RegimeMapReview
)
from usa_signal_bot.regime_map.trend_confirmation import trend_regime_to_text
from usa_signal_bot.regime_map.volatility_confirmation import volatility_map_regime_to_text
from usa_signal_bot.regime_map.momentum_confirmation import momentum_regime_to_text
from usa_signal_bot.regime_map.liquidity_confirmation import liquidity_map_regime_to_text
from usa_signal_bot.regime_map.symbol_regime_alignment import symbol_regime_alignment_to_text
from usa_signal_bot.regime_map.transition_risk import transition_risk_to_text

def timeframe_regime_snapshot_to_text(item: TimeframeRegimeSnapshot) -> str:
    return (f"Snapshot [{item.symbol} | {item.timeframe.value}]:\n"
            f"  {trend_regime_to_text(item.trend_regime)}\n"
            f"  {volatility_map_regime_to_text(item.volatility_regime)}\n"
            f"  {momentum_regime_to_text(item.momentum_regime)}\n"
            f"  {liquidity_map_regime_to_text(item.liquidity_regime)}\n"
            f"  Confidence: {item.confidence if item.confidence is not None else 'N/A'}")

def multi_timeframe_confirmation_to_text(item: MultiTimeframeRegimeConfirmation) -> str:
    text = (f"Confirmation [{item.symbol}]: {item.status.value}\n"
            f"  Dominant Trend: {item.dominant_trend_regime.value}\n"
            f"  Dominant Volatility: {item.dominant_volatility_regime.value}\n"
            f"  Dominant Momentum: {item.dominant_momentum_regime.value}\n"
            f"  Dominant Liquidity: {item.dominant_liquidity_regime.value}\n")
    if item.conflicts:
        text += f"  Conflicts: {'; '.join(item.conflicts)}\n"
    return text

def cross_sectional_regime_map_to_text(item: CrossSectionalRegimeMap, limit: int = 100) -> str:
    return (f"Cross Sectional Map [{item.universe_name}]:\n"
            f"  Regime: {item.cross_sectional_regime.value}\n"
            f"  Breadth: {item.breadth_regime.value} (Score: {item.breadth_score if item.breadth_score is not None else 'N/A'})\n"
            f"  Dispersion: {item.dispersion_score if item.dispersion_score is not None else 'N/A'}\n"
            f"  Symbols: {item.symbol_count} (Uptrend: {item.uptrend_count}, Downtrend: {item.downtrend_count}, Range: {item.range_count})")

def regime_transition_signal_to_text(item: RegimeTransitionSignal) -> str:
    target = item.symbol or item.universe_name or "Unknown"
    return f"Transition [{target}]: {item.transition_type.value} -> Risk: {item.risk.value}"

def regime_map_review_to_text(item: RegimeMapReview, limit: int = 100) -> str:
    text = f"=== Regime Map Review [{item.universe_name}] ===\n"
    text += f"Report Type: {item.report_type.value}\n"
    text += f"Guard Status: {item.guard_status.value}\n\n"

    if item.cross_sectional_map:
        text += cross_sectional_regime_map_to_text(item.cross_sectional_map) + "\n\n"

    text += "--- Alignments ---\n"
    for a in item.alignments[:limit]:
        text += symbol_regime_alignment_to_text(a) + "\n"

    if item.transition_signals:
        text += "\n--- Transitions ---\n"
        text += transition_risk_to_text(item.transition_signals) + "\n"
        for t in item.transition_signals[:limit]:
             text += regime_transition_signal_to_text(t) + "\n"

    text += "\n" + regime_map_limitations_text()
    return text

def regime_map_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Regime Map Store: {summary['review_count']} reviews total."

def regime_map_limitations_text() -> str:
    return ("DISCLAIMER: Regime map analysis is based on heuristics and historical data. "
            "It is for local research only. A PASS or CONFIRMED status is NOT investment advice "
            "and does NOT guarantee market performance. No live broker execution is performed.")
