from dataclasses import dataclass
from typing import Any, Dict, Optional
from usa_signal_bot.core.config_schema import RebalanceThresholdsConfig

@dataclass
class RebalanceThresholdPolicy:
    min_symbol_drift_pct: float
    min_exposure_drift_pct: float
    min_bucket_drift_pct: float
    min_trade_notional_usd: float
    max_turnover_pct_equity: float
    max_action_count: int
    cost_sensitive_multiplier: float
    regime_sensitive_multiplier: float
    drawdown_sensitive_multiplier: float

def default_rebalance_threshold_policy() -> RebalanceThresholdPolicy:
    cfg = RebalanceThresholdsConfig()
    return RebalanceThresholdPolicy(
        min_symbol_drift_pct=cfg.min_symbol_drift_pct,
        min_exposure_drift_pct=cfg.min_exposure_drift_pct,
        min_bucket_drift_pct=cfg.min_bucket_drift_pct,
        min_trade_notional_usd=cfg.min_trade_notional_usd,
        max_turnover_pct_equity=cfg.max_turnover_pct_equity,
        max_action_count=cfg.max_action_count,
        cost_sensitive_multiplier=cfg.cost_sensitive_multiplier,
        regime_sensitive_multiplier=cfg.regime_sensitive_multiplier,
        drawdown_sensitive_multiplier=cfg.drawdown_sensitive_multiplier
    )

def build_rebalance_threshold_policy_from_config(config_dict: Optional[Dict[str, Any]] = None) -> RebalanceThresholdPolicy:
    if not config_dict:
        return default_rebalance_threshold_policy()

    return RebalanceThresholdPolicy(
        min_symbol_drift_pct=config_dict.get("min_symbol_drift_pct", 1.0),
        min_exposure_drift_pct=config_dict.get("min_exposure_drift_pct", 3.0),
        min_bucket_drift_pct=config_dict.get("min_bucket_drift_pct", 5.0),
        min_trade_notional_usd=config_dict.get("min_trade_notional_usd", 25.0),
        max_turnover_pct_equity=config_dict.get("max_turnover_pct_equity", 10.0),
        max_action_count=config_dict.get("max_action_count", 50),
        cost_sensitive_multiplier=config_dict.get("cost_sensitive_multiplier", 1.5),
        regime_sensitive_multiplier=config_dict.get("regime_sensitive_multiplier", 1.5),
        drawdown_sensitive_multiplier=config_dict.get("drawdown_sensitive_multiplier", 2.0)
    )

def adjust_threshold_policy_for_cost(policy: RebalanceThresholdPolicy, cost_payload: Optional[Dict[str, Any]] = None) -> RebalanceThresholdPolicy:
    if not cost_payload:
        return policy

    is_high_cost = cost_payload.get("status") in ["WARNING", "HIGH", "EXCESSIVE"]
    if is_high_cost:
        multiplier = policy.cost_sensitive_multiplier
        return RebalanceThresholdPolicy(
            min_symbol_drift_pct=policy.min_symbol_drift_pct * multiplier,
            min_exposure_drift_pct=policy.min_exposure_drift_pct * multiplier,
            min_bucket_drift_pct=policy.min_bucket_drift_pct * multiplier,
            min_trade_notional_usd=policy.min_trade_notional_usd * multiplier,
            max_turnover_pct_equity=policy.max_turnover_pct_equity / multiplier,
            max_action_count=policy.max_action_count,
            cost_sensitive_multiplier=policy.cost_sensitive_multiplier,
            regime_sensitive_multiplier=policy.regime_sensitive_multiplier,
            drawdown_sensitive_multiplier=policy.drawdown_sensitive_multiplier
        )
    return policy

def adjust_threshold_policy_for_regime(policy: RebalanceThresholdPolicy, regime_payload: Optional[Dict[str, Any]] = None) -> RebalanceThresholdPolicy:
    if not regime_payload:
        return policy

    risk_level = regime_payload.get("transition_risk")
    if risk_level in ["HIGH", "CRITICAL"]:
        multiplier = policy.regime_sensitive_multiplier
        return RebalanceThresholdPolicy(
            min_symbol_drift_pct=policy.min_symbol_drift_pct * multiplier,
            min_exposure_drift_pct=policy.min_exposure_drift_pct * multiplier,
            min_bucket_drift_pct=policy.min_bucket_drift_pct * multiplier,
            min_trade_notional_usd=policy.min_trade_notional_usd * multiplier,
            max_turnover_pct_equity=policy.max_turnover_pct_equity / multiplier,
            max_action_count=policy.max_action_count,
            cost_sensitive_multiplier=policy.cost_sensitive_multiplier,
            regime_sensitive_multiplier=policy.regime_sensitive_multiplier,
            drawdown_sensitive_multiplier=policy.drawdown_sensitive_multiplier
        )
    return policy

def adjust_threshold_policy_for_drawdown(policy: RebalanceThresholdPolicy, drawdown_pct: Optional[float] = None) -> RebalanceThresholdPolicy:
    if drawdown_pct is None or drawdown_pct <= 0:
        return policy

    if drawdown_pct > 6.0:  # Moderate+ drawdown
        multiplier = policy.drawdown_sensitive_multiplier
        return RebalanceThresholdPolicy(
            min_symbol_drift_pct=policy.min_symbol_drift_pct * multiplier,
            min_exposure_drift_pct=policy.min_exposure_drift_pct * multiplier,
            min_bucket_drift_pct=policy.min_bucket_drift_pct * multiplier,
            min_trade_notional_usd=policy.min_trade_notional_usd * multiplier,
            max_turnover_pct_equity=policy.max_turnover_pct_equity / multiplier,
            max_action_count=policy.max_action_count,
            cost_sensitive_multiplier=policy.cost_sensitive_multiplier,
            regime_sensitive_multiplier=policy.regime_sensitive_multiplier,
            drawdown_sensitive_multiplier=policy.drawdown_sensitive_multiplier
        )
    return policy

def threshold_policy_to_text(policy: RebalanceThresholdPolicy) -> str:
    lines = ["Rebalance Threshold Policy:"]
    lines.append(f"  Min Symbol Drift: {policy.min_symbol_drift_pct}%")
    lines.append(f"  Min Exposure Drift: {policy.min_exposure_drift_pct}%")
    lines.append(f"  Min Bucket Drift: {policy.min_bucket_drift_pct}%")
    lines.append(f"  Min Trade Notional: ${policy.min_trade_notional_usd:.2f}")
    lines.append(f"  Max Turnover: {policy.max_turnover_pct_equity}%")
    return "\n".join(lines)
