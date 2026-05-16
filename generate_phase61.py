import os
import sys

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created {path}")

# --- portfolio_construction/portfolio_models.py ---
portfolio_models_code = """from dataclasses import dataclass, field
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
"""

write_file("usa_signal_bot/portfolio_construction/portfolio_models.py", portfolio_models_code)

# --- portfolio_construction/sector_cluster_registry.py ---
registry_code = """import json
from pathlib import Path
from usa_signal_bot.portfolio_construction.portfolio_models import SectorClusterRecord
from usa_signal_bot.core.enums import SectorClusterSource

def load_sector_cluster_registry(path: Path) -> list[SectorClusterRecord]:
    if not path.exists():
        return []
    records = []
    try:
        if path.suffix == ".jsonl":
            with open(path, "r") as f:
                for line in f:
                    if not line.strip(): continue
                    data = json.loads(line)
                    records.append(SectorClusterRecord(
                        record_id=data.get("record_id", ""),
                        symbol=data.get("symbol", ""),
                        sector=data.get("sector"),
                        industry=data.get("industry"),
                        cluster=data.get("cluster"),
                        source=SectorClusterSource(data.get("source", "UNKNOWN")) if data.get("source") else SectorClusterSource.UNKNOWN,
                        confidence=data.get("confidence"),
                        notes=data.get("notes", []),
                        metadata=data.get("metadata", {})
                    ))
        else:
            with open(path, "r") as f:
                data_list = json.load(f)
            for data in data_list:
                records.append(SectorClusterRecord(
                    record_id=data.get("record_id", ""),
                    symbol=data.get("symbol", ""),
                    sector=data.get("sector"),
                    industry=data.get("industry"),
                    cluster=data.get("cluster"),
                    source=SectorClusterSource(data.get("source", "UNKNOWN")) if data.get("source") else SectorClusterSource.UNKNOWN,
                    confidence=data.get("confidence"),
                    notes=data.get("notes", []),
                    metadata=data.get("metadata", {})
                ))
    except Exception:
        pass
    return records

def write_sector_cluster_registry_example(path: Path) -> Path:
    from usa_signal_bot.portfolio_construction.portfolio_models import create_sector_cluster_record_id
    examples = [
        {"symbol": "AAPL", "sector": "technology", "industry": "hardware", "cluster": "mega_cap_tech", "source": "MANUAL_REGISTRY", "confidence": 100.0},
        {"symbol": "MSFT", "sector": "technology", "industry": "software", "cluster": "mega_cap_tech", "source": "MANUAL_REGISTRY", "confidence": 100.0},
        {"symbol": "NVDA", "sector": "technology", "industry": "semiconductors", "cluster": "ai_semis", "source": "MANUAL_REGISTRY", "confidence": 100.0},
        {"symbol": "XOM", "sector": "energy", "industry": "integrated_energy", "cluster": "energy", "source": "MANUAL_REGISTRY", "confidence": 90.0},
        {"symbol": "JPM", "sector": "financials", "industry": "banks", "cluster": "large_banks", "source": "MANUAL_REGISTRY", "confidence": 95.0},
        {"symbol": "UNH", "sector": "healthcare", "industry": "managed_care", "cluster": "healthcare", "source": "MANUAL_REGISTRY", "confidence": 90.0},
        {"symbol": "SPY", "sector": "broad_market", "industry": "etf", "cluster": "index_proxy", "source": "MANUAL_REGISTRY", "confidence": 90.0},
        {"symbol": "QQQ", "sector": "broad_market", "industry": "etf", "cluster": "growth_index_proxy", "source": "MANUAL_REGISTRY", "confidence": 90.0},
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump([
            {
                "record_id": create_sector_cluster_record_id(ex["symbol"]),
                **ex
            } for ex in examples
        ], f, indent=2)
    return path

def merge_sector_cluster_records(primary: list[SectorClusterRecord], secondary: list[SectorClusterRecord]) -> list[SectorClusterRecord]:
    merged = {}
    for r in secondary:
        merged[r.symbol] = r
    for r in primary:
        merged[r.symbol] = r
    return list(merged.values())

def sector_cluster_record_for_symbol(records: list[SectorClusterRecord], symbol: str) -> SectorClusterRecord | None:
    for r in records:
        if r.symbol == symbol:
            return r
    return None

def sector_cluster_registry_to_text(records: list[SectorClusterRecord], limit: int = 100) -> str:
    lines = [f"Sector Cluster Registry (Records: {len(records)})"]
    for i, r in enumerate(records[:limit]):
        lines.append(f"  {r.symbol}: sector={r.sector}, cluster={r.cluster}, source={r.source.value if hasattr(r.source, 'value') else str(r.source)}")
    if len(records) > limit:
        lines.append(f"  ... and {len(records) - limit} more.")
    lines.append("")
    lines.append("Note: Sector/cluster map is a local proxy and gives no official classification guarantees.")
    return "\\n".join(lines)
"""

