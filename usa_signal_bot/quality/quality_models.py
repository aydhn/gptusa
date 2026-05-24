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
    advanced_transition_context_score: float = 0.0
    handoff_freeze_ingestion_score: float = 0.0
    runtime_boundary_score: float = 0.0
    module_inventory_score: float = 0.0
    config_consolidation_score: float = 0.0
    phase101_non_execution_compliance_score: float = 0.0

    phase102_runtime_registry_score: float = 0.0
    phase102_config_surface_score: float = 0.0
    phase102_provider_contract_score: float = 0.0
    phase102_provider_safety_score: float = 0.0
    phase102_non_execution_compliance_score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class QualityDimension:
    GOVERNANCE = "GOVERNANCE"

class QualitySeverity:
    LOW = "LOW"
    HIGH = "HIGH"

class QualityStatus:
    WARN = "WARN"
    ERROR = "ERROR"

@dataclass
class QualityIssue:
    issue_id: str
    dimension: str
    severity: str
    status: str
    title: str
    message: str

def create_quality_issue_id() -> str:
    return "qi_test"
