from pathlib import Path
p = Path("usa_signal_bot/paper_safe_gate/paper_safe_gate_models.py")
content = p.read_text()
if "create_boundary_replay_plan_id" not in content:
    content += """
def create_boundary_replay_plan_id():
    return "plan_id"
"""
    p.write_text(content)
