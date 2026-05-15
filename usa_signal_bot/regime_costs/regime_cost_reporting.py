import json
from typing import Dict, Any
from usa_signal_bot.regime_costs.regime_cost_models import (
    CostRegimeSnapshot, RegimeCostMultiplier, RegimeCostCurveSelection,
    AdaptiveExecutionRealismDecision, RegimeAwareCostBreakdown, RegimeCostReview
)

def cost_regime_snapshot_to_text(item: CostRegimeSnapshot) -> str:
    return f"Regime Snapshot for {item.symbol}: Vol={item.volatility_regime.value}, Liq={item.liquidity_regime.value}, Spread={item.spread_regime.value}, Session={item.session_regime.value}, Lifecycle={item.lifecycle_regime.value} => Combined={item.combined_regime.value}"

def regime_cost_multiplier_to_text(item: RegimeCostMultiplier) -> str:
    return f"Regime Multipliers for {item.symbol}: Combined={item.combined_multiplier:.2f} (Vol={item.volatility_multiplier:.2f}, Liq={item.liquidity_multiplier:.2f}, Spread={item.spread_multiplier:.2f})"

def regime_cost_curve_selection_to_text(item: RegimeCostCurveSelection) -> str:
    return f"Cost Curve Selection for {item.symbol}: Profile={item.profile.value}, Curve ID={item.selected_curve_id}"

def adaptive_execution_realism_decision_to_text(item: AdaptiveExecutionRealismDecision) -> str:
    return f"Adaptive Execution Decision for {item.symbol}: {item.decision.value} (Combined Regime: {item.combined_regime.value})"

def regime_aware_cost_breakdown_to_text(item: RegimeAwareCostBreakdown) -> str:
    return f"Regime Cost Breakdown for {item.symbol}: Base BPS={item.total_base_cost_bps}, Adjusted BPS={item.total_adjusted_cost_bps}, Status={item.status.value}"

def regime_cost_review_to_text(item: RegimeCostReview, limit: int = 100) -> str:
    s = f"--- Regime Cost Review: {item.review_id} ---\n"
    s += f"Symbols Count: {len(item.symbols)}\n"
    s += f"Snapshots: {len(item.snapshots)}\n"
    s += f"Decisions: {len(item.adaptive_decisions)}\n"
    s += regime_cost_limitations_text()
    return s

def regime_cost_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Regime Cost Store: {summary.get('reviews_count', 0)} reviews found."

def regime_cost_limitations_text() -> str:
    return (
        "\n*** REGIME COST LIMITATIONS & DISCLAIMER ***\n"
        "1. No broker / live / demo order is sent.\n"
        "2. No real order book data is used.\n"
        "3. Regime cost curves are heuristic estimates, not guarantees.\n"
        "4. This output is for local backtesting/paper trading realism only.\n"
        "5. NOT INVESTMENT ADVICE. A PASS decision is NOT a live trading approval.\n"
        "********************************************\n"
    )
