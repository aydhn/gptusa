from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    RuntimeServiceGraphStatus,
    RuntimeServiceGraphDecision,
    RuntimeServiceKind,
    RuntimeServiceStatus,
    DependencyType,
    DependencyContractStatus,
    OrchestrationMode,
    OrchestrationDecision,
    OrchestrationStepStatus,
    RuntimeServiceGraphRiskFlag,
    RuntimeServiceGraphReportType
)

@dataclass
class RuntimeRegistryIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    available: bool
    registry_normalized: bool
    provider_interfaces_ready: bool
    safety_policy_valid: bool
    activation_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    dashboard_enabled: bool
    valid_for_phase103: bool
    risk_flags: List[RuntimeServiceGraphRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RuntimeServiceNode:
    service_id: str
    service_name: str
    kind: RuntimeServiceKind
    status: RuntimeServiceStatus
    package_path: Optional[str]
    capabilities: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    optional_dependencies: List[str] = field(default_factory=list)
    blocked_capabilities: List[str] = field(default_factory=list)
    phase_introduced: int = 103
    future_phase_ready: bool = False
    metadata_only: bool = True
    read_only: bool = True
    local_compute_allowed: bool = False
    network_allowed: bool = False
    execution_allowed: bool = False
    broker_allowed: bool = False
    order_allowed: bool = False
    paper_mutation_allowed: bool = False
    telegram_real_send_allowed: bool = False
    scraping_allowed: bool = False
    dashboard_allowed: bool = False
    risk_flags: List[RuntimeServiceGraphRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RuntimeServiceEdge:
    edge_id: str
    source_service_id: str
    target_service_id: str
    dependency_type: DependencyType
    required: bool
    read_only: bool
    metadata_only: bool
    future_phase: bool
    blocked: bool
    rationale: str
    risk_flags: List[RuntimeServiceGraphRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DependencyContract:
    contract_id: str
    source_service_id: str
    target_service_id: str
    dependency_type: DependencyType
    status: DependencyContractStatus
    allowed_capabilities: List[str] = field(default_factory=list)
    blocked_capabilities: List[str] = field(default_factory=list)
    requires_metadata_only: bool = True
    requires_read_only: bool = True
    allows_network: bool = False
    allows_execution: bool = False
    allows_broker: bool = False
    allows_order: bool = False
    allows_paper_mutation: bool = False
    allows_telegram_real_send: bool = False
    allows_scraping: bool = False
    allows_dashboard: bool = False
    validation_errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    risk_flags: List[RuntimeServiceGraphRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RuntimeServiceGraph:
    graph_id: str
    created_at_utc: str
    status: RuntimeServiceGraphStatus
    decision: RuntimeServiceGraphDecision
    source_runtime_registry_review_id: Optional[str]
    nodes: List[RuntimeServiceNode] = field(default_factory=list)
    edges: List[RuntimeServiceEdge] = field(default_factory=list)
    dependency_contracts: List[DependencyContract] = field(default_factory=list)
    graph_has_cycles: bool = False
    missing_dependency_count: int = 0
    invalid_contract_count: int = 0
    blocked_route_count: int = 0
    provider_nodes_ready: bool = False
    core_nodes_ready: bool = False
    graph_valid: bool = False
    activation_allowed: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    scraping_enabled: bool = False
    dashboard_enabled: bool = False
    risk_flags: List[RuntimeServiceGraphRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class OrchestrationStep:
    step_id: str
    service_id: str
    service_name: str
    order_index: int
    mode: OrchestrationMode
    status: OrchestrationStepStatus
    action: str
    metadata_only: bool = True
    read_only: bool = True
    execution_allowed: bool = False
    network_allowed: bool = False
    broker_allowed: bool = False
    order_allowed: bool = False
    paper_mutation_allowed: bool = False
    telegram_real_send_allowed: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[RuntimeServiceGraphRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SafeOrchestrationPlan:
    plan_id: str
    created_at_utc: str
    decision: OrchestrationDecision
    mode: OrchestrationMode
    graph_id: Optional[str]
    steps: List[OrchestrationStep] = field(default_factory=list)
    startup_order: List[str] = field(default_factory=list)
    dry_run_only: bool = True
    metadata_only: bool = True
    read_only: bool = True
    execution_allowed: bool = False
    network_allowed: bool = False
    broker_allowed: bool = False
    order_allowed: bool = False
    paper_mutation_allowed: bool = False
    telegram_real_send_allowed: bool = False
    scraping_allowed: bool = False
    dashboard_allowed: bool = False
    risk_flags: List[RuntimeServiceGraphRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class OrchestrationDryRunResult:
    result_id: str
    created_at_utc: str
    plan_id: Optional[str]
    graph_id: Optional[str]
    status: RuntimeServiceGraphStatus
    executed_step_count: int = 0
    blocked_step_count: int = 0
    skipped_step_count: int = 0
    dry_run_only: bool = True
    metadata_only: bool = True
    execution_performed: bool = False
    network_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    scraping_used: bool = False
    dashboard_started: bool = False
    passed: bool = False
    risk_flags: List[RuntimeServiceGraphRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RuntimeServiceGraphFullReview:
    review_id: str
    created_at_utc: str
    report_type: RuntimeServiceGraphReportType
    registry_ingestion: RuntimeRegistryIngestionResult
    service_graph: RuntimeServiceGraph
    orchestration_plan: SafeOrchestrationPlan
    dry_run_result: OrchestrationDryRunResult
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def create_runtime_registry_ingestion_id() -> str:
    return f"ingest_{uuid.uuid4().hex[:8]}"

def create_service_id(prefix: str = "service") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_edge_id(prefix: str = "edge") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_dependency_contract_id(prefix: str = "dependency_contract") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_runtime_service_graph_id(prefix: str = "runtime_service_graph") -> str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:4]}"

def create_orchestration_step_id(prefix: str = "orchestration_step") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_orchestration_plan_id(prefix: str = "safe_orchestration_plan") -> str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:4]}"

def create_orchestration_dry_run_result_id(prefix: str = "orchestration_dry_run") -> str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:4]}"

def create_runtime_service_graph_full_review_id(prefix: str = "runtime_service_graph_full_review") -> str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:4]}"

