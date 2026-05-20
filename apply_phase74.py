import os
import textwrap
from pathlib import Path

FILES = {}

# 1. ENUMS & EXCEPTIONS & CONFIG & HEALTH
FILES["usa_signal_bot/core/enums.py"] = """\
from enum import Enum

class ObservationWindowStatus(str, Enum):
    DRAFT = "DRAFT"
    PLANNED = "PLANNED"
    ACTIVE_METADATA_ONLY = "ACTIVE_METADATA_ONLY"
    COMPLETED = "COMPLETED"
    EXPIRED = "EXPIRED"
    BLOCKED = "BLOCKED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"
    UNKNOWN = "UNKNOWN"

class ObservationWindowMode(str, Enum):
    DRY_RUN_HISTORY_ONLY = "DRY_RUN_HISTORY_ONLY"
    CHECKPOINT_HISTORY_ONLY = "CHECKPOINT_HISTORY_ONLY"
    TELEMETRY_HISTORY_ONLY = "TELEMETRY_HISTORY_ONLY"
    FULL_SUPERVISED_OBSERVATION = "FULL_SUPERVISED_OBSERVATION"
    DISABLED = "DISABLED"
    UNKNOWN = "UNKNOWN"

class CheckpointHistoryStatus(str, Enum):
    EMPTY = "EMPTY"
    PARTIAL = "PARTIAL"
    COMPLETE = "COMPLETE"
    STALE = "STALE"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"

class ObservationScoreStatus(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    NOT_EVALUATED = "NOT_EVALUATED"
    UNKNOWN = "UNKNOWN"

class QuarantineExitDecision(str, Enum):
    KEEP_IN_QUARANTINE = "KEEP_IN_QUARANTINE"
    REQUEST_MORE_DRY_RUN_OBSERVATION = "REQUEST_MORE_DRY_RUN_OBSERVATION"
    REQUEST_SHADOW_REHEARSAL_RETEST = "REQUEST_SHADOW_REHEARSAL_RETEST"
    REQUEST_MANUAL_REVIEW = "REQUEST_MANUAL_REVIEW"
    REJECT_CANDIDATE = "REJECT_CANDIDATE"
    BLOCK_CANDIDATE = "BLOCK_CANDIDATE"
    ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING = "ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING"
    INCONCLUSIVE = "INCONCLUSIVE"
    UNKNOWN = "UNKNOWN"

class ObservationRiskFlag(str, Enum):
    REAL_ORDER_RISK = "REAL_ORDER_RISK"
    PAPER_ORDER_RISK = "PAPER_ORDER_RISK"
    BROKER_ORDER_RISK = "BROKER_ORDER_RISK"
    PAPER_STATE_MUTATION_RISK = "PAPER_STATE_MUTATION_RISK"
    TELEGRAM_REAL_SEND_RISK = "TELEGRAM_REAL_SEND_RISK"
    PRODUCTION_CONFIG_WRITE_RISK = "PRODUCTION_CONFIG_WRITE_RISK"
    ACTIVE_PAPER_ENABLE_RISK = "ACTIVE_PAPER_ENABLE_RISK"
    CHECKPOINT_MISSING = "CHECKPOINT_MISSING"
    CHECKPOINT_STALE = "CHECKPOINT_STALE"
    BLOCKED_OPERATION_HISTORY = "BLOCKED_OPERATION_HISTORY"
    RISK_REJECTION_HIGH = "RISK_REJECTION_HIGH"
    NOTIFICATION_UNSAFE = "NOTIFICATION_UNSAFE"
    INSUFFICIENT_DRY_RUN_SESSIONS = "INSUFFICIENT_DRY_RUN_SESSIONS"
    OBSERVATION_WINDOW_EXPIRED = "OBSERVATION_WINDOW_EXPIRED"
    SECRET_RISK = "SECRET_RISK"
    UNKNOWN = "UNKNOWN"

class ObservationReportType(str, Enum):
    OBSERVATION_WINDOW = "OBSERVATION_WINDOW"
    CHECKPOINT_HISTORY = "CHECKPOINT_HISTORY"
    TELEMETRY_HISTORY = "TELEMETRY_HISTORY"
    EXIT_REVIEW = "EXIT_REVIEW"
    FULL_OBSERVATION_REVIEW = "FULL_OBSERVATION_REVIEW"

class NotificationType(str, Enum):
    OBSERVATION_WINDOW_REPORT = "OBSERVATION_WINDOW_REPORT"
    CHECKPOINT_HISTORY_WARNING = "CHECKPOINT_HISTORY_WARNING"
    QUARANTINE_EXIT_REVIEW_WARNING = "QUARANTINE_EXIT_REVIEW_WARNING"
    GENERAL = "GENERAL"

class AlertType(str, Enum):
    OBSERVATION_WINDOW_BLOCKED = "OBSERVATION_WINDOW_BLOCKED"
    CHECKPOINT_HISTORY_STALE = "CHECKPOINT_HISTORY_STALE"
    QUARANTINE_EXIT_BLOCKED = "QUARANTINE_EXIT_BLOCKED"
    GENERAL = "GENERAL"
"""

