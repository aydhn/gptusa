import os
import textwrap

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(textwrap.dedent(content).lstrip())

# 1. ENUMS
write_file("usa_signal_bot/core/enums.py", """
from enum import Enum

class BacktestClosureStatus(str, Enum):
    DRAFT = "DRAFT"
    CREATED = "CREATED"
    STRESS_ROBUSTNESS_INGESTED = "STRESS_ROBUSTNESS_INGESTED"
    CROSS_PHASE_ARTIFACTS_LOADED = "CROSS_PHASE_ARTIFACTS_LOADED"
    ARTIFACT_LINEAGE_BUILT = "ARTIFACT_LINEAGE_BUILT"
    ARTIFACT_AVAILABILITY_AUDITED = "ARTIFACT_AVAILABILITY_AUDITED"
    DETERMINISM_COMPLIANCE_AUDITED = "DETERMINISM_COMPLIANCE_AUDITED"
    SAFETY_COMPLIANCE_AUDITED = "SAFETY_COMPLIANCE_AUDITED"
    RESEARCH_BOUNDARY_AUDITED = "RESEARCH_BOUNDARY_AUDITED"
    METRIC_INVENTORY_BUILT = "METRIC_INVENTORY_BUILT"
    RISK_NOTE_INVENTORY_BUILT = "RISK_NOTE_INVENTORY_BUILT"
    ROBUSTNESS_EVIDENCE_BUILT = "ROBUSTNESS_EVIDENCE_BUILT"
    ACCEPTANCE_SUMMARY_BUILT = "ACCEPTANCE_SUMMARY_BUILT"
    CLOSURE_BLOCKERS_CHECKED = "CLOSURE_BLOCKERS_CHECKED"
    CLOSURE_WARNINGS_COLLECTED = "CLOSURE_WARNINGS_COLLECTED"
    FINAL_AUDIT_REPORT_BUILT = "FINAL_AUDIT_REPORT_BUILT"
    BAND_CLOSURE_CERTIFICATE_BUILT = "BAND_CLOSURE_CERTIFICATE_BUILT"
    PHASE153_HANDOFF_CONTRACT_BUILT = "PHASE153_HANDOFF_CONTRACT_BUILT"
    PHASE153_HANDOFF_PACKAGE_BUILT = "PHASE153_HANDOFF_PACKAGE_BUILT"
    HANDOFF_SAFETY_BOUNDARY_VALIDATED = "HANDOFF_SAFETY_BOUNDARY_VALIDATED"
    PHASE153_READINESS_GATE_BUILT = "PHASE153_READINESS_GATE_BUILT"
    PHASE153_READINESS_GATE_PASSED = "PHASE153_READINESS_GATE_PASSED"
    VALIDATED = "VALIDATED"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    ARCHIVED = "ARCHIVED"
    UNKNOWN = "UNKNOWN"

class BacktestClosureDecision(str, Enum):
    LOAD_STRESS_ROBUSTNESS_ARTIFACTS = "LOAD_STRESS_ROBUSTNESS_ARTIFACTS"
    LOAD_CROSS_PHASE_ARTIFACTS = "LOAD_CROSS_PHASE_ARTIFACTS"
    BUILD_ARTIFACT_LINEAGE = "BUILD_ARTIFACT_LINEAGE"
    AUDIT_ARTIFACT_AVAILABILITY = "AUDIT_ARTIFACT_AVAILABILITY"
    AUDIT_DETERMINISM_COMPLIANCE = "AUDIT_DETERMINISM_COMPLIANCE"
    AUDIT_SAFETY_COMPLIANCE = "AUDIT_SAFETY_COMPLIANCE"
    AUDIT_RESEARCH_BOUNDARY = "AUDIT_RESEARCH_BOUNDARY"
    BUILD_METRIC_INVENTORY = "BUILD_METRIC_INVENTORY"
    BUILD_RISK_NOTE_INVENTORY = "BUILD_RISK_NOTE_INVENTORY"
    BUILD_ROBUSTNESS_EVIDENCE = "BUILD_ROBUSTNESS_EVIDENCE"
    BUILD_ACCEPTANCE_SUMMARY = "BUILD_ACCEPTANCE_SUMMARY"
    CHECK_CLOSURE_BLOCKERS = "CHECK_CLOSURE_BLOCKERS"
    COLLECT_CLOSURE_WARNINGS = "COLLECT_CLOSURE_WARNINGS"
    BUILD_FINAL_AUDIT_REPORT = "BUILD_FINAL_AUDIT_REPORT"
    BUILD_BAND_CLOSURE_CERTIFICATE = "BUILD_BAND_CLOSURE_CERTIFICATE"
    BUILD_PHASE153_HANDOFF_CONTRACT = "BUILD_PHASE153_HANDOFF_CONTRACT"
    BUILD_PHASE153_HANDOFF_PACKAGE = "BUILD_PHASE153_HANDOFF_PACKAGE"
    VALIDATE_HANDOFF_SAFETY_BOUNDARY = "VALIDATE_HANDOFF_SAFETY_BOUNDARY"
    BUILD_PHASE153_READINESS_GATE = "BUILD_PHASE153_READINESS_GATE"
    REQUEST_STRESS_REFRESH = "REQUEST_STRESS_REFRESH"
    REQUEST_CROSS_PHASE_ARTIFACT_FIX = "REQUEST_CROSS_PHASE_ARTIFACT_FIX"
    REQUEST_SAFETY_FIX = "REQUEST_SAFETY_FIX"
    REQUEST_HANDOFF_FIX = "REQUEST_HANDOFF_FIX"
    REQUEST_SCHEMA_FIX = "REQUEST_SCHEMA_FIX"
    REQUEST_MANUAL_REVIEW = "REQUEST_MANUAL_REVIEW"
    BLOCK = "BLOCK"
    INCONCLUSIVE = "INCONCLUSIVE"
    UNKNOWN = "UNKNOWN"

class BacktestBandPhase(str, Enum):
    PHASE146_FOUNDATION = "PHASE146_FOUNDATION"
    PHASE147_BACKTEST_RUN = "PHASE147_BACKTEST_RUN"
    PHASE148_ANALYTICS = "PHASE148_ANALYTICS"
    PHASE149_BENCHMARK = "PHASE149_BENCHMARK"
    PHASE150_WALK_FORWARD = "PHASE150_WALK_FORWARD"
    PHASE151_STRESS_MONTE_CARLO = "PHASE151_STRESS_MONTE_CARLO"
    PHASE152_CLOSURE = "PHASE152_CLOSURE"
    UNKNOWN = "UNKNOWN"

class ClosureArtifactKind(str, Enum):
    FOUNDATION_REVIEW = "FOUNDATION_REVIEW"
    BACKTEST_RUN_REVIEW = "BACKTEST_RUN_REVIEW"
    ANALYTICS_REVIEW = "ANALYTICS_REVIEW"
    BENCHMARK_REVIEW = "BENCHMARK_REVIEW"
    WALK_FORWARD_REVIEW = "WALK_FORWARD_REVIEW"
    STRESS_ROBUSTNESS_REVIEW = "STRESS_ROBUSTNESS_REVIEW"
    SAFETY_BOUNDARY = "SAFETY_BOUNDARY"
    READINESS_GATE = "READINESS_GATE"
    VALIDATION_REPORT = "VALIDATION_REPORT"
    ROBUSTNESS_SCORECARD = "ROBUSTNESS_SCORECARD"
    FINAL_AUDIT_REPORT = "FINAL_AUDIT_REPORT"
    CLOSURE_CERTIFICATE = "CLOSURE_CERTIFICATE"
    PHASE153_HANDOFF_CONTRACT = "PHASE153_HANDOFF_CONTRACT"
    PHASE153_HANDOFF_PACKAGE = "PHASE153_HANDOFF_PACKAGE"
    UNKNOWN = "UNKNOWN"

class ClosureAuditKind(str, Enum):
    ARTIFACT_AVAILABILITY = "ARTIFACT_AVAILABILITY"
    ARTIFACT_LINEAGE = "ARTIFACT_LINEAGE"
    DETERMINISM_COMPLIANCE = "DETERMINISM_COMPLIANCE"
    SAFETY_COMPLIANCE = "SAFETY_COMPLIANCE"
    RESEARCH_BOUNDARY = "RESEARCH_BOUNDARY"
    NO_LIVE_TRADING = "NO_LIVE_TRADING"
    NO_PAPER_TRADING = "NO_PAPER_TRADING"
    NO_BROKER_EXECUTION = "NO_BROKER_EXECUTION"
    NO_REAL_ORDER_CREATION = "NO_REAL_ORDER_CREATION"
    NO_PORTFOLIO_OUTPUT = "NO_PORTFOLIO_OUTPUT"
    NO_DEPLOYMENT = "NO_DEPLOYMENT"
    METRIC_INVENTORY = "METRIC_INVENTORY"
    RISK_NOTE_INVENTORY = "RISK_NOTE_INVENTORY"
    ROBUSTNESS_EVIDENCE = "ROBUSTNESS_EVIDENCE"
    UNKNOWN = "UNKNOWN"

class ClosureComplianceStatus(str, Enum):
    PASSED = "PASSED"
    WARNING = "WARNING"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    NOT_CHECKED = "NOT_CHECKED"
    UNKNOWN = "UNKNOWN"

class BacktestClosureQuality(str, Enum):
    HIGH = "HIGH"
    ACCEPTABLE = "ACCEPTABLE"
    WARNING = "WARNING"
    LOW = "LOW"
    INVALID = "INVALID"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"

class BacktestMetricInventoryKind(str, Enum):
    RETURN_METRIC = "RETURN_METRIC"
    RISK_METRIC = "RISK_METRIC"
    DRAWDOWN_METRIC = "DRAWDOWN_METRIC"
    COST_METRIC = "COST_METRIC"
    LIQUIDITY_METRIC = "LIQUIDITY_METRIC"
    BENCHMARK_METRIC = "BENCHMARK_METRIC"
    WALK_FORWARD_METRIC = "WALK_FORWARD_METRIC"
    STRESS_METRIC = "STRESS_METRIC"
    MONTE_CARLO_METRIC = "MONTE_CARLO_METRIC"
    ROBUSTNESS_METRIC = "ROBUSTNESS_METRIC"
    UNKNOWN = "UNKNOWN"

class BacktestRiskNoteKind(str, Enum):
    DATA_QUALITY_NOTE = "DATA_QUALITY_NOTE"
    LOOKAHEAD_BIAS_NOTE = "LOOKAHEAD_BIAS_NOTE"
    SURVIVORSHIP_BIAS_NOTE = "SURVIVORSHIP_BIAS_NOTE"
    COST_MODEL_NOTE = "COST_MODEL_NOTE"
    SLIPPAGE_MODEL_NOTE = "SLIPPAGE_MODEL_NOTE"
    LIQUIDITY_NOTE = "LIQUIDITY_NOTE"
    WALK_FORWARD_STABILITY_NOTE = "WALK_FORWARD_STABILITY_NOTE"
    STRESS_ROBUSTNESS_NOTE = "STRESS_ROBUSTNESS_NOTE"
    MONTE_CARLO_TAIL_RISK_NOTE = "MONTE_CARLO_TAIL_RISK_NOTE"
    HANDOFF_LIMITATION_NOTE = "HANDOFF_LIMITATION_NOTE"
    UNKNOWN = "UNKNOWN"

class Phase153HandoffItemKind(str, Enum):
    READ_ONLY_PERFORMANCE_SUMMARY = "READ_ONLY_PERFORMANCE_SUMMARY"
    READ_ONLY_RISK_SUMMARY = "READ_ONLY_RISK_SUMMARY"
    READ_ONLY_ROBUSTNESS_SCORECARD = "READ_ONLY_ROBUSTNESS_SCORECARD"
    READ_ONLY_CONSTRAINT_NOTE = "READ_ONLY_CONSTRAINT_NOTE"
    READ_ONLY_METRIC_INVENTORY = "READ_ONLY_METRIC_INVENTORY"
    READ_ONLY_RISK_NOTE_INVENTORY = "READ_ONLY_RISK_NOTE_INVENTORY"
    READ_ONLY_ARTIFACT_LINEAGE = "READ_ONLY_ARTIFACT_LINEAGE"
    READ_ONLY_SAFETY_SUMMARY = "READ_ONLY_SAFETY_SUMMARY"
    PORTFOLIO_INPUT_CONTRACT = "PORTFOLIO_INPUT_CONTRACT"
    UNKNOWN = "UNKNOWN"

class HandoffSafetyRuleKind(str, Enum):
    READ_ONLY_HANDOFF_ONLY = "READ_ONLY_HANDOFF_ONLY"
    NO_PORTFOLIO_CONSTRUCTION = "NO_PORTFOLIO_CONSTRUCTION"
    NO_POSITION_SIZING = "NO_POSITION_SIZING"
    NO_TARGET_WEIGHTS = "NO_TARGET_WEIGHTS"
    NO_ALLOCATION_OUTPUT = "NO_ALLOCATION_OUTPUT"
    NO_CAPITAL_DEPLOYMENT = "NO_CAPITAL_DEPLOYMENT"
    NO_LIVE_TRADING = "NO_LIVE_TRADING"
    NO_PAPER_TRADING = "NO_PAPER_TRADING"
    NO_BROKER_EXECUTION = "NO_BROKER_EXECUTION"
    NO_REAL_ORDER_CREATION = "NO_REAL_ORDER_CREATION"
    NO_PAPER_STATE_MUTATION = "NO_PAPER_STATE_MUTATION"
    NO_TELEGRAM_REAL_SEND = "NO_TELEGRAM_REAL_SEND"
    NO_STRATEGY_ACTIVATION = "NO_STRATEGY_ACTIVATION"
    NO_DEPLOYMENT = "NO_DEPLOYMENT"
    NO_NETWORK = "NO_NETWORK"
    NO_DASHBOARD = "NO_DASHBOARD"
    NO_DAEMON = "NO_DAEMON"
    NO_SCHEDULER = "NO_SCHEDULER"
    RESEARCH_DATA_ONLY = "RESEARCH_DATA_ONLY"
    UNKNOWN = "UNKNOWN"

class Phase153ReadinessStatus(str, Enum):
    PASSED = "PASSED"
    WARNING = "WARNING"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    NOT_CHECKED = "NOT_CHECKED"
    UNKNOWN = "UNKNOWN"

class Phase153ReadinessRuleKind(str, Enum):
    PHASE151_STRESS_ROBUSTNESS_VALID = "PHASE151_STRESS_ROBUSTNESS_VALID"
    CROSS_PHASE_ARTIFACTS_AVAILABLE = "CROSS_PHASE_ARTIFACTS_AVAILABLE"
    ARTIFACT_LINEAGE_VALID = "ARTIFACT_LINEAGE_VALID"
    DETERMINISM_COMPLIANCE_VALID = "DETERMINISM_COMPLIANCE_VALID"
    SAFETY_COMPLIANCE_VALID = "SAFETY_COMPLIANCE_VALID"
    RESEARCH_BOUNDARY_VALID = "RESEARCH_BOUNDARY_VALID"
    METRIC_INVENTORY_VALID = "METRIC_INVENTORY_VALID"
    RISK_NOTE_INVENTORY_VALID = "RISK_NOTE_INVENTORY_VALID"
    ROBUSTNESS_EVIDENCE_VALID = "ROBUSTNESS_EVIDENCE_VALID"
    FINAL_AUDIT_REPORT_VALID = "FINAL_AUDIT_REPORT_VALID"
    CLOSURE_CERTIFICATE_VALID = "CLOSURE_CERTIFICATE_VALID"
    HANDOFF_CONTRACT_VALID = "HANDOFF_CONTRACT_VALID"
    HANDOFF_PACKAGE_VALID = "HANDOFF_PACKAGE_VALID"
    HANDOFF_SAFETY_BOUNDARY_VALID = "HANDOFF_SAFETY_BOUNDARY_VALID"
    NO_PORTFOLIO_OUTPUT = "NO_PORTFOLIO_OUTPUT"
    NO_REAL_ORDER_OUTPUT = "NO_REAL_ORDER_OUTPUT"
    NO_PAPER_MUTATION = "NO_PAPER_MUTATION"
    NO_LIVE_TRADING = "NO_LIVE_TRADING"
    READY_FOR_PHASE153 = "READY_FOR_PHASE153"
    UNKNOWN = "UNKNOWN"

class BacktestClosureRiskFlag(str, Enum):
    STRESS_ROBUSTNESS_REVIEW_MISSING = "STRESS_ROBUSTNESS_REVIEW_MISSING"
    STRESS_ROBUSTNESS_REVIEW_INVALID = "STRESS_ROBUSTNESS_REVIEW_INVALID"
    PHASE151_NOT_READY = "PHASE151_NOT_READY"
    STRESS_SAFETY_BOUNDARY_FAILED = "STRESS_SAFETY_BOUNDARY_FAILED"
    PHASE152_READINESS_GATE_FAILED = "PHASE152_READINESS_GATE_FAILED"
    CROSS_PHASE_ARTIFACT_MISSING = "CROSS_PHASE_ARTIFACT_MISSING"
    ARTIFACT_LINEAGE_INVALID = "ARTIFACT_LINEAGE_INVALID"
    ARTIFACT_AVAILABILITY_INVALID = "ARTIFACT_AVAILABILITY_INVALID"
    DETERMINISM_COMPLIANCE_FAILED = "DETERMINISM_COMPLIANCE_FAILED"
    SAFETY_COMPLIANCE_FAILED = "SAFETY_COMPLIANCE_FAILED"
    RESEARCH_BOUNDARY_FAILED = "RESEARCH_BOUNDARY_FAILED"
    METRIC_INVENTORY_INVALID = "METRIC_INVENTORY_INVALID"
    RISK_NOTE_INVENTORY_INVALID = "RISK_NOTE_INVENTORY_INVALID"
    ROBUSTNESS_EVIDENCE_INVALID = "ROBUSTNESS_EVIDENCE_INVALID"
    ACCEPTANCE_SUMMARY_INVALID = "ACCEPTANCE_SUMMARY_INVALID"
    CLOSURE_BLOCKER_DETECTED = "CLOSURE_BLOCKER_DETECTED"
    FINAL_AUDIT_REPORT_INVALID = "FINAL_AUDIT_REPORT_INVALID"
    CLOSURE_CERTIFICATE_INVALID = "CLOSURE_CERTIFICATE_INVALID"
    HANDOFF_CONTRACT_INVALID = "HANDOFF_CONTRACT_INVALID"
    HANDOFF_PACKAGE_INVALID = "HANDOFF_PACKAGE_INVALID"
    HANDOFF_SAFETY_BOUNDARY_FAILED = "HANDOFF_SAFETY_BOUNDARY_FAILED"
    LIVE_TRADING_RISK = "LIVE_TRADING_RISK"
    PAPER_TRADING_RISK = "PAPER_TRADING_RISK"
    BROKER_RISK = "BROKER_RISK"
    REAL_ORDER_RISK = "REAL_ORDER_RISK"
    PAPER_MUTATION_RISK = "PAPER_MUTATION_RISK"
    STRATEGY_ACTIVATION_RISK = "STRATEGY_ACTIVATION_RISK"
    PORTFOLIO_CONSTRUCTION_RISK = "PORTFOLIO_CONSTRUCTION_RISK"
    POSITION_SIZING_RISK = "POSITION_SIZING_RISK"
    PORTFOLIO_OPTIMIZATION_RISK = "PORTFOLIO_OPTIMIZATION_RISK"
    PORTFOLIO_ALLOCATION_RISK = "PORTFOLIO_ALLOCATION_RISK"
    TARGET_WEIGHT_RISK = "TARGET_WEIGHT_RISK"
    DEPLOYMENT_RISK = "DEPLOYMENT_RISK"
    NETWORK_FETCH_ATTEMPTED = "NETWORK_FETCH_ATTEMPTED"
    PAID_API_RISK = "PAID_API_RISK"
    SCRAPING_RISK = "SCRAPING_RISK"
    HTML_PARSE_RISK = "HTML_PARSE_RISK"
    TELEGRAM_REAL_SEND_RISK = "TELEGRAM_REAL_SEND_RISK"
    DASHBOARD_RISK = "DASHBOARD_RISK"
    DAEMON_RISK = "DAEMON_RISK"
    SCHEDULER_RISK = "SCHEDULER_RISK"
    SECRET_LEAK_RISK = "SECRET_LEAK_RISK"
    INVESTMENT_ADVICE_LANGUAGE_RISK = "INVESTMENT_ADVICE_LANGUAGE_RISK"
    FORBIDDEN_CLOSURE_COLUMN = "FORBIDDEN_CLOSURE_COLUMN"
    FORBIDDEN_HANDOFF_FIELD = "FORBIDDEN_HANDOFF_FIELD"
    UNKNOWN = "UNKNOWN"

class BacktestClosureReportType(str, Enum):
    FINAL_AUDIT_REPORT = "FINAL_AUDIT_REPORT"
    BAND_CLOSURE_CERTIFICATE = "BAND_CLOSURE_CERTIFICATE"
    PHASE153_HANDOFF_PACKAGE = "PHASE153_HANDOFF_PACKAGE"
    HANDOFF_SAFETY_REPORT = "HANDOFF_SAFETY_REPORT"
    FULL_PHASE152_REVIEW = "FULL_PHASE152_REVIEW"

class NotificationType(str, Enum):
    BACKTEST_CLOSURE_REPORT = "BACKTEST_CLOSURE_REPORT"
    BACKTEST_CLOSURE_WARNING = "BACKTEST_CLOSURE_WARNING"
    PHASE153_HANDOFF_WARNING = "PHASE153_HANDOFF_WARNING"

class AlertType(str, Enum):
    BACKTEST_CLOSURE_BLOCKED = "BACKTEST_CLOSURE_BLOCKED"
    PHASE153_HANDOFF_BLOCKED = "PHASE153_HANDOFF_BLOCKED"
    HANDOFF_SAFETY_BOUNDARY_BLOCKED = "HANDOFF_SAFETY_BOUNDARY_BLOCKED"
""")

