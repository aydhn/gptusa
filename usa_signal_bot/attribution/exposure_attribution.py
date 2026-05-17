"""Exposure concentration attribution."""

from typing import Any, Dict, List
from usa_signal_bot.core.enums import AttributionDimension
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent, RiskAttributionContribution
from usa_signal_bot.attribution.risk_attribution import concentration_risk_contribution_proxy

def exposure_contribution_by_symbol(events: List[AttributionTradeEvent]) -> List[RiskAttributionContribution]:
    return concentration_risk_contribution_proxy(events, AttributionDimension.SYMBOL)

def exposure_contribution_by_sector(events: List[AttributionTradeEvent]) -> List[RiskAttributionContribution]:
    return concentration_risk_contribution_proxy(events, AttributionDimension.SECTOR)

def exposure_contribution_by_cluster(events: List[AttributionTradeEvent]) -> List[RiskAttributionContribution]:
    return concentration_risk_contribution_proxy(events, AttributionDimension.CLUSTER)

def exposure_concentration_summary(events: List[AttributionTradeEvent]) -> Dict[str, Any]:
    symbols = exposure_contribution_by_symbol(events)
    sectors = exposure_contribution_by_sector(events)
    return {
        "top_symbol_exposure_pct": symbols[0].concentration_contribution_pct if symbols else 0.0,
        "top_sector_exposure_pct": sectors[0].concentration_contribution_pct if sectors else 0.0
    }

def exposure_attribution_to_text(contributions: List[RiskAttributionContribution], limit: int = 100) -> str:
    lines = ["--- Exposure Attribution ---"]
    for c in contributions[:limit]:
        lines.append(f"{c.name}: Exposure: {c.concentration_contribution_pct or 0.0:.1f}%")
    return "\n".join(lines)
