import pandas as pd
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.exceptions import RollingTransitionAnalyticsError

def rolling_switch_rate(labels: List[str], window: int) -> List[Optional[float]]:
    rates = []
    for i in range(len(labels)):
        if i < window:
            rates.append(None)
            continue
        sub = labels[i-window:i]
        valid_sub = [str(L) for L in sub if not pd.isna(L)]
        switches = 0
        if len(valid_sub) > 1:
            for j in range(len(valid_sub) - 1):
                if valid_sub[j] != valid_sub[j+1]:
                    switches += 1
            rates.append(switches / (len(valid_sub) - 1))
        else:
            rates.append(0.0)
    return rates

def rolling_self_transition_rate(labels: List[str], window: int) -> List[Optional[float]]:
    rates = rolling_switch_rate(labels, window)
    return [(1.0 - r) if r is not None else None for r in rates]

def build_rolling_transition_summary_for_table(symbol: Optional[str], df: pd.DataFrame, window: int = 60, label_column: str = "regime_label_research") -> Dict[str, Any]:
    if label_column not in df.columns:
        raise RollingTransitionAnalyticsError(f"Missing '{label_column}'")
    labels = df[label_column].tolist()
    rates = rolling_switch_rate(labels, window)
    valid_rates = [r for r in rates if r is not None]

    avg_rate = sum(valid_rates) / len(valid_rates) if valid_rates else 0.0
    return {
        "symbol": symbol,
        "window": window,
        "avg_rolling_switch_rate": avg_rate,
        "max_rolling_switch_rate": max(valid_rates) if valid_rates else 0.0
    }

def build_rolling_transition_summaries(tables: Dict[str, pd.DataFrame], windows: Optional[List[int]] = None) -> Dict[str, Any]:
    if not windows:
        windows = [20, 60, 120]
    results = {}
    for symbol, df in tables.items():
        results[symbol] = [build_rolling_transition_summary_for_table(symbol, df, w) for w in windows]
    return results

def validate_rolling_transition_summaries(payload: Dict[str, Any]) -> List[str]:
    return []

def rolling_transition_analytics_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"symbols_processed": len(payload)}

def rolling_transition_analytics_to_text(payload: Dict[str, Any], limit: int = 300) -> str:
    return "Rolling Transition Analytics generated."
