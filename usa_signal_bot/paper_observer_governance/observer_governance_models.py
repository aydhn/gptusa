from dataclasses import dataclass, field
from typing import Any
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    ObserverComparisonOutcome, ObserverMetricDirection, EvidenceFreshnessStatus,
    ObserverGovernanceStatus, ObserverGovernanceDecision, ObserverGovernanceRiskFlag,
    ObserverGovernanceGateType, ObserverGovernanceReportType
)

@dataclass
class ObserverMetricComparison:
    comparison_id: str
    metric_name: str
    paper_value: float | int | str | None
    observer_value: float | int | str | None
    delta_value: float | None
    delta_pct: float | None
    direction: ObserverMetricDirection
    interpretation: str
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ObserverPaperComparisonReport:
    report_id: str
    created_at_utc: str
    paper_snapshot_id: str | None
    observer_session_id: str | None
    candidate_id: str | None
    outcome: ObserverComparisonOutcome
    metric_comparisons: list[ObserverMetricComparison]
    signal_delta: dict[str, Any]
    proposal_delta: dict[str, Any]
    risk_delta: dict[str, Any]
    drift_delta: dict[str, Any]
    safety_compliance: dict[str, Any]
    notification_comparison: dict[str, Any]
    blocked_operation_comparison: dict[str, Any]
    risk_flags: list[ObserverGovernanceRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PromotionEvidenceItem:
    evidence_id: str
    created_at_utc: str
    evidence_type: str
    source_phase: str | None
    source_ref_id: str | None
    status: EvidenceFreshnessStatus
    summary: dict[str, Any]
    required: bool
    available: bool
    fresh: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PromotionEvidenceRefresh:
    refresh_id: str
    created_at_utc: str
    candidate_id: str | None
    evidence_items: list[PromotionEvidenceItem]
    required_count: int
    available_count: int
    fresh_count: int
    missing_count: int
    stale_count: int
    evidence_score: float | None
    status: EvidenceFreshnessStatus
    required_followups: list[str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ObserverGovernanceGate:
    gate_id: str
    gate_type: ObserverGovernanceGateType
    status: ObserverGovernanceStatus
    observed_value: Any | None
    threshold: Any | None
    description: str
    risk_flags: list[ObserverGovernanceRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ObserverGovernanceDecisionResult:
    decision_id: str
    created_at_utc: str
    candidate_id: str | None
    comparison_report_id: str | None
    evidence_refresh_id: str | None
    decision: ObserverGovernanceDecision
    status: ObserverGovernanceStatus
    risk_flags: list[ObserverGovernanceRiskFlag]
    rationale: str
    required_followups: list[str]
    manual_review_required: bool
    allowed_for_active_paper: bool
    allowed_for_broker_execution: bool
    allowed_for_paper_state_mutation: bool
    allowed_for_config_patch: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ObserverGovernanceAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    rationale: str
    evidence_refs: list[str]
    risk_flags: list[ObserverGovernanceRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ObserverGovernanceReview:
    review_id: str
    created_at_utc: str
    report_type: ObserverGovernanceReportType
    comparison_reports: list[ObserverPaperComparisonReport]
    evidence_refreshes: list[PromotionEvidenceRefresh]
    gates: list[ObserverGovernanceGate]
    decisions: list[ObserverGovernanceDecisionResult]
    audit_entries: list[ObserverGovernanceAuditEntry]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def observer_metric_comparison_to_dict(item: ObserverMetricComparison) -> dict:
    return item.__dict__

def observer_paper_comparison_report_to_dict(item: ObserverPaperComparisonReport) -> dict:
    return {
        **item.__dict__,
        "outcome": item.outcome.value,
        "metric_comparisons": [observer_metric_comparison_to_dict(m) for m in item.metric_comparisons],
        "risk_flags": [f.value for f in item.risk_flags]
    }

def promotion_evidence_item_to_dict(item: PromotionEvidenceItem) -> dict:
    return {**item.__dict__, "status": item.status.value}

def promotion_evidence_refresh_to_dict(item: PromotionEvidenceRefresh) -> dict:
    return {
        **item.__dict__,
        "evidence_items": [promotion_evidence_item_to_dict(e) for e in item.evidence_items],
        "status": item.status.value
    }

def observer_governance_gate_to_dict(item: ObserverGovernanceGate) -> dict:
    return {
        **item.__dict__,
        "gate_type": item.gate_type.value,
        "status": item.status.value,
        "risk_flags": [f.value for f in item.risk_flags]
    }

def observer_governance_decision_result_to_dict(item: ObserverGovernanceDecisionResult) -> dict:
    return {
        **item.__dict__,
        "decision": item.decision.value,
        "status": item.status.value,
        "risk_flags": [f.value for f in item.risk_flags]
    }

def observer_governance_audit_entry_to_dict(item: ObserverGovernanceAuditEntry) -> dict:
    return {**item.__dict__, "risk_flags": [f.value for f in item.risk_flags]}

def observer_governance_review_to_dict(item: ObserverGovernanceReview) -> dict:
    return {
        **item.__dict__,
        "report_type": item.report_type.value,
        "comparison_reports": [observer_paper_comparison_report_to_dict(r) for r in item.comparison_reports],
        "evidence_refreshes": [promotion_evidence_refresh_to_dict(e) for e in item.evidence_refreshes],
        "gates": [observer_governance_gate_to_dict(g) for g in item.gates],
        "decisions": [observer_governance_decision_result_to_dict(d) for d in item.decisions],
        "audit_entries": [observer_governance_audit_entry_to_dict(a) for a in item.audit_entries]
    }

def validate_observer_metric_comparison(item: ObserverMetricComparison) -> None:
    pass

def validate_observer_paper_comparison_report(item: ObserverPaperComparisonReport) -> None:
    pass

def validate_promotion_evidence_refresh(item: PromotionEvidenceRefresh) -> None:
    if item.evidence_score is not None and not (0 <= item.evidence_score <= 100):
        raise ValueError("evidence_score must be between 0 and 100")

def validate_observer_governance_gate(item: ObserverGovernanceGate) -> None:
    pass

def validate_observer_governance_decision_result(item: ObserverGovernanceDecisionResult) -> None:
    if item.allowed_for_active_paper: raise ValueError("allowed_for_active_paper must be False")
    if item.allowed_for_broker_execution: raise ValueError("allowed_for_broker_execution must be False")
    if item.allowed_for_paper_state_mutation: raise ValueError("allowed_for_paper_state_mutation must be False")
    if item.allowed_for_config_patch: raise ValueError("allowed_for_config_patch must be False")

def validate_observer_governance_review(item: ObserverGovernanceReview) -> None:
    for d in item.decisions:
        validate_observer_governance_decision_result(d)

def create_observer_metric_comparison_id(metric_name: str) -> str:
    return f"comp_{metric_name}_{uuid.uuid4().hex[:8]}"

def create_observer_paper_comparison_report_id(prefix: str = "observer_paper_comparison") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def create_promotion_evidence_item_id(prefix: str = "promotion_evidence") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_promotion_evidence_refresh_id(prefix: str = "evidence_refresh") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def create_observer_governance_gate_id(prefix: str = "observer_governance_gate") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_observer_governance_decision_id(prefix: str = "observer_governance_decision") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def create_observer_governance_audit_id(prefix: str = "observer_governance_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_observer_governance_review_id(prefix: str = "observer_governance_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"
