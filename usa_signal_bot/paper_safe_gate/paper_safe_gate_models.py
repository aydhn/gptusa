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
