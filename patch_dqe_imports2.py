import re

with open("usa_signal_bot/quality/data_quality_evaluator.py", "r") as f:
    content = f.read()

content = "from usa_signal_bot.quality.quality_models import QualityIssue, QualityDimension, QualitySeverity, QualityStatus, create_quality_issue_id\n" + content

with open("usa_signal_bot/quality/data_quality_evaluator.py", "w") as f:
    f.write(content)
