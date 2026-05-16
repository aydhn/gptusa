from usa_signal_bot.portfolio_construction.portfolio_models import ExposureSnapshot, PortfolioCandidate, PortfolioAllocation, create_exposure_snapshot_id
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
    return "\n".join(lines)
