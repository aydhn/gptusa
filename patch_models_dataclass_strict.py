file_path = "usa_signal_bot/regime_classification/freeze_preparation/phase134_models.py"

with open(file_path, "r") as f:
    content = f.read()

content = content.replace("class DriftReportQaRuleResult:", "@dataclass\nclass DriftReportQaRuleResult:")
# Remove duplicate @dataclasses
content = content.replace("@dataclass\n@dataclass", "@dataclass")

with open(file_path, "w") as f:
    f.write(content)
