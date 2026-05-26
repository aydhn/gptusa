from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    ProviderFreezeStatus,
    ProviderFreezeDecision,
    ProviderFreezeItemStatus,
    MultiProviderReviewStatus,
    MultiProviderReviewKind,
    DataLayerRehearsalStatus,
    DataLayerRehearsalScenarioKind,
    DataLayerOutputContractStatus,
    ProviderFreezeRiskFlag,
    ProviderFreezeReportType
)

def create_provider_governance_ingestion_id() -> str:
    return f"pgi_{uuid.uuid4().hex}"

def create_provider_freeze_evidence_id() -> str:
    return f"pfe_{uuid.uuid4().hex}"

def create_provider_expansion_freeze_id() -> str:
    return f"pef_{uuid.uuid4().hex}"

def create_multi_provider_review_item_id() -> str:
    return f"mri_{uuid.uuid4().hex}"

def create_multi_provider_review_report_id() -> str:
    return f"mrr_{uuid.uuid4().hex}"

def create_rehearsal_scenario_id() -> str:
    return f"rsc_{uuid.uuid4().hex}"

def create_rehearsal_step_id() -> str:
    return f"rst_{uuid.uuid4().hex}"

def create_rehearsal_report_id() -> str:
    return f"rrp_{uuid.uuid4().hex}"

def create_output_contract_id() -> str:
    return f"oct_{uuid.uuid4().hex}"

def create_freeze_artifact_manifest_id() -> str:
    return f"fam_{uuid.uuid4().hex}"

def create_provider_freeze_context_id() -> str:
    return f"pfc_{uuid.uuid4().hex}"

def create_provider_freeze_full_review_id() -> str:
    return f"pfr_{uuid.uuid4().hex}"