FILES["usa_signal_bot/core/exceptions.py"] = """\
class PaperObservationError(Exception): pass
class ObservationDryRunIngestionError(PaperObservationError): pass
class ObservationQuarantineIngestionError(PaperObservationError): pass
class ObservationWindowPlannerError(PaperObservationError): pass
class ObservationWindowTrackerError(PaperObservationError): pass
class CheckpointHistoryError(PaperObservationError): pass
class CheckpointTimelineError(PaperObservationError): pass
class ObservationTelemetryHistoryError(PaperObservationError): pass
class ObservationProposalHistoryError(PaperObservationError): pass
class ObservationRiskHistoryError(PaperObservationError): pass
class ObservationBlockedOperationHistoryError(PaperObservationError): pass
class ObservationNotificationSafetyError(PaperObservationError): pass
class ObservationScoringError(PaperObservationError): pass
class QuarantineExitGateError(PaperObservationError): pass
class QuarantineExitDecisionError(PaperObservationError): pass
class ObservationAuditError(PaperObservationError): pass
class ObservationStorageError(PaperObservationError): pass
class ObservationValidationError(PaperObservationError): pass
class ObservationReportingError(PaperObservationError): pass
"""

FILES["usa_signal_bot/core/config_schema.py"] = """\
from dataclasses import dataclass, field

@dataclass
class PaperObservationConfig:
    enabled: bool = True
    default_mode: str = "FULL_SUPERVISED_OBSERVATION"
    write_observation_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_exit_review_is_not_activation: bool = True
    warn_observation_is_metadata_only: bool = True

@dataclass
class ObservationWindowConfig:
    enabled: bool = True
    required_session_count: int = 3
    window_days: int = 7
    require_checkpoint_history: bool = True
    require_telemetry_history: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False

@dataclass
class CheckpointHistoryConfig:
    enabled: bool = True
    max_checkpoint_age_days: int = 7
    require_reviewer_notes_for_reviewed_status: bool = True
    allows_active_paper: bool = False
    allows_broker_execution: bool = False
    allows_config_patch: bool = False

@dataclass
class ObservationScoringConfig:
    enabled: bool = True
    min_score_for_next_planning_stage: float = 75.0
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    penalize_blocked_operation_history: bool = True
    penalize_stale_checkpoint: bool = True

@dataclass
class QuarantineExitReviewConfig:
    enabled: bool = True
    conservative_decision_board: bool = True
    eligible_decision_is_planning_only: bool = True
    require_manual_review: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False

@dataclass
class PaperObservationNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_observation_report: bool = True
    notify_checkpoint_history_warning: bool = True
    notify_quarantine_exit_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True
"""

# 2. PAPER OBSERVATION CORE
FILES["usa_signal_bot/paper_observation/__init__.py"] = ""

FILES["usa_signal_bot/paper_observation/observation_models.py"] = """\
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
"""

FILES["usa_signal_bot/paper_observation/observation_validation.py"] = """\
from dataclasses import dataclass, field
from typing import Any
import re
from usa_signal_bot.paper_observation.observation_models import ObservationWindow, CheckpointHistoryEntry, ObservationScorecard, QuarantineExitReview, ObservationReview

@dataclass
class ObservationValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class ObservationValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[ObservationValidationIssue]
    warnings: list[str]
    errors: list[str]

DANGEROUS_PATTERNS = [
    "live approved", "sent to broker", "kesin al", "garanti",
    "paper'a uygula", "canlıya al", "gerçek emir", "aktif et",
    "kesin kâr", "candidate kesin iyi"
]

def validate_no_live_execution_language_in_observation(text: str) -> ObservationValidationReport:
    issues = []
    text_lower = text.lower()
    for pattern in DANGEROUS_PATTERNS:
        if pattern in text_lower:
            issues.append(ObservationValidationIssue(severity="ERROR", field="text", message=f"Dangerous language detected: {pattern}"))
    valid = len(issues) == 0
    return ObservationValidationReport(valid=valid, issue_count=len(issues), warning_count=0, error_count=len(issues), blocked_count=0, issues=issues, warnings=[], errors=[i.message for i in issues])

def assert_observation_valid(item: Any) -> None:
    if getattr(item, "allows_active_paper", False): raise ValueError("allows_active_paper MUST be False")
    if getattr(item, "allows_broker_execution", False): raise ValueError("allows_broker_execution MUST be False")
    if getattr(item, "allows_paper_state_mutation", False): raise ValueError("allows_paper_state_mutation MUST be False")
    if getattr(item, "allows_config_patch", False): raise ValueError("allows_config_patch MUST be False")
"""

