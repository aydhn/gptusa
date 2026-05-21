import datetime
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, List, Optional, Dict

from usa_signal_bot.core.enums import (
    ControlledPlanningTicketStatus,
    PaperAdjacentRehearsalStatus,
    PaperAdjacentRehearsalMode,
    ApprovalQueueItemStatus,
    ApprovalQueueDecision,
    ControlledPlanningSafetyFlag,
    ControlledPlanningReportType
)
from usa_signal_bot.core.exceptions import ControlledPlanningValidationError

def _now_str() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

@dataclass
class ControlledPlanningTicket:
    ticket_id: str
    created_at_utc: str
    status: ControlledPlanningTicketStatus
    candidate_id: Optional[str]
    source_observation_review_id: Optional[str]
    source_exit_review_id: Optional[str]
    source_exit_decision: Optional[str]
    observation_score: Optional[float]
    evidence_refs: List[str]
    required_followups: List[str]
    safety_flags: List[ControlledPlanningSafetyFlag]
    manual_review_required: bool
    final_approval_required: bool
    allowed_for_active_paper: bool
    allowed_for_broker_execution: bool
    allowed_for_paper_state_mutation: bool
    allowed_for_config_patch: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperAdjacentRehearsalContext:
    context_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    planning_ticket_id: Optional[str]
    mode: PaperAdjacentRehearsalMode
    read_only_paper_snapshot: Dict[str, Any]
    candidate_metadata: Dict[str, Any]
    output_path: Optional[str]
    allow_active_paper: bool
    allow_paper_state_mutation: bool
    allow_paper_orders: bool
    allow_broker_orders: bool
    allow_telegram_real_send: bool
    allow_config_patch: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperAdjacentProposal:
    proposal_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    symbol: Optional[str]
    proposal_type: str
    side: Optional[str]
    quantity: Optional[float]
    notional_usd: Optional[float]
    risk_status: Optional[str]
    reason: str
    is_real_order: bool
    will_mutate_paper_state: bool
    will_send_to_broker: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperAdjacentRehearsalRun:
    run_id: str
    created_at_utc: str
    status: PaperAdjacentRehearsalStatus
    context: Optional[PaperAdjacentRehearsalContext]
    proposals: List[PaperAdjacentProposal]
    safety_flags: List[ControlledPlanningSafetyFlag]
    started_at_utc: Optional[str]
    completed_at_utc: Optional[str]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FinalHumanApprovalQueueItem:
    queue_item_id: str
    created_at_utc: str
    status: ApprovalQueueItemStatus
    candidate_id: Optional[str]
    planning_ticket_id: Optional[str]
    rehearsal_run_id: Optional[str]
    decision: ApprovalQueueDecision
    reviewer_notes: Optional[str]
    reviewer_id: Optional[str]
    reviewed_at_utc: Optional[str]
    required_evidence_refs: List[str]
    safety_flags: List[ControlledPlanningSafetyFlag]
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ControlledPlanningAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str]
    rationale: str
    evidence_refs: List[str]
    safety_flags: List[ControlledPlanningSafetyFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ControlledPlanningReview:
    review_id: str
    created_at_utc: str
    report_type: ControlledPlanningReportType
    planning_tickets: List[ControlledPlanningTicket]
    rehearsal_runs: List[PaperAdjacentRehearsalRun]
    approval_queue_items: List[FinalHumanApprovalQueueItem]
    audit_entries: List[ControlledPlanningAuditEntry]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

def controlled_planning_ticket_to_dict(item: ControlledPlanningTicket) -> dict:
    return asdict(item)

def paper_adjacent_rehearsal_context_to_dict(item: PaperAdjacentRehearsalContext) -> dict:
    return asdict(item)

def paper_adjacent_proposal_to_dict(item: PaperAdjacentProposal) -> dict:
    return asdict(item)

def paper_adjacent_rehearsal_run_to_dict(item: PaperAdjacentRehearsalRun) -> dict:
    return asdict(item)

def final_human_approval_queue_item_to_dict(item: FinalHumanApprovalQueueItem) -> dict:
    return asdict(item)

def controlled_planning_audit_entry_to_dict(item: ControlledPlanningAuditEntry) -> dict:
    return asdict(item)

def controlled_planning_review_to_dict(item: ControlledPlanningReview) -> dict:
    return asdict(item)

def validate_controlled_planning_ticket(item: ControlledPlanningTicket) -> None:
    if item.allowed_for_active_paper:
        raise ControlledPlanningValidationError("Ticket allowed_for_active_paper must be false")
    if item.allowed_for_broker_execution:
        raise ControlledPlanningValidationError("Ticket allowed_for_broker_execution must be false")
    if item.allowed_for_paper_state_mutation:
        raise ControlledPlanningValidationError("Ticket allowed_for_paper_state_mutation must be false")
    if item.allowed_for_config_patch:
        raise ControlledPlanningValidationError("Ticket allowed_for_config_patch must be false")

def validate_paper_adjacent_rehearsal_context(item: PaperAdjacentRehearsalContext) -> None:
    if item.allow_active_paper: raise ControlledPlanningValidationError("Context allow_active_paper must be false")
    if item.allow_paper_state_mutation: raise ControlledPlanningValidationError("Context allow_paper_state_mutation must be false")
    if item.allow_paper_orders: raise ControlledPlanningValidationError("Context allow_paper_orders must be false")
    if item.allow_broker_orders: raise ControlledPlanningValidationError("Context allow_broker_orders must be false")
    if item.allow_telegram_real_send: raise ControlledPlanningValidationError("Context allow_telegram_real_send must be false")
    if item.allow_config_patch: raise ControlledPlanningValidationError("Context allow_config_patch must be false")

def validate_paper_adjacent_proposal(item: PaperAdjacentProposal) -> None:
    if item.is_real_order: raise ControlledPlanningValidationError("Proposal is_real_order must be false")
    if item.will_mutate_paper_state: raise ControlledPlanningValidationError("Proposal will_mutate_paper_state must be false")
    if item.will_send_to_broker: raise ControlledPlanningValidationError("Proposal will_send_to_broker must be false")

def validate_paper_adjacent_rehearsal_run(item: PaperAdjacentRehearsalRun) -> None:
    if item.context:
        validate_paper_adjacent_rehearsal_context(item.context)
    for p in item.proposals:
        validate_paper_adjacent_proposal(p)

def validate_final_human_approval_queue_item(item: FinalHumanApprovalQueueItem) -> None:
    if item.allows_active_paper: raise ControlledPlanningValidationError("ApprovalItem allows_active_paper must be false")
    if item.allows_broker_execution: raise ControlledPlanningValidationError("ApprovalItem allows_broker_execution must be false")
    if item.allows_paper_state_mutation: raise ControlledPlanningValidationError("ApprovalItem allows_paper_state_mutation must be false")
    if item.allows_config_patch: raise ControlledPlanningValidationError("ApprovalItem allows_config_patch must be false")

def validate_controlled_planning_review(item: ControlledPlanningReview) -> None:
    for t in item.planning_tickets:
        validate_controlled_planning_ticket(t)
    for r in item.rehearsal_runs:
        validate_paper_adjacent_rehearsal_run(r)
    for q in item.approval_queue_items:
        validate_final_human_approval_queue_item(q)

def create_controlled_planning_ticket_id(prefix: str = "controlled_planning_ticket") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_adjacent_context_id(prefix: str = "paper_adjacent_context") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_adjacent_proposal_id(prefix: str = "paper_adjacent_proposal") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_adjacent_rehearsal_run_id(prefix: str = "paper_adjacent_run") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_final_approval_queue_item_id(prefix: str = "final_approval_queue") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_controlled_planning_audit_id(prefix: str = "controlled_planning_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_controlled_planning_review_id(prefix: str = "controlled_planning_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
