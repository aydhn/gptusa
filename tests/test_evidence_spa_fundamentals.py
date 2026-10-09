import numpy as np
import pandas as pd
import pytest

from usa_signal_bot.evidence.factors_fundamental import value_quality_weights
from usa_signal_bot.evidence.fundamentals import align_to_dates, fundamental_frames, pit_series
from usa_signal_bot.evidence.hypothesis_log import HypothesisLog
from usa_signal_bot.evidence.spa import spa_test


def test_spa_noise_not_significant_even_with_many_models():
    rng = np.random.default_rng(0)
    d = rng.normal(0, 0.01, (1000, 50))
    r = spa_test(d, n_boot=400, seed=1)
    assert r.p_value_spa > 0.1 and r.p_value_rc > 0.1


def test_spa_detects_true_winner_and_is_not_inflated_by_junk_models():
    rng = np.random.default_rng(1)
    d = rng.normal(0, 0.01, (1500, 30))
    d[:, 7] += 0.002
    r = spa_test(d, n_boot=400, seed=2)
    assert r.best_index == 7 and r.p_value_spa < 0.05
    # adding clearly bad models must not make the test less powerful under SPA (RC is known to be hurt by them)
    bad = rng.normal(-0.01, 0.01, (1500, 40))
    r2 = spa_test(np.hstack([d, bad]), n_boot=400, seed=2)
    assert r2.p_value_spa <= r2.p_value_rc + 1e-9
    assert r2.p_value_spa < 0.05


def test_spa_validation():
    with pytest.raises(ValueError):
        spa_test(np.zeros(10))


def test_hypothesis_log_cumulative_trials(tmp_path):
    log = HypothesisLog(tmp_path / "h.jsonl", clock=lambda: "t0")
    log.append("r1", "SMA", {"window": 50}, 500, 0.05, "X")
    log.append("r1", "SMA", {"window": 100}, 500, 0.07, "X")
    log.append("r2", "SMA", {"window": 50}, 500, 0.06, "X")  # same candidate re-run: not a new trial
    log.append("r2", "MOM", {"lb": 126}, 500, 0.02, "Y")
    assert log.n_trials() == 3 and log.n_trials("X") == 2
    assert log.sharpe_variance("X") > 0
    assert len(HypothesisLog(tmp_path / "h.jsonl", lambda: "t").entries()) == 4


def _facts(eq=100.0, ni=20.0):
    def row(end, val, filed, form="10-K"):
        return {"end": end, "val": val, "filed": filed, "form": form}

    return {"facts": {"us-gaap": {
        "StockholdersEquity": {"units": {"USD": [row("2019-12-31", eq, "2020-02-15"), row("2019-12-31", 90.0, "2020-08-01", "10-Q")]}},
        "NetIncomeLoss": {"units": {"USD": [row("2019-12-31", ni, "2020-02-15")]}},
    }, }, "dei": {}}


def test_pit_series_uses_filing_date_and_original_value():
    f = _facts()
    f["facts"]["us-gaap"]["StockholdersEquity"]["units"]["USD"].append(
        {"end": "2019-12-31", "val": 80.0, "filed": "2021-03-01", "form": "10-K"})  # later restatement of same period
    s = pit_series(f, ("StockholdersEquity",))
    assert s.loc[pd.Timestamp("2020-02-15")] == 100.0  # first filed wins
    assert pd.Timestamp("2021-03-01") not in s.index
    idx = pd.date_range("2020-01-01", periods=60, freq="B")
    a = align_to_dates(s, idx)
    assert a.loc[:"2020-02-14"].isna().all() and a.loc["2020-02-17":].eq(100.0).all()  # nothing before filing


def test_fundamental_frames_and_weights_no_lookahead():
    f = _facts()
    f["facts"]["dei"] = {"EntityCommonStockSharesOutstanding": {"units": {"shares": [
        {"end": "2020-01-31", "val": 10.0, "filed": "2020-02-15", "form": "10-K"}]}}}
    idx = pd.date_range("2020-01-01", periods=80, freq="B")
    prices = pd.DataFrame({"A": 5.0, "B": 5.0}, index=idx)
    g = _facts(eq=50.0, ni=1.0)
    g["facts"]["dei"] = f["facts"]["dei"]
    fr = fundamental_frames({"A": f, "B": g}, prices)
    assert fr["book_to_price"]["A"].loc[:"2020-02-14"].isna().all()
    assert fr["book_to_price"]["A"].iloc[-1] == pytest.approx(100.0 / (10 * 5.0))
    assert fr["roe"]["A"].iloc[-1] == pytest.approx(0.2)
    w = value_quality_weights(prices, pd.DataFrame(True, index=idx, columns=prices.columns), fr["book_to_price"], fr["roe"], top_frac=0.5)
    assert (w.loc[:"2020-02-14"].sum(axis=1) == 0).all()  # no positions before any fundamental is public
    assert w["A"].iloc[-1] == 1.0
