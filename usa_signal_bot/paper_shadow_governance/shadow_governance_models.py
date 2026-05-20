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
