import re
with open('usa_signal_bot/portfolio/portfolio_candidates.py', 'r') as f:
    content = f.read()

# Fix how we extract fields from SelectedCandidate since it wraps a RankedSignal which wraps a StrategySignal
old_sel_extract = """
def portfolio_candidate_from_selected_candidate(candidate: SelectedCandidate, default_price: Optional[float] = None) -> PortfolioCandidate:
    from usa_signal_bot.portfolio.portfolio_models import create_portfolio_basket_id

    price = candidate.price if getattr(candidate, 'price', None) is not None else default_price

    return PortfolioCandidate(
        candidate_id=f"cand_{candidate.symbol}_{candidate.timeframe}",
        signal_id=candidate.signal_id,
        symbol=candidate.symbol,
        timeframe=candidate.timeframe,
        strategy_name=candidate.strategy_name,
        action=candidate.action,
        rank_score=candidate.rank_score,
        confidence=candidate.confidence,
        risk_score=candidate.risk_score,
        approved_quantity=0.0, # Will be set by allocation
        approved_notional=0.0, # Will be set by allocation
        price=price,
        volatility_value=getattr(candidate, 'volatility_value', None),
        atr_value=getattr(candidate, 'atr_value', None),
        risk_flags=getattr(candidate, 'risk_flags', []),
        status=PortfolioCandidateStatus.ELIGIBLE,
        metadata={}
    )
"""

new_sel_extract = """
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
        rank_score=rs.final_score,
        confidence=sig.confidence,
        risk_score=rs.risk_penalty,
        approved_quantity=0.0, # Will be set by allocation
        approved_notional=0.0, # Will be set by allocation
        price=price,
        volatility_value=getattr(sig, 'volatility_value', None),
        atr_value=getattr(sig, 'atr_value', None),
        risk_flags=getattr(sig, 'risk_flags', []),
        status=PortfolioCandidateStatus.ELIGIBLE,
        metadata={}
    )
"""

content = content.replace(old_sel_extract.strip(), new_sel_extract.strip())

# Fix RiskDecision logic, taking attributes from the decision directly since candidate_profile is not present.
old_risk_ext = """
    # Handle potentially missing attributes on CandidateRiskProfile if they exist
    candidate_profile = decision.candidate_profile

    return PortfolioCandidate(
        candidate_id=decision.decision_id,
        signal_id=candidate_profile.signal_id if candidate_profile and hasattr(candidate_profile, 'signal_id') else getattr(decision, 'signal_id', None),
        symbol=decision.symbol,
        timeframe=decision.timeframe,
        strategy_name=candidate_profile.strategy_name if candidate_profile and hasattr(candidate_profile, 'strategy_name') else getattr(decision, 'strategy_name', None),
        action=decision.action,
        rank_score=candidate_profile.rank_score if candidate_profile and hasattr(candidate_profile, 'rank_score') else getattr(decision, 'rank_score', None),
        confidence=candidate_profile.confidence if candidate_profile and hasattr(candidate_profile, 'confidence') else getattr(decision, 'confidence', None),
        risk_score=candidate_profile.risk_score if candidate_profile and hasattr(candidate_profile, 'risk_score') else getattr(decision, 'risk_score', None),
        approved_quantity=decision.approved_quantity,
        approved_notional=decision.approved_notional,
        price=candidate_profile.price if candidate_profile and hasattr(candidate_profile, 'price') else getattr(decision, 'price', None),
        volatility_value=candidate_profile.volatility_value if candidate_profile and hasattr(candidate_profile, 'volatility_value') else getattr(decision, 'volatility_value', None),
        atr_value=candidate_profile.atr_value if candidate_profile and hasattr(candidate_profile, 'atr_value') else getattr(decision, 'atr_value', None),
        risk_flags=decision.risk_flags if hasattr(decision, 'risk_flags') else getattr(candidate_profile, 'risk_flags', []),
        status=status,
        metadata={"rejection_reasons": decision.rejection_reasons} if getattr(decision, 'rejection_reasons', None) else {}
    )
"""

new_risk_ext = """
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
"""
content = content.replace(old_risk_ext.strip(), new_risk_ext.strip())

with open('usa_signal_bot/portfolio/portfolio_candidates.py', 'w') as f:
    f.write(content)
