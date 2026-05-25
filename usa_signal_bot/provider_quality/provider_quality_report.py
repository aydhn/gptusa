import datetime
from typing import List, Optional

from usa_signal_bot.core.enums import ProviderQualityStatus, ProviderQualityDecision, ProviderQualityReportType
from usa_signal_bot.provider_quality.phase109_models import (
    ProviderQualityContext,
    ProviderQualityFullReview,
    create_provider_quality_context_id,
    create_provider_quality_full_review_id,
    ProviderCacheIngestionResult,
    ProviderDataQualityScore,
    SourceTrustProfile,
    ProviderSelectionScore,
    ProviderRanking
)

def build_provider_quality_context(
    ingestion: ProviderCacheIngestionResult,
    data_quality_scores: Optional[List[ProviderDataQualityScore]] = None,
    trust_profiles: Optional[List[SourceTrustProfile]] = None,
    selection_scores: Optional[List[ProviderSelectionScore]] = None,
    rankings: Optional[List[ProviderRanking]] = None
) -> ProviderQualityContext:

    data_quality_scores = data_quality_scores or []
    trust_profiles = trust_profiles or []
    selection_scores = selection_scores or []
    rankings = rankings or []

    context_id = create_provider_quality_context_id()
    created_at_utc = datetime.datetime.utcnow().isoformat() + "Z"

    # Collect errors to determine status
    all_errors = []
    all_errors.extend(ingestion.errors)
    for q in data_quality_scores: all_errors.extend(q.errors)
    for t in trust_profiles: all_errors.extend(t.errors)
    for s in selection_scores: all_errors.extend(s.errors)
    for r in rankings: all_errors.extend(r.errors)

    # Collect warnings
    all_warnings = []
    all_warnings.extend(ingestion.warnings)
    for q in data_quality_scores: all_warnings.extend(q.warnings)
    for t in trust_profiles: all_warnings.extend(t.warnings)
    for s in selection_scores: all_warnings.extend(s.warnings)
    for r in rankings: all_warnings.extend(r.warnings)

    status = ProviderQualityStatus.VALIDATED if not all_errors else ProviderQualityStatus.FAILED
    decision = ProviderQualityDecision.RANK_PROVIDERS if not all_errors else ProviderQualityDecision.BLOCK

    return ProviderQualityContext(
        context_id=context_id,
        created_at_utc=created_at_utc,
        status=status,
        decision=decision,
        source_provider_cache_review_id=ingestion.source_review_id,
        ingestion=ingestion,
        data_quality_scores=data_quality_scores,
        trust_profiles=trust_profiles,
        selection_scores=selection_scores,
        rankings=rankings,
        provider_quality_ready=True,
        source_trust_ready=True,
        provider_selection_scoring_ready=True,
        metadata_only=True,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        risk_flags=ingestion.risk_flags, # Risk flags will be aggregated fully by the safety validator
        warnings=list(set(all_warnings)),
        errors=list(set(all_errors))
    )

def build_provider_quality_full_review(
    ingestion: ProviderCacheIngestionResult,
    data_quality_scores: Optional[List[ProviderDataQualityScore]] = None,
    trust_profiles: Optional[List[SourceTrustProfile]] = None,
    selection_scores: Optional[List[ProviderSelectionScore]] = None,
    rankings: Optional[List[ProviderRanking]] = None
) -> ProviderQualityFullReview:

    context = build_provider_quality_context(ingestion, data_quality_scores, trust_profiles, selection_scores, rankings)

    return ProviderQualityFullReview(
        review_id=create_provider_quality_full_review_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        report_type=ProviderQualityReportType.FULL_PHASE109_REVIEW,
        ingestion=ingestion,
        context=context,
        data_quality_scores=context.data_quality_scores,
        trust_profiles=context.trust_profiles,
        selection_scores=context.selection_scores,
        rankings=context.rankings,
        output_paths={},
        warnings=context.warnings,
        errors=context.errors
    )

def provider_quality_limitations_text() -> str:
    return (
        "Phase 109 Limitations:\n"
        "- This phase strictly handles Provider Data Quality Scoring and Ranking.\n"
        "- It DOES NOT perform Active Paper Trading, Broker Order Creation, or Paper State Mutations.\n"
        "- The scores are strictly for Research Data Selection and MUST NOT be interpreted as Trade Signals.\n"
        "- Execution terminology ('buy', 'sell', 'guaranteed') is actively blocked.\n"
    )
