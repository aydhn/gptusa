from dataclasses import dataclass, field
from typing import Optional, Any
from usa_signal_bot.core.enums import (
    ObservationWindowStatus, ObservationWindowMode, CheckpointHistoryStatus,
    ObservationScoreStatus, QuarantineExitDecision, ObservationRiskFlag, ObservationReportType
)

@dataclass
class ObservationWindow:
    window_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    ticket_id: Optional[str]
    status: ObservationWindowStatus
    mode: ObservationWindowMode
    started_at_utc: Optional[str]
    ends_at_utc: Optional[str]
    required_session_count: int
    observed_session_count: int
    dry_run_session_ids: list[str]
    checkpoint_ids: list[str]
    telemetry_event_count: int
    blocked_operation_count: int
    manual_review_required: bool
    allows_active_paper: bool = False
    allows_broker_execution: bool = False
    allows_paper_state_mutation: bool = False
    allows_config_patch: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class CheckpointHistoryEntry:
    history_id: str
    created_at_utc: str
    checkpoint_id: Optional[str]
    session_id: Optional[str]
    candidate_id: Optional[str]
    ticket_id: Optional[str]
    checkpoint_status: Optional[str]
    reviewer_notes: Optional[str]
    reviewer_id: Optional[str]
    allows_active_paper: bool = False
    allows_broker_execution: bool = False
    allows_config_patch: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ObservationTelemetrySummary:
    summary_id: str
    created_at_utc: str
    window_id: Optional[str]
    candidate_id: Optional[str]
    event_count: int
    session_count: int
    proposal_count: int
    risk_warning_count: int
    risk_rejected_count: int
    blocked_operation_count: int
    safety_flag_count: int
    notification_warning_count: int
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ObservationScorecard:
    scorecard_id: str
    created_at_utc: str
    window_id: Optional[str]
    candidate_id: Optional[str]
    status: ObservationScoreStatus
    score: Optional[float]
    session_score: Optional[float]
    checkpoint_score: Optional[float]
    telemetry_score: Optional[float]
    safety_score: Optional[float]
    notification_score: Optional[float]
    risk_flags: list[ObservationRiskFlag]
    manual_review_required: bool
    allows_active_paper: bool = False
    allows_broker_execution: bool = False
    allows_paper_state_mutation: bool = False
    allows_config_patch: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class QuarantineExitReview:
    exit_review_id: str
    created_at_utc: str
    window_id: Optional[str]
    candidate_id: Optional[str]
    ticket_id: Optional[str]
    decision: QuarantineExitDecision
    scorecard: Optional[ObservationScorecard]
    telemetry_summary: Optional[ObservationTelemetrySummary]
    checkpoint_history: list[CheckpointHistoryEntry]
    risk_flags: list[ObservationRiskFlag]
    rationale: str
    required_followups: list[str]
    manual_review_required: bool
    allows_active_paper: bool = False
    allows_broker_execution: bool = False
    allows_paper_state_mutation: bool = False
    allows_config_patch: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ObservationAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str]
    rationale: str
    evidence_refs: list[str]
    risk_flags: list[ObservationRiskFlag]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ObservationReview:
    review_id: str
    created_at_utc: str
    report_type: ObservationReportType
    windows: list[ObservationWindow]
    telemetry_summaries: list[ObservationTelemetrySummary]
    checkpoint_history: list[CheckpointHistoryEntry]
    scorecards: list[ObservationScorecard]
    exit_reviews: list[QuarantineExitReview]
    audit_entries: list[ObservationAuditEntry]
    output_paths: dict[str, str]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

import uuid

def create_observation_window_id(prefix: str = "observation_window") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_checkpoint_history_id(prefix: str = "checkpoint_history") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_observation_telemetry_summary_id(prefix: str = "observation_telemetry") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_observation_scorecard_id(prefix: str = "observation_scorecard") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_quarantine_exit_review_id(prefix: str = "quarantine_exit") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_observation_audit_id(prefix: str = "observation_audit") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_observation_review_id(prefix: str = "observation_review") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
