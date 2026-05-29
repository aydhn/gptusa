import pandas as pd
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.exceptions import RegimeChurnDiagnosticsError
from usa_signal_bot.core.enums import RegimeDiagnosticsQuality, RegimeChurnLevel
from usa_signal_bot.regime_classification.diagnostics.phase129_models import (
    RegimeChurnDiagnostic,
    create_regime_churn_diagnostic_id,
    _now
)

def churn_level_from_switch_rate(switch_rate: Optional[float]) -> RegimeChurnLevel:
    if switch_rate is None:
        return RegimeChurnLevel.INSUFFICIENT_DATA
    if switch_rate < 0.05:
        return RegimeChurnLevel.LOW
    elif switch_rate < 0.15:
        return RegimeChurnLevel.MODERATE
    elif switch_rate < 0.30:
        return RegimeChurnLevel.HIGH
    else:
        return RegimeChurnLevel.EXTREME

def compute_switch_rate(labels: List[str]) -> float:
    valid_labels = [str(L) for L in labels if not pd.isna(L)]
    if len(valid_labels) < 2:
        return 0.0
    switches = 0
    for i in range(len(valid_labels) - 1):
        if valid_labels[i] != valid_labels[i + 1]:
            switches += 1
    return switches / (len(valid_labels) - 1)

def count_low_confidence(confidences: List[float], threshold: float = 40.0) -> int:
    return sum(1 for c in confidences if not pd.isna(c) and c < threshold)

def build_churn_diagnostic_for_table(symbol: Optional[str], df: pd.DataFrame, label_column: str = "regime_label_research", confidence_column: str = "regime_label_confidence") -> RegimeChurnDiagnostic:
    if label_column not in df.columns:
        raise RegimeChurnDiagnosticsError(f"Missing column '{label_column}'")

    labels = df[label_column].tolist()
    valid_labels = [str(L) for L in labels if not pd.isna(L)]
    switch_rate = compute_switch_rate(labels)
    switches = int(switch_rate * (len(valid_labels) - 1)) if len(valid_labels) > 1 else 0

    low_conf = 0
    if confidence_column in df.columns:
        low_conf = count_low_confidence(df[confidence_column].tolist())

    level = churn_level_from_switch_rate(switch_rate)
    notes = [f"Switch rate: {switch_rate:.4f}"]
    if level in (RegimeChurnLevel.HIGH, RegimeChurnLevel.EXTREME):
        notes.append("High churn detected. Consider applying smoother rolling windows or lowering threshold.")

    return RegimeChurnDiagnostic(
        churn_id=create_regime_churn_diagnostic_id(),
        created_at_utc=_now(),
        symbol=symbol,
        label_column=label_column,
        row_count=len(df),
        switch_count=switches,
        switch_rate=switch_rate,
        churn_level=level,
        low_confidence_count=low_conf,
        conflict_count=0, # placeholder, could be loaded from stability profiles if available
        window_disagreement_count=0, # placeholder
        notes=notes,
        quality=RegimeDiagnosticsQuality.HIGH if level != RegimeChurnLevel.EXTREME else RegimeDiagnosticsQuality.WARNING,
        research_metadata_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
    )

def build_churn_diagnostics(tables: Dict[str, pd.DataFrame]) -> List[RegimeChurnDiagnostic]:
    diags = []
    for symbol, df in tables.items():
        diags.append(build_churn_diagnostic_for_table(symbol, df))
    return diags

def validate_churn_diagnostics(items: List[RegimeChurnDiagnostic]) -> List[str]:
    errors = []
    for d in items:
        if d.switch_rate < 0 or d.switch_rate > 1:
            errors.append(f"Invalid switch rate {d.switch_rate} for {d.symbol}")
    return errors

def churn_diagnostics_summary(items: List[RegimeChurnDiagnostic]) -> Dict[str, Any]:
    levels = [d.churn_level.value for d in items]
    return {
        "count": len(items),
        "high_extreme_count": sum(1 for d in items if d.churn_level in (RegimeChurnLevel.HIGH, RegimeChurnLevel.EXTREME))
    }

def churn_diagnostics_to_text(items: List[RegimeChurnDiagnostic], limit: int = 300) -> str:
    lines = ["Regime Churn Diagnostics"]
    for d in items[:limit]:
        lines.append(f"[{d.symbol or 'UNKNOWN'}] Rate: {d.switch_rate:.4f}, Level: {d.churn_level.value}, LowConf: {d.low_confidence_count}")
    return "\n".join(lines)
