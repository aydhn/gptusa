import os
import json
from pathlib import Path

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

ensure_dir('usa_signal_bot/paper_pre_rehearsal')
ensure_dir('usa_signal_bot/paper_final_handoff')
ensure_dir('usa_signal_bot/paper_readiness_rehearsal')
ensure_dir('usa_signal_bot/paper_promotion_dossier')
ensure_dir('usa_signal_bot/paper')
ensure_dir('usa_signal_bot/quality')
ensure_dir('usa_signal_bot/observability')
ensure_dir('usa_signal_bot/notifications')
ensure_dir('usa_signal_bot/core')
ensure_dir('usa_signal_bot/app')
ensure_dir('tests')
ensure_dir('docs')
ensure_dir('config')

# Let's create the enums addition script
with open('usa_signal_bot/core/enums.py', 'r') as f:
    enums_content = f.read()

if "PrePaperDryRehearsalStatus" not in enums_content:
    new_enums = """
class PrePaperDryRehearsalStatus(str, Enum):
    DRAFT = "DRAFT"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    ARCHIVED = "ARCHIVED"
    UNKNOWN = "UNKNOWN"

class PrePaperDryRehearsalDecision(str, Enum):
    RUN_GUARDED_PRE_PAPER_DRY_REHEARSAL = "RUN_GUARDED_PRE_PAPER_DRY_REHEARSAL"
    REQUEST_FINAL_HANDOFF_REFRESH = "REQUEST_FINAL_HANDOFF_REFRESH"
    REQUEST_ARCHIVE_INTEGRITY_REFRESH = "REQUEST_ARCHIVE_INTEGRITY_REFRESH"
    REQUEST_MANUAL_REVIEW = "REQUEST_MANUAL_REVIEW"
    REJECT = "REJECT"
    BLOCK = "BLOCK"
    INCONCLUSIVE = "INCONCLUSIVE"
    UNKNOWN = "UNKNOWN"

class MutationFirewallStatus(str, Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    BLOCKING = "BLOCKING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"

class MutationAttemptType(str, Enum):
    PAPER_STATE_WRITE = "PAPER_STATE_WRITE"
    PAPER_ORDER_CREATE = "PAPER_ORDER_CREATE"
    PAPER_POSITION_MUTATION = "PAPER_POSITION_MUTATION"
    PAPER_PORTFOLIO_MUTATION = "PAPER_PORTFOLIO_MUTATION"
    PAPER_CASH_MUTATION = "PAPER_CASH_MUTATION"
    PAPER_EQUITY_MUTATION = "PAPER_EQUITY_MUTATION"
    PAPER_FILL_CREATE = "PAPER_FILL_CREATE"
    BROKER_ORDER_SEND = "BROKER_ORDER_SEND"
    TELEGRAM_REAL_SEND = "TELEGRAM_REAL_SEND"
    PRODUCTION_CONFIG_PATCH = "PRODUCTION_CONFIG_PATCH"
    ACTIVE_PAPER_ENABLE = "ACTIVE_PAPER_ENABLE"
    OBSERVER_UNLOCK = "OBSERVER_UNLOCK"
    ARCHIVE_UNLOCK = "ARCHIVE_UNLOCK"
    FINAL_LOCK_UNLOCK = "FINAL_LOCK_UNLOCK"
    UNKNOWN = "UNKNOWN"

class FirewallAction(str, Enum):
    ALLOW_READ_ONLY = "ALLOW_READ_ONLY"
    DENY_AND_RECORD = "DENY_AND_RECORD"
    BLOCK_SESSION = "BLOCK_SESSION"
    QUARANTINE_OUTPUT = "QUARANTINE_OUTPUT"
    UNKNOWN = "UNKNOWN"

class ActivationDeniedCheckpointStatus(str, Enum):
    DRAFT = "DRAFT"
    CREATED = "CREATED"
    DENIED_BY_DEFAULT = "DENIED_BY_DEFAULT"
    VALIDATED = "VALIDATED"
    BLOCKED = "BLOCKED"
    ARCHIVED = "ARCHIVED"
    UNKNOWN = "UNKNOWN"

class ActivationDeniedDecision(str, Enum):
    DENY_ACTIVATION_AND_CONTINUE_AUDIT = "DENY_ACTIVATION_AND_CONTINUE_AUDIT"
    REQUEST_FIREWALL_REPLAY = "REQUEST_FIREWALL_REPLAY"
    REQUEST_ZERO_MUTATION_AUDIT = "REQUEST_ZERO_MUTATION_AUDIT"
    REQUEST_MANUAL_REVIEW = "REQUEST_MANUAL_REVIEW"
    REJECT = "REJECT"
    BLOCK = "BLOCK"
    INCONCLUSIVE = "INCONCLUSIVE"
    UNKNOWN = "UNKNOWN"

class PrePaperRiskFlag(str, Enum):
    REAL_ORDER_RISK = "REAL_ORDER_RISK"
    PAPER_ORDER_RISK = "PAPER_ORDER_RISK"
    BROKER_ORDER_RISK = "BROKER_ORDER_RISK"
    PAPER_STATE_MUTATION_RISK = "PAPER_STATE_MUTATION_RISK"
    PAPER_POSITION_MUTATION_RISK = "PAPER_POSITION_MUTATION_RISK"
    PAPER_PORTFOLIO_MUTATION_RISK = "PAPER_PORTFOLIO_MUTATION_RISK"
    PAPER_CASH_MUTATION_RISK = "PAPER_CASH_MUTATION_RISK"
    TELEGRAM_REAL_SEND_RISK = "TELEGRAM_REAL_SEND_RISK"
    PRODUCTION_CONFIG_WRITE_RISK = "PRODUCTION_CONFIG_WRITE_RISK"
    ACTIVE_PAPER_ENABLE_RISK = "ACTIVE_PAPER_ENABLE_RISK"
    FIREWALL_DISABLED_RISK = "FIREWALL_DISABLED_RISK"
    FIREWALL_BYPASS_RISK = "FIREWALL_BYPASS_RISK"
    ACTIVATION_ALLOWED_RISK = "ACTIVATION_ALLOWED_RISK"
    ARCHIVE_UNLOCK_RISK = "ARCHIVE_UNLOCK_RISK"
    FINAL_LOCK_UNLOCK_RISK = "FINAL_LOCK_UNLOCK_RISK"
    BASELINE_MUTATION_RISK = "BASELINE_MUTATION_RISK"
    SECRET_RISK = "SECRET_RISK"
    UNKNOWN = "UNKNOWN"

class PrePaperReportType(str, Enum):
    DRY_REHEARSAL_REPORT = "DRY_REHEARSAL_REPORT"
    MUTATION_FIREWALL_REPORT = "MUTATION_FIREWALL_REPORT"
    ACTIVATION_DENIED_CHECKPOINT_REPORT = "ACTIVATION_DENIED_CHECKPOINT_REPORT"
    SAFETY_REVIEW = "SAFETY_REVIEW"
    FULL_PRE_PAPER_REHEARSAL_REVIEW = "FULL_PRE_PAPER_REHEARSAL_REVIEW"
"""
    enums_content += new_enums

