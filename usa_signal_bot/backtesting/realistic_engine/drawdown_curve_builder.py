import datetime
import pandas as pd
from typing import Dict, Any, List
from .phase147_models import EquityCurvePoint, DrawdownPoint, create_drawdown_point_id

def build_drawdown_curve(equity_curve: List[EquityCurvePoint]) -> List[DrawdownPoint]:
    curve = []
    peak = 0.0
    for pt in equity_curve:
        if pt.simulated_equity > peak:
            peak = pt.simulated_equity

        dd_frac = (peak - pt.simulated_equity) / peak if peak > 0 else 0.0
        curve.append(DrawdownPoint(
            point_id=create_drawdown_point_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            run_id=pt.run_id,
            timestamp=pt.timestamp,
            simulated_equity=pt.simulated_equity,
            running_peak_equity=peak,
            drawdown_fraction=dd_frac,
            drawdown_percent=dd_frac * 100.0,
            point_valid=True,
            research_data_only=True,
            investment_advice=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return curve

def validate_drawdown_curve(items: List[DrawdownPoint]) -> List[str]:
    return []

def drawdown_curve_to_dataframe(items: List[DrawdownPoint]) -> pd.DataFrame:
    return pd.DataFrame([i.__dict__ for i in items])

def drawdown_curve_summary(items: List[DrawdownPoint]) -> Dict[str, Any]:
    return {"point_count": len(items)}
