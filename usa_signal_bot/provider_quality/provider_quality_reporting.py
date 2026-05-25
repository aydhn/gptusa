from typing import Dict, Any
from usa_signal_bot.provider_quality.phase109_models import (
    ProviderQualityContext,
    ProviderQualityFullReview,
    ProviderCacheIngestionResult,
    ProviderDataQualityScore,
    DataQualityScoreComponent,
    SourceTrustProfile,
    ProviderSelectionScore,
    ProviderRanking
)
from usa_signal_bot.provider_quality.provider_cache_ingestion import provider_cache_ingestion_to_text
from usa_signal_bot.provider_quality.data_quality_scorer import provider_data_quality_score_to_text
from usa_signal_bot.provider_quality.source_trust_model import source_trust_profile_to_text
from usa_signal_bot.provider_quality.provider_selection_scorer import provider_selection_score_to_text
from usa_signal_bot.provider_quality.provider_ranking_engine import provider_ranking_to_text

def data_quality_score_component_to_text(item: DataQualityScoreComponent) -> str:
    return f"{item.component.value}: {item.score:.1f} ({item.grade.value}) - {item.explanation}"

def provider_quality_context_to_text(item: ProviderQualityContext, limit: int = 300) -> str:
    lines = [
        f"Provider Quality Context: {item.context_id} | Status: {item.status.value}",
        f"Ingestion: {item.ingestion.ingestion_id}",
        f"Quality Scores: {len(item.data_quality_scores)}",
        f"Trust Profiles: {len(item.trust_profiles)}",
        f"Selection Scores: {len(item.selection_scores)}",
        f"Rankings: {len(item.rankings)}"
    ]
    if item.errors:
        lines.append(f"Errors: {item.errors}")
    if item.warnings:
        lines.append(f"Warnings: {item.warnings}")
    return "\n".join(lines)[:limit]

def provider_quality_full_review_to_text(item: ProviderQualityFullReview, limit: int = 300) -> str:
    lines = [
        f"Provider Quality Full Review: {item.review_id}",
        f"Context ID: {item.context.context_id}",
        f"Report Type: {item.report_type.value}",
        f"Warnings: {len(item.warnings)}",
        f"Errors: {len(item.errors)}"
    ]
    return "\n".join(lines)[:limit]

def provider_quality_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return (
        f"Provider Quality Store:\n"
        f"  Contexts: {summary.get('contexts_count', 0)}\n"
        f"  Reviews: {summary.get('reviews_count', 0)}\n"
        f"  Data Quality Scores: {summary.get('data_quality_scores_count', 0)}\n"
        f"  Source Trust Profiles: {summary.get('source_trust_profiles_count', 0)}\n"
        f"  Selection Scores: {summary.get('provider_selection_scores_count', 0)}\n"
        f"  Rankings: {summary.get('provider_rankings_count', 0)}"
    )

def provider_quality_limitations_text() -> str:
    from usa_signal_bot.provider_quality.provider_quality_report import provider_quality_limitations_text as inner
    return inner()
