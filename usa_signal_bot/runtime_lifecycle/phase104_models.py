from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
import datetime
import uuid

from usa_signal_bot.core.enums import (
    RuntimeLifecycleStatus,
    RuntimeLifecycleDecision,
    StartupCheckType,
    StartupCheckStatus,
    ServiceReadinessStatus,
    ReadinessGateStatus,
    ReadinessGateDecision,
    LifecycleTransitionStatus,
    LifecycleRiskFlag,
    RuntimeLifecycleReportType
)

@dataclass
class ServiceGraphIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_graph_id: Optional[str]
    available: bool
    service_graph_valid: bool
    dry_run_passed: bool
    graph_has_cycles: bool
    missing_dependency_count: int
    invalid_contract_count: int
    blocked_route_count: int
    execution_performed: bool
    network_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    scraping_used: bool
    dashboard_started: bool
    valid_for_phase104: bool
    risk_flags: List[LifecycleRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class StartupCheckItem:
    check_id: str
    created_at_utc: str
    check_type: StartupCheckType
    service_id: Optional[str]
    service_name: Optional[str]
    status: StartupCheckStatus
    required: bool
    message: str
    details: Dict[str, Any]
    risk_flags: List[LifecycleRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class StartupCheckReport:
    report_id: str
    created_at_utc: str
    status: RuntimeLifecycleStatus
    total_checks: int
    passed_checks: int
    warning_checks: int
    failed_checks: int
    blocked_checks: int
    skipped_checks: int
    items: List[StartupCheckItem]
    startup_checks_passed: bool
    startup_checks_metadata_only: bool
    execution_performed: bool
    network_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    scraping_used: bool
    dashboard_started: bool
    risk_flags: List[LifecycleRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class ServiceReadinessItem:
    readiness_id: str
    created_at_utc: str
    service_id: str
    service_name: str
    readiness_status: ServiceReadinessStatus
    metadata_ready: bool
    read_only_ready: bool
    local_compute_ready: bool
    config_ready: bool
    dependency_ready: bool
    validation_ready: bool
    observability_ready: bool
    notification_boundary_ready: bool
    provider_interface_ready: bool
    no_execution_ready: bool
    required_followups: List[str]
    risk_flags: List[LifecycleRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class ServiceReadinessMatrix:
    matrix_id: str
    created_at_utc: str
    items: List[ServiceReadinessItem]
    total_services: int
    ready_services: int
    blocked_services: int
    not_ready_services: int
    disabled_services: int
    all_required_services_ready: bool
    no_execution_ready: bool
    risk_flags: List[LifecycleRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class ReadinessGate:
    gate_id: str
    created_at_utc: str
    status: ReadinessGateStatus
    decision: ReadinessGateDecision
    source_service_graph_review_id: Optional[str]
    source_startup_report_id: Optional[str]
    source_readiness_matrix_id: Optional[str]
    startup_report: Optional[StartupCheckReport]
    readiness_matrix: Optional[ServiceReadinessMatrix]
    gate_passed: bool
    metadata_only: bool
    read_only: bool
    ready_for_phase105: bool
    activation_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    dashboard_enabled: bool
    execution_performed: bool
    network_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    scraping_used: bool
    dashboard_started: bool
    risk_flags: List[LifecycleRiskFlag]
    required_followups: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class LifecycleTransition:
    transition_id: str
    created_at_utc: str
    from_status: RuntimeLifecycleStatus
    to_status: RuntimeLifecycleStatus
    transition_status: LifecycleTransitionStatus
    allowed: bool
    metadata_only: bool
    read_only: bool
    reason: str
    risk_flags: List[LifecycleRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class RuntimeLifecycleContext:
    context_id: str
    created_at_utc: str
    status: RuntimeLifecycleStatus
    decision: RuntimeLifecycleDecision
    source_service_graph_ingestion_id: Optional[str]
    startup_report: StartupCheckReport
    readiness_matrix: ServiceReadinessMatrix
    readiness_gate: ReadinessGate
    transitions: List[LifecycleTransition]
    lifecycle_ready: bool
    ready_for_phase105: bool
    activation_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    dashboard_enabled: bool
    execution_performed: bool
    network_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    scraping_used: bool
    dashboard_started: bool
    risk_flags: List[LifecycleRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class RuntimeLifecycleFullReview:
    review_id: str
    created_at_utc: str
    report_type: RuntimeLifecycleReportType
    service_graph_ingestion: ServiceGraphIngestionResult
    lifecycle_context: RuntimeLifecycleContext
    startup_report: StartupCheckReport
    readiness_matrix: ServiceReadinessMatrix
    readiness_gate: ReadinessGate
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]


def _now_str() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def create_service_graph_ingestion_id() -> str:
    return f"SGI-{uuid.uuid4().hex[:8]}"

def create_startup_check_id() -> str:
    return f"SCK-{uuid.uuid4().hex[:8]}"

def create_startup_check_report_id() -> str:
    return f"SCR-{uuid.uuid4().hex[:8]}"

def create_service_readiness_id() -> str:
    return f"SRI-{uuid.uuid4().hex[:8]}"

def create_service_readiness_matrix_id() -> str:
    return f"SRM-{uuid.uuid4().hex[:8]}"

def create_readiness_gate_id() -> str:
    return f"RG-{uuid.uuid4().hex[:8]}"

def create_lifecycle_transition_id() -> str:
    return f"LT-{uuid.uuid4().hex[:8]}"

def create_runtime_lifecycle_context_id() -> str:
    return f"RLC-{uuid.uuid4().hex[:8]}"

def create_runtime_lifecycle_full_review_id() -> str:
    return f"RLR-{uuid.uuid4().hex[:8]}"

# Dict serializers
import dataclasses
def service_graph_ingestion_result_to_dict(item: ServiceGraphIngestionResult) -> dict:
    return dataclasses.asdict(item)

def startup_check_item_to_dict(item: StartupCheckItem) -> dict:
    return dataclasses.asdict(item)

def startup_check_report_to_dict(item: StartupCheckReport) -> dict:
    return dataclasses.asdict(item)

def service_readiness_item_to_dict(item: ServiceReadinessItem) -> dict:
    return dataclasses.asdict(item)

def service_readiness_matrix_to_dict(item: ServiceReadinessMatrix) -> dict:
    return dataclasses.asdict(item)

def readiness_gate_to_dict(item: ReadinessGate) -> dict:
    return dataclasses.asdict(item)

def lifecycle_transition_to_dict(item: LifecycleTransition) -> dict:
    return dataclasses.asdict(item)

def runtime_lifecycle_context_to_dict(item: RuntimeLifecycleContext) -> dict:
    return dataclasses.asdict(item)

def runtime_lifecycle_full_review_to_dict(item: RuntimeLifecycleFullReview) -> dict:
    return dataclasses.asdict(item)

# Validations
from usa_signal_bot.core.exceptions import LifecycleValidationError

def validate_service_graph_ingestion_result(item: ServiceGraphIngestionResult) -> None:
    if item.execution_performed:
        raise LifecycleValidationError("Service graph ingestion execution_performed MUST be False")
    if item.network_used or item.broker_used or item.order_created or item.paper_state_mutated or item.telegram_real_sent or item.scraping_used or item.dashboard_started:
        raise LifecycleValidationError("Service graph ingestion execution flags MUST be False")

def validate_startup_check_report(item: StartupCheckReport) -> None:
    if item.execution_performed or item.network_used or item.broker_used or item.order_created or item.paper_state_mutated or item.telegram_real_sent or item.scraping_used or item.dashboard_started:
        raise LifecycleValidationError("Startup check report execution flags MUST be False")
    if not item.startup_checks_metadata_only:
        raise LifecycleValidationError("startup_checks_metadata_only MUST be True")

def validate_service_readiness_matrix(item: ServiceReadinessMatrix) -> None:
    if not item.no_execution_ready and item.all_required_services_ready:
        raise LifecycleValidationError("Service readiness matrix CANNOT be ready if no_execution_ready is False")

def validate_readiness_gate(item: ReadinessGate) -> None:
    if item.activation_allowed or item.active_paper_enabled or item.broker_execution_enabled or item.paper_state_mutation_enabled or item.telegram_real_send_enabled or item.scraping_enabled or item.dashboard_enabled:
        raise LifecycleValidationError("Readiness gate MUST strictly forbid execution enablement")
    if item.execution_performed or item.network_used or item.broker_used or item.order_created or item.paper_state_mutated or item.telegram_real_sent or item.scraping_used or item.dashboard_started:
        raise LifecycleValidationError("Readiness gate MUST strictly forbid execution performance")
    if not item.metadata_only:
        raise LifecycleValidationError("Readiness gate metadata_only MUST be True")

def validate_runtime_lifecycle_context(item: RuntimeLifecycleContext) -> None:
    if item.activation_allowed or item.active_paper_enabled or item.broker_execution_enabled or item.paper_state_mutation_enabled or item.telegram_real_send_enabled or item.scraping_enabled or item.dashboard_enabled:
        raise LifecycleValidationError("Lifecycle context MUST strictly forbid execution enablement")
    if item.execution_performed or item.network_used or item.broker_used or item.order_created or item.paper_state_mutated or item.telegram_real_sent or item.scraping_used or item.dashboard_started:
        raise LifecycleValidationError("Lifecycle context MUST strictly forbid execution performance")

def validate_runtime_lifecycle_full_review(item: RuntimeLifecycleFullReview) -> None:
    validate_service_graph_ingestion_result(item.service_graph_ingestion)
    validate_startup_check_report(item.startup_report)
    validate_service_readiness_matrix(item.readiness_matrix)
    validate_readiness_gate(item.readiness_gate)
    validate_runtime_lifecycle_context(item.lifecycle_context)