def runtime_registry_ingestion_result_to_dict(item: RuntimeRegistryIngestionResult) -> dict:
    from dataclasses import asdict
    return asdict(item)

def runtime_service_node_to_dict(item: RuntimeServiceNode) -> dict:
    from dataclasses import asdict
    return asdict(item)

def runtime_service_edge_to_dict(item: RuntimeServiceEdge) -> dict:
    from dataclasses import asdict
    return asdict(item)

def dependency_contract_to_dict(item: DependencyContract) -> dict:
    from dataclasses import asdict
    return asdict(item)

def runtime_service_graph_to_dict(item: RuntimeServiceGraph) -> dict:
    from dataclasses import asdict
    return asdict(item)

def orchestration_step_to_dict(item: OrchestrationStep) -> dict:
    from dataclasses import asdict
    return asdict(item)

def safe_orchestration_plan_to_dict(item: SafeOrchestrationPlan) -> dict:
    from dataclasses import asdict
    return asdict(item)

def orchestration_dry_run_result_to_dict(item: OrchestrationDryRunResult) -> dict:
    from dataclasses import asdict
    return asdict(item)

def runtime_service_graph_full_review_to_dict(item: RuntimeServiceGraphFullReview) -> dict:
    from dataclasses import asdict
    return asdict(item)

def validate_runtime_registry_ingestion_result(item: RuntimeRegistryIngestionResult) -> None:
    if item.activation_allowed: raise ValueError("activation_allowed must be false")
    if item.active_paper_enabled: raise ValueError("active_paper_enabled must be false")
    if item.broker_execution_enabled: raise ValueError("broker_execution_enabled must be false")
    if item.paper_state_mutation_enabled: raise ValueError("paper_state_mutation_enabled must be false")
    if item.telegram_real_send_enabled: raise ValueError("telegram_real_send_enabled must be false")
    if item.scraping_enabled: raise ValueError("scraping_enabled must be false")
    if item.dashboard_enabled: raise ValueError("dashboard_enabled must be false")

def validate_runtime_service_node(item: RuntimeServiceNode) -> None:
    if item.execution_allowed: raise ValueError("execution_allowed must be false")
    if item.broker_allowed: raise ValueError("broker_allowed must be false")
    if item.order_allowed: raise ValueError("order_allowed must be false")
    if item.paper_mutation_allowed: raise ValueError("paper_mutation_allowed must be false")
    if item.telegram_real_send_allowed: raise ValueError("telegram_real_send_allowed must be false")
    if item.scraping_allowed: raise ValueError("scraping_allowed must be false")
    if item.dashboard_allowed: raise ValueError("dashboard_allowed must be false")

def validate_dependency_contract(item: DependencyContract) -> None:
    pass

def validate_runtime_service_graph(item: RuntimeServiceGraph) -> None:
    pass

def validate_safe_orchestration_plan(item: SafeOrchestrationPlan) -> None:
    if not item.dry_run_only: raise ValueError("dry_run_only must be true")
    if item.execution_allowed: raise ValueError("execution_allowed must be false")
    if item.network_allowed: raise ValueError("network_allowed must be false")
    if item.broker_allowed: raise ValueError("broker_allowed must be false")
    if item.order_allowed: raise ValueError("order_allowed must be false")
    if item.paper_mutation_allowed: raise ValueError("paper_mutation_allowed must be false")
    if item.telegram_real_send_allowed: raise ValueError("telegram_real_send_allowed must be false")
    if item.scraping_allowed: raise ValueError("scraping_allowed must be false")
    if item.dashboard_allowed: raise ValueError("dashboard_allowed must be false")

def validate_orchestration_dry_run_result(item: OrchestrationDryRunResult) -> None:
    if item.execution_performed: raise ValueError("execution_performed must be false")
    if item.network_used: raise ValueError("network_used must be false")
    if item.broker_used: raise ValueError("broker_used must be false")
    if item.order_created: raise ValueError("order_created must be false")
    if item.paper_state_mutated: raise ValueError("paper_state_mutated must be false")
    if item.telegram_real_sent: raise ValueError("telegram_real_sent must be false")
    if item.scraping_used: raise ValueError("scraping_used must be false")
    if item.dashboard_started: raise ValueError("dashboard_started must be false")

def validate_runtime_service_graph_full_review(item: RuntimeServiceGraphFullReview) -> None:
    pass
