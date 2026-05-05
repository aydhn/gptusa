from dataclasses import dataclass, field
from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.risk.risk_models import PositionSizingRequest, PositionSizingResult, RiskCheckResult, RiskDecision
from usa_signal_bot.risk.risk_limits import (
    RiskLimitConfig,
    check_symbol_exposure,
    check_strategy_exposure,
    check_portfolio_exposure,
    check_open_positions_count,
    check_cash_buffer
)
from usa_signal_bot.core.enums import RiskCheckStatus

@dataclass
class ExposureSnapshot:
    portfolio_equity: float
    available_cash: float
    total_exposure: float
    open_positions: int
    exposure_by_symbol: dict[str, float] = field(default_factory=dict)
    exposure_by_strategy: dict[str, float] = field(default_factory=dict)
    exposure_by_timeframe: dict[str, float] = field(default_factory=dict)
    timestamp_utc: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ExposureGuardResult:
    candidate_id: str
    approved: bool
    proposed_notional: float
    checks: list[RiskCheckResult]
    warnings: list[str]
    errors: list[str]

def create_empty_exposure_snapshot(portfolio_equity: float, available_cash: float) -> ExposureSnapshot:
    return ExposureSnapshot(
        portfolio_equity=portfolio_equity,
        available_cash=available_cash,
        total_exposure=0.0,
        open_positions=0,
        timestamp_utc=datetime.now(timezone.utc).isoformat()
    )

def build_exposure_snapshot_from_backtest_portfolio(portfolio: Any, prices: dict[str, float]) -> ExposureSnapshot:
    total_exposure = 0.0
    exposure_by_symbol = {}
    open_positions = 0

    for symbol, position in getattr(portfolio, 'positions', {}).items():
        price = prices.get(symbol, 0.0)
        notional = position.quantity * price if hasattr(position, 'quantity') else 0.0
        exposure_by_symbol[symbol] = notional
        total_exposure += notional
        if notional > 0:
            open_positions += 1

    return ExposureSnapshot(
        portfolio_equity=portfolio.equity if hasattr(portfolio, 'equity') else total_exposure,
        available_cash=portfolio.cash if hasattr(portfolio, 'cash') else 0.0,
        total_exposure=total_exposure,
        open_positions=open_positions,
        exposure_by_symbol=exposure_by_symbol,
        timestamp_utc=datetime.now(timezone.utc).isoformat()
    )

def update_exposure_snapshot_with_decision(snapshot: ExposureSnapshot, decision: RiskDecision) -> ExposureSnapshot:
    import copy
    new_snap = copy.deepcopy(snapshot)
    if decision.approved_notional > 0:
        new_snap.total_exposure += decision.approved_notional
        new_snap.available_cash -= decision.approved_notional

        sym = decision.symbol
        new_snap.exposure_by_symbol[sym] = new_snap.exposure_by_symbol.get(sym, 0.0) + decision.approved_notional

        strat = decision.strategy_name or "unknown_strategy"
        new_snap.exposure_by_strategy[strat] = new_snap.exposure_by_strategy.get(strat, 0.0) + decision.approved_notional

        tf = decision.timeframe
        new_snap.exposure_by_timeframe[tf] = new_snap.exposure_by_timeframe.get(tf, 0.0) + decision.approved_notional

        if new_snap.exposure_by_symbol[sym] == decision.approved_notional:
            new_snap.open_positions += 1

        new_snap.timestamp_utc = datetime.now(timezone.utc).isoformat()

    return new_snap

def evaluate_exposure_for_candidate(request: PositionSizingRequest, sizing_result: PositionSizingResult, snapshot: ExposureSnapshot, config: RiskLimitConfig | None = None) -> ExposureGuardResult:
    if config is None:
        from usa_signal_bot.risk.risk_limits import default_risk_limit_config
        config = default_risk_limit_config()

    notional = sizing_result.approved_notional
    checks = []

    current_sym_exp = snapshot.exposure_by_symbol.get(request.symbol, 0.0)
    checks.append(check_symbol_exposure(request.symbol, notional, current_sym_exp, snapshot.portfolio_equity, config))

    current_strat_exp = snapshot.exposure_by_strategy.get(request.strategy_name or "unknown_strategy", 0.0)
    checks.append(check_strategy_exposure(request.strategy_name, notional, current_strat_exp, snapshot.portfolio_equity, config))

    checks.append(check_portfolio_exposure(snapshot.total_exposure, notional, snapshot.portfolio_equity, config))

    is_new = snapshot.exposure_by_symbol.get(request.symbol, 0.0) == 0.0
    if is_new and notional > 0:
        checks.append(check_open_positions_count(snapshot.open_positions + 1, config))
    else:
        checks.append(check_open_positions_count(snapshot.open_positions, config))

    checks.append(check_cash_buffer(snapshot.available_cash, notional, snapshot.portfolio_equity, config))

    failed_checks = [c for c in checks if c.status == RiskCheckStatus.FAILED]
    approved = len(failed_checks) == 0

    errors = [c.message for c in failed_checks]
    warnings = [c.message for c in checks if c.status == RiskCheckStatus.WARNING]

    return ExposureGuardResult(
        candidate_id=request.candidate_id,
        approved=approved,
        proposed_notional=notional if approved else 0.0,
        checks=checks,
        warnings=warnings,
        errors=errors
    )

def exposure_snapshot_to_dict(snapshot: ExposureSnapshot) -> dict[str, Any]:
    return {
        "portfolio_equity": snapshot.portfolio_equity,
        "available_cash": snapshot.available_cash,
        "total_exposure": snapshot.total_exposure,
        "open_positions": snapshot.open_positions,
        "exposure_by_symbol": snapshot.exposure_by_symbol,
        "exposure_by_strategy": snapshot.exposure_by_strategy,
        "exposure_by_timeframe": snapshot.exposure_by_timeframe,
        "timestamp_utc": snapshot.timestamp_utc,
        "metadata": snapshot.metadata
    }

def exposure_guard_result_to_dict(result: ExposureGuardResult) -> dict[str, Any]:
    from usa_signal_bot.risk.risk_models import risk_check_result_to_dict
    return {
        "candidate_id": result.candidate_id,
        "approved": result.approved,
        "proposed_notional": result.proposed_notional,
        "checks": [risk_check_result_to_dict(c) for c in result.checks],
        "warnings": result.warnings,
        "errors": result.errors
    }

def exposure_snapshot_to_text(snapshot: ExposureSnapshot) -> str:
    lines = [
        "=== Exposure Snapshot ===",
        f"Timestamp: {snapshot.timestamp_utc}",
        f"Equity: {snapshot.portfolio_equity:.2f}",
        f"Cash: {snapshot.available_cash:.2f}",
        f"Total Exposure: {snapshot.total_exposure:.2f} ({(snapshot.total_exposure/max(snapshot.portfolio_equity, 1)):.2%})",
        f"Open Positions: {snapshot.open_positions}",
        "--- By Symbol ---"
    ]
    for sym, exp in snapshot.exposure_by_symbol.items():
        if exp > 0:
            lines.append(f"  {sym}: {exp:.2f}")

    lines.append("--- By Strategy ---")
    for strat, exp in snapshot.exposure_by_strategy.items():
        if exp > 0:
            lines.append(f"  {strat}: {exp:.2f}")

    return "\n".join(lines)
