import re
from pathlib import Path

path = Path("usa_signal_bot/core/enums.py")
content = path.read_text()

# Append missing UNKNOWN to FullSystemIntegrationReportType
new_content = content.replace(
    'FULL_PHASE158_REVIEW = "FULL_PHASE158_REVIEW"',
    'FULL_PHASE158_REVIEW = "FULL_PHASE158_REVIEW"\n    UNKNOWN = "UNKNOWN"'
)

path.write_text(new_content)
