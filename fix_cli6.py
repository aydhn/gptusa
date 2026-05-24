from pathlib import Path

p = Path("usa_signal_bot/paper_safe_gate/paper_safe_gate_models.py")
content = p.read_text()
to_add = """
def create_integrity_audit_id(): return "audit_id"
"""
if "create_integrity_audit_id" not in content:
    content += to_add
    p.write_text(content)