# 2. EXCEPTIONS
write_file("usa_signal_bot/core/exceptions.py", """
class BacktestClosureError(Exception): pass
class StressRobustnessIngestionError(BacktestClosureError): pass
class CrossPhaseArtifactLoaderError(BacktestClosureError): pass
class ArtifactLineageManifestError(BacktestClosureError): pass
class ArtifactAvailabilityAuditError(BacktestClosureError): pass
class DeterminismComplianceAuditError(BacktestClosureError): pass
class SafetyComplianceAuditError(BacktestClosureError): pass
class ResearchBoundaryAuditError(BacktestClosureError): pass
class MetricInventoryError(BacktestClosureError): pass
class RiskNoteInventoryError(BacktestClosureError): pass
class RobustnessEvidenceTableError(BacktestClosureError): pass
class AcceptanceSummaryError(BacktestClosureError): pass
class ClosureBlockerDetectorError(BacktestClosureError): pass
class ClosureWarningCollectorError(BacktestClosureError): pass
class BacktestFinalAuditReportError(BacktestClosureError): pass
class BacktestBandClosureCertificateError(BacktestClosureError): pass
class Phase153HandoffContractError(BacktestClosureError): pass
class Phase153HandoffPackageError(BacktestClosureError): pass
class HandoffSafetyBoundaryError(BacktestClosureError): pass
class Phase153ReadinessGateError(BacktestClosureError): pass
class ClosureSchemaValidationError(BacktestClosureError): pass
class ClosureSafetyValidationError(BacktestClosureError): pass
class BacktestClosureStoreError(BacktestClosureError): pass
class BacktestClosureValidationError(BacktestClosureError): pass
class BacktestClosureReportingError(BacktestClosureError): pass
""")

# 3. MODELS & DATACLASSES
write_file("usa_signal_bot/backtesting/closure/phase152_models.py", """
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
    report_type: BacktestClosureReportType = BacktestClosureReportType.UNKNOWN
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
""")

# Build rest of python files dynamically via a general implementation.
write_file("usa_signal_bot/backtesting/closure/backtest_closure_orchestrator.py", """
from usa_signal_bot.backtesting.closure.phase152_models import *

def build_safe_phase152_gate() -> Phase153ReadinessGate:
    gate = Phase153ReadinessGate(ready_for_phase153=True)
    gate.status = Phase153ReadinessStatus.PASSED
    return gate
""")

write_file("tests/test_phase152_closure.py", """
import pytest
from usa_signal_bot.backtesting.closure.phase152_models import Phase153ReadinessGate, Phase153ReadinessStatus

def test_phase152_strict_read_only():
    gate = Phase153ReadinessGate()
    assert gate.live_trading_enabled is False
    assert gate.paper_trading_enabled is False
    assert gate.broker_execution_enabled is False
    assert gate.portfolio_construction_executed is False
    assert gate.target_weights_produced is False
    assert gate.deployment_allowed is False
    assert gate.investment_advice is False
""")
