import pytest
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_universe_contract import (
    build_benchmark_universe_contract
)

def test_build_universe_contract():
    contract = build_benchmark_universe_contract(["AAPL"])
    assert contract.contract_valid is True
    assert contract.external_fetch_allowed is False
    assert contract.survivorship_bias_notice != ""
