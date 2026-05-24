import re

with open("usa_signal_bot/quality/quality_models.py", "r") as f:
    content = f.read()

content = content.replace("        advanced_transition_context_score: float = 0.0", "    advanced_transition_context_score: float = 0.0")

with open("usa_signal_bot/quality/quality_models.py", "w") as f:
    f.write(content)