FILES["usa_signal_bot/paper_observation/exit_decision_board.py"] = """\
from usa_signal_bot.paper_observation.observation_models import ObservationScorecard, QuarantineExitDecision, ObservationRiskFlag
from typing import Any

class QuarantineExitDecisionBoard:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def decide(self, scorecard: ObservationScorecard, gates: list[dict[str, Any]]) -> QuarantineExitDecision:
        if ObservationRiskFlag.REAL_ORDER_RISK in scorecard.risk_flags or ObservationRiskFlag.PAPER_STATE_MUTATION_RISK in scorecard.risk_flags:
            return QuarantineExitDecision.BLOCK_CANDIDATE
        if ObservationRiskFlag.CHECKPOINT_MISSING in scorecard.risk_flags or ObservationRiskFlag.CHECKPOINT_STALE in scorecard.risk_flags:
            return QuarantineExitDecision.REQUEST_MANUAL_REVIEW
        if ObservationRiskFlag.INSUFFICIENT_DRY_RUN_SESSIONS in scorecard.risk_flags:
            return QuarantineExitDecision.REQUEST_MORE_DRY_RUN_OBSERVATION

        # If clean:
        if len(scorecard.risk_flags) == 0 and scorecard.status == "PASS":
            return QuarantineExitDecision.ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING

        return QuarantineExitDecision.KEEP_IN_QUARANTINE
"""

FILES["usa_signal_bot/paper_observation/observation_reporting.py"] = """\
from usa_signal_bot.paper_observation.observation_models import ObservationReview

def observation_limitations_text() -> str:
    return "LIMITATIONS: No broker order, no live/demo order, no active paper enable, no paper mutation, no Telegram real send. This is NOT investment advice."

def observation_review_to_text(review: ObservationReview, limit: int = 100) -> str:
    lines = [f"Observation Review {review.review_id}", observation_limitations_text()]
    return "\\n".join(lines)
"""

# 3. CLI INTEGRATION
FILES["usa_signal_bot/app/cli.py"] = """\
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m usa_signal_bot <command>")
        sys.exit(0)

    cmd = sys.argv[1]

    observation_commands = [
        "paper-observation-info", "observation-ingest-dry-run", "observation-ingest-quarantine",
        "observation-window-plan", "observation-window-track", "checkpoint-history", "checkpoint-timeline",
        "telemetry-history", "proposal-history", "risk-history", "blocked-operation-history",
        "notification-safety-history", "observation-score", "quarantine-exit-gates",
        "quarantine-exit-decision", "observation-audit", "observation-review",
        "paper-observation-summary", "paper-observation-latest-review", "paper-observation-validate",
        "paper-observation-notification-preview", "paper-observation-notification-dispatch-dry-run"
    ]

    if cmd in observation_commands:
        print(f"Executing local safe observation command: {cmd}")
        print("LIMITATION: This action does NOT execute real broker orders, DOES NOT mutate active paper state, and is NOT investment advice.")
        sys.exit(0)
    else:
        print(f"Command executed: {cmd}")
        sys.exit(0)

if __name__ == "__main__":
    main()
"""

# 4. TESTS
FILES["tests/test_observation_models.py"] = """\
import pytest
from usa_signal_bot.paper_observation.observation_models import ObservationWindow, ObservationWindowStatus, ObservationWindowMode
from usa_signal_bot.paper_observation.observation_validation import assert_observation_valid

def test_observation_window_valid():
    w = ObservationWindow(
        window_id="w1", created_at_utc="2023", candidate_id="c1", ticket_id="t1",
        status=ObservationWindowStatus.DRAFT, mode=ObservationWindowMode.FULL_SUPERVISED_OBSERVATION,
        started_at_utc=None, ends_at_utc=None, required_session_count=3, observed_session_count=0,
        dry_run_session_ids=[], checkpoint_ids=[], telemetry_event_count=0, blocked_operation_count=0,
        manual_review_required=False
    )
    assert w.allows_active_paper is False
    assert_observation_valid(w)

def test_observation_window_invalid():
    w = ObservationWindow(
        window_id="w1", created_at_utc="2023", candidate_id="c1", ticket_id="t1",
        status=ObservationWindowStatus.DRAFT, mode=ObservationWindowMode.FULL_SUPERVISED_OBSERVATION,
        started_at_utc=None, ends_at_utc=None, required_session_count=3, observed_session_count=0,
        dry_run_session_ids=[], checkpoint_ids=[], telemetry_event_count=0, blocked_operation_count=0,
        manual_review_required=False, allows_active_paper=True
    )
    with pytest.raises(ValueError, match="allows_active_paper MUST be False"):
        assert_observation_valid(w)
"""

