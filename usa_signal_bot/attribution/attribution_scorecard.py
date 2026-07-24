"""Attribution scorecard generator."""

from typing import List, Optional
from usa_signal_bot.core.enums import AttributionQuality
from usa_signal_bot.attribution.attribution_models import (
    AttributionTradeEvent,
    AttributionContribution,
    RiskAttributionContribution,
    SignalContribution,
    AttributionScorecard,
    create_attribution_scorecard_id
)

def calculate_attribution_quality_score(events: List[AttributionTradeEvent]) -> Optional[float]:
    if not events:
        return None
    valid_pnl = sum(1 for e in events if e.net_pnl_usd is not None)
    return (valid_pnl / len(events)) * 100.0

def calculate_signal_contribution_score(signal_contributions: List[SignalContribution]) -> Optional[float]:
    if not signal_contributions:
        return None
    positive = sum(1 for c in signal_contributions if c.net_pnl_usd > 0)
    return (positive / len(signal_contributions)) * 100.0

def calculate_cost_efficiency_score(events: List[AttributionTradeEvent]) -> Optional[float]:
    gross = sum(e.gross_pnl_usd for e in events if e.gross_pnl_usd is not None)
    cost = sum(e.total_cost_usd for e in events if e.total_cost_usd is not None)
    if gross <= 0:
        return 0.0
    efficiency = 100.0 - ((cost / gross) * 100.0)
    return max(0.0, min(100.0, efficiency))

def calculate_risk_contribution_score(risk_contributions: List[RiskAttributionContribution]) -> Optional[float]:
    if not risk_contributions:
        return None
    # Simplified mock score
    return 80.0

def build_attribution_scorecard(
    events: List[AttributionTradeEvent],
    performance_contributions: Optional[List[AttributionContribution]] = None,
    risk_contributions: Optional[List[RiskAttributionContribution]] = None,
    signal_contributions: Optional[List[SignalContribution]] = None
) -> AttributionScorecard:

    perf = performance_contributions or []
    risk = risk_contributions or []
    sig = signal_contributions or []

    total_gross = 0.0
    total_net = 0.0
    total_cost = 0.0

    for e in events:
        if e.gross_pnl_usd is not None:
            total_gross += e.gross_pnl_usd
        if e.net_pnl_usd is not None:
            total_net += e.net_pnl_usd
        if e.total_cost_usd is not None:
            total_cost += e.total_cost_usd

    pos_count = 0
    neg_count = 0
    for c in perf:
        if c.net_pnl_usd > 0:
            pos_count += 1
        elif c.net_pnl_usd < 0:
            neg_count += 1

    detrimental = 0
    for s in sig:
        if s.net_pnl_usd < 0:
            detrimental += 1
    high_risk = len(risk) # Mock

    from usa_signal_bot.attribution.pnl_attribution import classify_attribution_quality
    quality = classify_attribution_quality(events)

    scores = {
        "attribution_quality": calculate_attribution_quality_score(events),
        "signal_contribution": calculate_signal_contribution_score(sig),
        "cost_efficiency": calculate_cost_efficiency_score(events),
        "risk_contribution": calculate_risk_contribution_score(risk)
    }

    from datetime import datetime, timezone
    return AttributionScorecard(
        scorecard_id=create_attribution_scorecard_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        total_gross_pnl_usd=total_gross,
        total_net_pnl_usd=total_net,
        total_cost_usd=total_cost,
        total_trade_count=len(events),
        positive_contributor_count=pos_count,
        negative_contributor_count=neg_count,
        detrimental_signal_count=detrimental,
        high_risk_contributor_count=high_risk,
        attribution_quality=quality,
        summary_scores=scores
    )

def attribution_scorecard_to_text(scorecard: AttributionScorecard) -> str:
    lines = [
        "=== ATTRIBUTION SCORECARD ===",
        f"Quality: {scorecard.attribution_quality.value}",
        f"Total Net PnL: ${scorecard.total_net_pnl_usd:.2f}",
        f"Total Cost: ${scorecard.total_cost_usd:.2f}",
        f"Contributors: {scorecard.positive_contributor_count} Pos / {scorecard.negative_contributor_count} Neg",
        f"Detrimental Signals: {scorecard.detrimental_signal_count}",
        "Scores:"
    ]
    for k, v in scorecard.summary_scores.items():
        val = f"{v:.1f}" if v is not None else "N/A"
        lines.append(f"  - {k}: {val}")
    return "\n".join(lines)
