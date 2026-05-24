import re

with open("usa_signal_bot/quality/quality_models.py", "r") as f:
    content = f.read()

new_fields = """
    phase102_runtime_registry_score: float = 0.0
    phase102_config_surface_score: float = 0.0
    phase102_provider_contract_score: float = 0.0
    phase102_provider_safety_score: float = 0.0
    phase102_non_execution_compliance_score: float = 0.0
"""

if "phase102_runtime_registry_score" not in content:
    content = content.replace("    metadata: dict[str, Any] = field(default_factory=dict)", new_fields + "    metadata: dict[str, Any] = field(default_factory=dict)")
    with open("usa_signal_bot/quality/quality_models.py", "w") as f:
        f.write(content)
