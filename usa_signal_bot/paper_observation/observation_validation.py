from dataclasses import dataclass, field
from typing import Any
import re
from usa_signal_bot.paper_observation.observation_models import ObservationWindow, CheckpointHistoryEntry, ObservationScorecard, QuarantineExitReview, ObservationReview

@dataclass
class ObservationValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class ObservationValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[ObservationValidationIssue]
    warnings: list[str]
    errors: list[str]

DANGEROUS_PATTERNS = [
    "live approved", "sent to broker", "kesin al", "garanti",
    "paper'a uygula", "canlıya al", "gerçek emir", "aktif et",
    "kesin kâr", "candidate kesin iyi"
]

def validate_no_live_execution_language_in_observation(text: str) -> ObservationValidationReport:
    issues = []
    text_lower = text.lower()
    for pattern in DANGEROUS_PATTERNS:
        if pattern in text_lower:
            issues.append(ObservationValidationIssue(severity="ERROR", field="text", message=f"Dangerous language detected: {pattern}"))
    valid = len(issues) == 0
    return ObservationValidationReport(valid=valid, issue_count=len(issues), warning_count=0, error_count=len(issues), blocked_count=0, issues=issues, warnings=[], errors=[i.message for i in issues])

def assert_observation_valid(item: Any) -> None:
    if getattr(item, "allows_active_paper", False): raise ValueError("allows_active_paper MUST be False")
    if getattr(item, "allows_broker_execution", False): raise ValueError("allows_broker_execution MUST be False")
    if getattr(item, "allows_paper_state_mutation", False): raise ValueError("allows_paper_state_mutation MUST be False")
    if getattr(item, "allows_config_patch", False): raise ValueError("allows_config_patch MUST be False")
