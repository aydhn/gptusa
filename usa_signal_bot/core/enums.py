from enum import Enum

class ShadowSessionStatus(str, Enum):
    DRAFT = "DRAFT"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"
    INVALID = "INVALID"
    UNKNOWN = "UNKNOWN"

class ShadowRuntimeMode(str, Enum):
    MOCK_SHADOW = "MOCK_SHADOW"
    SIGNAL_ONLY_SHADOW = "SIGNAL_ONLY_SHADOW"
    PORTFOLIO_SHADOW = "PORTFOLIO_SHADOW"
    REBALANCE_SHADOW = "REBALANCE_SHADOW"
    FULL_PAPER_SHADOW = "FULL_PAPER_SHADOW"
    DISABLED = "DISABLED"
    UNKNOWN = "UNKNOWN"

class ShadowLedgerEventType(str, Enum):
    SESSION_STARTED = "SESSION_STARTED"
    SIGNAL_PREVIEWED = "SIGNAL_PREVIEWED"
    CANDIDATE_SELECTED = "CANDIDATE_SELECTED"
    ORDER_INTENT_CREATED = "ORDER_INTENT_CREATED"
    RISK_GATE_EVALUATED = "RISK_GATE_EVALUATED"
    FILL_SIMULATED = "FILL_SIMULATED"
    POSITION_UPDATED = "POSITION_UPDATED"
    PNL_UPDATED = "PNL_UPDATED"
    REBALANCE_PREVIEWED = "REBALANCE_PREVIEWED"
    NOTIFICATION_PREVIEWED = "NOTIFICATION_PREVIEWED"
    SESSION_COMPLETED = "SESSION_COMPLETED"
    BLOCKED_OPERATION = "BLOCKED_OPERATION"
    UNKNOWN = "UNKNOWN"

class ShadowOrderIntentStatus(str, Enum):
    DRAFT = "DRAFT"
    RISK_APPROVED = "RISK_APPROVED"
    RISK_REJECTED = "RISK_REJECTED"
    SIMULATED = "SIMULATED"
    CANCELLED = "CANCELLED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"

class ShadowFillStatus(str, Enum):
    NOT_FILLED = "NOT_FILLED"
    SIMULATED_FILLED = "SIMULATED_FILLED"
    SIMULATED_PARTIAL = "SIMULATED_PARTIAL"
    SIMULATED_REJECTED = "SIMULATED_REJECTED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"

