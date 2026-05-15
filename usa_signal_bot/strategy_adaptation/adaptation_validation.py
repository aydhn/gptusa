
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.exceptions import StrategyAdaptationValidationError

@dataclass
class StrategyAdaptationValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[Any]
    warnings: List[str]
    errors: List[str]
