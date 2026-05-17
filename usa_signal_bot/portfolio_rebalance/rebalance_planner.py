from typing import Any, Dict, List, Optional, Tuple
import datetime
from datetime import timezone

from usa_signal_bot.core.enums import RebalanceMode, RebalanceActionType, RebalanceStatus
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    CurrentPortfolioState, TargetPortfolioState, DriftMeasurement, RebalanceAction,
    TurnoverAssessment, RebalancePlan, PortfolioPosition, create_rebalance_action_id,
    create_rebalance_plan_id
)
from usa_signal_bot.portfolio_rebalance.drift_calculator import calculate_symbol_drift
from usa_signal_bot.portfolio_rebalance.rebalance_thresholds import (
    RebalanceThresholdPolicy, default_rebalance_threshold_policy
)
from usa_signal_bot.portfolio_rebalance.dust_guard import suppress_dust_rebalance_actions
from usa_signal_bot.portfolio_rebalance.turnover_cost import estimate_actions_turnover_cost
from usa_signal_bot.portfolio_rebalance.turnover_control import assess_turnover, suppress_actions_to_fit_turnover
from usa_signal_bot.portfolio_rebalance.cost_aware_rebalance import apply_cost_aware_rebalance_filter
from usa_signal_bot.portfolio_rebalance.regime_rebalance_throttle import apply_regime_rebalance_throttle
from usa_signal_bot.portfolio_rebalance.drawdown_rebalance_throttle import apply_drawdown_rebalance_throttle

class RebalancePlanner:
    def __init__(self, mode: RebalanceMode = RebalanceMode.HYBRID, threshold_policy: Optional[RebalanceThresholdPolicy] = None):
        self.mode = mode
        self.threshold_policy = threshold_policy or default_rebalance_threshold_policy()

    def action_from_symbol_delta(
        self,
        symbol: str,
        current_position: Optional[PortfolioPosition],
        target_position: Optional[PortfolioPosition]
    ) -> RebalanceAction:

        current_notional = current_position.market_value_usd if current_position else 0.0
        target_notional = target_position.market_value_usd if target_position else 0.0

        delta = target_notional - current_notional

        if current_position is None and target_position is not None:
            action_type = RebalanceActionType.ENTER
        elif current_position is not None and target_position is None:
            action_type = RebalanceActionType.EXIT
        elif delta > 0:
            action_type = RebalanceActionType.INCREASE
        elif delta < 0:
            action_type = RebalanceActionType.DECREASE
        else:
            action_type = RebalanceActionType.HOLD

        return RebalanceAction(
            action_id=create_rebalance_action_id(symbol),
            symbol=symbol,
            action_type=action_type,
            status=RebalanceStatus.PROPOSED if action_type != RebalanceActionType.HOLD else RebalanceStatus.NOT_NEEDED,
            current_notional_usd=current_notional,
            target_notional_usd=target_notional,
            delta_notional_usd=delta,
            warnings=[],
            errors=[],
            metadata={}
        )

    def propose_actions(
        self,
        current: CurrentPortfolioState,
        target: TargetPortfolioState,
        drift_measurements: List[DriftMeasurement]
    ) -> List[RebalanceAction]:

        current_map = {p.symbol: p for p in current.positions}
        target_map = {p.symbol: p for p in target.target_positions}

        all_symbols = set(current_map.keys()).union(set(target_map.keys()))
        actions = []

        for symbol in sorted(all_symbols):
            curr_pos = current_map.get(symbol)
            tgt_pos = target_map.get(symbol)

            action = self.action_from_symbol_delta(symbol, curr_pos, tgt_pos)

            # Use threshold policy
            if action.status == RebalanceStatus.PROPOSED:
                drift_m = next((m for m in drift_measurements if m.name == symbol and m.drift_type.value == "SYMBOL_WEIGHT"), None)
                if drift_m and drift_m.absolute_drift is not None:
                    if drift_m.absolute_drift < self.threshold_policy.min_symbol_drift_pct:
                        action.status = RebalanceStatus.NOT_NEEDED

            actions.append(action)

        return actions

    def apply_rebalance_controls(
        self,
        actions: List[RebalanceAction],
        current: CurrentPortfolioState,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[RebalanceAction], TurnoverAssessment]:

        context = context or {}

        # 1. Dust guard
        actions = suppress_dust_rebalance_actions(actions, self.threshold_policy.min_trade_notional_usd)

        # 2. Cost estimation and filtering
        cost_map = context.get("cost_payloads_by_symbol")
        actions = estimate_actions_turnover_cost(actions, cost_map)
        actions = apply_cost_aware_rebalance_filter(actions, cost_map)

        # 3. Regime throttle
        regime_payload = context.get("regime_payload")
        transition_payload = context.get("transition_payload")
        actions = apply_regime_rebalance_throttle(actions, regime_payload, transition_payload)

        # 4. Drawdown throttle
        drawdown_pct = context.get("drawdown_pct")
        actions = apply_drawdown_rebalance_throttle(actions, drawdown_pct)

        # 5. Turnover cap (this assesses and suppresses to fit)
        actions = suppress_actions_to_fit_turnover(actions, current.total_equity_usd, self.threshold_policy.max_turnover_pct_equity)

        # 6. Final turnover assessment
        turnover = assess_turnover(actions, current.total_equity_usd, self.threshold_policy.max_turnover_pct_equity)

        return actions, turnover

    def decide_plan_status(self, actions: List[RebalanceAction], drift_measurements: List[DriftMeasurement], turnover: Optional[TurnoverAssessment] = None) -> RebalanceStatus:
        if all(a.status == RebalanceStatus.NOT_NEEDED for a in actions):
            return RebalanceStatus.NOT_NEEDED

        has_proposed = any(a.status == RebalanceStatus.PROPOSED for a in actions)
        if not has_proposed:
            return RebalanceStatus.BLOCKED # All actions were suppressed or blocked

        return RebalanceStatus.PROPOSED

    def build_plan(self, current: CurrentPortfolioState, target: TargetPortfolioState, context: Optional[Dict[str, Any]] = None) -> RebalancePlan:
        drift_measurements = calculate_symbol_drift(current, target, self.threshold_policy.min_symbol_drift_pct)

        actions = self.propose_actions(current, target, drift_measurements)

        actions, turnover = self.apply_rebalance_controls(actions, current, context)

        status = self.decide_plan_status(actions, drift_measurements, turnover)

        total_delta = sum(a.delta_notional_usd for a in actions if a.delta_notional_usd is not None and a.status == RebalanceStatus.PROPOSED)
        proposed_count = sum(1 for a in actions if a.status == RebalanceStatus.PROPOSED)
        suppressed_count = sum(1 for a in actions if "SUPPRESSED" in a.status.value)
        blocked_count = sum(1 for a in actions if a.status == RebalanceStatus.BLOCKED)

        return RebalancePlan(
            plan_id=create_rebalance_plan_id(),
            created_at_utc=datetime.datetime.now(timezone.utc).isoformat(),
            mode=self.mode,
            status=status,
            proposed_action_count=proposed_count,
            suppressed_action_count=suppressed_count,
            blocked_action_count=blocked_count,
            current_state=current,
            target_state=target,
            drift_measurements=drift_measurements,
            actions=actions,
            turnover_assessment=turnover,
            total_delta_notional_usd=total_delta
        )
