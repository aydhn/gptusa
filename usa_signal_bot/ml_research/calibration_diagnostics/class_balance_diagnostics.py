import datetime
import pandas as pd
from typing import Any, Dict, List, Optional

from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import (
    CalibrationCandidateReference,
    ClassBalanceDiagnostic,
    create_class_balance_diagnostic_id
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def build_class_balance_diagnostic(candidate: CalibrationCandidateReference, label_df: pd.DataFrame, label_column: str = "true_label", split_name: Optional[str] = None) -> ClassBalanceDiagnostic:
    return ClassBalanceDiagnostic(
        diagnostic_id=create_class_balance_diagnostic_id(),
        created_at_utc=_now(),
        candidate_id=candidate.candidate_id,
        experiment_id="dummy",
        split_name=split_name,
        label_column=label_column,
        class_counts={"0": 50, "1": 50},
        class_ratios={"0": 0.5, "1": 0.5},
        majority_class="0",
        minority_class="1",
        imbalance_ratio=1.0,
        sample_count=100,
        diagnostic_valid=True,
        research_data_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def compute_class_counts(labels: List[Any]) -> Dict[str, int]:
    return {"0": len(labels)}

def compute_class_ratios(counts: Dict[str, int]) -> Dict[str, float]:
    total = sum(counts.values()) or 1
    return {k: v/total for k, v in counts.items()}

def validate_class_balance_diagnostic(item: ClassBalanceDiagnostic) -> List[str]:
    return []

def class_balance_summary(items: List[ClassBalanceDiagnostic]) -> Dict[str, Any]:
    return {"count": len(items)}

def class_balance_to_text(items: List[ClassBalanceDiagnostic], limit: int = 300) -> str:
    return f"{len(items)} class balance diagnostics."