def _utcnow_str() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class ProviderGovernanceIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str] = None
    source_review_id: Optional[str] = None
    source_context_id: Optional[str] = None
    available: bool = False
    provider_governance_ready: bool = False
    provider_expansion_accepted: bool = False
    lineage_ready: bool = False
    audit_ready: bool = False
    metadata_only: bool = True
    research_data_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    valid_for_phase114: bool = False
    risk_flags: List[ProviderFreezeRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderFreezeEvidenceItem:
    evidence_id: str
    created_at_utc: str
    source_phase: int
    evidence_name: str
    source_ref_id: Optional[str] = None
    source_path: Optional[str] = None
    status: ProviderFreezeItemStatus = ProviderFreezeItemStatus.UNKNOWN
    required: bool = True
    available: bool = False
    valid: bool = False
    frozen: bool = False
    immutable: bool = False
    metadata_only: bool = True
    artifact_hash: Optional[str] = None
    stale: bool = False
    contains_secret: bool = False
    contains_execution: bool = False
    contains_trade_signal: bool = False
    contains_order_decision: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ProviderFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderExpansionFreezeBundle:
    freeze_id: str
    created_at_utc: str
    status: ProviderFreezeStatus = ProviderFreezeStatus.UNKNOWN
    decision: ProviderFreezeDecision = ProviderFreezeDecision.UNKNOWN
    phase_start: int = 106
    phase_end: int = 114
    next_phase: int = 115
    final_phase: int = 160
    evidence_items: List[ProviderFreezeEvidenceItem] = field(default_factory=list)
    freeze_hash: Optional[str] = None
    frozen: bool = False
    immutable: bool = False
    metadata_only: bool = True
    research_data_only: bool = True
    total_items: int = 0
    frozen_items: int = 0
    missing_items: int = 0
    stale_items: int = 0
    invalid_items: int = 0
    secret_violation_count: int = 0
    execution_violation_count: int = 0
    trade_signal_violation_count: int = 0
    order_decision_violation_count: int = 0
    freeze_valid: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ProviderFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MultiProviderReviewItem:
    review_item_id: str
    created_at_utc: str
    review_kind: MultiProviderReviewKind = MultiProviderReviewKind.UNKNOWN
    name: str = ""
    status: MultiProviderReviewStatus = MultiProviderReviewStatus.UNKNOWN
    required: bool = True
    passed: bool = False
    score: Optional[float] = None
    rationale: str = ""
    related_evidence_ids: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ProviderFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MultiProviderFinalReviewReport:
    report_id: str
    created_at_utc: str
    status: MultiProviderReviewStatus = MultiProviderReviewStatus.UNKNOWN
    items: List[MultiProviderReviewItem] = field(default_factory=list)
    total_items: int = 0
    passed_items: int = 0
    warning_items: int = 0
    failed_items: int = 0
    blocked_items: int = 0
    multi_provider_review_passed: bool = False
    provider_consistency_passed: bool = False
    provider_coverage_passed: bool = False
    provider_safety_passed: bool = False
    no_execution_boundary_passed: bool = False
    no_scraping_boundary_passed: bool = False
    no_paid_api_boundary_passed: bool = False
    no_broker_order_boundary_passed: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ProviderFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DataLayerRehearsalScenario:
    scenario_id: str
    created_at_utc: str
    scenario_kind: DataLayerRehearsalScenarioKind = DataLayerRehearsalScenarioKind.UNKNOWN
    name: str = ""
    description: str = ""
    required: bool = True
    metadata_only: bool = True
    dry_run_only: bool = True
    research_data_only: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    expected_outputs: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ProviderFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DataLayerRehearsalStep:
    step_id: str
    created_at_utc: str
    scenario_id: Optional[str] = None
    step_name: str = ""
    status: DataLayerRehearsalStatus = DataLayerRehearsalStatus.UNKNOWN
    passed: bool = False
    output_contract_status: DataLayerOutputContractStatus = DataLayerOutputContractStatus.UNKNOWN
    message: str = ""
    outputs: Dict[str, Any] = field(default_factory=dict)
    metadata_only: bool = True
    dry_run_only: bool = True
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ProviderFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DataLayerRehearsalReport:
    rehearsal_id: str
    created_at_utc: str
    status: DataLayerRehearsalStatus = DataLayerRehearsalStatus.UNKNOWN
    scenarios: List[DataLayerRehearsalScenario] = field(default_factory=list)
    steps: List[DataLayerRehearsalStep] = field(default_factory=list)
    total_scenarios: int = 0
    passed_scenarios: int = 0
    warning_scenarios: int = 0
    failed_scenarios: int = 0
    blocked_scenarios: int = 0
    rehearsal_passed: bool = False
    output_contracts_passed: bool = False
    metadata_only: bool = True
    dry_run_only: bool = True
    research_data_only: bool = True
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ProviderFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DataLayerOutputContract:
    contract_id: str
    created_at_utc: str
    status: DataLayerOutputContractStatus = DataLayerOutputContractStatus.UNKNOWN
    allowed_output_kinds: List[str] = field(default_factory=list)
    blocked_output_kinds: List[str] = field(default_factory=list)
    metadata_only_required: bool = True
    research_data_only_required: bool = True
    trade_signal_blocked: bool = True
    order_decision_blocked: bool = True
    execution_blocked: bool = True
    broker_blocked: bool = True
    paper_mutation_blocked: bool = True
    telegram_real_send_blocked: bool = True
    scraping_blocked: bool = True
    html_parsing_blocked: bool = True
    paid_api_blocked: bool = True
    network_default_enabled_blocked: bool = True
    contract_valid: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ProviderFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderFreezeArtifactManifest:
    manifest_id: str
    created_at_utc: str
    freeze_id: Optional[str] = None
    artifacts: List[Dict[str, Any]] = field(default_factory=list)
    total_artifacts: int = 0
    hashed_artifacts: int = 0
    missing_artifacts: int = 0
    invalid_artifacts: int = 0
    secret_violation_count: int = 0
    execution_violation_count: int = 0
    trade_signal_violation_count: int = 0
    order_decision_violation_count: int = 0
    manifest_valid: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ProviderFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderFreezeContext:
    context_id: str
    created_at_utc: str
    status: ProviderFreezeStatus = ProviderFreezeStatus.UNKNOWN
    decision: ProviderFreezeDecision = ProviderFreezeDecision.UNKNOWN
    source_provider_governance_review_id: Optional[str] = None
    ingestion: ProviderGovernanceIngestionResult = field(default_factory=lambda: ProviderGovernanceIngestionResult(ingestion_id="", created_at_utc=""))
    freeze_bundle: ProviderExpansionFreezeBundle = field(default_factory=lambda: ProviderExpansionFreezeBundle(freeze_id="", created_at_utc=""))
    multi_provider_review: MultiProviderFinalReviewReport = field(default_factory=lambda: MultiProviderFinalReviewReport(report_id="", created_at_utc=""))
    rehearsal_report: DataLayerRehearsalReport = field(default_factory=lambda: DataLayerRehearsalReport(rehearsal_id="", created_at_utc=""))
    output_contract: DataLayerOutputContract = field(default_factory=lambda: DataLayerOutputContract(contract_id="", created_at_utc=""))
    artifact_manifest: ProviderFreezeArtifactManifest = field(default_factory=lambda: ProviderFreezeArtifactManifest(manifest_id="", created_at_utc=""))
    provider_expansion_frozen: bool = False
    multi_provider_review_passed: bool = False
    data_layer_rehearsal_passed: bool = False
    output_contracts_passed: bool = False
    metadata_only: bool = True
    research_data_only: bool = True
    activation_allowed: bool = False
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
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    ready_for_phase115: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[ProviderFreezeRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderFreezeFullReview:
    review_id: str
    created_at_utc: str
    report_type: ProviderFreezeReportType = ProviderFreezeReportType.UNKNOWN
    ingestion: ProviderGovernanceIngestionResult = field(default_factory=lambda: ProviderGovernanceIngestionResult(ingestion_id="", created_at_utc=""))
    context: ProviderFreezeContext = field(default_factory=lambda: ProviderFreezeContext(context_id="", created_at_utc=""))
    freeze_bundle: ProviderExpansionFreezeBundle = field(default_factory=lambda: ProviderExpansionFreezeBundle(freeze_id="", created_at_utc=""))
    multi_provider_review: MultiProviderFinalReviewReport = field(default_factory=lambda: MultiProviderFinalReviewReport(report_id="", created_at_utc=""))
    rehearsal_report: DataLayerRehearsalReport = field(default_factory=lambda: DataLayerRehearsalReport(rehearsal_id="", created_at_utc=""))
    output_contract: DataLayerOutputContract = field(default_factory=lambda: DataLayerOutputContract(contract_id="", created_at_utc=""))
    artifact_manifest: ProviderFreezeArtifactManifest = field(default_factory=lambda: ProviderFreezeArtifactManifest(manifest_id="", created_at_utc=""))
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def provider_governance_ingestion_result_to_dict(item: ProviderGovernanceIngestionResult) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    if d.get("risk_flags"):
        d["risk_flags"] = [f.value for f in d["risk_flags"]]
    return d

def provider_freeze_evidence_item_to_dict(item: ProviderFreezeEvidenceItem) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["status"] = d["status"].value
    if d.get("risk_flags"):
        d["risk_flags"] = [f.value for f in d["risk_flags"]]
    return d

def provider_expansion_freeze_bundle_to_dict(item: ProviderExpansionFreezeBundle) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["status"] = d["status"].value
    d["decision"] = d["decision"].value
    d["evidence_items"] = [provider_freeze_evidence_item_to_dict(e) for e in item.evidence_items]
    if d.get("risk_flags"):
        d["risk_flags"] = [f.value for f in d["risk_flags"]]
    return d

def multi_provider_review_item_to_dict(item: MultiProviderReviewItem) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["review_kind"] = d["review_kind"].value
    d["status"] = d["status"].value
    if d.get("risk_flags"):
        d["risk_flags"] = [f.value for f in d["risk_flags"]]
    return d

def multi_provider_final_review_report_to_dict(item: MultiProviderFinalReviewReport) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["status"] = d["status"].value
    d["items"] = [multi_provider_review_item_to_dict(i) for i in item.items]
    if d.get("risk_flags"):
        d["risk_flags"] = [f.value for f in d["risk_flags"]]
    return d

def data_layer_rehearsal_scenario_to_dict(item: DataLayerRehearsalScenario) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["scenario_kind"] = d["scenario_kind"].value
    if d.get("risk_flags"):
        d["risk_flags"] = [f.value for f in d["risk_flags"]]
    return d

def data_layer_rehearsal_step_to_dict(item: DataLayerRehearsalStep) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["status"] = d["status"].value
    d["output_contract_status"] = d["output_contract_status"].value
    if d.get("risk_flags"):
        d["risk_flags"] = [f.value for f in d["risk_flags"]]
    return d

def data_layer_rehearsal_report_to_dict(item: DataLayerRehearsalReport) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["status"] = d["status"].value
    d["scenarios"] = [data_layer_rehearsal_scenario_to_dict(s) for s in item.scenarios]
    d["steps"] = [data_layer_rehearsal_step_to_dict(s) for s in item.steps]
    if d.get("risk_flags"):
        d["risk_flags"] = [f.value for f in d["risk_flags"]]
    return d

def data_layer_output_contract_to_dict(item: DataLayerOutputContract) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["status"] = d["status"].value
    if d.get("risk_flags"):
        d["risk_flags"] = [f.value for f in d["risk_flags"]]
    return d

def provider_freeze_artifact_manifest_to_dict(item: ProviderFreezeArtifactManifest) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    if d.get("risk_flags"):
        d["risk_flags"] = [f.value for f in d["risk_flags"]]
    return d

def provider_freeze_context_to_dict(item: ProviderFreezeContext) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["status"] = d["status"].value
    d["decision"] = d["decision"].value
    d["ingestion"] = provider_governance_ingestion_result_to_dict(item.ingestion)
    d["freeze_bundle"] = provider_expansion_freeze_bundle_to_dict(item.freeze_bundle)
    d["multi_provider_review"] = multi_provider_final_review_report_to_dict(item.multi_provider_review)
    d["rehearsal_report"] = data_layer_rehearsal_report_to_dict(item.rehearsal_report)
    d["output_contract"] = data_layer_output_contract_to_dict(item.output_contract)
    d["artifact_manifest"] = provider_freeze_artifact_manifest_to_dict(item.artifact_manifest)
    if d.get("risk_flags"):
        d["risk_flags"] = [f.value for f in d["risk_flags"]]
    return d

def provider_freeze_full_review_to_dict(item: ProviderFreezeFullReview) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["report_type"] = d["report_type"].value
    d["ingestion"] = provider_governance_ingestion_result_to_dict(item.ingestion)
    d["context"] = provider_freeze_context_to_dict(item.context)
    d["freeze_bundle"] = provider_expansion_freeze_bundle_to_dict(item.freeze_bundle)
    d["multi_provider_review"] = multi_provider_final_review_report_to_dict(item.multi_provider_review)
    d["rehearsal_report"] = data_layer_rehearsal_report_to_dict(item.rehearsal_report)
    d["output_contract"] = data_layer_output_contract_to_dict(item.output_contract)
    d["artifact_manifest"] = provider_freeze_artifact_manifest_to_dict(item.artifact_manifest)
    return d

def validate_provider_governance_ingestion_result(item: ProviderGovernanceIngestionResult) -> None:
    from usa_signal_bot.core.exceptions import ProviderGovernanceIngestionError
    if not item.provider_governance_ready:
        raise ProviderGovernanceIngestionError("provider_governance_ready must be True")
    if not item.provider_expansion_accepted:
        raise ProviderGovernanceIngestionError("provider_expansion_accepted must be True")
    if not item.lineage_ready:
        raise ProviderGovernanceIngestionError("lineage_ready must be True")
    if not item.audit_ready:
        raise ProviderGovernanceIngestionError("audit_ready must be True")
    if not item.metadata_only:
        raise ProviderGovernanceIngestionError("metadata_only must be True")
    if not item.research_data_only:
        raise ProviderGovernanceIngestionError("research_data_only must be True")
    if item.produces_trade_signal:
        raise ProviderGovernanceIngestionError("produces_trade_signal must be False")
    if item.produces_order_decision:
        raise ProviderGovernanceIngestionError("produces_order_decision must be False")
    if item.network_used or item.paid_api_used or item.scraping_used or item.html_parsing_used or item.broker_used or item.order_created or item.paper_state_mutated or item.telegram_real_sent or item.dashboard_started:
        raise ProviderGovernanceIngestionError("Execution properties must be False")

def validate_provider_expansion_freeze_bundle(item: ProviderExpansionFreezeBundle) -> None:
    from usa_signal_bot.core.exceptions import ProviderFreezeBundleError
    if item.phase_start != 106 or item.phase_end != 114 or item.next_phase != 115 or item.final_phase != 160:
        raise ProviderFreezeBundleError("Invalid phase bounds")
    if not item.frozen or not item.immutable:
        raise ProviderFreezeBundleError("Must be frozen and immutable")

def validate_multi_provider_final_review_report(item: MultiProviderFinalReviewReport) -> None:
    from usa_signal_bot.core.exceptions import MultiProviderFinalReviewError
    pass # further logic handled in final_review_safety_validator.py

def validate_data_layer_rehearsal_report(item: DataLayerRehearsalReport) -> None:
    pass

def validate_data_layer_output_contract(item: DataLayerOutputContract) -> None:
    pass

def validate_provider_freeze_artifact_manifest(item: ProviderFreezeArtifactManifest) -> None:
    pass

def validate_provider_freeze_context(item: ProviderFreezeContext) -> None:
    from usa_signal_bot.core.exceptions import ProviderFreezeValidationError
    if item.activation_allowed or item.active_paper_enabled or item.broker_execution_enabled or item.order_creation_enabled or item.paper_state_mutation_enabled or item.telegram_real_send_enabled or item.scraping_enabled or item.html_parse_enabled or item.paid_api_enabled or item.dashboard_enabled or item.network_default_enabled:
        raise ProviderFreezeValidationError("Execution must be strictly disabled")

def validate_provider_freeze_full_review(item: ProviderFreezeFullReview) -> None:
    pass
