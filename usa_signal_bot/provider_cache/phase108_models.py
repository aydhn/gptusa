from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
from usa_signal_bot.core.enums import (
    ProviderCacheStatus,
    ProviderCacheDecision,
    ProviderCacheRecordStatus,
    StaleFreshStatus,
    FallbackDryRunStatus,
    FallbackDryRunDecision,
    SourceComparisonStatus,
    SourceConfidenceLevel,
    SourceComparisonMetric,
    ProviderCacheRiskFlag,
    ProviderCacheReportType,
)
import uuid
from datetime import datetime, timezone

@dataclass
class ProviderRuntimeIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    provider_runtime_ready: bool
    adapter_contracts_valid: bool
    cache_aware_dry_run_ready: bool
    metadata_only: bool
    network_enabled_by_default: bool
    paid_api_enabled: bool
    scraping_enabled: bool
    html_parse_enabled: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    dashboard_enabled: bool
    valid_for_phase108: bool
    risk_flags: List[ProviderCacheRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class ProviderCacheRecord:
    record_id: str
    created_at_utc: str
    provider_name: str
    symbol: str
    capability: str
    interval: Optional[str]
    cache_key: str
    cache_path: str
    status: ProviderCacheRecordStatus
    rows: int
    first_timestamp: Optional[str]
    last_timestamp: Optional[str]
    fetched_at_utc: Optional[str]
    as_of_utc: Optional[str]
    stale_after_seconds: Optional[int]
    file_size_bytes: Optional[int]
    schema_valid: bool
    checksum: Optional[str]
    quality_flags: List[str]
    risk_flags: List[ProviderCacheRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class ProviderCacheIndex:
    index_id: str
    created_at_utc: str
    cache_root: str
    records: List[ProviderCacheRecord]
    total_records: int
    fresh_records: int
    stale_records: int
    missing_records: int
    corrupt_records: int
    index_valid: bool
    risk_flags: List[ProviderCacheRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class StaleFreshPolicy:
    policy_id: str
    created_at_utc: str
    default_ttl_seconds: int
    intraday_ttl_seconds: int
    daily_ttl_seconds: int
    fundamentals_ttl_seconds: int
    macro_ttl_seconds: int
    allow_stale_read: bool
    stale_read_requires_warning: bool
    block_expired: bool
    timezone: str
    policy_valid: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class StaleFreshEvaluation:
    evaluation_id: str
    created_at_utc: str
    cache_record_id: Optional[str]
    provider_name: str
    symbol: str
    status: StaleFreshStatus
    age_seconds: Optional[int]
    ttl_seconds: Optional[int]
    fresh: bool
    stale: bool
    expired: bool
    readable: bool
    refresh_required_future: bool
    risk_flags: List[ProviderCacheRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class FallbackDryRunPlan:
    plan_id: str
    created_at_utc: str
    provider_kind: str
    capability: str
    symbol: str
    interval: Optional[str]
    primary_provider: Optional[str]
    fallback_chain: List[str]
    cache_only: bool
    dry_run_only: bool
    allow_network: bool
    allow_paid_api: bool
    allow_scraping: bool
    allow_html_parsing: bool
    allow_broker: bool
    allow_order: bool
    allow_paper_mutation: bool
    expected_schema: List[str]
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderCacheRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class FallbackDryRunResult:
    result_id: str
    created_at_utc: str
    plan_id: Optional[str]
    status: FallbackDryRunStatus
    decision: FallbackDryRunDecision
    selected_provider: Optional[str]
    selected_cache_record_id: Optional[str]
    attempted_providers: List[str]
    skipped_providers: List[str]
    fallback_exhausted: bool
    cache_hit: bool
    cache_miss: bool
    stale_used: bool
    source_comparison_required: bool
    dry_run_only: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    passed: bool
    risk_flags: List[ProviderCacheRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class SourceComparisonInput:
    comparison_id: str
    created_at_utc: str
    symbol: str
    capability: str
    interval: Optional[str]
    source_records: List[ProviderCacheRecord]
    compare_columns: List[str]
    tolerance_pct: float
    min_rows_required: int
    dry_run_only: bool
    metadata: Dict[str, Any]

@dataclass
class SourceComparisonResult:
    result_id: str
    created_at_utc: str
    comparison_id: Optional[str]
    symbol: str
    status: SourceComparisonStatus
    confidence: SourceConfidenceLevel
    compared_source_count: int
    matched_source_count: int
    missing_source_count: int
    material_difference_count: int
    metrics: Dict[str, Any]
    disagreement_score: Optional[float]
    confidence_score: Optional[float]
    source_rank_hints: List[Dict[str, Any]]
    outlier_sources: List[str]
    drift_warnings: List[str]
    schema_valid: bool
    dry_run_only: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    risk_flags: List[ProviderCacheRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class DataConfidenceHint:
    hint_id: str
    created_at_utc: str
    symbol: str
    provider_name: Optional[str]
    confidence: SourceConfidenceLevel
    confidence_score: Optional[float]
    reason: str
    recommended_action: str
    risk_flags: List[ProviderCacheRiskFlag]
    warnings: List[str]
    metadata: Dict[str, Any]

@dataclass
class ProviderCacheContext:
    context_id: str
    created_at_utc: str
    status: ProviderCacheStatus
    decision: ProviderCacheDecision
    source_provider_runtime_review_id: Optional[str]
    ingestion: ProviderRuntimeIngestionResult
    cache_index: ProviderCacheIndex
    stale_fresh_policy: StaleFreshPolicy
    stale_fresh_evaluations: List[StaleFreshEvaluation]
    fallback_plans: List[FallbackDryRunPlan]
    fallback_results: List[FallbackDryRunResult]
    source_comparisons: List[SourceComparisonResult]
    confidence_hints: List[DataConfidenceHint]
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
    risk_flags: List[ProviderCacheRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class ProviderCacheFullReview:
    review_id: str
    created_at_utc: str
    report_type: ProviderCacheReportType
    ingestion: ProviderRuntimeIngestionResult
    context: ProviderCacheContext
    cache_index: ProviderCacheIndex
    stale_fresh_policy: StaleFreshPolicy
    fallback_results: List[FallbackDryRunResult]
    source_comparisons: List[SourceComparisonResult]
    confidence_hints: List[DataConfidenceHint]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

def create_provider_runtime_ingestion_id() -> str:
    return f"PRI-{uuid.uuid4().hex[:8].upper()}"

def create_provider_cache_record_id() -> str:
    return f"PCR-{uuid.uuid4().hex[:8].upper()}"

def create_provider_cache_index_id() -> str:
    return f"PCI-{uuid.uuid4().hex[:8].upper()}"

def create_stale_fresh_policy_id() -> str:
    return f"SFP-{uuid.uuid4().hex[:8].upper()}"

def create_stale_fresh_evaluation_id() -> str:
    return f"SFE-{uuid.uuid4().hex[:8].upper()}"

def create_fallback_dry_run_plan_id() -> str:
    return f"FDP-{uuid.uuid4().hex[:8].upper()}"

def create_fallback_dry_run_result_id() -> str:
    return f"FDR-{uuid.uuid4().hex[:8].upper()}"

def create_source_comparison_id() -> str:
    return f"SCI-{uuid.uuid4().hex[:8].upper()}"

def create_source_comparison_result_id() -> str:
    return f"SCR-{uuid.uuid4().hex[:8].upper()}"

def create_data_confidence_hint_id() -> str:
    return f"DCH-{uuid.uuid4().hex[:8].upper()}"

def create_provider_cache_context_id() -> str:
    return f"PCC-{uuid.uuid4().hex[:8].upper()}"

def create_provider_cache_full_review_id() -> str:
    return f"PFR-{uuid.uuid4().hex[:8].upper()}"

def provider_runtime_ingestion_result_to_dict(item: ProviderRuntimeIngestionResult) -> dict:
    return {
        "ingestion_id": item.ingestion_id,
        "created_at_utc": item.created_at_utc,
        "source_path": item.source_path,
        "source_review_id": item.source_review_id,
        "source_context_id": item.source_context_id,
        "available": item.available,
        "provider_runtime_ready": item.provider_runtime_ready,
        "adapter_contracts_valid": item.adapter_contracts_valid,
        "cache_aware_dry_run_ready": item.cache_aware_dry_run_ready,
        "metadata_only": item.metadata_only,
        "network_enabled_by_default": item.network_enabled_by_default,
        "paid_api_enabled": item.paid_api_enabled,
        "scraping_enabled": item.scraping_enabled,
        "html_parse_enabled": item.html_parse_enabled,
        "broker_execution_enabled": item.broker_execution_enabled,
        "order_creation_enabled": item.order_creation_enabled,
        "paper_state_mutation_enabled": item.paper_state_mutation_enabled,
        "telegram_real_send_enabled": item.telegram_real_send_enabled,
        "dashboard_enabled": item.dashboard_enabled,
        "valid_for_phase108": item.valid_for_phase108,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def provider_cache_record_to_dict(item: ProviderCacheRecord) -> dict:
    return {
        "record_id": item.record_id,
        "created_at_utc": item.created_at_utc,
        "provider_name": item.provider_name,
        "symbol": item.symbol,
        "capability": item.capability,
        "interval": item.interval,
        "cache_key": item.cache_key,
        "cache_path": item.cache_path,
        "status": item.status.value,
        "rows": item.rows,
        "first_timestamp": item.first_timestamp,
        "last_timestamp": item.last_timestamp,
        "fetched_at_utc": item.fetched_at_utc,
        "as_of_utc": item.as_of_utc,
        "stale_after_seconds": item.stale_after_seconds,
        "file_size_bytes": item.file_size_bytes,
        "schema_valid": item.schema_valid,
        "checksum": item.checksum,
        "quality_flags": item.quality_flags,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def provider_cache_index_to_dict(item: ProviderCacheIndex) -> dict:
    return {
        "index_id": item.index_id,
        "created_at_utc": item.created_at_utc,
        "cache_root": item.cache_root,
        "records": [provider_cache_record_to_dict(r) for r in item.records],
        "total_records": item.total_records,
        "fresh_records": item.fresh_records,
        "stale_records": item.stale_records,
        "missing_records": item.missing_records,
        "corrupt_records": item.corrupt_records,
        "index_valid": item.index_valid,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def stale_fresh_policy_to_dict(item: StaleFreshPolicy) -> dict:
    return {
        "policy_id": item.policy_id,
        "created_at_utc": item.created_at_utc,
        "default_ttl_seconds": item.default_ttl_seconds,
        "intraday_ttl_seconds": item.intraday_ttl_seconds,
        "daily_ttl_seconds": item.daily_ttl_seconds,
        "fundamentals_ttl_seconds": item.fundamentals_ttl_seconds,
        "macro_ttl_seconds": item.macro_ttl_seconds,
        "allow_stale_read": item.allow_stale_read,
        "stale_read_requires_warning": item.stale_read_requires_warning,
        "block_expired": item.block_expired,
        "timezone": item.timezone,
        "policy_valid": item.policy_valid,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def stale_fresh_evaluation_to_dict(item: StaleFreshEvaluation) -> dict:
    return {
        "evaluation_id": item.evaluation_id,
        "created_at_utc": item.created_at_utc,
        "cache_record_id": item.cache_record_id,
        "provider_name": item.provider_name,
        "symbol": item.symbol,
        "status": item.status.value,
        "age_seconds": item.age_seconds,
        "ttl_seconds": item.ttl_seconds,
        "fresh": item.fresh,
        "stale": item.stale,
        "expired": item.expired,
        "readable": item.readable,
        "refresh_required_future": item.refresh_required_future,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def fallback_dry_run_plan_to_dict(item: FallbackDryRunPlan) -> dict:
    return {
        "plan_id": item.plan_id,
        "created_at_utc": item.created_at_utc,
        "provider_kind": item.provider_kind,
        "capability": item.capability,
        "symbol": item.symbol,
        "interval": item.interval,
        "primary_provider": item.primary_provider,
        "fallback_chain": item.fallback_chain,
        "cache_only": item.cache_only,
        "dry_run_only": item.dry_run_only,
        "allow_network": item.allow_network,
        "allow_paid_api": item.allow_paid_api,
        "allow_scraping": item.allow_scraping,
        "allow_html_parsing": item.allow_html_parsing,
        "allow_broker": item.allow_broker,
        "allow_order": item.allow_order,
        "allow_paper_mutation": item.allow_paper_mutation,
        "expected_schema": item.expected_schema,
        "warnings": item.warnings,
        "errors": item.errors,
        "risk_flags": [f.value for f in item.risk_flags],
        "metadata": item.metadata,
    }

def fallback_dry_run_result_to_dict(item: FallbackDryRunResult) -> dict:
    return {
        "result_id": item.result_id,
        "created_at_utc": item.created_at_utc,
        "plan_id": item.plan_id,
        "status": item.status.value,
        "decision": item.decision.value,
        "selected_provider": item.selected_provider,
        "selected_cache_record_id": item.selected_cache_record_id,
        "attempted_providers": item.attempted_providers,
        "skipped_providers": item.skipped_providers,
        "fallback_exhausted": item.fallback_exhausted,
        "cache_hit": item.cache_hit,
        "cache_miss": item.cache_miss,
        "stale_used": item.stale_used,
        "source_comparison_required": item.source_comparison_required,
        "dry_run_only": item.dry_run_only,
        "network_used": item.network_used,
        "paid_api_used": item.paid_api_used,
        "scraping_used": item.scraping_used,
        "html_parsing_used": item.html_parsing_used,
        "broker_used": item.broker_used,
        "order_created": item.order_created,
        "paper_state_mutated": item.paper_state_mutated,
        "telegram_real_sent": item.telegram_real_sent,
        "dashboard_started": item.dashboard_started,
        "passed": item.passed,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def source_comparison_input_to_dict(item: SourceComparisonInput) -> dict:
    return {
        "comparison_id": item.comparison_id,
        "created_at_utc": item.created_at_utc,
        "symbol": item.symbol,
        "capability": item.capability,
        "interval": item.interval,
        "source_records": [provider_cache_record_to_dict(r) for r in item.source_records],
        "compare_columns": item.compare_columns,
        "tolerance_pct": item.tolerance_pct,
        "min_rows_required": item.min_rows_required,
        "dry_run_only": item.dry_run_only,
        "metadata": item.metadata,
    }

def source_comparison_result_to_dict(item: SourceComparisonResult) -> dict:
    return {
        "result_id": item.result_id,
        "created_at_utc": item.created_at_utc,
        "comparison_id": item.comparison_id,
        "symbol": item.symbol,
        "status": item.status.value,
        "confidence": item.confidence.value,
        "compared_source_count": item.compared_source_count,
        "matched_source_count": item.matched_source_count,
        "missing_source_count": item.missing_source_count,
        "material_difference_count": item.material_difference_count,
        "metrics": item.metrics,
        "disagreement_score": item.disagreement_score,
        "confidence_score": item.confidence_score,
        "source_rank_hints": item.source_rank_hints,
        "outlier_sources": item.outlier_sources,
        "drift_warnings": item.drift_warnings,
        "schema_valid": item.schema_valid,
        "dry_run_only": item.dry_run_only,
        "network_used": item.network_used,
        "paid_api_used": item.paid_api_used,
        "scraping_used": item.scraping_used,
        "html_parsing_used": item.html_parsing_used,
        "broker_used": item.broker_used,
        "order_created": item.order_created,
        "paper_state_mutated": item.paper_state_mutated,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def data_confidence_hint_to_dict(item: DataConfidenceHint) -> dict:
    return {
        "hint_id": item.hint_id,
        "created_at_utc": item.created_at_utc,
        "symbol": item.symbol,
        "provider_name": item.provider_name,
        "confidence": item.confidence.value,
        "confidence_score": item.confidence_score,
        "reason": item.reason,
        "recommended_action": item.recommended_action,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "metadata": item.metadata,
    }

def provider_cache_context_to_dict(item: ProviderCacheContext) -> dict:
    return {
        "context_id": item.context_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "decision": item.decision.value,
        "source_provider_runtime_review_id": item.source_provider_runtime_review_id,
        "ingestion": provider_runtime_ingestion_result_to_dict(item.ingestion),
        "cache_index": provider_cache_index_to_dict(item.cache_index),
        "stale_fresh_policy": stale_fresh_policy_to_dict(item.stale_fresh_policy),
        "stale_fresh_evaluations": [stale_fresh_evaluation_to_dict(e) for e in item.stale_fresh_evaluations],
        "fallback_plans": [fallback_dry_run_plan_to_dict(p) for p in item.fallback_plans],
        "fallback_results": [fallback_dry_run_result_to_dict(r) for r in item.fallback_results],
        "source_comparisons": [source_comparison_result_to_dict(c) for c in item.source_comparisons],
        "confidence_hints": [data_confidence_hint_to_dict(h) for h in item.confidence_hints],
        "provider_cache_ready": item.provider_cache_ready,
        "stale_fresh_policy_valid": item.stale_fresh_policy_valid,
        "fallback_dry_run_ready": item.fallback_dry_run_ready,
        "source_comparison_ready": item.source_comparison_ready,
        "metadata_only": item.metadata_only,
        "cache_only_default": item.cache_only_default,
        "network_enabled_by_default": item.network_enabled_by_default,
        "paid_api_enabled": item.paid_api_enabled,
        "scraping_enabled": item.scraping_enabled,
        "html_parse_enabled": item.html_parse_enabled,
        "broker_execution_enabled": item.broker_execution_enabled,
        "order_creation_enabled": item.order_creation_enabled,
        "paper_state_mutation_enabled": item.paper_state_mutation_enabled,
        "telegram_real_send_enabled": item.telegram_real_send_enabled,
        "dashboard_enabled": item.dashboard_enabled,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def provider_cache_full_review_to_dict(item: ProviderCacheFullReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value,
        "ingestion": provider_runtime_ingestion_result_to_dict(item.ingestion),
        "context": provider_cache_context_to_dict(item.context),
        "cache_index": provider_cache_index_to_dict(item.cache_index),
        "stale_fresh_policy": stale_fresh_policy_to_dict(item.stale_fresh_policy),
        "fallback_results": [fallback_dry_run_result_to_dict(r) for r in item.fallback_results],
        "source_comparisons": [source_comparison_result_to_dict(c) for c in item.source_comparisons],
        "confidence_hints": [data_confidence_hint_to_dict(h) for h in item.confidence_hints],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }

# Validations
from usa_signal_bot.core.exceptions import ProviderCacheSafetyValidationError

def validate_provider_runtime_ingestion_result(item: ProviderRuntimeIngestionResult) -> None:
    if not item.provider_runtime_ready:
        raise ProviderCacheSafetyValidationError("provider_runtime_ready must be true")
    if not item.adapter_contracts_valid:
        raise ProviderCacheSafetyValidationError("adapter_contracts_valid must be true")
    if not item.cache_aware_dry_run_ready:
        raise ProviderCacheSafetyValidationError("cache_aware_dry_run_ready must be true")
    if not item.metadata_only:
        raise ProviderCacheSafetyValidationError("metadata_only must be true")
    if item.network_enabled_by_default:
        raise ProviderCacheSafetyValidationError("network_enabled_by_default must be false")
    if item.paid_api_enabled:
        raise ProviderCacheSafetyValidationError("paid_api_enabled must be false")
    if item.scraping_enabled:
        raise ProviderCacheSafetyValidationError("scraping_enabled must be false")
    if item.html_parse_enabled:
        raise ProviderCacheSafetyValidationError("html_parse_enabled must be false")
    if item.broker_execution_enabled:
        raise ProviderCacheSafetyValidationError("broker_execution_enabled must be false")
    if item.order_creation_enabled:
        raise ProviderCacheSafetyValidationError("order_creation_enabled must be false")
    if item.paper_state_mutation_enabled:
        raise ProviderCacheSafetyValidationError("paper_state_mutation_enabled must be false")
    if item.telegram_real_send_enabled:
        raise ProviderCacheSafetyValidationError("telegram_real_send_enabled must be false")
    if item.dashboard_enabled:
        raise ProviderCacheSafetyValidationError("dashboard_enabled must be false")

def validate_provider_cache_record(item: ProviderCacheRecord) -> None:
    if ".." in item.cache_path:
        raise ProviderCacheSafetyValidationError("Cache path traversal detected")

def validate_provider_cache_index(item: ProviderCacheIndex) -> None:
    for record in item.records:
        validate_provider_cache_record(record)

def validate_stale_fresh_policy(item: StaleFreshPolicy) -> None:
    pass

def validate_fallback_dry_run_plan(item: FallbackDryRunPlan) -> None:
    if not item.dry_run_only:
        raise ProviderCacheSafetyValidationError("Fallback plan dry_run_only must be true")
    if item.allow_network:
        raise ProviderCacheSafetyValidationError("Fallback plan allow_network must be false")

def validate_fallback_dry_run_result(item: FallbackDryRunResult) -> None:
    if item.network_used:
        raise ProviderCacheSafetyValidationError("Fallback result network_used must be false")
    if item.paid_api_used:
        raise ProviderCacheSafetyValidationError("paid_api_used must be false")
    if item.scraping_used or item.html_parsing_used or item.broker_used or item.order_created or item.paper_state_mutated or item.telegram_real_sent or item.dashboard_started:
         raise ProviderCacheSafetyValidationError("Unsafe execution used in fallback")

def validate_source_comparison_result(item: SourceComparisonResult) -> None:
    if not item.dry_run_only:
        raise ProviderCacheSafetyValidationError("Source comparison dry_run_only must be true")
    if item.network_used:
         raise ProviderCacheSafetyValidationError("Source comparison network_used must be false")

def validate_provider_cache_context(item: ProviderCacheContext) -> None:
    validate_provider_runtime_ingestion_result(item.ingestion)
    validate_provider_cache_index(item.cache_index)
    validate_stale_fresh_policy(item.stale_fresh_policy)
    for p in item.fallback_plans:
        validate_fallback_dry_run_plan(p)
    for r in item.fallback_results:
        validate_fallback_dry_run_result(r)
    for c in item.source_comparisons:
        validate_source_comparison_result(c)

def validate_provider_cache_full_review(item: ProviderCacheFullReview) -> None:
    validate_provider_cache_context(item.context)
