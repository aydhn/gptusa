from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
from usa_signal_bot.core.enums import (
    FinalClosureStatus,
    FinalClosureDecision,
    FinalInputKind,
    FinalArtifactKind,
    FinalPhaseBandKind,
    FinalAuditAreaKind,
    FinalAuditStatus,
    FinalSafetyRuleKind,
    ProjectClosureStatus,
    FinalClosureReadinessStatus,
    FinalClosureReadinessRuleKind,
    FinalClosureQuality,
    FinalClosureRiskFlag,
    FinalClosureReportType
)
import uuid
import datetime

def generate_timestamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def create_phase160_handoff_ingestion_id() -> str:
    return f"phi-{uuid.uuid4().hex[:8]}"

def create_final_input_reference_id() -> str:
    return f"fir-{uuid.uuid4().hex[:8]}"

def create_final_artifact_record_id() -> str:
    return f"far-{uuid.uuid4().hex[:8]}"

def create_final_artifact_index_id() -> str:
    return f"fai-{uuid.uuid4().hex[:8]}"

def create_final_phase_lineage_record_id() -> str:
    return f"flr-{uuid.uuid4().hex[:8]}"

def create_final_phase_lineage_id() -> str:
    return f"fpl-{uuid.uuid4().hex[:8]}"

def create_final_system_audit_checklist_item_id() -> str:
    return f"faci-{uuid.uuid4().hex[:8]}"

def create_final_system_audit_checklist_id() -> str:
    return f"fac-{uuid.uuid4().hex[:8]}"

def create_final_system_audit_report_id() -> str:
    return f"fsar-{uuid.uuid4().hex[:8]}"

def create_final_safety_closure_id() -> str:
    return f"fsc-{uuid.uuid4().hex[:8]}"

def create_final_limitation_record_id() -> str:
    return f"flrec-{uuid.uuid4().hex[:8]}"

def create_final_limitation_register_id() -> str:
    return f"flreg-{uuid.uuid4().hex[:8]}"

def create_final_documentation_index_id() -> str:
    return f"fdi-{uuid.uuid4().hex[:8]}"

def create_final_runbook_index_id() -> str:
    return f"fri-{uuid.uuid4().hex[:8]}"

def create_final_test_evidence_summary_id() -> str:
    return f"ftes-{uuid.uuid4().hex[:8]}"

def create_final_quality_observability_summary_id() -> str:
    return f"fqos-{uuid.uuid4().hex[:8]}"

def create_final_delivery_certificate_id() -> str:
    return f"fdc-{uuid.uuid4().hex[:8]}"

def create_project_closure_report_id() -> str:
    return f"pcr-{uuid.uuid4().hex[:8]}"

def create_project_closure_manifest_id() -> str:
    return f"pcm-{uuid.uuid4().hex[:8]}"

def create_final_safety_boundary_rule_id() -> str:
    return f"fsbr-{uuid.uuid4().hex[:8]}"

def create_final_safety_boundary_result_id() -> str:
    return f"fsbres-{uuid.uuid4().hex[:8]}"

def create_final_closure_readiness_rule_id() -> str:
    return f"fcrr-{uuid.uuid4().hex[:8]}"

def create_final_closure_readiness_gate_id() -> str:
    return f"fcrg-{uuid.uuid4().hex[:8]}"

def create_final_closure_context_id() -> str:
    return f"fcc-{uuid.uuid4().hex[:8]}"

def create_final_closure_full_review_id() -> str:
    return f"fcfr-{uuid.uuid4().hex[:8]}"