write_file("usa_signal_bot/portfolio_construction/sector_cluster_registry.py", registry_code)

# --- portfolio_construction/sector_cluster_resolver.py ---
resolver_code = """from usa_signal_bot.portfolio_construction.portfolio_models import SectorClusterRecord, PortfolioCandidate, create_sector_cluster_record_id
from usa_signal_bot.core.enums import SectorClusterSource

class SectorClusterResolver:
    def __init__(self, records: list[SectorClusterRecord] | None = None, config: dict | None = None):
        self.records = records or []
        self.config = config or {}
        self.unknown_sector_bucket = self.config.get("unknown_sector_bucket", "unknown_sector")
        self.unknown_cluster_bucket = self.config.get("unknown_cluster_bucket", "unknown_cluster")
        self.use_etf_proxy = self.config.get("use_etf_proxy_heuristic", True)

    def resolve(self, symbol: str) -> SectorClusterRecord:
        for r in self.records:
            if r.symbol == symbol:
                return r

        # ETF proxy heuristic
        if self.use_etf_proxy and symbol in ["SPY", "QQQ", "IWM", "DIA", "VOO", "VTI"]:
            return SectorClusterRecord(
                record_id=create_sector_cluster_record_id(symbol),
                symbol=symbol,
                sector="broad_market",
                industry="etf",
                cluster="index_proxy",
                source=SectorClusterSource.ETF_PROXY_HEURISTIC,
                confidence=80.0
            )

        return SectorClusterRecord(
            record_id=create_sector_cluster_record_id(symbol),
            symbol=symbol,
            sector=self.unknown_sector_bucket,
            industry=None,
            cluster=self.unknown_cluster_bucket,
            source=SectorClusterSource.UNKNOWN,
            confidence=0.0
        )

    def resolve_many(self, symbols: list[str]) -> list[SectorClusterRecord]:
        return [self.resolve(s) for s in symbols]

    def sector_for_symbol(self, symbol: str) -> str | None:
        return self.resolve(symbol).sector

    def cluster_for_symbol(self, symbol: str) -> str | None:
        return self.resolve(symbol).cluster

    def resolve_candidate(self, candidate: PortfolioCandidate) -> PortfolioCandidate:
        rec = self.resolve(candidate.symbol)
        candidate.sector = rec.sector
        candidate.cluster = rec.cluster
        return candidate
"""

write_file("usa_signal_bot/portfolio_construction/sector_cluster_resolver.py", resolver_code)

