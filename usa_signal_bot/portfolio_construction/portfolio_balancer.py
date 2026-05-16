from usa_signal_bot.portfolio_construction.portfolio_models import (
    PortfolioCandidate, PortfolioAllocation, PortfolioConstructionPlan,
    create_portfolio_construction_plan_id, ExposureSnapshot
)
from usa_signal_bot.portfolio_construction.allocation_planner import PortfolioAllocationPlanner
from usa_signal_bot.portfolio_construction.exposure_calculator import calculate_exposure_snapshot
from usa_signal_bot.portfolio_construction.exposure_limits import check_gross_exposure_limit, check_net_exposure_limit, check_long_exposure_limit, check_short_exposure_limit
from usa_signal_bot.portfolio_construction.concentration_guards import assess_all_concentration
from usa_signal_bot.core.enums import PortfolioConstructionMode, PortfolioAllocationStatus, PortfolioGuardDecision
import datetime

class PortfolioBalancer:
    def __init__(self, config: dict | None = None):
        self.config = config or {}
        self.mode = PortfolioConstructionMode(self.config.get("mode", "HYBRID"))
        self.planner = PortfolioAllocationPlanner(mode=self.mode, config=self.config)
        self.max_gross = self.config.get("portfolio_exposure_limits", {}).get("max_gross_exposure_pct_equity", 100.0)
        self.max_net = self.config.get("portfolio_exposure_limits", {}).get("max_abs_net_exposure_pct_equity", 80.0)
        self.max_long = self.config.get("portfolio_exposure_limits", {}).get("max_long_exposure_pct_equity", 100.0)
        self.max_short = self.config.get("portfolio_exposure_limits", {}).get("max_short_exposure_pct_equity", 50.0)

    def apply_exposure_limits(self, plan: PortfolioConstructionPlan) -> PortfolioConstructionPlan:
        # Simplistic pro-rata reduction if exposure limits exceeded
        if not plan.exposure_snapshot or not plan.exposure_snapshot.total_equity_usd:
            return plan

        assessments = []
        assessments.append(check_gross_exposure_limit(plan.exposure_snapshot, self.max_gross))
        assessments.append(check_net_exposure_limit(plan.exposure_snapshot, self.max_net))
        assessments.append(check_long_exposure_limit(plan.exposure_snapshot, self.max_long))
        assessments.append(check_short_exposure_limit(plan.exposure_snapshot, self.max_short))

        reduce_ratio = 1.0
        for a in assessments:
            if a.decision in [PortfolioGuardDecision.CAP, PortfolioGuardDecision.REDUCE]:
                if a.exposure_pct_equity and a.exposure_pct_equity > 0:
                    ratio = a.limit_pct_equity / a.exposure_pct_equity
                    if ratio < reduce_ratio:
                        reduce_ratio = ratio

        if reduce_ratio < 1.0:
            for alloc in plan.allocations:
                if alloc.final_notional_usd and alloc.status == PortfolioAllocationStatus.APPROVED:
                    alloc.final_notional_usd *= reduce_ratio
                    alloc.weight_pct_equity = (alloc.weight_pct_equity or 0.0) * reduce_ratio
                    alloc.status = PortfolioAllocationStatus.REDUCED
                    alloc.guard_decisions.append(PortfolioGuardDecision.REDUCE)
                    alloc.adjustment_reasons.append(f"Pro-rata reduced by {reduce_ratio:.2f} due to exposure limits")

        plan.concentration_assessments.extend(assessments)
        return plan

    def apply_concentration_guards(self, plan: PortfolioConstructionPlan) -> PortfolioConstructionPlan:
        if not plan.exposure_snapshot: return plan
        cfg = self.config.get("portfolio_concentration_limits", {})
        assessments = assess_all_concentration(plan.exposure_snapshot, cfg)
        plan.concentration_assessments.extend(assessments)

        for a in assessments:
            if a.decision in [PortfolioGuardDecision.CAP, PortfolioGuardDecision.REDUCE]:
                # find matching allocations and reduce
                for alloc in plan.allocations:
                    # simplistic check for symbol matches
                    if a.exposure_type.value == "SYMBOL" and alloc.symbol == a.name:
                        self._cap_allocation(alloc, a.limit_pct_equity, plan.exposure_snapshot.total_equity_usd)
        return plan

    def _cap_allocation(self, alloc: PortfolioAllocation, limit_pct: float, total_equity: float | None):
        if total_equity and alloc.weight_pct_equity and alloc.weight_pct_equity > limit_pct:
            alloc.final_notional_usd = total_equity * (limit_pct / 100.0)
            alloc.weight_pct_equity = limit_pct
            alloc.status = PortfolioAllocationStatus.CAPPED
            alloc.guard_decisions.append(PortfolioGuardDecision.CAP)
            alloc.adjustment_reasons.append("Capped due to concentration limit")

    def build_plan(self, candidates: list[PortfolioCandidate], total_equity_usd: float | None = None, existing_allocations: list[PortfolioAllocation] | None = None) -> PortfolioConstructionPlan:
        allocs = self.planner.plan_allocations(candidates, total_equity_usd)

        plan = PortfolioConstructionPlan(
            plan_id=create_portfolio_construction_plan_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            mode=self.mode,
            candidates=candidates,
            allocations=allocs,
            exposure_snapshot=None,
            concentration_assessments=[],
            conflicts=[],
            total_allocated_notional_usd=0.0,
            approved_count=0,
            reduced_count=0,
            capped_count=0,
            suppressed_count=0,
            blocked_count=0,
            warnings=[],
            errors=[],
            metadata={}
        )

        plan.exposure_snapshot = calculate_exposure_snapshot(plan.allocations, total_equity_usd)
        plan = self.apply_exposure_limits(plan)
        plan.exposure_snapshot = calculate_exposure_snapshot(plan.allocations, total_equity_usd) # recalc
        plan = self.apply_concentration_guards(plan)

        # update totals
        plan.total_allocated_notional_usd = sum((a.final_notional_usd or 0.0) for a in plan.allocations)
        plan.approved_count = len([a for a in plan.allocations if a.status == PortfolioAllocationStatus.APPROVED])
        plan.reduced_count = len([a for a in plan.allocations if a.status == PortfolioAllocationStatus.REDUCED])
        plan.capped_count = len([a for a in plan.allocations if a.status == PortfolioAllocationStatus.CAPPED])
        plan.suppressed_count = len([a for a in plan.allocations if a.status == PortfolioAllocationStatus.SUPPRESSED])
        plan.blocked_count = len([a for a in plan.allocations if a.status == PortfolioAllocationStatus.BLOCKED])

        return plan
