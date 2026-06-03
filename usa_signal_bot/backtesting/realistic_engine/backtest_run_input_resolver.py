import pandas as pd
from typing import Dict, Any, List

def validate_price_bars_for_run(df: pd.DataFrame) -> List[str]:
    errors = []
    required = ["symbol", "timestamp", "open", "high", "low", "close", "volume"]
    for c in required:
        if c not in df.columns:
            errors.append(f"Missing price column: {c}")
    return errors

def validate_research_predictions_for_run(df: pd.DataFrame) -> List[str]:
    errors = []
    required = ["symbol", "timestamp"]
    for c in required:
        if c not in df.columns:
            errors.append(f"Missing prediction column: {c}")
    return errors

def align_price_and_prediction_frames(price_bars: pd.DataFrame, research_predictions: pd.DataFrame) -> pd.DataFrame:
    # merge on symbol and timestamp
    df = pd.merge(price_bars, research_predictions, on=["symbol", "timestamp"], how="inner")
    return df

def detect_forbidden_backtest_run_columns(columns: List[str]) -> List[str]:
    forbidden = ["buy_signal", "sell_signal", "entry", "exit", "broker_order",
                 "paper_order", "live_order", "sent_to_broker", "strategy_active",
                 "deployment_enabled", "portfolio_weight", "target_weight", "allocation"]
    found = [c for c in columns if c in forbidden]
    return found

def resolve_backtest_run_inputs(price_bars: pd.DataFrame, research_predictions: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    err_prices = validate_price_bars_for_run(price_bars)
    err_preds = validate_research_predictions_for_run(research_predictions)
    if err_prices or err_preds:
        raise ValueError(f"Input validation failed: {err_prices} {err_preds}")

    aligned = align_price_and_prediction_frames(price_bars, research_predictions)
    forb = detect_forbidden_backtest_run_columns(list(aligned.columns))
    if forb:
        raise ValueError(f"Forbidden columns detected: {forb}")
    return {"aligned_data": aligned}

def backtest_run_input_resolver_summary(frames: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    return {"frames_resolved": list(frames.keys())}
