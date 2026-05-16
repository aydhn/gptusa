import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created {path}")

# --- portfolio_construction/allocation_planner.py ---
alloc_planner_code = """from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioCandidate, PortfolioAllocation, create_portfolio_candidate_id, create_portfolio_allocation_id
from usa_signal_bot.portfolio_construction.sector_cluster_resolver import SectorClusterResolver
from usa_signal_bot.core.enums import PortfolioConstructionMode, PortfolioAllocationStatus
from typing import Any

class PortfolioAllocationPlanner:
    def __init__(self, mode: PortfolioConstructionMode = PortfolioConstructionMode.HYBRID, config: dict | None = None):
        self.mode = mode
        self.config = config or {}

    def build_candidates(self, raw_candidates: list[dict[str, Any]], resolver: SectorClusterResolver | None = None) -> list[PortfolioCandidate]:
        candidates = []
        for rc in raw_candidates:
            symbol = rc.get("symbol")
            if not symbol: continue
            cand = PortfolioCandidate(
                candidate_id=create_portfolio_candidate_id(symbol),
                symbol=symbol,
                strategy_name=rc.get("strategy_name", rc.get("strategy")),
                side=rc.get("side", "LONG"),
                score=rc.get("score", rc.get("rank_score")),
                confidence=rc.get("confidence", rc.get("ensemble_confidence")),
                requested_notional_usd=rc.get("notional_usd", rc.get("suggested_notional_usd")),
                sized_notional_usd=rc.get("final_notional_usd"),
                sized_quantity=rc.get("final_quantity"),
                sector=rc.get("sector"),
                cluster=rc.get("cluster"),
                regime_label=rc.get("regime_label", rc.get("regime")),
                liquidity_bucket=rc.get("liquidity_bucket"),
                cost_bucket=rc.get("cost_bucket"),
                metadata=rc
            )
            if resolver and (not cand.sector or not cand.cluster):
                cand = resolver.resolve_candidate(cand)
            candidates.append(cand)
        return candidates

    def initial_weight_for_candidate(self, candidate: PortfolioCandidate, candidates: list[PortfolioCandidate]) -> float:
        if self.mode == PortfolioConstructionMode.DISABLED:
            return 0.0

        n = len(candidates)
        if n == 0: return 0.0

        # Blocked or suppressed
        if candidate.metadata.get("status") in ["BLOCKED", "SUPPRESSED"]:
            return 0.0

        if self.mode == PortfolioConstructionMode.EQUAL_WEIGHT:
            return 1.0 / n

        elif self.mode == PortfolioConstructionMode.SCORE_WEIGHTED:
            score_sum = sum(max(c.score or 0.0, 0.0) for c in candidates)
            if score_sum <= 0: return 1.0 / n
            return max(candidate.score or 0.0, 0.0) / score_sum

        elif self.mode == PortfolioConstructionMode.CONFIDENCE_WEIGHTED:
            conf_sum = sum(max(c.confidence or 0.0, 0.0) for c in candidates)
            if conf_sum <= 0: return 1.0 / n
            return max(candidate.confidence or 0.0, 0.0) / conf_sum

        elif self.mode == PortfolioConstructionMode.SIZE_RESULT_WEIGHTED:
            size_sum = sum(max(c.sized_notional_usd or 0.0, 0.0) for c in candidates)
            if size_sum <= 0: return 1.0 / n
            return max(candidate.sized_notional_usd or 0.0, 0.0) / size_sum

        elif self.mode == PortfolioConstructionMode.HYBRID:
            # mix of score, conf, size
            s_weight = max(candidate.score or 0.0, 0.0)
            c_weight = max(candidate.confidence or 0.0, 0.0) / 100.0
            z_weight = max(candidate.sized_notional_usd or 0.0, 0.0)

            raw_w = (s_weight * 0.3) + (c_weight * 0.3) + (z_weight * 0.4 if z_weight > 0 else 1.0)
            return raw_w

        return 1.0 / n

    def normalize_candidate_weights(self, candidates: list[PortfolioCandidate]) -> dict[str, float]:
        raw_weights = {c.symbol: self.initial_weight_for_candidate(c, candidates) for c in candidates}
        total_w = sum(raw_weights.values())
        if total_w <= 0:
            return {c.symbol: 0.0 for c in candidates}
        return {s: w / total_w for s, w in raw_weights.items()}

    def allocation_from_candidate(self, candidate: PortfolioCandidate, weight: float, total_equity_usd: float | None) -> PortfolioAllocation:
        alloc_notional = None
        if total_equity_usd is not None:
            alloc_notional = total_equity_usd * weight

        status = PortfolioAllocationStatus.APPROVED if weight > 0 else PortfolioAllocationStatus.SUPPRESSED

        return PortfolioAllocation(
            allocation_id=create_portfolio_allocation_id(candidate.symbol),
            symbol=candidate.symbol,
            strategy_name=candidate.strategy_name,
            side=candidate.side,
            initial_notional_usd=alloc_notional,
            final_notional_usd=alloc_notional,
            final_quantity=None,  # Price is needed to calc quantity
            weight_pct_equity=weight * 100.0,
            status=status,
            guard_decisions=[],
            adjustment_reasons=[],
            warnings=[],
            errors=[],
            metadata={"candidate_id": candidate.candidate_id}
        )

    def plan_allocations(self, candidates: list[PortfolioCandidate], total_equity_usd: float | None = None) -> list[PortfolioAllocation]:
        weights = self.normalize_candidate_weights(candidates)
        allocs = []
        for c in candidates:
            w = weights.get(c.symbol, 0.0)
            allocs.append(self.allocation_from_candidate(c, w, total_equity_usd))
        return allocs
"""
write_file("usa_signal_bot/portfolio_construction/allocation_planner.py", alloc_planner_code)

# --- portfolio_construction/portfolio_balancer.py ---
balancer_code = """from usa_signal_bot.portfolio_construction.portfolio_models import (
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
"""
write_file("usa_signal_bot/portfolio_construction/portfolio_balancer.py", balancer_code)

print("Generated step 4")