# --- portfolio_construction/exposure_calculator.py ---
calc_code = """from usa_signal_bot.portfolio_construction.portfolio_models import ExposureSnapshot, PortfolioCandidate, PortfolioAllocation, create_exposure_snapshot_id
import datetime

def _get_notional(item: any) -> float:
    if isinstance(item, PortfolioCandidate):
        return item.sized_notional_usd or item.requested_notional_usd or 0.0
    elif isinstance(item, PortfolioAllocation):
        return item.final_notional_usd or item.initial_notional_usd or 0.0
    elif isinstance(item, dict):
        return item.get("final_notional_usd", item.get("sized_notional_usd", item.get("notional_usd", 0.0)))
    return 0.0

def _get_symbol(item: any) -> str:
    if isinstance(item, PortfolioCandidate) or isinstance(item, PortfolioAllocation):
        return item.symbol
    elif isinstance(item, dict):
        return item.get("symbol", "UNKNOWN")
    return "UNKNOWN"

def _get_side(item: any) -> str:
    if isinstance(item, PortfolioCandidate) or isinstance(item, PortfolioAllocation):
        return item.side or "LONG"
    elif isinstance(item, dict):
        return item.get("side", "LONG")
    return "LONG"

def _get_attr(item: any, attr: str, default: str = "UNKNOWN") -> str:
    if hasattr(item, attr):
        val = getattr(item, attr)
        return val if val else default
    elif isinstance(item, dict):
        return item.get(attr, default)
    return default

def calculate_gross_exposure_usd(items: list[any]) -> float:
    return sum(abs(_get_notional(i)) for i in items)

def calculate_long_exposure_usd(items: list[any]) -> float:
    return sum(abs(_get_notional(i)) for i in items if _get_side(i).upper() == "LONG")

def calculate_short_exposure_usd(items: list[any]) -> float:
    return -sum(abs(_get_notional(i)) for i in items if _get_side(i).upper() == "SHORT")

def calculate_net_exposure_usd(items: list[any]) -> float:
    return calculate_long_exposure_usd(items) + calculate_short_exposure_usd(items)

def group_exposure_by_symbol(items: list[any]) -> dict[str, float]:
    res = {}
    for i in items:
        sym = _get_symbol(i)
        notional = _get_notional(i)
        side = _get_side(i).upper()
        if side == "SHORT": notional = -abs(notional)
        else: notional = abs(notional)
        res[sym] = res.get(sym, 0.0) + notional
    return res

def group_exposure_by_strategy(items: list[any]) -> dict[str, float]:
    res = {}
    for i in items:
        strat = _get_attr(i, "strategy_name", "UNKNOWN")
        notional = abs(_get_notional(i))
        res[strat] = res.get(strat, 0.0) + notional
    return res

def group_exposure_by_sector(items: list[any]) -> dict[str, float]:
    res = {}
    for i in items:
        sec = _get_attr(i, "sector", "UNKNOWN")
        notional = abs(_get_notional(i))
        res[sec] = res.get(sec, 0.0) + notional
    return res

def group_exposure_by_cluster(items: list[any]) -> dict[str, float]:
    res = {}
    for i in items:
        clus = _get_attr(i, "cluster", "UNKNOWN")
        notional = abs(_get_notional(i))
        res[clus] = res.get(clus, 0.0) + notional
    return res

def group_exposure_by_regime(items: list[any]) -> dict[str, float]:
    res = {}
    for i in items:
        reg = _get_attr(i, "regime_label", "UNKNOWN")
        notional = abs(_get_notional(i))
        res[reg] = res.get(reg, 0.0) + notional
    return res

def group_exposure_by_liquidity_bucket(items: list[any]) -> dict[str, float]:
    res = {}
    for i in items:
        reg = _get_attr(i, "liquidity_bucket", "UNKNOWN")
        notional = abs(_get_notional(i))
        res[reg] = res.get(reg, 0.0) + notional
    return res

def group_exposure_by_cost_bucket(items: list[any]) -> dict[str, float]:
    res = {}
    for i in items:
        reg = _get_attr(i, "cost_bucket", "UNKNOWN")
        notional = abs(_get_notional(i))
        res[reg] = res.get(reg, 0.0) + notional
    return res

def exposure_pct_equity(exposure_usd: float, total_equity_usd: float | None) -> float | None:
    if not total_equity_usd or total_equity_usd <= 0: return None
    return (exposure_usd / total_equity_usd) * 100.0

def calculate_exposure_snapshot(candidates_or_allocations: list[any], total_equity_usd: float | None = None) -> ExposureSnapshot:
    return ExposureSnapshot(
        snapshot_id=create_exposure_snapshot_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        total_equity_usd=total_equity_usd,
        gross_exposure_usd=calculate_gross_exposure_usd(candidates_or_allocations),
        net_exposure_usd=calculate_net_exposure_usd(candidates_or_allocations),
        long_exposure_usd=calculate_long_exposure_usd(candidates_or_allocations),
        short_exposure_usd=calculate_short_exposure_usd(candidates_or_allocations),
        symbol_exposures=group_exposure_by_symbol(candidates_or_allocations),
        strategy_exposures=group_exposure_by_strategy(candidates_or_allocations),
        sector_exposures=group_exposure_by_sector(candidates_or_allocations),
        cluster_exposures=group_exposure_by_cluster(candidates_or_allocations),
        regime_exposures=group_exposure_by_regime(candidates_or_allocations),
        liquidity_bucket_exposures=group_exposure_by_liquidity_bucket(candidates_or_allocations),
        cost_bucket_exposures=group_exposure_by_cost_bucket(candidates_or_allocations),
        warnings=[],
        errors=[],
        metadata={}
    )

def exposure_snapshot_to_text(snapshot: ExposureSnapshot) -> str:
    lines = [f"Exposure Snapshot ({snapshot.snapshot_id})"]
    lines.append(f"  Total Equity: ${snapshot.total_equity_usd:.2f}" if snapshot.total_equity_usd else "  Total Equity: Unknown")
    lines.append(f"  Gross Exposure: ${snapshot.gross_exposure_usd:.2f}")
    lines.append(f"  Net Exposure: ${snapshot.net_exposure_usd:.2f}")
    lines.append(f"  Long Exposure: ${snapshot.long_exposure_usd:.2f}")
    lines.append(f"  Short Exposure: ${snapshot.short_exposure_usd:.2f}")
    return "\\n".join(lines)
"""

write_file("usa_signal_bot/portfolio_construction/exposure_calculator.py", calc_code)

print("Generated step 1")
