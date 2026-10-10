import pytest
import json
from usa_signal_bot.release.phase158_integration_ingestion import ingest_full_system_integration_review_payload

def test_ingest_full_system_integration_review_payload():
    payload = {
        "ready_for_phase159": True,
        "research_data_only": True,
        "integration_only": True,
        "dry_run_only": True,
        "live_trading_enabled": False,
    }

    res = ingest_full_system_integration_review_payload(payload)
    assert res.valid_for_phase159 == True
    assert res.ready_for_phase159 == True
    assert res.live_trading_enabled == False
    assert res.investment_advice == False
