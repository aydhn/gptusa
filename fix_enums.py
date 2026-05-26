import re

with open('usa_signal_bot/core/enums.py', 'r') as f:
    content = f.read()

# Add UNKNOWN to ProviderFreezeReportType
if 'UNKNOWN = "UNKNOWN"' not in content.split('class ProviderFreezeReportType(str, Enum):')[1].split('class ')[0]:
    content = content.replace(
        'class ProviderFreezeReportType(str, Enum):',
        'class ProviderFreezeReportType(str, Enum):\n    UNKNOWN = "UNKNOWN"'
    )

with open('usa_signal_bot/core/enums.py', 'w') as f:
    f.write(content)