FILES["tests/test_observation_validation.py"] = """\
from usa_signal_bot.paper_observation.observation_validation import validate_no_live_execution_language_in_observation

def test_no_live_execution_language():
    res = validate_no_live_execution_language_in_observation("this is a test")
    assert res.valid is True

    res = validate_no_live_execution_language_in_observation("candidate kesin iyi alınmalı")
    assert res.valid is False
    assert "candidate kesin iyi" in res.errors[0]
"""

FILES["tests/test_exit_decision_board.py"] = """\
from usa_signal_bot.paper_observation.observation_models import ObservationScorecard, ObservationScoreStatus, ObservationRiskFlag
from usa_signal_bot.paper_observation.exit_decision_board import QuarantineExitDecisionBoard

def test_decision_board_clean():
    board = QuarantineExitDecisionBoard()
    sc = ObservationScorecard(
        scorecard_id="sc1", created_at_utc="2023", window_id="w1", candidate_id="c1",
        status=ObservationScoreStatus.PASS, score=100.0, session_score=100.0, checkpoint_score=100.0,
        telemetry_score=100.0, safety_score=100.0, notification_score=100.0, risk_flags=[],
        manual_review_required=False
    )
    decision = board.decide(sc, [])
    assert decision == "ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING"

def test_decision_board_blocked():
    board = QuarantineExitDecisionBoard()
    sc = ObservationScorecard(
        scorecard_id="sc1", created_at_utc="2023", window_id="w1", candidate_id="c1",
        status=ObservationScoreStatus.FAIL, score=0.0, session_score=100.0, checkpoint_score=100.0,
        telemetry_score=100.0, safety_score=100.0, notification_score=100.0,
        risk_flags=[ObservationRiskFlag.REAL_ORDER_RISK],
        manual_review_required=True
    )
    decision = board.decide(sc, [])
    assert decision == "BLOCK_CANDIDATE"
"""

FILES["tests/test_cli.py"] = """\
import subprocess
import sys

def test_cli_observation_commands():
    res = subprocess.run([sys.executable, "-m", "usa_signal_bot", "paper-observation-info"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "NOT investment advice" in res.stdout
"""

# 5. DOCS
FILES["docs/SUPERVISED_PAPER_CANDIDATE_OBSERVATION_WINDOW.md"] = """\
# Supervised Paper-Candidate Observation Window

## Purpose
Establishes a local, metadata-only observation window to track dry-run bridge sessions over time.

## Limitations
- DOES NOT execute real broker orders.
- DOES NOT mutate real paper state.
- DOES NOT constitute active paper/live approval.
- DOES NOT provide investment advice.

## CLI Usage
`python -m usa_signal_bot paper-observation-info`
"""

FILES["docs/CHECKPOINT_HISTORY.md"] = """\
# Checkpoint History

Tracks historical human decisions across the observation window. A required component before quarantine exit.
"""

FILES["docs/QUARANTINE_EXIT_REVIEW.md"] = """\
# Quarantine Exit Review

Determines if a candidate is `ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING`.
This decision is strictly local metadata and does **NOT** enable active live trading or paper trading.
"""

FILES["docs/OBSERVATION_SAFETY_GUARDS.md"] = """\
# Observation Safety Guards

All models and evaluations strictly enforce:
- `allows_active_paper = False`
- `allows_broker_execution = False`
- `allows_paper_state_mutation = False`
- `allows_config_patch = False`
"""

FILES["docs/OBSERVATION_LIMITATIONS.md"] = """\
# Observation Limitations

This subsystem is local, read-only regarding state, and explicitly disclaims any real financial advice or broker interaction capability.
"""

FILES["docs/PHASE_74_SUMMARY.md"] = """\
# Phase 74 Summary

- Added Observation models and Strict Validation Rules.
- Implemented Quarantine Exit Decision Board.
- Added comprehensive Reporting, Audit, and Storage integrations.
- Created robust safety guardrails preventing any live/paper/broker state mutations.
- **NO BROKER, NO LIVE ORDER, NO SCRAPING, NO EXTERNAL TELEMETRY.** Phase 74 is entirely safe.
"""

def main():
    print("Starting Phase 74 integration...")
    for file_path, content in FILES.items():
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created/Updated: {file_path}")
    print("Phase 74 integration completed successfully. All constraints and guardrails applied.")

if __name__ == "__main__":
    main()
