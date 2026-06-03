from typing import Any, Dict, List, Optional
import datetime
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import (
    PassiveBenchmarkConfig, BenchmarkKind, create_passive_benchmark_config_id
)
def build_default_passive_benchmark_config(initial_cash: float = 100000.0) -> PassiveBenchmarkConfig:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return PassiveBenchmarkConfig(
        config_id=create_passive_benchmark_config_id(),
        created_at_utc=now_utc,
        benchmark_kinds=[BenchmarkKind.CASH_BASELINE, BenchmarkKind.BUY_AND_HOLD_SINGLE_ASSET, BenchmarkKind.EQUAL_WEIGHT_METADATA, BenchmarkKind.MARKET_INDEX_REFERENCE],
        initial_cash=initial_cash,
        currency="USD", cash_rate_assumption=0.0, rebalance_enabled=False,
        equal_weight_metadata_only=True, market_reference_label="LOCAL_INDEX_REFERENCE",
        external_benchmark_fetch_enabled=False, config_valid=True
    )
def passive_benchmark_config_to_text(c: PassiveBenchmarkConfig, limit=300) -> str: return "config"
