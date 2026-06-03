import datetime
import hashlib
import statistics

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    MonteCarloReplayResult,
    MonteCarloDistributionSummary,
    create_monte_carlo_distribution_summary_id
)

def build_monte_carlo_distribution_summary(results: list[MonteCarloReplayResult], ruin_threshold_return: float = -0.5) -> MonteCarloDistributionSummary:
    if not results:
        return MonteCarloDistributionSummary(
            summary_id=create_monte_carlo_distribution_summary_id(),
            created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
            path_count=0, metric_values={}, return_mean=None, return_median=None, return_std=None,
            return_min=None, return_max=None, return_p05=None, return_p95=None, drawdown_mean=None,
            drawdown_p95=None, loss_probability=None, ruin_probability_approx=None, summary_hash=None,
            summary_valid=False, non_trading_metric=True, not_investment_advice=True, not_strategy_activation=True,
            research_data_only=True, warnings=["No results"], errors=[], risk_flags=[], metadata={}
        )

    returns = sorted([r.total_return for r in results if r.total_return is not None])
    drawdowns = sorted([r.max_drawdown for r in results if r.max_drawdown is not None])

    rmean = sum(returns) / len(returns) if returns else None
    rmed = percentile(returns, 0.50)
    rstd = statistics.stdev(returns) if len(returns) > 1 else 0.0
    rmin = returns[0] if returns else None
    rmax = returns[-1] if returns else None
    rp05 = percentile(returns, 0.05)
    rp95 = percentile(returns, 0.95)

    dmean = sum(drawdowns) / len(drawdowns) if drawdowns else None
    dp95 = percentile(drawdowns, 0.95)

    loss_prob = calculate_loss_probability(results)
    ruin_prob = calculate_ruin_probability_approx(results, ruin_threshold_return)

    summary = MonteCarloDistributionSummary(
        summary_id=create_monte_carlo_distribution_summary_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        path_count=len(results),
        metric_values={},
        return_mean=rmean,
        return_median=rmed,
        return_std=rstd,
        return_min=rmin,
        return_max=rmax,
        return_p05=rp05,
        return_p95=rp95,
        drawdown_mean=dmean,
        drawdown_p95=dp95,
        loss_probability=loss_prob,
        ruin_probability_approx=ruin_prob,
        summary_hash=None,
        summary_valid=True,
        non_trading_metric=True,
        not_investment_advice=True,
        not_strategy_activation=True,
        research_data_only=True,
        warnings=[], errors=[], risk_flags=[], metadata={"ruin_threshold": ruin_threshold_return}
    )
    summary.summary_hash = compute_monte_carlo_distribution_summary_hash(summary)
    return summary

def percentile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    idx = int(len(values) * p)
    if idx >= len(values):
        idx = len(values) - 1
    return values[idx]

def calculate_loss_probability(results: list[MonteCarloReplayResult]) -> float | None:
    if not results:
        return None
    losses = sum(1 for r in results if r.total_return is not None and r.total_return < 0)
    return losses / len(results)

def calculate_ruin_probability_approx(results: list[MonteCarloReplayResult], ruin_threshold_return: float = -0.5) -> float | None:
    if not results:
        return None
    ruins = sum(1 for r in results if r.total_return is not None and r.total_return < ruin_threshold_return)
    return ruins / len(results)

def compute_monte_carlo_distribution_summary_hash(summary: MonteCarloDistributionSummary) -> str:
    s = f"{summary.path_count}:{summary.return_mean}:{summary.loss_probability}"
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
