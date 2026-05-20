import os
import pathlib

def write_file(path, content):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

def append_file(path, content):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    mode = 'a' if p.exists() else 'w'
    with open(p, mode, encoding='utf-8') as f:
        f.write("\n" + content.strip() + "\n")

# --- CORE ENUMS ---
append_file("usa_signal_bot/core/enums.py", """
from enum import Enum

class ShadowComparisonRole(str, Enum):
    BASELINE = "BASELINE"
    CANDIDATE = "CANDIDATE"
    REFERENCE = "REFERENCE"
    UNKNOWN = "UNKNOWN"

class ShadowComparisonOutcome(str, Enum):
    CANDIDATE_BETTER = "CANDIDATE_BETTER"
    BASELINE_BETTER = "BASELINE_BETTER"
    MIXED = "MIXED"
    INCONCLUSIVE = "INCONCLUSIVE"
    BLOCKED = "BLOCKED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    UNKNOWN = "UNKNOWN"

class ShadowMetricDirection(str, Enum):
    IMPROVED = "IMPROVED"
    WORSENED = "WORSENED"
    UNCHANGED = "UNCHANGED"
    MIXED = "MIXED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    UNKNOWN = "UNKNOWN"

class ShadowAcceptanceStatus(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    NOT_EVALUATED = "NOT_EVALUATED"
    UNKNOWN = "UNKNOWN"

class ShadowAcceptanceGateType(str, Enum):
    NO_REAL_ORDER_RISK = "NO_REAL_ORDER_RISK"
    NO_PAPER_MUTATION_RISK = "NO_PAPER_MUTATION_RISK"
    NO_TELEGRAM_REAL_SEND_RISK = "NO_TELEGRAM_REAL_SEND_RISK"
    NO_PRODUCTION_CONFIG_WRITE_RISK = "NO_PRODUCTION_CONFIG_WRITE_RISK"
    LEDGER_COMPLETE = "LEDGER_COMPLETE"
    SAFETY_FLAGS_NOT_INCREASED = "SAFETY_FLAGS_NOT_INCREASED"
    COST_NOT_WORSE = "COST_NOT_WORSE"
    PNL_NOT_WORSE = "PNL_NOT_WORSE"
    RISK_NOT_WORSE = "RISK_NOT_WORSE"
    BLOCKED_INTENTS_ACCEPTABLE = "BLOCKED_INTENTS_ACCEPTABLE"
    NOTIFICATION_SAFE = "NOTIFICATION_SAFE"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"
    UNKNOWN = "UNKNOWN"

class ShadowGovernanceDecision(str, Enum):
    ACCEPT_AS_SANDBOXED_PAPER_CANDIDATE = "ACCEPT_AS_SANDBOXED_PAPER_CANDIDATE"
    ACCEPT_FOR_MORE_SHADOW_TESTING = "ACCEPT_FOR_MORE_SHADOW_TESTING"
    REQUEST_MORE_SHADOW_DATA = "REQUEST_MORE_SHADOW_DATA"
    REQUEST_REHEARSAL_RETEST = "REQUEST_REHEARSAL_RETEST"
    REJECT_SHADOW_CANDIDATE = "REJECT_SHADOW_CANDIDATE"
    BLOCK_SHADOW_CANDIDATE = "BLOCK_SHADOW_CANDIDATE"
    INCONCLUSIVE = "INCONCLUSIVE"
    UNKNOWN = "UNKNOWN"

class ShadowGovernanceRiskFlag(str, Enum):
    REAL_ORDER_RISK = "REAL_ORDER_RISK"
    BROKER_FIELD_RISK = "BROKER_FIELD_RISK"
    PAPER_STATE_MUTATION_RISK = "PAPER_STATE_MUTATION_RISK"
    TELEGRAM_REAL_SEND_RISK = "TELEGRAM_REAL_SEND_RISK"
    PRODUCTION_CONFIG_WRITE_RISK = "PRODUCTION_CONFIG_WRITE_RISK"
    SAFETY_FLAGS_INCREASED = "SAFETY_FLAGS_INCREASED"
    COST_REGRESSION = "COST_REGRESSION"
    PNL_REGRESSION = "PNL_REGRESSION"
    RISK_REGRESSION = "RISK_REGRESSION"
    LEDGER_INCOMPLETE = "LEDGER_INCOMPLETE"
    NOTIFICATION_UNSAFE = "NOTIFICATION_UNSAFE"
    TOO_FEW_SHADOW_EVENTS = "TOO_FEW_SHADOW_EVENTS"
    BLOCKED_INTENTS_HIGH = "BLOCKED_INTENTS_HIGH"
    MISSING_BASELINE_SESSION = "MISSING_BASELINE_SESSION"
    MISSING_CANDIDATE_SESSION = "MISSING_CANDIDATE_SESSION"
    UNKNOWN = "UNKNOWN"

class ShadowGovernanceReportType(str, Enum):
    SHADOW_COMPARISON = "SHADOW_COMPARISON"
    ACCEPTANCE_SCORECARD = "ACCEPTANCE_SCORECARD"
    REHEARSAL_DECISION = "REHEARSAL_DECISION"
    SHADOW_EVIDENCE_PACK = "SHADOW_EVIDENCE_PACK"
    FULL_SHADOW_GOVERNANCE_REVIEW = "FULL_SHADOW_GOVERNANCE_REVIEW"

class NotificationType(str, Enum):
    SHADOW_GOVERNANCE_REPORT = "SHADOW_GOVERNANCE_REPORT"
    SHADOW_ACCEPTANCE_WARNING = "SHADOW_ACCEPTANCE_WARNING"
    SHADOW_DECISION_WARNING = "SHADOW_DECISION_WARNING"

class AlertType(str, Enum):
    SHADOW_GOVERNANCE_BLOCKED = "SHADOW_GOVERNANCE_BLOCKED"
    SHADOW_ACCEPTANCE_FAILED = "SHADOW_ACCEPTANCE_FAILED"
    SHADOW_COMPARISON_INCONCLUSIVE = "SHADOW_COMPARISON_INCONCLUSIVE"
""")

