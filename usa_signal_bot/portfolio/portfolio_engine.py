from typing import List, Optional
from datetime import datetime, timezone

from usa_signal_bot.portfolio.portfolio_models import (
    AllocationRequest,
    PortfolioCandidate,
    PortfolioBasket,
    PortfolioConstructionResult,
    create_portfolio_basket_id,
    create_portfolio_run_id,
    AllocationResult
)
from usa_signal_bot.portfolio.allocation_methods import (
    AllocationConfig,
    default_allocation_config,
    allocate_candidates
)
from usa_signal_bot.portfolio.risk_budgeting import (
    RiskBudgetConfig,
    default_risk_budget_config,
    RiskBudgetReport,
    build_risk_budget_report
)
from usa_signal_bot.portfolio.concentration_guards import (
    ConcentrationGuardConfig,
    default_concentration_guard_config,
    ConcentrationReport,
    build_concentration_report,
    apply_concentration_caps
)
from usa_signal_bot.portfolio.portfolio_candidates import (
    portfolio_candidates_from_risk_decisions,
    portfolio_candidate_from_selected_candidate,
    filter_eligible_portfolio_candidates
)
from usa_signal_bot.core.enums import (
    PortfolioConstructionStatus,
    PortfolioReviewStatus,
    AllocationMethod,
    AllocationStatus,
    RiskBudgetStatus
)
from usa_signal_bot.risk.risk_models import RiskDecision
from usa_signal_bot.strategies.candidate_selection import SelectedCandidate

class PortfolioConstructionEngine:
    def __init__(
        self,
        allocation_config: Optional[AllocationConfig] = None,
        risk_budget_config: Optional[RiskBudgetConfig] = None,
        concentration_config: Optional[ConcentrationGuardConfig] = None
    ):
        self.allocation_config = allocation_config or default_allocation_config()
        self.risk_budget_config = risk_budget_config or default_risk_budget_config()
        self.concentration_config = concentration_config or default_concentration_guard_config()

    def construct_portfolio(self, request: AllocationRequest) -> PortfolioConstructionResult:
        run_id = create_portfolio_run_id()
        created_at_utc = datetime.now(timezone.utc).isoformat()

        eligible_candidates = filter_eligible_portfolio_candidates(request.candidates)

        if not eligible_candidates:
            return PortfolioConstructionResult(
                run_id=run_id,
                created_at_utc=created_at_utc,
                status=PortfolioConstructionStatus.EMPTY,
                request=request,
                risk_budget_report=build_risk_budget_report([], request.portfolio_equity, self.risk_budget_config),
                concentration_report=build_concentration_report([], self.concentration_config),
                approved_allocations=[],
                rejected_allocations=[],
                warnings=["No eligible candidates provided."],
                errors=[],
                basket=None
            )

        raw_allocations = allocate_candidates(request, self.allocation_config)
        allocations_after_concentration = apply_concentration_caps(raw_allocations, self.concentration_config)

        risk_budget_report = build_risk_budget_report(allocations_after_concentration, request.portfolio_equity, self.risk_budget_config)
        concentration_report = build_concentration_report(allocations_after_concentration, self.concentration_config)

        basket = self.build_basket(request, allocations_after_concentration, risk_budget_report, concentration_report)

        approved = [a for a in allocations_after_concentration if a.status in [AllocationStatus.ALLOCATED, AllocationStatus.CAPPED, AllocationStatus.REDUCED]]
        rejected = [a for a in allocations_after_concentration if a.status in [AllocationStatus.REJECTED, AllocationStatus.ZERO]]

        status = PortfolioConstructionStatus.COMPLETED if approved else PortfolioConstructionStatus.EMPTY

        return PortfolioConstructionResult(
            run_id=run_id,
            created_at_utc=created_at_utc,
            status=status,
            request=request,
            risk_budget_report=risk_budget_report,
            concentration_report=concentration_report,
            approved_allocations=approved,
            rejected_allocations=rejected,
            warnings=[],
            errors=[],
            basket=basket
        )

    def build_basket(
        self,
        request: AllocationRequest,
        allocations: List[AllocationResult],
        risk_budget_report: RiskBudgetReport,
        concentration_report: ConcentrationReport
    ) -> PortfolioBasket:
        total_target_notional = sum(a.target_notional for a in allocations if a.status in [AllocationStatus.ALLOCATED, AllocationStatus.CAPPED, AllocationStatus.REDUCED])
        total_target_weight = sum(a.target_weight for a in allocations if a.status in [AllocationStatus.ALLOCATED, AllocationStatus.CAPPED, AllocationStatus.REDUCED])

        cash_buffer = self.calculate_cash_buffer_after_allocation(request.available_cash, total_target_notional)

        basket_id = create_portfolio_basket_id()
        review_status = self.review_portfolio_basket(risk_budget_report, concentration_report)

        return PortfolioBasket(
            basket_id=basket_id,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            method=request.method,
            portfolio_equity=request.portfolio_equity,
            available_cash=request.available_cash,
            candidates=request.candidates,
            allocations=allocations,
            total_target_notional=total_target_notional,
            total_target_weight=total_target_weight,
            cash_buffer_after_allocation=cash_buffer,
            review_status=review_status,
            warnings=[],
            errors=[]
        )

    def review_portfolio_basket(
        self,
        risk_budget_report: RiskBudgetReport,
        concentration_report: ConcentrationReport
    ) -> PortfolioReviewStatus:
        if risk_budget_report.status == RiskBudgetStatus.BREACHED or concentration_report.breach_count > 0:
            return PortfolioReviewStatus.NEEDS_REVIEW
        return PortfolioReviewStatus.ACCEPTABLE

    def calculate_cash_buffer_after_allocation(self, available_cash: float, total_target_notional: float) -> float:
        return available_cash - total_target_notional

    def run_from_risk_decisions(
        self,
        decisions: List[RiskDecision],
        portfolio_equity: float,
        available_cash: float,
        method: Optional[AllocationMethod] = None
    ) -> PortfolioConstructionResult:
        from usa_signal_bot.portfolio.portfolio_models import create_allocation_request_id
        candidates = portfolio_candidates_from_risk_decisions(decisions)
        method = method or self.allocation_config.method

        request = AllocationRequest(
            request_id=create_allocation_request_id(),
            candidates=candidates,
            portfolio_equity=portfolio_equity,
            available_cash=available_cash,
            method=method,
            max_total_allocation_pct=self.allocation_config.max_total_allocation_pct,
            created_at_utc=datetime.now(timezone.utc).isoformat()
        )
        return self.construct_portfolio(request)

    def run_from_selected_candidates(
        self,
        candidates: List[SelectedCandidate],
        portfolio_equity: float,
        available_cash: float,
        method: Optional[AllocationMethod] = None
    ) -> PortfolioConstructionResult:
        from usa_signal_bot.portfolio.portfolio_models import create_allocation_request_id
        portfolio_candidates = [portfolio_candidate_from_selected_candidate(c) for c in candidates]
        method = method or self.allocation_config.method

        request = AllocationRequest(
            request_id=create_allocation_request_id(),
            candidates=portfolio_candidates,
            portfolio_equity=portfolio_equity,
            available_cash=available_cash,
            method=method,
            max_total_allocation_pct=self.allocation_config.max_total_allocation_pct,
            created_at_utc=datetime.now(timezone.utc).isoformat()
        )
        return self.construct_portfolio(request)
