from dataclasses import dataclass, field
from typing import Any
import uuid
import datetime
from usa_signal_bot.core.enums import (
    BacktestClosureStatus, BacktestClosureDecision, BacktestBandPhase,
    ClosureArtifactKind, ClosureAuditKind, ClosureComplianceStatus,
    BacktestClosureQuality, BacktestMetricInventoryKind, BacktestRiskNoteKind,
    Phase153HandoffItemKind, HandoffSafetyRuleKind, Phase153ReadinessStatus,
    Phase153ReadinessRuleKind, BacktestClosureRiskFlag, BacktestClosureReportType
)

def _now(): return datetime.datetime.utcnow().isoformat() + "Z"
def _uid(): return str(uuid.uuid4())

@dataclass
class StressRobustnessIngestionResult:
    ingestion_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    source_path: str | None = None
    source_review_id: str | None = None
    source_context_id: str | None = None
    available: bool = False
    walk_forward_ingested: bool = False
    scenario_policy_built: bool = False
    scenario_replays_built: bool = False
    scenario_metrics_built: bool = False
    cost_liquidity_sensitivity_built: bool = False
    monte_carlo_policy_built: bool = False
    monte_carlo_paths_built: bool = False
    monte_carlo_replays_built: bool = False
    monte_carlo_distributions_built: bool = False
    tail_risk_diagnostics_built: bool = False
    robustness_scorecard_built: bool = False
    stress_validation_report_built: bool = False
    monte_carlo_robustness_report_built: bool = False
    safety_boundary_validated: bool = False
    phase152_readiness_gate_built: bool = False
    phase152_readiness_gate_passed: bool = False
    ready_for_phase152: bool = False
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    deterministic: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    strategy_activation_allowed: bool = False
    portfolio_optimization_enabled: bool = False
    portfolio_allocation_output_enabled: bool = False
    deployment_allowed: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    dashboard_started: bool = False
    daemon_started: bool = False
    scheduler_enabled: bool = False
    stress_test_executed: bool = False
    monte_carlo_executed: bool = False
    produces_live_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    valid_for_phase152: bool = False
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ClosureArtifactReference:
    artifact_ref_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    phase: BacktestBandPhase = BacktestBandPhase.UNKNOWN
    artifact_kind: ClosureArtifactKind = ClosureArtifactKind.UNKNOWN
    artifact_name: str = ""
    source_path: str | None = None
    source_hash: str | None = None
    available: bool = False
    read_only: bool = True
    required: bool = True
    valid: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ArtifactLineageManifest:
    manifest_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    artifacts: list[ClosureArtifactReference] = field(default_factory=list)
    phase_order: list[BacktestBandPhase] = field(default_factory=list)
    lineage_hash: str | None = None
    manifest_valid: bool = False
    all_required_available: bool = False
    deterministic_hashes_available: bool = False
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ClosureAuditCheck:
    check_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    audit_kind: ClosureAuditKind = ClosureAuditKind.UNKNOWN
    name: str = ""
    status: ClosureComplianceStatus = ClosureComplianceStatus.NOT_CHECKED
    required: bool = True
    passed: bool = False
    expected_value: Any | None = None
    observed_value: Any | None = None
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ArtifactAvailabilityAudit:
    audit_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    checks: list[ClosureAuditCheck] = field(default_factory=list)
    audit_passed: bool = False
    required_artifact_count: int = 0
    available_artifact_count: int = 0
    missing_artifact_count: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DeterminismComplianceAudit:
    audit_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    checks: list[ClosureAuditCheck] = field(default_factory=list)
    audit_passed: bool = False
    deterministic_artifact_count: int = 0
    non_deterministic_artifact_count: int = 0
    all_hashes_consistent: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SafetyComplianceAudit:
    audit_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    checks: list[ClosureAuditCheck] = field(default_factory=list)
    audit_passed: bool = False
    no_live_trading: bool = True
    no_paper_trading: bool = True
    no_broker_execution: bool = True
    no_real_order_creation: bool = True
    no_paper_state_mutation: bool = True
    no_telegram_real_send: bool = True
    no_strategy_activation: bool = True
    no_portfolio_output: bool = True
    no_deployment: bool = True
    no_network: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ResearchBoundaryAudit:
    audit_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    checks: list[ClosureAuditCheck] = field(default_factory=list)
    audit_passed: bool = False
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    no_investment_advice: bool = True
    no_live_signal: bool = True
    no_order_decision: bool = True
    no_portfolio_weights: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestMetricInventoryItem:
    item_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    metric_kind: BacktestMetricInventoryKind = BacktestMetricInventoryKind.UNKNOWN
    metric_name: str = ""
    source_phase: BacktestBandPhase = BacktestBandPhase.UNKNOWN
    source_artifact: str = ""
    value: float | int | str | None = None
    sample_count: int | None = None
    non_trading_metric: bool = True
    not_investment_advice: bool = True
    suitable_for_phase153_research_input: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestRiskNote:
    note_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    note_kind: BacktestRiskNoteKind = BacktestRiskNoteKind.UNKNOWN
    source_phase: BacktestBandPhase = BacktestBandPhase.UNKNOWN
    title: str = ""
    note: str = ""
    severity: str = "INFO"
    suitable_for_phase153_research_input: bool = True
    not_investment_advice: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RobustnessEvidenceRecord:
    evidence_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    source_phase: BacktestBandPhase = BacktestBandPhase.UNKNOWN
    evidence_name: str = ""
    evidence_value: float | int | str | None = None
    evidence_status: ClosureComplianceStatus = ClosureComplianceStatus.NOT_CHECKED
    supports_closure: bool = False
    supports_phase153_handoff: bool = False
    limitations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class AcceptanceSummary:
    summary_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    checks: list[ClosureAuditCheck] = field(default_factory=list)
    acceptance_passed: bool = False
    passed_count: int = 0
    warning_count: int = 0
    failed_count: int = 0
    blocked_count: int = 0
    quality: BacktestClosureQuality = BacktestClosureQuality.UNKNOWN
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ClosureBlocker:
    blocker_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    blocker_name: str = ""
    blocker_detected: bool = False
    severity: str = "CRITICAL"
    message: str = ""
    source_phase: BacktestBandPhase | None = None
    risk_flag: BacktestClosureRiskFlag = BacktestClosureRiskFlag.UNKNOWN
    resolution_hint: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestFinalAuditReport:
    report_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    artifact_lineage: ArtifactLineageManifest = field(default_factory=ArtifactLineageManifest)
    availability_audit: ArtifactAvailabilityAudit = field(default_factory=ArtifactAvailabilityAudit)
    determinism_audit: DeterminismComplianceAudit = field(default_factory=DeterminismComplianceAudit)
    safety_audit: SafetyComplianceAudit = field(default_factory=SafetyComplianceAudit)
    research_boundary_audit: ResearchBoundaryAudit = field(default_factory=ResearchBoundaryAudit)
    metric_inventory: list[BacktestMetricInventoryItem] = field(default_factory=list)
    risk_notes: list[BacktestRiskNote] = field(default_factory=list)
    robustness_evidence: list[RobustnessEvidenceRecord] = field(default_factory=list)
    acceptance_summary: AcceptanceSummary = field(default_factory=AcceptanceSummary)
    blockers: list[ClosureBlocker] = field(default_factory=list)
    report_hash: str | None = None
    report_valid: bool = False
    final_audit_passed: bool = False
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    no_live_trading: bool = True
    no_paper_trading: bool = True
    no_broker_execution: bool = True
    no_portfolio_output: bool = True
    no_deployment: bool = True
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestBandClosureCertificate:
    certificate_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    band_name: str = "Realistic Backtest Band"
    start_phase: int = 146
    end_phase: int = 152
    closed: bool = False
    closure_status: ClosureComplianceStatus = ClosureComplianceStatus.NOT_CHECKED
    final_audit_report_id: str = ""
    acceptance_summary_id: str = ""
    closure_hash: str | None = None
    limitations: list[str] = field(default_factory=list)
    next_phase: int = 153
    ready_for_phase153: bool = False
    not_deployment_approval: bool = True
    not_strategy_activation: bool = True
    not_investment_advice: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Phase153HandoffContract:
    contract_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    source_certificate_id: str = ""
    source_final_audit_report_id: str = ""
    allowed_item_kinds: list[Phase153HandoffItemKind] = field(default_factory=list)
    forbidden_fields: list[str] = field(default_factory=list)
    read_only: bool = True
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    portfolio_construction_allowed: bool = False
    position_sizing_allowed: bool = False
    target_weights_allowed: bool = False
    allocation_output_allowed: bool = False
    capital_deployment_allowed: bool = False
    broker_execution_allowed: bool = False
    paper_trading_allowed: bool = False
    live_trading_allowed: bool = False
    contract_valid: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Phase153HandoffItem:
    item_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    item_kind: Phase153HandoffItemKind = Phase153HandoffItemKind.UNKNOWN
    source_phase: BacktestBandPhase = BacktestBandPhase.UNKNOWN
    name: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    read_only: bool = True
    research_data_only: bool = True
    contains_portfolio_weight: bool = False
    contains_position_size: bool = False
    contains_allocation: bool = False
    contains_order: bool = False
    contains_live_signal: bool = False
    not_investment_advice: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Phase153HandoffPackage:
    package_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    contract: Phase153HandoffContract = field(default_factory=Phase153HandoffContract)
    items: list[Phase153HandoffItem] = field(default_factory=list)
    source_certificate: BacktestBandClosureCertificate = field(default_factory=BacktestBandClosureCertificate)
    package_hash: str | None = None
    package_valid: bool = False
    read_only: bool = True
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    portfolio_construction_executed: bool = False
    position_sizing_executed: bool = False
    target_weights_produced: bool = False
    allocation_output_produced: bool = False
    capital_deployment_allowed: bool = False
    broker_execution_enabled: bool = False
    paper_trading_enabled: bool = False
    live_trading_enabled: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class HandoffSafetyBoundaryRule:
    rule_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    rule_kind: HandoffSafetyRuleKind = HandoffSafetyRuleKind.UNKNOWN
    name: str = ""
    required: bool = True
    passed: bool = False
    expected_value: Any | None = None
    observed_value: Any | None = None
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class HandoffSafetyBoundaryResult:
    boundary_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    rules: list[HandoffSafetyBoundaryRule] = field(default_factory=list)
    boundary_passed: bool = False
    read_only_handoff_only: bool = True
    no_portfolio_construction: bool = True
    no_position_sizing: bool = True
    no_target_weights: bool = True
    no_allocation_output: bool = True
    no_capital_deployment: bool = True
    no_live_trading: bool = True
    no_paper_trading: bool = True
    no_broker_execution: bool = True
    no_real_order_creation: bool = True
    no_paper_state_mutation: bool = True
    no_telegram_real_send: bool = True
    no_strategy_activation: bool = True
    no_deployment: bool = True
    no_network: bool = True
    no_dashboard: bool = True
    no_daemon: bool = True
    no_scheduler: bool = True
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Phase153ReadinessRule:
    rule_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    rule_kind: Phase153ReadinessRuleKind = Phase153ReadinessRuleKind.UNKNOWN
    name: str = ""
    status: Phase153ReadinessStatus = Phase153ReadinessStatus.NOT_CHECKED
    required: bool = True
    passed: bool = False
    expected_value: Any | None = None
    observed_value: Any | None = None
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Phase153ReadinessGate:
    gate_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    status: Phase153ReadinessStatus = Phase153ReadinessStatus.NOT_CHECKED
    rules: list[Phase153ReadinessRule] = field(default_factory=list)
    final_audit_report: BacktestFinalAuditReport = field(default_factory=BacktestFinalAuditReport)
    closure_certificate: BacktestBandClosureCertificate = field(default_factory=BacktestBandClosureCertificate)
    handoff_contract: Phase153HandoffContract = field(default_factory=Phase153HandoffContract)
    handoff_package: Phase153HandoffPackage = field(default_factory=Phase153HandoffPackage)
    handoff_safety_boundary: HandoffSafetyBoundaryResult = field(default_factory=HandoffSafetyBoundaryResult)
    ready_for_phase153: bool = False
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    portfolio_construction_executed: bool = False
    position_sizing_executed: bool = False
    target_weights_produced: bool = False
    allocation_output_produced: bool = False
    deployment_allowed: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestClosureContext:
    context_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    status: BacktestClosureStatus = BacktestClosureStatus.DRAFT
    decision: BacktestClosureDecision = BacktestClosureDecision.UNKNOWN
    source_stress_robustness_review_id: str | None = None
    ingestion: StressRobustnessIngestionResult = field(default_factory=StressRobustnessIngestionResult)
    artifact_lineage: ArtifactLineageManifest = field(default_factory=ArtifactLineageManifest)
    availability_audit: ArtifactAvailabilityAudit = field(default_factory=ArtifactAvailabilityAudit)
    determinism_audit: DeterminismComplianceAudit = field(default_factory=DeterminismComplianceAudit)
    safety_audit: SafetyComplianceAudit = field(default_factory=SafetyComplianceAudit)
    research_boundary_audit: ResearchBoundaryAudit = field(default_factory=ResearchBoundaryAudit)
    final_audit_report: BacktestFinalAuditReport = field(default_factory=BacktestFinalAuditReport)
    closure_certificate: BacktestBandClosureCertificate = field(default_factory=BacktestBandClosureCertificate)
    handoff_contract: Phase153HandoffContract = field(default_factory=Phase153HandoffContract)
    handoff_package: Phase153HandoffPackage = field(default_factory=Phase153HandoffPackage)
    handoff_safety_boundary: HandoffSafetyBoundaryResult = field(default_factory=HandoffSafetyBoundaryResult)
    phase153_readiness_gate: Phase153ReadinessGate = field(default_factory=Phase153ReadinessGate)
    stress_robustness_ingested: bool = False
    cross_phase_artifacts_loaded: bool = False
    artifact_lineage_built: bool = False
    artifact_availability_audited: bool = False
    determinism_compliance_audited: bool = False
    safety_compliance_audited: bool = False
    research_boundary_audited: bool = False
    metric_inventory_built: bool = False
    risk_note_inventory_built: bool = False
    robustness_evidence_built: bool = False
    acceptance_summary_built: bool = False
    closure_blockers_checked: bool = False
    closure_warnings_collected: bool = False
    final_audit_report_built: bool = False
    band_closure_certificate_built: bool = False
    phase153_handoff_contract_built: bool = False
    phase153_handoff_package_built: bool = False
    handoff_safety_boundary_validated: bool = False
    phase153_readiness_gate_built: bool = False
    phase153_readiness_gate_passed: bool = False
    ready_for_phase153: bool = False
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    deterministic: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    strategy_activation_allowed: bool = False
    portfolio_construction_executed: bool = False
    position_sizing_executed: bool = False
    portfolio_optimization_enabled: bool = False
    portfolio_allocation_output_enabled: bool = False
    target_weights_produced: bool = False
    deployment_allowed: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    dashboard_started: bool = False
    daemon_started: bool = False
    scheduler_enabled: bool = False
    produces_live_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestClosureRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestClosureFullReview:
    review_id: str = field(default_factory=_uid)
    created_at_utc: str = field(default_factory=_now)
    report_type: BacktestClosureReportType = BacktestClosureReportType.FULL_PHASE152_REVIEW
    ingestion: StressRobustnessIngestionResult = field(default_factory=StressRobustnessIngestionResult)
    context: BacktestClosureContext = field(default_factory=BacktestClosureContext)
    final_audit_report: BacktestFinalAuditReport = field(default_factory=BacktestFinalAuditReport)
    closure_certificate: BacktestBandClosureCertificate = field(default_factory=BacktestBandClosureCertificate)
    handoff_contract: Phase153HandoffContract = field(default_factory=Phase153HandoffContract)
    handoff_package: Phase153HandoffPackage = field(default_factory=Phase153HandoffPackage)
    handoff_safety_boundary: HandoffSafetyBoundaryResult = field(default_factory=HandoffSafetyBoundaryResult)
    phase153_readiness_gate: Phase153ReadinessGate = field(default_factory=Phase153ReadinessGate)
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
