import pandas as pd

from usa_signal_bot.evidence.fundamentals import fundamental_frames, split_adjust_shares


def _facts(equity, shares, filed):
    return {
        "facts": {
            "us-gaap": {
                "StockholdersEquity": {"units": {"USD": [{"filed": filed, "end": filed, "val": equity, "form": "10-K"}]}}
            },
            "dei": {
                "EntityCommonStockSharesOutstanding": {
                    "units": {"shares": [{"filed": filed, "end": filed, "val": shares, "form": "10-K"}]}
                }
            },
        }
    }


def test_split_adjust_only_splits_after_filing():
    s = pd.Series([100.0, 100.0], index=pd.to_datetime(["2020-01-10", "2020-09-01"]))
    sp = pd.DataFrame({"symbol": ["A"], "date": [pd.Timestamp("2020-06-01")], "ratio": [4.0]})
    out = split_adjust_shares(s, sp, "A")
    assert list(out) == [400.0, 100.0]
    assert list(split_adjust_shares(s, sp, "B")) == [100.0, 100.0]


def test_book_to_price_continuous_across_split():
    idx = pd.bdate_range("2020-01-13", "2020-12-31")
    # actual price 100 before the 4:1 split on 2020-06-01, 25 after; yfinance-adjusted price is flat 25
    prices = pd.DataFrame({"A": 25.0}, index=idx)
    splits = pd.DataFrame({"symbol": ["A"], "date": [pd.Timestamp("2020-06-01")], "ratio": [4.0]})
    f = _facts(equity=1000.0, shares=100.0, filed="2020-01-10")
    fixed = fundamental_frames({"A": f}, prices, splits)["book_to_price"]["A"]
    assert fixed.nunique() == 1 and abs(fixed.iloc[0] - 1000.0 / (400.0 * 25.0)) < 1e-12
