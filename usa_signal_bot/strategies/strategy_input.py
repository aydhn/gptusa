from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
import datetime
from usa_signal_bot.features.feature_store import read_feature_rows_jsonl, list_feature_outputs

@dataclass
class StrategyFeatureFrame:
    symbol: str
    timeframe: str
    rows: List[Dict[str, Any]]
    feature_names: List[str]
    source_path: Optional[str] = None

@dataclass
class StrategyInputBatch:
    frames: List[StrategyFeatureFrame]
    provider_name: str
    symbols: List[str]
    timeframes: List[str]
    created_at_utc: str
    universe_name: Optional[str] = None

@dataclass
class StrategyInputValidationResult:
    valid: bool
    symbol: Optional[str]
    timeframe: Optional[str]
    row_count: int
    missing_required_features: List[str]
    messages: List[str]

def validate_strategy_feature_frame(frame: StrategyFeatureFrame, required_features: List[str], min_rows: int = 1) -> StrategyInputValidationResult:
    messages = []
    valid = True

    if len(frame.rows) < min_rows:
        valid = False
        messages.append(f"Insufficient rows: expected >= {min_rows}, got {len(frame.rows)}")

    missing = [f for f in required_features if f not in frame.feature_names]
    if missing:
        valid = False
        messages.append(f"Missing required features: {missing}")

    return StrategyInputValidationResult(
        valid=valid,
        symbol=frame.symbol,
        timeframe=frame.timeframe,
        row_count=len(frame.rows),
        missing_required_features=missing,
        messages=messages
    )

def validate_strategy_input_batch(batch: StrategyInputBatch, required_features: List[str], min_rows: int = 1) -> List[StrategyInputValidationResult]:
    return [validate_strategy_feature_frame(f, required_features, min_rows) for f in batch.frames]

def load_strategy_feature_frames_from_feature_store(data_root: Path, symbols: List[str], timeframes: List[str], feature_names: Optional[List[str]] = None) -> StrategyInputBatch:
    frames = []

    # Very basic implementation for reading feature store
    # Since we can't easily query which JSONL has which symbol/timeframe efficiently without an index
    # We'll just read the latest ones and filter.
    outputs = list_feature_outputs(data_root)

    symbol_tf_data = {}

    for path in outputs:
        # Avoid loading massive files if we only need a few symbols
        # For this skeleton, we just load them. In a real system, we'd use partitioned data or an index.
        try:
            raw_rows = read_feature_rows_jsonl(path)
            for r in raw_rows:
                sym = r.get("symbol")
                tf = r.get("timeframe")

                if sym in symbols and tf in timeframes:
                    key = (sym, tf)
                    if key not in symbol_tf_data:
                        symbol_tf_data[key] = []

                    # Convert to simpler dict
                    flat_row = {"timestamp_utc": r.get("timestamp_utc")}
                    features = r.get("features", {})
                    flat_row.update(features)

                    symbol_tf_data[key].append(flat_row)
        except Exception:
            pass # Ignore read errors for now

    # Sort and create frames
    for (sym, tf), rows in symbol_tf_data.items():
        # Sort by timestamp
        rows.sort(key=lambda x: x.get("timestamp_utc", ""))

        # Deduplicate
        unique_rows = []
        seen = set()
        for r in rows:
            ts = r.get("timestamp_utc")
            if ts not in seen:
                seen.add(ts)
                unique_rows.append(r)

        if unique_rows:
            all_features = list(unique_rows[-1].keys())
            if "timestamp_utc" in all_features:
                all_features.remove("timestamp_utc")

            frames.append(StrategyFeatureFrame(
                symbol=sym,
                timeframe=tf,
                rows=unique_rows,
                feature_names=all_features
            ))

    return StrategyInputBatch(
        frames=frames,
        provider_name="feature_store",
        symbols=symbols,
        timeframes=timeframes,
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )

def filter_valid_strategy_frames(batch: StrategyInputBatch, validation_results: List[StrategyInputValidationResult]) -> StrategyInputBatch:
    valid_keys = {(r.symbol, r.timeframe) for r in validation_results if r.valid}

    valid_frames = [f for f in batch.frames if (f.symbol, f.timeframe) in valid_keys]

    return StrategyInputBatch(
        frames=valid_frames,
        provider_name=batch.provider_name,
        symbols=batch.symbols,
        timeframes=batch.timeframes,
        created_at_utc=batch.created_at_utc,
        universe_name=batch.universe_name
    )
