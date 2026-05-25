
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import *

@dataclass
class EventImpactIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    event_impact_ready: bool
    macro_regime_metadata_ready: bool
    calendar_aware_validation_ready: bool
    metadata_only: bool
    research_context_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    valid_for_phase113: bool
    risk_flags: List[ProviderGovernanceRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class ProviderExpansionEvidenceItem:
    evidence_id: str
    created_at_utc: str
    source_phase: int
    evidence_name: str
    criterion_kind: ProviderAcceptanceCriterionKind
    source_review_id: Optional[str]
    source_path: Optional[str]
    available: bool
    valid: bool
    metadata_only: bool
    no_execution_confirmed: bool
    no_scraping_confirmed: bool
    no_paid_api_confirmed: bool
    no_broker_order_confirmed: bool
    artifact_hash: Optional[str]
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ProviderAcceptanceCriterion:
    criterion_id: str
    created_at_utc: str
    criterion_kind: ProviderAcceptanceCriterionKind
    name: str
    status: ProviderAcceptanceStatus
    required: bool
    passed: bool
    evidence_ids: List[str]
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ProviderAcceptanceReport:
    report_id: str
    created_at_utc: str
    status: ProviderAcceptanceStatus
    criteria: List[ProviderAcceptanceCriterion]
    total_criteria: int
    passed_criteria: int
    warning_criteria: int
    failed_criteria: int
    blocked_criteria: int
    provider_expansion_accepted: bool
    metadata_only_acceptance: bool
    no_execution_confirmed: bool
    no_scraping_confirmed: bool
    no_paid_api_confirmed: bool
    no_broker_order_confirmed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ProviderGovernanceRule:
    rule_id: str
    created_at_utc: str
    rule_kind: ProviderGovernanceRuleKind
    name: str
    status: ProviderGovernanceRuleStatus
    required: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    passed: bool
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ProviderGovernancePolicy:
    policy_id: str
    created_at_utc: str
    status: ProviderGovernanceStatus
    rules: List[ProviderGovernanceRule]
    free_source_only: bool
    no_scraping: bool
    no_html_parsing: bool
    no_paid_api: bool
    no_broker: bool
    no_order: bool
    no_paper_mutation: bool
    no_telegram_real_send: bool
    no_dashboard: bool
    no_trade_signal_from_data_layer: bool
    require_lineage: bool
    require_audit_manifest: bool
    require_no_secrets: bool
    policy_valid: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class DataLineageNode:
    node_id: str
    created_at_utc: str
    node_kind: DataLineageNodeKind
    label: str
    source_phase: Optional[int]
    source_ref_id: Optional[str]
    artifact_path: Optional[str]
    artifact_hash: Optional[str]
    metadata_only: bool
    contains_secret: bool
    contains_trade_signal: bool
    contains_order_decision: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class DataLineageEdge:
    edge_id: str
    created_at_utc: str
    edge_kind: DataLineageEdgeKind
    source_node_id: str
    target_node_id: str
    label: str
    valid: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class DataLineageGraph:
    graph_id: str
    created_at_utc: str
    nodes: List[DataLineageNode]
    edges: List[DataLineageEdge]
    total_nodes: int
    total_edges: int
    graph_valid: bool
    missing_required_node_count: int
    invalid_edge_count: int
    secret_node_count: int
    trade_signal_node_count: int
    order_decision_node_count: int
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class AuditTrailEvent:
    audit_event_id: str
    created_at_utc: str
    event_kind: AuditTrailEventKind
    source_phase: Optional[int]
    source_ref_id: Optional[str]
    message: str
    artifact_path: Optional[str]
    artifact_hash: Optional[str]
    metadata_only: bool
    contains_secret: bool
    contains_execution: bool
    contains_order: bool
    contains_trade_signal: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class AuditArtifactManifest:
    manifest_id: str
    created_at_utc: str
    status: AuditArtifactStatus
    artifacts: List[Dict[str, Any]]
    audit_events: List[AuditTrailEvent]
    total_artifacts: int
    hashed_artifacts: int
    missing_artifacts: int
    secret_violation_count: int
    execution_violation_count: int
    order_violation_count: int
    trade_signal_violation_count: int
    manifest_valid: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class NoExecutionProof:
    proof_id: str
    created_at_utc: str
    provider_expansion_phases: List[int]
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    scraping_used: bool
    html_parsing_used: bool
    paid_api_used: bool
    dashboard_started: bool
    network_fetch_default_enabled: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    proof_valid: bool
    evidence_ids: List[str]
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ProviderGovernanceContext:
    context_id: str
    created_at_utc: str
    status: ProviderGovernanceStatus
    decision: ProviderGovernanceDecision
    source_event_impact_review_id: Optional[str]
    ingestion: EventImpactIngestionResult
    evidence_items: List[ProviderExpansionEvidenceItem]
    acceptance_report: ProviderAcceptanceReport
    governance_policy: ProviderGovernancePolicy
    lineage_graph: DataLineageGraph
    audit_manifest: AuditArtifactManifest
    no_execution_proof: NoExecutionProof
    provider_governance_ready: bool
    provider_expansion_accepted: bool
    lineage_ready: bool
    audit_ready: bool
    metadata_only: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
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
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ProviderGovernanceFullReview:
    review_id: str
    created_at_utc: str
    report_type: ProviderGovernanceReportType
    ingestion: EventImpactIngestionResult
    context: ProviderGovernanceContext
    evidence_items: List[ProviderExpansionEvidenceItem]
    acceptance_report: ProviderAcceptanceReport
    governance_policy: ProviderGovernancePolicy
    lineage_graph: DataLineageGraph
    audit_manifest: AuditArtifactManifest
    no_execution_proof: NoExecutionProof
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

# IDs
def create_event_impact_ingestion_id() -> str: return str(uuid.uuid4())
def create_provider_expansion_evidence_id() -> str: return str(uuid.uuid4())
def create_provider_acceptance_criterion_id() -> str: return str(uuid.uuid4())
def create_provider_acceptance_report_id() -> str: return str(uuid.uuid4())
def create_provider_governance_rule_id() -> str: return str(uuid.uuid4())
def create_provider_governance_policy_id() -> str: return str(uuid.uuid4())
def create_data_lineage_node_id() -> str: return str(uuid.uuid4())
def create_data_lineage_edge_id() -> str: return str(uuid.uuid4())
def create_data_lineage_graph_id() -> str: return str(uuid.uuid4())
def create_audit_trail_event_id() -> str: return str(uuid.uuid4())
def create_audit_artifact_manifest_id() -> str: return str(uuid.uuid4())
def create_no_execution_proof_id() -> str: return str(uuid.uuid4())
def create_provider_governance_context_id() -> str: return str(uuid.uuid4())
def create_provider_governance_full_review_id() -> str: return str(uuid.uuid4())
