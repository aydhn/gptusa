from dataclasses import dataclass, field
from typing import Any, Optional
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    DiagnosticScope, FailureModeType, DiagnosticSeverity,
    DiagnosticStatus, FailureClusterType, RemediationHintType,
    DiagnosticEvidenceQuality, DiagnosticReportType
)

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
    metadata: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass
class FailureModeAssessment:
    assessment_id: str
    created_at_utc: str
    failure_mode: FailureModeType
    severity: DiagnosticSeverity
    evidence_quality: DiagnosticEvidenceQuality
    affected_scope: DiagnosticScope
    affected_name: Optional[str]
    event_count: int
    loss_count: int
    total_net_loss_usd: Optional[float] = None
    total_cost_drag_usd: Optional[float] = None
    confidence_score: Optional[float] = None
    evidence: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FailureCluster:
    cluster_id: str
    created_at_utc: str
    cluster_type: FailureClusterType
    name: str
    event_count: int
    failure_modes: list[FailureModeType]
    severity: DiagnosticSeverity
    evidence_quality: DiagnosticEvidenceQuality
    total_net_pnl_usd: Optional[float] = None
    total_cost_usd: Optional[float] = None
    representative_events: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class StrategyDiagnosticResult:
    diagnostic_id: str
    created_at_utc: str
    strategy_name: str
    status: DiagnosticStatus
    severity: DiagnosticSeverity
    event_count: int
    trade_count: int
    failure_modes: list[FailureModeAssessment] = field(default_factory=list)
    win_rate: Optional[float] = None
    total_net_pnl_usd: Optional[float] = None
    total_cost_usd: Optional[float] = None
    cost_drag_pct: Optional[float] = None
    clusters: list[FailureCluster] = field(default_factory=list)
    remediation_hints: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RemediationHint:
    hint_id: str
    created_at_utc: str
    hint_type: RemediationHintType
    severity: DiagnosticSeverity
    target_scope: DiagnosticScope
    target_name: Optional[str]
    title: str
    description: str
    evidence_refs: list[str] = field(default_factory=list)
    safe_action: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

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
    score_components: dict[str, Optional[float]] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DiagnosticReview:
    review_id: str
    created_at_utc: str
    report_type: DiagnosticReportType
    events: list[DiagnosticEvent] = field(default_factory=list)
    failure_assessments: list[FailureModeAssessment] = field(default_factory=list)
    failure_clusters: list[FailureCluster] = field(default_factory=list)
    strategy_diagnostics: list[StrategyDiagnosticResult] = field(default_factory=list)
    remediation_hints: list[RemediationHint] = field(default_factory=list)
    scorecard: Optional[DiagnosticScorecard] = None
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def create_diagnostic_event_id(symbol: Optional[str] = None) -> str:
    base = f"ev_{uuid.uuid4().hex[:8]}"
    return f"{base}_{symbol}" if symbol else base

def create_failure_mode_assessment_id(mode: FailureModeType) -> str:
    return f"fma_{mode.value}_{uuid.uuid4().hex[:8]}"

def create_failure_cluster_id(name: str) -> str:
    sanitized = name.lower().replace(" ", "_").replace("/", "_")
    return f"fc_{sanitized}_{uuid.uuid4().hex[:8]}"

def create_strategy_diagnostic_result_id(strategy_name: str) -> str:
    sanitized = strategy_name.lower().replace(" ", "_")
    return f"sdr_{sanitized}_{uuid.uuid4().hex[:8]}"

def create_remediation_hint_id(hint_type: RemediationHintType) -> str:
    return f"rh_{hint_type.value}_{uuid.uuid4().hex[:8]}"

def create_diagnostic_scorecard_id(prefix: str = "diagnostic_scorecard") -> str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

def create_diagnostic_review_id(prefix: str = "diagnostic_review") -> str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

def validate_diagnostic_event(item: DiagnosticEvent) -> None:
    pass

def validate_failure_mode_assessment(item: FailureModeAssessment) -> None:
    if item.event_count < 0 or item.loss_count < 0:
        raise ValueError("Counts cannot be negative")
    if item.confidence_score is not None and not (0 <= item.confidence_score <= 100):
        raise ValueError("Confidence score must be 0-100")

def validate_failure_cluster(item: FailureCluster) -> None:
    if item.event_count < 0:
        raise ValueError("Event count cannot be negative")

def validate_strategy_diagnostic_result(item: StrategyDiagnosticResult) -> None:
    if item.event_count < 0 or item.trade_count < 0:
        raise ValueError("Counts cannot be negative")
    if item.win_rate is not None and not (0 <= item.win_rate <= 100):
        raise ValueError("Win rate must be 0-100")

def validate_remediation_hint(item: RemediationHint) -> None:
    pass

def validate_diagnostic_review(item: DiagnosticReview) -> None:
    pass

def diagnostic_event_to_dict(item: DiagnosticEvent) -> dict:
    from dataclasses import asdict
    return asdict(item)

def failure_mode_assessment_to_dict(item: FailureModeAssessment) -> dict:
    from dataclasses import asdict
    return asdict(item)

def failure_cluster_to_dict(item: FailureCluster) -> dict:
    from dataclasses import asdict
    return asdict(item)

def strategy_diagnostic_result_to_dict(item: StrategyDiagnosticResult) -> dict:
    from dataclasses import asdict
    return asdict(item)

def remediation_hint_to_dict(item: RemediationHint) -> dict:
    from dataclasses import asdict
    return asdict(item)

def diagnostic_scorecard_to_dict(item: DiagnosticScorecard) -> dict:
    from dataclasses import asdict
    return asdict(item)

def diagnostic_review_to_dict(item: DiagnosticReview) -> dict:
    from dataclasses import asdict
    return asdict(item)
