from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioConstructionPlan, PortfolioAllocationStatus, PortfolioGuardDecision
from usa_signal_bot.core.enums import PortfolioConflictType

def detect_symbol_overlap_conflicts(plan: PortfolioConstructionPlan) -> list[dict[str, any]]:
    conflicts = []
    symbol_sides = {}
    for a in plan.allocations:
        if a.symbol not in symbol_sides:
            symbol_sides[a.symbol] = set()
        symbol_sides[a.symbol].add(a.side)

    for sym, sides in symbol_sides.items():
        if len(sides) > 1:
            conflicts.append({
                "type": PortfolioConflictType.SIDE_CONFLICT.value if hasattr(PortfolioConflictType.SIDE_CONFLICT, 'value') else str(PortfolioConflictType.SIDE_CONFLICT),
                "symbol": sym,
                "message": f"Symbol {sym} has conflicting allocations: {sides}"
            })
    return conflicts

def detect_portfolio_conflicts(plan: PortfolioConstructionPlan) -> list[dict[str, any]]:
    conflicts = []
    conflicts.extend(detect_symbol_overlap_conflicts(plan))
    # Sector/cluster conflicts can be inferred from concentration assessments
    for c in plan.concentration_assessments:
        if c.decision in [PortfolioGuardDecision.CAP, PortfolioGuardDecision.BLOCK]:
            conflicts.append({
                "type": f"{c.exposure_type.value if hasattr(c.exposure_type, 'value') else str(c.exposure_type)}_OVEREXPOSURE",
                "symbol": None,
                "message": f"{c.name} exceeded limits: {c.exposure_pct_equity}% vs {c.limit_pct_equity}%"
            })
    return conflicts

def resolve_portfolio_conflicts(plan: PortfolioConstructionPlan) -> PortfolioConstructionPlan:
    conflicts = detect_portfolio_conflicts(plan)
    plan.conflicts.extend(conflicts)

    # Build symbol index for O(1) lookups
    from collections import defaultdict
    allocations_by_symbol = defaultdict(list)
    for a in plan.allocations:
        allocations_by_symbol[a.symbol].append(a)

    # simple side conflict resolution: keep highest weight
    for c in conflicts:
        if c.get("type") == "SIDE_CONFLICT":
            sym = c.get("symbol")
            sym_allocs = allocations_by_symbol.get(sym, [])
            if not sym_allocs: continue
            best = max(sym_allocs, key=lambda x: x.weight_pct_equity or 0.0)
            for a in sym_allocs:
                if a != best and a.status != PortfolioAllocationStatus.SUPPRESSED:
                    a.status = PortfolioAllocationStatus.SUPPRESSED
                    a.guard_decisions.append(PortfolioGuardDecision.SUPPRESS)
                    a.adjustment_reasons.append("Suppressed due to side conflict resolution")
                    a.final_notional_usd = 0.0
                    a.weight_pct_equity = 0.0
                    plan.suppressed_count += 1
    return plan

def portfolio_conflicts_to_text(conflicts: list[dict[str, any]]) -> str:
    if not conflicts: return "No portfolio conflicts detected."
    lines = ["Portfolio Conflicts"]
    for c in conflicts:
        lines.append(f"  [{c.get('type')}] {c.get('message')}")
    return "\n".join(lines)
