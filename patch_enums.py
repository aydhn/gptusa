import re

with open("usa_signal_bot/core/enums.py", "r") as f:
    content = f.read()

to_append = """
from enum import Enum

class RepairItemType(Enum):
    CODE_FIX = "code_fix"
    CONFIG_CHANGE = "config_change"
    DATA_FIX = "data_fix"

class RepairPriority(Enum):
    LOW = "low"
    HIGH = "high"

class RepairStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"

class HypothesisStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"

class HypothesisConfidence(Enum):
    LOW = "low"
    HIGH = "high"

class ExperimentType(Enum):
    BACKTEST = "backtest"

class ExperimentScope(Enum):
    LOCAL = "local"

class ExperimentStatus(Enum):
    PENDING = "pending"

class AcceptanceGateType(Enum):
    MANUAL = "manual"

class AcceptanceGateStatus(Enum):
    PASS = "pass"

class ResearchRiskLevel(Enum):
    LOW = "low"

class ResearchWorkflowReportType(Enum):
    WEEKLY = "weekly"
"""

if "RepairItemType" not in content:
    with open("usa_signal_bot/core/enums.py", "a") as f:
        f.write(to_append)

print("Enums patched.")
