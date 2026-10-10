import json

import numpy as np
import pandas as pd
import pytest

from usa_signal_bot.evidence.data import synthetic_market
from usa_signal_bot.evidence.earnings_drift import earnings_drift_weights, filing_dates
from usa_signal_bot.evidence.macro_regime import lagged_to_trading_days, macro_regime_weights
from usa_signal_bot.evidence.report import run_evidence
from usa_signal_bot.evidence.sector_rotation import (
    BENCH_ETF, SECTOR_ETFS, load_etf_prices, sector_lowvol_weights, sector_momentum_weights,
)
from usa_signal_bot.evidence.universe import PointInTimeUniverse
from usa_signal_bot.evidence.walk_forward import WalkForwardConfig

CUT = 400


def _market(n_symbols=8, n_days=600):
    data = synthetic_market(seed=3, n_symbols=n_symbols, n_days=n_days)
    p = data.prices
    m = PointInTimeUniverse.from_frame(data.memberships).membership_matrix(p.index, p.columns)
    return data, p, m


def _macro(index, seed=0):
    rng = np.random.default_rng(seed)
    out = {}
    for sid, base in (("VIXCLS", 20.0), ("T10Y2Y", 0.5), ("BAA10Y", 2.0)):
        out[sid] = pd.Series(base + np.cumsum(rng.normal(0, 0.3, len(index))), index=index)
    return out


def _alter_future(s: pd.Series, cut_date) -> pd.Series:
    s = s.copy()
    s[s.index > cut_date] = s[s.index > cut_date] * 5 + 7
    return s


def test_macro_lag_is_at_least_one_day():
    idx = pd.bdate_range("2020-01-01", periods=10)
    s = pd.Series(np.arange(10.0), index=idx)
    lag = lagged_to_trading_days(s, idx)
    assert lag.iloc[3] == s.iloc[2]
    with pytest.raises(ValueError):
        lagged_to_trading_days(s, idx, lag=0)


def test_macro_weights_ignore_future_macro_and_prices():
    _data, p, m = _market()
    macro = _macro(p.index)
    cut_date = p.index[CUT]
    altered_px = p.copy()
    altered_px.iloc[CUT + 1:] = altered_px.iloc[CUT + 1:] * 3.0
    macro2 = {k: _alter_future(v, cut_date) for k, v in macro.items()}
    for sig, param in (("VIXCLS", 20.0), ("T10Y2Y", 0.0), ("BAA10Y", 126)):
        a = macro_regime_weights(p, m, macro, sig, param, 0.0).iloc[: CUT + 1]
        b = macro_regime_weights(altered_px, m, macro2, sig, param, 0.0).iloc[: CUT + 1]
        pd.testing.assert_frame_equal(a, b)


def test_macro_value_of_day_t_does_not_affect_weight_t():
    _data, p, m = _market()
    macro = _macro(p.index)
    t = p.index[CUT]
    changed = {k: v.copy() for k, v in macro.items()}
    changed["VIXCLS"].loc[t] = 999.0  # same-day shock must not be visible at t
    a = macro_regime_weights(p, m, macro, "VIXCLS", 25.0, 0.0).loc[t]
    b = macro_regime_weights(p, m, changed, "VIXCLS", 25.0, 0.0).loc[t]
    pd.testing.assert_series_equal(a, b)


def test_macro_risk_off_is_cash():
    _data, p, m = _market()
    macro = {"VIXCLS": pd.Series(80.0, index=p.index)}
    w = macro_regime_weights(p, m, macro, "VIXCLS", 25.0, 0.0).iloc[5:]
    assert float(w.to_numpy().sum()) == 0.0


def _etfs(n=700, seed=1):
    idx = pd.bdate_range("2018-01-01", periods=n)
    rng = np.random.default_rng(seed)
    cols = SECTOR_ETFS + [BENCH_ETF]
    px = pd.DataFrame(100 * np.cumprod(1 + rng.normal(0.0003, 0.01, (n, len(cols))), axis=0), index=idx, columns=cols)
    px.loc[:idx[min(200, n - 1)], "XLC"] = np.nan  # late-listed ETF
    return px


