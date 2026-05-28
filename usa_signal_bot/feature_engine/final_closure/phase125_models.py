import uuid
import datetime
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
from usa_signal_bot.core.enums import (
    FeatureFactorFinalClosureStatus,
    FeatureFactorFinalClosureDecision,
    FinalClosureRuleKind,
    FinalClosureRuleStatus,
    FreezeSealStatus,
    EngineReadinessCertificateStatus,
    Phase126KickoffGateStatus,
    Phase126KickoffRequirementKind,
    FinalClosureArtifactKind,
    FinalClosureQuality,
    FinalClosureRiskFlag,
    FinalClosureReportType
)
from usa_signal_bot.core.exceptions import (
    FeatureFactorFinalClosureError,
    FreezePreparationIngestionError,
    FinalArtifactChainLoaderError,
    FinalClosureChecksError,
    FinalSchemaLineageSafetyClosureError,
    FreezeSealBuilderError,
    EngineReadinessCertificateError,
    Phase126KickoffGateError,
    FinalClosureSafetyValidationError,
    FinalClosureStoreError,
    FinalClosureValidationError,
    FinalClosureReportingError
)

@dataclass
class FreezePreparationIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    artifact_chain_ready: bool
    integration_rehearsal_ready: bool
    report_qa_accepted: bool
    freeze_candidate_ready: bool
    freeze_readiness_gate_ready: bool
    ready_for_phase125: bool
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
    investment_advice: bool
    deployment_allowed: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    valid_for_phase125: bool
    risk_flags: List[FinalClosureRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class FinalClosureArtifactReference:
    reference_id: str
    created_at_utc: str
    artifact_kind: FinalClosureArtifactKind
    phase_number: Optional[int]
    artifact_name: str
    artifact_path: Optional[str]
    artifact_hash: Optional[str]
    schema_signature: Optional[str]
    lineage_reference: Optional[str]
    safety_reference: Optional[str]
    required: bool
    available: bool
    immutable: bool
    research_data_only: bool
    contains_secret: bool
    contains_forbidden_columns: bool
    contains_execution_language: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[FinalClosureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class FinalClosureRule:
    rule_id: str
    created_at_utc: str
    rule_kind: FinalClosureRuleKind
    name: str
    status: FinalClosureRuleStatus
    required: bool
    passed: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[FinalClosureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class FinalClosureResult:
    closure_result_id: str
    created_at_utc: str
    rules: List[FinalClosureRule]
    total_rules: int
    passed_rules: int
    warning_rules: int
    failed_rules: int
    blocked_rules: int
    closure_passed: bool
    quality: FinalClosureQuality
    artifact_count: int
    missing_required_artifact_count: int
    unsafe_artifact_count: int
    warnings: List[str]
    errors: List[str]
    risk_flags: List[FinalClosureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class FinalClosureManifest:
    manifest_id: str
    created_at_utc: str
    artifacts: List[FinalClosureArtifactReference]
    total_artifacts: int
    required_artifacts: int
    available_artifacts: int
    missing_required_artifacts: int
    manifest_hash: Optional[str]
    manifest_version: str
    immutable: bool
    research_data_only: bool
    no_secret_leak: bool
    no_forbidden_columns: bool
    no_execution_language: bool
    final_manifest_valid: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[FinalClosureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class FreezeSealMetadata:
    seal_id: str
    created_at_utc: str
    status: FreezeSealStatus
    seal_version: str
    source_manifest_id: Optional[str]
    source_manifest_hash: Optional[str]
    seal_hash: Optional[str]
    sealed: bool
    immutable: bool
    freeze_scope: List[str]
    phase_range: str
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[FinalClosureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EngineReadinessCertificate:
    certificate_id: str
    created_at_utc: str
    status: EngineReadinessCertificateStatus
    certificate_version: str
    source_seal_id: Optional[str]
    feature_factor_engine_closed: bool
    freeze_seal_valid: bool
    final_manifest_valid: bool
    schema_contract_available: bool
    lineage_contract_available: bool
    safety_contract_available: bool
    factor_tables_available: bool
    factor_diagnostics_available: bool
    research_reports_available: bool
    ready_for_phase126: bool
    certified_for_research_handoff: bool
    certified_for_trading_activation: bool
    certified_for_deployment: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[FinalClosureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class Phase126KickoffRequirement:
    requirement_id: str
    created_at_utc: str
    requirement_kind: Phase126KickoffRequirementKind
    name: str
    status: Phase126KickoffGateStatus
    required: bool
    passed: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[FinalClosureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class Phase126KickoffGate:
    gate_id: str
    created_at_utc: str
    status: Phase126KickoffGateStatus
    requirements: List[Phase126KickoffRequirement]
    total_requirements: int
    passed_requirements: int
    failed_requirements: int
    blocked_requirements: int
    ready_for_phase126: bool
    regime_classification_input_contract_ready: bool
    feature_factor_engine_closed: bool
    freeze_seal_valid: bool
    engine_certificate_valid: bool
    research_handoff_ready: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[FinalClosureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class FinalClosureAudit:
    audit_id: str
    created_at_utc: str
    phase_range: str
    artifact_hashes: Dict[str, str]
    final_manifest_hash: Optional[str]
    seal_hash: Optional[str]
    certificate_id: Optional[str]
    kickoff_gate_id: Optional[str]
    deterministic: bool
    local_only: bool
    no_network: bool
    no_broker: bool
    no_order: bool
    no_paper_mutation: bool
    no_trade_signal: bool
    no_portfolio_weights: bool
    no_investment_advice: bool
    no_deployment: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[FinalClosureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class FinalClosureContext:
    context_id: str
    created_at_utc: str
    status: FeatureFactorFinalClosureStatus
    decision: FeatureFactorFinalClosureDecision
    source_freeze_preparation_review_id: Optional[str]
    ingestion: FreezePreparationIngestionResult
    artifacts: List[FinalClosureArtifactReference]
    closure_result: FinalClosureResult
    final_manifest: FinalClosureManifest
    freeze_seal: FreezeSealMetadata
    readiness_certificate: EngineReadinessCertificate
    phase126_kickoff_gate: Phase126KickoffGate
    audit: FinalClosureAudit
    final_artifacts_ready: bool
    final_checks_passed: bool
    freeze_seal_ready: bool
    engine_certificate_ready: bool
    phase126_kickoff_gate_ready: bool
    feature_factor_engine_final_closed: bool
    ready_for_phase126: bool
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
    deployment_allowed: bool
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
    warnings: List[str]
    errors: List[str]
    risk_flags: List[FinalClosureRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class FinalClosureFullReview:
    review_id: str
    created_at_utc: str
    report_type: FinalClosureReportType
    ingestion: FreezePreparationIngestionResult
    context: FinalClosureContext
    closure_result: FinalClosureResult
    final_manifest: FinalClosureManifest
    freeze_seal: FreezeSealMetadata
    readiness_certificate: EngineReadinessCertificate
    phase126_kickoff_gate: Phase126KickoffGate
    audit: FinalClosureAudit
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]


def create_freeze_preparation_ingestion_id() -> str:
    return f"fpi_{uuid.uuid4().hex[:8]}"

def create_final_closure_artifact_reference_id() -> str:
    return f"fca_{uuid.uuid4().hex[:8]}"

def create_final_closure_rule_id() -> str:
    return f"fcr_{uuid.uuid4().hex[:8]}"

def create_final_closure_result_id() -> str:
    return f"fcres_{uuid.uuid4().hex[:8]}"

def create_final_closure_manifest_id() -> str:
    return f"fcm_{uuid.uuid4().hex[:8]}"

def create_freeze_seal_id() -> str:
    return f"fsl_{uuid.uuid4().hex[:8]}"

def create_engine_readiness_certificate_id() -> str:
    return f"erc_{uuid.uuid4().hex[:8]}"

def create_phase126_kickoff_requirement_id() -> str:
    return f"p126kr_{uuid.uuid4().hex[:8]}"

def create_phase126_kickoff_gate_id() -> str:
    return f"p126kg_{uuid.uuid4().hex[:8]}"

def create_final_closure_audit_id() -> str:
    return f"fcaud_{uuid.uuid4().hex[:8]}"

def create_final_closure_context_id() -> str:
    return f"fcc_{uuid.uuid4().hex[:8]}"

def create_final_closure_full_review_id() -> str:
    return f"fcfr_{uuid.uuid4().hex[:8]}"

def freeze_preparation_ingestion_result_to_dict(item: FreezePreparationIngestionResult) -> dict:
    import dataclasses
    d = dataclasses.asdict(item)
    d['risk_flags'] = [f.value for f in d['risk_flags']]
    return d

def final_closure_artifact_reference_to_dict(item: FinalClosureArtifactReference) -> dict:
    import dataclasses
    d = dataclasses.asdict(item)
    d['artifact_kind'] = d['artifact_kind'].value
    d['risk_flags'] = [f.value for f in d['risk_flags']]
    return d

def final_closure_rule_to_dict(item: FinalClosureRule) -> dict:
    import dataclasses
    d = dataclasses.asdict(item)
    d['rule_kind'] = d['rule_kind'].value
    d['status'] = d['status'].value
    d['risk_flags'] = [f.value for f in d['risk_flags']]
    return d

def final_closure_result_to_dict(item: FinalClosureResult) -> dict:
    import dataclasses
    d = dataclasses.asdict(item)
    d['rules'] = [final_closure_rule_to_dict(r) for r in item.rules]
    d['quality'] = d['quality'].value
    d['risk_flags'] = [f.value for f in d['risk_flags']]
    return d

def final_closure_manifest_to_dict(item: FinalClosureManifest) -> dict:
    import dataclasses
    d = dataclasses.asdict(item)
    d['artifacts'] = [final_closure_artifact_reference_to_dict(r) for r in item.artifacts]
    d['risk_flags'] = [f.value for f in d['risk_flags']]
    return d

def freeze_seal_metadata_to_dict(item: FreezeSealMetadata) -> dict:
    import dataclasses
    d = dataclasses.asdict(item)
    d['status'] = d['status'].value
    d['risk_flags'] = [f.value for f in d['risk_flags']]
    return d

def engine_readiness_certificate_to_dict(item: EngineReadinessCertificate) -> dict:
    import dataclasses
    d = dataclasses.asdict(item)
    d['status'] = d['status'].value
    d['risk_flags'] = [f.value for f in d['risk_flags']]
    return d

def phase126_kickoff_requirement_to_dict(item: Phase126KickoffRequirement) -> dict:
    import dataclasses
    d = dataclasses.asdict(item)
    d['requirement_kind'] = d['requirement_kind'].value
    d['status'] = d['status'].value
    d['risk_flags'] = [f.value for f in d['risk_flags']]
    return d

def phase126_kickoff_gate_to_dict(item: Phase126KickoffGate) -> dict:
    import dataclasses
    d = dataclasses.asdict(item)
    d['status'] = d['status'].value
    d['requirements'] = [phase126_kickoff_requirement_to_dict(r) for r in item.requirements]
    d['risk_flags'] = [f.value for f in d['risk_flags']]
    return d

def final_closure_audit_to_dict(item: FinalClosureAudit) -> dict:
    import dataclasses
    d = dataclasses.asdict(item)
    d['risk_flags'] = [f.value for f in d['risk_flags']]
    return d

def final_closure_context_to_dict(item: FinalClosureContext) -> dict:
    import dataclasses
    d = dataclasses.asdict(item)
    d['status'] = d['status'].value
    d['decision'] = d['decision'].value
    d['ingestion'] = freeze_preparation_ingestion_result_to_dict(item.ingestion)
    d['artifacts'] = [final_closure_artifact_reference_to_dict(r) for r in item.artifacts]
    d['closure_result'] = final_closure_result_to_dict(item.closure_result)
    d['final_manifest'] = final_closure_manifest_to_dict(item.final_manifest)
    d['freeze_seal'] = freeze_seal_metadata_to_dict(item.freeze_seal)
    d['readiness_certificate'] = engine_readiness_certificate_to_dict(item.readiness_certificate)
    d['phase126_kickoff_gate'] = phase126_kickoff_gate_to_dict(item.phase126_kickoff_gate)
    d['audit'] = final_closure_audit_to_dict(item.audit)
    d['risk_flags'] = [f.value for f in d['risk_flags']]
    return d

def final_closure_full_review_to_dict(item: FinalClosureFullReview) -> dict:
    import dataclasses
    d = dataclasses.asdict(item)
    d['report_type'] = d['report_type'].value
    d['ingestion'] = freeze_preparation_ingestion_result_to_dict(item.ingestion)
    d['context'] = final_closure_context_to_dict(item.context)
    d['closure_result'] = final_closure_result_to_dict(item.closure_result)
    d['final_manifest'] = final_closure_manifest_to_dict(item.final_manifest)
    d['freeze_seal'] = freeze_seal_metadata_to_dict(item.freeze_seal)
    d['readiness_certificate'] = engine_readiness_certificate_to_dict(item.readiness_certificate)
    d['phase126_kickoff_gate'] = phase126_kickoff_gate_to_dict(item.phase126_kickoff_gate)
    d['audit'] = final_closure_audit_to_dict(item.audit)
    return d

def validate_freeze_preparation_ingestion_result(item: FreezePreparationIngestionResult) -> None:
    if not item.artifact_chain_ready: raise FreezePreparationIngestionError("artifact_chain_ready must be true")
    if not item.integration_rehearsal_ready: raise FreezePreparationIngestionError("integration_rehearsal_ready must be true")
    if not item.report_qa_accepted: raise FreezePreparationIngestionError("report_qa_accepted must be true")
    if not item.freeze_candidate_ready: raise FreezePreparationIngestionError("freeze_candidate_ready must be true")
    if not item.freeze_readiness_gate_ready: raise FreezePreparationIngestionError("freeze_readiness_gate_ready must be true")
    if not item.ready_for_phase125: raise FreezePreparationIngestionError("ready_for_phase125 must be true")
    if not item.research_data_only: raise FreezePreparationIngestionError("research_data_only must be true")

    _validate_non_execution_properties(item, FreezePreparationIngestionError)

def validate_final_closure_artifact_reference(item: FinalClosureArtifactReference) -> None:
    pass

def validate_final_closure_result(item: FinalClosureResult) -> None:
    pass

def validate_final_closure_manifest(item: FinalClosureManifest) -> None:
    if not item.no_secret_leak: raise FinalClosureValidationError("Final manifest no_secret_leak must be true")
    if not item.no_forbidden_columns: raise FinalClosureValidationError("Final manifest no_forbidden_columns must be true")
    if not item.no_execution_language: raise FinalClosureValidationError("Final manifest no_execution_language must be true")

def validate_freeze_seal_metadata(item: FreezeSealMetadata) -> None:
    if not item.sealed: raise FinalClosureValidationError("Freeze seal sealed must be true")
    if not item.immutable: raise FinalClosureValidationError("Freeze seal immutable must be true")

def validate_engine_readiness_certificate(item: EngineReadinessCertificate) -> None:
    if not item.certified_for_research_handoff: raise FinalClosureValidationError("Engine certificate certified_for_research_handoff must be true")
    if item.certified_for_trading_activation: raise FinalClosureValidationError("Engine certificate certified_for_trading_activation must be false")
    if item.certified_for_deployment: raise FinalClosureValidationError("Engine certificate certified_for_deployment must be false")

def validate_phase126_kickoff_gate(item: Phase126KickoffGate) -> None:
    pass # condition handled inside builder based on valid closure

def validate_final_closure_audit(item: FinalClosureAudit) -> None:
    pass

def validate_final_closure_context(item: FinalClosureContext) -> None:
    _validate_non_execution_properties(item, FinalClosureValidationError)

def validate_final_closure_full_review(item: FinalClosureFullReview) -> None:
    pass

def _validate_non_execution_properties(item: Any, exception_class) -> None:
    if item.activation_allowed: raise exception_class("activation_allowed must be false")
    if item.strategy_activation_allowed: raise exception_class("strategy_activation_allowed must be false")
    if item.deployment_allowed: raise exception_class("deployment_allowed must be false")
    if item.active_paper_enabled: raise exception_class("active_paper_enabled must be false")
    if item.broker_execution_enabled: raise exception_class("broker_execution_enabled must be false")
    if item.order_creation_enabled: raise exception_class("order_creation_enabled must be false")
    if item.paper_state_mutation_enabled: raise exception_class("paper_state_mutation_enabled must be false")
    if item.telegram_real_send_enabled: raise exception_class("telegram_real_send_enabled must be false")
    if item.scraping_enabled: raise exception_class("scraping_enabled must be false")
    if item.html_parse_enabled: raise exception_class("html_parse_enabled must be false")
    if item.paid_api_enabled: raise exception_class("paid_api_enabled must be false")
    if item.dashboard_enabled: raise exception_class("dashboard_enabled must be false")
    if item.network_default_enabled: raise exception_class("network_default_enabled must be false")
    if item.produces_trade_signal: raise exception_class("produces_trade_signal must be false")
    if item.produces_order_decision: raise exception_class("produces_order_decision must be false")
    if item.produces_portfolio_weights: raise exception_class("produces_portfolio_weights must be false")
    if item.investment_advice: raise exception_class("investment_advice must be false")
    if item.network_used: raise exception_class("network_used must be false")
    if item.paid_api_used: raise exception_class("paid_api_used must be false")
    if item.scraping_used: raise exception_class("scraping_used must be false")
    if item.html_parsing_used: raise exception_class("html_parsing_used must be false")
    if item.broker_used: raise exception_class("broker_used must be false")
    if item.order_created: raise exception_class("order_created must be false")
    if item.paper_state_mutated: raise exception_class("paper_state_mutated must be false")
    if item.telegram_real_sent: raise exception_class("telegram_real_sent must be false")
    if item.dashboard_started: raise exception_class("dashboard_started must be false")
