from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import (
    DiagnosticScope,
    FailureModeType,
    DiagnosticSeverity,
    DiagnosticStatus,
    FailureClusterType,
    RemediationHintType,
    DiagnosticEvidenceQuality,
    DiagnosticReportType
)
import uuid

@dataclass
class DiagnosticEvent:
    event_id: str
    scope: DiagnosticScope
    symbol: Optional[str] = None
    strategy_name: Optional[str] = None
    signal_id: Optional[str] = None
    signal_family: Optional[str] = None
    timestamp_utc: Optional[str] = None
    side: Optional[str] = None
    gross_pnl_usd: Optional[float] = None
    net_pnl_usd: Optional[float] = None
    total_cost_usd: Optional[float] = None
    return_pct: Optional[float] = None
    drawdown_impact_usd: Optional[float] = None
    signal_score: Optional[float] = None
    confidence: Optional[float] = None
    regime_label: Optional[str] = None
    sector: Optional[str] = None
    cluster: Optional[str] = None
    liquidity_bucket: Optional[str] = None
    cost_bucket: Optional[str] = None
    sizing_status: Optional[str] = None
    rebalance_action_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class FailureModeAssessment:
    assessment_id: str
    created_at_utc: str
    failure_mode: FailureModeType
    severity: DiagnosticSeverity
    evidence_quality: DiagnosticEvidenceQuality
    affected_scope: DiagnosticScope
    affected_name: Optional[str] = None
    event_count: int = 0
    loss_count: int = 0
    total_net_loss_usd: Optional[float] = None
    total_cost_drag_usd: Optional[float] = None
    confidence_score: Optional[float] = None
    evidence: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FailureCluster:
    cluster_id: str
    created_at_utc: str
    cluster_type: FailureClusterType
    name: str
    event_count: int
    failure_modes: List[FailureModeType]
    total_net_pnl_usd: Optional[float] = None
    total_cost_usd: Optional[float] = None
    severity: DiagnosticSeverity = DiagnosticSeverity.UNKNOWN
    evidence_quality: DiagnosticEvidenceQuality = DiagnosticEvidenceQuality.UNKNOWN
    representative_events: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StrategyDiagnosticResult:
    diagnostic_id: str
    created_at_utc: str
    strategy_name: str
    status: DiagnosticStatus
    severity: DiagnosticSeverity
    event_count: int
    trade_count: int
    win_rate: Optional[float] = None
    total_net_pnl_usd: Optional[float] = None
    total_cost_usd: Optional[float] = None
    cost_drag_pct: Optional[float] = None
    failure_modes: List[FailureModeAssessment] = field(default_factory=list)
    clusters: List[FailureCluster] = field(default_factory=list)
    remediation_hints: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RemediationHint:
    hint_id: str
    created_at_utc: str
    hint_type: RemediationHintType
    severity: DiagnosticSeverity
    target_scope: DiagnosticScope
    target_name: Optional[str] = None
    title: str = ""
    description: str = ""
    evidence_refs: List[str] = field(default_factory=list)
    safe_action: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DiagnosticScorecard:
    scorecard_id: str
    created_at_utc: str
    diagnostic_status: DiagnosticStatus
    total_event_count: int
    total_failure_count: int
    high_severity_count: int
    critical_severity_count: int
    degraded_strategy_count: int
    noisy_evidence_count: int
    score_components: Dict[str, Optional[float]] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DiagnosticReview:
    review_id: str
    created_at_utc: str
    report_type: DiagnosticReportType
    events: List[DiagnosticEvent] = field(default_factory=list)
    failure_assessments: List[FailureModeAssessment] = field(default_factory=list)
    failure_clusters: List[FailureCluster] = field(default_factory=list)
    strategy_diagnostics: List[StrategyDiagnosticResult] = field(default_factory=list)
    remediation_hints: List[RemediationHint] = field(default_factory=list)
    scorecard: Optional[DiagnosticScorecard] = None
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def diagnostic_event_to_dict(item: DiagnosticEvent) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def failure_mode_assessment_to_dict(item: FailureModeAssessment) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def failure_cluster_to_dict(item: FailureCluster) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def strategy_diagnostic_result_to_dict(item: StrategyDiagnosticResult) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def remediation_hint_to_dict(item: RemediationHint) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def diagnostic_scorecard_to_dict(item: DiagnosticScorecard) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def diagnostic_review_to_dict(item: DiagnosticReview) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def validate_diagnostic_event(item: DiagnosticEvent) -> None:
    from usa_signal_bot.core.exceptions import DiagnosticsValidationError
    if item.signal_score is not None and (item.signal_score < 0 or item.signal_score > 100):
        raise DiagnosticsValidationError("signal_score must be between 0 and 100")
    if item.confidence is not None and (item.confidence < 0 or item.confidence > 100):
        raise DiagnosticsValidationError("confidence must be between 0 and 100")

def validate_failure_mode_assessment(item: FailureModeAssessment) -> None:
    from usa_signal_bot.core.exceptions import DiagnosticsValidationError
    if item.event_count < 0:
        raise DiagnosticsValidationError("event_count cannot be negative")
    if item.loss_count < 0:
        raise DiagnosticsValidationError("loss_count cannot be negative")
    if item.confidence_score is not None and (item.confidence_score < 0 or item.confidence_score > 100):
        raise DiagnosticsValidationError("confidence_score must be between 0 and 100")

def validate_failure_cluster(item: FailureCluster) -> None:
    from usa_signal_bot.core.exceptions import DiagnosticsValidationError
    if item.event_count < 0:
        raise DiagnosticsValidationError("event_count cannot be negative")

def validate_strategy_diagnostic_result(item: StrategyDiagnosticResult) -> None:
    from usa_signal_bot.core.exceptions import DiagnosticsValidationError
    if item.event_count < 0:
        raise DiagnosticsValidationError("event_count cannot be negative")
    if item.trade_count < 0:
        raise DiagnosticsValidationError("trade_count cannot be negative")
    if item.win_rate is not None and (item.win_rate < 0 or item.win_rate > 100):
        raise DiagnosticsValidationError("win_rate must be between 0 and 100")

def validate_remediation_hint(item: RemediationHint) -> None:
    pass

def validate_diagnostic_review(item: DiagnosticReview) -> None:
    pass

def create_diagnostic_event_id(symbol: Optional[str] = None) -> str:
    return f"evt_{uuid.uuid4().hex[:8]}"

def create_failure_mode_assessment_id(mode: FailureModeType) -> str:
    return f"fma_{mode.value}_{uuid.uuid4().hex[:8]}"

def create_failure_cluster_id(name: str) -> str:
    import re
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name).lower()
    return f"fcl_{safe_name}_{uuid.uuid4().hex[:8]}"

def create_strategy_diagnostic_result_id(strategy_name: str) -> str:
    import re
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', strategy_name).lower()
    return f"sdr_{safe_name}_{uuid.uuid4().hex[:8]}"

def create_remediation_hint_id(hint_type: RemediationHintType) -> str:
    return f"rmh_{hint_type.value}_{uuid.uuid4().hex[:8]}"

def create_diagnostic_scorecard_id(prefix: str = "diagnostic_scorecard") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_diagnostic_review_id(prefix: str = "diagnostic_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
