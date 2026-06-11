from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid
import datetime

from usa_signal_bot.core.exceptions import Phase134ValidationError
from usa_signal_bot.core.enums import (
    RegimeResearchFreezeStatus,
    RegimeResearchFreezeDecision,
    MonitoringValidationRuleKind,
    MonitoringValidationStatus,
    DriftReportQaStatus,
    DriftReportLanguageRiskKind,
    DriftReportSectionKind,
    ResearchFreezeArtifactKind,
    ResearchFreezeReadinessStatus,
    ResearchFreezeReadinessRuleKind,
    ResearchFreezeQuality,
    ResearchFreezeRiskFlag,
    RegimeResearchFreezeReportType,
)


def _now_utc_str() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


@dataclass
class RegimeMonitoringIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    context_validation_ingested: bool
    artifacts_loaded: bool
    baseline_built: bool
    snapshot_built: bool
    drift_tracked: bool
    degradation_diagnostics_built: bool
    readiness_gate_built: bool
    readiness_gate_passed: bool
    ready_for_phase134: bool
    metadata_only: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
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
    model_training_used: bool
    model_prediction_used: bool
    heavy_ml_dependency_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    daemon_started: bool
    scheduler_enabled: bool
    valid_for_phase134: bool
    risk_flags: List[ResearchFreezeRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MonitoringValidationRule:
    rule_id: str
    created_at_utc: str
    rule_kind: MonitoringValidationRuleKind
    name: str
    status: MonitoringValidationStatus
    required: bool
    passed: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    rationale: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ResearchFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MonitoringValidationResult:
    validation_id: str
    created_at_utc: str
    rules: List[MonitoringValidationRule]
    total_rules: int
    passed_rules: int
    warning_rules: int
    failed_rules: int
    blocked_rules: int
    validation_passed: bool
    baseline_available: bool
    snapshot_available: bool
    drift_result_available: bool
    degradation_diagnostics_available: bool
    monitoring_readiness_gate_passed: bool
    consistency_valid: bool
    safety_boundary_valid: bool
    quality: ResearchFreezeQuality
    research_metadata_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    model_training_used: bool
    model_prediction_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ResearchFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DriftReportSection:
    section_id: str
    created_at_utc: str
    section_kind: DriftReportSectionKind
    title: str
    body: str
    bullet_points: List[str] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    qa_status: DriftReportQaStatus = DriftReportQaStatus.NOT_CHECKED
    language_risks: List[DriftReportLanguageRiskKind] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DriftReportDocument:
    document_id: str
    created_at_utc: str
    title: str
    sections: List[DriftReportSection]
    source_review_id: Optional[str]
    rendered_markdown: Optional[str]
    rendered_text: Optional[str]
    rendered_json: Optional[Dict[str, Any]]
    document_hash: Optional[str]
    research_metadata_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    qa_status: DriftReportQaStatus
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ResearchFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DriftReportQaRuleResult:
    qa_result_id: str
    created_at_utc: str
    rule_name: str
    status: DriftReportQaStatus
    passed: bool
    language_risk: Optional[DriftReportLanguageRiskKind]
    matched_terms: List[str] = field(default_factory=list)
    field_name: Optional[str] = None
    message: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResearchFreezeArtifactReference:
    reference_id: str
    created_at_utc: str
    artifact_kind: ResearchFreezeArtifactKind
    artifact_name: str
    source_phase: int
    source_path: Optional[str]
    source_review_id: Optional[str]
    artifact_hash: Optional[str]
    required: bool
    available: bool
    immutable: bool
    research_metadata_only: bool
    activation_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ResearchFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResearchFreezePackage:
    package_id: str
    created_at_utc: str
    package_name: str
    package_version: str
    artifact_references: List[ResearchFreezeArtifactReference]
    drift_report: DriftReportDocument
    monitoring_validation: MonitoringValidationResult
    required_artifact_count: int
    available_required_artifact_count: int
    missing_required_artifact_count: int
    package_hash: Optional[str]
    manifest_hash: Optional[str]
    package_valid: bool
    quality: ResearchFreezeQuality
    research_metadata_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    model_training_used: bool
    model_prediction_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ResearchFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResearchFreezeReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: ResearchFreezeReadinessRuleKind
    name: str
    status: ResearchFreezeReadinessStatus
    required: bool
    passed: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    rationale: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ResearchFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResearchFreezeReadinessGate:
    gate_id: str
    created_at_utc: str
    status: ResearchFreezeReadinessStatus
    rules: List[ResearchFreezeReadinessRule]
    freeze_package: ResearchFreezePackage
    ready_for_phase135: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    model_training_used: bool
    model_prediction_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ResearchFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RegimeResearchFreezeContext:
    context_id: str
    created_at_utc: str
    status: RegimeResearchFreezeStatus
    decision: RegimeResearchFreezeDecision
    source_regime_monitoring_review_id: Optional[str]
    ingestion: RegimeMonitoringIngestionResult
    monitoring_validation: MonitoringValidationResult
    drift_report: DriftReportDocument
    drift_report_qa_results: List[DriftReportQaRuleResult]
    freeze_package: ResearchFreezePackage
    readiness_gate: ResearchFreezeReadinessGate
    monitoring_ingested: bool
    monitoring_artifacts_loaded: bool
    monitoring_validated: bool
    drift_report_built: bool
    drift_report_qa_passed: bool
    freeze_package_built: bool
    freeze_package_validated: bool
    readiness_gate_built: bool
    readiness_gate_passed: bool
    ready_for_phase135: bool
    metadata_only: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
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
    model_training_used: bool
    model_prediction_used: bool
    heavy_ml_dependency_used: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    daemon_started: bool
    scheduler_enabled: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ResearchFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RegimeResearchFreezeFullReview:
    review_id: str
    created_at_utc: str
    report_type: RegimeResearchFreezeReportType
    ingestion: RegimeMonitoringIngestionResult
    context: RegimeResearchFreezeContext
    monitoring_validation: MonitoringValidationResult
    drift_report: DriftReportDocument
    drift_report_qa_results: List[DriftReportQaRuleResult]
    freeze_package: ResearchFreezePackage
    readiness_gate: ResearchFreezeReadinessGate
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def create_regime_monitoring_ingestion_id() -> str:
    return f"ingest_{uuid.uuid4().hex[:12]}"


def create_monitoring_validation_rule_id() -> str:
    return f"val_rule_{uuid.uuid4().hex[:12]}"


def create_monitoring_validation_result_id() -> str:
    return f"val_res_{uuid.uuid4().hex[:12]}"


def create_drift_report_section_id() -> str:
    return f"drift_sec_{uuid.uuid4().hex[:12]}"


def create_drift_report_document_id() -> str:
    return f"drift_doc_{uuid.uuid4().hex[:12]}"


def create_drift_report_qa_result_id() -> str:
    return f"drift_qa_{uuid.uuid4().hex[:12]}"


def create_research_freeze_artifact_reference_id() -> str:
    return f"freeze_ref_{uuid.uuid4().hex[:12]}"


def create_research_freeze_package_id() -> str:
    return f"freeze_pkg_{uuid.uuid4().hex[:12]}"


def create_research_freeze_readiness_rule_id() -> str:
    return f"ready_rule_{uuid.uuid4().hex[:12]}"


def create_research_freeze_readiness_gate_id() -> str:
    return f"ready_gate_{uuid.uuid4().hex[:12]}"


def create_regime_research_freeze_context_id() -> str:
    return f"ctx_{uuid.uuid4().hex[:12]}"


def create_regime_research_freeze_full_review_id() -> str:
    return f"rev_{uuid.uuid4().hex[:12]}"


def regime_monitoring_ingestion_result_to_dict(
    item: RegimeMonitoringIngestionResult,
) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def monitoring_validation_rule_to_dict(item: MonitoringValidationRule) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def monitoring_validation_result_to_dict(item: MonitoringValidationResult) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def drift_report_section_to_dict(item: DriftReportSection) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def drift_report_document_to_dict(item: DriftReportDocument) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def drift_report_qa_rule_result_to_dict(item: DriftReportQaRuleResult) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def research_freeze_artifact_reference_to_dict(
    item: ResearchFreezeArtifactReference,
) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def research_freeze_package_to_dict(item: ResearchFreezePackage) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def research_freeze_readiness_rule_to_dict(item: ResearchFreezeReadinessRule) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def research_freeze_readiness_gate_to_dict(item: ResearchFreezeReadinessGate) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def regime_research_freeze_context_to_dict(item: RegimeResearchFreezeContext) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def regime_research_freeze_full_review_to_dict(
    item: RegimeResearchFreezeFullReview,
) -> dict:
    from usa_signal_bot.core.serialization import to_dict_clean

    return to_dict_clean(item)


def validate_regime_monitoring_ingestion_result(
    item: RegimeMonitoringIngestionResult,
) -> None:
    if hasattr(item, "research_metadata_only") and not item.research_metadata_only:
        raise Phase134ValidationError("research_metadata_only must be True")
    if hasattr(item, "produces_trade_signal") and item.produces_trade_signal:
        raise Phase134ValidationError("produces_trade_signal must be False")
    if hasattr(item, "produces_order_decision") and item.produces_order_decision:
        raise Phase134ValidationError("produces_order_decision must be False")


def validate_monitoring_validation_rule(item: MonitoringValidationRule) -> None:
    if hasattr(item, "research_metadata_only") and not item.research_metadata_only:
        raise Phase134ValidationError("research_metadata_only must be True")
    if hasattr(item, "produces_trade_signal") and item.produces_trade_signal:
        raise Phase134ValidationError("produces_trade_signal must be False")
    if hasattr(item, "produces_order_decision") and item.produces_order_decision:
        raise Phase134ValidationError("produces_order_decision must be False")


def validate_monitoring_validation_result(item: MonitoringValidationResult) -> None:
    if hasattr(item, "research_metadata_only") and not item.research_metadata_only:
        raise Phase134ValidationError("research_metadata_only must be True")
    if hasattr(item, "produces_trade_signal") and item.produces_trade_signal:
        raise Phase134ValidationError("produces_trade_signal must be False")
    if hasattr(item, "produces_order_decision") and item.produces_order_decision:
        raise Phase134ValidationError("produces_order_decision must be False")


def validate_drift_report_section(item: DriftReportSection) -> None:
    if hasattr(item, "research_metadata_only") and not item.research_metadata_only:
        raise Phase134ValidationError("research_metadata_only must be True")
    if hasattr(item, "produces_trade_signal") and item.produces_trade_signal:
        raise Phase134ValidationError("produces_trade_signal must be False")
    if hasattr(item, "produces_order_decision") and item.produces_order_decision:
        raise Phase134ValidationError("produces_order_decision must be False")


def validate_drift_report_document(item: DriftReportDocument) -> None:
    if hasattr(item, "research_metadata_only") and not item.research_metadata_only:
        raise Phase134ValidationError("research_metadata_only must be True")
    if hasattr(item, "produces_trade_signal") and item.produces_trade_signal:
        raise Phase134ValidationError("produces_trade_signal must be False")
    if hasattr(item, "produces_order_decision") and item.produces_order_decision:
        raise Phase134ValidationError("produces_order_decision must be False")


def validate_drift_report_qa_rule_result(item: DriftReportQaRuleResult) -> None:
    if hasattr(item, "research_metadata_only") and not item.research_metadata_only:
        raise Phase134ValidationError("research_metadata_only must be True")
    if hasattr(item, "produces_trade_signal") and item.produces_trade_signal:
        raise Phase134ValidationError("produces_trade_signal must be False")
    if hasattr(item, "produces_order_decision") and item.produces_order_decision:
        raise Phase134ValidationError("produces_order_decision must be False")


def validate_research_freeze_artifact_reference(
    item: ResearchFreezeArtifactReference,
) -> None:
    if hasattr(item, "research_metadata_only") and not item.research_metadata_only:
        raise Phase134ValidationError("research_metadata_only must be True")
    if hasattr(item, "produces_trade_signal") and item.produces_trade_signal:
        raise Phase134ValidationError("produces_trade_signal must be False")
    if hasattr(item, "produces_order_decision") and item.produces_order_decision:
        raise Phase134ValidationError("produces_order_decision must be False")


def validate_research_freeze_package(item: ResearchFreezePackage) -> None:
    if hasattr(item, "research_metadata_only") and not item.research_metadata_only:
        raise Phase134ValidationError("research_metadata_only must be True")
    if hasattr(item, "produces_trade_signal") and item.produces_trade_signal:
        raise Phase134ValidationError("produces_trade_signal must be False")
    if hasattr(item, "produces_order_decision") and item.produces_order_decision:
        raise Phase134ValidationError("produces_order_decision must be False")


def validate_research_freeze_readiness_rule(item: ResearchFreezeReadinessRule) -> None:
    if hasattr(item, "research_metadata_only") and not item.research_metadata_only:
        raise Phase134ValidationError("research_metadata_only must be True")
    if hasattr(item, "produces_trade_signal") and item.produces_trade_signal:
        raise Phase134ValidationError("produces_trade_signal must be False")
    if hasattr(item, "produces_order_decision") and item.produces_order_decision:
        raise Phase134ValidationError("produces_order_decision must be False")


def validate_research_freeze_readiness_gate(item: ResearchFreezeReadinessGate) -> None:
    if hasattr(item, "research_metadata_only") and not item.research_metadata_only:
        raise Phase134ValidationError("research_metadata_only must be True")
    if hasattr(item, "produces_trade_signal") and item.produces_trade_signal:
        raise Phase134ValidationError("produces_trade_signal must be False")
    if hasattr(item, "produces_order_decision") and item.produces_order_decision:
        raise Phase134ValidationError("produces_order_decision must be False")


def validate_regime_research_freeze_context(item: RegimeResearchFreezeContext) -> None:
    if hasattr(item, "research_metadata_only") and not item.research_metadata_only:
        raise Phase134ValidationError("research_metadata_only must be True")
    if hasattr(item, "produces_trade_signal") and item.produces_trade_signal:
        raise Phase134ValidationError("produces_trade_signal must be False")
    if hasattr(item, "produces_order_decision") and item.produces_order_decision:
        raise Phase134ValidationError("produces_order_decision must be False")


def validate_regime_research_freeze_full_review(
    item: RegimeResearchFreezeFullReview,
) -> None:
    if hasattr(item, "research_metadata_only") and not item.research_metadata_only:
        raise Phase134ValidationError("research_metadata_only must be True")
    if hasattr(item, "produces_trade_signal") and item.produces_trade_signal:
        raise Phase134ValidationError("produces_trade_signal must be False")
    if hasattr(item, "produces_order_decision") and item.produces_order_decision:
        raise Phase134ValidationError("produces_order_decision must be False")
