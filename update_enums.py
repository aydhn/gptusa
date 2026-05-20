import re

file_path = "usa_signal_bot/core/enums.py"
with open(file_path, "r") as f:
    content = f.read()

new_enums = """
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
"""

content += "\n" + new_enums

content = content.replace(
    '    DRY_RUN_BRIDGE_WARNING = "dry_run_bridge_warning"',
    '    DRY_RUN_BRIDGE_WARNING = "dry_run_bridge_warning"\n    DRY_RUN_BRIDGE_REPORT = "dry_run_bridge_report"\n    DRY_RUN_BRIDGE_SAFETY_WARNING = "dry_run_bridge_safety_warning"\n    HUMAN_REVIEW_CHECKPOINT_WARNING = "human_review_checkpoint_warning"'
)

content = content.replace(
    '    DRY_RUN_BRIDGE_BLOCKED = "dry_run_bridge_blocked"',
    '    DRY_RUN_BRIDGE_BLOCKED = "dry_run_bridge_blocked"\n    DRY_RUN_BRIDGE_REAL_ORDER_RISK = "dry_run_bridge_real_order_risk"\n    HUMAN_REVIEW_CHECKPOINT_REQUIRED = "human_review_checkpoint_required"'
)

with open(file_path, "w") as f:
    f.write(content)
