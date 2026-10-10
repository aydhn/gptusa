import numpy as np
import pandas as pd

from usa_signal_bot.evidence.costs import CostModel
from usa_signal_bot.evidence.data import synthetic_market
from usa_signal_bot.evidence.factors_rel import (
    beta_tilt_weights, low_turnover_mix_weights, regime_beta_weights, vol_target_beta_weights,
)
from usa_signal_bot.evidence.report import _after_tax_cagr, run_evidence
from usa_signal_bot.evidence.universe import PointInTimeUniverse


def _setup():
    d = synthetic_market(seed=3)
    members = PointInTimeUniverse.from_frame(d.memberships).membership_matrix(d.prices.index, d.prices.columns)
    return d.prices, members


def test_rel_weights_long_only_no_leverage():
    prices, members = _setup()
    for fn in (beta_tilt_weights, low_turnover_mix_weights, vol_target_beta_weights, regime_beta_weights):
        w = fn(prices, members)
        assert (w >= -1e-12).all().all()
        assert (w.sum(axis=1) <= 1 + 1e-9).all()


def test_beta_tilt_zero_equals_benchmark_weights():
    prices, members = _setup()
    w = beta_tilt_weights(prices, members, tilt=0.0, rebalance=1)
    bench = (members & prices.notna()).astype(float)
    bench = bench.div(bench.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    assert np.allclose(w.to_numpy(), bench.to_numpy(), atol=1e-9)


def test_after_tax_cagr_monotone():
    r = pd.Series(0.0005, index=pd.bdate_range("2020-01-01", periods=756))
    assert _after_tax_cagr(r, 0.25) < _after_tax_cagr(r, 0.15) < _after_tax_cagr(r, 0.0)


def test_report_contains_sensitivity_and_conclusion():
    rep = run_evidence(synthetic_market(seed=3), CostModel(), families=["Rejim beta", "Vol hedefli beta"], cash_rate=0.02, inflation=0.025)
    md = rep.to_markdown()
    assert "Vergi ve maliyet duyarlılığı" in md and "**Sonuç:**" in md
