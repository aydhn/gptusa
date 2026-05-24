from pathlib import Path

p = Path("usa_signal_bot/paper_safe_gate/paper_safe_gate_models.py")
content = p.read_text()
to_add = """
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
"""
if "PaperSafeGateAssertion" not in content:
    content += to_add
    p.write_text(content)
