from types import SimpleNamespace as NS

import pytest

from usa_signal_bot.ml_loop.registry import CANDIDATE, ModelRegistry, PromotionThresholds
from usa_signal_bot.ml_loop.retrain_trigger import RetrainPolicy, evaluate_retrain, register_retrain_candidate


def _r(sev, name="m"):
    return NS(severity=sev, metric_name=name)


def test_no_trigger_on_low_drift():
    assert not evaluate_retrain([_r("LOW"), _r("NONE"), _r("MEDIUM")]).triggered


def test_trigger_on_high_and_on_many_medium():
    assert evaluate_retrain([_r("HIGH", "psi")]).triggered
    assert evaluate_retrain([_r("MEDIUM")] * 3).triggered
    assert evaluate_retrain([_r("MEDIUM")], RetrainPolicy(min_severity="MEDIUM")).triggered


def test_candidate_is_never_active_and_cannot_be_approved(tmp_path):
    reg = ModelRegistry(tmp_path, clock=lambda: "2026-01-01T00:00:00Z")
    req = evaluate_retrain([_r("BLOCKING")])
    assert req.activation_allowed is False
    rec = register_retrain_candidate(reg, "retrain-1", req, "fp")
    assert rec.status == CANDIDATE and rec.activation_allowed is False
    assert register_retrain_candidate(reg, "x", evaluate_retrain([_r("LOW")]), "fp") is None
    assert reg.evaluate_promotion("retrain-1", PromotionThresholds()).status == "REJECTED"
    with pytest.raises(PermissionError):
        reg.approve("retrain-1", "me", "note")
    assert reg.get("retrain-1").activation_allowed is False
