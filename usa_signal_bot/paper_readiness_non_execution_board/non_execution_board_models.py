# Mock models for phase 94 output integration
from dataclasses import dataclass, field
from typing import Any

@dataclass
class PaperReadinessNonExecutionBoard:
    board_id: str
    status: str
    decision: str
    board_gates: list[Any] = field(default_factory=list)
    board_assertions: list[Any] = field(default_factory=list)
    activation_denied: bool = True
    activation_allowed: bool = False
    admission_allowed: bool = False
    transition_allowed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RuntimeMapReplayResult:
    result_id: str
    status: str
    outcome: str
    all_dangerous_routes_denied: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class NonExecutionSealIntegrityAudit:
    audit_id: str
    status: str
    decision: str
    seal_hash_matches: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class NonExecutionBoardFullReview:
    review_id: str
    non_execution_board: PaperReadinessNonExecutionBoard
    runtime_replay_result: RuntimeMapReplayResult
    seal_integrity_audit: NonExecutionSealIntegrityAudit
    metadata: dict[str, Any] = field(default_factory=dict)
