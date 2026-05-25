from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.provider_cache.phase108_models import (
    DataConfidenceHint,
    SourceComparisonResult,
    SourceConfidenceLevel,
    create_data_confidence_hint_id,
    ProviderCacheRiskFlag,
    SourceComparisonStatus
)

def build_data_confidence_hint(symbol: str, provider_name: str | None, comparison_result: SourceComparisonResult | None = None, reason: str | None = None) -> DataConfidenceHint:
    conf = SourceConfidenceLevel.UNKNOWN
    score = None
    rec_action = "review_data_source"

    if comparison_result:
        conf = comparison_result.confidence
        score = comparison_result.confidence_score
        if comparison_result.status == SourceComparisonStatus.MATCH:
            rec_action = "proceed_with_research"
        else:
            rec_action = "use_with_warning"

    if not reason:
        reason = "Automated comparison check"

    return DataConfidenceHint(
        hint_id=create_data_confidence_hint_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        symbol=symbol,
        provider_name=provider_name,
        confidence=conf,
        confidence_score=score,
        reason=reason,
        recommended_action=rec_action,
        risk_flags=[],
        warnings=[],
        metadata={}
    )

def build_confidence_hints_from_comparison(result: SourceComparisonResult) -> list[DataConfidenceHint]:
    return [build_data_confidence_hint(result.symbol, None, result)]

def confidence_level_from_score(score: float | None) -> SourceConfidenceLevel:
    if score is None: return SourceConfidenceLevel.UNKNOWN
    if score >= 90: return SourceConfidenceLevel.HIGH
    if score >= 70: return SourceConfidenceLevel.MEDIUM
    if score >= 40: return SourceConfidenceLevel.LOW
    return SourceConfidenceLevel.VERY_LOW

def data_confidence_hints_summary(items: list[DataConfidenceHint]) -> dict[str, Any]:
    return {"total": len(items)}

def data_confidence_hints_to_text(items: list[DataConfidenceHint], limit: int = 200) -> str:
    return f"Hints count: {len(items)}"
