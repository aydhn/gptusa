import datetime
from typing import List, Dict, Any, Optional

from usa_signal_bot.provider_quality.phase109_models import ProviderSelectionScore, ProviderRanking, create_provider_ranking_id

def assign_provider_ranks(selection_scores: List[ProviderSelectionScore]) -> List[ProviderSelectionScore]:
    # Filter out blocked providers for ranking
    valid_scores = [s for s in selection_scores if not s.blocked]
    # Sort by final score descending
    valid_scores.sort(key=lambda x: x.final_selection_score, reverse=True)

    for i, score in enumerate(valid_scores):
        score.rank = i + 1

    return selection_scores

def rank_providers_for_symbol(symbol: Optional[str], capability: str, selection_scores: List[ProviderSelectionScore]) -> ProviderRanking:
    selection_scores = assign_provider_ranks(selection_scores)

    ranked_names = []
    blocked_names = []

    # Re-sort full list: unblocked by rank first, then blocked
    sorted_scores = sorted(selection_scores, key=lambda x: (x.blocked, x.rank if x.rank is not None else 9999))

    for s in sorted_scores:
        if s.blocked:
            blocked_names.append(s.provider_name)
        else:
            ranked_names.append(s.provider_name)

    preferred = ranked_names[0] if ranked_names else None
    fallbacks = ranked_names[1:] if len(ranked_names) > 1 else []

    risk_flags = []
    warnings = []

    if not preferred:
        warnings.append("No selectable providers available.")

    for s in selection_scores:
        risk_flags.extend(s.risk_flags)

    risk_flags = list(set(risk_flags))

    return ProviderRanking(
        ranking_id=create_provider_ranking_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        symbol=symbol,
        capability=capability,
        scores=sorted_scores,
        ranked_provider_names=ranked_names,
        preferred_provider=preferred,
        fallback_providers=fallbacks,
        blocked_providers=blocked_names,
        ranking_valid=True,
        ranking_is_research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        risk_flags=risk_flags,
        warnings=warnings
    )

def provider_ranking_summary(ranking: ProviderRanking) -> Dict[str, Any]:
    return {
        "ranking_id": ranking.ranking_id,
        "symbol": ranking.symbol,
        "preferred": ranking.preferred_provider,
        "fallbacks": ranking.fallback_providers,
        "blocked": ranking.blocked_providers
    }

def provider_ranking_to_text(ranking: ProviderRanking, limit: int = 100) -> str:
    lines = [
        f"Provider Ranking | Symbol: {ranking.symbol}",
        f"Preferred: {ranking.preferred_provider}",
        f"Fallbacks: {', '.join(ranking.fallback_providers)}",
        f"Blocked: {', '.join(ranking.blocked_providers)}"
    ]
    return "\n".join(lines)
