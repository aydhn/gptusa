# Mock models for phase 92
from dataclasses import dataclass, field
from typing import Any

@dataclass
class FinalPaperSafeGateReview:
    review_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