def test_sector_rotation_no_lookahead_and_excludes_spy():
    px = _etfs()
    members = px.notna()
    altered = px.copy()
    altered.iloc[CUT + 1:] = altered.iloc[CUT + 1:] * 2.5
    for fn, kw in ((sector_momentum_weights, {"lookback": 63, "top_n": 3}), (sector_lowvol_weights, {"window": 63, "top_n": 4})):
        a = fn(px, members, **kw)
        b = fn(altered, members, **kw)
        pd.testing.assert_frame_equal(a.iloc[: CUT + 1], b.iloc[: CUT + 1])
        assert (a[BENCH_ETF] == 0).all()
        assert (a["XLC"].iloc[:200] == 0).all()
        assert a.sum(axis=1).max() <= 1.0 + 1e-9


def test_load_etf_prices_roundtrip(tmp_path):
    px = _etfs(50)
    for c in px.columns:
        pd.DataFrame({"Date": px.index, "Adj Close": px[c].to_numpy()}).dropna().to_csv(tmp_path / f"{c}.csv", index=False)
    loaded = load_etf_prices(tmp_path)
    assert set(loaded.columns) == set(px.columns)
    np.testing.assert_allclose(loaded["SPY"].to_numpy(), px["SPY"].to_numpy())


def _facts(dates, ni=None):
    rows = [{"filed": d, "end": d, "val": 1e9 + i, "form": "10-Q"} for i, d in enumerate(dates)]
    facts = {"facts": {"us-gaap": {"StockholdersEquity": {"units": {"USD": rows}}}, "dei": {}}}
    if ni:
        facts["facts"]["us-gaap"]["NetIncomeLoss"] = {"units": {"USD": [
            {"filed": d, "end": d, "val": v, "form": "10-K"} for d, v in ni]}}
    return facts


def test_earnings_drift_entry_after_filing_and_no_lookahead():
    _data, p, m = _market()
    sym = p.columns[0]
    fdate = p.index[300]
    facts = {sym: _facts([str(fdate.date())])}
    assert list(filing_dates(facts[sym])) == [fdate]
    w = earnings_drift_weights(p, m, facts, mode="reaction", hold=20, tilt=1.0)
    base = earnings_drift_weights(p, m, {}, mode="reaction", hold=20, tilt=1.0)
    # nothing changes up to and including the filing day (signal complete only at the next close)
    pd.testing.assert_frame_equal(w.iloc[:301], base.iloc[:301])
    # future prices must not alter earlier weights
    altered = p.copy()
    altered.iloc[CUT + 1:] = altered.iloc[CUT + 1:] * 3.0
    w2 = earnings_drift_weights(altered, m, facts, mode="reaction", hold=20, tilt=1.0)
    pd.testing.assert_frame_equal(w.iloc[: CUT + 1], w2.iloc[: CUT + 1])


def test_earnings_drift_ni_growth_signal_timing():
    _data, p, m = _market()
    sym = p.columns[1]
    d1, d2 = p.index[100], p.index[300]
    facts = {sym: _facts([str(d1.date()), str(d2.date())], ni=[(str(d1.date()), 1e9), (str(d2.date()), 2e9)])}
    base = earnings_drift_weights(p, m, {}, mode="ni_growth", hold=30, tilt=1.0)
    w = earnings_drift_weights(p, m, facts, mode="ni_growth", hold=30, tilt=1.0)
    pd.testing.assert_frame_equal(w.iloc[:301], base.iloc[:301])
    assert w[sym].iloc[302] > base[sym].iloc[302]  # growth -> overweight from the day after the filing day's close
    assert w[sym].iloc[340] == pytest.approx(base[sym].iloc[340])  # signal expired after `hold`


def test_run_evidence_with_new_families_is_backward_compatible_and_runs():
    data = synthetic_market(seed=5, n_symbols=10, n_days=1000)
    cfg = WalkForwardConfig(train_days=252, test_days=63, step_days=63)
    base = run_evidence(data, cfg=cfg, families=["SMA trend"])
    assert [r.name for r in base.results] == ["SMA trend"]
    idx = data.prices.index
    facts = {data.prices.columns[0]: _facts([str(idx[400].date()), str(idx[600].date())])}
    rep = run_evidence(data, cfg=cfg, families=["Makro rejim (FRED)", "Sektör momentum (ETF)", "Bildirim sonrası sürüklenme"],
                       macro=_macro(idx), etf_prices=_etfs(1000).set_axis(idx), fundamentals=facts)
    names = [r.name for r in rep.results]
    assert names == ["Makro rejim (FRED)", "Bildirim sonrası sürüklenme", "Sektör momentum (ETF)"]
    assert all(r.oos_returns is not None and len(r.oos_returns) > 0 for r in rep.results)
    assert "SPY" in rep.to_markdown()
