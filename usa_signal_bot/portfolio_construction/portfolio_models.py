from dataclasses import dataclass, field
from typing import Any
import uuid
import datetime

from usa_signal_bot.core.enums import (
    SectorClusterSource, ExposureType, ConcentrationRiskLevel,
    PortfolioGuardDecision, PortfolioAllocationStatus,
    PortfolioConstructionMode, PortfolioConstructionReportType
)

@dataclass
class SectorClusterRecord:
    record_id: str
    symbol: str
    sector: str | None
    industry: str | None
    cluster: str | None
    source: SectorClusterSource
    confidence: float | None
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PortfolioCandidate:
    candidate_id: str
    symbol: str
    strategy_name: str | None
    side: str | None
    score: float | None
    confidence: float | None
    requested_notional_usd: float | None
    sized_notional_usd: float | None
    sized_quantity: float | None
    sector: str | None
    cluster: str | None
    regime_label: str | None
    liquidity_bucket: str | None
    cost_bucket: str | None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ExposureSnapshot:
    snapshot_id: str
    created_at_utc: str
    total_equity_usd: float | None
    gross_exposure_usd: float
    net_exposure_usd: float
    long_exposure_usd: float
    short_exposure_usd: float
    symbol_exposures: dict[str, float]
    strategy_exposures: dict[str, float]
    sector_exposures: dict[str, float]
    cluster_exposures: dict[str, float]
    regime_exposures: dict[str, float]
    liquidity_bucket_exposures: dict[str, float]
    cost_bucket_exposures: dict[str, float]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ConcentrationAssessment:
    assessment_id: str
    created_at_utc: str
    exposure_type: ExposureType
    name: str
    exposure_usd: float
    exposure_pct_equity: float | None
    limit_pct_equity: float | None
    risk_level: ConcentrationRiskLevel
    decision: PortfolioGuardDecision
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PortfolioAllocation:
    allocation_id: str
    symbol: str
    strategy_name: str | None
    side: str | None
    initial_notional_usd: float | None
    final_notional_usd: float | None
    final_quantity: float | None
    weight_pct_equity: float | None
    status: PortfolioAllocationStatus
    guard_decisions: list[PortfolioGuardDecision]
    adjustment_reasons: list[str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PortfolioConstructionPlan:
    plan_id: str
    created_at_utc: str
    mode: PortfolioConstructionMode
    candidates: list[PortfolioCandidate]
    allocations: list[PortfolioAllocation]
    exposure_snapshot: ExposureSnapshot | None
    concentration_assessments: list[ConcentrationAssessment]
    conflicts: list[dict[str, Any]]
    total_allocated_notional_usd: float | None
    approved_count: int
    reduced_count: int
    capped_count: int
    suppressed_count: int
    blocked_count: int
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PortfolioConstructionReview:
    review_id: str
    created_at_utc: str
    report_type: PortfolioConstructionReportType
    plan: PortfolioConstructionPlan | None
    exposure_snapshot: ExposureSnapshot | None
    sector_cluster_records: list[SectorClusterRecord]
    concentration_assessments: list[ConcentrationAssessment]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def sector_cluster_record_to_dict(item: SectorClusterRecord) -> dict:
    return {
        "record_id": item.record_id,
        "symbol": item.symbol,
        "sector": item.sector,
        "industry": item.industry,
        "cluster": item.cluster,
        "source": item.source.value if hasattr(item.source, "value") else str(item.source),
        "confidence": item.confidence,
        "notes": item.notes,
        "metadata": item.metadata,
    }

def portfolio_candidate_to_dict(item: PortfolioCandidate) -> dict:
    return {
        "candidate_id": item.candidate_id,
        "symbol": item.symbol,
        "strategy_name": item.strategy_name,
        "side": item.side,
        "score": item.score,
        "confidence": item.confidence,
        "requested_notional_usd": item.requested_notional_usd,
        "sized_notional_usd": item.sized_notional_usd,
        "sized_quantity": item.sized_quantity,
        "sector": item.sector,
        "cluster": item.cluster,
        "regime_label": item.regime_label,
        "liquidity_bucket": item.liquidity_bucket,
        "cost_bucket": item.cost_bucket,
        "metadata": item.metadata,
    }

def exposure_snapshot_to_dict(item: ExposureSnapshot) -> dict:
    return {
        "snapshot_id": item.snapshot_id,
        "created_at_utc": item.created_at_utc,
        "total_equity_usd": item.total_equity_usd,
        "gross_exposure_usd": item.gross_exposure_usd,
        "net_exposure_usd": item.net_exposure_usd,
        "long_exposure_usd": item.long_exposure_usd,
        "short_exposure_usd": item.short_exposure_usd,
        "symbol_exposures": item.symbol_exposures,
        "strategy_exposures": item.strategy_exposures,
        "sector_exposures": item.sector_exposures,
        "cluster_exposures": item.cluster_exposures,
        "regime_exposures": item.regime_exposures,
        "liquidity_bucket_exposures": item.liquidity_bucket_exposures,
        "cost_bucket_exposures": item.cost_bucket_exposures,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def concentration_assessment_to_dict(item: ConcentrationAssessment) -> dict:
    return {
        "assessment_id": item.assessment_id,
        "created_at_utc": item.created_at_utc,
        "exposure_type": item.exposure_type.value if hasattr(item.exposure_type, "value") else str(item.exposure_type),
        "name": item.name,
        "exposure_usd": item.exposure_usd,
        "exposure_pct_equity": item.exposure_pct_equity,
        "limit_pct_equity": item.limit_pct_equity,
        "risk_level": item.risk_level.value if hasattr(item.risk_level, "value") else str(item.risk_level),
        "decision": item.decision.value if hasattr(item.decision, "value") else str(item.decision),
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def portfolio_allocation_to_dict(item: PortfolioAllocation) -> dict:
    return {
        "allocation_id": item.allocation_id,
        "symbol": item.symbol,
        "strategy_name": item.strategy_name,
        "side": item.side,
        "initial_notional_usd": item.initial_notional_usd,
        "final_notional_usd": item.final_notional_usd,
        "final_quantity": item.final_quantity,
        "weight_pct_equity": item.weight_pct_equity,
        "status": item.status.value if hasattr(item.status, "value") else str(item.status),
        "guard_decisions": [g.value if hasattr(g, "value") else str(g) for g in item.guard_decisions],
        "adjustment_reasons": item.adjustment_reasons,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def portfolio_construction_plan_to_dict(item: PortfolioConstructionPlan) -> dict:
    return {
        "plan_id": item.plan_id,
        "created_at_utc": item.created_at_utc,
        "mode": item.mode.value if hasattr(item.mode, "value") else str(item.mode),
        "candidates": [portfolio_candidate_to_dict(c) for c in item.candidates],
        "allocations": [portfolio_allocation_to_dict(a) for a in item.allocations],
        "exposure_snapshot": exposure_snapshot_to_dict(item.exposure_snapshot) if item.exposure_snapshot else None,
        "concentration_assessments": [concentration_assessment_to_dict(c) for c in item.concentration_assessments],
        "conflicts": item.conflicts,
        "total_allocated_notional_usd": item.total_allocated_notional_usd,
        "approved_count": item.approved_count,
        "reduced_count": item.reduced_count,
        "capped_count": item.capped_count,
        "suppressed_count": item.suppressed_count,
        "blocked_count": item.blocked_count,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def portfolio_construction_review_to_dict(item: PortfolioConstructionReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value if hasattr(item.report_type, "value") else str(item.report_type),
        "plan": portfolio_construction_plan_to_dict(item.plan) if item.plan else None,
        "exposure_snapshot": exposure_snapshot_to_dict(item.exposure_snapshot) if item.exposure_snapshot else None,
        "sector_cluster_records": [sector_cluster_record_to_dict(r) for r in item.sector_cluster_records],
        "concentration_assessments": [concentration_assessment_to_dict(c) for c in item.concentration_assessments],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }

def validate_sector_cluster_record(item: SectorClusterRecord) -> None:
    if not item.symbol:
        raise ValueError("SectorClusterRecord symbol is empty")

def validate_portfolio_candidate(item: PortfolioCandidate) -> None:
    if not item.symbol:
        raise ValueError("PortfolioCandidate symbol is empty")
    if item.requested_notional_usd is not None and item.requested_notional_usd < 0:
        raise ValueError("requested_notional_usd cannot be negative")
    if item.sized_notional_usd is not None and item.sized_notional_usd < 0:
        raise ValueError("sized_notional_usd cannot be negative")
    if item.sized_quantity is not None and item.sized_quantity < 0:
        raise ValueError("sized_quantity cannot be negative")
    if item.confidence is not None and (item.confidence < 0 or item.confidence > 100):
        raise ValueError("confidence must be 0-100")

def validate_exposure_snapshot(item: ExposureSnapshot) -> None:
    if item.total_equity_usd is not None and item.total_equity_usd < 0:
        raise ValueError("total_equity_usd cannot be negative")
    if item.gross_exposure_usd < 0:
        raise ValueError("gross_exposure_usd cannot be negative")
    if item.long_exposure_usd < 0:
        raise ValueError("long_exposure_usd cannot be negative")
    if item.short_exposure_usd > 0:
        raise ValueError("short_exposure_usd must be negative or zero")

def validate_concentration_assessment(item: ConcentrationAssessment) -> None:
    if not item.name:
        raise ValueError("ConcentrationAssessment name is empty")
    if item.exposure_pct_equity is not None and item.exposure_pct_equity < 0:
        raise ValueError("exposure_pct_equity cannot be negative")
    if item.limit_pct_equity is not None and item.limit_pct_equity < 0:
        raise ValueError("limit_pct_equity cannot be negative")

def validate_portfolio_allocation(item: PortfolioAllocation) -> None:
    if not item.symbol:
        raise ValueError("PortfolioAllocation symbol is empty")
    if item.initial_notional_usd is not None and item.initial_notional_usd < 0:
        raise ValueError("initial_notional_usd cannot be negative")
    if item.final_notional_usd is not None and item.final_notional_usd < 0:
        raise ValueError("final_notional_usd cannot be negative")
    if item.final_quantity is not None and item.final_quantity < 0:
        raise ValueError("final_quantity cannot be negative")
    if item.weight_pct_equity is not None and (item.weight_pct_equity < 0 or item.weight_pct_equity > 200):
        raise ValueError("weight_pct_equity invalid")

def create_sector_cluster_record_id(symbol: str) -> str:
    return f"sec_rec_{symbol}_{uuid.uuid4().hex[:8]}"

def create_portfolio_candidate_id(symbol: str) -> str:
    return f"port_cand_{symbol}_{uuid.uuid4().hex[:8]}"

def create_exposure_snapshot_id(prefix: str = "exposure_snapshot") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_concentration_assessment_id(name: str) -> str:
    safe_name = "".join(c for c in name if c.isalnum() or c == "_")
    return f"conc_ass_{safe_name}_{uuid.uuid4().hex[:8]}"

def create_portfolio_allocation_id(symbol: str) -> str:
    return f"port_alloc_{symbol}_{uuid.uuid4().hex[:8]}"

def create_portfolio_construction_plan_id(prefix: str = "portfolio_plan") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_portfolio_construction_review_id(prefix: str = "portfolio_construction_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
