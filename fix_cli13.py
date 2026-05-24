from pathlib import Path

p = Path("usa_signal_bot/paper_safe_gate/paper_safe_gate_models.py")
content = p.read_text()
to_add = """
def create_paper_safe_rule_id(): return "rule_id"
"""
if "create_paper_safe_rule_id" not in content:
    content += to_add
    p.write_text(content)
