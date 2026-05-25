
from usa_signal_bot.data_providers.kickoff_gate_ingestion import ingest_provider_kickoff_gate_payload

def test_ingest_provider_kickoff_gate_payload():
    payload = {
        "ready_for_phase106": True,
        "metadata_only": True,
        "allow_broker_execution": False,
        "allow_scraping": False
    }
    res = ingest_provider_kickoff_gate_payload(payload)
    assert res.valid_for_phase106 is True
    assert res.metadata_only is True

    bad_payload = {
        "ready_for_phase106": True,
        "metadata_only": True,
        "allow_broker_execution": True,
        "allow_scraping": False
    }
    res_bad = ingest_provider_kickoff_gate_payload(bad_payload)
    assert res_bad.valid_for_phase106 is False
