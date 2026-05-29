from typing import Any

from usa_signal_bot.core.enums import RegimeBehaviorSummaryKind, MarketBehaviorQuality, MarketBehaviorRiskFlag
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    MarketBehaviorProfile, RegimeBehaviorSummary
)

def build_regime_behavior_summaries(profiles: list[MarketBehaviorProfile]) -> list[RegimeBehaviorSummary]:
    sums = []
    # Just basic grouping by symbol and build generic ones for now
    symbols = set(p.symbol for p in profiles if p.symbol)
    for sym in symbols:
        sym_profs = [p for p in profiles if p.symbol == sym]
        sums.append(build_transition_summary(sym_profs))
        sums.append(build_persistence_summary(sym_profs))
        sums.append(build_duration_churn_summary(sym_profs))
        sums.append(build_stability_summary(sym_profs))

    sums.append(build_cross_symbol_summary(profiles))
    return sums

def _build_generic_summary(profiles: list[MarketBehaviorProfile], kind: RegimeBehaviorSummaryKind, title: str) -> RegimeBehaviorSummary:
    s = RegimeBehaviorSummary()
    if profiles and profiles[0].symbol:
        s.symbol = profiles[0].symbol
    s.summary_kind = kind
    s.title = title
    s.summary_text = f"Research summary for {title}. Data is derived heuristically."
    s.quality = MarketBehaviorQuality.HIGH
    return s

def build_transition_summary(profiles: list[MarketBehaviorProfile]) -> RegimeBehaviorSummary:
    return _build_generic_summary(profiles, RegimeBehaviorSummaryKind.REGIME_TRANSITION_SUMMARY, "Transition Summary")

def build_persistence_summary(profiles: list[MarketBehaviorProfile]) -> RegimeBehaviorSummary:
    return _build_generic_summary(profiles, RegimeBehaviorSummaryKind.REGIME_PERSISTENCE_SUMMARY, "Persistence Summary")

def build_duration_churn_summary(profiles: list[MarketBehaviorProfile]) -> RegimeBehaviorSummary:
    return _build_generic_summary(profiles, RegimeBehaviorSummaryKind.REGIME_DURATION_SUMMARY, "Duration/Churn Summary")

def build_stability_summary(profiles: list[MarketBehaviorProfile]) -> RegimeBehaviorSummary:
    return _build_generic_summary(profiles, RegimeBehaviorSummaryKind.REGIME_STABILITY_SUMMARY, "Stability Summary")

def build_cross_symbol_summary(profiles: list[MarketBehaviorProfile]) -> RegimeBehaviorSummary:
    return _build_generic_summary(profiles, RegimeBehaviorSummaryKind.CROSS_SYMBOL_SUMMARY, "Cross-Symbol Summary")

def validate_regime_behavior_summaries(summaries: list[RegimeBehaviorSummary]) -> list[str]:
    errs = []
    for s in summaries:
        if not s.research_metadata_only: errs.append(f"Summary {s.summary_id} research_metadata_only must be true")
        if s.investment_advice: errs.append(f"Summary {s.summary_id} investment_advice must be false")
        if s.produces_trade_signal: errs.append(f"Summary {s.summary_id} produces_trade_signal must be false")
        if s.produces_order_decision: errs.append(f"Summary {s.summary_id} produces_order_decision must be false")
        if s.produces_portfolio_weights: errs.append(f"Summary {s.summary_id} produces_portfolio_weights must be false")
    return errs

def regime_behavior_summaries_to_text(summaries: list[RegimeBehaviorSummary], limit: int = 300) -> str:
    lines = [f"Summaries ({len(summaries)}):"]
    for s in summaries[:5]:
        lines.append(f"- {s.title} for {s.symbol}: quality={s.quality.value}")
    return "\n".join(lines)[:limit]
