from usa_signal_bot.feature_engine.kickoff_gate_ingestion import ingest_feature_factor_kickoff_gate_payload

def test_ingest_feature_factor_kickoff_gate_payload_safe():
    payload = {
        "kickoff_gate": {
            "phase116_ready": True,
            "phase116_scope_allowed": True,
            "activation_allowed": False,
            "broker_execution_enabled": False
        }
    }
    result = ingest_feature_factor_kickoff_gate_payload(payload)
    assert result.valid_for_phase116 is True

def test_ingest_feature_factor_kickoff_gate_payload_unsafe():
    payload = {
        "kickoff_gate": {
            "phase116_ready": True,
            "activation_allowed": True
        }
    }
    result = ingest_feature_factor_kickoff_gate_payload(payload)
    assert result.valid_for_phase116 is False
