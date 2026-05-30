import json
from pathlib import Path

def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def write_text(path, text):
    with open(path, "w") as f:
        f.write(text)

base = Path("tests/fixtures/regime_monitoring")
base.mkdir(parents=True, exist_ok=True)

write_json(base / "sample_regime_context_validation_review.json", {
    "review_id": "rev1",
    "context": {
        "context_id": "ctx1",
        "alignment_ingested": True,
        "alignment_artifacts_loaded": True,
        "validation_specs_ready": True,
        "compatibility_validated": True,
        "conditional_diagnostics_built": True,
        "acceptance_gate_built": True,
        "acceptance_gate_passed": True,
        "ready_for_phase133": True,
        "metadata_only": True,
        "research_data_only": True,
        "activation_allowed": False,
        "strategy_activation_allowed": False,
        "deployment_allowed": False,
        "active_paper_enabled": False,
        "produces_trade_signal": False
    },
    "acceptance_gate": {"ready_for_phase133": True}
})

write_json(base / "sample_regime_context_validation_review_blocked.json", {
    "review_id": "rev2",
    "context": {
        "ready_for_phase133": False,
        "produces_trade_signal": True
    },
    "acceptance_gate": {"ready_for_phase133": False}
})

write_json(base / "sample_compatibility_validation_result.json", {"symbol_results": [{"compatibility_category": "LOW_COMPATIBILITY"}, {"compatibility_category": "HIGH"}]})
write_text(base / "sample_conditional_diagnostics.json", '{"diagnostic_type": "UNCERTAIN_CONTEXT", "action": "WARN"}\n{"diagnostic_type": "DATA_QUALITY_LIMITED", "action": "BLOCK"}\n')
write_text(base / "sample_conditional_diagnostics_profiles.json", '{"profile": "p1"}\n')
write_json(base / "sample_acceptance_gate_pass.json", {"status": "PASSED"})
write_json(base / "sample_acceptance_gate_fail.json", {"status": "FAILED"})
write_json(base / "sample_monitoring_baseline.json", {"baseline_id": "b1", "baseline_version": "v1", "produces_trade_signal": False, "research_metadata_only": True, "baseline_valid": True})
write_json(base / "sample_monitoring_snapshot_current.json", {"snapshot_id": "s1", "produces_trade_signal": False, "research_metadata_only": True, "snapshot_valid": True})
write_json(base / "sample_monitoring_snapshot_previous.json", {"snapshot_id": "s0", "produces_trade_signal": False, "research_metadata_only": True, "snapshot_valid": True})
write_json(base / "sample_drift_observations_expected.json", [{"metric_name": "m1", "drift_severity": "NONE"}])
write_json(base / "sample_context_degradation_expected.json", [{"diagnostic_text": "d1"}])
write_json(base / "sample_invalid_regime_monitoring_payload.json", {"foo": "bar"})

write_text(base / "sample_forbidden_monitoring_columns.csv", "symbol,buy_signal,value\nAAPL,1,100\n")
write_text(base / "sample_unsafe_monitoring_text.txt", "This is an order to buy_signal 100 shares.")
