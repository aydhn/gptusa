with open("usa_signal_bot/core/enums.py", "r") as f:
    content = f.read()

append_enums = """
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
"""

if "ObservationWindowStatus" not in content:
    with open("usa_signal_bot/core/enums.py", "a") as f:
        f.write(append_enums)

with open("usa_signal_bot/core/exceptions.py", "a") as f:
    f.write("""
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
""")

with open("usa_signal_bot/app/cli.py", "r") as f:
    content = f.read()

cmd_str = """
    "paper-observation-info", "observation-ingest-dry-run", "observation-ingest-quarantine",
    "observation-window-plan", "observation-window-track", "checkpoint-history", "checkpoint-timeline",
    "telemetry-history", "proposal-history", "risk-history", "blocked-operation-history",
    "notification-safety-history", "observation-score", "quarantine-exit-gates",
    "quarantine-exit-decision", "observation-audit", "observation-review",
    "paper-observation-summary", "paper-observation-latest-review", "paper-observation-validate",
    "paper-observation-notification-preview", "paper-observation-notification-dispatch-dry-run"
"""
if "paper-observation-info" not in content:
    # Basic insertion logic
    content = content.replace(
        'valid_commands = [',
        'valid_commands = [\n    ' + cmd_str + ','
    )
    # Check if there is an unknown command check to insert safe print
    if 'print(f"Executing command: {cmd}")' in content:
        content = content.replace(
            'print(f"Executing command: {cmd}")',
            'print(f"Executing command: {cmd}")\n    if cmd in [' + cmd_str + ']:\n        print("LIMITATION: This action does NOT execute real broker orders, DOES NOT mutate active paper state, and is NOT investment advice.")'
        )
    with open("usa_signal_bot/app/cli.py", "w") as f:
        f.write(content)
