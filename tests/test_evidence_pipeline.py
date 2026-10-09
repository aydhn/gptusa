import numpy as np
import pandas as pd

from usa_signal_bot.evidence.corporate_actions import validate_adjusted_prices
from usa_signal_bot.evidence.costs import CostModel
from usa_signal_bot.evidence.data import synthetic_market
from usa_signal_bot.evidence.metrics import sharpe_ci, summarize
from usa_signal_bot.evidence.report import run_evidence
from usa_signal_bot.evidence.strategies import momentum_weights, sma_trend_weights
from usa_signal_bot.evidence.universe import Membership, PointInTimeUniverse
from usa_signal_bot.evidence.walk_forward import WalkForwardConfig, backtest_weights


def test_point_in_time_universe_has_no_lookahead():
    u = PointInTimeUniverse([Membership("A", pd.Timestamp("2020-01-10"), pd.Timestamp("2020-02-10"))])
    assert u.members(pd.Timestamp("2020-01-09")) == []
    assert u.members(pd.Timestamp("2020-01-10")) == ["A"]
    assert u.members(pd.Timestamp("2020-02-11")) == []


def test_unadjusted_split_is_flagged():
    idx = pd.bdate_range("2020-01-01", periods=10)
    px = pd.DataFrame({"X": [100.0] * 5 + [50.0] * 5}, index=idx)
    splits = pd.DataFrame({"symbol": ["X"], "date": [idx[5]], "ratio": [2.0]})
    kinds = {i.kind for i in validate_adjusted_prices(px, splits)}
    assert kinds == {"UNADJUSTED_SPLIT"}
    assert validate_adjusted_prices(px.where(px > 0, 1.0).assign(X=100.0), splits) == []


def test_strategy_weights_do_not_use_future_prices():
    data = synthetic_market(seed=3, n_symbols=8, n_days=600)
    prices = data.prices
    members = PointInTimeUniverse.from_frame(data.memberships).membership_matrix(prices.index, prices.columns)
    cut = 400
    altered = prices.copy()
    altered.iloc[cut + 1 :] = altered.iloc[cut + 1 :] * 3.0  # change only the future
    for fn, kw in ((sma_trend_weights, {"window": 50}), (momentum_weights, {"lookback": 126})):
        a = fn(prices, members, **kw).iloc[: cut + 1]
        b = fn(altered, members, **kw).iloc[: cut + 1]
        pd.testing.assert_frame_equal(a, b)


def test_costs_reduce_returns():
    idx = pd.bdate_range("2020-01-01", periods=6)
    rets = pd.DataFrame({"A": [0.01] * 6}, index=idx)
    w = pd.DataFrame({"A": [1.0, 0.0, 1.0, 0.0, 1.0, 0.0]}, index=idx)
    free, _ = backtest_weights(w, rets, CostModel(0.0, 0.0))
    paid, turn = backtest_weights(w, rets, CostModel(1.0, 5.0))
    assert paid.sum() < free.sum()
    assert turn.sum() > 0


def test_metrics_and_bootstrap_are_deterministic():
    rng = np.random.default_rng(1)
    r = pd.Series(rng.normal(0.0005, 0.01, 800))
    assert summarize(r).n_days == 800
    assert sharpe_ci(r, seed=5) == sharpe_ci(r, seed=5)


def test_report_is_deterministic_and_labels_synthetic_data():
    cfg = WalkForwardConfig(train_days=252, test_days=63, step_days=63)
    a = run_evidence(synthetic_market(seed=11, n_days=1200), cfg=cfg).to_markdown()
    b = run_evidence(synthetic_market(seed=11, n_days=1200), cfg=cfg).to_markdown()
    assert a == b
    assert "SENTETİK VERİ" in a
    assert "yatırım tavsiyesi değildir" in a
