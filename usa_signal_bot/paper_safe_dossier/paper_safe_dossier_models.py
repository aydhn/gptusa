# Mock models for phase 93
from dataclasses import dataclass, field
from typing import Any

@dataclass
class PaperSafeDossierFullReview:
    review_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
