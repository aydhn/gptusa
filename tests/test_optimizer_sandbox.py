import pytest
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerSandboxCandidate, OptimizerPolicy
from usa_signal_bot.portfolio.optimization.optimizer_policy import build_default_optimizer_policy
from usa_signal_bot.portfolio.optimization.equal_baseline_optimizer import build_equal_baseline_optimizer_results, validate_equal_baseline_optimizer_results
from usa_signal_bot.portfolio.optimization.sandbox_weight_normalization import normalize_optimizer_results

def test_equal_baseline_optimizer():
    c1 = OptimizerSandboxCandidate(symbol="AAPL")
    c2 = OptimizerSandboxCandidate(symbol="MSFT")
    policy = build_default_optimizer_policy()

    results = build_equal_baseline_optimizer_results([c1, c2], policy)
    assert len(results) == 2
    assert results[0].sandbox_optimizer_weight == 0.5
    assert results[1].sandbox_optimizer_weight == 0.5

    errs = validate_equal_baseline_optimizer_results(results)
    assert len(errs) == 0

def test_sandbox_weight_normalization():
    c1 = OptimizerSandboxCandidate(symbol="AAPL")
    c2 = OptimizerSandboxCandidate(symbol="MSFT")
    policy = build_default_optimizer_policy()

    results = build_equal_baseline_optimizer_results([c1, c2], policy)
    results[0].sandbox_optimizer_weight = 0.8
    results[1].sandbox_optimizer_weight = 0.2

    norm = normalize_optimizer_results(results, policy)
    assert norm[0].normalized_sandbox_optimizer_weight == 0.8
    assert norm[1].normalized_sandbox_optimizer_weight == 0.2

    # In a real pipeline, cap would trigger here.
