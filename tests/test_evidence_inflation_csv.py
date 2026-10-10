import pandas as pd

from usa_signal_bot.evidence.rates import average_inflation


def test_average_inflation_geometric():
    lvl = pd.Series([100.0, 121.0], index=pd.to_datetime(["2020-01-01", "2022-01-01"]))
    assert abs(average_inflation(lvl, "2020-01-01", "2022-01-01") - 0.10) < 2e-3
