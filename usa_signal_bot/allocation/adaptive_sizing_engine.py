from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timezone

from usa_signal_bot.core.enums import CapitalAllocationMode, PositionSizeStatus, RiskBudgetStatus, SizingAdjustmentReason
from usa_signal_bot.allocation.allocation_models import (
    CapitalState, RiskBudget, SizingInput, SizingAdjustment, PositionSizeResult,
    create_position_size_result_id, validate_position_size_result
)
from usa_signal_bot.allocation.confidence_scaling import combine_confidence_inputs, confidence_to_size_multiplier
from usa_signal_bot.allocation.volatility_sizing import notional_from_volatility_target, volatility_size_multiplier, volatility_sizing_adjustment
from usa_signal_bot.allocation.liquidity_size_adjuster import apply_liquidity_size_adjustment, liquidity_size_multiplier
from usa_signal_bot.allocation.cost_size_adjuster import apply_cost_size_adjustment, cost_size_multiplier
from usa_signal_bot.allocation.regime_size_adjuster import apply_regime_size_adjustment, regime_size_multiplier
from usa_signal_bot.allocation.drawdown_throttle import apply_drawdown_throttle, drawdown_risk_multiplier
from usa_signal_bot.allocation.concentration_guard import apply_concentration_guard, concentration_size_multiplier
from usa_signal_bot.allocation.position_caps import apply_max_position_notional_cap, apply_portfolio_cap, apply_min_position_notional_floor
from usa_signal_bot.allocation.dollar_risk_sizing import calculate_dollar_risk_amount

