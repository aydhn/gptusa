import re

file_path = "usa_signal_bot/regime_classification/freeze_preparation/phase134_models.py"

with open(file_path, "r") as f:
    content = f.read()

# Make sure dataclasses handles field properly. It might be overridden somewhere.
# No, wait, DriftReportQaRuleResult is not marked as @dataclass!

content = content.replace("class DriftReportQaRuleResult:", "@dataclass\nclass DriftReportQaRuleResult:")

with open(file_path, "w") as f:
    f.write(content)
