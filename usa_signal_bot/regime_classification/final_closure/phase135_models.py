from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    RegimeFinalClosureStatus,
    RegimeFinalClosureDecision,
    RegimeArtifactChainKind,
    RegimeArtifactChainValidationStatus,
    RegimeFinalClosureRuleKind,
    RegimeFreezeSealStatus,
    RegimeFreezeSealKind,
    MLKickoffReadinessStatus,
    MLKickoffReadinessRuleKind,
    MLInputContractArtifactKind,
    RegimeFinalClosureQuality,
    RegimeFinalClosureRiskFlag,
    RegimeFinalClosureReportType,
)

@dataclass
class RegimeResearchFreezeIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str] = None
    source_review_id: Optional[str] = None
    source_context_id: Optional[str] = None
    available: bool = False
    monitoring_ingested: bool = False
    monitoring_artifacts_loaded: bool = False
    monitoring_validated: bool = False
    drift_report_built: bool = False
    drift_report_qa_passed: bool = False
    freeze_package_built: bool = False
    freeze_package_validated: bool = False
    readiness_gate_built: bool = False
    readiness_gate_passed: bool = False
    ready_for_phase135: bool = False
    metadata_only: bool = True
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    paid_api_enabled: bool = False
    dashboard_enabled: bool = False
    network_default_enabled: bool = False
    daemon_started: bool = False
    scheduler_enabled: bool = False
    model_training_used: bool = False
    model_prediction_used: bool = False
    heavy_ml_dependency_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    valid_for_phase135: bool = False
    risk_flags: List[RegimeFinalClosureRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeArtifactChainReference:
    reference_id: str
    created_at_utc: str
    chain_kind: RegimeArtifactChainKind
    phase_number: int
    artifact_name: str
    source_review_id: Optional[str] = None
    source_path: Optional[str] = None
    artifact_hash: Optional[str] = None
    required: bool = True
    available: bool = False
    immutable: bool = True
    read_only: bool = True
    research_metadata_only: bool = True
    activation_allowed: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[RegimeFinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeArtifactChainValidationRule:
    rule_id: str
    created_at_utc: str
    chain_kind: RegimeArtifactChainKind
    name: str
    status: RegimeArtifactChainValidationStatus
    required: bool
    passed: bool
    expected_value: Any = None
    observed_value: Any = None
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[RegimeFinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeArtifactChainValidationResult:
    validation_id: str
    created_at_utc: str
    references: List[RegimeArtifactChainReference]
    rules: List[RegimeArtifactChainValidationRule]
    required_reference_count: int = 0
    available_required_reference_count: int = 0
    missing_required_reference_count: int = 0
    invalid_hash_count: int = 0
    chain_complete: bool = False
    chain_valid: bool = False
    quality: RegimeFinalClosureQuality = RegimeFinalClosureQuality.UNKNOWN
    research_metadata_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    model_training_used: bool = False
    model_prediction_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[RegimeFinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeFinalClosureRule:
    rule_id: str
    created_at_utc: str
    rule_kind: RegimeFinalClosureRuleKind
    name: str
    status: RegimeArtifactChainValidationStatus
    required: bool
    passed: bool
    expected_value: Any = None
    observed_value: Any = None
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[RegimeFinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeFinalClosureResult:
    closure_result_id: str
    created_at_utc: str
    rules: List[RegimeFinalClosureRule]
    artifact_chain_validation: RegimeArtifactChainValidationResult
    total_rules: int = 0
    passed_rules: int = 0
    warning_rules: int = 0
    failed_rules: int = 0
    blocked_rules: int = 0
    closure_passed: bool = False
    ready_for_freeze_seal: bool = False
    ready_for_phase136_kickoff_gate: bool = False
    quality: RegimeFinalClosureQuality = RegimeFinalClosureQuality.UNKNOWN
    research_metadata_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    model_training_used: bool = False
    model_prediction_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[RegimeFinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeFreezeSeal:
    seal_id: str
    created_at_utc: str
    seal_kind: RegimeFreezeSealKind
    seal_status: RegimeFreezeSealStatus
    source_closure_result_id: Optional[str] = None
    source_freeze_review_id: Optional[str] = None
    artifact_chain_hash: Optional[str] = None
    closure_hash: Optional[str] = None
    seal_hash: Optional[str] = None
    seal_version: str = "phase135.v1"
    sealed_phase_start: int = 126
    sealed_phase_end: int = 135
    next_phase: int = 136
    immutable: bool = True
    research_metadata_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    model_training_used: bool = False
    model_prediction_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[RegimeFinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeFinalSafetyAudit:
    audit_id: str
    created_at_utc: str
    source_closure_result_id: Optional[str] = None
    source_seal_id: Optional[str] = None
    safety_passed: bool = False
    no_signal_output: bool = True
    no_order_output: bool = True
    no_portfolio_output: bool = True
    no_execution_output: bool = True
    no_broker: bool = True
    no_paper_mutation: bool = True
    no_telegram_real_send: bool = True
    no_scraping: bool = True
    no_html_parse: bool = True
    no_paid_api: bool = True
    no_dashboard: bool = True
    no_network_default: bool = True
    no_daemon: bool = True
    no_scheduler: bool = True
    no_deployment: bool = True
    no_model_training: bool = True
    no_model_prediction: bool = True
    no_investment_advice: bool = True
    no_secret_leak: bool = True
    quality: RegimeFinalClosureQuality = RegimeFinalClosureQuality.UNKNOWN
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[RegimeFinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLInputContractArtifact:
    artifact_id: str
    created_at_utc: str
    artifact_kind: MLInputContractArtifactKind
    artifact_name: str
    source_phase: int
    source_path: Optional[str] = None
    source_hash: Optional[str] = None
    allowed_for_phase136: bool = True
    required_for_phase136: bool = False
    read_only: bool = True
    research_metadata_only: bool = True
    contains_labels: bool = False
    contains_features: bool = False
    contains_targets: bool = False
    contains_trade_signals: bool = False
    contains_order_decisions: bool = False
    contains_portfolio_weights: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[RegimeFinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLInputContract:
    contract_id: str
    created_at_utc: str
    contract_version: str
    artifact_inputs: List[MLInputContractArtifact]
    allowed_input_kinds: List[MLInputContractArtifactKind]
    forbidden_output_fields: List[str]
    required_non_activation_flags: Dict[str, bool]
    phase136_allowed_scope: List[str]
    phase136_forbidden_scope: List[str]
    training_allowed_in_phase135: bool = False
    prediction_allowed_in_phase135: bool = False
    broker_allowed: bool = False
    order_allowed: bool = False
    portfolio_weight_allowed: bool = False
    deployment_allowed: bool = False
    contract_valid: bool = False
    research_metadata_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[RegimeFinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLKickoffReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: MLKickoffReadinessRuleKind
    name: str
    status: MLKickoffReadinessStatus
    required: bool
    passed: bool
    expected_value: Any = None
    observed_value: Any = None
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[RegimeFinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLKickoffReadinessGate:
    gate_id: str
    created_at_utc: str
    status: MLKickoffReadinessStatus
    rules: List[MLKickoffReadinessRule]
    input_contract: MLInputContract
    freeze_seal: RegimeFreezeSeal
    final_safety_audit: RegimeFinalSafetyAudit
    ready_for_phase136: bool = False
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    training_started: bool = False
    prediction_started: bool = False
    model_training_used: bool = False
    model_prediction_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[RegimeFinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeFinalClosureContext:
    context_id: str
    created_at_utc: str
    status: RegimeFinalClosureStatus
    decision: RegimeFinalClosureDecision
    source_research_freeze_review_id: Optional[str] = None
    ingestion: RegimeResearchFreezeIngestionResult = field(default_factory=lambda: RegimeResearchFreezeIngestionResult(ingestion_id="dummy", created_at_utc="dummy"))
    artifact_chain_validation: RegimeArtifactChainValidationResult = field(default_factory=lambda: RegimeArtifactChainValidationResult(validation_id="dummy", created_at_utc="dummy", references=[], rules=[]))
    final_closure_result: RegimeFinalClosureResult = field(default_factory=lambda: RegimeFinalClosureResult(closure_result_id="dummy", created_at_utc="dummy", rules=[], artifact_chain_validation=RegimeArtifactChainValidationResult(validation_id="dummy", created_at_utc="dummy", references=[], rules=[])))
    freeze_seal: RegimeFreezeSeal = field(default_factory=lambda: RegimeFreezeSeal(seal_id="dummy", created_at_utc="dummy", seal_kind=RegimeFreezeSealKind.UNKNOWN, seal_status=RegimeFreezeSealStatus.UNKNOWN))
    final_safety_audit: RegimeFinalSafetyAudit = field(default_factory=lambda: RegimeFinalSafetyAudit(audit_id="dummy", created_at_utc="dummy"))
    ml_input_contract: MLInputContract = field(default_factory=lambda: MLInputContract(contract_id="dummy", created_at_utc="dummy", contract_version="dummy", artifact_inputs=[], allowed_input_kinds=[], forbidden_output_fields=[], required_non_activation_flags={}, phase136_allowed_scope=[], phase136_forbidden_scope=[]))
    ml_kickoff_gate: MLKickoffReadinessGate = field(default_factory=lambda: MLKickoffReadinessGate(gate_id="dummy", created_at_utc="dummy", status=MLKickoffReadinessStatus.UNKNOWN, rules=[], input_contract=MLInputContract(contract_id="dummy", created_at_utc="dummy", contract_version="dummy", artifact_inputs=[], allowed_input_kinds=[], forbidden_output_fields=[], required_non_activation_flags={}, phase136_allowed_scope=[], phase136_forbidden_scope=[]), freeze_seal=RegimeFreezeSeal(seal_id="dummy", created_at_utc="dummy", seal_kind=RegimeFreezeSealKind.UNKNOWN, seal_status=RegimeFreezeSealStatus.UNKNOWN), final_safety_audit=RegimeFinalSafetyAudit(audit_id="dummy", created_at_utc="dummy")))
    research_freeze_ingested: bool = False
    artifact_chain_loaded: bool = False
    artifact_chain_validated: bool = False
    final_closure_validated: bool = False
    freeze_seal_created: bool = False
    final_safety_audit_passed: bool = False
    ml_input_contract_built: bool = False
    ml_kickoff_gate_built: bool = False
    ml_kickoff_gate_passed: bool = False
    ready_for_phase136: bool = False
    metadata_only: bool = True
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    paid_api_enabled: bool = False
    dashboard_enabled: bool = False
    network_default_enabled: bool = False
    daemon_started: bool = False
    scheduler_enabled: bool = False
    model_training_used: bool = False
    model_prediction_used: bool = False
    heavy_ml_dependency_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[RegimeFinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeFinalClosureFullReview:
    review_id: str
    created_at_utc: str
    report_type: RegimeFinalClosureReportType
    ingestion: RegimeResearchFreezeIngestionResult
    context: RegimeFinalClosureContext
    artifact_chain_validation: RegimeArtifactChainValidationResult
    final_closure_result: RegimeFinalClosureResult
    freeze_seal: RegimeFreezeSeal
    final_safety_audit: RegimeFinalSafetyAudit
    ml_input_contract: MLInputContract
    ml_kickoff_gate: MLKickoffReadinessGate
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

# Creation functions
def create_regime_research_freeze_ingestion_id() -> str:
    return f"rrfi_{uuid.uuid4().hex}"

def create_regime_artifact_chain_reference_id() -> str:
    return f"racr_{uuid.uuid4().hex}"

def create_regime_artifact_chain_validation_rule_id() -> str:
    return f"racvr_{uuid.uuid4().hex}"

def create_regime_artifact_chain_validation_result_id() -> str:
    return f"racvr_res_{uuid.uuid4().hex}"

def create_regime_final_closure_rule_id() -> str:
    return f"rfcr_{uuid.uuid4().hex}"

def create_regime_final_closure_result_id() -> str:
    return f"rfc_res_{uuid.uuid4().hex}"

def create_regime_freeze_seal_id() -> str:
    return f"rfs_{uuid.uuid4().hex}"

def create_regime_final_safety_audit_id() -> str:
    return f"rfsa_{uuid.uuid4().hex}"

def create_ml_input_contract_artifact_id() -> str:
    return f"mlica_{uuid.uuid4().hex}"

def create_ml_input_contract_id() -> str:
    return f"mlic_{uuid.uuid4().hex}"

def create_ml_kickoff_readiness_rule_id() -> str:
    return f"mlkrr_{uuid.uuid4().hex}"

def create_ml_kickoff_readiness_gate_id() -> str:
    return f"mlkrg_{uuid.uuid4().hex}"

def create_regime_final_closure_context_id() -> str:
    return f"rfcc_{uuid.uuid4().hex}"

def create_regime_final_closure_full_review_id() -> str:
    return f"rfcfr_{uuid.uuid4().hex}"