# --- CORE EXCEPTIONS ---
append_file("usa_signal_bot/core/exceptions.py", """
class PaperShadowGovernanceError(Exception): pass
class ShadowSessionIngestionError(PaperShadowGovernanceError): pass
class ShadowMetricExtractionError(PaperShadowGovernanceError): pass
class ShadowSessionComparisonError(PaperShadowGovernanceError): pass
class ShadowRiskDeltaError(PaperShadowGovernanceError): pass
class ShadowSafetyDeltaError(PaperShadowGovernanceError): pass
class ShadowLedgerCompletenessError(PaperShadowGovernanceError): pass
class ShadowAcceptanceGateError(PaperShadowGovernanceError): pass
class ShadowAcceptanceScoringError(PaperShadowGovernanceError): pass
class ShadowDecisionBoardError(PaperShadowGovernanceError): pass
class ShadowEvidencePackError(PaperShadowGovernanceError): pass
class ShadowGovernanceAuditError(PaperShadowGovernanceError): pass
class ShadowGovernanceStorageError(PaperShadowGovernanceError): pass
class ShadowGovernanceValidationError(PaperShadowGovernanceError): pass
class ShadowGovernanceReportingError(PaperShadowGovernanceError): pass
""")

# --- CORE CONFIG SCHEMA ---
append_file("usa_signal_bot/core/config_schema.py", """
from dataclasses import dataclass, field
from typing import List

@dataclass
class PaperShadowGovernanceConfig:
    enabled: bool = True
    write_shadow_governance_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_shadow_acceptance_is_not_approval: bool = True
    warn_shadow_pnl_is_simulated: bool = True

@dataclass
class ShadowComparisonConfig:
    enabled: bool = True
    require_baseline_session: bool = True
    require_candidate_session: bool = True
    required_metrics: List[str] = field(default_factory=lambda: [
        "signal_count", "candidate_count", "intent_count",
        "risk_approved_intent_count", "blocked_intent_count",
        "simulated_fill_count", "simulated_total_cost_usd",
        "simulated_slippage_usd", "simulated_pnl_usd",
        "return_pct", "max_drawdown_pct", "safety_flag_count",
        "ledger_event_count", "notification_warning_count"
    ])

@dataclass
class ShadowAcceptanceConfig:
    enabled: bool = True
    min_acceptance_score: float = 70.0
    block_on_real_order_risk: bool = True
    block_on_paper_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    request_retest_on_incomplete_ledger: bool = True
    warn_on_cost_regression: bool = True
    warn_on_risk_regression: bool = True
    warn_on_safety_flags_increased: bool = True

@dataclass
class ShadowRehearsalGovernanceConfig:
    enabled: bool = True
    conservative_decision_board: bool = True
    allow_real_orders: bool = False
    allow_paper_state_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_production_config_write: bool = False
    accepted_status_means_sandboxed_candidate_only: bool = True
    require_manual_review: bool = True

@dataclass
class ShadowEvidencePackConfig:
    enabled: bool = True
    required_items: List[str] = field(default_factory=lambda: [
        "baseline_shadow_session", "candidate_shadow_session",
        "metric_comparisons", "acceptance_gates", "safety_delta",
        "risk_delta", "ledger_completeness", "notification_review",
        "shadow_pnl_snapshot"
    ])
    request_more_data_on_missing_evidence: bool = True

@dataclass
class PaperShadowGovernanceNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_shadow_governance_report: bool = True
    notify_shadow_acceptance_warning: bool = True
    notify_shadow_decision_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True
""")

