from typing import Any
from usa_signal_bot.regime_map.regime_map_models import (
    TimeframeRegimeSnapshot,
    MultiTimeframeRegimeConfirmation,
    CrossSectionalRegimeMap,
    SymbolRegimeAlignment,
    RegimeTransitionSignal,
    RegimeMapReview
)
from usa_signal_bot.regime_map.transition_detector import transition_detector_summary_to_text
from usa_signal_bot.regime_map.transition_risk import transition_risk_to_text

def timeframe_regime_snapshot_to_text(item: TimeframeRegimeSnapshot) -> str:
    lines = [
        f"Symbol: {item.symbol} | Timeframe: {item.timeframe.value}",
        f"  Trend: {item.trend_regime.value}",
        f"  Volatility: {item.volatility_regime.value}",
        f"  Momentum: {item.momentum_regime.value}",
        f"  Liquidity: {item.liquidity_regime.value}"
    ]
    if item.confidence is not None:
        lines.append(f"  Confidence: {item.confidence:.1f}%")
    return "\n".join(lines)

def multi_timeframe_confirmation_to_text(item: MultiTimeframeRegimeConfirmation) -> str:
    lines = [
        f"Symbol Confirmation: {item.symbol} | Status: {item.status.value}",
        f"  Dominant Trend: {item.dominant_trend_regime.value}",
        f"  Dominant Volatility: {item.dominant_volatility_regime.value}",
        f"  Dominant Momentum: {item.dominant_momentum_regime.value}",
        f"  Dominant Liquidity: {item.dominant_liquidity_regime.value}"
    ]
    if item.confidence is not None:
         lines.append(f"  Aggregate Confidence: {item.confidence:.1f}%")
    if item.conflicts:
         lines.append(f"  Conflicts: {', '.join(item.conflicts)}")
    return "\n".join(lines)

def cross_sectional_regime_map_to_text(item: CrossSectionalRegimeMap, limit: int = 100) -> str:
    lines = [
        f"Cross-Sectional Map: {item.universe_name} ({item.symbol_count} symbols)",
        f"  Regime: {item.cross_sectional_regime.value}",
        f"  Breadth: {item.breadth_regime.value}",
    ]
    if item.breadth_score is not None:
         lines.append(f"  Breadth Score: {item.breadth_score:.1f}")
    if item.dispersion_score is not None:
         lines.append(f"  Dispersion Score: {item.dispersion_score:.1f}")

    lines.append(f"  Uptrend Count: {item.uptrend_count} | Downtrend Count: {item.downtrend_count}")
    lines.append(f"  High Vol Count: {item.high_vol_count} | Thin Liq Count: {item.thin_liquidity_count}")

    return "\n".join(lines)

def symbol_regime_alignment_to_text(item: SymbolRegimeAlignment) -> str:
    lines = [
        f"Alignment: {item.symbol} vs {item.universe_name} -> {item.status.value}"
    ]
    if item.alignment_score is not None:
        lines.append(f"  Score: {item.alignment_score:.1f}")
    if item.conflict_reasons:
        lines.append("  Conflicts:")
        for r in item.conflict_reasons:
            lines.append(f"    - {r}")
    if item.recommended_guards:
        lines.append(f"  Recommended Guards: {', '.join(item.recommended_guards)}")
    return "\n".join(lines)

def regime_transition_signal_to_text(item: RegimeTransitionSignal) -> str:
    target = item.symbol if item.symbol else item.universe_name
    lines = [
        f"Transition Signal: {target} -> {item.transition_type.value}",
        f"  Risk Level: {item.risk.value}"
    ]
    if item.evidence:
         lines.append(f"  Evidence: {item.evidence}")
    return "\n".join(lines)

def regime_map_review_to_text(item: RegimeMapReview, limit: int = 100) -> str:
    lines = [
        f"=== REGIME MAP REVIEW: {item.report_type.value} ===",
        f"Universe: {item.universe_name}",
        f"Created At: {item.created_at_utc}",
        f"Guard Status: {item.guard_status.value}",
        ""
    ]

    if item.cross_sectional_map:
        lines.append("--- CROSS-SECTIONAL MAP ---")
        lines.append(cross_sectional_regime_map_to_text(item.cross_sectional_map))
        lines.append("")

    if item.transition_signals:
         lines.append("--- TRANSITION RISKS ---")
         lines.append(transition_risk_to_text(item.transition_signals))
         for s in item.transition_signals[:limit]:
             lines.append(f"  - {s.transition_type.value} ({s.risk.value})")
         lines.append("")

    if item.alignments:
        conflicts = [a for a in item.alignments if a.status.value in ["CONFLICTED", "DIVERGENT"]]
        lines.append(f"--- ALIGNMENTS ({len(item.alignments)} total, {len(conflicts)} conflicted) ---")
        for a in conflicts[:limit]:
             lines.append(symbol_regime_alignment_to_text(a))
        lines.append("")

    lines.append(regime_map_limitations_text())
    return "\n".join(lines)

def regime_map_store_summary_to_text(summary: dict[str, Any]) -> str:
    lines = [
        "Regime Map Store Summary:",
        f"  Snapshots: {summary.get('snapshots', 0)}",
        f"  Confirmations: {summary.get('confirmations', 0)}",
        f"  Cross-Sectional Maps: {summary.get('cross_sectional_maps', 0)}",
        f"  Alignments: {summary.get('alignments', 0)}",
        f"  Transitions: {summary.get('transitions', 0)}",
        f"  Reviews: {summary.get('reviews', 0)}"
    ]
    return "\n".join(lines)

def regime_map_limitations_text() -> str:
    return (
        "*** REGIME MAP LIMITATIONS ***\n"
        "1. This is a heuristic evaluation for local research purposes only.\n"
        "2. Does not constitute investment advice.\n"
        "3. Transition risks are not definitive predictions.\n"
        "4. A 'CONFIRMED' or 'ALIGNED' status is NOT a live trading approval.\n"
        "5. No broker execution or real market order is associated with this report."
    )
