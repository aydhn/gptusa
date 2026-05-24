from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from usa_signal_bot.core.enums import (
    CoreRuntimeAcceptanceStatus,
    CoreRuntimeAcceptanceDecision,
    AdvancedFoundationFreezeStatus,
    AdvancedFoundationFreezeDecision,
    DataProviderExpansionKickoffGateStatus,
    DataProviderExpansionKickoffGateDecision,
    ProviderKickoffRuleStatus,
    ProviderKickoffAssertionStatus,
    CoreRuntimeAcceptanceRiskFlag,
    CoreRuntimeAcceptanceReportType
)
import uuid
import datetime
from usa_signal_bot.core.exceptions import (
    LifecycleReviewIngestionError,
    CoreRuntimeAcceptanceValidationError,
    FoundationFreezeValidationError,
    ProviderKickoffGateValidationError
)

def _now() -> str:
    return datetime.datetime.now(datetime.UTC).isoformat() + "Z"

@dataclass
class LifecycleReviewIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str] = None
    source_review_id: Optional[str] = None
    source_lifecycle_context_id: Optional[str] = None
    source_readiness_gate_id: Optional[str] = None
    available: bool = False
    lifecycle_ready: bool = False
    ready_for_phase105: bool = False
    readiness_gate_passed: bool = False
    startup_checks_passed: bool = False
    all_required_services_ready: bool = False
    activation_allowed: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    scraping_enabled: bool = False
    dashboard_enabled: bool = False
    execution_performed: bool = False
    network_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    scraping_used: bool = False
    dashboard_started: bool = False
    valid_for_phase105: bool = False
    risk_flags: List[CoreRuntimeAcceptanceRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConsolidationEvidenceItem:
    evidence_id: str
    created_at_utc: str
    evidence_type: str
    source_phase: int
    source_ref_id: Optional[str] = None
    source_path: Optional[str] = None
    required: bool = False
    available: bool = False
    fresh: bool = False
    stale: bool = False
    summary: Dict[str, Any] = field(default_factory=dict)
    risk_flags: List[CoreRuntimeAcceptanceRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CoreRuntimeAcceptanceItem:
    item_id: str
    created_at_utc: str
    acceptance_name: str
    status: CoreRuntimeAcceptanceStatus
    decision: CoreRuntimeAcceptanceDecision
    accepted: bool = False
    required: bool = False
    rationale: str = ""
    risk_flags: List[CoreRuntimeAcceptanceRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CoreRuntimeAcceptanceReport:
    report_id: str
    created_at_utc: str
    status: CoreRuntimeAcceptanceStatus
    decision: CoreRuntimeAcceptanceDecision
    source_lifecycle_review_id: Optional[str] = None
    items: List[CoreRuntimeAcceptanceItem] = field(default_factory=list)
    accepted_item_count: int = 0
    blocked_item_count: int = 0
    failed_item_count: int = 0
    core_runtime_accepted: bool = False
    metadata_only_acceptance: bool = True
    read_only_acceptance: bool = True
    activation_allowed: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    scraping_enabled: bool = False
    dashboard_enabled: bool = False
    risk_flags: List[CoreRuntimeAcceptanceRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AdvancedFoundationFreezeItem:
    freeze_item_id: str
    created_at_utc: str
    evidence_type: str
    source_phase: int
    source_ref_id: Optional[str] = None
    source_path: Optional[str] = None
    frozen: bool = False
    immutable: bool = False
    available: bool = False
    fresh: bool = False
    stale: bool = False
    item_hash: Optional[str] = None
    risk_flags: List[CoreRuntimeAcceptanceRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AdvancedFoundationFreezeBundle:
    freeze_id: str
    created_at_utc: str
    status: AdvancedFoundationFreezeStatus
    decision: AdvancedFoundationFreezeDecision
    items: List[AdvancedFoundationFreezeItem] = field(default_factory=list)
    evidence_refs: List[str] = field(default_factory=list)
    freeze_hash: Optional[str] = None
    frozen: bool = False
    immutable: bool = False
    freeze_is_metadata_only: bool = True
    phase_start: int = 101
    phase_end: int = 105
    next_phase: int = 106
    final_phase: int = 160
    missing_evidence_count: int = 0
    stale_evidence_count: int = 0
    risk_flags: List[CoreRuntimeAcceptanceRiskFlag] = field(default_factory=list)
    required_followups: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderKickoffRule:
    rule_id: str
    created_at_utc: str
    rule_name: str
    status: ProviderKickoffRuleStatus
    expected_value: Any = None
    observed_value: Any = None
    required: bool = False
    description: str = ""
    risk_flags: List[CoreRuntimeAcceptanceRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderKickoffAssertion:
    assertion_id: str
    created_at_utc: str
    assertion_name: str
    status: ProviderKickoffAssertionStatus
    expected_value: Any = None
    observed_value: Any = None
    description: str = ""
    risk_flags: List[CoreRuntimeAcceptanceRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DataProviderExpansionKickoffGate:
    gate_id: str
    created_at_utc: str
    status: DataProviderExpansionKickoffGateStatus
    decision: DataProviderExpansionKickoffGateDecision
    source_acceptance_report_id: Optional[str] = None
    source_foundation_freeze_id: Optional[str] = None
    acceptance_report: Optional[CoreRuntimeAcceptanceReport] = None
    foundation_freeze: Optional[AdvancedFoundationFreezeBundle] = None
    rules: List[ProviderKickoffRule] = field(default_factory=list)
    assertions: List[ProviderKickoffAssertion] = field(default_factory=list)
    gate_hash: Optional[str] = None
    sealed: bool = False
    immutable: bool = False
    frozen: bool = False
    metadata_only: bool = True
    provider_ready: bool = False
    ready_for_phase106: bool = False
    phase106_scope_allowed: bool = False
    activation_allowed: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    dashboard_enabled: bool = False
    paid_api_enabled: bool = False
    provider_network_fetch_required: bool = False
    execution_performed: bool = False
    network_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    scraping_used: bool = False
    dashboard_started: bool = False
    risk_flags: List[CoreRuntimeAcceptanceRiskFlag] = field(default_factory=list)
    required_followups: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CoreRuntimeAcceptanceFullReview:
    review_id: str
    created_at_utc: str
    report_type: CoreRuntimeAcceptanceReportType
    lifecycle_ingestion: LifecycleReviewIngestionResult
    evidence_items: List[ConsolidationEvidenceItem]
    acceptance_report: CoreRuntimeAcceptanceReport
    foundation_freeze: AdvancedFoundationFreezeBundle
    kickoff_gate: DataProviderExpansionKickoffGate
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def create_lifecycle_review_ingestion_id() -> str:
    return f"lri_{uuid.uuid4().hex[:8]}"

def create_consolidation_evidence_id() -> str:
    return f"ce_{uuid.uuid4().hex[:8]}"

def create_core_runtime_acceptance_item_id() -> str:
    return f"crai_{uuid.uuid4().hex[:8]}"

def create_core_runtime_acceptance_report_id() -> str:
    return f"crar_{uuid.uuid4().hex[:8]}"

def create_foundation_freeze_item_id() -> str:
    return f"ffi_{uuid.uuid4().hex[:8]}"

def create_foundation_freeze_id() -> str:
    return f"ff_{uuid.uuid4().hex[:8]}"

def create_provider_kickoff_rule_id() -> str:
    return f"pkr_{uuid.uuid4().hex[:8]}"

def create_provider_kickoff_assertion_id() -> str:
    return f"pka_{uuid.uuid4().hex[:8]}"

def create_data_provider_kickoff_gate_id() -> str:
    return f"dpg_{uuid.uuid4().hex[:8]}"

def create_core_runtime_acceptance_full_review_id() -> str:
    return f"craf_{uuid.uuid4().hex[:8]}"

def lifecycle_review_ingestion_result_to_dict(item: LifecycleReviewIngestionResult) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["risk_flags"] = [f.name for f in item.risk_flags]
    return d

def consolidation_evidence_item_to_dict(item: ConsolidationEvidenceItem) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["risk_flags"] = [f.name for f in item.risk_flags]
    return d

def core_runtime_acceptance_item_to_dict(item: CoreRuntimeAcceptanceItem) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["status"] = item.status.name
    d["decision"] = item.decision.name
    d["risk_flags"] = [f.name for f in item.risk_flags]
    return d

def core_runtime_acceptance_report_to_dict(item: CoreRuntimeAcceptanceReport) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["status"] = item.status.name
    d["decision"] = item.decision.name
    d["items"] = [core_runtime_acceptance_item_to_dict(i) for i in item.items]
    d["risk_flags"] = [f.name for f in item.risk_flags]
    return d

def advanced_foundation_freeze_item_to_dict(item: AdvancedFoundationFreezeItem) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["risk_flags"] = [f.name for f in item.risk_flags]
    return d

def advanced_foundation_freeze_bundle_to_dict(item: AdvancedFoundationFreezeBundle) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["status"] = item.status.name
    d["decision"] = item.decision.name
    d["items"] = [advanced_foundation_freeze_item_to_dict(i) for i in item.items]
    d["risk_flags"] = [f.name for f in item.risk_flags]
    return d

def provider_kickoff_rule_to_dict(item: ProviderKickoffRule) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["status"] = item.status.name
    d["risk_flags"] = [f.name for f in item.risk_flags]
    return d

def provider_kickoff_assertion_to_dict(item: ProviderKickoffAssertion) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["status"] = item.status.name
    d["risk_flags"] = [f.name for f in item.risk_flags]
    return d

def data_provider_expansion_kickoff_gate_to_dict(item: DataProviderExpansionKickoffGate) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["status"] = item.status.name
    d["decision"] = item.decision.name
    if item.acceptance_report:
        d["acceptance_report"] = core_runtime_acceptance_report_to_dict(item.acceptance_report)
    if item.foundation_freeze:
        d["foundation_freeze"] = advanced_foundation_freeze_bundle_to_dict(item.foundation_freeze)
    d["rules"] = [provider_kickoff_rule_to_dict(r) for r in item.rules]
    d["assertions"] = [provider_kickoff_assertion_to_dict(a) for a in item.assertions]
    d["risk_flags"] = [f.name for f in item.risk_flags]
    return d

def core_runtime_acceptance_full_review_to_dict(item: CoreRuntimeAcceptanceFullReview) -> dict:
    from dataclasses import asdict
    d = asdict(item)
    d["report_type"] = item.report_type.name
    d["lifecycle_ingestion"] = lifecycle_review_ingestion_result_to_dict(item.lifecycle_ingestion)
    d["evidence_items"] = [consolidation_evidence_item_to_dict(i) for i in item.evidence_items]
    d["acceptance_report"] = core_runtime_acceptance_report_to_dict(item.acceptance_report)
    d["foundation_freeze"] = advanced_foundation_freeze_bundle_to_dict(item.foundation_freeze)
    d["kickoff_gate"] = data_provider_expansion_kickoff_gate_to_dict(item.kickoff_gate)
    return d

def validate_lifecycle_review_ingestion_result(item: LifecycleReviewIngestionResult) -> None:
    if not item.lifecycle_ready:
        raise LifecycleReviewIngestionError("lifecycle_ready is false")
    if not item.ready_for_phase105:
        raise LifecycleReviewIngestionError("ready_for_phase105 is false")
    if not item.readiness_gate_passed:
        raise LifecycleReviewIngestionError("readiness_gate_passed is false")
    if not item.startup_checks_passed:
        raise LifecycleReviewIngestionError("startup_checks_passed is false")
    if not item.all_required_services_ready:
        raise LifecycleReviewIngestionError("all_required_services_ready is false")

    _validate_no_execution(item, LifecycleReviewIngestionError)

def validate_core_runtime_acceptance_report(item: CoreRuntimeAcceptanceReport) -> None:
    if not item.core_runtime_accepted:
        raise CoreRuntimeAcceptanceValidationError("core_runtime_accepted is false")

    _validate_no_execution(item, CoreRuntimeAcceptanceValidationError)

def validate_advanced_foundation_freeze_bundle(item: AdvancedFoundationFreezeBundle) -> None:
    if not item.frozen:
        raise FoundationFreezeValidationError("frozen is false")
    if not item.immutable:
        raise FoundationFreezeValidationError("immutable is false")
    if not item.freeze_is_metadata_only:
        raise FoundationFreezeValidationError("freeze_is_metadata_only is false")
    if item.phase_start != 101:
        raise FoundationFreezeValidationError("phase_start is not 101")
    if item.phase_end != 105:
        raise FoundationFreezeValidationError("phase_end is not 105")
    if item.next_phase != 106:
        raise FoundationFreezeValidationError("next_phase is not 106")
    if item.final_phase != 160:
        raise FoundationFreezeValidationError("final_phase is not 160")

def validate_data_provider_expansion_kickoff_gate(item: DataProviderExpansionKickoffGate) -> None:
    if not item.sealed:
        raise ProviderKickoffGateValidationError("sealed is false")
    if not item.immutable:
        raise ProviderKickoffGateValidationError("immutable is false")
    if not item.frozen:
        raise ProviderKickoffGateValidationError("frozen is false")
    if not item.metadata_only:
        raise ProviderKickoffGateValidationError("metadata_only is false")
    if not item.provider_ready:
        raise ProviderKickoffGateValidationError("provider_ready is false")
    if not item.ready_for_phase106:
        raise ProviderKickoffGateValidationError("ready_for_phase106 is false")

    if getattr(item, "paid_api_enabled", False):
        raise ProviderKickoffGateValidationError("paid_api_enabled is true")
    if getattr(item, "provider_network_fetch_required", False):
        raise ProviderKickoffGateValidationError("provider_network_fetch_required is true")
    if getattr(item, "html_parse_enabled", False):
        raise ProviderKickoffGateValidationError("html_parse_enabled is true")

    _validate_no_execution(item, ProviderKickoffGateValidationError)

def validate_core_runtime_acceptance_full_review(item: CoreRuntimeAcceptanceFullReview) -> None:
    validate_lifecycle_review_ingestion_result(item.lifecycle_ingestion)
    validate_core_runtime_acceptance_report(item.acceptance_report)
    validate_advanced_foundation_freeze_bundle(item.foundation_freeze)
    validate_data_provider_expansion_kickoff_gate(item.kickoff_gate)


def _validate_no_execution(item: Any, exception_cls) -> None:
    if getattr(item, 'activation_allowed', False):
        raise exception_cls("activation_allowed is true")
    if getattr(item, 'active_paper_enabled', False):
        raise exception_cls("active_paper_enabled is true")
    if getattr(item, 'broker_execution_enabled', False):
        raise exception_cls("broker_execution_enabled is true")
    if getattr(item, 'paper_state_mutation_enabled', False):
        raise exception_cls("paper_state_mutation_enabled is true")
    if getattr(item, 'telegram_real_send_enabled', False):
        raise exception_cls("telegram_real_send_enabled is true")
    if getattr(item, 'scraping_enabled', False):
        raise exception_cls("scraping_enabled is true")
    if getattr(item, 'dashboard_enabled', False):
        raise exception_cls("dashboard_enabled is true")
    if getattr(item, 'execution_performed', False):
        raise exception_cls("execution_performed is true")
    if getattr(item, 'network_used', False):
        raise exception_cls("network_used is true")
    if getattr(item, 'broker_used', False):
        raise exception_cls("broker_used is true")
    if getattr(item, 'order_created', False):
        raise exception_cls("order_created is true")
    if getattr(item, 'paper_state_mutated', False):
        raise exception_cls("paper_state_mutated is true")
    if getattr(item, 'telegram_real_sent', False):
        raise exception_cls("telegram_real_sent is true")
    if getattr(item, 'scraping_used', False):
        raise exception_cls("scraping_used is true")
    if getattr(item, 'dashboard_started', False):
        raise exception_cls("dashboard_started is true")
