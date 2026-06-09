import os
from pathlib import Path

content = """
from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
import uuid
from datetime import datetime

from usa_signal_bot.core.enums import (
    FullSystemIntegrationStatus,
    FullSystemIntegrationDecision,
    IntegrationInputKind,
    SystemArtifactKind,
    IntegrationDependencyKind,
    E2ERehearsalScenarioKind,
    RehearsalStepStatus,
    IntegrationReportKind,
    IntegrationSafetyRuleKind,
    Phase159ReadinessStatus,
    Phase159ReadinessRuleKind,
    FullSystemIntegrationQuality,
    FullSystemIntegrationRiskFlag,
    FullSystemIntegrationReportType
)

def create_phase158_handoff_ingestion_id() -> str:
    return f"phi-{uuid.uuid4().hex[:8]}"

def create_integration_input_reference_id() -> str:
    return f"iir-{uuid.uuid4().hex[:8]}"

def create_system_artifact_record_id() -> str:
    return f"sar-{uuid.uuid4().hex[:8]}"

def create_system_artifact_inventory_id() -> str:
    return f"sai-{uuid.uuid4().hex[:8]}"

def create_integration_dependency_edge_id() -> str:
    return f"ide-{uuid.uuid4().hex[:8]}"

def create_integration_dependency_graph_id() -> str:
    return f"idg-{uuid.uuid4().hex[:8]}"

def create_integration_boundary_contract_id() -> str:
    return f"ibc-{uuid.uuid4().hex[:8]}"

def create_e2e_rehearsal_scenario_id() -> str:
    return f"ers-{uuid.uuid4().hex[:8]}"

def create_dry_run_execution_step_id() -> str:
    return f"dre-{uuid.uuid4().hex[:8]}"

def create_e2e_rehearsal_plan_id() -> str:
    return f"erp-{uuid.uuid4().hex[:8]}"

def create_acceptance_rehearsal_result_id() -> str:
    return f"arr-{uuid.uuid4().hex[:8]}"

def create_integration_check_report_id() -> str:
    return f"icr-{uuid.uuid4().hex[:8]}"

def create_integration_safety_boundary_rule_id() -> str:
    return f"isbr-{uuid.uuid4().hex[:8]}"

def create_integration_safety_boundary_result_id() -> str:
    return f"isb-{uuid.uuid4().hex[:8]}"

def create_final_delivery_preparation_checklist_item_id() -> str:
    return f"fdpci-{uuid.uuid4().hex[:8]}"

def create_final_delivery_preparation_checklist_id() -> str:
    return f"fdpc-{uuid.uuid4().hex[:8]}"

def create_phase159_readiness_rule_id() -> str:
    return f"p159rr-{uuid.uuid4().hex[:8]}"

def create_phase159_readiness_gate_id() -> str:
    return f"p159rg-{uuid.uuid4().hex[:8]}"

def create_full_system_integration_context_id() -> str:
    return f"fsic-{uuid.uuid4().hex[:8]}"

def create_full_system_integration_full_review_id() -> str:
    return f"fsifr-{uuid.uuid4().hex[:8]}"

def _now_str() -> str:
    return datetime.utcnow().isoformat() + "Z"

@dataclass
class Phase158HandoffIngestionResult:
    ingestion_id: str = field(default_factory=create_phase158_handoff_ingestion_id)
    created_at_utc: str = field(default_factory=_now_str)
    source_path: Optional[str] = None
    source_package_id: Optional[str] = None
    source_certificate_id: Optional[str] = None
    available: bool = False
    package_valid: bool = False
    closure_certificate_valid: bool = False
    phase158_readiness_gate_passed: bool = False
    ready_for_phase158: bool = False
    read_only: bool = True
    research_data_only: bool = True
    integration_handoff_only: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    strategy_activation_allowed: bool = False
    actual_target_weights_produced: bool = False
    actual_allocation_produced: bool = False
    actual_position_size_produced: bool = False
    order_size_produced: bool = False
    capital_deployment_allowed: bool = False
    deployment_allowed: bool = False
    network_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    dashboard_started: bool = False
    daemon_started: bool = False
    scheduler_enabled: bool = False
    investment_advice: bool = False
    valid_for_phase158: bool = False
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ingestion_id": self.ingestion_id,
            "created_at_utc": self.created_at_utc,
            "source_path": self.source_path,
            "source_package_id": self.source_package_id,
            "source_certificate_id": self.source_certificate_id,
            "available": self.available,
            "package_valid": self.package_valid,
            "closure_certificate_valid": self.closure_certificate_valid,
            "phase158_readiness_gate_passed": self.phase158_readiness_gate_passed,
            "ready_for_phase158": self.ready_for_phase158,
            "read_only": self.read_only,
            "research_data_only": self.research_data_only,
            "integration_handoff_only": self.integration_handoff_only,
            "live_trading_enabled": self.live_trading_enabled,
            "paper_trading_enabled": self.paper_trading_enabled,
            "broker_execution_enabled": self.broker_execution_enabled,
            "real_order_creation_enabled": self.real_order_creation_enabled,
            "paper_state_mutation_enabled": self.paper_state_mutation_enabled,
            "telegram_real_send_enabled": self.telegram_real_send_enabled,
            "strategy_activation_allowed": self.strategy_activation_allowed,
            "actual_target_weights_produced": self.actual_target_weights_produced,
            "actual_allocation_produced": self.actual_allocation_produced,
            "actual_position_size_produced": self.actual_position_size_produced,
            "order_size_produced": self.order_size_produced,
            "capital_deployment_allowed": self.capital_deployment_allowed,
            "deployment_allowed": self.deployment_allowed,
            "network_used": self.network_used,
            "scraping_used": self.scraping_used,
            "html_parsing_used": self.html_parsing_used,
            "dashboard_started": self.dashboard_started,
            "daemon_started": self.daemon_started,
            "scheduler_enabled": self.scheduler_enabled,
            "investment_advice": self.investment_advice,
            "valid_for_phase158": self.valid_for_phase158,
            "risk_flags": [r.value for r in self.risk_flags],
            "warnings": self.warnings,
            "errors": self.errors,
            "metadata": self.metadata
        }

@dataclass
class IntegrationInputReference:
    input_ref_id: str = field(default_factory=create_integration_input_reference_id)
    created_at_utc: str = field(default_factory=_now_str)
    input_kind: IntegrationInputKind = IntegrationInputKind.UNKNOWN
    source_artifact_name: str = ""
    source_path: Optional[str] = None
    source_hash: Optional[str] = None
    available: bool = False
    read_only: bool = True
    required: bool = False
    valid: bool = False
    forbidden_fields_detected: List[str] = field(default_factory=list)
    research_data_only: bool = True
    integration_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_ref_id": self.input_ref_id,
            "created_at_utc": self.created_at_utc,
            "input_kind": self.input_kind.value if isinstance(self.input_kind, IntegrationInputKind) else self.input_kind,
            "source_artifact_name": self.source_artifact_name,
            "source_path": self.source_path,
            "source_hash": self.source_hash,
            "available": self.available,
            "read_only": self.read_only,
            "required": self.required,
            "valid": self.valid,
            "forbidden_fields_detected": self.forbidden_fields_detected,
            "research_data_only": self.research_data_only,
            "integration_only": self.integration_only,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class SystemArtifactRecord:
    artifact_id: str = field(default_factory=create_system_artifact_record_id)
    created_at_utc: str = field(default_factory=_now_str)
    artifact_kind: SystemArtifactKind = SystemArtifactKind.UNKNOWN
    artifact_name: str = ""
    module_path: Optional[str] = None
    source_phase: Optional[int] = None
    available: bool = False
    required_for_integration: bool = False
    has_schema: bool = False
    has_tests: bool = False
    has_cli: bool = False
    has_health_check: bool = False
    has_docs: bool = False
    read_only: bool = True
    deterministic_hash: Optional[str] = None
    artifact_valid: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "created_at_utc": self.created_at_utc,
            "artifact_kind": self.artifact_kind.value if isinstance(self.artifact_kind, SystemArtifactKind) else self.artifact_kind,
            "artifact_name": self.artifact_name,
            "module_path": self.module_path,
            "source_phase": self.source_phase,
            "available": self.available,
            "required_for_integration": self.required_for_integration,
            "has_schema": self.has_schema,
            "has_tests": self.has_tests,
            "has_cli": self.has_cli,
            "has_health_check": self.has_health_check,
            "has_docs": self.has_docs,
            "read_only": self.read_only,
            "deterministic_hash": self.deterministic_hash,
            "artifact_valid": self.artifact_valid,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class SystemArtifactInventory:
    inventory_id: str = field(default_factory=create_system_artifact_inventory_id)
    created_at_utc: str = field(default_factory=_now_str)
    artifacts: List[SystemArtifactRecord] = field(default_factory=list)
    artifact_count: int = 0
    required_artifact_count: int = 0
    available_required_count: int = 0
    missing_required_count: int = 0
    inventory_hash: Optional[str] = None
    inventory_valid: bool = False
    research_data_only: bool = True
    integration_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "inventory_id": self.inventory_id,
            "created_at_utc": self.created_at_utc,
            "artifacts": [a.to_dict() for a in self.artifacts],
            "artifact_count": self.artifact_count,
            "required_artifact_count": self.required_artifact_count,
            "available_required_count": self.available_required_count,
            "missing_required_count": self.missing_required_count,
            "inventory_hash": self.inventory_hash,
            "inventory_valid": self.inventory_valid,
            "research_data_only": self.research_data_only,
            "integration_only": self.integration_only,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class IntegrationDependencyEdge:
    edge_id: str = field(default_factory=create_integration_dependency_edge_id)
    created_at_utc: str = field(default_factory=_now_str)
    source_artifact_id: str = ""
    target_artifact_id: str = ""
    dependency_kind: IntegrationDependencyKind = IntegrationDependencyKind.UNKNOWN
    required: bool = False
    valid: bool = False
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "created_at_utc": self.created_at_utc,
            "source_artifact_id": self.source_artifact_id,
            "target_artifact_id": self.target_artifact_id,
            "dependency_kind": self.dependency_kind.value if isinstance(self.dependency_kind, IntegrationDependencyKind) else self.dependency_kind,
            "required": self.required,
            "valid": self.valid,
            "rationale": self.rationale,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class IntegrationDependencyGraph:
    graph_id: str = field(default_factory=create_integration_dependency_graph_id)
    created_at_utc: str = field(default_factory=_now_str)
    nodes: List[SystemArtifactRecord] = field(default_factory=list)
    edges: List[IntegrationDependencyEdge] = field(default_factory=list)
    node_count: int = 0
    edge_count: int = 0
    graph_hash: Optional[str] = None
    graph_valid: bool = False
    missing_dependency_count: int = 0
    cyclic_dependency_detected: bool = False
    research_data_only: bool = True
    integration_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "created_at_utc": self.created_at_utc,
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
            "node_count": self.node_count,
            "edge_count": self.edge_count,
            "graph_hash": self.graph_hash,
            "graph_valid": self.graph_valid,
            "missing_dependency_count": self.missing_dependency_count,
            "cyclic_dependency_detected": self.cyclic_dependency_detected,
            "research_data_only": self.research_data_only,
            "integration_only": self.integration_only,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class IntegrationBoundaryContract:
    contract_id: str = field(default_factory=create_integration_boundary_contract_id)
    created_at_utc: str = field(default_factory=_now_str)
    read_only_phase158_handoff: bool = True
    dry_run_rehearsal_only: bool = True
    local_fixture_only: bool = True
    no_live_trading: bool = True
    no_paper_state_mutation: bool = True
    no_broker_execution: bool = True
    no_real_order_creation: bool = True
    no_telegram_real_send: bool = True
    no_strategy_activation: bool = True
    no_deployment: bool = True
    no_production_patch: bool = True
    no_network: bool = True
    no_scraping: bool = True
    no_html_parsing: bool = True
    no_dashboard: bool = True
    no_daemon: bool = True
    no_scheduler: bool = True
    no_actual_target_weights: bool = True
    no_actual_allocation: bool = True
    no_order_size: bool = True
    no_capital_deployment: bool = True
    no_investment_advice: bool = True
    forbidden_fields: List[str] = field(default_factory=list)
    contract_valid: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "created_at_utc": self.created_at_utc,
            "read_only_phase158_handoff": self.read_only_phase158_handoff,
            "dry_run_rehearsal_only": self.dry_run_rehearsal_only,
            "local_fixture_only": self.local_fixture_only,
            "no_live_trading": self.no_live_trading,
            "no_paper_state_mutation": self.no_paper_state_mutation,
            "no_broker_execution": self.no_broker_execution,
            "no_real_order_creation": self.no_real_order_creation,
            "no_telegram_real_send": self.no_telegram_real_send,
            "no_strategy_activation": self.no_strategy_activation,
            "no_deployment": self.no_deployment,
            "no_production_patch": self.no_production_patch,
            "no_network": self.no_network,
            "no_scraping": self.no_scraping,
            "no_html_parsing": self.no_html_parsing,
            "no_dashboard": self.no_dashboard,
            "no_daemon": self.no_daemon,
            "no_scheduler": self.no_scheduler,
            "no_actual_target_weights": self.no_actual_target_weights,
            "no_actual_allocation": self.no_actual_allocation,
            "no_order_size": self.no_order_size,
            "no_capital_deployment": self.no_capital_deployment,
            "no_investment_advice": self.no_investment_advice,
            "forbidden_fields": self.forbidden_fields,
            "contract_valid": self.contract_valid,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class E2ERehearsalScenario:
    scenario_id: str = field(default_factory=create_e2e_rehearsal_scenario_id)
    created_at_utc: str = field(default_factory=_now_str)
    scenario_kind: E2ERehearsalScenarioKind = E2ERehearsalScenarioKind.UNKNOWN
    name: str = ""
    enabled: bool = True
    dry_run: bool = True
    local_fixture_only: bool = True
    required_artifacts: List[str] = field(default_factory=list)
    expected_outputs: List[str] = field(default_factory=list)
    forbidden_actions: List[str] = field(default_factory=list)
    scenario_valid: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "created_at_utc": self.created_at_utc,
            "scenario_kind": self.scenario_kind.value if isinstance(self.scenario_kind, E2ERehearsalScenarioKind) else self.scenario_kind,
            "name": self.name,
            "enabled": self.enabled,
            "dry_run": self.dry_run,
            "local_fixture_only": self.local_fixture_only,
            "required_artifacts": self.required_artifacts,
            "expected_outputs": self.expected_outputs,
            "forbidden_actions": self.forbidden_actions,
            "scenario_valid": self.scenario_valid,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class DryRunExecutionStep:
    step_id: str = field(default_factory=create_dry_run_execution_step_id)
    created_at_utc: str = field(default_factory=_now_str)
    scenario_id: str = ""
    step_name: str = ""
    command_preview: Optional[str] = None
    status: RehearsalStepStatus = RehearsalStepStatus.UNKNOWN
    dry_run: bool = True
    executed_real_side_effect: bool = False
    wrote_local_artifact: bool = False
    used_network: bool = False
    mutated_paper_state: bool = False
    sent_telegram: bool = False
    used_broker: bool = False
    created_order: bool = False
    deployed: bool = False
    output_summary: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "created_at_utc": self.created_at_utc,
            "scenario_id": self.scenario_id,
            "step_name": self.step_name,
            "command_preview": self.command_preview,
            "status": self.status.value if isinstance(self.status, RehearsalStepStatus) else self.status,
            "dry_run": self.dry_run,
            "executed_real_side_effect": self.executed_real_side_effect,
            "wrote_local_artifact": self.wrote_local_artifact,
            "used_network": self.used_network,
            "mutated_paper_state": self.mutated_paper_state,
            "sent_telegram": self.sent_telegram,
            "used_broker": self.used_broker,
            "created_order": self.created_order,
            "deployed": self.deployed,
            "output_summary": self.output_summary,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class E2ERehearsalPlan:
    plan_id: str = field(default_factory=create_e2e_rehearsal_plan_id)
    created_at_utc: str = field(default_factory=_now_str)
    scenarios: List[E2ERehearsalScenario] = field(default_factory=list)
    scenario_count: int = 0
    dry_run: bool = True
    local_fixture_only: bool = True
    plan_hash: Optional[str] = None
    plan_valid: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "created_at_utc": self.created_at_utc,
            "scenarios": [s.to_dict() for s in self.scenarios],
            "scenario_count": self.scenario_count,
            "dry_run": self.dry_run,
            "local_fixture_only": self.local_fixture_only,
            "plan_hash": self.plan_hash,
            "plan_valid": self.plan_valid,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class AcceptanceRehearsalResult:
    result_id: str = field(default_factory=create_acceptance_rehearsal_result_id)
    created_at_utc: str = field(default_factory=_now_str)
    plan: E2ERehearsalPlan = field(default_factory=E2ERehearsalPlan)
    execution_steps: List[DryRunExecutionStep] = field(default_factory=list)
    passed_count: int = 0
    warning_count: int = 0
    failed_count: int = 0
    blocked_count: int = 0
    result_hash: Optional[str] = None
    result_valid: bool = False
    dry_run_only: bool = True
    no_real_side_effects: bool = True
    no_network: bool = True
    no_paper_mutation: bool = True
    no_broker_execution: bool = True
    no_real_orders: bool = True
    no_telegram_real_send: bool = True
    no_deployment: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "created_at_utc": self.created_at_utc,
            "plan": self.plan.to_dict(),
            "execution_steps": [s.to_dict() for s in self.execution_steps],
            "passed_count": self.passed_count,
            "warning_count": self.warning_count,
            "failed_count": self.failed_count,
            "blocked_count": self.blocked_count,
            "result_hash": self.result_hash,
            "result_valid": self.result_valid,
            "dry_run_only": self.dry_run_only,
            "no_real_side_effects": self.no_real_side_effects,
            "no_network": self.no_network,
            "no_paper_mutation": self.no_paper_mutation,
            "no_broker_execution": self.no_broker_execution,
            "no_real_orders": self.no_real_orders,
            "no_telegram_real_send": self.no_telegram_real_send,
            "no_deployment": self.no_deployment,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class IntegrationCheckReport:
    report_id: str = field(default_factory=create_integration_check_report_id)
    created_at_utc: str = field(default_factory=_now_str)
    report_kind: IntegrationReportKind = IntegrationReportKind.UNKNOWN
    title: str = ""
    passed: bool = False
    checked_items: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocked_count: int = 0
    findings: List[str] = field(default_factory=list)
    report_hash: Optional[str] = None
    report_valid: bool = False
    dry_run_only: bool = True
    no_real_side_effects: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "created_at_utc": self.created_at_utc,
            "report_kind": self.report_kind.value if isinstance(self.report_kind, IntegrationReportKind) else self.report_kind,
            "title": self.title,
            "passed": self.passed,
            "checked_items": self.checked_items,
            "warning_count": self.warning_count,
            "error_count": self.error_count,
            "blocked_count": self.blocked_count,
            "findings": self.findings,
            "report_hash": self.report_hash,
            "report_valid": self.report_valid,
            "dry_run_only": self.dry_run_only,
            "no_real_side_effects": self.no_real_side_effects,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class IntegrationSafetyBoundaryRule:
    rule_id: str = field(default_factory=create_integration_safety_boundary_rule_id)
    created_at_utc: str = field(default_factory=_now_str)
    rule_kind: IntegrationSafetyRuleKind = IntegrationSafetyRuleKind.UNKNOWN
    name: str = ""
    required: bool = False
    passed: bool = False
    expected_value: Any = None
    observed_value: Any = None
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "created_at_utc": self.created_at_utc,
            "rule_kind": self.rule_kind.value if isinstance(self.rule_kind, IntegrationSafetyRuleKind) else self.rule_kind,
            "name": self.name,
            "required": self.required,
            "passed": self.passed,
            "expected_value": self.expected_value,
            "observed_value": self.observed_value,
            "rationale": self.rationale,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class IntegrationSafetyBoundaryResult:
    boundary_id: str = field(default_factory=create_integration_safety_boundary_result_id)
    created_at_utc: str = field(default_factory=_now_str)
    rules: List[IntegrationSafetyBoundaryRule] = field(default_factory=list)
    boundary_passed: bool = False
    full_system_integration_only: bool = True
    read_only_phase158_handoff: bool = True
    dry_run_rehearsal_only: bool = True
    no_live_trading: bool = True
    no_paper_state_mutation: bool = True
    no_broker_execution: bool = True
    no_real_order_creation: bool = True
    no_telegram_real_send: bool = True
    no_strategy_activation: bool = True
    no_deployment: bool = True
    no_production_patch: bool = True
    no_network: bool = True
    no_scraping: bool = True
    no_html_parsing: bool = True
    no_dashboard: bool = True
    no_daemon: bool = True
    no_scheduler: bool = True
    no_actual_target_weights: bool = True
    no_actual_allocation: bool = True
    no_order_size: bool = True
    no_capital_deployment: bool = True
    no_investment_advice: bool = True
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "boundary_id": self.boundary_id,
            "created_at_utc": self.created_at_utc,
            "rules": [r.to_dict() for r in self.rules],
            "boundary_passed": self.boundary_passed,
            "full_system_integration_only": self.full_system_integration_only,
            "read_only_phase158_handoff": self.read_only_phase158_handoff,
            "dry_run_rehearsal_only": self.dry_run_rehearsal_only,
            "no_live_trading": self.no_live_trading,
            "no_paper_state_mutation": self.no_paper_state_mutation,
            "no_broker_execution": self.no_broker_execution,
            "no_real_order_creation": self.no_real_order_creation,
            "no_telegram_real_send": self.no_telegram_real_send,
            "no_strategy_activation": self.no_strategy_activation,
            "no_deployment": self.no_deployment,
            "no_production_patch": self.no_production_patch,
            "no_network": self.no_network,
            "no_scraping": self.no_scraping,
            "no_html_parsing": self.no_html_parsing,
            "no_dashboard": self.no_dashboard,
            "no_daemon": self.no_daemon,
            "no_scheduler": self.no_scheduler,
            "no_actual_target_weights": self.no_actual_target_weights,
            "no_actual_allocation": self.no_actual_allocation,
            "no_order_size": self.no_order_size,
            "no_capital_deployment": self.no_capital_deployment,
            "no_investment_advice": self.no_investment_advice,
            "research_data_only": self.research_data_only,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class FinalDeliveryPreparationChecklistItem:
    item_id: str = field(default_factory=create_final_delivery_preparation_checklist_item_id)
    created_at_utc: str = field(default_factory=_now_str)
    name: str = ""
    required: bool = False
    passed: bool = False
    status: RehearsalStepStatus = RehearsalStepStatus.UNKNOWN
    owner_area: str = ""
    evidence: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "created_at_utc": self.created_at_utc,
            "name": self.name,
            "required": self.required,
            "passed": self.passed,
            "status": self.status.value if isinstance(self.status, RehearsalStepStatus) else self.status,
            "owner_area": self.owner_area,
            "evidence": self.evidence,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class FinalDeliveryPreparationChecklist:
    checklist_id: str = field(default_factory=create_final_delivery_preparation_checklist_id)
    created_at_utc: str = field(default_factory=_now_str)
    items: List[FinalDeliveryPreparationChecklistItem] = field(default_factory=list)
    item_count: int = 0
    passed_count: int = 0
    warning_count: int = 0
    failed_count: int = 0
    blocked_count: int = 0
    checklist_hash: Optional[str] = None
    checklist_valid: bool = False
    ready_for_release_candidate_audit: bool = False
    not_deployment_approval: bool = True
    not_trading_approval: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "checklist_id": self.checklist_id,
            "created_at_utc": self.created_at_utc,
            "items": [i.to_dict() for i in self.items],
            "item_count": self.item_count,
            "passed_count": self.passed_count,
            "warning_count": self.warning_count,
            "failed_count": self.failed_count,
            "blocked_count": self.blocked_count,
            "checklist_hash": self.checklist_hash,
            "checklist_valid": self.checklist_valid,
            "ready_for_release_candidate_audit": self.ready_for_release_candidate_audit,
            "not_deployment_approval": self.not_deployment_approval,
            "not_trading_approval": self.not_deployment_approval,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class Phase159ReadinessRule:
    rule_id: str = field(default_factory=create_phase159_readiness_rule_id)
    created_at_utc: str = field(default_factory=_now_str)
    rule_kind: Phase159ReadinessRuleKind = Phase159ReadinessRuleKind.UNKNOWN
    name: str = ""
    status: Phase159ReadinessStatus = Phase159ReadinessStatus.UNKNOWN
    required: bool = False
    passed: bool = False
    expected_value: Any = None
    observed_value: Any = None
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "created_at_utc": self.created_at_utc,
            "rule_kind": self.rule_kind.value if isinstance(self.rule_kind, Phase159ReadinessRuleKind) else self.rule_kind,
            "name": self.name,
            "status": self.status.value if isinstance(self.status, Phase159ReadinessStatus) else self.status,
            "required": self.required,
            "passed": self.passed,
            "expected_value": self.expected_value,
            "observed_value": self.observed_value,
            "rationale": self.rationale,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class Phase159ReadinessGate:
    gate_id: str = field(default_factory=create_phase159_readiness_gate_id)
    created_at_utc: str = field(default_factory=_now_str)
    status: Phase159ReadinessStatus = Phase159ReadinessStatus.UNKNOWN
    rules: List[Phase159ReadinessRule] = field(default_factory=list)
    inventory: SystemArtifactInventory = field(default_factory=SystemArtifactInventory)
    dependency_graph: IntegrationDependencyGraph = field(default_factory=IntegrationDependencyGraph)
    rehearsal_result: AcceptanceRehearsalResult = field(default_factory=AcceptanceRehearsalResult)
    integration_reports: List[IntegrationCheckReport] = field(default_factory=list)
    safety_boundary: IntegrationSafetyBoundaryResult = field(default_factory=IntegrationSafetyBoundaryResult)
    final_delivery_checklist: FinalDeliveryPreparationChecklist = field(default_factory=FinalDeliveryPreparationChecklist)
    ready_for_phase159: bool = False
    research_data_only: bool = True
    integration_only: bool = True
    dry_run_only: bool = True
    live_trading_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    production_patch_allowed: bool = False
    network_used: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "created_at_utc": self.created_at_utc,
            "status": self.status.value if isinstance(self.status, Phase159ReadinessStatus) else self.status,
            "rules": [r.to_dict() for r in self.rules],
            "inventory": self.inventory.to_dict(),
            "dependency_graph": self.dependency_graph.to_dict(),
            "rehearsal_result": self.rehearsal_result.to_dict(),
            "integration_reports": [r.to_dict() for r in self.integration_reports],
            "safety_boundary": self.safety_boundary.to_dict(),
            "final_delivery_checklist": self.final_delivery_checklist.to_dict(),
            "ready_for_phase159": self.ready_for_phase159,
            "research_data_only": self.research_data_only,
            "integration_only": self.integration_only,
            "dry_run_only": self.dry_run_only,
            "live_trading_enabled": self.live_trading_enabled,
            "paper_state_mutation_enabled": self.paper_state_mutation_enabled,
            "broker_execution_enabled": self.broker_execution_enabled,
            "real_order_creation_enabled": self.real_order_creation_enabled,
            "telegram_real_send_enabled": self.telegram_real_send_enabled,
            "strategy_activation_allowed": self.strategy_activation_allowed,
            "deployment_allowed": self.deployment_allowed,
            "production_patch_allowed": self.production_patch_allowed,
            "network_used": self.network_used,
            "investment_advice": self.investment_advice,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class FullSystemIntegrationContext:
    context_id: str = field(default_factory=create_full_system_integration_context_id)
    created_at_utc: str = field(default_factory=_now_str)
    status: FullSystemIntegrationStatus = FullSystemIntegrationStatus.UNKNOWN
    decision: FullSystemIntegrationDecision = FullSystemIntegrationDecision.UNKNOWN
    source_phase158_handoff_package_id: Optional[str] = None
    ingestion: Phase158HandoffIngestionResult = field(default_factory=Phase158HandoffIngestionResult)
    input_references: List[IntegrationInputReference] = field(default_factory=list)
    inventory: SystemArtifactInventory = field(default_factory=SystemArtifactInventory)
    dependency_graph: IntegrationDependencyGraph = field(default_factory=IntegrationDependencyGraph)
    boundary_contract: IntegrationBoundaryContract = field(default_factory=IntegrationBoundaryContract)
    rehearsal_plan: E2ERehearsalPlan = field(default_factory=E2ERehearsalPlan)
    rehearsal_result: AcceptanceRehearsalResult = field(default_factory=AcceptanceRehearsalResult)
    integration_reports: List[IntegrationCheckReport] = field(default_factory=list)
    safety_boundary: IntegrationSafetyBoundaryResult = field(default_factory=IntegrationSafetyBoundaryResult)
    final_delivery_checklist: FinalDeliveryPreparationChecklist = field(default_factory=FinalDeliveryPreparationChecklist)
    phase159_readiness_gate: Phase159ReadinessGate = field(default_factory=Phase159ReadinessGate)
    phase158_handoff_ingested: bool = False
    artifacts_loaded: bool = False
    inputs_resolved: bool = False
    artifact_inventory_built: bool = False
    dependency_graph_built: bool = False
    boundary_contract_built: bool = False
    e2e_rehearsal_plan_built: bool = False
    dry_run_rehearsal_executed: bool = False
    acceptance_result_built: bool = False
    schema_compatibility_report_built: bool = False
    cli_integration_report_built: bool = False
    config_integration_report_built: bool = False
    storage_integration_report_built: bool = False
    health_integration_report_built: bool = False
    quality_observability_report_built: bool = False
    notification_dry_run_report_built: bool = False
    safety_boundary_validated: bool = False
    final_delivery_checklist_built: bool = False
    phase159_readiness_gate_built: bool = False
    phase159_readiness_gate_passed: bool = False
    ready_for_phase159: bool = False
    research_data_only: bool = True
    integration_only: bool = True
    dry_run_only: bool = True
    deterministic: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    production_patch_allowed: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    dashboard_started: bool = False
    daemon_started: bool = False
    scheduler_enabled: bool = False
    actual_target_weights_produced: bool = False
    actual_allocation_produced: bool = False
    order_size_produced: bool = False
    capital_deployment_allowed: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FullSystemIntegrationRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "context_id": self.context_id,
            "created_at_utc": self.created_at_utc,
            "status": self.status.value if isinstance(self.status, FullSystemIntegrationStatus) else self.status,
            "decision": self.decision.value if isinstance(self.decision, FullSystemIntegrationDecision) else self.decision,
            "source_phase158_handoff_package_id": self.source_phase158_handoff_package_id,
            "ingestion": self.ingestion.to_dict(),
            "input_references": [i.to_dict() for i in self.input_references],
            "inventory": self.inventory.to_dict(),
            "dependency_graph": self.dependency_graph.to_dict(),
            "boundary_contract": self.boundary_contract.to_dict(),
            "rehearsal_plan": self.rehearsal_plan.to_dict(),
            "rehearsal_result": self.rehearsal_result.to_dict(),
            "integration_reports": [r.to_dict() for r in self.integration_reports],
            "safety_boundary": self.safety_boundary.to_dict(),
            "final_delivery_checklist": self.final_delivery_checklist.to_dict(),
            "phase159_readiness_gate": self.phase159_readiness_gate.to_dict(),
            "phase158_handoff_ingested": self.phase158_handoff_ingested,
            "artifacts_loaded": self.artifacts_loaded,
            "inputs_resolved": self.inputs_resolved,
            "artifact_inventory_built": self.artifact_inventory_built,
            "dependency_graph_built": self.dependency_graph_built,
            "boundary_contract_built": self.boundary_contract_built,
            "e2e_rehearsal_plan_built": self.e2e_rehearsal_plan_built,
            "dry_run_rehearsal_executed": self.dry_run_rehearsal_executed,
            "acceptance_result_built": self.acceptance_result_built,
            "schema_compatibility_report_built": self.schema_compatibility_report_built,
            "cli_integration_report_built": self.cli_integration_report_built,
            "config_integration_report_built": self.config_integration_report_built,
            "storage_integration_report_built": self.storage_integration_report_built,
            "health_integration_report_built": self.health_integration_report_built,
            "quality_observability_report_built": self.quality_observability_report_built,
            "notification_dry_run_report_built": self.notification_dry_run_report_built,
            "safety_boundary_validated": self.safety_boundary_validated,
            "final_delivery_checklist_built": self.final_delivery_checklist_built,
            "phase159_readiness_gate_built": self.phase159_readiness_gate_built,
            "phase159_readiness_gate_passed": self.phase159_readiness_gate_passed,
            "ready_for_phase159": self.ready_for_phase159,
            "research_data_only": self.research_data_only,
            "integration_only": self.integration_only,
            "dry_run_only": self.dry_run_only,
            "deterministic": self.deterministic,
            "live_trading_enabled": self.live_trading_enabled,
            "paper_trading_enabled": self.paper_trading_enabled,
            "paper_state_mutation_enabled": self.paper_state_mutation_enabled,
            "broker_execution_enabled": self.broker_execution_enabled,
            "real_order_creation_enabled": self.real_order_creation_enabled,
            "telegram_real_send_enabled": self.telegram_real_send_enabled,
            "strategy_activation_allowed": self.strategy_activation_allowed,
            "deployment_allowed": self.deployment_allowed,
            "production_patch_allowed": self.production_patch_allowed,
            "network_used": self.network_used,
            "paid_api_used": self.paid_api_used,
            "scraping_used": self.scraping_used,
            "html_parsing_used": self.html_parsing_used,
            "dashboard_started": self.dashboard_started,
            "daemon_started": self.daemon_started,
            "scheduler_enabled": self.scheduler_enabled,
            "actual_target_weights_produced": self.actual_target_weights_produced,
            "actual_allocation_produced": self.actual_allocation_produced,
            "order_size_produced": self.order_size_produced,
            "capital_deployment_allowed": self.capital_deployment_allowed,
            "investment_advice": self.investment_advice,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [r.value for r in self.risk_flags],
            "metadata": self.metadata
        }

@dataclass
class FullSystemIntegrationFullReview:
    review_id: str = field(default_factory=create_full_system_integration_full_review_id)
    created_at_utc: str = field(default_factory=_now_str)
    report_type: FullSystemIntegrationReportType = FullSystemIntegrationReportType.UNKNOWN
    ingestion: Phase158HandoffIngestionResult = field(default_factory=Phase158HandoffIngestionResult)
    context: FullSystemIntegrationContext = field(default_factory=FullSystemIntegrationContext)
    inventory: SystemArtifactInventory = field(default_factory=SystemArtifactInventory)
    dependency_graph: IntegrationDependencyGraph = field(default_factory=IntegrationDependencyGraph)
    rehearsal_result: AcceptanceRehearsalResult = field(default_factory=AcceptanceRehearsalResult)
    integration_reports: List[IntegrationCheckReport] = field(default_factory=list)
    safety_boundary: IntegrationSafetyBoundaryResult = field(default_factory=IntegrationSafetyBoundaryResult)
    final_delivery_checklist: FinalDeliveryPreparationChecklist = field(default_factory=FinalDeliveryPreparationChecklist)
    phase159_readiness_gate: Phase159ReadinessGate = field(default_factory=Phase159ReadinessGate)
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "review_id": self.review_id,
            "created_at_utc": self.created_at_utc,
            "report_type": self.report_type.value if isinstance(self.report_type, FullSystemIntegrationReportType) else self.report_type,
            "ingestion": self.ingestion.to_dict(),
            "context": self.context.to_dict(),
            "inventory": self.inventory.to_dict(),
            "dependency_graph": self.dependency_graph.to_dict(),
            "rehearsal_result": self.rehearsal_result.to_dict(),
            "integration_reports": [r.to_dict() for r in self.integration_reports],
            "safety_boundary": self.safety_boundary.to_dict(),
            "final_delivery_checklist": self.final_delivery_checklist.to_dict(),
            "phase159_readiness_gate": self.phase159_readiness_gate.to_dict(),
            "output_paths": self.output_paths,
            "warnings": self.warnings,
            "errors": self.errors
        }
"""
with open("usa_signal_bot/integration/phase158_models.py", "w") as f:
    f.write(content)
