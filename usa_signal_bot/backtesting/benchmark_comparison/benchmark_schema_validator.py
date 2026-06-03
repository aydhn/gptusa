from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import *
def validate_benchmark_column_names(cols: list) -> list:
    forbidden = {"broker_order"}
    return [c for c in cols if c in forbidden]
