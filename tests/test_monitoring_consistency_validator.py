from usa_signal_bot.regime_classification.freeze_preparation.monitoring_consistency_validator import validate_baseline_snapshot_consistency

def test_validate_baseline_snapshot_consistency():
    errs = validate_baseline_snapshot_consistency(None, None)
    assert len(errs) == 2
    errs = validate_baseline_snapshot_consistency({"a":1}, {"b":2})
    assert len(errs) == 0
