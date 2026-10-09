import numpy as np
import pandas as pd
import pytest

from usa_signal_bot.evidence.data import synthetic_market
from usa_signal_bot.evidence.universe import PointInTimeUniverse
from usa_signal_bot.ml_loop import ModelRegistry, PromotionThresholds, PurgedKFold, assert_no_leakage, check_leakage, run_training
from usa_signal_bot.ml_loop.registry import APPROVED, ELIGIBLE, REJECTED
from usa_signal_bot.ml_loop.training import build_panel


def test_purged_kfold_purges_and_embargoes():
    cv = PurgedKFold(n_splits=4, horizon=5, embargo=3)
    folds = list(cv.split(200))
    assert len(folds) == 4
    for train, test in folds:
        assert set(train).isdisjoint(test)
        assert_no_leakage(train, test, 5, 3)
        t0, t1 = test.min(), test.max()
        assert not ((train >= t0 - 5) & (train <= t1 + 3)).any()


def test_assert_no_leakage_detects_overlap():
    with pytest.raises(AssertionError):
        assert_no_leakage(np.array([0, 1, 2, 3]), np.array([4, 5]), horizon=3, embargo=0)


def test_leakage_guard_flags_forward_looking_feature():
    rng = np.random.default_rng(0)
    idx = pd.bdate_range("2020-01-01", periods=400)
    label = pd.Series(rng.normal(size=400), index=idx)
    clean = pd.DataFrame({"noise": rng.normal(size=400)}, index=idx)
    assert check_leakage(clean, label, horizon=5).clean
    leaky = clean.assign(peek=label.shift(1))  # value of tomorrow's label appears at t (future leak)
    leaky["peek"] = label.shift(1)
    rep = check_leakage(leaky.fillna(0.0), label, horizon=5)
    assert not rep.clean and any("forward-looking" in i for i in rep.issues)
    assert not check_leakage(clean.assign(copy=label), label, horizon=5).clean


def test_panel_features_do_not_change_when_future_changes():
    data = synthetic_market(seed=2, n_symbols=8, n_days=400)
    members = PointInTimeUniverse.from_frame(data.memberships).membership_matrix(data.prices.index, data.prices.columns)
    x1, _ = build_panel(data.prices, members, horizon=5)
    altered = data.prices.copy()
    altered.iloc[300:] = altered.iloc[300:] * 2.0
    x2, _ = build_panel(altered, members, horizon=5)
    cutoff = data.prices.index[290]
    a = x1[x1.index.get_level_values("date") <= cutoff]
    b = x2[x2.index.get_level_values("date") <= cutoff]
    pd.testing.assert_frame_equal(a, b)


def test_training_is_deterministic_and_reports_honest_metrics():
    data = synthetic_market(seed=4, n_symbols=14, n_days=900)
    members = PointInTimeUniverse.from_frame(data.memberships).membership_matrix(data.prices.index, data.prices.columns)
    r1 = run_training(data.prices, members)
    r2 = run_training(data.prices, members)
    assert r1.metrics == r2.metrics and r1.fingerprint == r2.fingerprint
    assert r1.metrics["n_folds"] >= 3 and r1.leakage.clean
    assert abs(r1.metrics["oos_ic_mean"]) < 0.2  # no alpha is planted, so no big IC


def _reg(tmp_path):
    return ModelRegistry(tmp_path, clock=lambda: "2026-01-01T00:00:00Z")


def test_promotion_gate_and_human_approval(tmp_path):
    reg = _reg(tmp_path)
    good = {"oos_ic_mean": 0.05, "baseline_ic_mean": 0.0, "positive_fold_fraction": 0.8}
    reg.register("m_good", {"a": 1}, good, "fp", leakage_clean=True)
    rec = reg.evaluate_promotion("m_good", PromotionThresholds())
    assert rec.status == ELIGIBLE and rec.activation_allowed is False
    with pytest.raises(ValueError):
        reg.approve("m_good", "", "ok")
    approved = reg.approve("m_good", "reviewer", "reviewed OOS report")
    assert approved.status == APPROVED and approved.approved_by == "reviewer"
    assert approved.activation_allowed is False  # approval never switches anything on


def test_gate_rejects_weak_or_leaky_models_and_blocks_approval(tmp_path):
    reg = _reg(tmp_path)
    reg.register("weak", {}, {"oos_ic_mean": 0.001, "baseline_ic_mean": 0.0, "positive_fold_fraction": 0.4}, "fp", True)
    reg.register("leaky", {}, {"oos_ic_mean": 0.2, "baseline_ic_mean": 0.0, "positive_fold_fraction": 1.0}, "fp", False)
    assert reg.evaluate_promotion("weak", PromotionThresholds()).status == REJECTED
    leaky = reg.evaluate_promotion("leaky", PromotionThresholds())
    assert leaky.status == REJECTED and "leakage check not clean" in leaky.gate_reasons
    with pytest.raises(PermissionError):
        reg.approve("leaky", "someone", "try anyway")
    with pytest.raises(FileExistsError):
        reg.register("weak", {}, {}, "fp", True)
