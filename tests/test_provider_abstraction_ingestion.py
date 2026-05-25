from usa_signal_bot.data_provider_runtime.provider_abstraction_ingestion import ingest_provider_abstraction_review_payload
from usa_signal_bot.core.enums import ProviderRuntimeRiskFlag

def test_ingest_provider_abstraction_review_payload():
    payload = {
        "context": {
            "provider_abstraction_ready": True,
            "provider_registry_valid": True,
            "provider_safety_valid": True,
            "metadata_only": True
        }
    }
    res = ingest_provider_abstraction_review_payload(payload)
    assert res.valid_for_phase107 is True
    assert ProviderRuntimeRiskFlag.PROVIDER_ABSTRACTION_INVALID not in res.risk_flags
