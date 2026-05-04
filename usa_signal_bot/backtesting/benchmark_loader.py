import datetime
from pathlib import Path
from typing import Optional

from usa_signal_bot.core.enums import BenchmarkType
from usa_signal_bot.core.exceptions import BenchmarkLoaderError
from usa_signal_bot.backtesting.benchmark_models import BenchmarkSpec, BenchmarkSet
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.data.cache import read_cached_bars_for_symbols_timeframe

def default_benchmark_specs() -> list[BenchmarkSpec]:
    return [
        BenchmarkSpec(benchmark_id="SPY_ETF", name="SPDR S&P 500 ETF", symbol="SPY", benchmark_type=BenchmarkType.ETF),
        BenchmarkSpec(benchmark_id="QQQ_ETF", name="Invesco QQQ Trust", symbol="QQQ", benchmark_type=BenchmarkType.ETF),
        BenchmarkSpec(benchmark_id="IWM_ETF", name="iShares Russell 2000 ETF", symbol="IWM", benchmark_type=BenchmarkType.ETF),
        BenchmarkSpec(benchmark_id="CASH_BASE", name="Cash Baseline", symbol="CASH", benchmark_type=BenchmarkType.CASH)
    ]

def default_benchmark_set() -> BenchmarkSet:
    return BenchmarkSet(
        name="default",
        benchmarks=default_benchmark_specs(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        description="Default benchmark set with SPY, QQQ, IWM, and CASH"
    )

def core_equity_benchmark_set() -> BenchmarkSet:
    specs = [
        BenchmarkSpec(benchmark_id="SPY_ETF", name="SPDR S&P 500 ETF", symbol="SPY", benchmark_type=BenchmarkType.ETF),
        BenchmarkSpec(benchmark_id="QQQ_ETF", name="Invesco QQQ Trust", symbol="QQQ", benchmark_type=BenchmarkType.ETF),
        BenchmarkSpec(benchmark_id="IWM_ETF", name="iShares Russell 2000 ETF", symbol="IWM", benchmark_type=BenchmarkType.ETF)
    ]
    return BenchmarkSet(
        name="core_equity",
        benchmarks=specs,
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        description="Core US Equity ETFs (SPY, QQQ, IWM)"
    )

def tech_growth_benchmark_set() -> BenchmarkSet:
    specs = [
        BenchmarkSpec(benchmark_id="QQQ_ETF", name="Invesco QQQ Trust", symbol="QQQ", benchmark_type=BenchmarkType.ETF),
        BenchmarkSpec(benchmark_id="SPY_ETF", name="SPDR S&P 500 ETF", symbol="SPY", benchmark_type=BenchmarkType.ETF),
        BenchmarkSpec(benchmark_id="CASH_BASE", name="Cash Baseline", symbol="CASH", benchmark_type=BenchmarkType.CASH)
    ]
    return BenchmarkSet(
        name="tech_growth",
        benchmarks=specs,
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        description="Tech/Growth Focus (QQQ vs SPY vs CASH)"
    )

def broad_market_benchmark_set() -> BenchmarkSet:
    specs = [
        BenchmarkSpec(benchmark_id="SPY_ETF", name="SPDR S&P 500 ETF", symbol="SPY", benchmark_type=BenchmarkType.ETF),
        BenchmarkSpec(benchmark_id="VTI_ETF", name="Vanguard Total Stock Market ETF", symbol="VTI", benchmark_type=BenchmarkType.ETF),
        BenchmarkSpec(benchmark_id="IWM_ETF", name="iShares Russell 2000 ETF", symbol="IWM", benchmark_type=BenchmarkType.ETF),
        BenchmarkSpec(benchmark_id="DIA_ETF", name="SPDR Dow Jones Industrial Average ETF", symbol="DIA", benchmark_type=BenchmarkType.ETF),
        BenchmarkSpec(benchmark_id="CASH_BASE", name="Cash Baseline", symbol="CASH", benchmark_type=BenchmarkType.CASH)
    ]
    return BenchmarkSet(
        name="broad_market",
        benchmarks=specs,
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        description="Broad Market Coverage"
    )

def list_benchmark_sets() -> list[BenchmarkSet]:
    return [
        default_benchmark_set(),
        core_equity_benchmark_set(),
        tech_growth_benchmark_set(),
        broad_market_benchmark_set()
    ]

def get_benchmark_set(name: str) -> BenchmarkSet:
    for bs in list_benchmark_sets():
        if bs.name == name:
            return bs
    raise BenchmarkLoaderError(f"Unknown benchmark set name: {name}")

def load_benchmark_market_data_from_cache(
    data_root: Path,
    benchmark_set: BenchmarkSet,
    timeframe: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    provider_name: str = "yfinance"
) -> dict[str, list[OHLCVBar]]:
    data = {}

    for spec in benchmark_set.benchmarks:
        if not spec.enabled:
            continue

        if spec.benchmark_type == BenchmarkType.CASH:
            continue

        try:
            bars = read_cached_bars_for_symbols_timeframe(data_root=data_root, symbols=[spec.symbol], timeframe=timeframe, provider_name=provider_name)

            if start_date or end_date:
                filtered_bars = []
                for bar in bars:
                    bar_date = bar.timestamp_utc[:10]
                    if start_date and bar_date < start_date:
                        continue
                    if end_date and bar_date > end_date:
                        continue
                    filtered_bars.append(bar)
                data[spec.symbol] = filtered_bars
            else:
                data[spec.symbol] = bars
        except Exception:
            pass

    return data

def validate_benchmark_cache_coverage(
    data: dict[str, list[OHLCVBar]],
    benchmark_set: BenchmarkSet
) -> list[str]:
    messages = []

    for spec in benchmark_set.benchmarks:
        if not spec.enabled or spec.benchmark_type == BenchmarkType.CASH:
            continue

        if spec.symbol not in data:
            messages.append(f"Missing cache data for benchmark {spec.symbol}. Please run data pipeline or active-universe-download to fetch it.")
        elif not data[spec.symbol]:
            messages.append(f"Cache data for benchmark {spec.symbol} is empty.")

    return messages
