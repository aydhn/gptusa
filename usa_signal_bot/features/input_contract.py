from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path
from datetime import datetime, timezone

from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.data.cache import read_cached_bars_for_symbols_timeframe

@dataclass
class FeatureInput:
    symbol: str
    timeframe: str
    bars: List[OHLCVBar]
    source: str = "cache"
    readiness_status: Optional[str] = None

@dataclass
class FeatureBatchInput:
    inputs: List[FeatureInput]
    created_at_utc: str
    provider_name: str
    universe_name: Optional[str] = None
    eligible_symbols: List[str] = field(default_factory=list)

@dataclass
class FeatureInputValidationResult:
    valid: bool
    symbol: Optional[str]
    timeframe: Optional[str]
    bar_count: int
    messages: List[str]

def validate_feature_input(input_: FeatureInput, min_bars: int = 2) -> FeatureInputValidationResult:
    messages = []
    valid = True

    if not input_.symbol:
        messages.append("Symbol cannot be empty.")
        valid = False

    if not input_.timeframe:
        messages.append("Timeframe cannot be empty.")
        valid = False

    bar_count = len(input_.bars) if input_.bars else 0
    if bar_count == 0:
        messages.append("Bars list is empty.")
        valid = False
    elif bar_count < min_bars:
        messages.append(f"Not enough bars. Expected >= {min_bars}, got {bar_count}.")
        valid = False

    if input_.eligible_symbols is not None if hasattr(input_, "eligible_symbols") else False:
        pass

    return FeatureInputValidationResult(
        valid=valid,
        symbol=input_.symbol,
        timeframe=input_.timeframe,
        bar_count=bar_count,
        messages=messages
    )

def validate_feature_batch_input(batch: FeatureBatchInput, min_bars: int = 2) -> List[FeatureInputValidationResult]:
    results = []
    for input_ in batch.inputs:
        res = validate_feature_input(input_, min_bars)
        if batch.eligible_symbols and input_.symbol not in batch.eligible_symbols:
            res.valid = False
            res.messages.append(f"Symbol {input_.symbol} is not in eligible_symbols list.")
        results.append(res)
    return results

def build_feature_inputs_from_cache(data_root: Path, symbols: List[str], timeframes: List[str], provider_name: str = "yfinance") -> FeatureBatchInput:
    inputs = []
    for tf in timeframes:
        all_bars = read_cached_bars_for_symbols_timeframe(data_root, symbols, tf, provider_name=provider_name)
        bars_by_symbol = {}
        for b in all_bars:
            bars_by_symbol.setdefault(b.symbol, []).append(b)

        for sym, bars in bars_by_symbol.items():
            inputs.append(FeatureInput(
                symbol=sym,
                timeframe=tf,
                bars=bars,
                source="cache"
            ))

    return FeatureBatchInput(
        inputs=inputs,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        provider_name=provider_name
    )

def filter_valid_feature_inputs(batch: FeatureBatchInput, validation_results: List[FeatureInputValidationResult]) -> FeatureBatchInput:
    valid_pairs = {(res.symbol, res.timeframe) for res in validation_results if res.valid}

    valid_inputs = [
        inp for inp in batch.inputs
        if (inp.symbol, inp.timeframe) in valid_pairs
    ]

    return FeatureBatchInput(
        inputs=valid_inputs,
        created_at_utc=batch.created_at_utc,
        provider_name=batch.provider_name,
        universe_name=batch.universe_name,
        eligible_symbols=batch.eligible_symbols
    )
