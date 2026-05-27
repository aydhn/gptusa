from dataclasses import dataclass, field
from typing import Any
import uuid
from usa_signal_bot.core.enums import (
    FactorValidationStatus,
    FactorValidationDecision,
    FactorValidationRuleKind,
    FactorValidationRuleStatus,
    FactorDriftStatus,
    FactorDriftMetricKind,
    FactorVersionStatus,
    FactorStoreHardeningStatus,
    FactorArtifactKind,
    FactorValidationQuality,
    FactorValidationRiskFlag,
    FactorValidationReportType
)
from usa_signal_bot.core.serialization import dataclass_to_dict

@dataclass
class FactorScoringIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: str | None
    source_review_id: str | None
    source_context_id: str | None
    available: bool
    factor_scoring_ready: bool
    factor_normalization_ready: bool
    factor_diagnostics_ready: bool
    factor_table_ready: bool
    ready_for_phase122: bool
    metadata_only: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    html_parse_enabled: bool
    paid_api_enabled: bool
    dashboard_enabled: bool
    network_default_enabled: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    valid_for_phase122: bool
    risk_flags: list[FactorValidationRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class FactorValidationRule:
    rule_id: str
    created_at_utc: str
    rule_kind: FactorValidationRuleKind
    name: str
    status: FactorValidationRuleStatus
    required: bool
    expected_value: Any | None
    observed_value: Any | None
    passed: bool
    symbol: str | None
    factor_column: str | None
    rationale: str
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorValidationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorValidationResult:
    validation_id: str
    created_at_utc: str
    symbol: str
    factor_table_path: str | None
    rules: list[FactorValidationRule]
    total_rules: int
    passed_rules: int
    warning_rules: int
    failed_rules: int
    blocked_rules: int
    validation_passed: bool
    quality: FactorValidationQuality
    factor_columns: list[str]
    forbidden_columns_present: list[str]
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorValidationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorDriftBaseline:
    baseline_id: str
    created_at_utc: str
    symbol: str
    factor_columns: list[str]
    baseline_window_start: str | None
    baseline_window_end: str | None
    row_count: int
    baseline_stats: dict[str, dict[str, Any]]
    baseline_hash: str | None
    baseline_valid: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorValidationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorDriftObservation:
    observation_id: str
    created_at_utc: str
    symbol: str
    factor_column: str
    metric_kind: FactorDriftMetricKind
    baseline_value: float | None
    observed_value: float | None
    absolute_change: float | None
    relative_change: float | None
    drift_score: float
    drift_status: FactorDriftStatus
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorValidationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorDriftReport:
    drift_report_id: str
    created_at_utc: str
    symbol: str
    baseline_id: str | None
    observations: list[FactorDriftObservation]
    overall_drift_status: FactorDriftStatus
    max_drift_score: float
    average_drift_score: float
    high_drift_factor_columns: list[str]
    critical_drift_factor_columns: list[str]
    baseline_available: bool
    drift_report_valid: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorValidationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorSchemaSignature:
    signature_id: str
    created_at_utc: str
    symbol: str | None
    required_columns: list[str]
    factor_columns: list[str]
    raw_factor_columns: list[str]
    normalized_factor_columns: list[str]
    percentile_factor_columns: list[str]
    rank_factor_columns: list[str]
    diagnostics_columns: list[str]
    schema_hash: str
    schema_version: str
    schema_valid: bool
    forbidden_columns_present: list[str]
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorValidationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorVersionMetadata:
    version_id: str
    created_at_utc: str
    version: str
    status: FactorVersionStatus
    source_review_id: str | None
    schema_signature_id: str | None
    artifact_hashes: dict[str, str]
    parent_version: str | None
    sealed: bool
    immutable: bool
    supersedes: str | None
    rollback_candidate: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorValidationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorArtifactManifestItem:
    artifact_id: str
    created_at_utc: str
    artifact_kind: FactorArtifactKind
    path: str | None
    artifact_hash: str | None
    size_bytes: int | None
    required: bool
    available: bool
    immutable: bool
    contains_secret: bool
    contains_forbidden_columns: bool
    contains_execution_language: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorValidationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorArtifactManifest:
    manifest_id: str
    created_at_utc: str
    version_id: str | None
    items: list[FactorArtifactManifestItem]
    total_items: int
    available_items: int
    missing_items: int
    invalid_items: int
    secret_violation_count: int
    forbidden_column_violation_count: int
    execution_language_violation_count: int
    manifest_hash: str | None
    manifest_valid: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorValidationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorStoreSnapshot:
    snapshot_id: str
    created_at_utc: str
    version_id: str | None
    snapshot_path: str | None
    included_artifacts: list[str]
    snapshot_hash: str | None
    artifact_count: int
    snapshot_valid: bool
    immutable: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorValidationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorRollbackMetadata:
    rollback_id: str
    created_at_utc: str
    current_version: str | None
    rollback_version: str | None
    rollback_available: bool
    rollback_reason: str | None
    rollback_metadata_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    order_creation_allowed: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorValidationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorStoreHardeningResult:
    hardening_id: str
    created_at_utc: str
    status: FactorStoreHardeningStatus
    schema_signature: FactorSchemaSignature
    version_metadata: FactorVersionMetadata
    artifact_manifest: FactorArtifactManifest
    snapshot: FactorStoreSnapshot
    rollback_metadata: FactorRollbackMetadata
    retention_policy: dict[str, Any]
    store_hardened: bool
    overwrite_safe: bool
    immutable_artifacts: bool
    no_secret_leak: bool
    no_forbidden_columns: bool
    no_execution_language: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorValidationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorValidationContext:
    context_id: str
    created_at_utc: str
    status: FactorValidationStatus
    decision: FactorValidationDecision
    source_factor_scoring_review_id: str | None
    ingestion: FactorScoringIngestionResult
    validation_results: list[FactorValidationResult]
    drift_baselines: list[FactorDriftBaseline]
    drift_reports: list[FactorDriftReport]
    schema_signatures: list[FactorSchemaSignature]
    version_metadata: FactorVersionMetadata
    artifact_manifest: FactorArtifactManifest
    store_snapshot: FactorStoreSnapshot
    rollback_metadata: FactorRollbackMetadata
    hardening_result: FactorStoreHardeningResult
    factor_validation_ready: bool
    drift_monitoring_ready: bool
    factor_versioning_ready: bool
    factor_store_hardened: bool
    ready_for_phase123: bool
    metadata_only: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    html_parse_enabled: bool
    paid_api_enabled: bool
    dashboard_enabled: bool
    network_default_enabled: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorValidationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorValidationFullReview:
    review_id: str
    created_at_utc: str
    report_type: FactorValidationReportType
    ingestion: FactorScoringIngestionResult
    context: FactorValidationContext
    validation_results: list[FactorValidationResult]
    drift_reports: list[FactorDriftReport]
    schema_signatures: list[FactorSchemaSignature]
    version_metadata: FactorVersionMetadata
    artifact_manifest: FactorArtifactManifest
    hardening_result: FactorStoreHardeningResult
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def create_factor_scoring_ingestion_id() -> str:
    return f"ingest-{uuid.uuid4().hex[:8]}"

def create_factor_validation_rule_id() -> str:
    return f"rule-{uuid.uuid4().hex[:8]}"

def create_factor_validation_result_id() -> str:
    return f"val-{uuid.uuid4().hex[:8]}"

def create_factor_drift_baseline_id() -> str:
    return f"baseline-{uuid.uuid4().hex[:8]}"

def create_factor_drift_observation_id() -> str:
    return f"obs-{uuid.uuid4().hex[:8]}"

def create_factor_drift_report_id() -> str:
    return f"drift-{uuid.uuid4().hex[:8]}"

def create_factor_schema_signature_id() -> str:
    return f"sig-{uuid.uuid4().hex[:8]}"

def create_factor_version_id() -> str:
    return f"ver-{uuid.uuid4().hex[:8]}"

def create_factor_manifest_item_id() -> str:
    return f"item-{uuid.uuid4().hex[:8]}"

def create_factor_artifact_manifest_id() -> str:
    return f"manifest-{uuid.uuid4().hex[:8]}"

def create_factor_store_snapshot_id() -> str:
    return f"snap-{uuid.uuid4().hex[:8]}"

def create_factor_rollback_id() -> str:
    return f"rb-{uuid.uuid4().hex[:8]}"

def create_factor_store_hardening_id() -> str:
    return f"hard-{uuid.uuid4().hex[:8]}"

def create_factor_validation_context_id() -> str:
    return f"ctx-{uuid.uuid4().hex[:8]}"

def create_factor_validation_full_review_id() -> str:
    return f"rev-{uuid.uuid4().hex[:8]}"

def factor_scoring_ingestion_result_to_dict(item: FactorScoringIngestionResult) -> dict:
    return dataclass_to_dict(item)

def factor_validation_rule_to_dict(item: FactorValidationRule) -> dict:
    return dataclass_to_dict(item)

def factor_validation_result_to_dict(item: FactorValidationResult) -> dict:
    return dataclass_to_dict(item)

def factor_drift_baseline_to_dict(item: FactorDriftBaseline) -> dict:
    return dataclass_to_dict(item)

def factor_drift_observation_to_dict(item: FactorDriftObservation) -> dict:
    return dataclass_to_dict(item)

def factor_drift_report_to_dict(item: FactorDriftReport) -> dict:
    return dataclass_to_dict(item)

def factor_schema_signature_to_dict(item: FactorSchemaSignature) -> dict:
    return dataclass_to_dict(item)

def factor_version_metadata_to_dict(item: FactorVersionMetadata) -> dict:
    return dataclass_to_dict(item)

def factor_artifact_manifest_item_to_dict(item: FactorArtifactManifestItem) -> dict:
    return dataclass_to_dict(item)

def factor_artifact_manifest_to_dict(item: FactorArtifactManifest) -> dict:
    return dataclass_to_dict(item)

def factor_store_snapshot_to_dict(item: FactorStoreSnapshot) -> dict:
    return dataclass_to_dict(item)

def factor_rollback_metadata_to_dict(item: FactorRollbackMetadata) -> dict:
    return dataclass_to_dict(item)

def factor_store_hardening_result_to_dict(item: FactorStoreHardeningResult) -> dict:
    return dataclass_to_dict(item)

def factor_validation_context_to_dict(item: FactorValidationContext) -> dict:
    return dataclass_to_dict(item)

def factor_validation_full_review_to_dict(item: FactorValidationFullReview) -> dict:
    return dataclass_to_dict(item)

def validate_factor_scoring_ingestion_result(item: FactorScoringIngestionResult) -> None:
    if not item.factor_scoring_ready or not item.factor_normalization_ready or not item.factor_diagnostics_ready or not item.factor_table_ready:
        item.valid_for_phase122 = False
    if not item.ready_for_phase122:
        item.valid_for_phase122 = False
    if not item.research_data_only:
        item.valid_for_phase122 = False
    if item.activation_allowed or item.strategy_activation_allowed or item.active_paper_enabled:
        item.valid_for_phase122 = False
    if item.broker_execution_enabled or item.order_creation_enabled or item.paper_state_mutation_enabled:
        item.valid_for_phase122 = False
    if item.telegram_real_send_enabled or item.scraping_enabled or item.html_parse_enabled or item.paid_api_enabled:
        item.valid_for_phase122 = False
    if item.dashboard_enabled or item.network_default_enabled:
        item.valid_for_phase122 = False
    if item.produces_trade_signal or item.produces_order_decision or item.produces_portfolio_weights:
        item.valid_for_phase122 = False
    if item.network_used or item.paid_api_used or item.scraping_used or item.html_parsing_used:
        item.valid_for_phase122 = False
    if item.broker_used or item.order_created or item.paper_state_mutated or item.telegram_real_sent or item.dashboard_started:
        item.valid_for_phase122 = False

def validate_factor_validation_result(item: FactorValidationResult) -> None:
    pass

def validate_factor_drift_baseline(item: FactorDriftBaseline) -> None:
    pass

def validate_factor_drift_report(item: FactorDriftReport) -> None:
    pass

def validate_factor_schema_signature(item: FactorSchemaSignature) -> None:
    if len(item.forbidden_columns_present) > 0:
        item.schema_valid = False

def validate_factor_version_metadata(item: FactorVersionMetadata) -> None:
    if not item.sealed or not item.immutable:
        item.warnings.append("Version is not sealed or immutable")
    if item.activation_allowed or item.strategy_activation_allowed:
        item.errors.append("Version enables activation")

def validate_factor_artifact_manifest(item: FactorArtifactManifest) -> None:
    if item.secret_violation_count > 0 or item.forbidden_column_violation_count > 0 or item.execution_language_violation_count > 0:
        item.manifest_valid = False

def validate_factor_store_snapshot(item: FactorStoreSnapshot) -> None:
    if not item.research_data_only:
        item.snapshot_valid = False

def validate_factor_rollback_metadata(item: FactorRollbackMetadata) -> None:
    if item.activation_allowed or item.strategy_activation_allowed or item.order_creation_allowed:
        item.warnings.append("Rollback allows activation")

def validate_factor_store_hardening_result(item: FactorStoreHardeningResult) -> None:
    if not item.no_secret_leak or not item.no_forbidden_columns or not item.no_execution_language:
        item.store_hardened = False
    if not item.research_data_only:
        item.store_hardened = False

def validate_factor_validation_context(item: FactorValidationContext) -> None:
    pass

def validate_factor_validation_full_review(item: FactorValidationFullReview) -> None:
    pass