@dataclass
class Phase160HandoffIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_package_id: Optional[str]
    source_freeze_certificate_id: Optional[str]
    available: bool
    package_valid: bool
    final_freeze_certificate_valid: bool
    release_candidate_audit_valid: bool
    release_candidate_risk_register_valid: bool
    evidence_bundle_valid: bool
    phase160_readiness_gate_passed: bool
    ready_for_phase160: bool
    read_only: bool
    research_data_only: bool
    final_delivery_handoff_only: bool
    live_trading_enabled: bool
    paper_trading_enabled: bool
    paper_state_mutation_enabled: bool
    broker_execution_enabled: bool
    real_order_creation_enabled: bool
    telegram_real_send_enabled: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    production_patch_allowed: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    dashboard_started: bool
    daemon_started: bool
    scheduler_enabled: bool
    actual_target_weights_produced: bool
    actual_allocation_produced: bool
    order_size_produced: bool
    capital_deployment_allowed: bool
    investment_advice: bool
    valid_for_phase160: bool
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ingestion_id": self.ingestion_id,
            "created_at_utc": self.created_at_utc,
            "source_path": self.source_path,
            "source_package_id": self.source_package_id,
            "source_freeze_certificate_id": self.source_freeze_certificate_id,
            "available": self.available,
            "package_valid": self.package_valid,
            "final_freeze_certificate_valid": self.final_freeze_certificate_valid,
            "release_candidate_audit_valid": self.release_candidate_audit_valid,
            "release_candidate_risk_register_valid": self.release_candidate_risk_register_valid,
            "evidence_bundle_valid": self.evidence_bundle_valid,
            "phase160_readiness_gate_passed": self.phase160_readiness_gate_passed,
            "ready_for_phase160": self.ready_for_phase160,
            "read_only": self.read_only,
            "research_data_only": self.research_data_only,
            "final_delivery_handoff_only": self.final_delivery_handoff_only,
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
            "valid_for_phase160": self.valid_for_phase160,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "warnings": self.warnings,
            "errors": self.errors,
            "metadata": self.metadata,
        }

