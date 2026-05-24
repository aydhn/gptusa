from pathlib import Path

p = Path("usa_signal_bot/paper_safe_gate/paper_safe_gate_models.py")
content = p.read_text()
to_add = """
from enum import Enum
class FrozenEvidenceIntegrityStatus(str, Enum):
    VALIDATED = "VALIDATED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"

class BoundaryCertificateReplayStatus(str, Enum):
    VALIDATED = "VALIDATED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
"""
if "FrozenEvidenceIntegrityStatus" not in content:
    content += to_add
    p.write_text(content)
