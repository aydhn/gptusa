from pathlib import Path
import re

p = Path("usa_signal_bot/paper_safe_gate/paper_safe_gate_models.py")
content = p.read_text()
to_add = """
@dataclass
class FrozenEvidenceIntegrityItem:
    item_id: str
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FrozenEvidenceIntegrityAudit:
    audit_id: str
    metadata: dict[str, Any] = field(default_factory=dict)

def create_frozen_evidence_integrity_audit_id(): return "audit_id"
"""
if "FrozenEvidenceIntegrityItem" not in content:
    content += to_add
    p.write_text(content)
