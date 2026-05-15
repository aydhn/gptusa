from typing import Optional, Dict, Any, List
from usa_signal_bot.core.enums import CostLifecycleRegime

def classify_cost_lifecycle_regime(corporate_action_status: Optional[Any] = None, lifecycle_status: Optional[Any] = None, adjusted_validation_status: Optional[Any] = None) -> CostLifecycleRegime:
    ls = str(lifecycle_status).upper() if lifecycle_status else ""
    ca = str(corporate_action_status).upper() if corporate_action_status else ""
    adj = str(adjusted_validation_status).upper() if adjusted_validation_status else ""

    if "DELIST" in ls or "BANKRUPT" in ls:
        return CostLifecycleRegime.DELISTING_RISK
    if "INCONSISTENT" in adj or "WARNING" in adj:
        return CostLifecycleRegime.ADJUSTED_DATA_RISK
    if "POST_SPLIT" in ca:
        return CostLifecycleRegime.POST_SPLIT_WINDOW
    if "SPLIT" in ca or "DIVIDEND" in ca or "PENDING" in ca:
        return CostLifecycleRegime.CORPORATE_ACTION_WATCH
    if "REVIEW" in ls:
        return CostLifecycleRegime.LIFECYCLE_REVIEW

    return CostLifecycleRegime.NORMAL

def lifecycle_cost_multiplier(regime: CostLifecycleRegime) -> float:
    mapping = {
        CostLifecycleRegime.NORMAL: 1.00,
        CostLifecycleRegime.CORPORATE_ACTION_WATCH: 1.50,
        CostLifecycleRegime.POST_SPLIT_WINDOW: 2.00,
        CostLifecycleRegime.ADJUSTED_DATA_RISK: 2.50,
        CostLifecycleRegime.LIFECYCLE_REVIEW: 2.50,
        CostLifecycleRegime.DELISTING_RISK: 4.00,
        CostLifecycleRegime.UNKNOWN: 1.00,
    }
    return mapping.get(regime, 1.00)

def lifecycle_cost_warnings(regime: CostLifecycleRegime, evidence: Optional[Dict[str, Any]] = None) -> List[str]:
    warnings = []
    if regime == CostLifecycleRegime.DELISTING_RISK:
        warnings.append("Delisting risk detected. Execution highly uncertain.")
    elif regime == CostLifecycleRegime.ADJUSTED_DATA_RISK:
        warnings.append("Adjusted data inconsistency. Simulated costs may be flawed.")
    return warnings

def lifecycle_regime_to_text(regime: CostLifecycleRegime, multiplier: Optional[float] = None) -> str:
    mult_text = f" (Multiplier: {multiplier:.2f})" if multiplier is not None else ""
    return f"Lifecycle Regime: {regime.value}{mult_text}"