@dataclass
class FinalInputReference:
    input_ref_id: str
    created_at_utc: str
    input_kind: FinalInputKind
    source_artifact_name: str
    source_path: Optional[str]
    source_hash: Optional[str]
    available: bool
    read_only: bool
    required: bool
    valid: bool
    forbidden_fields_detected: List[str] = field(default_factory=list)
    research_data_only: bool = True
    final_closure_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_ref_id": self.input_ref_id,
            "created_at_utc": self.created_at_utc,
            "input_kind": self.input_kind.value,
            "source_artifact_name": self.source_artifact_name,
            "source_path": self.source_path,
            "source_hash": self.source_hash,
            "available": self.available,
            "read_only": self.read_only,
            "required": self.required,
            "valid": self.valid,
            "forbidden_fields_detected": self.forbidden_fields_detected,
            "research_data_only": self.research_data_only,
            "final_closure_only": self.final_closure_only,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalArtifactRecord:
    artifact_id: str
    created_at_utc: str
    artifact_kind: FinalArtifactKind
    artifact_name: str
    source_phase_range: Optional[str]
    module_path: Optional[str]
    doc_path: Optional[str]
    test_path: Optional[str]
    available: bool
    required: bool
    read_only: bool
    deterministic_hash: Optional[str]
    artifact_valid: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "created_at_utc": self.created_at_utc,
            "artifact_kind": self.artifact_kind.value,
            "artifact_name": self.artifact_name,
            "source_phase_range": self.source_phase_range,
            "module_path": self.module_path,
            "doc_path": self.doc_path,
            "test_path": self.test_path,
            "available": self.available,
            "required": self.required,
            "read_only": self.read_only,
            "deterministic_hash": self.deterministic_hash,
            "artifact_valid": self.artifact_valid,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalArtifactIndex:
    index_id: str
    created_at_utc: str
    artifacts: List[FinalArtifactRecord] = field(default_factory=list)
    artifact_count: int = 0
    required_artifact_count: int = 0
    available_required_count: int = 0
    missing_required_count: int = 0
    index_hash: Optional[str] = None
    index_valid: bool = False
    research_data_only: bool = True
    final_closure_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index_id": self.index_id,
            "created_at_utc": self.created_at_utc,
            "artifacts": [a.to_dict() for a in self.artifacts],
            "artifact_count": self.artifact_count,
            "required_artifact_count": self.required_artifact_count,
            "available_required_count": self.available_required_count,
            "missing_required_count": self.missing_required_count,
            "index_hash": self.index_hash,
            "index_valid": self.index_valid,
            "research_data_only": self.research_data_only,
            "final_closure_only": self.final_closure_only,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalPhaseLineageRecord:
    lineage_record_id: str
    created_at_utc: str
    band_kind: FinalPhaseBandKind
    start_phase: int
    end_phase: int
    band_name: str
    completed: bool
    closure_artifact_name: Optional[str]
    closure_artifact_hash: Optional[str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lineage_record_id": self.lineage_record_id,
            "created_at_utc": self.created_at_utc,
            "band_kind": self.band_kind.value,
            "start_phase": self.start_phase,
            "end_phase": self.end_phase,
            "band_name": self.band_name,
            "completed": self.completed,
            "closure_artifact_name": self.closure_artifact_name,
            "closure_artifact_hash": self.closure_artifact_hash,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalPhaseLineage:
    lineage_id: str
    created_at_utc: str
    records: List[FinalPhaseLineageRecord] = field(default_factory=list)
    start_phase: int = 1
    end_phase: int = 160
    final_phase: int = 160
    all_bands_completed: bool = False
    lineage_hash: Optional[str] = None
    lineage_valid: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lineage_id": self.lineage_id,
            "created_at_utc": self.created_at_utc,
            "records": [r.to_dict() for r in self.records],
            "start_phase": self.start_phase,
            "end_phase": self.end_phase,
            "final_phase": self.final_phase,
            "all_bands_completed": self.all_bands_completed,
            "lineage_hash": self.lineage_hash,
            "lineage_valid": self.lineage_valid,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalSystemAuditChecklistItem:
    item_id: str
    created_at_utc: str
    area_kind: FinalAuditAreaKind
    name: str
    required: bool
    passed: bool
    status: FinalAuditStatus
    evidence: Optional[str]
    rationale: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "created_at_utc": self.created_at_utc,
            "area_kind": self.area_kind.value,
            "name": self.name,
            "required": self.required,
            "passed": self.passed,
            "status": self.status.value,
            "evidence": self.evidence,
            "rationale": self.rationale,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalSystemAuditChecklist:
    checklist_id: str
    created_at_utc: str
    items: List[FinalSystemAuditChecklistItem] = field(default_factory=list)
    item_count: int = 0
    passed_count: int = 0
    warning_count: int = 0
    failed_count: int = 0
    blocked_count: int = 0
    checklist_hash: Optional[str] = None
    checklist_valid: bool = False
    audit_ready: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
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
            "audit_ready": self.audit_ready,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalSystemAuditReport:
    audit_id: str
    created_at_utc: str
    checklist: FinalSystemAuditChecklist
    artifact_index: FinalArtifactIndex
    phase_lineage: FinalPhaseLineage
    audit_status: FinalAuditStatus
    audit_passed: bool
    audit_hash: Optional[str]
    not_deployment_approval: bool = True
    not_trading_approval: bool = True
    not_investment_advice: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "created_at_utc": self.created_at_utc,
            "checklist": self.checklist.to_dict(),
            "artifact_index": self.artifact_index.to_dict(),
            "phase_lineage": self.phase_lineage.to_dict(),
            "audit_status": self.audit_status.value,
            "audit_passed": self.audit_passed,
            "audit_hash": self.audit_hash,
            "not_deployment_approval": self.not_deployment_approval,
            "not_trading_approval": self.not_trading_approval,
            "not_investment_advice": self.not_investment_advice,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalSafetyClosure:
    closure_id: str
    created_at_utc: str
    no_live_trading: bool
    no_paper_state_mutation: bool
    no_broker_execution: bool
    no_real_order_creation: bool
    no_telegram_real_send: bool
    no_strategy_activation: bool
    no_deployment: bool
    no_production_patch: bool
    no_network: bool
    no_scraping: bool
    no_html_parsing: bool
    no_dashboard: bool
    no_daemon: bool
    no_scheduler: bool
    no_actual_target_weights: bool
    no_actual_allocation: bool
    no_order_size: bool
    no_capital_deployment: bool
    no_investment_advice: bool
    safety_closure_passed: bool
    closure_hash: Optional[str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "closure_id": self.closure_id,
            "created_at_utc": self.created_at_utc,
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
            "safety_closure_passed": self.safety_closure_passed,
            "closure_hash": self.closure_hash,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalLimitationRecord:
    limitation_id: str
    created_at_utc: str
    title: str
    description: str
    area_kind: FinalAuditAreaKind
    severity: str
    applies_to_final_delivery: bool
    not_blocking: bool
    mitigation_note: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "limitation_id": self.limitation_id,
            "created_at_utc": self.created_at_utc,
            "title": self.title,
            "description": self.description,
            "area_kind": self.area_kind.value,
            "severity": self.severity,
            "applies_to_final_delivery": self.applies_to_final_delivery,
            "not_blocking": self.not_blocking,
            "mitigation_note": self.mitigation_note,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalLimitationRegister:
    register_id: str
    created_at_utc: str
    limitations: List[FinalLimitationRecord] = field(default_factory=list)
    limitation_count: int = 0
    blocking_limitation_count: int = 0
    register_hash: Optional[str] = None
    register_valid: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "register_id": self.register_id,
            "created_at_utc": self.created_at_utc,
            "limitations": [l.to_dict() for l in self.limitations],
            "limitation_count": self.limitation_count,
            "blocking_limitation_count": self.blocking_limitation_count,
            "register_hash": self.register_hash,
            "register_valid": self.register_valid,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalDocumentationIndex:
    index_id: str
    created_at_utc: str
    doc_paths: List[str] = field(default_factory=list)
    required_docs: List[str] = field(default_factory=list)
    available_required_docs: List[str] = field(default_factory=list)
    missing_required_docs: List[str] = field(default_factory=list)
    index_hash: Optional[str] = None
    index_valid: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index_id": self.index_id,
            "created_at_utc": self.created_at_utc,
            "doc_paths": self.doc_paths,
            "required_docs": self.required_docs,
            "available_required_docs": self.available_required_docs,
            "missing_required_docs": self.missing_required_docs,
            "index_hash": self.index_hash,
            "index_valid": self.index_valid,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalRunbookIndex:
    index_id: str
    created_at_utc: str
    runbook_paths: List[str] = field(default_factory=list)
    required_runbooks: List[str] = field(default_factory=list)
    available_required_runbooks: List[str] = field(default_factory=list)
    missing_required_runbooks: List[str] = field(default_factory=list)
    index_hash: Optional[str] = None
    index_valid: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index_id": self.index_id,
            "created_at_utc": self.created_at_utc,
            "runbook_paths": self.runbook_paths,
            "required_runbooks": self.required_runbooks,
            "available_required_runbooks": self.available_required_runbooks,
            "missing_required_runbooks": self.missing_required_runbooks,
            "index_hash": self.index_hash,
            "index_valid": self.index_valid,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalTestEvidenceSummary:
    summary_id: str
    created_at_utc: str
    test_files: List[str] = field(default_factory=list)
    fixture_groups: List[str] = field(default_factory=list)
    expected_test_command: str = "pytest"
    tests_run_by_codex: bool = False
    tests_passed_by_codex: Optional[bool] = None
    summary_hash: Optional[str] = None
    summary_valid: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary_id": self.summary_id,
            "created_at_utc": self.created_at_utc,
            "test_files": self.test_files,
            "fixture_groups": self.fixture_groups,
            "expected_test_command": self.expected_test_command,
            "tests_run_by_codex": self.tests_run_by_codex,
            "tests_passed_by_codex": self.tests_passed_by_codex,
            "summary_hash": self.summary_hash,
            "summary_valid": self.summary_valid,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalQualityObservabilitySummary:
    summary_id: str
    created_at_utc: str
    quality_metrics: List[str] = field(default_factory=list)
    observability_metrics: List[str] = field(default_factory=list)
    acceptance_scores: List[str] = field(default_factory=list)
    summary_hash: Optional[str] = None
    summary_valid: bool = False
    no_network_export: bool = True
    no_external_push: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary_id": self.summary_id,
            "created_at_utc": self.created_at_utc,
            "quality_metrics": self.quality_metrics,
            "observability_metrics": self.observability_metrics,
            "acceptance_scores": self.acceptance_scores,
            "summary_hash": self.summary_hash,
            "summary_valid": self.summary_valid,
            "no_network_export": self.no_network_export,
            "no_external_push": self.no_external_push,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalDeliveryCertificate:
    certificate_id: str
    created_at_utc: str
    project_name: str
    total_phases: int
    final_phase: int
    source_audit_id: str
    source_safety_closure_id: str
    source_limitation_register_id: str
    delivered: bool
    delivery_status: ProjectClosureStatus
    certificate_hash: Optional[str] = None
    not_deployment_approval: bool = True
    not_trading_approval: bool = True
    not_broker_approval: bool = True
    not_investment_advice: bool = True
    limitations: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "certificate_id": self.certificate_id,
            "created_at_utc": self.created_at_utc,
            "project_name": self.project_name,
            "total_phases": self.total_phases,
            "final_phase": self.final_phase,
            "source_audit_id": self.source_audit_id,
            "source_safety_closure_id": self.source_safety_closure_id,
            "source_limitation_register_id": self.source_limitation_register_id,
            "delivered": self.delivered,
            "delivery_status": self.delivery_status.value,
            "certificate_hash": self.certificate_hash,
            "not_deployment_approval": self.not_deployment_approval,
            "not_trading_approval": self.not_trading_approval,
            "not_broker_approval": self.not_broker_approval,
            "not_investment_advice": self.not_investment_advice,
            "limitations": self.limitations,
            "next_steps": self.next_steps,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class ProjectClosureReport:
    report_id: str
    created_at_utc: str
    project_name: str
    total_phases: int
    final_delivery_certificate: FinalDeliveryCertificate
    final_audit_report: FinalSystemAuditReport
    final_safety_closure: FinalSafetyClosure
    limitation_register: FinalLimitationRegister
    documentation_index: FinalDocumentationIndex
    runbook_index: FinalRunbookIndex
    test_evidence_summary: FinalTestEvidenceSummary
    quality_observability_summary: FinalQualityObservabilitySummary
    closure_status: ProjectClosureStatus
    project_closed: bool
    report_hash: Optional[str] = None
    not_deployment_approval: bool = True
    not_trading_approval: bool = True
    not_investment_advice: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "created_at_utc": self.created_at_utc,
            "project_name": self.project_name,
            "total_phases": self.total_phases,
            "final_delivery_certificate": self.final_delivery_certificate.to_dict(),
            "final_audit_report": self.final_audit_report.to_dict(),
            "final_safety_closure": self.final_safety_closure.to_dict(),
            "limitation_register": self.limitation_register.to_dict(),
            "documentation_index": self.documentation_index.to_dict(),
            "runbook_index": self.runbook_index.to_dict(),
            "test_evidence_summary": self.test_evidence_summary.to_dict(),
            "quality_observability_summary": self.quality_observability_summary.to_dict(),
            "closure_status": self.closure_status.value,
            "project_closed": self.project_closed,
            "report_hash": self.report_hash,
            "not_deployment_approval": self.not_deployment_approval,
            "not_trading_approval": self.not_trading_approval,
            "not_investment_advice": self.not_investment_advice,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class ProjectClosureManifest:
    manifest_id: str
    created_at_utc: str
    project_name: str
    total_phases: int
    final_phase: int
    closure_report_id: str
    final_delivery_certificate_id: str
    final_review_id: Optional[str]
    manifest_hash: Optional[str]
    project_closed: bool
    closure_status: ProjectClosureStatus
    read_only: bool = True
    local_only: bool = True
    no_deployment: bool = True
    no_trading_activation: bool = True
    no_broker_activation: bool = True
    not_investment_advice: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "manifest_id": self.manifest_id,
            "created_at_utc": self.created_at_utc,
            "project_name": self.project_name,
            "total_phases": self.total_phases,
            "final_phase": self.final_phase,
            "closure_report_id": self.closure_report_id,
            "final_delivery_certificate_id": self.final_delivery_certificate_id,
            "final_review_id": self.final_review_id,
            "manifest_hash": self.manifest_hash,
            "project_closed": self.project_closed,
            "closure_status": self.closure_status.value,
            "read_only": self.read_only,
            "local_only": self.local_only,
            "no_deployment": self.no_deployment,
            "no_trading_activation": self.no_trading_activation,
            "no_broker_activation": self.no_broker_activation,
            "not_investment_advice": self.not_investment_advice,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalSafetyBoundaryRule:
    rule_id: str
    created_at_utc: str
    rule_kind: FinalSafetyRuleKind
    name: str
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    rationale: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "created_at_utc": self.created_at_utc,
            "rule_kind": self.rule_kind.value,
            "name": self.name,
            "required": self.required,
            "passed": self.passed,
            "expected_value": self.expected_value,
            "observed_value": self.observed_value,
            "rationale": self.rationale,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalSafetyBoundaryResult:
    boundary_id: str
    created_at_utc: str
    rules: List[FinalSafetyBoundaryRule] = field(default_factory=list)
    boundary_passed: bool = False
    final_audit_only: bool = True
    read_only_phase160_handoff: bool = True
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
    project_closure_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "boundary_id": self.boundary_id,
            "created_at_utc": self.created_at_utc,
            "rules": [r.to_dict() for r in self.rules],
            "boundary_passed": self.boundary_passed,
            "final_audit_only": self.final_audit_only,
            "read_only_phase160_handoff": self.read_only_phase160_handoff,
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
            "project_closure_only": self.project_closure_only,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalClosureReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: FinalClosureReadinessRuleKind
    name: str
    status: FinalClosureReadinessStatus
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    rationale: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "created_at_utc": self.created_at_utc,
            "rule_kind": self.rule_kind.value,
            "name": self.name,
            "status": self.status.value,
            "required": self.required,
            "passed": self.passed,
            "expected_value": self.expected_value,
            "observed_value": self.observed_value,
            "rationale": self.rationale,
            "warnings": self.warnings,
            "errors": self.errors,
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalClosureReadinessGate:
    gate_id: str
    created_at_utc: str
    status: FinalClosureReadinessStatus
    rules: List[FinalClosureReadinessRule] = field(default_factory=list)
    final_audit_report: Optional[FinalSystemAuditReport] = None
    final_delivery_certificate: Optional[FinalDeliveryCertificate] = None
    project_closure_report: Optional[ProjectClosureReport] = None
    project_closure_manifest: Optional[ProjectClosureManifest] = None
    final_safety_boundary: Optional[FinalSafetyBoundaryResult] = None
    project_closed: bool = False
    research_data_only: bool = True
    final_closure_only: bool = True
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
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "created_at_utc": self.created_at_utc,
            "status": self.status.value,
            "rules": [r.to_dict() for r in self.rules],
            "final_audit_report": self.final_audit_report.to_dict() if self.final_audit_report else None,
            "final_delivery_certificate": self.final_delivery_certificate.to_dict() if self.final_delivery_certificate else None,
            "project_closure_report": self.project_closure_report.to_dict() if self.project_closure_report else None,
            "project_closure_manifest": self.project_closure_manifest.to_dict() if self.project_closure_manifest else None,
            "final_safety_boundary": self.final_safety_boundary.to_dict() if self.final_safety_boundary else None,
            "project_closed": self.project_closed,
            "research_data_only": self.research_data_only,
            "final_closure_only": self.final_closure_only,
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
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalClosureContext:
    context_id: str
    created_at_utc: str
    status: FinalClosureStatus
    decision: FinalClosureDecision
    source_phase160_handoff_package_id: Optional[str] = None
    ingestion: Optional[Phase160HandoffIngestionResult] = None
    input_references: List[FinalInputReference] = field(default_factory=list)
    artifact_index: Optional[FinalArtifactIndex] = None
    phase_lineage: Optional[FinalPhaseLineage] = None
    final_audit_checklist: Optional[FinalSystemAuditChecklist] = None
    final_audit_report: Optional[FinalSystemAuditReport] = None
    final_safety_closure: Optional[FinalSafetyClosure] = None
    limitation_register: Optional[FinalLimitationRegister] = None
    documentation_index: Optional[FinalDocumentationIndex] = None
    runbook_index: Optional[FinalRunbookIndex] = None
    test_evidence_summary: Optional[FinalTestEvidenceSummary] = None
    quality_observability_summary: Optional[FinalQualityObservabilitySummary] = None
    final_delivery_certificate: Optional[FinalDeliveryCertificate] = None
    project_closure_report: Optional[ProjectClosureReport] = None
    project_closure_manifest: Optional[ProjectClosureManifest] = None
    final_safety_boundary: Optional[FinalSafetyBoundaryResult] = None
    final_closure_readiness_gate: Optional[FinalClosureReadinessGate] = None
    phase160_handoff_ingested: bool = False
    artifacts_loaded: bool = False
    inputs_resolved: bool = False
    final_artifact_index_built: bool = False
    final_phase_lineage_built: bool = False
    final_system_audit_checklist_built: bool = False
    final_system_audit_report_built: bool = False
    final_safety_closure_built: bool = False
    final_limitation_register_built: bool = False
    final_documentation_index_built: bool = False
    final_runbook_index_built: bool = False
    final_test_evidence_summary_built: bool = False
    final_quality_observability_summary_built: bool = False
    final_delivery_certificate_built: bool = False
    project_closure_report_built: bool = False
    project_closure_manifest_built: bool = False
    final_safety_boundary_validated: bool = False
    final_closure_readiness_gate_built: bool = False
    final_closure_readiness_gate_passed: bool = False
    project_closed: bool = False
    research_data_only: bool = True
    final_closure_only: bool = True
    read_only: bool = True
    local_only: bool = True
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
    risk_flags: List[FinalClosureRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "context_id": self.context_id,
            "created_at_utc": self.created_at_utc,
            "status": self.status.value,
            "decision": self.decision.value,
            "source_phase160_handoff_package_id": self.source_phase160_handoff_package_id,
            "ingestion": self.ingestion.to_dict() if self.ingestion else None,
            "input_references": [i.to_dict() for i in self.input_references],
            "artifact_index": self.artifact_index.to_dict() if self.artifact_index else None,
            "phase_lineage": self.phase_lineage.to_dict() if self.phase_lineage else None,
            "final_audit_checklist": self.final_audit_checklist.to_dict() if self.final_audit_checklist else None,
            "final_audit_report": self.final_audit_report.to_dict() if self.final_audit_report else None,
            "final_safety_closure": self.final_safety_closure.to_dict() if self.final_safety_closure else None,
            "limitation_register": self.limitation_register.to_dict() if self.limitation_register else None,
            "documentation_index": self.documentation_index.to_dict() if self.documentation_index else None,
            "runbook_index": self.runbook_index.to_dict() if self.runbook_index else None,
            "test_evidence_summary": self.test_evidence_summary.to_dict() if self.test_evidence_summary else None,
            "quality_observability_summary": self.quality_observability_summary.to_dict() if self.quality_observability_summary else None,
            "final_delivery_certificate": self.final_delivery_certificate.to_dict() if self.final_delivery_certificate else None,
            "project_closure_report": self.project_closure_report.to_dict() if self.project_closure_report else None,
            "project_closure_manifest": self.project_closure_manifest.to_dict() if self.project_closure_manifest else None,
            "final_safety_boundary": self.final_safety_boundary.to_dict() if self.final_safety_boundary else None,
            "final_closure_readiness_gate": self.final_closure_readiness_gate.to_dict() if self.final_closure_readiness_gate else None,
            "phase160_handoff_ingested": self.phase160_handoff_ingested,
            "artifacts_loaded": self.artifacts_loaded,
            "inputs_resolved": self.inputs_resolved,
            "final_artifact_index_built": self.final_artifact_index_built,
            "final_phase_lineage_built": self.final_phase_lineage_built,
            "final_system_audit_checklist_built": self.final_system_audit_checklist_built,
            "final_system_audit_report_built": self.final_system_audit_report_built,
            "final_safety_closure_built": self.final_safety_closure_built,
            "final_limitation_register_built": self.final_limitation_register_built,
            "final_documentation_index_built": self.final_documentation_index_built,
            "final_runbook_index_built": self.final_runbook_index_built,
            "final_test_evidence_summary_built": self.final_test_evidence_summary_built,
            "final_quality_observability_summary_built": self.final_quality_observability_summary_built,
            "final_delivery_certificate_built": self.final_delivery_certificate_built,
            "project_closure_report_built": self.project_closure_report_built,
            "project_closure_manifest_built": self.project_closure_manifest_built,
            "final_safety_boundary_validated": self.final_safety_boundary_validated,
            "final_closure_readiness_gate_built": self.final_closure_readiness_gate_built,
            "final_closure_readiness_gate_passed": self.final_closure_readiness_gate_passed,
            "project_closed": self.project_closed,
            "research_data_only": self.research_data_only,
            "final_closure_only": self.final_closure_only,
            "read_only": self.read_only,
            "local_only": self.local_only,
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
            "risk_flags": [rf.value for rf in self.risk_flags],
            "metadata": self.metadata,
        }

@dataclass
class FinalClosureFullReview:
    review_id: str
    created_at_utc: str
    report_type: FinalClosureReportType
    ingestion: Phase160HandoffIngestionResult
    context: FinalClosureContext
    final_audit_report: FinalSystemAuditReport
    final_delivery_certificate: FinalDeliveryCertificate
    project_closure_report: ProjectClosureReport
    project_closure_manifest: ProjectClosureManifest
    final_closure_readiness_gate: FinalClosureReadinessGate
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "review_id": self.review_id,
            "created_at_utc": self.created_at_utc,
            "report_type": self.report_type.value,
            "ingestion": self.ingestion.to_dict(),
            "context": self.context.to_dict(),
            "final_audit_report": self.final_audit_report.to_dict(),
            "final_delivery_certificate": self.final_delivery_certificate.to_dict(),
            "project_closure_report": self.project_closure_report.to_dict(),
            "project_closure_manifest": self.project_closure_manifest.to_dict(),
            "final_closure_readiness_gate": self.final_closure_readiness_gate.to_dict(),
            "output_paths": self.output_paths,
            "warnings": self.warnings,
            "errors": self.errors,
        }
