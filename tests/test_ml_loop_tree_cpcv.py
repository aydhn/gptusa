import numpy as np
import pandas as pd
import pytest

from usa_signal_bot.evidence.data import synthetic_market
from usa_signal_bot.evidence.universe import PointInTimeUniverse
from usa_signal_bot.ml_loop.drift import DriftResult, feature_drift, psi, severity_from_psi
from usa_signal_bot.ml_loop.registry import CpcvThresholds, ModelRegistry
from usa_signal_bot.ml_loop.retrain_trigger import evaluate_retrain, register_retrain_candidate
from usa_signal_bot.ml_loop.tree_cpcv import CPCVModelResult, judge, run_tree_cpcv


def test_psi_detects_shift_and_ignores_noise():
    rng = np.random.default_rng(0)
    a = rng.normal(0, 1, 5000)
    assert psi(a, rng.normal(0, 1, 5000)) < 0.05
    assert severity_from_psi(psi(a, rng.normal(1.5, 1, 5000))) == "HIGH"


def test_drift_feeds_retrain_trigger_and_registry(tmp_path):
    rng = np.random.default_rng(1)
    ref = pd.DataFrame({"f": rng.normal(0, 1, 2000)})
    cur = pd.DataFrame({"f": rng.normal(2, 1, 2000)})
    req = evaluate_retrain(feature_drift(ref, cur))
    assert req.triggered and req.activation_allowed is False
    rec = register_retrain_candidate(ModelRegistry(tmp_path, lambda: "t"), "m1", req, "fp")
    assert rec.activation_allowed is False


def test_retrain_trigger_reads_ml_research_style_attribute():
    class R:  # mimics ml_research drift results (drift_severity field)
        drift_severity = "HIGH"
        metric_name = "x"

    assert evaluate_retrain([R()]).triggered


def test_judge_rejects_without_dsr_and_spa():
    r = CPCVModelResult("hgb", False, 3, [0.1] * 3, [1.0] * 3, [0.2] * 3, 0.1, 1.0, dsr_excess=0.5, spa_p=0.4, leakage_clean=True, n_trials=10)
    assert not judge(r).eligible and len(r.reasons) == 2
    r2 = CPCVModelResult("hgb", False, 3, [0.1] * 3, [1.0] * 3, [0.2] * 3, 0.1, 1.0, dsr_excess=0.99, spa_p=0.01, leakage_clean=True, n_trials=10)
    assert judge(r2).eligible


def test_cpcv_gate_in_registry(tmp_path):
    reg = ModelRegistry(tmp_path, lambda: "t")
    reg.register("m", {}, {"median_path_excess_sharpe": 0.3, "positive_path_fraction": 1.0, "dsr_excess": 0.4, "spa_p": 0.3}, "fp", True)
    rec = reg.evaluate_cpcv_promotion("m", CpcvThresholds())
    assert rec.status == "REJECTED" and rec.activation_allowed is False
    with pytest.raises(PermissionError):
        reg.approve("m", "me", "note")


def test_tree_cpcv_on_noise_is_not_eligible():
    pytest.importorskip("sklearn")
    d = synthetic_market(seed=5, n_symbols=12, n_days=900)
    members = PointInTimeUniverse.from_frame(d.memberships).membership_matrix(d.prices.index, d.prices.columns)
    res = run_tree_cpcv(d.prices, members, kind="hgb", n_groups=4, n_test_groups=2, n_trials=20)
    assert res.leakage_clean and res.n_paths >= 1
    assert not res.eligible  # no true alpha by construction
