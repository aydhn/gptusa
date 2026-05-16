from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioCandidate, PortfolioAllocation, create_portfolio_candidate_id, create_portfolio_allocation_id
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
