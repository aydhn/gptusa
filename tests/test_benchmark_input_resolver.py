import pytest
import pandas as pd
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_input_resolver import (
    build_benchmark_input_references,
    validate_strategy_equity_curve_frame
)

def test_validate_strategy_equity_curve_frame():
    df = pd.DataFrame({"timestamp": [], "simulated_equity": []})
    errors = validate_strategy_equity_curve_frame(df)
    assert len(errors) == 0

    df_err = pd.DataFrame({"timestamp": []})
    errors = validate_strategy_equity_curve_frame(df_err)
    assert len(errors) == 1
    assert "simulated_equity" in errors[0]

def test_build_benchmark_input_references():
    dataframes = {
        "equity": pd.DataFrame({"timestamp": [1], "simulated_equity": [100]})
    }
    refs = build_benchmark_input_references({"equity": {}}, dataframes)
    assert len(refs) == 1
    assert refs[0].row_count == 1
