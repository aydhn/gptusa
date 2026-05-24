from pathlib import Path

p = Path("usa_signal_bot/paper_safe_gate/paper_safe_gate_models.py")
content = p.read_text()
to_add = """
class PaperSafeGateRiskFlag(str, Enum):
    INTEGRITY_RISK = "INTEGRITY_RISK"
    BOUNDARY_RISK = "BOUNDARY_RISK"
    UNKNOWN = "UNKNOWN"
"""
if "PaperSafeGateRiskFlag" not in content:
    content += to_add
    p.write_text(content)
