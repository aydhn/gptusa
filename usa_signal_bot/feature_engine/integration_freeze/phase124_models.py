"""Phase 124 Integration Freeze Models."""
from dataclasses import dataclass, field
from typing import Any
import uuid
import datetime

from usa_signal_bot.core.enums import (
    FreezePreparationRiskFlag, ArtifactChainPhase, ArtifactChainStatus,
    IntegrationRehearsalStepKind, IntegrationRehearsalStepStatus,
    ReportQaAcceptanceStatus, FreezeCandidateStatus, FreezeReadinessStatus,
    FreezeReadinessRuleKind, FreezePreparationQuality,
    FeatureFactorIntegrationStatus, FeatureFactorIntegrationDecision,
    FreezePreparationReportType
)

@dataclass
class ExplainabilityIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: str | None
    source_review_id: str | None
    source_context_id: str | None
    available: bool
    attribution_ready: bool
    contribution_ready: bool
    interpretation_ready: bool
    research_report_ready: bool
    report_qa_passed: bool
    ready_for_phase124: bool
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
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    valid_for_phase124: bool
    risk_flags: list[FreezePreparationRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ArtifactChainReference:
    reference_id: str
    created_at_utc: str
    phase: ArtifactChainPhase
    artifact_name: str
    artifact_path: str | None
    artifact_hash: str | None
    artifact_required: bool
    artifact_available: bool
    schema_signature: str | None
    lineage_ref: str | None
    safety_boundary_ref: str | None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FreezePreparationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ArtifactChainIntegrityResult:
    integrity_id: str
    created_at_utc: str
    references: list[ArtifactChainReference]
    status: ArtifactChainStatus
    total_required: int
    total_available: int
    missing_required: int
    hash_mismatch_count: int
    schema_break_count: int
    lineage_break_count: int
    safety_break_count: int
    chain_complete: bool
    chain_valid: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FreezePreparationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class IntegrationRehearsalStep:
    step_id: str
    created_at_utc: str
    step_kind: IntegrationRehearsalStepKind
    status: IntegrationRehearsalStepStatus
    required: bool
    passed: bool
    observed_value: Any | None
    expected_value: Any | None
    message: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FreezePreparationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class IntegrationRehearsalResult:
    rehearsal_id: str
    created_at_utc: str
    steps: list[IntegrationRehearsalStep]
    total_steps: int
    passed_steps: int
    warning_steps: int
    failed_steps: int
    blocked_steps: int
    rehearsal_passed: bool
    quality: FreezePreparationQuality
    artifact_chain_status: ArtifactChainStatus
    report_qa_status: ReportQaAcceptanceStatus
    freeze_candidate_status: FreezeCandidateStatus
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FreezePreparationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ReportQaAcceptanceRule:
    rule_id: str
    created_at_utc: str
    name: str
    required: bool
    status: ReportQaAcceptanceStatus
    passed: bool
    matched_terms: list[str]
    message: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FreezePreparationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ReportQaAcceptanceGate:
    gate_id: str
    created_at_utc: str
    status: ReportQaAcceptanceStatus
    rules: list[ReportQaAcceptanceRule]
    qa_results_ref: str | None
    research_report_ref: str | None
    accepted: bool
    unsafe_language_count: int
    investment_advice_detected: bool
    trade_signal_language_detected: bool
    order_language_detected: bool
    portfolio_language_detected: bool
    guarantee_language_detected: bool
    broker_execution_language_detected: bool
    secret_language_detected: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FreezePreparationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FreezeCandidateArtifact:
    artifact_id: str
    created_at_utc: str
    phase: ArtifactChainPhase
    artifact_name: str
    artifact_kind: str
    path: str | None
    artifact_hash: str | None
    required: bool
    included: bool
    immutable: bool
    research_data_only: bool
    contains_secret: bool
    contains_forbidden_columns: bool
    contains_execution_language: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FreezePreparationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FreezeCandidateManifest:
    manifest_id: str
    created_at_utc: str
    status: FreezeCandidateStatus
    artifacts: list[FreezeCandidateArtifact]
    total_artifacts: int
    included_artifacts: int
    missing_required_artifacts: int
    manifest_hash: str | None
    immutable: bool
    research_data_only: bool
    no_secret_leak: bool
    no_forbidden_columns: bool
    no_execution_language: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    ready_for_final_closure: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FreezePreparationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FreezeReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: FreezeReadinessRuleKind
    name: str
    status: FreezeReadinessStatus
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FreezePreparationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FreezePreparationGate:
    gate_id: str
    created_at_utc: str
    status: FreezeReadinessStatus
    rules: list[FreezeReadinessRule]
    artifact_chain: ArtifactChainIntegrityResult
    report_qa_gate: ReportQaAcceptanceGate
    freeze_manifest: FreezeCandidateManifest
    ready_for_phase125: bool
    ready_for_phase126_kickoff_after_phase125: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FreezePreparationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FreezePreparationContext:
    context_id: str
    created_at_utc: str
    status: FeatureFactorIntegrationStatus
    decision: FeatureFactorIntegrationDecision
    source_explainability_review_id: str | None
    ingestion: ExplainabilityIngestionResult
    artifact_chain: ArtifactChainIntegrityResult
    rehearsal_result: IntegrationRehearsalResult
    report_qa_gate: ReportQaAcceptanceGate
    freeze_manifest: FreezeCandidateManifest
    freeze_gate: FreezePreparationGate
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
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FreezePreparationRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FreezePreparationFullReview:
    review_id: str
    created_at_utc: str
    report_type: FreezePreparationReportType
    ingestion: ExplainabilityIngestionResult
    context: FreezePreparationContext
    artifact_chain: ArtifactChainIntegrityResult
    rehearsal_result: IntegrationRehearsalResult
    report_qa_gate: ReportQaAcceptanceGate
    freeze_manifest: FreezeCandidateManifest
    freeze_gate: FreezePreparationGate
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def create_explainability_ingestion_id() -> str:
    return f"ingest_{uuid.uuid4().hex[:8]}"

def create_artifact_chain_reference_id() -> str:
    return f"artref_{uuid.uuid4().hex[:8]}"

def create_artifact_chain_integrity_id() -> str:
    return f"integ_{uuid.uuid4().hex[:8]}"

def create_integration_rehearsal_step_id() -> str:
    return f"step_{uuid.uuid4().hex[:8]}"

def create_integration_rehearsal_result_id() -> str:
    return f"reh_{uuid.uuid4().hex[:8]}"

def create_report_qa_acceptance_rule_id() -> str:
    return f"qarule_{uuid.uuid4().hex[:8]}"

def create_report_qa_acceptance_gate_id() -> str:
    return f"qagate_{uuid.uuid4().hex[:8]}"

def create_freeze_candidate_artifact_id() -> str:
    return f"fcart_{uuid.uuid4().hex[:8]}"

def create_freeze_candidate_manifest_id() -> str:
    return f"fcman_{uuid.uuid4().hex[:8]}"

def create_freeze_readiness_rule_id() -> str:
    return f"frrule_{uuid.uuid4().hex[:8]}"

def create_freeze_preparation_gate_id() -> str:
    return f"frgate_{uuid.uuid4().hex[:8]}"

def create_freeze_preparation_context_id() -> str:
    return f"fctx_{uuid.uuid4().hex[:8]}"

def create_freeze_preparation_full_review_id() -> str:
    return f"frev_{uuid.uuid4().hex[:8]}"

# Conversion functions
def _dataclass_to_dict(obj: Any) -> dict:
    from dataclasses import asdict
    if obj is None:
        return {}

    d = asdict(obj)
    # Convert enums to strings
    for k, v in d.items():
        if hasattr(v, "value"):
            d[k] = v.value
        elif isinstance(v, list) and v and hasattr(v[0], "value"):
            d[k] = [item.value for item in v]
        elif isinstance(v, dict):
             d[k] = _clean_dict_enums(v)
    return d

def _clean_dict_enums(d: dict) -> dict:
     res = {}
     for k, v in d.items():
         if hasattr(v, "value"):
             res[k] = v.value
         elif isinstance(v, list) and v and hasattr(v[0], "value"):
             res[k] = [item.value for item in v]
         elif isinstance(v, dict):
             res[k] = _clean_dict_enums(v)
         else:
             res[k] = v
     return res

def explainability_ingestion_result_to_dict(item: ExplainabilityIngestionResult) -> dict:
    return _dataclass_to_dict(item)

def artifact_chain_reference_to_dict(item: ArtifactChainReference) -> dict:
    return _dataclass_to_dict(item)

def artifact_chain_integrity_result_to_dict(item: ArtifactChainIntegrityResult) -> dict:
    return _dataclass_to_dict(item)

def integration_rehearsal_step_to_dict(item: IntegrationRehearsalStep) -> dict:
    return _dataclass_to_dict(item)

def integration_rehearsal_result_to_dict(item: IntegrationRehearsalResult) -> dict:
    return _dataclass_to_dict(item)

def report_qa_acceptance_rule_to_dict(item: ReportQaAcceptanceRule) -> dict:
    return _dataclass_to_dict(item)

def report_qa_acceptance_gate_to_dict(item: ReportQaAcceptanceGate) -> dict:
    return _dataclass_to_dict(item)

def freeze_candidate_artifact_to_dict(item: FreezeCandidateArtifact) -> dict:
    return _dataclass_to_dict(item)

def freeze_candidate_manifest_to_dict(item: FreezeCandidateManifest) -> dict:
    return _dataclass_to_dict(item)

def freeze_readiness_rule_to_dict(item: FreezeReadinessRule) -> dict:
    return _dataclass_to_dict(item)

def freeze_preparation_gate_to_dict(item: FreezePreparationGate) -> dict:
    return _dataclass_to_dict(item)

def freeze_preparation_context_to_dict(item: FreezePreparationContext) -> dict:
    return _dataclass_to_dict(item)

def freeze_preparation_full_review_to_dict(item: FreezePreparationFullReview) -> dict:
    return _dataclass_to_dict(item)

# Validators
def validate_explainability_ingestion_result(item: ExplainabilityIngestionResult) -> None:
    if not item.attribution_ready: raise ValueError("attribution_ready must be True")
    if not item.contribution_ready: raise ValueError("contribution_ready must be True")
    if not item.interpretation_ready: raise ValueError("interpretation_ready must be True")
    if not item.research_report_ready: raise ValueError("research_report_ready must be True")
    if not item.report_qa_passed: raise ValueError("report_qa_passed must be True")
    if not item.ready_for_phase124: raise ValueError("ready_for_phase124 must be True")
    if not item.research_data_only: raise ValueError("research_data_only must be True")

    if item.activation_allowed: raise ValueError("activation_allowed must be False")
    if item.strategy_activation_allowed: raise ValueError("strategy_activation_allowed must be False")
    if item.active_paper_enabled: raise ValueError("active_paper_enabled must be False")
    if item.broker_execution_enabled: raise ValueError("broker_execution_enabled must be False")
    if item.order_creation_enabled: raise ValueError("order_creation_enabled must be False")
    if item.paper_state_mutation_enabled: raise ValueError("paper_state_mutation_enabled must be False")
    if item.telegram_real_send_enabled: raise ValueError("telegram_real_send_enabled must be False")
    if item.scraping_enabled: raise ValueError("scraping_enabled must be False")
    if item.html_parse_enabled: raise ValueError("html_parse_enabled must be False")
    if item.paid_api_enabled: raise ValueError("paid_api_enabled must be False")
    if item.dashboard_enabled: raise ValueError("dashboard_enabled must be False")
    if item.network_default_enabled: raise ValueError("network_default_enabled must be False")
    if item.produces_trade_signal: raise ValueError("produces_trade_signal must be False")
    if item.produces_order_decision: raise ValueError("produces_order_decision must be False")
    if item.produces_portfolio_weights: raise ValueError("produces_portfolio_weights must be False")
    if item.investment_advice: raise ValueError("investment_advice must be False")
    if item.network_used: raise ValueError("network_used must be False")
    if item.paid_api_used: raise ValueError("paid_api_used must be False")
    if item.scraping_used: raise ValueError("scraping_used must be False")
    if item.html_parsing_used: raise ValueError("html_parsing_used must be False")
    if item.broker_used: raise ValueError("broker_used must be False")
    if item.order_created: raise ValueError("order_created must be False")
    if item.paper_state_mutated: raise ValueError("paper_state_mutated must be False")
    if item.telegram_real_sent: raise ValueError("telegram_real_sent must be False")
    if item.dashboard_started: raise ValueError("dashboard_started must be False")

def validate_artifact_chain_integrity_result(item: ArtifactChainIntegrityResult) -> None:
    pass

def validate_integration_rehearsal_result(item: IntegrationRehearsalResult) -> None:
    pass

def validate_report_qa_acceptance_gate(item: ReportQaAcceptanceGate) -> None:
    pass

def validate_freeze_candidate_manifest(item: FreezeCandidateManifest) -> None:
    if item.activation_allowed: raise ValueError("activation_allowed must be False")

def validate_freeze_preparation_gate(item: FreezePreparationGate) -> None:
    if item.ready_for_phase125:
        if not item.report_qa_gate.accepted:
            raise ValueError("ready_for_phase125 can only be true if QA is accepted")
        if not item.freeze_manifest.status == FreezeCandidateStatus.VALIDATED:
            raise ValueError("ready_for_phase125 can only be true if manifest is validated")
        if not item.artifact_chain.chain_valid:
             raise ValueError("ready_for_phase125 can only be true if artifact chain is valid")

    if item.activation_allowed or item.strategy_activation_allowed or item.broker_execution_enabled or item.order_creation_enabled or item.paper_state_mutation_enabled or item.produces_trade_signal or item.produces_order_decision or item.produces_portfolio_weights:
        raise ValueError("Active trading flags must be false")

def validate_freeze_preparation_context(item: FreezePreparationContext) -> None:
    pass

def validate_freeze_preparation_full_review(item: FreezePreparationFullReview) -> None:
    pass