class AdaptiveSizingEngine:
    def __init__(self, mode: CapitalAllocationMode = CapitalAllocationMode.ADAPTIVE, min_notional_usd: float = 10.0):
        self.mode = mode
        self.min_notional_usd = min_notional_usd

    def size_position(self, input_payload: SizingInput, capital_state: CapitalState, risk_budget: RiskBudget) -> PositionSizeResult:
        warnings = []
        errors = []
        adjustments = []

        # 1. Budget exhausted check
        if risk_budget.status in [RiskBudgetStatus.EXHAUSTED, RiskBudgetStatus.BLOCKED]:
            return self._build_blocked_result(input_payload, capital_state, risk_budget, "Risk budget exhausted or blocked.")

        # 2. Capital check
        if capital_state.available_cash_usd <= 0:
            return self._build_blocked_result(input_payload, capital_state, risk_budget, "Insufficient available cash.")

        # 3. Base Notional Calculation (Volatility / Dollar Risk)
        conf_score = combine_confidence_inputs(
            input_payload.signal_score,
            input_payload.signal_confidence,
            input_payload.ensemble_consensus_score,
            input_payload.regime_alignment_score,
            input_payload.cost_robustness_score,
            input_payload.execution_realism_score
        )
        conf_mult = confidence_to_size_multiplier(conf_score)

        if input_payload.atr_pct:
            initial_notional = notional_from_volatility_target(capital_state, risk_budget, input_payload.atr_pct, conf_mult)
            vol_adj = volatility_sizing_adjustment(input_payload.atr_pct)
            if vol_adj.multiplier != 1.0:
                 adjustments.append(vol_adj)
            vol_mult = vol_adj.multiplier
        else:
            # Fallback to pure dollar risk if ATR is missing, treating requested_notional if exists, else portfolio %
            risk_amt = calculate_dollar_risk_amount(capital_state, risk_budget.per_trade_risk_budget_pct)
            initial_notional = (input_payload.requested_notional_usd or (risk_amt * 10)) * conf_mult
            vol_mult = 1.0

        if initial_notional is None or initial_notional <= 0:
            return self._build_blocked_result(input_payload, capital_state, risk_budget, "Could not determine positive initial notional.")

        # 4. Apply Adjustments
        current_notional, current_adjs = self.apply_all_adjustments(initial_notional, input_payload, capital_state, risk_budget)
        adjustments.extend(current_adjs)

        # 5. Calculate final status and metrics
        status = self.decide_position_size_status(current_notional, adjustments, risk_budget)

        if current_notional is not None and current_notional < self.min_notional_usd:
            status = PositionSizeStatus.SUPPRESSED
            current_notional = 0.0

        quantity = self.quantity_from_notional(current_notional, input_payload.reference_price)

        risk_pct = 0.0
        risk_amount = 0.0
        if current_notional and current_notional > 0 and capital_state.total_equity_usd > 0:
            risk_pct = (current_notional / capital_state.total_equity_usd) * 100.0
            risk_amount = current_notional * (input_payload.stop_distance_pct or 1.0) / 100.0

        result = PositionSizeResult(
            result_id=create_position_size_result_id(input_payload.symbol),
            symbol=input_payload.symbol,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            mode=self.mode,
            status=status,
            side=input_payload.side,
            reference_price=input_payload.reference_price,
            initial_notional_usd=initial_notional,
            final_notional_usd=current_notional,
            final_quantity=quantity,
            risk_amount_usd=risk_amount,
            risk_pct_equity=risk_pct,
            confidence_multiplier=conf_mult,
            volatility_multiplier=vol_mult,
            liquidity_multiplier=liquidity_size_multiplier(input_payload.metadata.get("liquidity")),
            cost_multiplier=cost_size_multiplier(input_payload.metadata.get("cost")),
            regime_multiplier=regime_size_multiplier(input_payload.metadata.get("regime")),
            drawdown_multiplier=drawdown_risk_multiplier(input_payload.metadata.get("drawdown_pct")),
            concentration_multiplier=concentration_size_multiplier(input_payload.metadata.get("concentration_max_pct")),
            adjustments=adjustments,
            budget=risk_budget,
            capital_state=capital_state,
            warnings=warnings,
            errors=errors,
            metadata={"note": "Local adaptive sizing metadata. Not a live broker order."}
        )
        validate_position_size_result(result)
        return result

    def size_many(self, inputs: List[SizingInput], capital_state: CapitalState, risk_budget: RiskBudget) -> List[PositionSizeResult]:
        results = []
        for inp in inputs:
            results.append(self.size_position(inp, capital_state, risk_budget))
        return results

    def initial_notional(self, input_payload: SizingInput, capital_state: CapitalState, risk_budget: RiskBudget) -> Optional[float]:
         # Helper to just get base notional
         conf_score = combine_confidence_inputs(input_payload.signal_score, input_payload.signal_confidence)
         conf_mult = confidence_to_size_multiplier(conf_score)
         return notional_from_volatility_target(capital_state, risk_budget, input_payload.atr_pct, conf_mult)

    def apply_all_adjustments(self, notional_usd: Optional[float], input_payload: SizingInput, capital_state: CapitalState, risk_budget: RiskBudget) -> Tuple[Optional[float], List[SizingAdjustment]]:
        adjustments = []
        current = notional_usd

        # Liquidity
        current, adj = apply_liquidity_size_adjustment(current, input_payload.metadata.get("liquidity"), input_payload.metadata.get("tradability"))
        if adj: adjustments.append(adj)

        # Cost
        current, adj = apply_cost_size_adjustment(current, input_payload.metadata.get("cost"), input_payload.metadata.get("robustness"))
        if adj: adjustments.append(adj)

        # Regime
        current, adj = apply_regime_size_adjustment(current, input_payload.metadata.get("regime"), input_payload.metadata.get("transition"), input_payload.metadata.get("alignment"))
        if adj: adjustments.append(adj)

        # Drawdown
        current, adj = apply_drawdown_throttle(current, input_payload.metadata.get("drawdown_pct"))
        if adj: adjustments.append(adj)

        # Concentration
        current, adj = apply_concentration_guard(current, input_payload.metadata.get("concentration"))
        if adj: adjustments.append(adj)

        # Max Position Cap
        current, adj = apply_max_position_notional_cap(current, capital_state, risk_budget)
        if adj: adjustments.append(adj)

        # Portfolio Cap
        current, adj = apply_portfolio_cap(current, capital_state)
        if adj: adjustments.append(adj)

        # Floor check
        current, adj = apply_min_position_notional_floor(current, self.min_notional_usd)
        if adj: adjustments.append(adj)

        return current, adjustments

    def decide_position_size_status(self, final_notional_usd: Optional[float], adjustments: List[SizingAdjustment], budget: RiskBudget) -> PositionSizeStatus:
        if final_notional_usd is None or final_notional_usd <= 0:
            return PositionSizeStatus.BLOCKED

        has_reduction = any(a.multiplier < 1.0 for a in adjustments if a.reason not in [SizingAdjustmentReason.PORTFOLIO_CAP, SizingAdjustmentReason.DRAWDOWN_THROTTLE])
        has_cap = any(a.reason == SizingAdjustmentReason.PORTFOLIO_CAP for a in adjustments)
        has_throttle = any(a.reason == SizingAdjustmentReason.DRAWDOWN_THROTTLE for a in adjustments)

        if has_throttle:
            return PositionSizeStatus.THROTTLED
        elif has_reduction:
            return PositionSizeStatus.REDUCED
        elif has_cap:
            return PositionSizeStatus.CAPPED

        return PositionSizeStatus.APPROVED

    def quantity_from_notional(self, notional_usd: Optional[float], reference_price: Optional[float]) -> Optional[float]:
        if notional_usd is None or reference_price is None or reference_price <= 0:
            return None
        return notional_usd / reference_price

    def _build_blocked_result(self, input_payload: SizingInput, capital_state: CapitalState, budget: RiskBudget, reason_str: str) -> PositionSizeResult:
        return PositionSizeResult(
            result_id=create_position_size_result_id(input_payload.symbol),
            symbol=input_payload.symbol,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            mode=self.mode,
            status=PositionSizeStatus.BLOCKED,
            side=input_payload.side,
            reference_price=input_payload.reference_price,
            initial_notional_usd=None,
            final_notional_usd=0.0,
            final_quantity=0.0,
            risk_amount_usd=0.0,
            risk_pct_equity=0.0,
            confidence_multiplier=1.0,
            volatility_multiplier=1.0,
            liquidity_multiplier=1.0,
            cost_multiplier=1.0,
            regime_multiplier=1.0,
            drawdown_multiplier=1.0,
            concentration_multiplier=1.0,
            adjustments=[],
            budget=budget,
            capital_state=capital_state,
            warnings=[reason_str],
            errors=[],
            metadata={"note": "Blocked by engine."}
        )
