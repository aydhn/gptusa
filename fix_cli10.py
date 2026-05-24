from pathlib import Path

p = Path("usa_signal_bot/paper_safe_gate/paper_safe_gate_models.py")
content = p.read_text()
to_add = """
@dataclass
class PaperSafeGateRule:
    rule_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
"""
if "PaperSafeGateRule" not in content:
    content += to_add
    p.write_text(content)
