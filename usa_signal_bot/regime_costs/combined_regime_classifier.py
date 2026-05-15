from typing import Optional, Dict, Any, List
from usa_signal_bot.core.enums import (
    CostVolatilityRegime, CostLiquidityRegime, CostSpreadRegime, CostSessionRegime, CostLifecycleRegime, CombinedCostRegime
)
from usa_signal_bot.regime_costs.regime_cost_models import (
    CostRegimeSnapshot, RegimeCostMultiplier, create_cost_regime_snapshot_id, create_regime_cost_multiplier_id, get_utc_now_str
)
from usa_signal_bot.regime_costs.volatility_regime_cost import classify_cost_volatility_regime, volatility_cost_multiplier, volatility_cost_warnings
from usa_signal_bot.regime_costs.liquidity_regime_cost import classify_cost_liquidity_regime, liquidity_cost_multiplier, liquidity_cost_warnings
from usa_signal_bot.regime_costs.spread_regime_cost import classify_cost_spread_regime, spread_cost_multiplier, spread_cost_warnings
from usa_signal_bot.regime_costs.session_regime_cost import classify_cost_session_regime, session_cost_multiplier, session_cost_warnings
from usa_signal_bot.regime_costs.lifecycle_regime_cost import classify_cost_lifecycle_regime, lifecycle_cost_multiplier, lifecycle_cost_warnings

def classify_combined_cost_regime(volatility: CostVolatilityRegime, liquidity: CostLiquidityRegime, spread: CostSpreadRegime, session: CostSessionRegime, lifecycle: CostLifecycleRegime) -> CombinedCostRegime:
    if session in (CostSessionRegime.CLOSED, CostSessionRegime.HOLIDAY) or liquidity == CostLiquidityRegime.FROZEN:
        return CombinedCostRegime.BLOCKED

    if lifecycle == CostLifecycleRegime.DELISTING_RISK or \
       (volatility == CostVolatilityRegime.EXTREME and liquidity == CostLiquidityRegime.ILLIQUID) or \
       session in (CostSessionRegime.PREMARKET, CostSessionRegime.AFTER_HOURS):
        return CombinedCostRegime.HIGH_RISK

    if spread in (CostSpreadRegime.WIDE, CostSpreadRegime.VERY_WIDE) or liquidity == CostLiquidityRegime.THIN or volatility == CostVolatilityRegime.HIGH:
        return CombinedCostRegime.STRESSED

    if CostVolatilityRegime.INSUFFICIENT_DATA in (volatility, liquidity, spread):
        return CombinedCostRegime.INSUFFICIENT_DATA

    return CombinedCostRegime.NORMAL

def build_cost_regime_snapshot(
    symbol: str,
    vol_evidence: Optional[Dict[str, Any]] = None,
    liquidity_profile: Optional[Dict[str, Any]] = None,
    spread_proxy_bps: Optional[float] = None,
    session_type: Optional[Any] = None,
    corporate_action_metadata: Optional[Dict[str, Any]] = None,
    lifecycle_metadata: Optional[Dict[str, Any]] = None,
    extra_evidence: Optional[Dict[str, Any]] = None
) -> CostRegimeSnapshot:

    ve = vol_evidence or {}
    lp = liquidity_profile or {}

    vol = classify_cost_volatility_regime(ve.get("atr_pct"), ve.get("gap_pct"), ve.get("realized_vol_pct"))
    liq = classify_cost_liquidity_regime(lp.get("avg_dollar_volume"), lp.get("avg_daily_volume"), lp.get("liquidity_status"))
    spr = classify_cost_spread_regime(spread_proxy_bps)
    sess = classify_cost_session_regime(session_type)

    ca_stat = corporate_action_metadata.get("status") if corporate_action_metadata else None
    lf_stat = lifecycle_metadata.get("status") if lifecycle_metadata else None
    adj_stat = extra_evidence.get("adjusted_validation_status") if extra_evidence else None
    lfc = classify_cost_lifecycle_regime(ca_stat, lf_stat, adj_stat)

    combined = classify_combined_cost_regime(vol, liq, spr, sess, lfc)

    evidence = {
        "vol_evidence": ve,
        "liquidity_profile": lp,
        "spread_proxy_bps": spread_proxy_bps,
        "session_type": session_type,
        "corporate_action_metadata": corporate_action_metadata,
        "lifecycle_metadata": lifecycle_metadata,
        "extra": extra_evidence or {}
    }

    warnings = []
    warnings.extend(volatility_cost_warnings(vol))
    warnings.extend(liquidity_cost_warnings(liq))
    warnings.extend(spread_cost_warnings(spr))
    warnings.extend(session_cost_warnings(sess))
    warnings.extend(lifecycle_cost_warnings(lfc))

    return CostRegimeSnapshot(
        snapshot_id=create_cost_regime_snapshot_id(symbol),
        symbol=symbol,
        created_at_utc=get_utc_now_str(),
        volatility_regime=vol,
        liquidity_regime=liq,
        spread_regime=spr,
        session_regime=sess,
        lifecycle_regime=lfc,
        combined_regime=combined,
        evidence=evidence,
        warnings=warnings,
        errors=[],
        metadata={}
    )

def build_regime_cost_multiplier(symbol: Optional[str], snapshot: CostRegimeSnapshot) -> RegimeCostMultiplier:
    vm = volatility_cost_multiplier(snapshot.volatility_regime)
    lm = liquidity_cost_multiplier(snapshot.liquidity_regime)
    sm = spread_cost_multiplier(snapshot.spread_regime)
    sem = session_cost_multiplier(snapshot.session_regime)
    lfm = lifecycle_cost_multiplier(snapshot.lifecycle_regime)

    combined = max(1.0, vm * lm * sm * sem * lfm)
    # cap it to avoid ridiculous numbers (e.g. 500x)
    if combined > 10.0:
        combined = 10.0

    return RegimeCostMultiplier(
        multiplier_id=create_regime_cost_multiplier_id(symbol),
        symbol=symbol,
        created_at_utc=get_utc_now_str(),
        volatility_multiplier=vm,
        liquidity_multiplier=lm,
        spread_multiplier=sm,
        session_multiplier=sem,
        lifecycle_multiplier=lfm,
        combined_multiplier=combined,
        min_cost_bps=None,
        max_cost_bps=None,
        warnings=[],
        errors=[],
        metadata={}
    )

def combined_regime_warnings(snapshot: CostRegimeSnapshot) -> List[str]:
    w = []
    if snapshot.combined_regime == CombinedCostRegime.BLOCKED:
        w.append("Combined regime is BLOCKED. Fills should not be simulated.")
    elif snapshot.combined_regime == CombinedCostRegime.HIGH_RISK:
        w.append("Combined regime is HIGH RISK. Costs will be heavily penalized.")
    elif snapshot.combined_regime == CombinedCostRegime.STRESSED:
        w.append("Combined regime is STRESSED. Slippage and impact will be elevated.")
    return w

def combined_regime_to_text(snapshot: CostRegimeSnapshot) -> str:
    return f"Combined Cost Regime for {snapshot.symbol}: {snapshot.combined_regime.value}"
