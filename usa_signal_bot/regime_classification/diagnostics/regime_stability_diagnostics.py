import pandas as pd
from collections import Counter
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.exceptions import RegimeStabilityDiagnosticsError
from usa_signal_bot.core.enums import RegimeDiagnosticsQuality, RegimeStabilityDiagnosticKind
from usa_signal_bot.regime_classification.diagnostics.phase129_models import (
    RegimeStabilityDiagnostic,
    create_regime_stability_diagnostic_id,
    _now
)
from usa_signal_bot.regime_classification.diagnostics.regime_churn_diagnostics import compute_switch_rate

def compute_sequence_fragmentation_score(labels: List[str]) -> float:
    rate = compute_switch_rate(labels)
    # fragmentation score from 0 (stable) to 100 (fragmented)
    return min(100.0, rate * 100.0 * 2)

def compute_dominant_label_concentration(labels: List[str]) -> float:
    valid_labels = [str(L) for L in labels if not pd.isna(L)]
    if not valid_labels:
        return 0.0
    c = Counter(valid_labels)
    top = c.most_common(1)[0][1]
    return (top / len(valid_labels)) * 100.0

def compute_stability_diagnostic_score(labels: List[str], confidences: Optional[List[float]] = None) -> float:
    frag = compute_sequence_fragmentation_score(labels)
    conc = compute_dominant_label_concentration(labels)

    # Simple heuristic: high concentration is stable, high fragmentation is unstable.
    # Score 0 (unstable) to 100 (stable)
    score = (conc - frag)
    score = max(0.0, min(100.0, score + 50.0)) # center around 50
    return score

def build_stability_diagnostics_for_table(symbol: Optional[str], df: pd.DataFrame) -> List[RegimeStabilityDiagnostic]:
    diags = []
    if "regime_label_research" not in df.columns:
        return diags

    labels = df["regime_label_research"].tolist()
    confidences = df["regime_label_confidence"].tolist() if "regime_label_confidence" in df.columns else None

    score = compute_stability_diagnostic_score(labels, confidences)
    quality = RegimeDiagnosticsQuality.HIGH if score >= 60 else (RegimeDiagnosticsQuality.WARNING if score >= 30 else RegimeDiagnosticsQuality.LOW)

    diags.append(RegimeStabilityDiagnostic(
        stability_diag_id=create_regime_stability_diagnostic_id(),
        created_at_utc=_now(),
        symbol=symbol,
        diagnostic_kind=RegimeStabilityDiagnosticKind.SEQUENCE_FRAGMENTATION,
        diagnostic_name="Heuristic Stability Score",
        diagnostic_score=score,
        diagnostic_value=score,
        quality=quality,
        notes=["Score based on fragmentation and dominant label concentration."],
        research_metadata_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
    ))
    return diags

def build_stability_diagnostics(tables: Dict[str, pd.DataFrame]) -> List[RegimeStabilityDiagnostic]:
    diags = []
    for symbol, df in tables.items():
        diags.extend(build_stability_diagnostics_for_table(symbol, df))
    return diags

def validate_stability_diagnostics(items: List[RegimeStabilityDiagnostic]) -> List[str]:
    errors = []
    for d in items:
        if d.diagnostic_score < 0 or d.diagnostic_score > 100:
            errors.append(f"Invalid stability score {d.diagnostic_score}")
    return errors

def stability_diagnostics_summary(items: List[RegimeStabilityDiagnostic]) -> Dict[str, Any]:
    return {"count": len(items)}

def stability_diagnostics_to_text(items: List[RegimeStabilityDiagnostic], limit: int = 300) -> str:
    lines = ["Regime Stability Diagnostics"]
    for d in items[:limit]:
        lines.append(f"[{d.symbol or 'UNKNOWN'}] {d.diagnostic_name}: {d.diagnostic_score:.1f}")
    return "\n".join(lines)
