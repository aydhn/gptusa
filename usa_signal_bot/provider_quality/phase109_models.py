import uuid
import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from usa_signal_bot.core.enums import (
    ProviderQualityStatus,
    ProviderQualityDecision,
    DataQualityComponent,
    DataQualityGrade,
    SourceTrustLevel,
    ProviderSelectionScoreStatus,
    ProviderRankingDecision,
    ProviderQualityRiskFlag,
    ProviderQualityReportType,
)
from usa_signal_bot.core.exceptions import ProviderQualityValidationError


@dataclass
class ProviderCacheIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    provider_cache_ready: bool
    stale_fresh_policy_valid: bool
    fallback_dry_run_ready: bool
    source_comparison_ready: bool
    metadata_only: bool
    cache_only_default: bool
    network_enabled_by_default: bool
    paid_api_enabled: bool
    scraping_enabled: bool
    html_parse_enabled: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    dashboard_enabled: bool
    valid_for_phase109: bool
    risk_flags: List[ProviderQualityRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DataQualityScoreComponent:
    component_id: str
    created_at_utc: str
    provider_name: str
    symbol: Optional[str]
    component: DataQualityComponent
    raw_value: Optional[float]
    score: float
    weight: float
    weighted_score: float
    grade: DataQualityGrade
    explanation: str
    risk_flags: List[ProviderQualityRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderDataQualityScore:
    score_id: str
    created_at_utc: str
    provider_name: str
    symbol: Optional[str]
    capability: str
    components: List[DataQualityScoreComponent]
    total_score: float
    grade: DataQualityGrade
    usable_for_research: bool
    use_with_warning: bool
    blocked: bool
    explanation: str
    risk_flags: List[ProviderQualityRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SourceTrustProfile:
    profile_id: str
    created_at_utc: str
    provider_name: str
    provider_kind: str
    historical_score: Optional[float]
    schema_reliability_score: Optional[float]
    freshness_reliability_score: Optional[float]
    agreement_reliability_score: Optional[float]
    cache_reliability_score: Optional[float]
    safety_reliability_score: Optional[float]
    trust_score: float
    trust_level: SourceTrustLevel
    default_use_case: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ProviderQualityRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderSelectionScore:
    selection_score_id: str
    created_at_utc: str
    provider_name: str
    symbol: Optional[str]
    capability: str
    data_quality_score_id: Optional[str]
    trust_profile_id: Optional[str]
    quality_score: float
    trust_score: float
    freshness_score: float
    safety_score: float
    availability_score: float
    final_selection_score: float
    status: ProviderSelectionScoreStatus
    decision: ProviderRankingDecision
    rank: Optional[int]
    selectable_for_research: bool
    use_as_fallback: bool
    blocked: bool
    explanation: str
    risk_flags: List[ProviderQualityRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderRanking:
    ranking_id: str
    created_at_utc: str
    symbol: Optional[str]
    capability: str
    scores: List[ProviderSelectionScore]
    ranked_provider_names: List[str]
    preferred_provider: Optional[str]
    fallback_providers: List[str]
    blocked_providers: List[str]
    ranking_valid: bool
    ranking_is_research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    risk_flags: List[ProviderQualityRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderQualityContext:
    context_id: str
    created_at_utc: str
    status: ProviderQualityStatus
    decision: ProviderQualityDecision
    source_provider_cache_review_id: Optional[str]
    ingestion: ProviderCacheIngestionResult
    data_quality_scores: List[ProviderDataQualityScore]
    trust_profiles: List[SourceTrustProfile]
    selection_scores: List[ProviderSelectionScore]
    rankings: List[ProviderRanking]
    provider_quality_ready: bool
    source_trust_ready: bool
    provider_selection_scoring_ready: bool
    metadata_only: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    risk_flags: List[ProviderQualityRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderQualityFullReview:
    review_id: str
    created_at_utc: str
    report_type: ProviderQualityReportType
    ingestion: ProviderCacheIngestionResult
    context: ProviderQualityContext
    data_quality_scores: List[ProviderDataQualityScore]
    trust_profiles: List[SourceTrustProfile]
    selection_scores: List[ProviderSelectionScore]
    rankings: List[ProviderRanking]
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def create_provider_cache_ingestion_id() -> str:
    return f"cache_ingest_{uuid.uuid4().hex[:8]}"


def create_data_quality_component_id() -> str:
    return f"dq_comp_{uuid.uuid4().hex[:8]}"


def create_provider_data_quality_score_id() -> str:
    return f"pdqs_{uuid.uuid4().hex[:8]}"


def create_source_trust_profile_id() -> str:
    return f"trust_prof_{uuid.uuid4().hex[:8]}"


def create_provider_selection_score_id() -> str:
    return f"psel_score_{uuid.uuid4().hex[:8]}"


def create_provider_ranking_id() -> str:
    return f"prank_{uuid.uuid4().hex[:8]}"


def create_provider_quality_context_id() -> str:
    return f"pq_ctx_{uuid.uuid4().hex[:8]}"


def create_provider_quality_full_review_id() -> str:
    return f"pq_review_{uuid.uuid4().hex[:8]}"


def provider_cache_ingestion_result_to_dict(item: ProviderCacheIngestionResult) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def data_quality_score_component_to_dict(item: DataQualityScoreComponent) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def provider_data_quality_score_to_dict(item: ProviderDataQualityScore) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def source_trust_profile_to_dict(item: SourceTrustProfile) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def provider_selection_score_to_dict(item: ProviderSelectionScore) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def provider_ranking_to_dict(item: ProviderRanking) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def provider_quality_context_to_dict(item: ProviderQualityContext) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def provider_quality_full_review_to_dict(item: ProviderQualityFullReview) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def validate_provider_cache_ingestion_result(
    item: ProviderCacheIngestionResult,
) -> None:
    required_true = [
        "provider_cache_ready",
        "stale_fresh_policy_valid",
        "fallback_dry_run_ready",
        "metadata_only",
    ]
    for attr in required_true:
        if not getattr(item, attr):
            raise ProviderQualityValidationError(f"{attr} must be True")

    if not item.source_comparison_ready:
        item.warnings.append("source_comparison_ready is false")

    required_false = [
        "network_enabled_by_default",
        "paid_api_enabled",
        "scraping_enabled",
        "html_parse_enabled",
        "broker_execution_enabled",
        "order_creation_enabled",
        "paper_state_mutation_enabled",
        "telegram_real_send_enabled",
        "dashboard_enabled",
    ]
    for attr in required_false:
        if getattr(item, attr):
            raise ProviderQualityValidationError(f"{attr} must be False")


def validate_data_quality_score_component(item: DataQualityScoreComponent) -> None:
    if not (0 <= item.score <= 100):
        raise ProviderQualityValidationError("Score must be between 0 and 100")
    if not (0 <= item.weight <= 1.0):
        raise ProviderQualityValidationError("Weight must be between 0 and 1.0")


def validate_provider_data_quality_score(item: ProviderDataQualityScore) -> None:
    if not (0 <= item.total_score <= 100):
        raise ProviderQualityValidationError("total_score must be between 0 and 100")
    if item.blocked and item.usable_for_research:
        raise ProviderQualityValidationError(
            "blocked provider cannot be usable for research"
        )


def validate_source_trust_profile(item: SourceTrustProfile) -> None:
    if not (0 <= item.trust_score <= 100):
        raise ProviderQualityValidationError("trust_score must be between 0 and 100")


def validate_provider_selection_score(item: ProviderSelectionScore) -> None:
    if not (0 <= item.final_selection_score <= 100):
        raise ProviderQualityValidationError(
            "final_selection_score must be between 0 and 100"
        )


def validate_provider_ranking(item: ProviderRanking) -> None:
    if not item.ranking_is_research_data_only:
        raise ProviderQualityValidationError(
            "ranking_is_research_data_only must be True"
        )
    if item.produces_trade_signal:
        raise ProviderQualityValidationError("produces_trade_signal must be False")
    if item.produces_order_decision:
        raise ProviderQualityValidationError("produces_order_decision must be False")


def validate_provider_quality_context(item: ProviderQualityContext) -> None:
    if not item.research_data_only:
        raise ProviderQualityValidationError("research_data_only must be True")
    if item.produces_trade_signal:
        raise ProviderQualityValidationError("produces_trade_signal must be False")
    if item.produces_order_decision:
        raise ProviderQualityValidationError("produces_order_decision must be False")
    if item.network_used:
        raise ProviderQualityValidationError("network_used must be False")
    if item.paid_api_used:
        raise ProviderQualityValidationError("paid_api_used must be False")
    if item.scraping_used:
        raise ProviderQualityValidationError("scraping_used must be False")
    if item.html_parsing_used:
        raise ProviderQualityValidationError("html_parsing_used must be False")
    if item.broker_used:
        raise ProviderQualityValidationError("broker_used must be False")
    if item.order_created:
        raise ProviderQualityValidationError("order_created must be False")
    if item.paper_state_mutated:
        raise ProviderQualityValidationError("paper_state_mutated must be False")
    if item.telegram_real_sent:
        raise ProviderQualityValidationError("telegram_real_sent must be False")
    if item.dashboard_started:
        raise ProviderQualityValidationError("dashboard_started must be False")


def validate_provider_quality_full_review(item: ProviderQualityFullReview) -> None:
    validate_provider_cache_ingestion_result(item.ingestion)
    validate_provider_quality_context(item.context)
