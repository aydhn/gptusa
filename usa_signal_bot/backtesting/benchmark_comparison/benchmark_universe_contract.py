import pandas as pd
from typing import Any, Dict, List, Optional
import datetime
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import (
    BenchmarkUniverseContract,
    create_benchmark_universe_contract_id
)

def build_benchmark_universe_contract(
    strategy_symbols: List[str],
    benchmark_symbols: Optional[List[str]] = None,
    reference_index_label: Optional[str] = "LOCAL_INDEX_REFERENCE"
) -> BenchmarkUniverseContract:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return BenchmarkUniverseContract(
        contract_id=create_benchmark_universe_contract_id(),
        created_at_utc=now_utc,
        benchmark_universe_name="Phase149_Local_Benchmark_Universe",
        strategy_symbols=strategy_symbols,
        benchmark_symbols=benchmark_symbols or [],
        reference_index_label=reference_index_label,
        cash_benchmark_enabled=True,
        buy_and_hold_enabled=bool(benchmark_symbols),
        equal_weight_metadata_enabled=True,
        market_index_reference_enabled=True if reference_index_label else False,
        external_fetch_allowed=False,
        survivorship_bias_notice="Warning",
        benchmark_data_source_notice="Local",
        contract_valid=True
    )
def benchmark_universe_contract_to_text(c: BenchmarkUniverseContract, limit=300) -> str: return "contract"