class ShadowRiskGateStatus(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    UNKNOWN = "UNKNOWN"

class ShadowSafetyFlag(str, Enum):
    REAL_ORDER_RISK = "REAL_ORDER_RISK"
    BROKER_FIELD_RISK = "BROKER_FIELD_RISK"
    PAPER_STATE_MUTATION_RISK = "PAPER_STATE_MUTATION_RISK"
    TELEGRAM_REAL_SEND_RISK = "TELEGRAM_REAL_SEND_RISK"
    PRODUCTION_CONFIG_WRITE_RISK = "PRODUCTION_CONFIG_WRITE_RISK"
    UNSAFE_OUTPUT_PATH = "UNSAFE_OUTPUT_PATH"
    INVALID_SANDBOX_SOURCE = "INVALID_SANDBOX_SOURCE"
    INVALID_BUNDLE_SOURCE = "INVALID_BUNDLE_SOURCE"
    SECRET_RISK = "SECRET_RISK"
    UNKNOWN = "UNKNOWN"

class ShadowReportType(str, Enum):
    SESSION_CONTEXT = "SESSION_CONTEXT"
    LEDGER_REPORT = "LEDGER_REPORT"
    PNL_REPORT = "PNL_REPORT"
    RISK_REPORT = "RISK_REPORT"
    FULL_SHADOW_REHEARSAL_REVIEW = "FULL_SHADOW_REHEARSAL_REVIEW"

class NotificationType(str, Enum):
    QUARANTINE_REPORT = "quarantine_report"
    PROMOTION_TICKET_WARNING = "promotion_ticket_warning"
    DRY_RUN_BRIDGE_WARNING = "dry_run_bridge_warning"
    DRY_RUN_BRIDGE_REPORT = "dry_run_bridge_report"
    DRY_RUN_BRIDGE_SAFETY_WARNING = "dry_run_bridge_safety_warning"
    HUMAN_REVIEW_CHECKPOINT_WARNING = "human_review_checkpoint_warning"
    PAPER_SHADOW_REPORT = "PAPER_SHADOW_REPORT"
    SHADOW_SAFETY_WARNING = "SHADOW_SAFETY_WARNING"
    SHADOW_REHEARSAL_WARNING = "SHADOW_REHEARSAL_WARNING"

class AlertType(str, Enum):
    QUARANTINE_ENROLLMENT_BLOCKED = "quarantine_enrollment_blocked"
    PROMOTION_TICKET_BLOCKED = "promotion_ticket_blocked"
    DRY_RUN_BRIDGE_BLOCKED = "dry_run_bridge_blocked"
    DRY_RUN_BRIDGE_REAL_ORDER_RISK = "dry_run_bridge_real_order_risk"
    HUMAN_REVIEW_CHECKPOINT_REQUIRED = "human_review_checkpoint_required"
    PAPER_SHADOW_BLOCKED = "PAPER_SHADOW_BLOCKED"
    SHADOW_REAL_ORDER_RISK = "SHADOW_REAL_ORDER_RISK"
    SHADOW_SESSION_FAILED = "SHADOW_SESSION_FAILED"

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
    QUARANTINE_REPORT = "quarantine_report"
    PROMOTION_TICKET_WARNING = "promotion_ticket_warning"
    DRY_RUN_BRIDGE_WARNING = "dry_run_bridge_warning"
    DRY_RUN_BRIDGE_REPORT = "dry_run_bridge_report"
    DRY_RUN_BRIDGE_SAFETY_WARNING = "dry_run_bridge_safety_warning"
    HUMAN_REVIEW_CHECKPOINT_WARNING = "human_review_checkpoint_warning"
    SHADOW_GOVERNANCE_REPORT = "SHADOW_GOVERNANCE_REPORT"
    SHADOW_ACCEPTANCE_WARNING = "SHADOW_ACCEPTANCE_WARNING"
    SHADOW_DECISION_WARNING = "SHADOW_DECISION_WARNING"

class AlertType(str, Enum):
    QUARANTINE_ENROLLMENT_BLOCKED = "quarantine_enrollment_blocked"
    PROMOTION_TICKET_BLOCKED = "promotion_ticket_blocked"
    DRY_RUN_BRIDGE_BLOCKED = "dry_run_bridge_blocked"
    DRY_RUN_BRIDGE_REAL_ORDER_RISK = "dry_run_bridge_real_order_risk"
    HUMAN_REVIEW_CHECKPOINT_REQUIRED = "human_review_checkpoint_required"
    SHADOW_GOVERNANCE_BLOCKED = "SHADOW_GOVERNANCE_BLOCKED"
    SHADOW_ACCEPTANCE_FAILED = "SHADOW_ACCEPTANCE_FAILED"
    SHADOW_COMPARISON_INCONCLUSIVE = "SHADOW_COMPARISON_INCONCLUSIVE"


class QuarantineCandidateStatus(str, Enum):
    DRAFT = "draft"
    ELIGIBLE = "eligible"
    ENROLLED = "enrolled"
    WAITING_MANUAL_REVIEW = "waiting_manual_review"
    READY_FOR_SUPERVISED_DRY_RUN = "ready_for_supervised_dry_run"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    EXPIRED = "expired"
    ARCHIVED = "archived"
    UNKNOWN = "unknown"

class QuarantineEnrollmentDecision(str, Enum):
    ENROLL_AS_QUARANTINED_CANDIDATE = "enroll_as_quarantined_candidate"
    REQUEST_MANUAL_REVIEW = "request_manual_review"
    REQUEST_MORE_SHADOW_DATA = "request_more_shadow_data"
    REQUEST_REHEARSAL_RETEST = "request_rehearsal_retest"
    REJECT = "reject"
    BLOCK = "block"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"

class PromotionTicketStatus(str, Enum):
    DRAFT = "draft"
    READ_ONLY_CREATED = "read_only_created"
    WAITING_REVIEW = "waiting_review"
    APPROVED_FOR_SUPERVISED_DRY_RUN_PLANNING = "approved_for_supervised_dry_run_planning"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    EXPIRED = "expired"
    ARCHIVED = "archived"
    UNKNOWN = "unknown"

class BridgePlanStatus(str, Enum):
    DRAFT = "draft"
    READY = "ready"
    VALIDATED = "validated"
    BLOCKED = "blocked"
    EXPIRED = "expired"
    ARCHIVED = "archived"
    UNKNOWN = "unknown"

class BridgeMode(str, Enum):
    READ_ONLY_PREVIEW = "read_only_preview"
    SUPERVISED_DRY_RUN_PLANNING = "supervised_dry_run_planning"
    SHADOW_TO_PAPER_SNAPSHOT_COMPARE = "shadow_to_paper_snapshot_compare"
    QUARANTINE_OUTPUT_ONLY = "quarantine_output_only"
    DISABLED = "disabled"
    UNKNOWN = "unknown"

class BridgeOperation(str, Enum):
    READ_PROMOTION_TICKET = "read_promotion_ticket"
    READ_CANDIDATE_BUNDLE = "read_candidate_bundle"
    READ_SHADOW_GOVERNANCE = "read_shadow_governance"
    READ_PAPER_SNAPSHOT = "read_paper_snapshot"
    BUILD_DRY_RUN_PLAN = "build_dry_run_plan"
    WRITE_QUARANTINE_OUTPUT = "write_quarantine_output"
    GENERATE_NOTIFICATION_PREVIEW = "generate_notification_preview"
    WRITE_PAPER_STATE = "write_paper_state"
    SEND_PAPER_ORDER = "send_paper_order"
    SEND_BROKER_ORDER = "send_broker_order"
    SEND_TELEGRAM_REAL = "send_telegram_real"
    WRITE_PRODUCTION_CONFIG = "write_production_config"
    UNKNOWN = "unknown"

class BridgeOperationDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    WARN = "warn"
    REQUIRE_MANUAL_REVIEW = "require_manual_review"
    UNKNOWN = "unknown"

class QuarantineSafetyFlag(str, Enum):
    REAL_ORDER_RISK = "real_order_risk"
    BROKER_FIELD_RISK = "broker_field_risk"
    PAPER_STATE_MUTATION_RISK = "paper_state_mutation_risk"
    PAPER_ORDER_RISK = "paper_order_risk"
    TELEGRAM_REAL_SEND_RISK = "telegram_real_send_risk"
    PRODUCTION_CONFIG_WRITE_RISK = "production_config_write_risk"
    AUTO_ENABLE_RISK = "auto_enable_risk"
    UNSAFE_OUTPUT_PATH = "unsafe_output_path"
    MISSING_MANUAL_REVIEW = "missing_manual_review"
    MISSING_SHADOW_GOVERNANCE = "missing_shadow_governance"
    LOW_SHADOW_ACCEPTANCE_SCORE = "low_shadow_acceptance_score"
    BLOCKED_SHADOW_DECISION = "blocked_shadow_decision"
    EXPIRED_REVIEW_WINDOW = "expired_review_window"
    SECRET_RISK = "secret_risk"
    UNKNOWN = "unknown"

class QuarantineReportType(str, Enum):
    ENROLLMENT_REVIEW = "enrollment_review"
    PROMOTION_TICKET = "promotion_ticket"
    BRIDGE_PLAN = "bridge_plan"
    SAFETY_REVIEW = "safety_review"
    FULL_QUARANTINE_REVIEW = "full_quarantine_review"


class DryRunBridgeSessionStatus(str, Enum):
    DRAFT = "draft"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    UNKNOWN = "unknown"

class DryRunBridgeMode(str, Enum):
    READ_ONLY_PAPER_SNAPSHOT = "read_only_paper_snapshot"
    CANDIDATE_PROPOSAL_ONLY = "candidate_proposal_only"
    RISK_EVALUATION_ONLY = "risk_evaluation_only"
    NOTIFICATION_PREVIEW_ONLY = "notification_preview_only"
    FULL_SUPERVISED_DRY_RUN = "full_supervised_dry_run"
    DISABLED = "disabled"
    UNKNOWN = "unknown"

class DryRunProposalType(str, Enum):
    SIGNAL_PROPOSAL = "signal_proposal"
    ORDER_INTENT_PROPOSAL = "order_intent_proposal"
    PORTFOLIO_PROPOSAL = "portfolio_proposal"
    RISK_PROPOSAL = "risk_proposal"
    REBALANCE_PROPOSAL = "rebalance_proposal"
    NOTIFICATION_PROPOSAL = "notification_proposal"
    UNKNOWN = "unknown"

class DryRunProposalStatus(str, Enum):
    CREATED = "created"
    RISK_ACCEPTED = "risk_accepted"
    RISK_WARNING = "risk_warning"
    RISK_REJECTED = "risk_rejected"
    BLOCKED = "blocked"
    DISCARDED = "discarded"
    UNKNOWN = "unknown"

class BridgeTelemetryEventType(str, Enum):
    SESSION_STARTED = "session_started"
    QUARANTINE_LOADED = "quarantine_loaded"
    TICKET_LOADED = "ticket_loaded"
    BRIDGE_PLAN_LOADED = "bridge_plan_loaded"
    PAPER_SNAPSHOT_READ = "paper_snapshot_read"
    PROPOSAL_GENERATED = "proposal_generated"
    RISK_EVALUATED = "risk_evaluated"
    NOTIFICATION_PREVIEWED = "notification_previewed"
    OUTPUT_WRITTEN = "output_written"
    BLOCKED_OPERATION_ATTEMPTED = "blocked_operation_attempted"
    HUMAN_CHECKPOINT_CREATED = "human_checkpoint_created"
    HUMAN_CHECKPOINT_UPDATED = "human_checkpoint_updated"
    SESSION_COMPLETED = "session_completed"
    SESSION_BLOCKED = "session_blocked"
    UNKNOWN = "unknown"

class HumanReviewCheckpointStatus(str, Enum):
    REQUIRED = "required"
    WAITING_REVIEW = "waiting_review"
    REVIEWED_WITH_NOTES = "reviewed_with_notes"
    ACCEPTED_FOR_OBSERVATION_ONLY = "accepted_for_observation_only"
    REQUEST_CHANGES = "request_changes"
    REJECTED = "rejected"
    EXPIRED = "expired"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"

class DryRunBridgeSafetyFlag(str, Enum):
    REAL_ORDER_RISK = "real_order_risk"
    PAPER_ORDER_RISK = "paper_order_risk"
    BROKER_ORDER_RISK = "broker_order_risk"
    PAPER_STATE_MUTATION_RISK = "paper_state_mutation_risk"
    TELEGRAM_REAL_SEND_RISK = "telegram_real_send_risk"
    PRODUCTION_CONFIG_WRITE_RISK = "production_config_write_risk"
    ACTIVE_PAPER_ENABLE_RISK = "active_paper_enable_risk"
    UNSAFE_OUTPUT_PATH = "unsafe_output_path"
    MISSING_PROMOTION_TICKET = "missing_promotion_ticket"
    MISSING_QUARANTINE_CANDIDATE = "missing_quarantine_candidate"
    MISSING_BRIDGE_PLAN = "missing_bridge_plan"
    EXPIRED_TICKET = "expired_ticket"
    MISSING_HUMAN_REVIEW = "missing_human_review"
    SECRET_RISK = "secret_risk"
    UNKNOWN = "unknown"

class DryRunBridgeReportType(str, Enum):
    SESSION_REPORT = "session_report"
    TELEMETRY_REPORT = "telemetry_report"
    CHECKPOINT_REPORT = "checkpoint_report"
    SAFETY_REPORT = "safety_report"
    FULL_DRY_RUN_BRIDGE_REVIEW = "full_dry_run_bridge_review"

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
