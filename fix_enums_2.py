import re

with open('usa_signal_bot/core/enums.py', 'r') as f:
    content = f.read()

# Add to NotificationType
if "FREEZE_PREPARATION_REPORT = \"FREEZE_PREPARATION_REPORT\"" not in content:
    content = content.replace(
        "class NotificationType(str, Enum):",
        "class NotificationType(str, Enum):\n    FREEZE_PREPARATION_REPORT = \"FREEZE_PREPARATION_REPORT\"\n    INTEGRATION_REHEARSAL_WARNING = \"INTEGRATION_REHEARSAL_WARNING\"\n    FREEZE_READINESS_WARNING = \"FREEZE_READINESS_WARNING\""
    )

# Add to AlertType
if "FREEZE_PREPARATION_BLOCKED = \"FREEZE_PREPARATION_BLOCKED\"" not in content:
    content = content.replace(
        "class AlertType(str, Enum):",
        "class AlertType(str, Enum):\n    FREEZE_PREPARATION_BLOCKED = \"FREEZE_PREPARATION_BLOCKED\"\n    INTEGRATION_REHEARSAL_BLOCKED = \"INTEGRATION_REHEARSAL_BLOCKED\"\n    FREEZE_READINESS_BLOCKED = \"FREEZE_READINESS_BLOCKED\""
    )

with open('usa_signal_bot/core/enums.py', 'w') as f:
    f.write(content)
