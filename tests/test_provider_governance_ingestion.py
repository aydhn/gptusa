import unittest
from usa_signal_bot.provider_freeze.provider_governance_ingestion import ingest_provider_governance_review_payload

class TestProviderGovernanceIngestion(unittest.TestCase):
    def test_ingest_empty_payload(self):
        res = ingest_provider_governance_review_payload({})
        self.assertFalse(res.available)
        self.assertFalse(res.valid_for_phase114)

    def test_ingest_valid_payload(self):
        payload = {
            "review_id": "rev1",
            "context": {
                "context_id": "ctx1",
                "provider_governance_ready": True,
                "provider_expansion_accepted": True,
                "lineage_ready": True,
                "audit_ready": True,
                "metadata_only": True,
                "research_data_only": True,
                "produces_trade_signal": False
            }
        }
        res = ingest_provider_governance_review_payload(payload)
        self.assertTrue(res.available)
        self.assertTrue(res.valid_for_phase114)