# --- MODELS ---
write_file("usa_signal_bot/paper_shadow_governance/shadow_governance_models.py", """
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    ShadowMetricDirection, ShadowAcceptanceStatus, ShadowAcceptanceGateType,
    ShadowGovernanceRiskFlag, ShadowComparisonOutcome, ShadowGovernanceDecision,
    ShadowGovernanceReportType
)
from usa_signal_bot.core.exceptions import ShadowGovernanceValidationError

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class ShadowMetricComparison:
    comparison_id: str
    metric_name: str
    baseline_value: Optional[float]
    candidate_value: Optional[float]
    delta_value: Optional[float]
    delta_pct: Optional[float]
    direction: ShadowMetricDirection
    higher_is_better: bool
    interpretation: str
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowAcceptanceGate:
    gate_id: str
    gate_type: ShadowAcceptanceGateType
    status: ShadowAcceptanceStatus
    threshold: Optional[Any]
    observed_value: Optional[Any]
    description: str
    risk_flags: List[ShadowGovernanceRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowAcceptanceScorecard:
    scorecard_id: str
    created_at_utc: str
    baseline_session_id: Optional[str]
    candidate_session_id: Optional[str]
    overall_status: ShadowAcceptanceStatus
    acceptance_score: Optional[float]
    gate_pass_count: int
    gate_warning_count: int
    gate_fail_count: int
    gate_blocked_count: int
    metric_score_components: Dict[str, Optional[float]]
    risk_flags: List[ShadowGovernanceRiskFlag]
    manual_review_required: bool
    allowed_for_real_orders: bool
    allowed_for_paper_state_mutation: bool
    allowed_for_telegram_real_send: bool
    allowed_for_production_config_write: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowSessionComparisonReport:
    report_id: str
    created_at_utc: str
    baseline_session_id: Optional[str]
    candidate_session_id: Optional[str]
    outcome: ShadowComparisonOutcome
    metric_comparisons: List[ShadowMetricComparison]
    risk_delta: Dict[str, Any]
    safety_delta: Dict[str, Any]
    ledger_completeness: Dict[str, Any]
    notification_review: Dict[str, Any]
    acceptance_scorecard: Optional[ShadowAcceptanceScorecard]
    summary: Dict[str, Any]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowEvidencePack:
    evidence_pack_id: str
    created_at_utc: str
    baseline_session_id: Optional[str]
    candidate_session_id: Optional[str]
    comparison_report_id: Optional[str]
    required_evidence: List[str]
    available_evidence: List[str]
    missing_evidence: List[str]
    evidence_complete: bool
    evidence_summary: Dict[str, Any]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowDecisionBoardResult:
    decision_id: str
    created_at_utc: str
    comparison_report_id: Optional[str]
    scorecard_id: Optional[str]
    decision: ShadowGovernanceDecision
    outcome: ShadowComparisonOutcome
    acceptance_status: ShadowAcceptanceStatus
    risk_flags: List[ShadowGovernanceRiskFlag]
    rationale: str
    required_followups: List[str]
    manual_review_required: bool
    allowed_for_real_orders: bool
    allowed_for_paper_state_mutation: bool
    allowed_for_telegram_real_send: bool
    allowed_for_production_config_write: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowGovernanceAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    rationale: str
    evidence_refs: List[str]
    risk_flags: List[ShadowGovernanceRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowGovernanceReview:
    review_id: str
    created_at_utc: str
    report_type: ShadowGovernanceReportType
    comparison_reports: List[ShadowSessionComparisonReport]
    scorecards: List[ShadowAcceptanceScorecard]
    evidence_packs: List[ShadowEvidencePack]
    decisions: List[ShadowDecisionBoardResult]
    audit_entries: List[ShadowGovernanceAuditEntry]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

# FACTORIES
def create_shadow_metric_comparison_id(metric_name: str) -> str:
    return f"smc_{metric_name}_{uuid.uuid4().hex[:8]}"
def create_shadow_acceptance_gate_id(gate_type: ShadowAcceptanceGateType) -> str:
    return f"sag_{gate_type.value}_{uuid.uuid4().hex[:8]}"
def create_shadow_acceptance_scorecard_id(prefix: str = "shadow_scorecard") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_shadow_session_comparison_report_id(prefix: str = "shadow_comparison") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_shadow_evidence_pack_id(prefix: str = "shadow_evidence") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_shadow_decision_board_result_id(prefix: str = "shadow_decision") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_shadow_governance_audit_entry_id(prefix: str = "shadow_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_shadow_governance_review_id(prefix: str = "shadow_governance_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

# VALIDATORS
def validate_shadow_acceptance_scorecard(item: ShadowAcceptanceScorecard) -> None:
    if item.allowed_for_real_orders:
        raise ShadowGovernanceValidationError("Shadow governance cannot allow real orders.")
    if item.allowed_for_paper_state_mutation:
        raise ShadowGovernanceValidationError("Shadow governance cannot allow paper state mutation.")
    if item.allowed_for_telegram_real_send:
        raise ShadowGovernanceValidationError("Shadow governance cannot allow real telegram send.")
    if item.allowed_for_production_config_write:
        raise ShadowGovernanceValidationError("Shadow governance cannot allow production config write.")
    if item.acceptance_score is not None and not (0 <= item.acceptance_score <= 100):
        raise ShadowGovernanceValidationError("Acceptance score must be between 0 and 100.")

def validate_shadow_decision_board_result(item: ShadowDecisionBoardResult) -> None:
    if item.allowed_for_real_orders:
        raise ShadowGovernanceValidationError("Shadow governance cannot allow real orders.")
    if item.allowed_for_paper_state_mutation:
        raise ShadowGovernanceValidationError("Shadow governance cannot allow paper state mutation.")

# TO_DICT (stubs for serialization)
def shadow_metric_comparison_to_dict(item: ShadowMetricComparison) -> dict: return item.__dict__.copy()
def shadow_acceptance_gate_to_dict(item: ShadowAcceptanceGate) -> dict: return item.__dict__.copy()
def shadow_acceptance_scorecard_to_dict(item: ShadowAcceptanceScorecard) -> dict: return item.__dict__.copy()
def shadow_session_comparison_report_to_dict(item: ShadowSessionComparisonReport) -> dict: return item.__dict__.copy()
def shadow_evidence_pack_to_dict(item: ShadowEvidencePack) -> dict: return item.__dict__.copy()
def shadow_decision_board_result_to_dict(item: ShadowDecisionBoardResult) -> dict: return item.__dict__.copy()
def shadow_governance_audit_entry_to_dict(item: ShadowGovernanceAuditEntry) -> dict: return item.__dict__.copy()
def shadow_governance_review_to_dict(item: ShadowGovernanceReview) -> dict: return item.__dict__.copy()
""")

print("Core files and models generated successfully.")
