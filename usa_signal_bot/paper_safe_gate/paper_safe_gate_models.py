# Mock models for phase 92
from dataclasses import dataclass, field
from typing import Any

@dataclass
class FinalPaperSafeGateReview:
    review_id: str
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BoundaryCertificateReplayPlan:
    plan_id: str
    metadata: dict[str, Any] = field(default_factory=dict)

def create_boundary_replay_plan_id():
    return "plan_id"

def utcnow_iso():
    return "now"

@dataclass
class FrozenEvidenceIntegrityItem:
    item_id: str
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FrozenEvidenceIntegrityAudit:
    audit_id: str
    metadata: dict[str, Any] = field(default_factory=dict)

def create_frozen_evidence_integrity_audit_id(): return "audit_id"

def create_integrity_item_id(): return "item_id"

def create_integrity_audit_id(): return "audit_id"

from enum import Enum
class FrozenEvidenceIntegrityStatus(str, Enum):
    VALIDATED = "VALIDATED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"

class BoundaryCertificateReplayStatus(str, Enum):
    VALIDATED = "VALIDATED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"

class FrozenEvidenceIntegrityDecision(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"

class BoundaryCertificateReplayDecision(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"

class PaperSafeGateRiskFlag(str, Enum):
    INTEGRITY_RISK = "INTEGRITY_RISK"
    BOUNDARY_RISK = "BOUNDARY_RISK"
    UNKNOWN = "UNKNOWN"

@dataclass
class PaperSafeGateRule:
    rule_id: str
    metadata: dict[str, Any] = field(default_factory=dict)

class PaperSafeGateRuleStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"

@dataclass
class BoundaryCertificateReplayResult:
    result_id: str
    metadata: dict[str, Any] = field(default_factory=dict)

def create_paper_safe_rule_id(): return "rule_id"

@dataclass
class PaperSafeGateAssertion:
    assertion_id: str
    metadata: dict[str, Any] = field(default_factory=dict)

class PaperSafeGateAssertionStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"

def create_paper_safe_assertion_id(): return "assertion_id"

@dataclass
class FinalPaperSafeGate:
    gate_id: str
    metadata: dict[str, Any] = field(default_factory=dict)

class FinalPaperSafeGateStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"

class FinalPaperSafeGateDecision(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"

def create_final_paper_safe_gate_id(): return "gate_id"

@dataclass
class PaperSafeGateAuditEntry:
    audit_id: str
    metadata: dict[str, Any] = field(default_factory=dict)

def create_paper_safe_audit_entry_id(): return "audit_id"

def create_final_paper_safe_gate_review_id(): return "review_id"

class PaperSafeGateReportType(str, Enum):
    FULL = "FULL"


# --- Definitions recovered from git history (deleted by an accidental overwrite) ---
import uuid
import json
from dataclasses import asdict
from typing import Dict
from typing import List
from typing import Optional
from datetime import datetime
from datetime import timezone
from usa_signal_bot.core.enums import BoundaryCertificateReplayOutcome
from usa_signal_bot.core.exceptions import PaperSafeGateValidationError
from usa_signal_bot.core.exceptions import BoundaryReplayPlanError


@dataclass
class PaperSafeGateFullReview:
    review_id: 'str'
    created_at_utc: 'str'
    report_type: 'PaperSafeGateReportType'
    gates: 'List[FinalPaperSafeGate]'
    replay_plans: 'List[BoundaryCertificateReplayPlan]'
    replay_results: 'List[BoundaryCertificateReplayResult]'
    integrity_audits: 'List[FrozenEvidenceIntegrityAudit]'
    rules: 'List[PaperSafeGateRule]'
    assertions: 'List[PaperSafeGateAssertion]'
    audit_entries: 'List[PaperSafeGateAuditEntry]'
    output_paths: 'Dict[str, str]'
    warnings: 'List[str]'
    errors: 'List[str]'


def boundary_certificate_replay_plan_to_dict(item: 'BoundaryCertificateReplayPlan') -> 'dict':
    return asdict(item)


def boundary_certificate_replay_result_to_dict(item: 'BoundaryCertificateReplayResult') -> 'dict':
    return asdict(item)


def frozen_evidence_integrity_audit_to_dict(item: 'FrozenEvidenceIntegrityAudit') -> 'dict':
    return asdict(item)


def paper_safe_gate_rule_to_dict(item: 'PaperSafeGateRule') -> 'dict':
    return asdict(item)


def paper_safe_gate_assertion_to_dict(item: 'PaperSafeGateAssertion') -> 'dict':
    return asdict(item)


def final_paper_safe_gate_to_dict(item: 'FinalPaperSafeGate') -> 'dict':
    return asdict(item)


def paper_safe_gate_audit_entry_to_dict(item: 'PaperSafeGateAuditEntry') -> 'dict':
    return asdict(item)


def paper_safe_gate_full_review_to_dict(item: 'PaperSafeGateFullReview') -> 'dict':
    return asdict(item)


def create_boundary_replay_result_id(prefix='boundary_replay_result'):
    return f'{prefix}_{uuid.uuid4().hex[:8]}'


def create_paper_safe_audit_id(prefix='paper_safe_audit'):
    return f'{prefix}_{uuid.uuid4().hex[:8]}'


def create_paper_safe_full_review_id(prefix='paper_safe_full_review'):
    return f'{prefix}_{uuid.uuid4().hex[:8]}'
