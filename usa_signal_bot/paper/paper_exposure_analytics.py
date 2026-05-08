from typing import List, Dict, Optional
from usa_signal_bot.paper.paper_models import PaperEquitySnapshot, PaperPosition, PaperFill
from usa_signal_bot.paper.paper_analytics_models import PaperExposureMetrics
from usa_signal_bot.core.enums import PaperMetricStatus

def calculate_average_from_values(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return sum(values) / len(values)

def calculate_max_from_values(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return max(values)

def calculate_exposure_to_equity_ratios(snapshots: List[PaperEquitySnapshot]) -> List[float]:
    ratios = []
    for snapshot in snapshots:
        if snapshot.equity is None or snapshot.equity <= 0:
            continue
        ratios.append(snapshot.gross_exposure / snapshot.equity)
    return ratios

def calculate_largest_position_weight(positions: List[PaperPosition], equity: Optional[float]) -> Optional[float]:
    if not positions or equity is None or equity <= 0:
        return None
    max_market_value = max([p.market_value for p in positions])
    return max_market_value / equity

def calculate_paper_turnover_proxy(fills: List[PaperFill], starting_equity: Optional[float]) -> Optional[float]:
    if not fills or starting_equity is None or starting_equity <= 0:
        return None
    gross_notional = sum([abs(f.fill_price * f.filled_quantity) for f in fills])
    return gross_notional / starting_equity

def calculate_symbol_exposure_breakdown(positions: List[PaperPosition], equity: Optional[float]) -> Dict[str, float]:
    if not positions or equity is None or equity <= 0:
        return {}
    breakdown = {}
    for p in positions:
        breakdown[p.symbol] = p.market_value / equity
    return breakdown

def calculate_paper_exposure_metrics(snapshots: List[PaperEquitySnapshot], positions: Optional[List[PaperPosition]] = None) -> PaperExposureMetrics:
    if not snapshots:
        return PaperExposureMetrics(
            status=PaperMetricStatus.EMPTY,
            average_gross_exposure=None, max_gross_exposure=None,
            average_net_exposure=None, max_net_exposure=None,
            average_open_positions=None, max_open_positions=None,
            final_open_positions=len(positions) if positions else 0,
            exposure_to_equity_avg=None, exposure_to_equity_max=None,
            warnings=["No snapshots provided for exposure metrics."], errors=[]
        )

    gross_exposures = [s.gross_exposure for s in snapshots] # Absolute
    net_exposures = [s.gross_exposure for s in snapshots] # Assuming only long positions for now
    open_positions = [s.open_positions for s in snapshots if s.open_positions is not None]

    ratios = calculate_exposure_to_equity_ratios(snapshots)

    warnings = []
    if not ratios:
         warnings.append("Could not calculate exposure to equity ratios due to zero or negative equity.")

    return PaperExposureMetrics(
        status=PaperMetricStatus.OK,
        average_gross_exposure=calculate_average_from_values(gross_exposures),
        max_gross_exposure=calculate_max_from_values(gross_exposures),
        average_net_exposure=calculate_average_from_values(net_exposures),
        max_net_exposure=calculate_max_from_values(net_exposures),
        average_open_positions=calculate_average_from_values([float(x) for x in open_positions]) if open_positions else None,
        max_open_positions=int(max(open_positions)) if open_positions else None,
        final_open_positions=len(positions) if positions else (open_positions[-1] if open_positions else 0),
        exposure_to_equity_avg=calculate_average_from_values(ratios),
        exposure_to_equity_max=calculate_max_from_values(ratios),
        warnings=warnings,
        errors=[]
    )

def paper_exposure_metrics_to_text(metrics: PaperExposureMetrics) -> str:
    lines = [
        "--- Paper Exposure Metrics ---",
        f"Status: {metrics.status.value}",
        f"Final Open Positions: {metrics.final_open_positions}"
    ]
    if metrics.average_open_positions is not None:
         lines.append(f"Average Open Positions: {metrics.average_open_positions:.2f}")
    if metrics.max_open_positions is not None:
         lines.append(f"Max Open Positions: {metrics.max_open_positions}")
    if metrics.exposure_to_equity_avg is not None:
         lines.append(f"Average Exposure/Equity: {metrics.exposure_to_equity_avg * 100:.2f}%")
    if metrics.exposure_to_equity_max is not None:
         lines.append(f"Max Exposure/Equity: {metrics.exposure_to_equity_max * 100:.2f}%")

    if metrics.warnings:
        lines.append("\nWarnings: " + ", ".join(metrics.warnings))
    if metrics.errors:
        lines.append("\nErrors: " + ", ".join(metrics.errors))

    lines.append("")
    return "\n".join(lines)
