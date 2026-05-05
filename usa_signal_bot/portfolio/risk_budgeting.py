from dataclasses import dataclass, field
from typing import List, Dict, Optional
import uuid
from datetime import datetime, timezone
from usa_signal_bot.portfolio.portfolio_models import AllocationResult
from usa_signal_bot.core.enums import RiskBudgetType, RiskBudgetStatus, AllocationStatus

@dataclass
class RiskBudgetConfig:
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool = True

@dataclass
class RiskBudgetItem:
    budget_type: RiskBudgetType
    key: str
    used_weight: float
    limit_weight: float
    status: RiskBudgetStatus
    message: str

@dataclass
class RiskBudgetReport:
    report_id: str
    created_at_utc: str
    status: RiskBudgetStatus
    items: List[RiskBudgetItem]
    total_allocated_weight: float
    total_allocated_notional: float
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def default_risk_budget_config() -> RiskBudgetConfig:
    return RiskBudgetConfig(
        max_total_budget_pct=0.80,
        max_symbol_budget_pct=0.15,
        max_strategy_budget_pct=0.30,
        max_timeframe_budget_pct=0.50,
        max_single_candidate_budget_pct=0.10,
        min_cash_buffer_pct=0.05,
        enforce_budget=True
    )

def validate_risk_budget_config(config: RiskBudgetConfig) -> None:
    from usa_signal_bot.core.exceptions import RiskBudgetingError
    limits = [
        config.max_total_budget_pct,
        config.max_symbol_budget_pct,
        config.max_strategy_budget_pct,
        config.max_timeframe_budget_pct,
        config.max_single_candidate_budget_pct,
        config.min_cash_buffer_pct
    ]
    if any(limit < 0 or limit > 1 for limit in limits):
        raise RiskBudgetingError("All risk budget limits must be between 0 and 1.")

def calculate_weight_by_symbol(allocations: List[AllocationResult]) -> Dict[str, float]:
    weights = {}
    for a in allocations:
        if a.status in [AllocationStatus.ALLOCATED, AllocationStatus.CAPPED, AllocationStatus.REDUCED]:
            weights[a.symbol] = weights.get(a.symbol, 0.0) + a.target_weight
    return weights

def calculate_weight_by_strategy(allocations: List[AllocationResult]) -> Dict[str, float]:
    weights = {}
    for a in allocations:
        if a.status in [AllocationStatus.ALLOCATED, AllocationStatus.CAPPED, AllocationStatus.REDUCED]:
            strategy = a.strategy_name or "UNKNOWN"
            weights[strategy] = weights.get(strategy, 0.0) + a.target_weight
    return weights

def calculate_weight_by_timeframe(allocations: List[AllocationResult]) -> Dict[str, float]:
    weights = {}
    for a in allocations:
        if a.status in [AllocationStatus.ALLOCATED, AllocationStatus.CAPPED, AllocationStatus.REDUCED]:
            weights[a.timeframe] = weights.get(a.timeframe, 0.0) + a.target_weight
    return weights

def check_budget_items(weights: Dict[str, float], budget_type: RiskBudgetType, limit: float) -> List[RiskBudgetItem]:
    items = []
    for key, weight in weights.items():
        status = RiskBudgetStatus.BREACHED if weight > limit else RiskBudgetStatus.WITHIN_BUDGET
        message = f"Weight {weight:.4f} > Limit {limit:.4f}" if status == RiskBudgetStatus.BREACHED else "Within budget"
        items.append(RiskBudgetItem(
            budget_type=budget_type,
            key=key,
            used_weight=weight,
            limit_weight=limit,
            status=status,
            message=message
        ))
    return items

def build_risk_budget_report(allocations: List[AllocationResult], portfolio_equity: float, config: Optional[RiskBudgetConfig] = None) -> RiskBudgetReport:
    cfg = config or default_risk_budget_config()

    total_weight = sum(a.target_weight for a in allocations if a.status in [AllocationStatus.ALLOCATED, AllocationStatus.CAPPED, AllocationStatus.REDUCED])
    total_notional = sum(a.target_notional for a in allocations if a.status in [AllocationStatus.ALLOCATED, AllocationStatus.CAPPED, AllocationStatus.REDUCED])

    items = []
    status = RiskBudgetStatus.WITHIN_BUDGET
    warnings = []

    if total_weight > cfg.max_total_budget_pct:
        status = RiskBudgetStatus.BREACHED
        warnings.append(f"Total weight {total_weight:.4f} exceeds max_total_budget_pct {cfg.max_total_budget_pct:.4f}")

    items.append(RiskBudgetItem(
        budget_type=RiskBudgetType.PORTFOLIO,
        key="TOTAL",
        used_weight=total_weight,
        limit_weight=cfg.max_total_budget_pct,
        status=RiskBudgetStatus.BREACHED if total_weight > cfg.max_total_budget_pct else RiskBudgetStatus.WITHIN_BUDGET,
        message="Total portfolio weight limit check"
    ))

    items.extend(check_budget_items(calculate_weight_by_symbol(allocations), RiskBudgetType.SYMBOL, cfg.max_symbol_budget_pct))
    items.extend(check_budget_items(calculate_weight_by_strategy(allocations), RiskBudgetType.STRATEGY, cfg.max_strategy_budget_pct))
    items.extend(check_budget_items(calculate_weight_by_timeframe(allocations), RiskBudgetType.TIMEFRAME, cfg.max_timeframe_budget_pct))

    if any(item.status == RiskBudgetStatus.BREACHED for item in items):
        status = RiskBudgetStatus.BREACHED

    return RiskBudgetReport(
        report_id=f"rb_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        items=items,
        total_allocated_weight=total_weight,
        total_allocated_notional=total_notional,
        warnings=warnings,
        errors=[]
    )

def risk_budget_report_to_dict(report: RiskBudgetReport) -> dict:
    from dataclasses import asdict
    d = asdict(report)
    d["status"] = report.status.value if hasattr(report.status, "value") else str(report.status)
    for item in d["items"]:
        item["budget_type"] = item["budget_type"].value if hasattr(item["budget_type"], "value") else str(item["budget_type"])
        item["status"] = item["status"].value if hasattr(item["status"], "value") else str(item["status"])
    return d

def risk_budget_report_to_text(report: RiskBudgetReport) -> str:
    lines = [
        f"Risk Budget Report [{report.report_id}]",
        f"Status: {report.status.value if hasattr(report.status, 'value') else str(report.status)}",
        f"Total Weight: {report.total_allocated_weight:.4f} | Total Notional: {report.total_allocated_notional:.2f}",
        "-" * 50
    ]
    for item in report.items:
        st = item.status.value if hasattr(item.status, 'value') else str(item.status)
        bt = item.budget_type.value if hasattr(item.budget_type, 'value') else str(item.budget_type)
        lines.append(f"{bt} [{item.key}]: {item.used_weight:.4f} / {item.limit_weight:.4f} -> {st} ({item.message})")

    if report.warnings:
        lines.append("Warnings:")
        for w in report.warnings:
            lines.append(f"  - {w}")
    return "\n".join(lines)
