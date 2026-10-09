import math

import numpy as np
import pytest

from usa_signal_bot.evidence.stats import (
    deflated_sharpe_ratio,
    expected_max_sharpe,
    pbo_cscv,
    probabilistic_sharpe_ratio,
    trial_sharpe_variance,
)
from usa_signal_bot.ml_loop.cpcv import CombinatorialPurgedCV, assert_cpcv_no_leakage


def test_psr_half_at_benchmark_and_monotone():
    assert probabilistic_sharpe_ratio(0.1, 0.1, 250) == pytest.approx(0.5)
    assert probabilistic_sharpe_ratio(0.2, 0.0, 250) > probabilistic_sharpe_ratio(0.1, 0.0, 250)
    # longer sample => more confident
    assert probabilistic_sharpe_ratio(0.1, 0.0, 1000) > probabilistic_sharpe_ratio(0.1, 0.0, 250)


def test_psr_known_value():
    # SR=0.1, T=101, normal (skew 0, kurt 3): z = 0.1*sqrt(100)/sqrt(1+0.5*0.01) = 1/sqrt(1.005)
    z = 1.0 / math.sqrt(1.005)
    from statistics import NormalDist

    assert probabilistic_sharpe_ratio(0.1, 0.0, 101) == pytest.approx(NormalDist().cdf(z))


def test_expected_max_sharpe_matches_monte_carlo():
    rng = np.random.default_rng(0)
    n, var = 100, 1.0
    mc = rng.standard_normal((20000, n)).max(axis=1).mean()  # ~2.508
    assert expected_max_sharpe(n, 2, var_sr=var) == pytest.approx(mc, abs=0.05)


def test_expected_max_sharpe_depends_on_sample_length_and_trials():
    assert expected_max_sharpe(50, 250) > expected_max_sharpe(50, 2500)  # more data => smaller null max SR
    assert expected_max_sharpe(100, 500) > expected_max_sharpe(10, 500)
    assert expected_max_sharpe(1, 500) == 0.0
    # explicit 1/(T-1) null variance
    assert expected_max_sharpe(50, 251) == pytest.approx(expected_max_sharpe(50, 2, var_sr=1 / 250))


def test_dsr_decreases_with_trials():
    rng = np.random.default_rng(1)
    r = rng.normal(0.0008, 0.01, 1000)
    assert deflated_sharpe_ratio(r, 1) > deflated_sharpe_ratio(r, 10) > deflated_sharpe_ratio(r, 1000)


def test_dsr_noise_is_not_significant_signal_is():
    rng = np.random.default_rng(2)
    noise = rng.normal(0, 0.01, 1250)
    assert deflated_sharpe_ratio(noise, 100) < 0.95
    strong = rng.normal(0.003, 0.01, 1250)
    assert deflated_sharpe_ratio(strong, 100) > 0.99


def test_trial_sharpe_variance():
    rng = np.random.default_rng(3)
    trials = [rng.normal(0, 0.01, 500) for _ in range(30)]
    assert trial_sharpe_variance(trials) == pytest.approx(1 / 499, rel=0.6)


def test_pbo_noise_is_about_half_and_skill_is_low():
    rng = np.random.default_rng(4)
    noise = rng.normal(0, 0.01, (800, 20))
    assert 0.3 <= pbo_cscv(noise, 8).pbo <= 0.7
    skill = rng.normal(0, 0.01, (800, 20))
    skill[:, 0] += 0.01  # genuinely better in every block
    res = pbo_cscv(skill, 8)
    assert res.pbo == 0.0
    assert res.n_combinations == 70


def test_pbo_validation():
    with pytest.raises(ValueError):
        pbo_cscv(np.zeros((100, 1)))
    with pytest.raises(ValueError):
        pbo_cscv(np.zeros((100, 3)), n_blocks=5)


def test_cpcv_counts_and_paths():
    cv = CombinatorialPurgedCV(n_groups=6, n_test_groups=2, horizon=3, embargo=2)
    assert cv.n_splits == 15
    assert cv.n_paths == 5  # C(6,2)*2/6
    splits = list(cv.split(600))
    assert len(splits) == 15
    for train, test, _ in splits:
        assert set(train).isdisjoint(test)
        assert_cpcv_no_leakage(train, test, 3, 2)
    for p in cv.paths():
        assert sorted(g for _, g in p) == list(range(6))  # each group once per path


def test_cpcv_leak_detected():
    with pytest.raises(AssertionError):
        assert_cpcv_no_leakage(np.array([0, 1, 2, 9]), np.array([5, 6]), horizon=3, embargo=0)
