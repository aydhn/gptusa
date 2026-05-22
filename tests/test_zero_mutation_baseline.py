from usa_signal_bot.paper_firewall_audit.zero_mutation_baseline import collect_zero_mutation_baseline

def test_zero_mutation_baseline():
    baseline = collect_zero_mutation_baseline({"test": "data"}, "before")
    assert baseline.baseline_type == "before"
    assert baseline.paper_snapshot_hash is not None
