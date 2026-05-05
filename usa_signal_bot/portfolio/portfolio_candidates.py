from typing import List, Tuple, Optional
from usa_signal_bot.portfolio.portfolio_models import PortfolioCandidate
from usa_signal_bot.core.enums import PortfolioCandidateStatus, RiskDecisionStatus
from usa_signal_bot.risk.risk_models import RiskDecision
from usa_signal_bot.strategies.candidate_selection import SelectedCandidate

def portfolio_candidate_from_risk_decision(decision: RiskDecision) -> PortfolioCandidate:
    status = PortfolioCandidateStatus.UNKNOWN
    if decision.status in [RiskDecisionStatus.APPROVED, RiskDecisionStatus.REDUCED]:
        status = PortfolioCandidateStatus.ELIGIBLE
    elif decision.status == RiskDecisionStatus.REJECTED:
        status = PortfolioCandidateStatus.REJECTED
    elif decision.status == RiskDecisionStatus.NEEDS_REVIEW:
        status = PortfolioCandidateStatus.NEEDS_REVIEW

    return PortfolioCandidate(
        candidate_id=decision.decision_id,
        signal_id=getattr(decision, 'signal_id', None),
        symbol=decision.symbol,
        timeframe=decision.timeframe,
        strategy_name=getattr(decision, 'strategy_name', None),
        action=decision.action,
        rank_score=getattr(decision, 'rank_score', None),
        confidence=getattr(decision, 'confidence', None),
        risk_score=getattr(decision, 'risk_score', None),
        approved_quantity=decision.approved_quantity,
        approved_notional=decision.approved_notional,
        price=getattr(decision, 'price', None),
        volatility_value=getattr(decision, 'volatility_value', None),
        atr_value=getattr(decision, 'atr_value', None),
        risk_flags=getattr(decision, 'risk_flags', []),
        status=status,
        metadata={"rejection_reasons": decision.rejection_reasons} if getattr(decision, 'rejection_reasons', None) else {}
    )

def portfolio_candidates_from_risk_decisions(decisions: List[RiskDecision]) -> List[PortfolioCandidate]:
    return [portfolio_candidate_from_risk_decision(d) for d in decisions]

def portfolio_candidate_from_selected_candidate(candidate: SelectedCandidate, default_price: Optional[float] = None) -> PortfolioCandidate:
    from usa_signal_bot.portfolio.portfolio_models import create_portfolio_basket_id

    sig = candidate.ranked_signal.signal
    rs = candidate.ranked_signal

    price = sig.price if getattr(sig, 'price', None) is not None else default_price

    return PortfolioCandidate(
        candidate_id=f"cand_{sig.symbol}_{sig.timeframe}",
        signal_id=sig.signal_id,
        symbol=sig.symbol,
        timeframe=sig.timeframe,
        strategy_name=sig.strategy_name,
        action=sig.action,
        rank_score=rs.rank_score,
        confidence=sig.confidence,
        risk_score=rs.penalties.get("RISK_PENALTY", 50.0),
        approved_quantity=0.0, # Will be set by allocation
        approved_notional=0.0, # Will be set by allocation
        price=price,
        volatility_value=getattr(sig, 'volatility_value', None),
        atr_value=getattr(sig, 'atr_value', None),
        risk_flags=getattr(sig, 'risk_flags', []),
        status=PortfolioCandidateStatus.ELIGIBLE,
        metadata={}
    )

def filter_eligible_portfolio_candidates(candidates: List[PortfolioCandidate]) -> List[PortfolioCandidate]:
    return [c for c in candidates if c.status == PortfolioCandidateStatus.ELIGIBLE]

def reject_ineligible_portfolio_candidates(candidates: List[PortfolioCandidate]) -> Tuple[List[PortfolioCandidate], List[PortfolioCandidate]]:
    eligible = []
    ineligible = []
    for c in candidates:
        if c.status == PortfolioCandidateStatus.ELIGIBLE and c.approved_notional >= 0:
            eligible.append(c)
        else:
            ineligible.append(c)
    return eligible, ineligible

def infer_candidate_price(candidate: PortfolioCandidate) -> Optional[float]:
    return candidate.price

def sort_candidates_for_allocation(candidates: List[PortfolioCandidate]) -> List[PortfolioCandidate]:
    def sort_key(c: PortfolioCandidate):
        rank = c.rank_score if c.rank_score is not None else -1
        risk = c.risk_score if c.risk_score is not None else 100
        conf = c.confidence if c.confidence is not None else -1
        return (rank, -risk, conf, c.symbol)

    return sorted(candidates, key=sort_key, reverse=True)

def portfolio_candidates_to_text(candidates: List[PortfolioCandidate], limit: int = 30) -> str:
    lines = []
    lines.append(f"Portfolio Candidates ({len(candidates)} total)")
    lines.append("-" * 50)
    for i, c in enumerate(candidates[:limit]):
        status_str = c.status.value if hasattr(c.status, 'value') else str(c.status)
        price_str = f"{c.price:.2f}" if c.price is not None else "N/A"
        notional_str = f"{c.approved_notional:.2f}"
        lines.append(f"{i+1}. {c.symbol} ({c.timeframe}) - {status_str} | Price: {price_str} | Notional: {notional_str}")

    if len(candidates) > limit:
        lines.append(f"... and {len(candidates) - limit} more.")

    return "\n".join(lines)
