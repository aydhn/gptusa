from pathlib import Path
p = Path("usa_signal_bot/paper_safe_gate/paper_safe_gate_models.py")
content = p.read_text()
if "utcnow_iso" not in content:
    content += """
def utcnow_iso():
    return "now"
"""
    p.write_text(content)
