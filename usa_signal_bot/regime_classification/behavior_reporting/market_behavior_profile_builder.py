from typing import Any

from usa_signal_bot.core.enums import MarketBehaviorQuality, MarketBehaviorRiskFlag
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    MarketBehaviorProfileSpec, MarketBehaviorProfile
)

def build_market_behavior_profiles(
    transition_matrices: list[dict[str, Any]],
    persistence_profiles: list[dict[str, Any]],
    duration_profiles: list[dict[str, Any]],
    churn_diagnostics: list[dict[str, Any]],
    stability_diagnostics: list[dict[str, Any]],
    specs: list[MarketBehaviorProfileSpec] | None = None
) -> list[MarketBehaviorProfile]:
    from usa_signal_bot.regime_classification.behavior_reporting.market_behavior_profile_specs import build_default_market_behavior_profile_specs
    if specs is None:
        specs = build_default_market_behavior_profile_specs()

    payloads = {
        "transition_matrices": transition_matrices,
        "persistence_profiles": persistence_profiles,
        "duration_profiles": duration_profiles,
        "churn_diagnostics": churn_diagnostics,
        "stability_diagnostics": stability_diagnostics
    }

    profiles = []
    # Collect unique symbols
    symbols = set()
    for plist in payloads.values():
        for p in plist:
            if "symbol" in p:
                symbols.add(p["symbol"])

    if not symbols:
        symbols.add("UNKNOWN_SYMBOL")

    for symbol in symbols:
        for spec in specs:
            if spec.profile_name == "cross_symbol_behavior_profile":
                continue
            prof = build_behavior_profile_for_symbol(symbol, payloads, spec)
            profiles.append(prof)

    return profiles

def build_behavior_profile_for_symbol(symbol: str | None, payloads: dict[str, list[dict[str, Any]]], spec: MarketBehaviorProfileSpec) -> MarketBehaviorProfile:
    prof = MarketBehaviorProfile()
    prof.symbol = symbol
    prof.profile_name = spec.profile_name
    prof.profile_kind = spec.profile_kind

    snaps = {}
    diagnostic_notes = []

    for art_name in spec.required_artifacts:
        items = payloads.get(art_name, [])
        sym_items = [i for i in items if i.get("symbol") == symbol or symbol == "UNKNOWN_SYMBOL"]
        if not sym_items:
            prof.errors.append(f"Missing required artifact {art_name} for symbol {symbol}")
            continue
        item = sym_items[0]

        for sf in spec.source_fields:
            if sf in item:
                snaps[sf] = item[sf]
                if sf == "dominant_regime_label":
                    prof.dominant_regime_label = item[sf]
                if sf == "dominant_transition":
                    prof.dominant_transition = item[sf]
                if sf == "self_persistence_rate":
                    prof.persistence_score = float(item[sf])
                if sf == "stability_score":
                    prof.stability_score = float(item[sf])
                if sf == "churn_level":
                    prof.churn_level = item[sf]

        if "diagnostic_notes" in item:
            diagnostic_notes.extend(item["diagnostic_notes"])

    prof.metric_snapshot = snaps
    prof.diagnostic_notes = diagnostic_notes
    prof.summary = f"Research summary for {prof.profile_name}"
    prof.quality = infer_behavior_quality(prof)

    # Safety
    bad_terms = ["buy", "sell", "order", "portfolio_weight"]
    for t in bad_terms:
        if t in prof.summary.lower():
            prof.errors.append(f"Unsafe term '{t}' found in summary")
            prof.risk_flags.append(MarketBehaviorRiskFlag.INVESTMENT_ADVICE_LANGUAGE_RISK)

    return prof

def infer_behavior_quality(profile: MarketBehaviorProfile) -> MarketBehaviorQuality:
    if profile.errors:
        return MarketBehaviorQuality.INVALID
    if profile.warnings:
        return MarketBehaviorQuality.WARNING
    if not profile.metric_snapshot:
        return MarketBehaviorQuality.LOW
    return MarketBehaviorQuality.HIGH

def validate_market_behavior_profiles(profiles: list[MarketBehaviorProfile]) -> list[str]:
    errs = []
    for p in profiles:
        if not p.research_metadata_only: errs.append(f"Profile {p.profile_id} research_metadata_only must be true")
        if p.investment_advice: errs.append(f"Profile {p.profile_id} investment_advice must be false")
        if p.produces_trade_signal: errs.append(f"Profile {p.profile_id} produces_trade_signal must be false")
        if p.produces_order_decision: errs.append(f"Profile {p.profile_id} produces_order_decision must be false")
        if p.produces_portfolio_weights: errs.append(f"Profile {p.profile_id} produces_portfolio_weights must be false")
    return errs

def market_behavior_profiles_summary(profiles: list[MarketBehaviorProfile]) -> dict[str, Any]:
    return {"count": len(profiles), "symbols": list(set(p.symbol for p in profiles if p.symbol))}

def market_behavior_profiles_to_text(profiles: list[MarketBehaviorProfile], limit: int = 300) -> str:
    lines = [f"Profiles ({len(profiles)}):"]
    for p in profiles[:5]:
        lines.append(f"- {p.profile_name} for {p.symbol}: quality={p.quality.value}")
    return "\n".join(lines)[:limit]
