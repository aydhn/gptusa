from pathlib import Path

p = Path("usa_signal_bot/paper_safe_gate/paper_safe_gate_models.py")
content = p.read_text()
to_add = """
class PaperSafeGateRuleStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
"""
if "PaperSafeGateRuleStatus" not in content:
    content += to_add
    p.write_text(content)
