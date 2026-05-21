from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
from datetime import datetime, timezone
import uuid

from usa_signal_bot.core.enums import (
    PaperObserverEnrollmentStatus,
    ObserverRuntimeStatus,
    ObserverRuntimeMode,
    ObserverMonitoringMode,
    ObserverOutputType,
    ObserverDriftType,
    ObserverSafetyFlag,
    ObserverReportType
)
from usa_signal_bot.core.exceptions import ObserverValidationError

@dataclass
class LockedObserverPolicy:
    policy_id: str
    created_at_utc: str
    require_human_approval: bool
    require_planning_ticket: bool
    locked_runtime: bool
    allow_active_paper: bool
    allow_paper_state_mutation: bool
    allow_paper_orders: bool
    allow_broker_orders: bool
    allow_telegram_real_send: bool
    allow_config_patch: bool
    allowed_output_types: List[ObserverOutputType]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperObserverEnrollment:
    enrollment_id: str
    created_at_utc: str
    status: PaperObserverEnrollmentStatus
    candidate_id: Optional[str]
    planning_ticket_id: Optional[str]
    approval_queue_item_id: Optional[str]
    source_controlled_planning_review_id: Optional[str]
    source_approval_status: Optional[str]
    policy: Optional[LockedObserverPolicy]
    allowed_for_active_paper: bool
    allowed_for_broker_execution: bool
    allowed_for_paper_state_mutation: bool
    allowed_for_config_patch: bool
    safety_flags: List[ObserverSafetyFlag]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ObserverRuntimeContext:
    context_id: str
    created_at_utc: str
    enrollment_id: Optional[str]
    candidate_id: Optional[str]
    runtime_mode: ObserverRuntimeMode
    monitoring_mode: ObserverMonitoringMode
    read_only_paper_snapshot: Dict[str, Any]
    candidate_metadata: Dict[str, Any]
    output_path: Optional[str]
    locked: bool
    allow_active_paper: bool
    allow_paper_state_mutation: bool
    allow_paper_orders: bool
    allow_broker_orders: bool
    allow_telegram_real_send: bool
    allow_config_patch: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ObserverOutput:
    output_id: str
    created_at_utc: str
    output_type: ObserverOutputType
    symbol: Optional[str]
    status: str
    summary: Dict[str, Any]
    payload: Dict[str, Any]
    is_real_order: bool
    mutates_paper_state: bool
    sends_to_broker: bool
    sends_telegram_real: bool
    safety_flags: List[ObserverSafetyFlag]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ObserverDriftEvent:
    drift_id: str
    created_at_utc: str
    drift_type: ObserverDriftType
    symbol: Optional[str]
    baseline_value: Any
    observer_value: Any
    delta: Any
    severity: str
    description: str
    safety_flags: List[ObserverSafetyFlag]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ObserverRuntimeSession:
    session_id: str
    created_at_utc: str
    status: ObserverRuntimeStatus
    context: Optional[ObserverRuntimeContext]
    outputs: List[ObserverOutput] = field(default_factory=list)
    drift_events: List[ObserverDriftEvent] = field(default_factory=list)
    safety_flags: List[ObserverSafetyFlag] = field(default_factory=list)
    started_at_utc: Optional[str] = None
    completed_at_utc: Optional[str] = None
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ObserverAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    rationale: str
    evidence_refs: List[str] = field(default_factory=list)
    safety_flags: List[ObserverSafetyFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperObserverReview:
    review_id: str
    created_at_utc: str
    report_type: ObserverReportType
    enrollments: List[PaperObserverEnrollment] = field(default_factory=list)
    sessions: List[ObserverRuntimeSession] = field(default_factory=list)
    drift_events: List[ObserverDriftEvent] = field(default_factory=list)
    audit_entries: List[ObserverAuditEntry] = field(default_factory=list)
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

import dataclasses

def locked_observer_policy_to_dict(item: LockedObserverPolicy) -> dict:
    return dataclasses.asdict(item)

def paper_observer_enrollment_to_dict(item: PaperObserverEnrollment) -> dict:
    return dataclasses.asdict(item)

def observer_runtime_context_to_dict(item: ObserverRuntimeContext) -> dict:
    return dataclasses.asdict(item)

def observer_output_to_dict(item: ObserverOutput) -> dict:
    return dataclasses.asdict(item)

def observer_drift_event_to_dict(item: ObserverDriftEvent) -> dict:
    return dataclasses.asdict(item)

def observer_runtime_session_to_dict(item: ObserverRuntimeSession) -> dict:
    return dataclasses.asdict(item)

def observer_audit_entry_to_dict(item: ObserverAuditEntry) -> dict:
    return dataclasses.asdict(item)

def paper_observer_review_to_dict(item: PaperObserverReview) -> dict:
    return dataclasses.asdict(item)

def _validate_safety_properties(obj_dict: dict, obj_name: str) -> None:
    expected_false_flags = [
        "allow_active_paper",
        "allow_paper_state_mutation",
        "allow_paper_orders",
        "allow_broker_orders",
        "allow_telegram_real_send",
        "allow_config_patch",
        "allowed_for_active_paper",
        "allowed_for_broker_execution",
        "allowed_for_paper_state_mutation",
        "allowed_for_config_patch",
        "is_real_order",
        "mutates_paper_state",
        "sends_to_broker",
        "sends_telegram_real"
    ]
    for flag in expected_false_flags:
        if flag in obj_dict and obj_dict[flag] is True:
            raise ObserverValidationError(f"{obj_name}.{flag} MUST be False.")

    if "locked_runtime" in obj_dict and obj_dict["locked_runtime"] is False:
        raise ObserverValidationError(f"{obj_name}.locked_runtime MUST be True.")
    if "locked" in obj_dict and obj_dict["locked"] is False:
        raise ObserverValidationError(f"{obj_name}.locked MUST be True.")

def validate_locked_observer_policy(item: LockedObserverPolicy) -> None:
    _validate_safety_properties(locked_observer_policy_to_dict(item), "LockedObserverPolicy")

def validate_paper_observer_enrollment(item: PaperObserverEnrollment) -> None:
    _validate_safety_properties(paper_observer_enrollment_to_dict(item), "PaperObserverEnrollment")

def validate_observer_runtime_context(item: ObserverRuntimeContext) -> None:
    _validate_safety_properties(observer_runtime_context_to_dict(item), "ObserverRuntimeContext")

def validate_observer_output(item: ObserverOutput) -> None:
    _validate_safety_properties(observer_output_to_dict(item), "ObserverOutput")

def validate_observer_runtime_session(item: ObserverRuntimeSession) -> None:
    _validate_safety_properties(observer_runtime_session_to_dict(item), "ObserverRuntimeSession")
    if item.context:
        validate_observer_runtime_context(item.context)
    for out in item.outputs:
        validate_observer_output(out)

def validate_paper_observer_review(item: PaperObserverReview) -> None:
    for enr in item.enrollments:
        validate_paper_observer_enrollment(enr)
    for sess in item.sessions:
        validate_observer_runtime_session(sess)

def create_locked_observer_policy_id(prefix: str = "locked_observer_policy") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_observer_enrollment_id(prefix: str = "paper_observer_enrollment") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_observer_runtime_context_id(prefix: str = "observer_runtime_context") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_observer_output_id(prefix: str = "observer_output") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_observer_drift_id(prefix: str = "observer_drift") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_observer_runtime_session_id(prefix: str = "observer_runtime_session") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_observer_audit_id(prefix: str = "observer_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_observer_review_id(prefix: str = "paper_observer_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
