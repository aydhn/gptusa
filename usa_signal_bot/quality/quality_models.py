from dataclasses import dataclass, field
from typing import Any

@dataclass
class QualityScorecard:
    scorecard_id: str
    paper_readiness_board_dossier_quality_score: float = 0.0
    acceptance_board_seal_score: float = 0.0
    shadow_launch_blocker_score: float = 0.0
    board_dossier_continuity_score: float = 0.0
    board_dossier_non_execution_compliance_score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
