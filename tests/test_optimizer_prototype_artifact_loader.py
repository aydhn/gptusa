from usa_signal_bot.portfolio.risk_reporting.optimizer_prototype_artifact_loader import load_optimizer_prototype_artifacts

def test_load_optimizer_prototype_artifacts():
    res = load_optimizer_prototype_artifacts(None)
    assert isinstance(res, dict)
