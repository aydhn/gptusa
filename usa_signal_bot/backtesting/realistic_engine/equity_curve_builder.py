import datetime
import pandas as pd
from typing import Dict, Any, List
from .phase147_models import (
    BacktestRunConfig, ExposureStateRecord, EquityCurvePoint, create_equity_curve_point_id
)

def build_equity_curve(exposure_timeline: List[ExposureStateRecord], config: BacktestRunConfig) -> List[EquityCurvePoint]:
    curve = []
    by_time = {}
    for st in exposure_timeline:
        if st.timestamp not in by_time:
            by_time[st.timestamp] = {"eq": 0.0, "cash": 0.0, "mkt": 0.0}
        by_time[st.timestamp]["eq"] += st.simulated_equity
        by_time[st.timestamp]["cash"] += st.simulated_cash
        by_time[st.timestamp]["mkt"] += st.simulated_market_value

    for ts in sorted(by_time.keys()):
        val = by_time[ts]
        ret = (val["eq"] - config.initial_cash) / config.initial_cash if config.initial_cash > 0 else 0.0
        curve.append(EquityCurvePoint(
            point_id=create_equity_curve_point_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            run_id=config.config_id,
            timestamp=ts,
            simulated_equity=val["eq"],
            simulated_cash=val["cash"],
            simulated_market_value=val["mkt"],
            cumulative_simulated_return=ret,
            point_valid=True,
            research_data_only=True,
            investment_advice=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return curve

def validate_equity_curve(items: List[EquityCurvePoint]) -> List[str]:
    return []

def equity_curve_to_dataframe(items: List[EquityCurvePoint]) -> pd.DataFrame:
    return pd.DataFrame([i.__dict__ for i in items])

def equity_curve_summary(items: List[EquityCurvePoint]) -> Dict[str, Any]:
    return {"point_count": len(items)}
