from typing import Optional, List
from usa_signal_bot.core.enums import (
    CombinedCostRegime, AdaptiveExecutionDecision, RegimeCostAdjustmentStatus
)
from usa_signal_bot.regime_costs.regime_cost_models import (
    CostRegimeSnapshot, RegimeCostCurveSelection, AdaptiveExecutionRealismDecision,
    create_adaptive_execution_decision_id, get_utc_now_str
)
from usa_signal_bot.regime_costs.cost_curve_selector import select_cost_curve_profile

class AdaptiveExecutionRealismEngine:
    def __init__(
        self,
        block_on_closed_session: bool = True,
        block_on_frozen_liquidity: bool = True,
        require_review_on_high_risk: bool = True
    ):
        self.block_on_closed_session = block_on_closed_session
        self.block_on_frozen_liquidity = block_on_frozen_liquidity
        self.require_review_on_high_risk = require_review_on_high_risk

    def decide(self, symbol: str, snapshot: CostRegimeSnapshot, selection: Optional[RegimeCostCurveSelection] = None) -> AdaptiveExecutionRealismDecision:
        prof = selection.profile if selection else select_cost_curve_profile(snapshot)

        decision_val = AdaptiveExecutionDecision.USE_BASELINE_COSTS

        if snapshot.combined_regime == CombinedCostRegime.BLOCKED:
            if self.block_on_closed_session or self.block_on_frozen_liquidity:
                decision_val = AdaptiveExecutionDecision.BLOCK_FILL_SIMULATION
            else:
                decision_val = AdaptiveExecutionDecision.BLOCK_SIGNAL_METADATA
        elif snapshot.combined_regime == CombinedCostRegime.HIGH_RISK:
            decision_val = AdaptiveExecutionDecision.REQUIRE_REVIEW if self.require_review_on_high_risk else AdaptiveExecutionDecision.USE_STRESSED_COSTS
        elif snapshot.combined_regime == CombinedCostRegime.STRESSED:
            decision_val = AdaptiveExecutionDecision.USE_STRESSED_COSTS
        elif snapshot.combined_regime in (CombinedCostRegime.CONSERVATIVE, CombinedCostRegime.INSUFFICIENT_DATA):
            decision_val = AdaptiveExecutionDecision.USE_CONSERVATIVE_COSTS

        return AdaptiveExecutionRealismDecision(
            decision_id=create_adaptive_execution_decision_id(symbol),
            symbol=symbol,
            created_at_utc=get_utc_now_str(),
            decision=decision_val,
            status=RegimeCostAdjustmentStatus.APPLIED,
            combined_regime=snapshot.combined_regime,
            cost_curve_profile=prof,
            recommended_guards=self.recommended_guards(snapshot, selection),
            reasons=self.reasons_for_decision(snapshot),
            warnings=[],
            errors=[],
            metadata={}
        )

    def recommended_guards(self, snapshot: CostRegimeSnapshot, selection: Optional[RegimeCostCurveSelection] = None) -> List[str]:
        g = []
        if snapshot.combined_regime == CombinedCostRegime.HIGH_RISK:
            g.append("Require manual review")
        if snapshot.combined_regime == CombinedCostRegime.BLOCKED:
            g.append("Block all fill simulations")
        return g

    def reasons_for_decision(self, snapshot: CostRegimeSnapshot) -> List[str]:
        return [f"Combined regime was {snapshot.combined_regime.value}"]

    def should_block_fill_simulation(self, snapshot: CostRegimeSnapshot) -> bool:
        return snapshot.combined_regime == CombinedCostRegime.BLOCKED

    def should_block_signal_metadata(self, snapshot: CostRegimeSnapshot) -> bool:
        return snapshot.combined_regime == CombinedCostRegime.BLOCKED
