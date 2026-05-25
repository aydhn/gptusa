from usa_signal_bot.data_provider_runtime.phase107_models import *
import pytest

def test_provider_abstraction_ingestion_result():
    res = ProviderAbstractionIngestionResult()
    assert res.ingestion_id is not None
    assert res.available is False

def test_validate_provider_abstraction_ingestion_result():
    res = ProviderAbstractionIngestionResult(
        provider_abstraction_ready=True,
        provider_registry_valid=True,
        provider_safety_valid=True,
        metadata_only=True
    )
    # Should pass
    validate_provider_abstraction_ingestion_result(res)

    res.provider_abstraction_ready = False
    with pytest.raises(Exception):
        validate_provider_abstraction_ingestion_result(res)
