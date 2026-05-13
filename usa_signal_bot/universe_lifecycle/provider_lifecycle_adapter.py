from typing import Any, List, Dict
from usa_signal_bot.providers.provider_models import ProviderResponse
from usa_signal_bot.providers.provider_quality import ProviderQualityScore
from usa_signal_bot.core.enums import SymbolLifecycleStatus
from usa_signal_bot.universe_lifecycle.symbol_status_resolver import SymbolStatusResolver

def attach_lifecycle_metadata_to_provider_response(response: ProviderResponse, resolver: SymbolStatusResolver) -> ProviderResponse:
    if not response.data:
        return response
    records = resolver.resolve_many(list(response.data.keys()))
    metadata = response.metadata or {}
    lifecycle_map = {r.symbol: r.status.value for r in records}
    metadata["lifecycle_status"] = lifecycle_map
    response.metadata = metadata
    return response

def lifecycle_quality_adjustment_for_response(response: ProviderResponse, resolver: SymbolStatusResolver) -> Dict[str, Any]:
    if not response.data:
        return {"adjustment_score": 0.0, "reason": "No data"}
    symbols = list(response.data.keys())
    records = resolver.resolve_many(symbols)
    delisted = sum(1 for r in records if r.status == SymbolLifecycleStatus.DELISTED)
    unknown = sum(1 for r in records if r.status in [SymbolLifecycleStatus.UNKNOWN, SymbolLifecycleStatus.REVIEW_REQUIRED])
    adj = 0.0
    reason = ""
    if delisted > 0:
        adj -= 10.0
        reason = f"Contains {delisted} delisted symbols."
    if unknown > 0:
        adj -= (unknown / len(symbols)) * 20.0
        reason += f" Contains {unknown} unknown symbols."
    return {"adjustment_score": adj, "reason": reason.strip()}

def provider_quality_with_lifecycle_adjustment(score: ProviderQualityScore, response: ProviderResponse, resolver: SymbolStatusResolver) -> ProviderQualityScore:
    adj_info = lifecycle_quality_adjustment_for_response(response, resolver)
    adj = adj_info["adjustment_score"]
    if adj < 0:
        score.score = max(0.0, score.score + adj)
        score.summary += f" [Lifecycle Adjusted: {adj_info['reason']}]"
    return score

def provider_response_symbols_requiring_review(response: ProviderResponse, resolver: SymbolStatusResolver) -> List[str]:
    if not response.data:
        return []
    records = resolver.resolve_many(list(response.data.keys()))
    return [r.symbol for r in records if r.status in [SymbolLifecycleStatus.UNKNOWN, SymbolLifecycleStatus.REVIEW_REQUIRED]]