# Need to update NotificationType and AlertType safely
import re
if "PRE_PAPER_REHEARSAL_REPORT" not in enums_content:
    enums_content = re.sub(
        r'class NotificationType\(str, Enum\):',
        r'class NotificationType(str, Enum):\n    PRE_PAPER_REHEARSAL_REPORT = "PRE_PAPER_REHEARSAL_REPORT"\n    MUTATION_FIREWALL_WARNING = "MUTATION_FIREWALL_WARNING"\n    ACTIVATION_DENIED_CHECKPOINT_WARNING = "ACTIVATION_DENIED_CHECKPOINT_WARNING"',
        enums_content
    )
if "PRE_PAPER_REHEARSAL_BLOCKED" not in enums_content:
    enums_content = re.sub(
        r'class AlertType\(str, Enum\):',
        r'class AlertType(str, Enum):\n    PRE_PAPER_REHEARSAL_BLOCKED = "PRE_PAPER_REHEARSAL_BLOCKED"\n    MUTATION_FIREWALL_BLOCKED = "MUTATION_FIREWALL_BLOCKED"\n    ACTIVATION_DENIED_CHECKPOINT_BLOCKED = "ACTIVATION_DENIED_CHECKPOINT_BLOCKED"',
        enums_content
    )

with open('usa_signal_bot/core/enums.py', 'w') as f:
    f.write(enums_content)
