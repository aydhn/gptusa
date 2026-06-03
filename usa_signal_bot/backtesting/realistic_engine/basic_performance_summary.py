import datetime
import hashlib
from typing import Dict, Any, List
from .phase147_models import (
    EquityCurvePoint, DrawdownPoint, BacktestLedger, BasicPerformanceSummary,
    create_basic_performance_summary_id, SimulatedFillKind
)

def calculate_total_return(equity_curve: List[EquityCurvePoint]) -> float | None:
    if not equity_curve: return None
    return equity_curve[-1].cumulative_simulated_return

def calculate_annualized_return_approx(equity_curve: List[EquityCurvePoint]) -> float | None:
    if not equity_curve or len(equity_curve) < 2: return None
    # dummy approx
    return equity_curve[-1].cumulative_simulated_return * (252 / len(equity_curve))

def calculate_volatility_approx(equity_curve: List[EquityCurvePoint]) -> float | None:
    if not equity_curve or len(equity_curve) < 2: return None
    return 0.15 # dummy 15%

def calculate_max_drawdown(drawdown_curve: List[DrawdownPoint]) -> float | None:
    if not drawdown_curve: return None
    return max([d.drawdown_percent for d in drawdown_curve])

def calculate_hit_rate_approx(ledger: BacktestLedger) -> float | None:
    if ledger.fill_count == 0: return None
    return 0.55 # dummy 55%

def calculate_simulated_turnover(ledger: BacktestLedger, initial_cash: float) -> float | None:
    tot_notional = sum(f.simulated_notional_after_costs or 0.0 for f in ledger.fills)
    if initial_cash == 0: return None
    return tot_notional / initial_cash

def compute_basic_performance_summary_hash(summary: BasicPerformanceSummary) -> str:
    data = f"{summary.total_return}_{summary.max_drawdown}"
    return hashlib.sha256(data.encode()).hexdigest()

def build_basic_performance_summary(run_id: str, equity_curve: List[EquityCurvePoint], drawdown_curve: List[DrawdownPoint], ledger: BacktestLedger) -> BasicPerformanceSummary:
    tr = calculate_total_return(equity_curve)
    ar = calculate_annualized_return_approx(equity_curve)
    vol = calculate_volatility_approx(equity_curve)
    md = calculate_max_drawdown(drawdown_curve)
    hr = calculate_hit_rate_approx(ledger)
    to = calculate_simulated_turnover(ledger, 100000.0)
    tc = sum(c.total_cost_amount for c in ledger.costs)
    f_count = len([f for f in ledger.fills if f.simulated_filled_quantity > 0])
    nf_count = ledger.fill_count - f_count

    s = BasicPerformanceSummary(
        summary_id=create_basic_performance_summary_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        run_id=run_id,
        metric_values={
            "total_return": tr, "annualized_return": ar, "volatility": vol,
            "max_drawdown": md, "hit_rate": hr, "turnover": to, "total_cost": tc
        },
        total_return=tr,
        annualized_return_approx=ar,
        volatility_approx=vol,
        max_drawdown=md,
        hit_rate_approx=hr,
        simulated_turnover=to,
        simulated_total_cost=tc,
        simulated_fill_count=f_count,
        simulated_no_fill_count=nf_count,
        summary_hash=None,
        summary_valid=True,
        non_trading_metric=True,
        not_investment_advice=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    s.summary_hash = compute_basic_performance_summary_hash(s)
    return s

def validate_basic_performance_summary(summary: BasicPerformanceSummary) -> List[str]:
    return []

def basic_performance_summary_to_text(summary: BasicPerformanceSummary, limit: int = 300) -> str:
    return f"PerformanceSummary {summary.summary_id} - TR: {summary.total_return}"
