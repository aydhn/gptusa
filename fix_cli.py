from pathlib import Path
p = Path("usa_signal_bot/paper_safe_gate/paper_safe_gate_models.py")
content = p.read_text()
if "BoundaryCertificateReplayPlan" not in content:
    content += """
@dataclass
class BoundaryCertificateReplayPlan:
    plan_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
"""
    p.write_text(content)
